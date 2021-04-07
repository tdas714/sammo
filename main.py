import argparse
import sys
import os
from wallets import wallets, wallet
from blockchain import blockchain, block, proof
import params as prm
from transactions import transaction, tx, utxo
import pickle
from base58 import b58decode
import time
import asyncio
from network import network

#================Functions====================
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def checkargs(args, parser):
    for arg in vars(args):
        if getattr(args, arg) != None:
            return
        else:
            pass
    errorargs(parser)

def errorargs(parser):
    print(parser.print_help())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Sammo Blockchain Command-Line arguments')
    parser.add_argument('--getbalance', '-GB', type=str, help='Get balance of given address. - required Address')
    parser.add_argument('--createblockchain', '-CB', type=str, help='Creates initial blockchain, and mines genesis block - required Address')
    parser.add_argument('--printchain', '-P', const=True, nargs='?', type=str2bool, help='Prints the complete blockchain')
    parser.add_argument('--send', '-S', type=int, help='Sends amount from address to address - requires -> from, to')
    parser.add_argument('--sender', '-F', type=str, help='Address from amount to send - requires - send, to, amount')
    parser.add_argument('--to', '-T', type=str, help='Address to send the amount - requires -> from, send, amount')
    parser.add_argument('--createwallet', '-CW', const=True, nargs='?', type=str2bool, help='Creates a wallet for the user')
    parser.add_argument('--listaddress', '-L', const=True, nargs='?', type=str2bool, help='List of address created for a wallet')
    parser.add_argument('--reindexutxo', '-R', const=True, nargs='?', type=str2bool, help='RE-Indexing unspent transaction')
    parser.add_argument('--startnode', '-SN', type=str, help='Starts node in given address')
    parser.add_argument('--miner', '-M', const=True, nargs='?', type=str2bool, help='Sets the node as miner.')
    
    args = parser.parse_args()
    #===

    if not os.path.exists(prm.dataPath):
        os.mkdir(prm.dataPath)

    checkargs(args, parser)
    nodeid = os.environ.get('NODE_ID')
    
    if os.path.exists(f'data/kn{nodeid}.pkl'):
        with open(f'data/kn{nodeid}.pkl', 'rb') as f:
            knownNodes = pickle.load(f)
    else:
        knownNodes = [('localhost', 2000)]
    
    if nodeid == None:
        print('NODE_ID is not found')
        sys.exit()
    #===List Addresses
    if args.listaddress:
        wallets, done = wallets.createWallets(nodeid, prm)
        if done:
            addresses = wallets.getAllAddresses()
        else:
            print('No Wallet file found!')
            sys.exit()
        for addr in addresses:
            print(addr)
    #===Create Wallet
    if args.createwallet:
        wallets, done = wallets.createWallets(nodeid, prm)
        if not done:
            address = wallets.addWallet()
            wallets.saveFile(nodeid)
            print("New address is: ", address)
        else:
            print('Wallet File already exists!')
            sys.exit()
    #===Create Blockchain
    if args.createblockchain:
        if wallet.validateAddress(args.createblockchain, prm) == False:
            print('Address is not valid!')
            sys.exit()
        chain = blockchain.initBlockchain(nodeid, args.createblockchain, prm)
       
        utxoSet = utxo.UTXOSet(chain)
        utxoSet.reIndex(nodeid, prm)
        print('Finished')
    #====
    if args.printchain:
        chain = blockchain.ContinueBlockchain(nodeid, prm)
        for k in chain.Database:
            if not k.startswith(prm.utxoPrefix):
                block = chain.database[k]
                print(pickle.loads(block))
                prf = proof.newProof(block, prm)
                print("PoW: ", prf.validate())
     #====
    if args.getbalance:
        if wallet.validateAddress(args.getbalance, prm) == False:
            print('Address is not valid!')
            sys.exit()
        chain = blockchain.ContinueBlockchain(nodeid, prm)
        utxoSet = utxo.UTXOSet(chain)
        utxoSet.reIndex(nodeid, prm)
        balance = 0
        pubKeyHash = b58decode(args.getbalance.encode())
        pubkeyHash = pubKeyHash[1:len(pubKeyHash)-prm.checksumLength]
        
        utxos = utxoSet.findUnspentTransactions(pubkeyHash, prm)
        for out in utxos:
            balance += out.Value
        print(f"Balance of {args.getbalance} is {balance}")
    #====
    if args.send:
        if args.sender == None:
            print('No sender address is given')
            sys.exit()
        if args.to == None:
            print('No receiver address is given')
            sys.exit()

        if wallet.validateAddress(args.sender, prm) == False:
            print('Sender address is not valid!')
            sys.exit()
        if wallet.validateAddress(args.to, prm) == False:
            print('Receiver address is not valid!')
            sys.exit()
        
        chain = blockchain.ContinueBlockchain(nodeid, prm)
        utxoSet = utxo.UTXOSet(chain)
        ws, done = wallets.createWallets(nodeid, prm)
        if done:
            wallet = ws.getWallet(args.sender)
        else:
            print('Wallet File does not exists! Create One!')
            sys.exit()
        
        tx = transaction.newTransaction(wallet, args.to, args.send, utxoSet, prm)
        if args.miner:
            cbtx = transaction.CoinbaseTxn(args.sender, time.time(), prm)
            txs = [cbtx, tx]

            block = chain.mineBlock(txs, prm)
            if block != None:
                utxoSet.update(block, nodeid, prm)
        else:
            for node in knownNodes:
                if node != ('localhost', nodeid):
                    network.sendTx(node, tx, ('localhost', nodeid), knownNodes)
            print('Transaction sent')
        print('Success!')
    #=====
    if args.startnode:
        if not wallet.validateAddress(args.startnode, prm):
            print('Address is not valid')
            system.exit()
        asyncio.run(network.startServer(nodeid, args.startnode, knownNodes))
