import json
import time
from proof import NewProof
from merkle import NewMerkleTree

class Block():
    def __init__(self, timestamp, blockhash, transactions,
                prevhash, nonce, height):
        self.timestamp = timestamp
        self.blockhash = blockhash
        self.transactions = transactions
        self.prevhash = prevhash
        self.nonce = nonce
        self.height = height
    def __repr__(self):
        return f'{self.timestamp} {self.blockhash} {self.transactions} {self.prevhash} {self.nonce} {self.height}'
    def encode(self):
        return self.__repr__().encode()
    
    def HashTransactions(self):
        txhashes = []
        for trans in self.transactions:
            txhashes.append(trans.encode())
        tree = NewMerkleTree(txhashes)
        return tree.RootNode.Data

def CreateBlock(txs, prevhash, height):
    block = Block(time.time(), [], txs, prevhash, 0, height)
    print('Block')
    input(block)
    proof = NewProof(block)
    nonce, datahash = proof.run()
    block.blockhash = datahash
    block.nonce = nonce
    return block

def Genesis(cbtx):
    return CreateBlock([cbtx], [], 0)
