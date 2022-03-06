import random
class Algorithm:
    '''
    Super class for algorithms

    Just put the solve methods in for each, put an Algorithm object in Maze, have Maze.solve() call Algorithm.solve()
    Then, Maze is an interface. Takes in > filename and algorithm object, outputs image that is saved.
    '''
    def __init__(self, img_load, MARK):
        self.MARK = MARK
        self.img_load = img_load

    def Solve(self, G, v, MARK):
        raise NotImplementedError #Only call on subclasses

    def EnsureGraphLabelling(self, G, v):
        '''
        Resets all labels and weights of Nodes, resets root distance to 0

        Input: A Grapg G, the root Node v
        '''
        for vert in G.vertices.values():
            vert.label = "UNEXPLORED"
            vert.weight = 2**63 + 1
            for e in vert.edges:
                e.label = "UNEXPLORED"

        v.distance = 0

    def MarkNodes(self, v, w, edge):
        '''
        Marks the image with nodes that were considered in Purple. Used by all algorithms

        Input: a Node v, a Node w, the Edge between them edge
        '''
        v_x, v_y = map(int, v.value.split())
        self.img_load[v_y, v_x] = (255, 0, 255) 
        w_x, w_y = map(int, w.value.split())
        self.img_load[w_y, w_x] = (255, 0, 255)
        for middleVertex in edge.middle:
            m_x, m_y = map(int, middleVertex.value.split())
            self.img_load[m_y, m_x] = (255, 0, 255)  

class Dijkstra(Algorithm):
    def __init__(self, img_load, mark):
        Algorithm.__init__(self, img_load, mark)

    def Solve(self, G, v):
        '''
        Dijkstra Shortest Path through the maze. Slower, but guarentees a shortest path

        Input: a Graph G, start node v
        Output: number of nodes the algorithm explored
        '''
        self.EnsureGraphLabelling(G, v)
        count = 0 
        while(v != None and v != G.end):
            count+=1
            v.label = "VISITED"
            for edge in v.edges:
                w = edge.opposite(v)
                if(w.label != "VISITED" and w.distance > v.distance + edge.weight):
                    w.distance = v.distance + edge.weight
                    G.Heap.changeLocator(w.distance, w.value)
                    #G.Heap.insert((w.distance, w.value))
                    w.prev = v
                    if self.MARK:
                        self.MarkNodes(v, w, edge)

            v = G.smallestHeap()
        return count

class BFS(Algorithm):
    def __init__(self, img_load, mark):
        Algorithm.__init__(self, img_load, mark)

    def Solve(self, G, v):
        '''
        Breadth First Search through the maze. Finds shortest route, but slowly

        Input: a Graph G, start node v
        Output: number of nodes the algorithm explored
        '''
        self.EnsureGraphLabelling(G, v)
        S = [v]
        count = 0 
        distance = 0
        while(len(S) > 0):
            v = S.pop()
            count+=1
            #G.Heap.insert((count, v.value))

            v.label = "VISITED"
            distance = v.distance
            for edge in v.edges:
                w = edge.opposite(v)
                if w.label == "UNEXPLORED":
                    distance_temp = distance + edge.weight
                    w.label = "CONSIDERING"
                    S.insert(0, w)
                    w.distance = distance_temp
                    w.prev = v
                    if self.MARK:
                        self.MarkNodes(v, w, edge)
                if w == G.end:
                    w.prev = v
                    return count
            #v = G.smallestHeap()
        return count

class DFS(Algorithm):
    def __init__(self, img_load, mark):
        Algorithm.__init__(self, img_load, mark)
        
    def Solve(self, G, v):
        '''
        Depth First Search through the maze. Fast algorithm, but not necessarily shortest path.

        Input: a Graph G, start node v
        Output: number of nodes the algorithm explored
        '''
        self.EnsureGraphLabelling(G, v)
        S = [v]
        count = 0
        distance = 0 
        while(len(S) > 0):
            v = S.pop()
            count+=1
            v.label = "VISITED"
            random.shuffle(v.edges)
            distance = v.distance
            for edge in v.edges:
                w = edge.opposite(v)
                distance_temp = distance + edge.weight
                if w.label == "UNEXPLORED":

                    w.label = "CONSIDERING"
                    S.append(w)
                    w.distance = distance_temp
                    w.prev = v
                    if self.MARK:
                        self.MarkNodes(v, w, edge)

                if w == G.end:
                    w.prev = v
                    return count
        return count

class AStar(Algorithm):
    def __init__(self, img_load, mark):
        Algorithm.__init__(self, img_load, mark)

    def Solve(self, G, v):
        '''
        A* is essentially a Dijkstra algorithm, but will priritize downward movements instead of lateral ones
        A* will give the same result as Dijkstra, but hopefully faster

        Input: a Graph G, start node v
        Output: G is labelled, number of nodes the solution explored
        '''
        HEURISTIC_MULT = 1 #Should give optimal path when 1
        self.EnsureGraphLabelling(G, v)
        v_i, v_j = map(int, v.value.split())
        end_i, end_j = map(int, G.end.value.split())
        v.heuristic = HEURISTIC_MULT * ((abs(v_i - end_i)) + (abs(v_j - end_j)))
        count = 0
        while(v != None and v != G.end):
            count += 1
            v.label = "VISITED"
            for edge in v.edges:
                w = edge.opposite(v)
                node_i, node_j = map(int, w.value.split())
                if w.heuristic == -1:
                    #distFromEnd = math.ceil(((node_i - end_i)**2 + (node_j - end_j)**2) ** 0.5)
                    distFromEnd = HEURISTIC_MULT * ((abs(node_i - end_i)) + (abs(node_j - end_j)))
                    w.heuristic = distFromEnd
                if(w.label != "VISITED" and w.distance> v.distance + edge.weight ):
                    w.distance = v.distance + edge.weight
                    #G.Heap.insert((w.distance + w.heuristic, w.value))
                    G.Heap.changeLocator(w.distance + w.heuristic, w.value)
                    w.prev = v
                    if self.MARK:
                        self.MarkNodes(v, w, edge)

            
            v = G.smallestHeap()
        return count
