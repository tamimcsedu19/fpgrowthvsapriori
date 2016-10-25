

import collections


class aprioriMiner():
    def __init__(self):
        pass
    def testItemsets(self,itemset1,itemset2):
        itemset1 = sorted(list(itemset1))
        itemset2 = sorted(list(itemset2))

        if len(itemset1) == len(itemset2) and itemset1[:-1] == itemset2[:-1] and itemset1[-1]<itemset2[-1]:
            return True
        return False

    def pruneTest(self,fk_1,candidate):

        fk_1 = {tuple(sorted(x)) for x in fk_1}
        candidate = list(candidate)
        for i in range(len(candidate)):
            subset = candidate[:i]+candidate[i+1:]
            if tuple(sorted(subset)) not in fk_1:
                return False

        return True





    def prune(self,fk_1,fkCandidate):
        #fkCandidate: A list of candidates
        #Set of Fk-1
        # First convert each of the candidates and fk_1 into tuples
        fk = set()

        for candidate in fkCandidate:
            if self.pruneTest(fk_1,candidate):
                fk.add(tuple(candidate))
        return fk








    def genFk(self,fk_1):

        fk = set()
        for i in fk_1:
            for j in fk_1:
                i = sorted(i)
                j = sorted(j)
                if self.testItemsets(i,j):
                    l = list(i)
                    l.append(j[-1])
                    fk.add(tuple(l))


        return fk

    def genF1(self,transactions,supportThres):
        """
        Return the frequency of each item found in the transaction
        >>> genF1([['I1','I2','I5'],['I2','I4'],['I2','I3'],['I1','I2','I4'],['I1','I3'],['I2','I3'],['I1','I3'],['I1','I2','I3','I5'],['I1','I2','I3']]) == {'I1': 6, 'I2': 7, 'I3': 6, 'I4': 2, 'I5': 2}
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


        finalFreq = set()
        for key,val in freq.items():
            if val >= supportThres:
                finalFreq.add(key)



        return finalFreq

    def eliminateNonFrequent(self,transactions,candidates,supportThres):

        freqs = {}

        for t in transactions:
            st = set(t)
            for c in candidates:
                ct = set(c)
                if ct.issubset(st):
                    key = tuple(ct)
                    if key in freqs:
                        freqs[key] += 1
                    else:
                        freqs[key] = 1

        finalFreq = set()
        for key,val in freqs.items():
            if val >= supportThres:
                finalFreq.add(key)
        return finalFreq














    def mine(self,transactions,supportThres):

        transactionSet = {tuple(sorted(x)) for x in transactions}


        frequentItemsets = set()

        fk_1 = [(x,) for x in self.genF1(transactions,supportThres)] #f1

        while True:
            if len(fk_1) == 0:
                break
            frequentItemsets.update(fk_1)

            candidateFk = self.genFk(fk_1)
            prunedFK = self.prune(fk_1,candidateFk)
            fk = self.eliminateNonFrequent(transactions,prunedFK,supportThres)
            fk_1 = fk


        return frequentItemsets








    def getFrequentItemset(self,transactions,supportThres,sortKey=None):
        if sortKey:
            return sorted([sorted(list(x)) for x in self.mine(transactions,supportThres)],key=sortKey)
        else:
            return sorted([sorted(list(x)) for x in self.mine(transactions,supportThres)])


db = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'], ['I2', 'I3'], ['I1', 'I3'],['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]
