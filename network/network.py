import params as prm
from blockchain import blockchain
import pickle
import socket
import asyncio
import sys
from transactions import transaction, utxo
import time

#================Data Types===========================
class Version():
    def __init__(self, ver, bh, nd):
        self.version = ver
        self.bestHeight = bh
        self.AddrFrom = nd

class GetBlocks():
    def __init__(self, addr):
        self.AddrFrom = addr

class Request():
    def __init__(self, cmd, payload):
        self.Command = cmd
        self.Payload = payload

class Inv():
    def __init__(self, addr, ty, items):
        self.AddrFrom = addr
        self.Type = ty
        self.Items = items

class GetData():
    def __init__(self, addr, kind, ID):
        self.AddrFrom = addr
        self.Type = kind
        self.ID = ID

class Block():
    def __init__(self, addr, block):
        self.AddrFrom = addr
        self.Block = block

class Tx():
    def __init__(self, addr, tx):
        self.AddrFrom = addr
        self.Tx = tx

#=================Send Functions=================================
def sendData(addr, req, knownNodes):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(addr)
            s.sendall(req)
    except ConnectionRefusedError:
        updated = []
        for node in knownNodes:
            if addr != node:
                updated.append(node)


def sendVersion(addr, chain, nodeaddress, knownNodes):
    payload = Version(prm.version, len(chain.Database), nodeaddress)
    req = pickle.dumps(Request('version', payload))
    sendData(addr, req, knownNodes)

def sendGetBlocks(addr, nodeaddress, knownNodes):
    payload = GetBlocks(nodeaddress)
    req = pickle.dumps(Request('getblocks', payload))
    sendData(addr, req, knownNodes)

def sendInv(addr, kind, items, nodeaddress, knownNodes):
    inv = Inv(nodeaddress, kind, items)
    req = pickle.dumps(Request('inv', inv))
    sendData(addr, req, knownNodes)

def sendGetData(addr, kind, idx, nodeaddress, knownNodes):
    payload = GetData(nodeaddress, kind, idx)
    req = pickle.dumps(Request('getdata', payload))
    sendData(addr, req, knownNodes)

def sendBlock(addr, block, nodeaddress, knownNodes):
    data = Block(nodeaddress, block)
    req = pickle.dumps(Request('block', data))
    sendData(addr, req, knownNodes)

def sendTx(addr, tx, nodeaddress, knownNodes):
    data = Tx(nodeaddress, tx)
    print('Send tx data', data)
    req = pickle.dumps(Request('tx', data))
    sendData(addr, req, knownNodes)

#=======================Start Server=============================
async def startServer(nodeid, addr, knownNodes):
    blocksInTransit = []
    memoryPool = {}
    minerAddress = addr
    nodeaddress = ('localhost', int(nodeid))
    chain = blockchain.ContinueBlockchain(nodeid, prm)
    for node in knownNodes:
        if node != nodeaddress:
            sendVersion(node, chain, nodeaddress, knownNodes)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(nodeaddress)
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                reqs = []
                while True:
                    req = conn.recv(4096)
                    if not req : break
                    reqs.append(req)
                req = b''.join(reqs)
                result = await asyncio.gather(handleConnections(req, chain, nodeaddress, blocksInTransit, knownNodes, memoryPool, minerAddress))
                blocksInTransit, chain = result[0]


#===================Handle Functions==============================

async def handleConnections(req, chain, nodeaddress, blocksInTransit, knownNodes, memoryPool, minerAddress):
    req = pickle.loads(req)
    cmd = req.Command
    payload = req.Payload
    print('Received Command : ', cmd, 'from node: ', payload.AddrFrom)
    if cmd == 'block':
        blocksInTransit, chain = handleBlock(payload, chain, nodeaddress, blocksInTransit, knownNodes)
    elif cmd == 'inv':
        blocksInTransit = handleInv(payload, chain, nodeaddress, blocksInTransit, knownNodes)
    elif cmd == "getblocks":
        handleGetBlocks(payload, chain, nodeaddress, knownNodes)
    elif cmd == "getdata":
        handleGetData(payload, chain, nodeaddress, knownNodes)
    elif cmd == "tx":
        handleTx(payload, chain, nodeaddress, knownNodes, memoryPool, minerAddress)
    elif cmd == "version":
        handleVersion(payload, chain, nodeaddress, knownNodes)
    else:
        print("Unknown command")
        sys.exit()
    return blocksInTransit, chain

def handleVersion(payload, chain, nodeaddress, knownNodes):
    localHeight = len(chain.Database)
    otherHeight = payload.bestHeight
    if localHeight < otherHeight:
        
        sendGetBlocks(payload.AddrFrom, nodeaddress, knownNodes)
    elif localHeight > otherHeight:
        
        sendVersion(payload.AddrFrom, chain, nodeaddress, knownNodes)
    
    if not isNodeKnown(payload.AddrFrom, knownNodes):
        knownNodes.append(payload.AddrFrom)
        with open(f'data/kn{nodeaddress[1]}.pkl', 'wb+') as f:
            pickle.dump(knownNodes,f)

def handleGetBlocks(payload, chain, nodeaddress, knownNodes):
    blocks = chain.getBlockHashes(prm)
    sendInv(payload.AddrFrom, 'block', blocks, nodeaddress, knownNodes)

def handleInv(payload, chain, nodeaddress, blocksInTransit, knownNodes):
    print(f'Inventroy Received with {len(payload.Items)} {payload.Type}')
    
    if payload.Type == 'block':
        blocksInTransit = payload.Items
        blockHash = payload.Items[0]
        sendGetData(payload.AddrFrom, 'block', blockHash, nodeaddress, knownNodes)

        newInTrns = []

        for b in blocksInTransit:
            if b != blockHash:
                newInTrns.append(b)
        blocksInTransit = newInTrns
    if payload.Type == 'tx':
        txId = payload.Items[0]
        if memoryPool[txId].ID == '':
            sendGetData(payload.AddrFrom, 'tx', txId, nodeaddress, knownNodes)
    return blocksInTransit

def handleGetData(payload, chain, nodeaddress, knownNodes):
    if payload.Type == 'block':
        block = chain.getBlock(payload.ID)
        sendBlock(payload.AddrFrom, block, nodeaddress, knownNodes)
    elif payload.Type == 'tx':
        txid = payload.ID
        tx = memoryPool[txId]
        sendTx(payload.AddrFrom, tx, nodeaddress, knownNodes)

def handleBlock(payload, chain, nodeaddress, blocksInTransit, knownNodes):
    block = payload.Block
    chain.addBlock(block)

    if len(blocksInTransit) > 0:
        blockHash = blocksInTransit[0]
        sendGetData(payload.AddrFrom, 'block', blockHash, nodeaddress, knownNodes)
        blocksInTransit = blocksInTransit[1:]
    else:
        utxoSet = utxo.UTXOSet(chain)
        utxoSet.reIndex(nodeaddress[1], prm)
    return blocksInTransit, chain

def handleTx(payload, chain, nodeaddress,knownNodes, memoryPool, minerAddress):
    tx = payload.Tx
    memoryPool[tx.ID] = tx
    print(nodeaddress, len(memoryPool))

    if len(memoryPool) >= 1 and len(minerAddress) > 0:
        memoryPool = MineTx(chain, nodeaddress, knownNodes, memoryPool, minerAddress)

#====================Utils=========================

def MineTx(chain, nodeaddress, knownNodes, memoryPool, minerAddress):
    
    utxoSet = utxo.UTXOSet(chain)
    txs = []
    for idx in memoryPool:
        print(idx)
        tx = memoryPool[idx]
        if chain.verifyTransaction(tx, prm):
            txs.append(tx)
    
    if len(txs) == 0:
        print('All Transactions are Invalid!')
        sys.exit()

    cbtx = transaction.CoinbaseTxn(minerAddress, time.time(), prm)
    txs.append(cbtx)

    newBlock = chain.mineBlock(txs, prm)
    utxoSet.update(newBlock, str(nodeaddress[1]), prm)
    
    print('New Block Mined')
    
    for tx in txs:
        try:
            del memoryPool[tx.ID]
        except:
            pass
    for node in knownNodes:
        if node != nodeaddress and newBlock != None:
            sendInv(node, 'block', newBlock.Hash, nodeaddress, knownNodes)

    if len(memoryPool) > 0:
        memoryPool = MineTx(chain, nodeaddress, knownNodes, memoryPool, minerAddress)

    return memoryPool

def isNodeKnown(addr, knownNodes):
    if addr in knownNodes:
        return True
    return False
