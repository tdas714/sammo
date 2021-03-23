import os


class TxOutput():
    def __init__(self, value, PubKeyHash):
        self.value = value
        self.PubKeyHash = PubKeyHash

class TxInput():
    def __init__(self, ID, out, Signature, PubKey):
        self.ID = ID
        self.out = out
        self.Signature = Signature
        self.PubKey = PubKey

