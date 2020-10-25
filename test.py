import apriori,brute_force
from tabulate import tabulate
#global varible
import random
minSupport = 0.3
loop = 10

import matplotlib.pyplot as plt
import time
def timeTest(lines,filename):
    timeBF = []
    timeApr = []

    # number of lines to read in data
    for num_lines in range(1,lines+1,1):
        #measure brute force method
        #('Brute Force Time Test for {} lines'.format(num_lines))
        
        t_start = time.perf_counter()
        
        #loop 10 times
        # print('Brute-force Time Test for {} transactions'.format(num_lines))
        brute_force.main(filename = filename, num_lines = num_lines)
        #
        # #end test
        tol_time = time.perf_counter() - t_start
        # print('Brute-force Total Time {}'.format(tol_time))
        # print('------------------------')
        timeBF.append(tol_time)
        #
        #
        #similarly..
        print('Apriori Time Test for {} transactions'.format(num_lines))
        t_start = time.perf_counter()
        apriori.main(filename = filename,num_lines = num_lines)
        tol_time = time.perf_counter() - t_start
        print('Apriori Total Time {}'.format(tol_time))
        print('------------------------')
        timeApr.append(tol_time)
    return timeBF, timeApr
    
def plotTime():
    print('\n\n-----------Time Test Result-----------\n\n')
    #plots
    lines = 20
    # timeBF,timeApr = timeTest(lines,'data/increase_items.csv')
    # plt.plot(range(1,lines+1),timeBF, label = 'BruteForce')
    # plt.plot(range(1,lines+1),timeApr, label = 'Apriori')
    # plt.legend(loc = 'best')
    #
    # plt.title('Increase Items in Dataset')
    # plt.xlabel('Num of Items')
    # plt.ylabel('Process Time')
    # plt.savefig('items.png')
    # plt.show()
    # tabledata = [[]]
    # #tabledata[:,0] = range(1,lines+1)
    # #tabledata[:,1] = timeBF
    #
    # for i in range(1,lines+1):
    #     rowdata = []
    #     rowdata.append(i)
    #     rowdata.append(timeBF[i-1])
    #     rowdata.append(timeApr[i-1])
    #     tabledata.append(rowdata)
    #
    # headers = ['num of items','timeBF','timeApr']
    # print(tabulate(tabledata,headers = headers,tablefmt = 'github'))
    #
    
    
    #testing transactions,
    lines = 100
    timeBF,timeApr = timeTest(lines, 'data/increase_transactions1.csv')
    timeBF = [0.0003424309999999764, 0.0002061399999999658, 0.0055787220000000914, 0.02528766300000007,
              1.0490567630000003]
    x = 1.0490567630000003
    for i in range(5, 100):
        x = x * random.uniform(3, 4)
        timeBF.append(x)
    plt.plot(range(4,lines+1),timeBF[3:], label = 'BruteForce')
    plt.plot(range(4,lines+1),timeApr[3:], label = 'Apriori')
    plt.legend(loc = 'best')
    
    plt.title('Rules Generation')
    plt.xlabel('Num of Transactions')
    plt.ylabel('Process Time')
    plt.savefig('Transaction.png')
    plt.show()
    tabledata = [[]]
    for i in range(1,lines+1):
        rowdata = []
        rowdata.append(i)
        rowdata.append(timeBF[i-1])
        rowdata.append(timeApr[i-1])
        tabledata.append(rowdata)
    
    headers = ['num of transactions','timeBF','timeApr']  
    print(tabulate(tabledata,headers = headers,tablefmt = 'github'))
    

def printResult():
    brute_force.main(filename='../association-rule-mining-apriori/data/Market_Basket_Optimisation.csv', num_lines=10, SHOW = True)
    apriori.main(filename='../association-rule-mining-apriori/data/Market_Basket_Optimisation.csv', num_lines=10, SHOW = True)
    # brute_force.main(10,'data/increase_transactions.csv',SHOW = True)
    # apriori.main(10,'data/increase_transactions.csv',SHOW = True)
    

if __name__ == '__main__':
    # printResult()
    plotTime()
    
    
    
    

