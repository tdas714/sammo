import os


class ProofOfWork():
    def __init_(self, block, target=4):
        self.block = block
        self.target = target

    def Initdata(self, nonce):
        data = [[]]
        dat = []
        
        dat.append(self.block.prevhash)
        dat.append(self.block.HashTransactions())
        dat.append(ToHex(int(nonce)))
        dat.append(ToHex(int(target))))
        
        data.append(dat)
        data.append(bytearray())
        return data

    def run(self):
        nonce = 0
        while True:
            data = self.Initdata(nonce)
            datahash = sha256(data).hexdigest()
            print('\r', datahash)
            if datahash.startswith('0'*self.target):
                break
            else:
                nonce++
        print()
        return nonce, datahash
        
def NewProof(block):
    pow = ProofOfWork(block)
    return pow

