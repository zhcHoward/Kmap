#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""

from utils import (
    Term,
    find_essential_prime_implicants,
    find_prime_implicants,
)


class Minterms(object):
    """ Minterms stores expressions for 1s and "don't care". """

    def __init__(
        self, minterms=None, not_cares=None,
    ):
        if minterms is None:
            minterms = []
        if not_cares is None:
            not_cares = []

        self.minterms = minterms
        self.not_cares = not_cares

    def simplify(self):
        prime_implicants = find_prime_implicants(self.minterms, self.not_cares)
        result = find_essential_prime_implicants(prime_implicants, self.minterms)
        print(result)


if __name__ == "__main__":
    str_terms = ["0100", "1000", "1010", "1011", "1100", "1111"]
    terms_not_care = ["1001", "1110"]
    t_minterms = [Term(term) for term in str_terms]
    not_cares = [Term(term) for term in terms_not_care]

    minterms = Minterms(t_minterms, not_cares)
    minterms.simplify()
