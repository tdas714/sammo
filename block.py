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


def CreateBlock(txs, prevhash, height):
    block = Block(time.time(), bytearray(), txs, prevhash, 0, height)

def Genesis(cbtx):

