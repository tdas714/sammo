from hashlib import sha256

class MerkleTree():
    def __init__(self, rootnode):
        self.RootNode

class MerkleNode():
    def __init__(self, left='', right='', data=''):
        self.Left = left
        self.Right = right
        self.Data = data

def NewMerkleNode(left, right, data):
    node = MerkleNode()

    if left==None and right==None:
        datahash = sha256(data.encode()).hexdigest()
        node.Data = datahash
    else:
        prevhashs = left.Data.append(right.Data)
        datahash = sha256(prevhashs.encode()).hexdigest()
        node.Data = datahash

    node.Left = left
    node.Right= right
    return node

def NewMerkleTree(data):
    nodes = []
    for dat in data:
        nodes.append(NewMerkleNode(None, None, dat))

    if len(nodes) == 0:
        print("No merkle nodes found")
        sys.exit()

    for len(nodes) > 1:
        if len(nodes)%2 != 0:
            nodes.append(nodes[len(nodes)-1])

        level = []
        for i in range(len(nodes), 2):
            level.append(NewMerkleNode(nodes[i], nodes[i+1], None))
            
        nodes = level
    tree = MerkleTree(nodes[0])
    return tree

