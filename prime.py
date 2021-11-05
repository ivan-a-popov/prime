#!/usr/bin/env python3
"""Script working with prime numbers

Being run directly in terminal, the script finds all prime numbers
in defined range, and counts the total quantity of primes found.

Both starting and ending numbers must be positive integers,
so zero or negative value will not be accepted as valid input.

Please, note that the numbers defined as boundaries are not
taken in account, though can be primes themselves.
"""

import time
from math import sqrt


def get_input(input_value):
    """Inner function getting valid input from user"""

    err_message = 'Invalid input: expecting a positive integer.'

    while True:  # until we get valid input
        got_input = input("Enter the "+input_value+" bound: ")
        try:
            result = int(got_input)
        except ValueError:
            print(err_message)
            continue
        else:
            if int(got_input) <= 0:
                print(err_message)
                continue
            else:
                return result


def check(number):
    """Base function, checks if the number us a prime"""

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

        low = get_input('lower')
        top = get_input('upper')

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
