# prime

prime - Python script working with prime numbers

Being run directly in terminal, the script finds all prime numbers
in defined range, and counts the total quantity of primes found.
    
Both starting and ending numbers must be positive integers,
so zero or negative value will not be accepted as valid input.
    
Please, note that the numbers defined as boundaries are not
taken in account, though can be primes themselves.

If you want to check a single number for primality, you should contact my
prime telegram bot (http://t.me/ip_prime_bot), which uses the same base function.

FUNCTIONS

check(number)
	Base function, checks if number is a prime. Returns "True" if it is, "False" otherwise.
        
	Using the square root reduces the time needed for check drastically:
	if there's no divisor of N between 1 and sqrt(N)+1, there's just no sense in searching above.
	(See https://en.wikipedia.org/wiki/Prime_number#Trial_division for details.)
    
find(low, top)
	Returns the list of primes found in the given interval

TESTING

	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
	.venv/bin/pytest

DEPLOYMENT

	The bot deploys automatically on every push to main via GitHub Actions
	(.github/workflows/deploy.yml): the runner SSHes into the server, syncs
	the repository, installs dependencies and restarts the prime-bot systemd
	service (deploy.sh).

	One-time server setup:
	1. Fresh clone into /home/ipopov/prime as the ipopov user, not root
	   (old clones predate the history rewrite and cannot be reused).
	   If cloned as root: sudo chown -R ipopov:ipopov /home/ipopov/prime
	2. Create /home/ipopov/prime/.env with the bot credentials:
	   BOT_TOKEN=<token from @BotFather>
	   MASTER_ID=<your Telegram user id>
	   The bot loads it via python-dotenv, so it works the same under
	   systemd and in manual runs.
	3. Install the service:
	   sudo cp prime-bot.service /etc/systemd/system/
	   sudo systemctl daemon-reload && sudo systemctl enable --now prime-bot
	4. Allow passwordless restarts for the deploy user:
	   echo 'ipopov ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart prime-bot.service' > /etc/sudoers.d/prime-bot
	   chmod 440 /etc/sudoers.d/prime-bot && visudo -cf /etc/sudoers.d/prime-bot
	5. Add SSH_HOST, SSH_USER and SSH_PRIVATE_KEY secrets to the GitHub
	   repository (same values as for ivanpopov.pro).

