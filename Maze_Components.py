from PHeap import PHeap

class Vertex:
    def __init__(self, value):
        self.value = value
        self.label = "UNEXPLORED"
        self.distance = 2**60
        self.edges = []
        self.prev = None
        self.heuristic = -1

    def connection(self, w):
        for e in self.edges:
            if e.opposite(self) == w:
                return e

        return None

    def __eq__(self, v):
        try:
            return self.value == v.value
        except AttributeError:
            return False

class Edge:
    def __init__(self, u, v, weight = 0):
        self.ends = (u, v)
        self.label = "UNEXPLORED"
        self.weight = weight
        self.middle = []

    def opposite(self, node):
        if self.ends[0] == node:
            return self.ends[1]
        else:
            return self.ends[0]

class Graph:
    '''
    Class made of vertices and edges. vertices are stored in a dict, and ordered in a Priority Queue
    '''
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.end = None
        self.Heap = PHeap()

    def smallest(self):
        s_v = None
        s_weight = 2**63 + 1
        for k, v in self.vertices.items():
            if(v.distance < s_weight and v.label == "UNEXPLORED"):
                s_v = v
                s_weight = v.distance
        return s_v

    def smallestHeap(self):
        while not self.Heap.isEmpty():
            value = self.Heap.removeMin()
            retval = self.vertices.get(value[1])
            if retval is not None:
                return retval

        return None

    def __str__(self):
        return "Vertices: {}\nEdges: {}".format(len(self.vertices), len(self.edges))