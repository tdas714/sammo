import ecdsa
import os
from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
from hashlib import sha256
import hashlib
from base58 import b58encode, b58decode

checksumLength = 4
version = b'0x00'

class Wallet():
    def __init__(self, privkey, pubkey):
        self.PrivateKey = privkey
        self.PublicKey = pubkey
    def Address(self):
        pubHash = publicKeyHash(self.PublicKey)
        versionHash = version+pubHash
        checksum = Checksum(versionHash)
        fullHash = versionHash + checksum
        address = b58encode(fullHash)
        return address.decode()


def makeWallet():
    private, public = newKeyPair()
    w = Wallet(private, public)
    return w

def newKeyPair():
    curve = SECP256k1
    secexp = randrange_from_seed__trytryagain(os.urandom(curve.baselen), curve.order)
    private = SigningKey.from_secret_exponent(secexp, curve=curve)

    pub = private.verifying_key

    return private , pub.to_string()

def publicKeyHash(pubKey):
    pubHash = sha256(pubKey).digest()
    pubripeMD = hashlib.new('ripemd160', pubHash).digest()
    return pubHash

def Checksum(payload):
    first = sha256(payload).digest()
    second = sha256(first).digest()
    
    return bytes(list(second)[:checksumLength])

def validateAddress(address):
    pubkeyHash = list(b58decode(address.encode()))
    actualChecksum = pubkeyHash[len(pubkeyHash)-checksumLength:]
    version = pubkeyHash[:4]
    pubkeyHash = pubkeyHash[4:len(pubkeyHash)-checksumLength]
    targetChecksum = Checksum(bytes(version)+bytes(pubkeyHash))
    return bytes(actualChecksum) == targetChecksum

if __name__ == '__main__':
    w = makeWallet()
    addr = w.Address()
    print(validateAddress(addr))
