import params as prm
import json
from base58 import b58decode
from utils import serialize

class TxInput():
    
    def __init__(self, ID, out, Sig, PubKey):
        self.ID = ID
        self.out = out
        self.Sig = Sig
        self.PubKey = PubKey
    
    def get(self):
        return [self.ID, self.out, self.Sig, self.PubKey]
    
    def serialize(self):
        return serialize(self.get())

class TxOutput():
    
    def __init__(self, value, PubKeyHash):
        self.value = value
        self.PubKeyHash = PubKeyHash
    
    def get(self):
        return [self.value, self.PubKeyHash]
    
    def serialize(self):
        return serialize(self.get())
    
    def Lock(self, address):
        pubkeyhash = b58decode(address)
        pubkeyhash = pubkeyhash[1: len(pubkeyhash) - 4]
        self.PubKeyHash = pubkeyhash.hex()

def NewTxOutput(value, address):
    txo = TxOutput(value, [])
    txo.Lock(address)
    return txo



if __name__ == '__main__':
    txin = TxInput(bytearray(), -1, None, "This is a data")
    print(txin.__repr__().encode())
    txout = TxOutput(20, "to")
    print(txout)

