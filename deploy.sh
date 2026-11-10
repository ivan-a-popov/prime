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
grep -q "^BOT_TOKEN=" .env || { echo "ERROR: BOT_TOKEN is missing in .env"; exit 1; }

# Recreate the venv if it was copied from another path or its Python is gone.
# ([[ -d .venv ]] is not enough: pip's shebang then points at a missing interpreter.)
if [[ ! -x .venv/bin/python3 ]]; then
  rm -rf .venv
  python3 -m venv .venv
fi
.venv/bin/python3 -m pip install -q -r requirements.txt

systemctl restart prime-bot.service
echo "Deployed: $(git rev-parse --short HEAD)"
