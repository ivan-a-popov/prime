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
	if there's no divisor of N between 1 and sqrt(N)+1, there's just no sense in searching above.
	(See https://en.wikipedia.org/wiki/Prime_number#Trial_division for details.)
    
find(low=1, top=100)
	Returns the list of primes found in the given interval

