#!/usr/bin/env python3
"""
This script finds all the prime numbers in arbitrary range,
and counts the total quantity of primes found.

Both starting and ending numbers must be positive integers,
so zero or negative value will not be accepted as valid input.

Please, note that the numbers defined as boundaries are not
taken in account, though can be primes themselves.
"""

import time
from math import sqrt


def input_ok(input_value):  # function validates the input
    err_message = 'Invalid input: expecting a positive integer.'
    try:
        int(input_value)
    except ValueError:
        print(err_message)
        return False
    else:
        if int(input_value) <= 0:
            print(err_message)
            return False
        else:
            return True


def check(number):
    for divisor in range(2, int(sqrt(number) + 1)):
        if number % divisor == 0:
            return False
    else:
        return True


def find(start=1, stop=100):
    pass


if __name__ == '__main__':
    print(__doc__)
    while True:  # the main loop

        while True:  # checking the input
            low = input("Enter the lower bound: ")
            if input_ok(low):
                low = int(low)
                break
            else:
                continue

        while True:  # checking the input
            top = input("Enter the upper bound: ")
            if input_ok(top):
                top = int(top)
                break
            else:
                continue

        tic = time.perf_counter()
        print("Searching for prime numbers in range from", low, "to", str(top)+"...\n")
        count = 0
        for n in range(low+1, top):
            if check(n):
                if count == 0:
                    print('Prime numbers found:', end=" ")
                    print(n, end=", ")
                else:
                    print(n, end=", ")
                count += 1
        print("\b\b.\n"+'_'*42, "\n")
        toc = time.perf_counter()
        print("Finished.", count, "prime numbers found between", low, "and", top)
        print(f"It took {toc - tic:0.4f} sec. to calculate\n")
        wish = input("Do you wish to check another range? (y/N) ")
        if wish in ("Y", "y", "Да", "да", "ДА", "yes", "YES", "Yes", "yep", "yeah"):
            continue
        else:
            print("Ok. Bye-bye!")
            break
