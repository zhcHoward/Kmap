#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""
from copy import deepcopy

from utils import (
    Term, diff_terms, get_not_simplified_terms, remove_repeated_sources,
    remove_redundant_terms,
)


class Minterms():
    """ Minterms stores expressions for 1s and "don't care". """

    def __init__(self, minterms=None, maxterms=None, not_cares=None, nov=0):
        if minterms is None:
            minterms = []
        if maxterms is None:
            maxterms = []
        if not_cares is None:
            not_cares = []
        if not minterms and not maxterms:
            raise ValueError('Both of minterms and maxterms cannot be empty at the same time')
        elif not minterms:
            self.maxterms = maxterms
            self.not_cares = not_cares
            self.number_of_variables = self.maxterms[0].length
            self.minterms = self._generate_minterms()
        elif not maxterms:
            self.minterms = minterms
            self.not_cares = not_cares
            self.number_of_variables = self.minterms[0].length
            self.maxterms = self._generate_maxterms()
        else:
            self.minterms = minterms
            self.maxterms = maxterms
            self.not_cares = not_cares
            self.number_of_variables = self.maxterms[0].length
        self.result = None  # result won't be calculated during initialization

    def _generate_minterms(self):
        nov = self.number_of_variables
        minterms = []
        for i in range(2**(nov - 1)):
            term = Term('{1:0{0}b}'.format(nov, i))
            if term not in self.maxterms:
                minterms.append(term)

        self.minterms = minterms

    def _generate_maxterms(self):
        nov = self.number_of_variables
        maxterms = []
        for i in range(2**(nov - 1)):
            term = Term('{1:0{0}b}'.format(nov, i))
            if term not in self.minterms:
                maxterms.append(term)

        self.maxterms = maxterms

    def simplify(self):
        minterms_old = self.not_cares + self.minterms
        for i in range(len(minterms_old)):
            minterms_old[i].source = [i]
        no_new_term = False

        # loop until no terms can be simplified
        while not no_new_term:
            minterms_new = []
            no_new_term = True

            # look into terms two by two,
            # and simplify them if they can be simplified
            for i in range(len(minterms_old)):
                for j in range(i + 1, len(minterms_old)):
                    term = diff_terms(minterms_old[i], minterms_old[j])
                    if term:
                        minterms_new.append(term)
                        no_new_term = False

            # add the terms that can't be simplified to new terms for next loop
            minterms_new.extend(get_not_simplified_terms(minterms_old))

            # remove the repeated terms
            # and prepare for next loop
            minterms_old = []
            for term in set(minterms_new):
                term.flag = False
                minterms_old.append(term)

        minterms_new = deepcopy(minterms_old)
        minterms = remove_repeated_sources(minterms_new, minterms_old)
        self.result = remove_redundant_terms(minterms, self.not_cares)


if __name__ == '__main__':
    str_terms = [
        '0110', '1000', '1001', '1010', '1011', '1100', '1101', '1110']
    t_minterms = []
    for term in str_terms:
        t_minterms.append(Term(term))
    minterms = Minterms(t_minterms)
    minterms.simplify()
    print(minterms.result)
