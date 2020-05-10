# src/huffman.py


class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s-%s' % (self.left, self.right)


def huffmanCodeTree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffmanCodeTree(l, True, binString + '0'))
    d.update(huffmanCodeTree(r, False, binString + '1'))
    return d

def huffmanDecode(data,tree):
    rev = {}
    for v,k in tree.items():
        rev[k] = v
    start_idx = 0
    end_idx = 1
    max_idx = len(data)
    decode = ''
    while start_idx != max_idx:
        if data[start_idx : end_idx] in rev:
            decode += rev[data[start_idx : end_idx]] + " "
            start_idx = end_idx
        end_idx += 1

    return decode
