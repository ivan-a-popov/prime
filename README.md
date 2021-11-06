# prime

prime - Python script working with prime numbers

Being run directly in terminal, the script finds all prime numbers
in defined range, and counts the total quantity of primes found.
    
Both starting and ending numbers must be positive integers,
so zero or negative value will not be accepted as valid input.
    
Please, note that the numbers defined as boundaries are not
taken in account, though can be primes themselves.

FUNCTIONS

check(number)
	Base function, checks if number us a prime. Returns True if it is, False otherwise.
        
	Using the square root reduces the time needed for check drastically:
	If there's no divisor between 1 and sqrt(N), it just doesn't make sense to check the numbers above.
	(See https://en.wikipedia.org/wiki/Natural_number#Properties for details.)
    
find(low=1, top=100)
	Returns the list of primes found in the given interval

