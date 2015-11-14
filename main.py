#! /usr/bin/env python3
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""
from copy import deepcopy

""" Minterms stores expressions for 1s and "don't care". """


def simplify(minterms):
    # minterms_tmp: store minterms of current loop
    # source_tmp: store each minterms is from which 2 minterm
    # flag: store whether the corresponding minterm has been used to generate a new term
    # no_new_term: check whether there is a new term generated in current loop
    minterms_tmp = minterms
    source_tmp = [[i] for i in range(len(minterms_tmp))]
    flag = [False for i in range(len(minterms_tmp))]
    no_new_term = False

    # loop until no terms can be simplified
    while not no_new_term:
        minterms_new = []   # store new terms for next loop
        source_new = []     # store source for new terms
        no_new_term = True

        # look into terms two by two,
        # and simplify them if they can be simplified
        for i in range(len(minterms_tmp)):
            for j in range(i + 1, len(minterms_tmp)):
                dif = 0     # store number of different position of two terms
                pos = -1    # store which position is different
                for k in range(len(minterms_tmp[i])):
                    if dif < 2:
                        # compare two terms character by charater
                        if minterms_tmp[i][k] != minterms_tmp[j][k]:
                            dif += 1
                            pos = k
                    else:
                        # if dif >= 2, then these two term can't be simplified
                        # so jump out of the loop
                        break
                if dif == 1:
                    # change the charater which is different into '*'
                    # the rest remains
                    temp = minterms_tmp[i][:pos] + \
                        '*' + minterms_tmp[i][pos + 1:]
                    minterms_new.append(temp)
                    source_new.append(source_tmp[i] + source_tmp[j])
                    flag[i] = True
                    flag[j] = True
                    no_new_term = False

        # add the terms that can't be simplified to new terms for next loop
        for i in range(len(minterms_tmp)):
            if flag[i] == False:
                minterms_new.append(minterms_tmp[i])
                source_new.append(source_tmp[i])

        # remove the repeated terms
        i = 0
        while i < len(minterms_new):
            j = i + 1
            while j < len(minterms_new):
                if minterms_new[i] == minterms_new[j]:
                    minterms_new.pop(j)
                    source_new.pop(j)
                    j -= 1
                j += 1
            i += 1

        # prepare for next loop
        minterms_tmp = minterms_new
        source_tmp = source_new
        flag = [0 for i in range(len(minterms_tmp))]

    source_new = deepcopy(source_tmp)

    # remove source that appears in other terms' source list
    i = 0
    while i < len(minterms_tmp):
        j = 0
        while j < len(minterms_tmp):
            if i != j:
                k = 0
                while k < len(source_new[i]):
                    if source_new[i][k] in source_tmp[j]:
                        source_new[i].pop(k)
                        k -= 1
                    k += 1
            j += 1
        i += 1

    # remove terms that its source list is empty
    i = 0
    while i < len(minterms_tmp):
        if len(source_new[i]) == 0:
            minterms_tmp.pop(i)
        i += 1

    print(minterms_tmp)

if __name__ == '__main__':
    minterms = [
        '0110', '1000', '1001', '1010', '1011', '1100', '1101', '1110']
    simplify(minterms)
