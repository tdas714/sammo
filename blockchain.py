import pickle
import os
import sys
import params as prm
from transaction import CoinbaseTxn
from block import Genesis, Block


class Blockchain():
    def __init__(self, lastHash, database):
       self.lastHash = lastHash
       self.database = database

    def get(self):
        return [self.lastHash, self.database]
    def addBlock(self, block):
        if block.height == self.database[self.lastHash].height + 1:
            self.database[block.blockhash] = block.encode()
            self.lasthash = block.blockhash
            print(f'Block with hash - {block.blockhash} has been added')
    def getBestHeight(self):
        lbdata = self.database[self.lastHash]
        return lbdata.height
    def getBlock(self, blockhash):
        block = self.database[blockhash].decode()
        return block
    def getBlockHashes(self):
        hashs = []
        for k in self.database:
            hashs.append(k)
        return hashs
    def findTransaction(self, txID):
        for k in self.database:
            for tx in self.database[k].transactions:
                if txID == tx.ID:
                    return tx
        return None
    def mineBlock(self, transactions):
        for tx in transactions:
            if self.varifyTransaction(tx) != True:
                print('Invalid Transactions')
                return False
        lastheight = self.database[self.lasthash].height
        newblock = CreateBlock(transactions, self.lasthash, lastheight+1)
        self.database = {newblock.blockhash : newblock}
       
        return True
    def finndUTXO(self):
        UTXO = {}
        spentTXOs = {}

        for k in self.database:
            block = self.database[k]
            for tx in block.transactions:
                txid = tx.ID
                self.recurse(tx, spentTXOs, UTXO)
                
        return UTXO
    def recurse(self, tx, spentTXOx, UTXO):
        for outidx, out in enumerate(tx.outputs):
            if not spentTXOs[txid]:
                for spentout in spentTXOs[tsid]:
                    if spentout == outidx:
                        self.recurse(tx, spentTXOs, UTXO)
            outs = UTXO[txid]
            outs.outputs.append(out)
            UTXO[txid] = outs
        if tx.isCoinbase() == False:
            for inp in tx.inputs:
                spentTXOs[inp.ID].append(inp.out)
    
    def signTransaction(self, tx, privKey):
        prexTXs = {}
        for inp in tx.inputs:
            prevtx = self.findTransaction(inp.ID)
            if prevtx != None:
                prevTXs[prevtx.ID] = prevtx
        tx.sign(privKey, prevTXs)

    def varifyTransaction(self, tx):
        if tx.isCoinbase():
            return True
        prevTXs = {}
        for inp in tx.inputs:
            prevtx = self.findTransaction(inp.ID)
            if prevtx != None:
                prevTXs[prevtx.ID] = prevtx

        return tx.verify(prevTXs)

def DbExists(path):
    if os.path.exists(path):
        return True
    return False

def openDatabase(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data
def saveDatabase(path, chain):
    with open(path, 'wb+') as f:
        pickle.dump(chain, f)

def ContinueBlockchain(nodeid):
    path = prm.dbPath + nodeid
    if DbExists(path) == False:
        print("No Blockchain Found")
        sys.exit("Create a New one!")
    db = openDatabase(path)
    return db
        
def InitBlockchain(nodeid, address):
    path = prm.dbPath + nodeid
    if DbExists(path):
        print("Blockchain already Exists")
        sys.exit()
    db = {}
    cbtx = CoinbaseTxn(address, prm.genesisData)
    genesis = Genesis(cbtx)
    print('Genesis Block created!')
    db['db'] = {genesis.blockhash : genesis}
    chain = Blockchain(genesis.blockhash, db['db'])
    saveDatabase(path, chain)
    return chain
 
if __name__ == '__main__':
    #InitBlockchain('2000', '14u7fa9s5V8YnueZgmpwWDguRze585B52B')
    chain = ContinueBlockchain('2000')
    #print(chain.findTransaction('a3c3d1567d1d14e061368fb8457bc295bbf6a2309c428a4b07ebd644aaeb5819'))
    print(chain.getBestHeight())
