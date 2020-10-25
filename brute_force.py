
#generate all possible itemsets then calculate support value
#if n items is given, 2^n itemsets are created
import csv
from itertools import islice
from tabulate import tabulate
MIN_CONF = 0.5

def gen_datasets(filename = None,num_lines = 10):
    if filename == None: return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
    else:
        with open(filename, newline='') as csvfile:
            data = list(csv.reader(csvfile))
            
            return data[:num_lines]
        
    

def gen_itemsets(datasets):
    itemlist = [] #contain every item
    for transactions in datasets:
        for item in transactions:
            if item not in itemlist:
                itemlist.append(item)
    print('itemlist', len(itemlist))
    itemsets = []  #contain every possible itemset
    
    from itertools import combinations
    for i in range(1,len(itemlist)+1):    
        comb = combinations(itemlist,i)
        itemsets.extend(list(comb))
    print('itemsets', len(itemsets))
    #print(itemsets)
    return itemsets

#find how many times itemset exist in each transaction
def calculate_support(itemset,datasets):
    counter = 0
    for tran in datasets:    
        result = all(elem in tran for elem in itemset)
        if(result): counter += 1
    return counter/len(datasets)

#return a dictionary with itemset as keys and support as value
def gen_sup_list(itemsets,datasets,minSupport = 0.2):
    itemSupDic = {}
    sup_val = 0
    for itemset in itemsets:
        sup_val = calculate_support(itemset, datasets)
        if sup_val != 0:
            itemSupDic.update({itemset : sup_val})
    #print(itemSupDic)
    d = dict((k,v) for k,v in itemSupDic.items() if v >= minSupport)
    return d
  
#complete procedure to get most frequent association
def brute_force(num_lines = 10, filename = None):
    datasets = gen_datasets(filename,num_lines = num_lines)
    itemsets = gen_itemsets(datasets)
    return gen_sup_list(itemsets, datasets)

def printTable(dic):
    print('Brute Force Result:')
    #sort dic in descending order
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse = True)}
    headers = ['ItemSet','Support']
    sets = list(dic.items())
    sets = [[list(x[0]),x[1]] for x in sets]
    #print(sets)
    print(tabulate(sets,headers = headers,tablefmt = 'github'))
    print('\n')

def apriori_gen(l_prev):
    '''
    Function to generate c(k+1) from l(k).

    This function has been implemented as presented in Introduction to Data
    Mining,Tan Pang-Ning et al, section 6.2.3
    Parameters
    ----------
    l_prev : list
        l(k)

    Returns
    ----------
    c_curr : list
        c(k+1).
    '''
    n = len(l_prev)
    c_curr = []
    for i in range(n):
        for j in range(i + 1, n):
            temp_a = l_prev[i]
            temp_b = l_prev[j]
            if temp_a[:-1] == temp_b[:-1]:
                temp_c = []
                temp_c.extend(temp_a)
                temp_c.append(temp_b[-1])
                temp_c = sorted(temp_c)
                c_curr.append(temp_c)
    return c_curr

def generate_rules(frequent_items):
    '''
    Function to generate rules from frequent itemsets.

    Parameters
    ----------
    frequent_items : list
        list containing all frequent itemsets.

    Returns
    ----------
    rules : list
        list of generated rules.
    rules is stored in the following format-
    [(X, Y), (X,Y)]
    '''
    rules=[]
    for k_itemset in frequent_items:
        k=len(list(k_itemset.keys())[0])
        if k==1: # No rules can be generated using 1 itemsets
            continue
        for itemset, support in k_itemset.items():
            H_curr=[[x] for x in itemset]
            to_remove=[]
            for h in H_curr:
                X=tuple(sorted(set(itemset)-set(h)))
                Y=tuple(sorted(h))
                confidence = support / (frequent_items[k-2][X])
                if confidence > MIN_CONF:
                    rule=[]
                    rule.append(X)
                    rule.append(Y)
                    rules.append({tuple(rule):confidence})
                else:
                    to_remove.append(h)

            H_curr=[x for x in H_curr if x not in to_remove]

            for m in range(1,k-1):
                if k > m+1:
                    H_next=apriori_gen(H_curr)
                    to_remove=[]
                    for h in H_next:
                        X=tuple(sorted(set(itemset)-set(h)))
                        Y=tuple(sorted(h))
                        confidence = support / (frequent_items[k-m-2][X])
                        if confidence>MIN_CONF:
                            rule=[]
                            rule.append(X)
                            rule.append(Y)
                            rules.append({tuple(rule):confidence})
                        else:
                            to_remove.append(h)
                    H_next=[x for x in H_next if x not in to_remove]
                    H_curr=H_next
                else:
                    break
    return rules
    
def main(num_lines = 10, filename = None,SHOW = False):
    L = brute_force(num_lines = num_lines, filename = filename)
    if(SHOW):   printTable(L)
    print('')
