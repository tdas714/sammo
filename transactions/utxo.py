import params as prm
import blockchain
import pickle
from blockchain import blockchain
from transactions.tx import TxOutputs

class UTXOSet():
    def __init__(self, blch):
        self.blockchain = blch

    def reIndex(self, nid, prm):
        db  = self.blockchain.Database
        self.deleteByPrefix(prm.utxoPrefix)
        utxo = self.blockchain.findUTXO(prm)
        
        for txid, outs in utxo.items():
            key = txid.encode()
            key = prm.utxoPrefix+key
            db[key] = pickle.dumps(outs)

        self.blockchain.database = db
        blockchain.saveDatabase(prm.dataPath+f'blockchain_{str(nid)}', self.blockchain)

    def deleteByPrefix(self, prefix):
        keys = []
        for txn in self.blockchain.Database:
            if txn.startswith(prm.utxoPrefix):
                    keys.append(txn)
        for k in keys:
            del self.blockchain.Database[k]
    
    def findUnspentTransactions(self, pubkeyhash, prm):
        utxo = []
        for txn in self.blockchain.Database:
            if txn.startswith(prm.utxoPrefix):
                outs = pickle.loads(self.blockchain.Database[txn])
                for out in outs:
                    if out.isLockedWithKey(pubkeyhash.hex()):
                        utxo.append(out)
        return utxo

    def findSpendableOutputs(self, pubkeyHash, amount):
        unspentOuts = {}
        accumulated = 0
        db = self.blockchain.database
        for k in db:
            if k.startswith(prm.utxoPrefix):
                outs = pickle.loads(db[k])
                key = k.strip(prm.utxoPrefix).decode()
                for outID, out in enumerate(outs):
                    if out.isLockedWithKey(pubkeyHash.hex()) and accumulated < amount:
                        accumulated += out.Value
                        unspentOuts[key] = outID
        return accumulated, unspentOuts
    
    def update(self, block, nodid, prm):
        db  = self.blockchain.Database

        for txn in block.Transactions:

            if not txn.isCoinbase():

                for inp in txn.inputs:
                    updatedouts = []

                    inId = prm.utxoPrefix+inp.ID.encode()
                    outs = pickle.loads(db[inId])
                    for outId, out in enumerate(outs):
                        if outId != inp.Out:
                            updatedouts.append(out)

                    if len(updatedouts) == 0:
                        del db[inId]
                    else:
                        db[inId] = pickle.dumps(updatedouts)

            newoutputs = []
            for out in txn.outputs:
                newoutputs.append(out)
            txId = prm.utxoPrefix+txn.ID.encode()
            db[txId] = pickle.dumps(newoutputs)
        
        self.blockchain.Database = db
        blockchain.saveDatabase(prm.dataPath+f'blockchain_{str(nodid)}', self.blockchain)




