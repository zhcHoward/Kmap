#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Term():
    def __init__(self, term='', source=[], flag=False):
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

        for i in range(term1.length):
            if diff < 2:
                if term1.term[i] != term2.term[i]:
                    diff += 1
                    pos = i
            else:
                break

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
    for term1 in standard_terms:
        for term2 in terms:
            if term1 != term2:
                i = 0
                while i < len(term2.source):
                    if term2.source[i] in term1.source:
                        term2.source.pop(i)
                        i -= 1
                    i += 1
    return terms


# remove terms that its source list is empty
# or its source list only contains indexes from "don't care"
def remove_redundant_terms(terms, not_cares):
    i = 0
    while i < len(terms):
        case1 = terms[i].source
        case2 = set(terms[i].source).issubset(range(len(set(not_cares))))
        if not case1 or case2:
            terms.pop(i)
            i -= 1
        i += 1

    return terms
