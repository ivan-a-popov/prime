# Deployment

The bot deploys automatically on every push to `main` via GitHub Actions
(`.github/workflows/deploy.yml`): the runner SSHes into the server, syncs the
repository, installs dependencies and restarts the `prime-bot` systemd service
(`deploy.sh`).

## One-time server setup

1. Fresh clone into `/home/ipopov/prime` as the `ipopov` user, not root (old
   clones predate the history rewrite and cannot be reused). If cloned as root:
   `sudo chown -R ipopov:ipopov /home/ipopov/prime`

2. Create `/home/ipopov/prime/.env` with the bot credentials:

   ```
   BOT_TOKEN=<token from @BotFather>
   MASTER_ID=<your Telegram user id>
   ```

   The bot loads it via python-dotenv, so it works the same under systemd and in
   manual runs.

   If `api.telegram.org` is not directly reachable from the server, add one of:

   ```
   LOCAL_BOT_API_BASE=http://127.0.0.1:8081
   TELEGRAM_PROXY=socks5://user:pass@host:1080
   ```

   The proxy can also be assembled from `PROXY_HOST`, `PROXY_PORT`,
   `PROXY_TYPE`, `PROXY_USER` and `PROXY_PASS` parts; socks5 by default.

3. Install the service:

   ```bash
   sudo cp prime-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload && sudo systemctl enable --now prime-bot
   ```

4. Allow passwordless restarts for the deploy user:

   ```bash
   echo 'ipopov ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart prime-bot.service' > /etc/sudoers.d/prime-bot
   chmod 440 /etc/sudoers.d/prime-bot && visudo -cf /etc/sudoers.d/prime-bot
   ```

5. Add `SSH_HOST`, `SSH_USER` and `SSH_PRIVATE_KEY` secrets to the GitHub
   repository.
