import numpy as np
from PIL import Image
from Maze_Components import *
from Algorithm import *

class Maze:
    '''
    A Maze class that encapsulates all of the Maze solving algorithms
    Takes png images of mazes, black = walls, white = path, with entrences at the top and bottom

    Calling maze.Solve(ALGORITHM = alg) will solve the algorithm

    The preprocessor will create a simplified version of the maze in memory, using fewer nodes. This speeds up the creation
    of the graph and the solving of the algorithm.

    Algorithms currently implemented: BFS, DFS, Dijkstra, A*
    '''
    def __init__(self, filename, PREPROCESSING = True, CULLING = True):
        '''
        Takes an image, converts in into an RGB image, load into a numpy array, and turn the maze into a Graph
        This is done as a 1 pixel = 1 node (slow, memory inefficient) or as a smart one-pass procfessor (fast, memory efficient)

        The CULLING parameter will eliminate all nodes of degree 2, they just take processing time.AStar
        '''

        self.filename = filename
        self.img = Image.open(r"Mazes/{}.png".format(filename)).convert("RGB")
        self.img_load = self.img.load()
        self.G = Graph()
        if PREPROCESSING:
            self.root = self.CreateGraphFast(self.G, self.img, self.img_load)
        else:
            self.root = self.CreateGraphSlow(self.G, self.img, self.img_load)

        if CULLING:
            self.CullGraph(self.G)

        self.root.distance = 0

    def Solve(self, ALGORITHM = "ASTAR", MARK = False):
        '''
        Calls the solve algorithms that solve the maze. If MARK is True, then show all the nodes that were checked
        on the initial image in purple

        If the given String is not an algorithm, raise a ValueError
        '''
        alg = None
        if ALGORITHM not in ["ASTAR", "DIJKSTRA", "BFS", "DFS", "LEFT"]:
            raise ValueError("The input algorithm is invalid.")
        if ALGORITHM == "ASTAR":
            alg = AStar(self.img_load, MARK)
        elif ALGORITHM == "DIJKSTRA":
            alg = Dijkstra(self.img_load, MARK)
        elif ALGORITHM == "BFS":
            alg = BFS(self.img_load, MARK)
        elif ALGORITHM == "DFS":
            alg = DFS(self.img_load, MARK)
        elif ALGORITHM == "LEFT":
            raise NotImplementedError("This function is not implemented yet...")

        return alg.Solve(self.G, self.root)



    def CreateGraphFast(self, G, img, img_load):
        '''
        A one-pass pre-processor. Doesn't make any nodes in memory of passages, just corners and junctions. This takes equal
        Time but takes less memory and less time to solve

        Input: A Graph G, and Image img, and the loaded image, img_load
        output: The root node

        '''
        first = False
        arr = np.array([[round(img_load[y,x][1]/255) for y in range(img.size[0])] for x in range(img.size[1])])
 
        print("Loaded,Looping!")
        root, first = None, None
        #visited = 2
        len1 = len(arr)
        len2 = len(arr[0])
        for i in range(len1):
            for j in range(len2):
                #if path:
                
                if arr[i][j] == 1:
                    neighbors = []

                    #if start of maze
                    if not first:
                        first = True
                        root = Vertex("{} {}".format(i, j))
                        G.vertices[root.value] = root
                        G.Heap.insert((root.distance, root.value))
                        arr[i][j] = 2 #2 = NODE
                    elif i != len1-1 and j != len2-1:
                        #straight Horizontal
                        if (arr[i][j-1] != 0 and arr[i][j+1] != 0 and arr[i-1][j] == 0 and arr[i+1][j] == 0):
                            arr[i][j] = 3 #3 = PATH

                        #straight Vertical
                        elif (arr[i-1][j] != 0 and arr[i+1][j] != 0) and (arr[i][j+1] == 0 and arr[i][j-1] == 0):
                            arr[i][j] = 3 #3 = PATH
                        #turn or junction
                        else:
                            newNode = Vertex("{} {}".format(i, j))
                            G.vertices[newNode.value] = newNode
                            G.Heap.insert((newNode.distance, newNode.value))
                            arr[i][j] = 2
                            #while paths nearby, cull em
                            if arr[i-1][j] == 3 or arr[i-1][j] == 2:
                                _i, _j, weight = i, j, 1
                                while arr[_i-1][_j] == 3:
                                    _i -= 1
                                    neighbors.append(Vertex("{} {}".format(_i, _j)))
                                    weight += 1
                                    arr[_i][_j] = 2
                                
                                endNode = G.vertices["{} {}".format(_i-1, _j)]
                                edge = Edge(newNode, endNode, weight)
                                edge.middle = neighbors
                                newNode.edges.append(edge)
                                endNode.edges.append(edge)
                            neighbors = []
                            if arr[i][j-1] == 3 or arr[i][j-1] == 2:
                                _i, _j, weight = i, j, 1
                                while arr[_i][_j -1] == 3:
                                    _j -= 1
                                    neighbors.append(Vertex("{} {}".format(_i, _j)))
                                    weight += 1
                                    arr[_i][_j] = 2

                                endNode = G.vertices["{} {}".format(_i, _j-1)]
                                edge = Edge(newNode, endNode, weight)
                                edge.middle = neighbors
                                newNode.edges.append(edge)
                                endNode.edges.append(edge)

                    elif i == len1-1:
                        newNode = Vertex("{} {}".format(i, j))
                        _i, _j, weight = i, j, 1
                        middles = []
                        if arr[i-1][j] < 2:
                            continue
                        elif arr[i-1][j] == 3 or arr[i-1][j] == 2:
                            while (arr[_i-1][_j] == 3):
                                _i -= 1
                                weight += 1
                                middles.append(Vertex("{} {}".format(_i, _j)))
                                arr[_i][_j] = 2

                            endNode = G.vertices["{} {}".format(_i-1, _j)]
                            edge = Edge(newNode, endNode, weight)
                            edge.middle = middles
                            newNode.edges.append(edge)
                            endNode.edges.append(edge)
                            G.vertices[newNode.value] = newNode
                            G.Heap.insert((newNode.distance, newNode.value))
                            arr[i][j] = 2
                        G.end = newNode
                        return root

        return root

    def CreateGraphSlow(self, G, img, img_load):
        '''
        Takes an np.array and creates a Graph with a node at each path pixel, and edges to their
        path neighbours.

        Input: A Graph G, the image, and the loaded img
        Output: The start node
        '''
        arr = np.array([[round(img_load[y,x][1]/255) for y in range(img.size[0])] for x in range(img.size[1])])
        Garr = np.array([[None for i in range(img.size[0])] for j in range(img.size[1])])
        root, first = None, None
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i][j] == 1:
                    if not first:
                        root = Vertex("{} {}".format(i, j))
                        Garr[i][j] = root
                        G.vertices[root.value] = root
                        G.Heap.insert((root.distance, root.value))
                        first = True
                    else:
                        newNode = Vertex("{} {}".format(i, j))
                        if(Garr[i-1][j] != None):
                            tempNode = Garr[i-1][j]
                            edge = Edge(newNode, tempNode,1)
                            G.edges.append(edge)
                            newNode.edges.append(edge)
                            tempNode.edges.append(edge)
                        if(Garr[i][j-1] != None):
                            tempNode = Garr[i][j-1]
                            edge = Edge(newNode, tempNode, 1)
                            G.edges.append(edge)
                            newNode.edges.append(edge)
                            tempNode.edges.append(edge)
                        Garr[i][j] = newNode
                        G.vertices[newNode.value] = newNode
                        G.Heap.insert((newNode.distance, newNode.value))
                        #G.vertices.append(newNode)
                    if i == len(arr)-1:
                        G.end = G.vertices["{} {}".format(i,j)]
        return root

    def CullGraph(self, G):
        '''
        Removes all Nodes in the graph with only 2 vertices to optimize search algoithms

        Input: a Graph G
        '''
        repeat = True
        while repeat:
            repeat = False
            ToCull = []
            for k,v in G.vertices.items():
                if(len(v.edges) == 2 and v != G.end):
                    repeat = True
                    e0 = v.edges[0]
                    e1 = v.edges[1]
                    v0 = e0.opposite(v)
                    v1 = e1.opposite(v)
                    v0.edges.remove(e0)
                    v1.edges.remove(e1)
                    new_e = Edge(v0, v1, e0.weight + e1.weight)
                    for me in e0.middle:
                        new_e.middle.append(me)
                    for me in e1.middle:
                        new_e.middle.append(me)
                    new_e.middle.append(v)       
                    v0.edges.append(new_e)
                    v1.edges.append(new_e)
                    ToCull.append(v.value)
            for val in ToCull:
                G.vertices.pop(val, None)

    def ColorImage(self, out=None):
        '''
        Colors the image path found from Green -> Yellow -> Red

        Input: a Graph G
        '''
        last = self.G.end
        max_dist = 0
        while(last != None):
            max_dist+=1
            next_last = last.prev
            if next_last != None:
                edge = last.connection(next_last)
                max_dist+=len(edge.middle)
            last = next_last

        last = self.G.end
        last.distance = max_dist
        max_color = last.distance
        i = last.distance
        delta_i = 0
        red, green, blue = 255, 0 , 0
        while(last != None):

            if i < max_color / 2:
                red = red - ( round(delta_i * 255/max_color))
            else:
                green = green + (round(delta_i * 255/max_color))
            blue = 0
            lst = last.value.split()
            i = last.distance
            self.img_load[int(lst[1]),int(lst[0])] = (red, green, blue)
            delta_i = 2
            conn = last.connection(last.prev)
            if conn is not None:
                for m in conn.middle:
                    lst = m.value.split()
                    self.img_load[int(lst[1]),int(lst[0])] = (red, green, blue)
                    delta_i += 2
            last = last.prev

        if(self.img.size[0] < 1000):
            self.img = self.img.resize((1000, 1000))

        if out != None:
            self.img.save(out)

    
