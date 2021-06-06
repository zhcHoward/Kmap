#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from collections import defaultdict


class Term:
    def __init__(self, term="", source=None, flag=False):
        if source is None:
            source = set((int(term, 2),))
        self.term = term
        self.source = source
        self.flag = flag
        self.length = len(term)

    @property
    def ones(self):
        """ones counts the number of '1's in the term

        Returns:
            int: the amount of '1's
        """
        return len(list(filter(lambda c: c == "1", self.term)))

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
            new_term = "*".join((term1.term[:pos], term2.term[pos + 1 :]))
            new_source = term1.source | term2.source
            term1.flag = True
            term2.flag = True

            return Term(new_term, new_source)


def find_prime_implicants(minterms, not_cares):
    table = defaultdict(set)
    for term in minterms + not_cares:
        table[term.ones].add(term)

    prime_implicants = []
    new_implicants = True
    while new_implicants:
        new_implicants = False
        new_table = defaultdict(set)
        for key in sorted(table.keys()):
            # print(f"key == {key}")
            terms1 = table[key]
            terms2 = table[key + 1]
            if terms2:
                for t1, t2 in itertools.product(terms1, terms2):
                    new_term = diff_terms(t1, t2)
                    # print(f"{t1} + {t2} = {new_term}")
                    if not new_term:
                        continue

                    new_table[key].add(new_term)
                    new_implicants = True

            for term in terms1:
                if not term.flag:
                    # print(f"{term} become prime implicant")
                    prime_implicants.append(term)

        table = new_table

    return prime_implicants


def find_essential_prime_implicants(prime_implicants, minterms):
    chart = {}
    for source in itertools.chain.from_iterable((t.source for t in minterms)):
        chart[source] = set()

    for idx, implicant in enumerate(prime_implicants):
        for source in implicant.source:
            if source not in chart:
                continue

            chart[source].add(idx)

    sop = None
    for products in chart.values():
        sop = multiply(sop, products)

    min = 9999
    ids = set()
    for p in sop:
        length = len(p)
        if length < min:
            min = length
            ids = p

    return [prime_implicants[i] for i in ids]


def multiply(result, product):
    if not result:
        return set((frozenset((p,)) for p in product))
    else:
        new_result = set()
        for a, b in itertools.product(result, product):
            new_result.add(a | set((b,)))
        return new_result
