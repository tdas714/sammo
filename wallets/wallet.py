import ecdsa
import os
from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
from hashlib import sha256
import hashlib
from base58 import b58encode, b58decode

#================Sturctures==================
class Wallet():
    def __init__(self, privKey, pubKey):
        self.PrivateKey = privKey
        self.PublicKey = pubKey

    def Address(self, prm):
        pubHash = publicKeyHash(self.PublicKey)
        verHash = prm.version+pubHash
        checksum = Checksum(verHash, prm)
        fullHash = verHash+checksum
        address = b58encode(fullHash)
        return address


#=================Functions=====================

def newKeyPair():
    curve = SECP256k1
    secexp = randrange_from_seed__trytryagain(os.urandom(curve.baselen), curve.order)
    private = SigningKey.from_secret_exponent(secexp, curve=curve, hashfunc=sha256)
    
    pub = private.get_verifying_key()
    return private, pub.to_string()

def makeWallet():
    priv, pub = newKeyPair()
    w = Wallet(priv, pub)
    return w

def publicKeyHash(pubKey):
    pubHash = sha256(pubKey).digest()
    pubripeMD = hashlib.new('ripemd160', pubHash).digest()
    return pubripeMD

def Checksum(payload, prm):
    first = sha256(payload).digest()
    second = sha256(first).digest()
    return bytes(list(second)[:prm.checksumLength])

def validateAddress(address, prm):
    pubkeyHash = b58decode(address.encode())
    actualChecksum = pubkeyHash[len(pubkeyHash)-prm.checksumLength:]
    version = pubkeyHash[0]
    pubkeyHash = pubkeyHash[1:len(pubkeyHash)-prm.checksumLength]
    targetChecksum = Checksum(version.to_bytes(1, 'big')+pubkeyHash, prm)
    return bytes(actualChecksum) == targetChecksum

