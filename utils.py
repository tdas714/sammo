import os

def serialize(lo):
    arr = []
    for l in lo:
        arr.append(str(l).encode())
    arr = b''.join(arr)
    return arr
    
