import pickle
import os
import sys
import paramas as prm

 class Blockchain():
     def __init__(self, lastHash, database)
        self.lastHash = lastHash
        self.database = database

def DbExists(path):
    if os.path.exists(path):
        return True
    return False

def openDatabase(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def ContinueBlockchain(nodeid):
    path = prm.dbPath + nodeid
    if DbExists(path) == False:
        print("No Blockchain Found")
        sys.exit("Create a New one!")
    db = openDatabase(path)
    lasthash = db["lasthash"]
    chain = Blockchain(lasthash, db)
    return chain
        
def InitBlockchain(nodeid, address):
    path = prm.dbPath + nodeid
    if DbExists(path):
        print("Blockchain already Exists")
        sys.exit()
    db = {}
    cbtx = CoinbaseTxn(address, prm.genesisData)
    genesis = Genesis(cbtx)
    print('Genesis Block created!')
    db['db'] = [genesis.hash, genesis.Serialize()]
    db['lasthash'] = genesis.hash
    chain = Blockchain(genesis.hash, db)
    return chain
    
