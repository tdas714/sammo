import pickle
from base58 import b58decode

#===================Structures=========================
# Output structure of transaction
class TxOutput():
    def __init__(self, value, PubKeyHash):
        self.Value = value
        self.PubKeyHash = PubKeyHash
    
    def __str__(self):
        return f'\tvalue: {self.Value}\n\tscript: {self.PubKeyHash}'
    
    def lock(self, addressbytes):
        pubKeyHash = b58decode(addressbytes)
        pubKeyHash = pubKeyHash[1 : len(pubKeyHash)-4]
        self.PubKeyHash = pubKeyHash.hex()
    
    def isLockedWithKey(self, pubkeyhash):
        return self.PubKeyHash == pubkeyhash
# TxOutputs is a structure of TxOutput array
class TxOutputs():
    def __init__(self):
        self.Outputs = []
    
    def __str__(self):
        s = []
        for i, out in enumerate(self.Outputs):
            s.append(f'Output {i}: \n'+ str(out))
        return '\n'.join(s)
    
    def __len__(self):
        return len(self.Outputs)

    def append(self, out):
        self.Outputs.append(out)

# Input structure of transaction
class TxInput():
    def __init__(self, ID, out, Sig, PubKey):
        self.ID = ID
        self.Out = out
        self.Sig = Sig
        self.PubKey = PubKey
    
    def usesKey(self, pubKeyHash):
        lockingHash = wallet.PublicKeyHash(self.PubKey)
        return pubKeyHash == lockingHash

    def __str__(self):
        return f'\tTXID: {self.ID}\n\tOut: {self.Out}\n\tSignature: {self.Sig}\n\tPubKey: {self.PubKey}'

#================Functions=============================

def newTxOutput(value, address):
    txo = TxOutput(value, '')
    txo.lock(address)
    return txo

#================= Testing Purpposes====================
if __name__ == '__main__':
    out = newTxOutput(20, '19ktpBAuwZtoANWgnudhZRHfDoVVPckgzh')
    print(out)
