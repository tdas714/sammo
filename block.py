import json
import time

class Block():
    def __init__(self, timestamp, blockhash, transactions,
                prevhash, nonce, height):
        self.timestamp = timestamp
        self.blockhash = blockhash
        self.transactions = transactions
        self.prevhash = prevhash
        self.nonce = nonce
        self.height = height
    def __repr(self):
        return str(self.__dict__)
    def encode(self):
        return self.__repr__().encode()
    
    def HashTransactions(self):
        txhashes = []
        for trans in self.transactions:
            txhashes.append(trans.encode())
        tree = NewMerkleTree(txhashes)
        return tree.RootNode.Data

def CreateBlock(txs, prevhash, height):
    block = Block(time.time(), bytearray(), txs, prevhash, 0, height)
    pow = NewProof(block)
    nonce, datahash = pow.run()
    block.blockhash = datahash
    block.nonce = nonce
    return block

def Genesis(cbtx):
    return CreateBlock([cbtx], bytearray(), 0)
