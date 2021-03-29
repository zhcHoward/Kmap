#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""
import itertools
from copy import deepcopy

from utils import (
    Term,
    diff_terms,
    get_not_simplified_terms,
    remove_repeated_sources,
    remove_redundant_terms,
    read_matrix,
    make_chart,
    find_prime_implicants,
    petrick_method,
)


class Minterms(object):
    """ Minterms stores expressions for 1s and "don't care". """

    def __init__(self, minterms=None, not_cares=None, nov=0):
        #print(minterms)
        if minterms is None:
            minterms = []
        if not_cares is None:
            not_cares = []

        self.minterms = minterms
        self.not_cares = not_cares
        self.number_of_variables = nov if nov else self.minterms[0].length


    def simplify(self):
        minterms_old = self.not_cares + self.minterms
        minterms_original = deepcopy(minterms_old)
        print(minterms_old)
        no_new_term = False
        for idx, term in enumerate(minterms_old):
            term.source = [idx]

        # loop until no terms can be simplified
        while not no_new_term:
            minterms_new = []
            no_new_term = True

            print("minterms old",minterms_old)

            minterms_x = deepcopy(minterms_old)
            # look into terms two by two,
            # and simplify them if they can be simplified
            for term1, term2 in itertools.combinations(minterms_old, 2):
                term = diff_terms(term1, term2)
                
                if term:
                    minterms_new.append(term)
                    no_new_term = False

            print("No new term", no_new_term)
            # add the terms that can't be simplified to new terms for next loop
            minterms_new.extend(get_not_simplified_terms(minterms_old))

            print(minterms_new)
            print("set",set(minterms_new))
            # remove the repeated terms
            # and prepare for next loop
            minterms_old = []

            temp = []
            [temp.append(x) for x in minterms_new if x not in temp]

            for i in range(len(temp)):
                print(temp[i].term, temp[i].source)

            for term in temp:
                term.flag = False
                minterms_old.append(term)

            #minterms_old = remove_repeated_sources(minterms_old,minterms_x )
            #minterms_old = remove_redundant_terms(minterms_old, self.not_cares)

        minterms_new = deepcopy(minterms_old)
        print("copy",minterms_new)
        for i in range(len(minterms_new)):
            print(minterms_new[i].term, minterms_new[i].source)
        #minterms = remove_repeated_sources(minterms_new, minterms_old)
        #print("remove repeated sources",minterms)
#
        #for i in range(len(minterms)):
        #    print(minterms[i].term, minterms[i].source)
#
        #x = remove_redundant_terms(minterms, self.not_cares)
        #print("remove redundant terms",x)

        chart = make_chart(minterms_new, minterms_original)

        essential_prime_implicants, chart, ignore_sources, ignore_terms = find_prime_implicants(chart, minterms_new)

        prime_implicants_numbers = petrick_method(chart, ignore_sources, ignore_terms)

        final_result = deepcopy(essential_prime_implicants)

        for i in range(len(prime_implicants_numbers)):
            final_result.append(minterms_new[prime_implicants_numbers[i]])


        print("essnetial", essential_prime_implicants)
        print("num", prime_implicants_numbers)
        self.result = final_result
        


if __name__ == "__main__":
    str_terms = ["0001","0010","1001","1011","1100","1110","1111"]
    terms_not_care = [] #["1010", "1011", "1100", "1101", "1110", "1111"]
    #check = read_matrix()
    #print(check)
    t_minterms = [Term(term) for term in str_terms]
    not_cares = [Term(term) for term in terms_not_care]

    minterms = Minterms(minterms = t_minterms)
    minterms.simplify()
    print("Final Result",minterms.result)
