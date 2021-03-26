import sys
import os
import params as prm
import hashlib
import json
from tx import TxInput, TxOutput, NewTxOutput
from ecdsa import SigningKey, SECP256k1

class Transaction():
    
    def __init__(self, ID, inputs, outputs):
        self.ID = ID
        self.inputs = inputs
        self.outputs = outputs
        
    def get(self):
        return [self.ID, self.inputs, self.outputs]
    
    def serialize(self):
        return b''.join([str(self.ID).encode(), 
                b''.join([x.serialize() for x in self.inputs]), 
                b''.join([x.serialize() for x in self.outputs])])

    #@property
    def Hash(self):
        txCopy = Transaction([], self.inputs, self.outputs)
        
        txhash = hashlib.sha256(txCopy.serialize()).hexdigest()
        
        return txhash
    
    def isCoinbase(self):
        return len(self.inputs) == 1 and len(self.inputs[0].ID) == 0 and self.input[0].out == -1

    def sign(self, privKey, prevTXs):
        if self.isCoinbase():
            return 
        for inp in tx.inputs:
            if prevTXs[inp.ID].ID == None:
                print('ERROR: previous transaction is not correct')
        txcopy = self.trimmedCopy()
        for inpid, inp in enumerate(self.inputs):
            prevtx = prevTXs[inp.ID]
            txcopy.inputs[inpid].Sig = ''
            txcopy.inputs[inpid].PubKey = prevtx.outputs[inp.out].PubKeyHash
            sig = privKey.sign(txcopy.serialize())
            
            self.inputs[inpid].Sig = signature
            self.inputs[inpid].PubKey = ''

    def verify(self, prevTXs):
        if self.isCoinbase():
            return
        for inp in tx.inputs:
            if prevTXs[inp.ID].ID == None:
                print('ERROR: previous transaction is not correct')
        txcopy = self.trimmedCopy()
        for inId, inp in self.inputs:
            prevtx = prevTXs[inp.ID]
            txcopy.inputs[inId].Sig = ''
            txcopy.inputs[inId].PubKey = prevtx.outputs[inId].PubKeyHash
            datatoverify = txcopy.serialize()
            
            if inp.PubKey.verify(inp.Sig, datatoverify):
                txcopy.inputs[inId].PubKey = ''
                return True
        return False
    
    def trimmedCopy(self):
        inputs = []
        outputs = []
        for inp in self.inputs:
            inputs.append(TxInput(inp.Id, inp.out, '', ''))
        for out in self.outputs:
            outputs.append(TxOutput(out.value, out.PubKeyHash))
        
        txcopy = Transaction(self.ID, inputs, outputs)
        return txcopy


def CoinbaseTxn(to , data):
    if data == "":
        data = os.urandom(24)
    txin = TxInput('', -1, '', data.encode().hex())
    txout = NewTxOutput(prm.mineReward, to.encode())
    tx = Transaction([], [txin], [txout])
    tx.ID = tx.Hash()
    return tx

if __name__ == '__main__':
    # Test
    txin = TxInput('cbb161f4d69089ee0474d8efc76ff06487fb5b4d3c61767cca5c2df88349424a', 0, '', 'ab112c9e5b9a9e0a7f502ad800fb621bd9727e16bbe8428f9eca2133692b666d1aab2db61a9ed264861b9507a38d790807945f6985aae227e6c8608f10706b5a')
    txout1 = TxOutput(5, '6d87846811e01a0c5393b0ea9066af18d44cd523')
    txout2 = TxOutput(15, 'f341bee2fd9bf74b6441792ac8e8f5cc96eef44c')
    tx = Transaction('bd05b49a14e3124055f29d674c316e2bb0733d4165ecd187643abf933a07f414', [txin], [txout1, txout2])
    print(tx.serialize())
    from ecdsa.util import randrange_from_seed__trytryagain
    def make_key(seed):
        secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
        return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)
    seed = os.urandom(SECP256k1.baselen) # or other starting point
    sk1a = make_key(seed)
    sig = sk1a.sign(tx.serialize())
    print('sig', sig.hex())
    vk = sk1a.verifying_key
    print(vk.verify(sig, tx.serialize()))

