#!/usr/bin/env python3
"""Script working with prime numbers

Being run directly in terminal, the script finds all prime numbers
in defined range, and counts the total quantity of primes found.

Both starting and ending numbers must be positive integers,
so zero or negative value will not be accepted as valid input.

Please, note that the numbers defined as boundaries are not
taken in account, though can be primes themselves.

If you want to check a single number for primality, you should contact my
prime telegram bot (http://t.me/ip_prime_bot), which uses the same base function.
"""

from math import sqrt


def get_input(input_value):
    """Internal function getting valid input from user in interactive mode"""

    err_message = 'Invalid input: expecting a positive integer.'

    while True:  # Until we get valid input
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
    """Base function, checks if number us a prime. Returns True if it is, False otherwise.

    Using the square root reduces the time needed for check drastically:
    If there's no divisor of N between 1 and sqrt(N)+1, there's just no sense in searching above.
    (See https://en.wikipedia.org/wiki/Prime_number#Trial_division for details.)
    """

    if number % 2 == 0 and number != 2:
        return False
    # This looks a bit ugly, but excluding evens halves the quantity of checks in total, and 2 itself is a prime
    for divisor in range(3, int(sqrt(number) + 1), 2):
        if number % divisor == 0:
            return False
    else:
        return True


def find(low, top):
    """Returns the list of primes found in the given interval"""

    result = []
    for n in range(low + 1, top):
        if check(n):
            result.append(n)
    return result


if __name__ == '__main__':
    import time

    print(__doc__)
    while True:  # the main loop

        low = get_input('lower')
        top = get_input('upper')

        tic = time.perf_counter()
        print("Searching for prime numbers in range from", low, "to", str(top)+"...\n")
        result = find(low, top)
        toc = time.perf_counter()
        if result:
            print('Prime numbers found:\n', ", ".join(map(str, result)))
            print("_"*42)
        print("Finished.", len(result), "prime numbers found between", low, "and", top)
        print(f"It took {toc - tic:0.4f} sec. to calculate\n")

        wish = input("Do you wish to check another range? (y/N) ")
        if wish in ("Y", "y", "Да", "да", "ДА", "yes", "YES", "Yes", "yep", "yeah"):
            continue
        else:
            print("Ok. Bye-bye!")
            break
