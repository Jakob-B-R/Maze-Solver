class PHeap:
    '''
    Priority Queue tailed for use with 'mazes.py'. Stores vertices as their key in Graph dict in a list in heap order,
    (distance, value)
    '''

    def __init__(self):
        '''
        Define heap array, and HashMap, which holds the indexes in the heap of the values
        '''
        self.heap = []
        self.hashMap = {} 


    def insert(self, v):
        '''
        Insert a new Node to the heap

        Input: a Node v
        '''
        self.hashMap[v[1]] = len(self.heap)
        self.heap.append(v)
        self.percUp()


    def percUp(self):
        '''
        Perc The Last Node inserted up to its proper position
        O(log n)
        '''
        i = len(self.heap) - 1
        while i > 0:
            if self.heap[i][0] < self.heap[(i-1)//2][0]:
                #self.Swap(i, (i-1)//2)
                self.hashMap[self.heap[i][1]] = (i-1) // 2
                self.hashMap[self.heap[(i-1)//2][1]] = i
                self.heap[i], self.heap[(i-1)//2] = self.heap[(i-1) // 2], self.heap[i]


            i = (i-1) // 2

    def removeMin(self):
        '''
        Remove the Minimum element in the Heap

        O(log n)
        Output: A Node with the minumum weight
        '''
        if not self.isEmpty():
            retval = self.heap[0]
            self.heap[0] = self.heap[-1]
            self.heap.pop()
            self.percDown(0)
            
            self.hashMap.pop(retval[1])
            #self.downheap(0)
            return retval

        return None

    def downheap(self, i):
        '''
        Move the node at heap[i] down to it's position

        Input: And index i
        '''
        if self.heap[(i * 2 )][0] > len(self.heap):
            return

        bkIndex = i * 2 + 1
        bk = self.heap[i * 2 + 1]

        if self.heap[(i * 2) + 2][0] <= len(self.heap) and bk[0] > self.heap[(i * 2) + 2][0]:
            bk = self.heap[(i * 2) + 2]
            bkIndex = i * 2 + 2

        if self.heap[i][0] > bk[0]:
            bk, self.heap[i] = self.heap[i], bk
            self.downheap(bkIndex)

    def percDown(self, i):
        '''
        Move the node at heap[i] down to it's position

        Input: And index i
        '''
        n = len(self.heap) - 1
        while (i*2+ 1) <= n:
            mc = self.minChild(i)
            if self.heap[i][0] > self.heap[mc][0]:
                #self.Swap(i, mc)
                self.hashMap[self.heap[i][1]] = mc
                self.hashMap[self.heap[mc][1]] = i
                self.heap[i], self.heap[mc] = self.heap[mc], self.heap[i] 

            i = mc

    def Swap(self, i1, i2):
        '''
        Not used
        '''
        #i1, i2 = (distance, key)
        # hashmap = {key, index_in_heap}
        # heap = (distance, key)

        key1 = self.heap[i1][1]
        key2 = self.heap[i2][1]

        index1, index2 = self.hashMap[key1], self.hashMap[key2]

        self.hashMap[key1], self.hashMap[key2] = self.hashMap[key2], self.hashMap[key1]

        #self.hashMap[self.heap[i1[1]] = i2[0]
        #self.hashMap[self.heap[i2[1]]] = i1[0]

        self.heap[i1], self.heap[i2] = self.heap[i1], self.heap[i2]

    def minChild(self, i):
        '''
        Find the child of the node at heap[i] with the smallest distance

        Input: An index i
        Output: The new index
        '''
        n = len(self.heap) - 1
        if i * 2 + 2 > n:
            return i * 2 + 1

        if self.heap[i * 2 + 1][0] < self.heap[ i * 2 + 2][0]:
            return i * 2 + 1

        return i * 2 + 2

    def heapsort(self):
        '''
        Not used
        '''
        n = len(self.heap)

        self.buildMaxHeap()

        for i in range(n-1, 0, -1):

            #swap value of first indexed
            #with last index

            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]

            j, index = 0,0

            while True:
                index = 2 * j + 1

                if (index < i-1) and self.heap[index][0] < self.heap[index + 1][0]:
                    index +=1 

                if index < i and self.heap[j][0] < self.heap[index][0]:
                    self.heap[j], self.heap[index] = self.heap[index], self.heap[j]

                j = index
                if index >= i:
                    break

        return self.heap

    #LOCAL
    def buildMaxHeap(self):
        '''
        Not used
        '''
        n = len(self.heap)
        for i in range(n):
            if self.heap[i][0] > self.heap[int((i-1) /2)][0]:
                j = i

                #swp child and parent until
                #parent is smaller

                while self.heap[j][0] > self.heap[int((j-1)/2)][0]:
                    (self.heap[j], self.heap[int((j-1)/2)]) = (self.heap[int((j-1)/2)], self.heap[j])

                    j = int((j-1)/2)

    def changeLocator(self, new_locator, value):
        '''
        Lower the weight of a Node and update it's new position
        '''
        i = self.hashMap[value]
        v = self.heap[i]
        self.heap[i] = (new_locator, v[1])
        self.UpHeap(i)

    def UpHeap(self, i):
        while(i > 0):
            if self.heap[i][0] < self.heap[(i-1) // 2][0]: #less than parent
                self.hashMap[self.heap[i][1]] = (i-1) // 2
                self.hashMap[self.heap[(i-1) // 2][1]] = i
                self.heap[i], self.heap[(i-1) // 2] = self.heap[(i-1) // 2], self.heap[i]

                #self.Swap(i, (i-1) // 2)
                i = (i-1) // 2
            else:
                break

    def isEmpty(self):
        if len(self.heap) == 0:
            return True
        return False

    def __str__(self):
        return self.heap.__str__()


if __name__ == "__main__":
    import random
    h = PHeap()
    l = [(i,chr(i+65)) for i in range(26)]
    random.shuffle(l)
    for n in l:
        h.insert(n)

    print(h.heap)
    print("HM[m]", h.hashMap['M'])
    test_node = 'A'
    print(h.heap[h.hashMap[test_node]][1])
    assert(h.heap[h.hashMap[test_node]][1] ==test_node)

    print(h)
