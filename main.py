import os
import argparse

def no_of_argu(*args):
    return(len(args))

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
    parser.add_argument('--getbalance', '-GB', const=True, nargs='?', type=str2bool, help='get the balance for an address - requires -> address')
    parser.add_argument('--address', type=str, help='address for a wallet specific program')
    parser.add_argument('--createblockchain', '-CB', type=bool, help='Creates a new blockchain - requires -> address')
    parser.add_argument('--printchain', '-P', type=bool, help='Prints the complete blockchain')
    parser.add_argument('--send', '-S', type=bool, help='Sends amount from address to address - requires -> from, to, amount')
    parser.add_argument('--from', '-F', type=str, help='Address from amount to send - requires - send, to, amount')
    parser.add_argument('--to', '-T', type=str, help='Address to send the amount - requires -> from, send, amount')
    parser.add_argument('--amount', '-A', type=int, help='Amount to send - requires -> to, from, amount')
    parser.add_argument('--createwallet', '-CW', type=bool, help='Creates a wallet for the user')
    parser.add_argument('--listaddress', '-L', type=str2bool, const=True, nargs='?', help='List of address created for a wallet')
    parser.add_argument('--reindexutxo', '-R', type=bool, help='RE-Indexing unspent transaction')
    parser.add_argument('--startnode', '-SN', type=bool, help='Starts the network node - requires -> miner')
    parser.add_argument('--miner', '-M', type=str, help='Sets the node as miner requires -> startmnode')

    args = parser.parse_args()
    checkargs(args, parser)
    #================================================

    nodeid = os.environ.get('NODE_ID')


    if args.startnode:
        if args.miner == None:
            print('No miner address found!')
        else:
            wallet.validateAddress(args.miner)
        network.StartServer(nodeid, args.miner)

    if args.R:
        chain = ContinueBlockchain(nodeid)

        utxoSet = UTXOSet(chain)
        utxoSet.reIndex()

        count = utxoSet.countTransactions()
        print("Done! There are %d transactions in the UTXO set.\n", count)
    
    if args.L:
        wallets, _ = wallet.createWallets(nodeid)
        addresses = wallets.getAllAddresses()
        for addr in addresses:
            pritn(addr)
    
    if args.CW:
        wallets, _ = wallet.createWallets(nodeid)
        address = wallets.addWallet(nodeid)
        wallets.saveFile(nodeid)
        print("New address is: %s\n", address)
    
    if args.P:
        chain = ContinueBlockchain(nodeid)

        for block in chain:
            print("Hash: %x\n", block.blockhash)
            print("Prev. hash: %x\n", block.prevhash)
            proof = newProof(block)
            print("PoW: %s\n", proof.validate())
            for tx in block.transactions:
                print(tx)
    
    if args.CW:
        if args.address == None:
            print('No address is given')
        if validateAddress(args.address) == False:
            print('Address is not valid!')
        chain = InitBlockchain(nodeid, args.address)
        utxoSet = UTXOSet(chain)
        utxoSet.reIndex()
        print('Finished')

    if args.GB:
        if args.address == None:
            print('No address is given')
        if validateAddress(args.address) == False:
            print('Address is not valid!')
        chain = InitBlockchain(nodeid, args.address)
        utxoSet = UTXOSet(chain)

        balance = 0
        pubkeyHash = list(b58decode(address.encode()))
        pubkeyHash = pubkeyHash[4:len(pubkeyHash)-4]
        utxos = UTXOSet.findUnspentTransactions(bytes(pubkeyHash))

        for out in utxos:
            balance += out.value
        print("Balance of %s: %d\n", address, balance)

    if args.S:
        if args.F == None:
            print('No sender address is given')
        if args.T == None:
            print('No receiver address is given')
        if args.A == None:
            print('Amount is not given')
        
        if validateAddress(args.F) == False:
            print('Sender address is not valid!')
        if validateAddress(args.T) == False:
            print('Receiver address is not valid!')
        
        chain = InitBlockchain(nodeid, args.address)
        utxoSet = UTXOSet(chain)

        wallets = createWallets(nodeid)
        tx = NewTransaction(wallet, args.T, args.A, utxoSet)
        
        if args.M:
            cbtx = CoinbaseTx(args.F, '')
            txs = [cbtx, tx]
            block = chain.mineblock(txs)
            utxoSet.update(block)
        else:
            network.sendTx(network.knownNodes[0], tx)
            print('Transaction sent')
        print('Success!')



