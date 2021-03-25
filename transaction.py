import sys
import os
import params as prm
import hashlib
import json
from tx import TxInput, TxOutput, NewTxOutput

class Transaction():
    
    def __init__(self, ID, inputs, outputs):
        self.ID = ID
        self.inputs = inputs
        self.outputs = outputs
        
    def get(self):
        return [self.ID, self.inputs, self.outputs]
    
    def serialize(self):
        return b''.join([str(self.ID).encode(), 
                b''.join([x.serialize() for x in self.inputs]), 
                b''.join([x.serialize() for x in self.outputs])])

    #@property
    def Hash(self):
        txCopy = Transaction([], self.inputs, self.outputs)
        
        txhash = hashlib.sha256(txCopy.serialize()).hexdigest()
        
        return txhash
    
    def isCoinbase(self):
        return len(self.inputs) == 1 and len(self.inputs[0].ID) == 0 and self.input[0].out == -1



def CoinbaseTxn(to , data):
    if data == "":
        data = os.urandom(24)
    txin = TxInput('', -1, '', data.encode().hex())
    txout = NewTxOutput(prm.mineReward, to.encode())
    tx = Transaction([], [txin], [txout])
    tx.ID = tx.Hash()
    return tx

if __name__ == '__main__':
    print(CoinbaseTxn("to", "This is data"))
