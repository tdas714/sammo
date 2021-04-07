import os
import pickle
import sys
import wallets.wallet as wallet

#==============Structures=======================
class Wallets():
    def __init__(self, prm):
        self.Wallets = {}
        self.params = prm    
    def addWallet(self):
        w = wallet.makeWallet()
        address = w.Address(self.params).decode()
        self.Wallets[address] = w
        return address
    
    def getAllAddresses(self):
        addrs = []
        for addr in self.Wallets:
            addrs.append(addr)
        return addrs

    def getWallet(self, address):
        return self.Wallets[address]

    def loadFile(self, nodeid):
        walletFile = os.path.join(self.params.dataPath, f'wallet_{nodeid}.pkl')
        if os.path.exists(walletFile):
            with open(walletFile, 'rb') as f:
                data = pickle.load(f)
            self.Wallets = data
            return True
        else:
            return False
        

    def saveFile(self, nodeid):
        walletFile = os.path.join(self.params.dataPath, f'wallet_{nodeid}.pkl')
        with open(walletFile, 'wb+') as f:
            pickle.dump(self.Wallets, f)
        return True

#==============Functions========================

def createWallets(nodeid, prm):
    wallets = Wallets(prm)
    done = wallets.loadFile(nodeid)
    return wallets, done

