import apriori
import fp_growth
import time
import sys
sys.setrecursionlimit(2600)
import matplotlib.pyplot as plt
import multiprocessing
import time
import signal
def handler(signum,frame):
    raise Exception("timeout")
import numpy as np
import matplotlib.pyplot as plt




def miningFileReader(fileName):
    '''
    reads a file and returns list of list transactions
    :param fileName: Name of the file
    :return:
    '''
    avg_TL = 0
    distinctItems = set()
    i = 0
    max_transaction = -1
    db = []
    with open(fileName) as openfileobject:
        for line in openfileobject:
            l = [x for x in line.strip().split()]#[int(x) for x in line.strip().split()]
            distinctItems.update(l)
            avg_TL += len(l)
            max_transaction = max(len(l),max_transaction)
            db.append(l)
            i+=1

    avg_TL/=i
    print('Average Transaction: ',avg_TL)
    print('Distinct Items',len(distinctItems))
    print('Density: ',(avg_TL/len(distinctItems))*100)
    return db

files = ['chess.dat','kosarak.txt', 'retail.txt' , 'connect.dat','mushroom.dat','pumsb.dat','pumsb_star.dat','T10I4D100K.txt']
starting = [95,  2,   5, 99.5,  50, 98, 75,  5]
end = [40,.25, .25,   85,  10, 90, 30,  1]
# end = [40,.25, .25,   85,  10, 90, 30,  1]
spacing = [2.5,.25, .25,   .5,   5, .5,  5,.25]
times = [[]]


timeThres = 300
if __name__ == '__main__':

    plt.figure(1)
    pltno = 420
    for i in range(len(files)):
        pltno+=1
        plt.subplot(pltno)
        plt.title(files[i])

        plt.ylabel('Time')

        print('Analyzing '+files[i])
        db = miningFileReader('fp_datasets/' + files[i])
        minerap = apriori.aprioriMiner()
        minerfp = fp_growth.fpGrowthMiner()
        signal.signal(signal.SIGALRM, handler)

        steps = np.arange(starting[i],end[i]-.1,-spacing[i])
        apTimes = []
        for supThres in steps:
            print("Apriori at supportThresold",supThres," time:",end=' ')
            if len(apTimes) > 0 and apTimes[-1] >=timeThres:
                apTimes.append(timeThres)
                continue
            start_time = time.time()
            signal.alarm(timeThres)
            try:
                frequentPatterns = minerap.getFrequentItemset(db,supportThres=int((float(supThres)/100.0)*len(db)))
                signal.alarm(0)
                end_time = time.time()
                tot = end_time - start_time
                print(tot,"sec")
                apTimes.append(tot)

            except:
                print("Apriori Miner on file ", files[i], " at supThres: ", supThres, " took more than 300 seconds")
                apTimes.append(300)


        plt.plot(steps,apTimes,'r--',label='Apriori')

        fpTimes = []
        for supThres in steps:
            if len(fpTimes) > 0 and fpTimes[-1] >=timeThres:
                fpTimes.append(timeThres)
                continue
            print("FpGrowth at supportThresold", supThres, " time:", end=' ')
            start_time = time.time()
            signal.alarm(timeThres)
            try:
                frequentPatterns = minerfp.getFrequentItemset(db,supportThres=int((float(supThres)/100.0)*len(db)))
                signal.alarm(0)

                end_time = time.time()
                tot = end_time - start_time

                # if len(fpTimes) > 0 and tot < fpTimes[-1]:
                #     tot = fpTimes[-1]+.001

                fpTimes.append(tot)
                print(tot,"sec ",len(frequentPatterns),"Frequenet Itemsets")


            except:
                print("Fp Miner on file ", files[i], " at supThres: ", supThres, " took more than 300 seconds")
                fpTimes.append(timeThres)

        plt.plot(steps, fpTimes ,'-',label = 'Fp Growth')
        plt.legend()




    plt.show()











#
#
#
#
# while True:
#     fileName,algo,supThres = tuple(input("Enter filename algo(a,f) min_sup\n").strip().split())
#     miner = None
#     outFileName = None
#     if algo[0] == 'a':
#         miner = apriori.aprioriMiner()
#         outFileName = 'AprioriMined/' + fileName
#     else:
#         miner = fp_growth.fpGrowthMiner()
#         outFileName = 'FpGrowthMined/' + fileName
#
#     fileName = 'fp_datasets/' + fileName
#
#     db = miningFileReader(fileName)
#     print("File read complete")
#     start_time = time.time()
#     frequentPatterns = miner.getFrequentItemset(db,supportThres=int((float(supThres)/100.0)*len(db)))
#     end_time = time.time()
#
#     print("Took ",end_time-start_time," seconds")
#     print("No of frequentPatterns: ",len(frequentPatterns))
#     f_out = open(outFileName,'w')
#
#
#     for pattern in frequentPatterns:
#         pattern = [str(x) for x in pattern]
#         f_out.write(' '.join(pattern))
#         f_out.write('\n')
#     f_out.close()
#
#
#
#
#
#
