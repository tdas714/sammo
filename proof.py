import os
from hashlib import sha256

class ProofOfWork():
    def __init__(self, block, target=4):
        self.block = block
        self.target = target

    def Initdata(self, nonce):
        data = [[]]
        dat = []
        
        dat.append(self.block.prevhash)
        dat.append(self.block.HashTransactions())
        dat.append(ToHex(int(nonce)))
        dat.append(ToHex(int(self.target)))
        input(dat)
        data.append(dat)
        data.append(bytearray())
        return data

    def run(self):
        nonce = 0
        while True:
            data = self.Initdata(nonce)
            input(data)
            datahash = sha256(data).hexdigest()
            print('\r', datahash)
            if datahash.startswith('0'*self.target):
                break
            else:
                nonce+=1
        print()
        return nonce, datahash
        
def NewProof(block):
    proof = ProofOfWork(block)
    return proof

def ToHex(num):
    bytes_big = num.to_bytes(2, 'big')
    return bytes_big
