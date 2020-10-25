import csv
import pickle
MIN_CONF=0.5
from tabulate import tabulate
def gen_datasets(filename=None, num_lines=10):
    if filename == None:
        return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    else:
        with open(filename, newline='') as csvfile:
            data = list(csv.reader(csvfile))

            return data[:num_lines]


# Ck contains Candidate itemsets with length k
# Thus C1 contains all single item
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                # append if item not in C1
                C1.append([item])
    # sort C1 in ascending order
    # print('C1 Length', len(C1), 'C1', C1)
    C1.sort()
    return list(map(frozenset, C1))


# Calculate support of candidate sets and return if minSupport is reached for candidate item
def scanD(D, Ck, minSupport):
    ssCnt = {}  # store frequency each item appears
    for tid in D:
        for can in Ck:
            # s.issubset(t)  test if it has all
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    # print('ssCnt length', len(ssCnt), 'ssCnt', ssCnt)
    numItems = len(D)  # total number of dataset
    retList = []  #all item which reach minSupport
    supportData = {} # key : support value
    for key in ssCnt:
        # support = key frequency / total number of dataset
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

# take a list of frequent itemsets Lk and the size of the itemsets k
# produce Ck, candidate itemsets with length k
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[: k - 2]
            L2 = list(Lk[j])[: k - 2]
            # print '-----i=', i, k-2, Lk, Lk[i], list(Lk[i])[: k-2]
            # print '-----j=', j, k-2, Lk, Lk[j], list(Lk[j])[: k-2]
            L1.sort()
            L2.sort()
            # if first k-2 elements are equal (no duplicates)
            if L1 == L2:
                # set union
                # print 'union=', Lk[i] | Lk[j], Lk[i], Lk[j]
                retList.append(Lk[i] | Lk[j])
    return retList

#set default minSupport to 0.5: occur in at least 50% of all transactions
def apriori(dataSet, minSupport=0.5):

    C1 = createC1(dataSet)
    # print 'C1: ', C1

    D = list(map(set, dataSet))
    # print 'D=', D
    # calculate support and return list of item with support higher than minSupport
    L1, supportData = scanD(D, C1, minSupport)
    # print "L1=", L1, "\n", "outcome: ", supportData

    L = [L1] #L contains the list of frequent itemsets that met a minimun support of 0.5
    k = 2

    while (len(L[k-2]) > 0):
        # print 'k=', k, L, L[k-2]
        Ck = aprioriGen(L[k-2], k) #generate condidate list
        # print 'Ck', Ck
        # print('Ck Length', len(Ck), 'K=', k, 'CK', Ck)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        if len(Lk) == 0:
            break

        L.append(Lk)
        k += 1
        # print 'k=', k, len(L[k-2])
    return L, supportData


def printTable(dic,minSupport = 0.5):
    print('Apriori Result:')
    #sort dic in descending order
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse = True)}
    headers = ['ItemSet','Support']
    sets = list(dic.items())
    sets = [[list(x[0]),x[1]] for x in sets if x[1] >= minSupport]
    #print(sets)
    print(tabulate(sets,headers = headers,tablefmt = 'github'))

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


def display_rules(rules, frequent_items, write=False):
    '''
    Function to display and write rules to file in the prescribed format.

    Prescribed Format
    -----------------
    Association Rules-
    Precedent (itemset (support count)) ---> Antecedent (itemset (support count)) - confidence value

    Frequent itemsets-
    Frequent itemset (support count)

    Parameters
    ----------
    rules : list
        list containing all rules generated by generate_rules function.
    frequent_items : list
        list containing all frequent itemsets.
    write : bool
        write to file if true. Two files are created- association_rules.txt and frequent_itemsets.txt
    '''
    # reverse_map = pickle.load(open('reverse_map.pkl', 'rb'))
    reverse_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    # bad_chars = "[]''"
    # with open('outputs/association_rules.txt', 'w+') as f:
    #     for rule in rules:
    #         X, Y = list(rule.keys())[0]
    #         precedent_support_count, antecedent_support_count = (
    #         frequent_items[len(X) - 1][X], frequent_items[len(Y) - 1][Y])
    #         confidence = list(rule.values())[0]
    #         print(str([reverse_map[x] for x in X]).strip(bad_chars).replace("'", '') + '(' + str(
    #             precedent_support_count) + ')' + ' ---> ' + str([reverse_map[y] for y in Y]).strip(bad_chars).replace(
    #             "'", '') + '(' + str(antecedent_support_count) + ')' + ' - conf(' + str(confidence) + ')')
    #         f.write(str([reverse_map[x] for x in X]).strip(bad_chars).replace("'", '') + '(' + str(
    #             precedent_support_count) + ')' + ' ---> ' + str([reverse_map[y] for y in Y]).strip(bad_chars).replace(
    #             "'", '') + '(' + str(antecedent_support_count) + ')' + ' - conf(' + str(confidence) + ')' + '\n')
    #
    # with open('outputs/frequent_itemsets.txt', 'w+') as f:
    #     for k_itemset in frequent_items:
    #         for itemset, support in k_itemset.items():
    #             f.write(str([reverse_map[x] for x in itemset]).strip(bad_chars).replace("'", '') + ' (' + str(
    #                 support) + ')' + '\n')

def main(filename = None,SHOW = False,num_lines = 10):
    datasets = gen_datasets(filename,num_lines = num_lines)
    L,sd = apriori(datasets)
    rules = generate_rules([sd])
    print(rules)
    # display_rules(rules, [sd], write=True)
    if(SHOW):   printTable(sd)


