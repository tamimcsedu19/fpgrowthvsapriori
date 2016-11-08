import collections
import itertools






class FpNode():
    def __init__(self,key,parent):

        self.next = None
        self.key = key
        self.val = 0
        self.childs = {}
        self.parent = parent




    def incr(self,step=1):
        self.val+=step

    def containsChild(self,item):
        return item in self.childs

    def createChild(self,item,parent):
        newNode = FpNode(item,parent)
        self.childs[item] = newNode

    def findChild(self,item):
        if self.containsChild(item):
            return self.childs[item]
        else:
            raise NameError('No child as '+str(item)+ 'is in this node '+str(self.val)+' you need create the child first through createChild')

    def addNextItem(self,next):
        self.next = next





















class FpTree():

    def __init__(self):
        self.root = FpNode(None,None)
        self.lastNode = {}
        self.linkedNodes = {}

    def insert(self,transaction,step=1):
        nextItem = transaction[0]
        node = self.root

        if node.containsChild(nextItem): # If currentNode already contains a child of nextItem , we don't need to branch out
            nextNode = node.findChild(nextItem) # Next node is just the child
        else:

            '''
            We need to branch
            '''
            node.createChild(nextItem,node) # Create a node with nextItem
            nextNode = node.findChild(nextItem) #Find the newly created node

            if nextItem not in self.lastNode: # If this is the first insert of the item
                self.lastNode[nextItem] = nextNode # Add this node as this items last node
                self.linkedNodes[nextItem] = nextNode

            else:

                self.lastNode[nextItem].addNextItem(nextNode) # Add to the linked list of the last node
                self.lastNode[nextItem] = nextNode  #Make this node as the last node




        self.insertIntoNodeItem(nextNode, transaction, 0,step) #Now insert the node in the next node




        pass
    def insertIntoNodeItem(self,node,transaction,itemPos,step):

        item = transaction[itemPos] # First we increment the current node value
        node.incr(step)

        if(itemPos >= (len(transaction)-1)): #If the transaction is over , then return
            return

        '''
        Otherwise get ready for inserting the next item
        '''
        itemPos+=1

        '''
        Find the next item and then we will find the next node too.
        '''
        nextItem = transaction[itemPos]
        nextNode = None

        if node.containsChild(nextItem): # If currentNode already contains a child of nextItem , we don't need to branch out
            nextNode = node.findChild(nextItem) # Next node is just the child
        else:

            '''
            We need to branch
            '''
            node.createChild(nextItem,node) # Create a node with nextItem
            nextNode = node.findChild(nextItem) #Find the newly created node

            if nextItem not in self.lastNode: # If this is the first insert of the item
                self.lastNode[nextItem] = nextNode # Add this node as this items last node
                self.linkedNodes[nextItem] = nextNode
            else:

                self.lastNode[nextItem].addNextItem(nextNode) # Add to the linked list of the last node
                self.lastNode[nextItem] = nextNode  #Make this node as the last node




        self.insertIntoNodeItem(nextNode, transaction, itemPos,step) #Now insert the node in the next node

    def pathUptoRoot(self,node):
        if node is None:
            return []
        if node.parent is None:
            return []
        return self.pathUptoRoot(node.parent) + [node.key]


    def hasSinglePath(self,node=None):
        if node == None:
            node = self.root
        if len(node.childs) > 1:
            return False

        for key,val in node.childs.items():
            return self.hasSinglePath(val)

        return True






class fpGrowthMiner():
    def __init__(self):
        mined = []
        pass

    def findFrequency(self,transactions):
        """
        Return the frequency of each item found in the transaction
        >>> findFrequency([['I1','I2','I5'],['I2','I4'],['I2','I3'],['I1','I2','I4'],['I1','I3'],['I2','I3'],['I1','I3'],['I1','I2','I3','I5'],['I1','I2','I3']]) == {'I1': 6, 'I2': 7, 'I3': 6, 'I4': 2, 'I5': 2}
        True
        """
        freq = {}
        for t in transactions:
            tFreq = collections.Counter(t)
            for key, val in tFreq.items():
                if key in freq:
                    freq[key] += val
                else:
                    freq[key] = val

        return freq

    def buildFpTree(self,transactions,supportThres):
        """

        :param transactions:
        :return: The fpTree after inserting each transaction

        """

        freq = self.findFrequency(transactions)

        globalTree = FpTree()
        i = 0.0
        lenT = len(transactions)
        marker = 5
        for t in transactions:
            # if (100.0*i)/lenT > marker:
            #     print(marker,"% complete")
            #     marker+=5

            sortedT = sorted(t, key=lambda x: (-freq[x], x))
            end = len(sortedT)-1
            while freq[sortedT[end]] < supportThres:
                end-=1
                if end == -1:
                    break


            if end !=-1:
                globalTree.insert(sortedT[:end+1])
            i+=1

        return globalTree




    def fpGrowth(self,tree,suffixItems,supportThres):


        if tree.hasSinglePath():
            longestViablePath = []
            lenLongestViablePath = 0
            minSupport = 0
            for key, val in tree.linkedNodes.items():
                if val.val < supportThres:
                    continue

                pathUptoRoot = tree.pathUptoRoot(val)
                if len(pathUptoRoot) > lenLongestViablePath:
                    longestViablePath = pathUptoRoot
                    lenLongestViablePath = len(pathUptoRoot)
                    minSupport = val.val

            if minSupport < supportThres:
                return

            for r in range(lenLongestViablePath+1):
                for comb in itertools.combinations(longestViablePath,r):
                    fItemsets = tuple(sorted(list(comb) + suffixItems))
                    self.mined[fItemsets] = minSupport
            return












        for key,val in tree.linkedNodes.items():
            beta = suffixItems + [key]



            total = 0
            conditionalTree = FpTree()
            current = val
            while current != None:
                total+=current.val
                current = current.next

            if total >= supportThres:

                current = val
                while current != None:
                    transaction = tree.pathUptoRoot(current.parent)
                    if len(transaction) > 0:
                        conditionalTree.insert(transaction, step=current.val)
                    current = current.next


                self.mined[tuple(sorted(beta))] = total

                tree = conditionalTree

                if len(tree.root.childs) > 0:
                    self.fpGrowth(tree,beta,supportThres)


























    def getFrequentItemset(self,transactions,supportThres):




        self.mined = {}
        globalTree = self.buildFpTree(transactions,supportThres)
        print("Fp tree built")
        self.fpGrowth(globalTree,[],supportThres)

        finalFreq = []
        for key,val in self.mined.items():
            if val >= supportThres:
                finalFreq.append(sorted(list(key)))

        return sorted(finalFreq)












db = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'], ['I2', 'I3'], ['I1', 'I3'],['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]


