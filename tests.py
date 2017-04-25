#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Kmap import Minterms
from utils import Term


def test_result():
    str_terms = ['0110', '1000', '1001', '1010', '1011', '1100', '1101', '1110']
    t_minterms = []
    for term in str_terms:
        t_minterms.append(Term(term))
    minterms = Minterms(t_minterms)
    minterms.simplify()

    assert {m.term for m in minterms.result} == {'10**', '1*0*', '*110'}


if __name__ == "__main__":
    test_result()
