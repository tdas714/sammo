from transactions.tx import TxInput, TxOutput, newTxOutput, TxOutputs
import hashlib
import pickle
from wallets import wallet
from ecdsa import SECP256k1, VerifyingKey
import ecdsa
#================Structures========================
class Transaction():
    
    def __init__(self, ID, inputs, outputs):
        self.ID = ID
        self.inputs = inputs
        self.outputs = outputs
    
    def __str__(self):
        s = f'---Transactions: {self.ID}\n'
        for idx, x in enumerate(self.inputs):
            s += f'Input {idx}:\n {str(x)}\n'
        for idx, x in enumerate(self.outputs):
            s += f'Output {idx}:\n {str(x)}\n'
        return s

    def Hash(self):
        txCopy = Transaction('', self.inputs, self.outputs)
        txhash = hashlib.sha256(pickle.dumps(txCopy)).hexdigest()
        return txhash
    
    def isCoinbase(self):
        return len(self.inputs) == 1 and self.inputs[0].ID == '' and self.inputs[0].Out == -1
    
    def trimmedCopy(self):
        inputs = []
        outputs = []
        for inp in self.inputs:
            inputs.append(TxInput(inp.ID, inp.Out, '', ''))
        for out in self.outputs:
            outputs.append(TxOutput(out.Value, out.PubKeyHash))
        
        txcopy = Transaction(self.ID, inputs, outputs)
        return txcopy
    
    def sign(self, privKey, prevtxs):
        for inp in self.inputs:
            if prevtxs[inp.ID].ID == '':
                print('Previous transactions are not valid')
        txcopy = self.trimmedCopy()
        for inId, inp in enumerate(txcopy.inputs):
            prevtx = prevtxs[inp.ID]
            txcopy.inputs[inId].Sig = ''
            txcopy.inputs[inId].PubKey = prevtx.outputs[inp.Out].PubKeyHash
            datatosign = pickle.dumps(txcopy)

            sig = privKey.sign(datatosign)
            self.inputs[inId].Sig = sig.hex()
            txcopy.inputs[inId].PubKey = ''

    def verify(self, prevtxs):
        if self.isCoinbase():
            return True
        txcopy = self.trimmedCopy()
        curve = SECP256k1
        for inId, inp in enumerate(self.inputs):
            prevtx = prevtxs[inp.ID]
            txcopy.inputs[inId].Sig = ''
            txcopy.inputs[inId].PubKey = prevtx.outputs[inp.Out].PubKeyHash
            datatoverify = pickle.dumps(txcopy)
            vk = VerifyingKey.from_string(bytes.fromhex(inp.PubKey), curve = curve, hashfunc=hashlib.sha256)
            try:
                ve = vk.verify(bytes.fromhex(inp.Sig), datatoverify)
                if ve == True:
                    txcopy.inputs[inId].PubKey = ''
                    return True
            except Exception as ex:
                print("verify error: ", ex)
            #\x02\xf7\x07V\xe5\xb3\xc0\xca#8l@\x90C\xa6.\xe3\x02\x98\xe8\xe2\xa9\xc5\xbfMu\x9fU\xbd\xca\xe3\xe7i
            #\x03\x91o\x8b\x98Pj\xeb\xa2\xdb\xce\xa6\xa4\x14\xd7=c\xce \xa9\x86\x1e\x1fVf\xa6j\x8bG\x08\xce\xa8:
        return False

#=================Functions==================
def CoinbaseTxn(to , data, prm):
    print('coinbase to: ', to)
    txin = TxInput('', -1, '', data)
    txout = newTxOutput(prm.mineReward, to)
    tx = Transaction('', [txin], [txout])
    tx.ID = tx.Hash()
    return tx

def newTransaction(w, to, amount, utxo, prm):
    inputs = []
    outputs = []

    pubkeyhash = wallet.publicKeyHash(w.PublicKey)
    acc, validOuts = utxo.findSpendableOutputs(pubkeyhash, amount)
    for txid, outs in validOuts.items():
       txin = TxInput(txid, outs, '', w.PublicKey.hex())
       inputs.append(txin)
    outputs.append(newTxOutput(amount, to))
    if acc > amount:
        outputs.append(newTxOutput(acc-amount, w.Address(prm)))
    tx = Transaction('', inputs, outputs)
    tx.ID = tx.Hash()
    utxo.blockchain.signTransactions(tx, w.PrivateKey, prm)
    return tx
