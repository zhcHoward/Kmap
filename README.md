# Kmap
A simple function to simplify boolean algebra expressions, inspired by [Karnaugh Map(wikipedia)](https://en.wikipedia.org/wiki/Karnaugh_map).
# Introduction
Basically, this Kmap.py file contains a function which can simplify boolean algebra expressions according to the truth table. But to input the full truth table is unecessary and may be troublesome espacially when there are too many expressions. So the function simplify takes only minterms and "don't care" as input.
# Algorithm
There are 3 main variables for this function:

* `minterms` used for storing terms like `'1001'` and `'10**'`.
* `source` used for keeping track on where a term comes from, e.g. term `'1001'` comes from itself, the the source for it is only its index in minterms `[1]`. But for `'10**'`, it is generated by `['1000', '1001', '1010', '1011']` this 4 terms, so its source is `[1, 2, 3, 4]`.
* `flag` used for checking if a term has been used to generate a new term.

This function can be divided into 2 parts:

1. Simplify all the terms untill no more terms can be simpified, the output of the example below in this step is: `['10**', '1*0*', '1**0', '*110']` which is same as `AB' + AC' + AD' + BCD'`
2. In the 2nd step, the `source` of all terms will be checked.
If a term's source don't have at least 1 unique source or the unique term(s) is the term of "don't care, it means this term is unnecessary and this term will be removed. Then, you will get the final result.

# Example
On the wiki page(linked above), you can find a truth table which can be represented as:

* `f(A,B,C,D) = Σ(6,8,9,10,11,12,13,14)` or 
* `f(A,B,C,D) = A'BCD' + AB'C'D' + AB'C'D + AB'CD' + AB'CD + ABC'D' + ABC'D + ABCD'` (A' means not A)
 
So in the code, set `minterms = ['0110', '1000', '1001', '1010', '1011', '1100', '1101', '1110']`.
Then, run the code with `python3 Kmap.py` in a terminal, you will see the output.
For this one, the output is `['10**', '1*0*', '*110']`('\*' means the variable on that position has been simplified). This output means `AB' + AC' + BCD'` which is the same as the result on wiki.

For "don't cares", you just need to put terms for "don't care" into `not_care`, then run the code.


