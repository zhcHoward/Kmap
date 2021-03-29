#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import math

class Term():
    def __init__(self, term='', source=None, flag=False):
        if source is None:
            source = []
        self.term = term
        self.source = source
        self.flag = flag
        self.length = len(term)

    def __eq__(self, other):
        return self.term == other.term

    def __str__(self):
        return self.term

    def __hash__(self):
        return hash(self.term)

    def __repr__(self):
        return self.__str__()


def diff_terms(term1, term2):
    if term1.length == term2.length:
        diff = 0
        pos = -1

        for idx, (t1, t2) in enumerate(zip(term1.term, term2.term)):
            if diff > 1:
                break
            else:
                if t1 != t2:
                    diff += 1
                    pos = idx

        if diff == 1:
            new_term = '*'.join((term1.term[:pos], term2.term[pos + 1:]))
            new_source = term1.source + term2.source
            term1.flag = True
            term2.flag = True

            return Term(new_term, new_source)


def get_not_simplified_terms(terms):
    not_simplified_terms = []
    for term in terms:
        if not term.flag:
            not_simplified_terms.append(term)

    return not_simplified_terms


# remove source that appears in other terms' source list
def remove_repeated_sources(terms, standard_terms):
    for term1, term2 in itertools.product(standard_terms, terms):
        if term1 != term2:
            i = 0
            while i < len(term2.source):
               # print("source check ", term2.source[i],term1.source)
                if term2.source[i] in term1.source:
                #    print("source check popped", term2.source[i],term1.source)
                    term2.source.pop(i)
                    i -= 1
                i += 1
    return terms


# remove terms that its source list is empty
# or its source list only contains indexes from "don't care"
def remove_redundant_terms(terms, not_cares):
   # print("d")
   # print(terms)
   # print(set(not_cares))
    i = 0
    while i < len(terms):
        case1 = terms[i].source
    #    print("te")
    #    print(set(terms[i].source))
    #    print(range(len(set(not_cares))))
        case2 = set(terms[i].source).issubset(range(len(set(not_cares))))
        
       ## case2 = False
        #if(all(terms[i].source for x in not_cares)):
         #   case2 = True

        if not case1 or case2:
            terms.pop(i)
            i -= 1
        i += 1

     #   print(terms)

    return terms

def make_chart(simplified_terms,minterms):

    chart = [ [0 for x in range(len(minterms))] for x in range(len(simplified_terms))]

    print("simplified term", simplified_terms)

    print("minterm for chart", minterms)

    for i in range(len(simplified_terms)):
        for j in range(len(minterms)):
           #print("minterm check", minterms[j])
            if j in simplified_terms[i].source:
                chart[i][j] = 1

    print("chart", chart)

    return chart

def find_prime_implicants(chart, simplified_terms):

    prime_implicants = []

    print("chart dim",range(len(chart[0])),range(len(chart)) )

    change = 1
    ignore_sources = []
    ignore_terms   = []

    while change and (len(chart) - len(ignore_terms)) > 1:
        change = 0
        for i in range(len(chart[0])):
            print("chart dimension",range(len(chart[0])),range(len(chart)) )

            if i not in ignore_sources:
                print("source not covered", i)
                count = 0
                pos   = -1
                for j in range(len(chart)):
                    if j not in ignore_terms:
                        if chart[j][i] == 1:
                            count += 1
                            pos = j
                if count == 1:
                    prime_implicants.append(simplified_terms[pos])
                    change = 1
                    break
            else:
                print("source covered", i)

        if change:
            print("pos", pos, simplified_terms[pos], simplified_terms[pos].source)
            ignore_terms.append(int(pos))
            print("ignorew terms",ignore_terms)

            ignore_sources = ignore_sources + simplified_terms[pos].source

            print("ignore_sources", ignore_sources)
        


    print("prime", prime_implicants)

    prime_implicants = list(set(prime_implicants))
    
    print("prime", prime_implicants)

    return prime_implicants, chart, ignore_sources, ignore_terms


#multiply two terms (ex. (p1 + p2)(p1+p4+p5) )..it returns the product
def multiplication(list1, list2):
    list_result = []
    #if empty
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    #if one is empty
    elif len(list1)==0:
        return list2
    #if another is empty
    elif len(list2)==0:
        return list1

    #both not empty
    else:
        for i in list1:
            for j in list2:
                #if two term same
                if i == j:
                    #list_result.append(sorted(i))
                    list_result.append(i)
                else:
                    #list_result.append(sorted(list(set(i+j))))
                    list_result.append(list(set(i+j)))

        #sort and remove redundant lists and return this list
        list_result.sort()
        return list(list_result for list_result,_ in itertools.groupby(list_result))

def petrick_method(chart, ignore_sources, ignore_terms):

    p = []
    p_sources =[]

    print("chart", chart)

    for i in range(len(chart[0])):
        
        if i not in ignore_sources:

            p_sources.append(i)

            temp = [] 

            for j in range(len(chart)):

                if (j not in ignore_terms) and chart[j][i] == 1:

                    temp.append([j])

            if temp != []:
                p.append(temp)

    print("p", p, p_sources)        

    for i in range(len(p)-1):
        p[i+1] = multiplication(p[i],p[i+1])
        #print("Px", P)

    print("p", p)
    P = sorted(p[len(p)-1],key=len)
    print("P", P)
    final = []
    #find the terms with min length = this is the one with lowest cost (optimized result)
    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
            break
        else:
            break
    print("final", final[0])

    return final[0]


def read_matrix():
    x=0 
    file=open("table.txt","r")#reading input from file
    input1=file.readlines()
    countOnes={}
    flaggedRows={k: 0 for k in range(len(input1))}

    input1 = [i.strip() for i in input1]
   # for i in range(len(input1)) :
       # if (i == len(input1) - 1):
       #     input1[i]=list(input1[i][:])  #parsing data in required format
       #     size=len(input1[i])
       #     print(i,"2")
    
       # else:
       #     input1[i]=list(input1[i][:-1])  #parsing data in required format
       #     size=len(input1[i])
       #     print(i,"3")
    #   if(input1[]) 

    for i in range(len(input1)) :
        input1[i]=list(input1[i][:])  #parsing data in required format
        size=len(input1[i])

    input2 = []

    nov = int(2*math.log2(len(input1[i])))

    x = int(2**(nov/2))

    print("nov",nov)
    print("x",x)

    for i in range(x):
        for j in range(x):
            if(input1[i][j]=='1'):
                print(bin(i))
                cube = str(bin(i*x + j).replace("0b","").zfill(nov))
                print("cube",cube)
                input2.append(cube)

    print(input2)




    return input2