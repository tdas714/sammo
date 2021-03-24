import params as prm
import json

class TxInput():
    def __init__(self, ID, out, Sig, PubKey):
        self.ID = ID
        self.out = out
        self.Sig = Sig
        self.PubKey = PubKey
    def __repr__(self):
        return str(self.__dict__)

class TxOutput():
    def __init__(self, value, PubKeyHash):
        self.value = value
        self.PubKeyHash = PubKeyHash
    def __repr__(self):
        return str(self.__dict__)

if __name__ == '__main__':
    txin = TxInput(bytearray(), -1, None, "This is a data")
    print(txin.__repr__().encode())
    txout = TxOutput(20, "to")
    print(txout)
