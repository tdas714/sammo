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
        
    def __repr__(self):
        return f'{self.ID} {self.inputs} {self.outputs}'
    def encode(self):
        return self.__repr__().encode()
    #@property
    def Hash(self):
        txCopy = Transaction(bytearray(), self.inputs, self.outputs)
        txhash = hashlib.sha256(txCopy.encode()).hexdigest()
        
        return txhash



def CoinbaseTxn(to , data):
    if data == "":
        data = os.urandom(24)
    txin = TxInput([], -1, [], data.encode().hex())
    txout = NewTxOutput(prm.mineReward, to.encode())
    tx = Transaction(bytearray(), [txin], [txout])
    tx.ID = tx.Hash()
    return tx

if __name__ == '__main__':
    print(CoinbaseTxn("to", "This is data"))
