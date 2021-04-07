import hashlib
import pickle


class ProofOfWork():
    def __init__(self, block, target = 1):
        self.Block = block
        self.Target = target

    def Initdata(self, nonce, prm):
        dat = []
        dat.append(self.Block.Prevhash)
        dat.append(self.Block.HashTransactions())
        dat.append(nonce.to_bytes(8, 'big'))
        dat.append(prm.difficulty.to_bytes(8, 'big'))
        dat = b''.join(dat)

        return dat
    def run(self, prm):
        nonce = 0
        while True:
            data = self.Initdata(nonce, prm)
            datahash = hashlib.sha256(data).digest()
            print(datahash.hex(), end='\r')
            
            if datahash.hex().startswith(self.Target*'0'):
                break
            else:
                nonce+=1
        print()
        return nonce, datahash

    def validate(self):
        return pickle.loads(self.Block).Hash.hex().startswith('0'*self.Target)


#===========Functions=============

def newProof(block, prm):
    proof = ProofOfWork(block, prm.difficulty)
    return proof

