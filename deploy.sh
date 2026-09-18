#!/usr/bin/env bash
# Push local commits and deploy them on GoDaddy in one step.
# Requires SSH access on the hosting plan (see DEPLOYMENT.md Part B1).
# Fill in the placeholders below for your account, then:
#   git add -A && git commit -m "..." && ./deploy.sh
set -euo pipefail

SSH_HOST="yourdomain.com"          # or the server hostname GoDaddy gave you
SSH_USER="youruser"
APP_DIR="/home/youruser/digitanddata"

git push origin main

ssh "${SSH_USER}@${SSH_HOST}" bash -s <<EOF
  set -e
  cd "${APP_DIR}"
  git pull origin main
  source /home/${SSH_USER}/virtualenv/digitanddata/*/bin/activate
  pip install -r requirements.txt
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  mkdir -p tmp && touch tmp/restart.txt
EOF

echo "Deployed."
