import os
from transactions import transaction
from blockchain.block import Genesis, CreateBlock
import pickle
import sys
#=================Structures=======================
class Blockchain():
    def __init__(self, lh, db):
        self.Lasthash = lh
        self.Database = db
    def findUTXO(self, prm):
        UTXO = {}
        spentTXOs = {}

        for k in reversed(self.Database):
            if not k.startswith(prm.utxoPrefix):
                block = pickle.loads(self.Database[k])
                for tx in block.Transactions:
                    spentTXOs, UTXO = self.recurse(tx, spentTXOs, UTXO)
        return UTXO
    def recurse(self, tx, spentTXOs, UTXO):
        len_outs = len(tx.outputs)
        for outidx, out in enumerate(tx.outputs):
            if tx.ID in spentTXOs:
                spentout = spentTXOs[tx.ID]
                if spentout == outidx:
                    continue
            if tx.ID in UTXO:
                outs = UTXO[tx.ID]
            else:
                outs = []

            outs.append(out)
            UTXO[tx.ID] = outs
        if tx.isCoinbase() == False:
            for inp in tx.inputs:
                spentTXOs[inp.ID] = inp.Out
        return spentTXOs, UTXO

    def findTransaction(self, ID, prm):
        for k in self.Database:
            if not k.startswith(prm.utxoPrefix):
                block = pickle.loads(self.Database[k])
                
                for tx in block.Transactions:
                    if tx.ID == ID:
                        return tx

    def signTransactions(self, tx, privKey, prm):
        prevTxs = {}

        for inp in tx.inputs:
            prevTx = self.findTransaction(inp.ID, prm)
            prevTxs[prevTx.ID] = prevTx
        
        tx.sign(privKey, prevTxs)
    
    def verifyTransaction(self, tx, prm):
        if tx.isCoinbase():
            return True

        prevtxs = {}
        for inp in tx.inputs:
            prevtx = self.findTransaction(inp.ID, prm)
            prevtxs[prevtx.ID] = prevtx
        return tx.verify(prevtxs)

    def mineBlock(self, txs, prm):
        for tx in txs:
            if self.verifyTransaction(tx, prm) == False:
               print('Invalid Transactions')
               sys.exit()
        
        lastheight = pickle.loads(self.Database[self.Lasthash]).Height
        newblock = CreateBlock(txs, self.Lasthash, lastheight+1, prm)
        
        self.Database[newblock.Hash] = pickle.dumps(newblock)
        self.Lasthash = newblock.Hash
        return newblock
    
    def getBlockHashes(self, prm):
        blocks = []
        for txn in self.Database:
            if not txn.startswith(prm.utxoPrefix):
                blocks.append(pickle.loads(self.Database[txn]).Hash)
        return blocks

    def getBlock(self, blockhash):
        if blockhash in self.Database:
            block = pickle.loads(self.Database[blockhash])
        else:
            print("No block found")
            block = None
        return block

    def addBlock(self, block):
        self.Database[block.Hash] = pickle.dumps(block)
        lastblock = self.Database[self.Lasthash]
        lastheight = pickle.loads(lastblock).Height
        if block.Height > lastheight:
            self.Lasthash = block.Hash


#==============functions==================

def initBlockchain(nodeid, address, prm):
    path = prm.dataPath + nodeid
    if os.path.exists(path):
        print("Blockchain already Exists")
        sys.exit()
    db = {}
    cbtx = transaction.CoinbaseTxn(address, prm.genesisData, prm)
    genesis = Genesis(cbtx, prm)
    print('Genesis Block created!')
    db[genesis.Hash] = pickle.dumps(genesis)
    chain = Blockchain(genesis.Hash, db)
    saveDatabase(prm.dataPath+f'blockchain_gen', chain)
    return chain

def ContinueBlockchain(nodeid, prm):
    path = prm.dataPath + f'blockchain_{nodeid}'
    if os.path.exists(path):
        db = openDatabase(path)
    else:
        db = openDatabase(prm.dataPath+'blockchain_gen')
    return db

def openDatabase(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def saveDatabase(path, chain):
    with open(path, 'wb+') as f:
        pickle.dump(chain, f)


