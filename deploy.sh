#!/usr/bin/env bash
# Deploys the bot on the server: installs dependencies and restarts the
# systemd service. Git sync is done by the CI workflow before this script
# runs, so deploy.sh always executes in its freshest version.
set -Eeuo pipefail

cd "$(dirname "$0")"

# Secrets live only on the server, outside git.
if [[ ! -s .env ]]; then
  echo "ERROR: .env is missing or empty — create it on the server first."
  exit 1
fi
for var in BOT_TOKEN MASTER_ID; do
  grep -q "^$var=" .env || { echo "ERROR: $var is missing in .env"; exit 1; }
done

[[ -d .venv ]] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

sudo -n systemctl restart prime-bot.service
echo "Deployed: $(git rev-parse --short HEAD)"
