import os
from hashlib import sha256

class ProofOfWork():
    def __init__(self, block, target=4):
        self.block = block
        self.target = target

    def Initdata(self, nonce):
        dat = []

        dat.append(self.block.prevhash)
        dat.append(self.block.HashTransactions())
        dat.append(ToHex(int(nonce)))
        dat.append(ToHex(int(self.target)))
        dat = ''.join(dat)
        return dat.encode()

    def run(self):
        nonce = 0
        while True:
            data = self.Initdata(nonce)
            datahash = sha256(data).hexdigest()
            print(datahash, end='\r')
            if datahash.startswith('0'*self.target):
                break
            else:
                nonce+=1
        return nonce, datahash
        
def NewProof(block):
    proof = ProofOfWork(block)
    return proof

def ToHex(num):
    bytes_big = num.to_bytes(8, 'big')
    return bytes_big.hex()
