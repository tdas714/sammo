import time
from blockchain.proof import newProof
import pickle
import transactions.merkle as merkle

class Block():
    def __init__(self, timestamp, blockhash, transactions,
                    prevhash, nonce, height):
        self.Timestamp = timestamp
        self.Hash = blockhash
        self.Transactions = transactions
        self.Prevhash = prevhash
        self.Nonce = nonce
        self.Height = height
    
    def __str__(self):
        s = '='*20+'\n'
        s += f'TimeStamp: {self.Timestamp}\n'
        s += f'Block Hash: {self.Hash.hex()}\n'
        for trans in self.Transactions:
            s += '-'*20+'\n'
            s += f'{str(trans)}\n'
        s += f'Previous Hash: {self.Prevhash}\n'
        s += f'Nonce: {self.Nonce}\n'
        s += f'Block Height: {self.Height}'
        return s
    def HashTransactions(self):
        txhashes = []
        for trans in self.Transactions:
            txhashes.append(pickle.dumps(trans))
        tree = merkle.NewMerkleTree(txhashes)
        return tree.RootNode.Data

#==============Fucntions=============
def CreateBlock(txs, prevhash, height, prm):
    block = Block(time.time(), '', txs, prevhash, 0, height)
    
    proof = newProof(block, prm)
    nonce, datahash = proof.run(prm)
    block.Hash = datahash
    block.Nonce = nonce
    return block

def Genesis(cbtx, prm):
    return CreateBlock([cbtx], b'', 0, prm)
