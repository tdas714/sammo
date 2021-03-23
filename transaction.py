import sys
import os
import params as prm
import hashlib

class Transaction():
    def __init__(self, ID, inputs, outputs):
        self.ID = ID
        self.inputs = inputs
        self.outputs = outputs
    
    @property
    def Hash(self):
        txCopy = Transaction(bytearray(), self.inputs, self.outputs)
        txhash = hashlib.sha256(txCpoy.Serialize()).hexdigest()
        return txhash



def CoinbaseTxn(to , data):
    if data = "":
        data = os.urandom(24)
    txin = TxInput(bytearray(), -1, None, data)
    txout = TxOutput(prm.mineReward, to)

    tx = Transaction(None, [txin], [txout])
    txID = tx.Hash()
    return tx

