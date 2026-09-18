# Deploying to GoDaddy Shared Linux Hosting

This project is a Django app served on GoDaddy shared hosting through
cPanel's **"Setup Python App"** feature (which is backed by Phusion
Passenger). It uses:

- **PyMySQL** as the database driver (no C compiler needed on shared hosting)
- **WhiteNoise** to serve static files directly from Django (no separate
  static file server needed)
- **`passenger_wsgi.py`** as the entry point Passenger loads
- **`.env`** (via `python-dotenv`) for configuration — never committed to git

There are two parts to this guide:

- **Part A** — one-time initial setup on a fresh GoDaddy account
- **Part B** — the repeatable, low-hassle way to push future changes live

---

## Part A — One-time initial deployment

### A0. Prerequisites

- A GoDaddy Linux shared/cPanel hosting plan (Economy and up all include
  "Setup Python App" and "Git™ Version Control" under cPanel)
- cPanel login for the account
- A private GitHub (or GitLab/Bitbucket) repository for this project's code
- Your domain already pointed at the GoDaddy hosting account

### A1. Create the MySQL database

In cPanel → **MySQL® Databases**:

1. Create a database, e.g. `digitanddata` — cPanel will prefix it with your
   username, giving something like `youruser_digitanddata`.
2. Create a database user and password, then **add the user to the
   database** with **All Privileges**.
3. Note the final prefixed database name and username — you'll need them
   for `.env` in step A6.

### A2. Create the Python app (cPanel → Setup Python App)

1. cPanel → **Setup Python App** → **Create Application**.
2. **Python version**: pick the highest 3.9+ available.
3. **Application root**: a folder name, e.g. `digitanddata` (this becomes
   `/home/<cpanel-user>/digitanddata`).
4. **Application URL**: your domain or subdomain (e.g. `/` for the root
   domain, or a subdomain for staging).
5. **Application startup file**: `passenger_wsgi.py`
6. **Application Entry point**: `application`
7. Click **Create**. cPanel will:
   - Create the application root directory
   - Create a dedicated virtualenv at
     `/home/<cpanel-user>/virtualenv/digitanddata/<py-version>/`
   - Generate its own placeholder `passenger_wsgi.py` (you'll overwrite this
     with the project's own version, which already does the right thing —
     see `passenger_wsgi.py` in this repo)
8. Copy the **"Enter to the virtual environment"** command cPanel shows you
   (something like `source /home/<user>/virtualenv/digitanddata/3.11/bin/activate
   && cd /home/<user>/digitanddata`) — you'll use this in cPanel's Terminal
   whenever you need to run manual commands.

### A3. Push this project to GitHub

From your local machine, in this project directory:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

> `.gitignore` already excludes `venv/`, `.env`, `*.sqlite3`, `staticfiles/`,
> and `media/` — secrets and local artifacts never reach GitHub.

### A4. Connect the GoDaddy app root to your git repo

In cPanel → **Git™ Version Control** → **Create**:

1. **Clone URL**: your GitHub repo's URL.
2. **Repository Path**: point it at the **same directory** Setup Python App
   created — e.g. `/home/<cpanel-user>/digitanddata`. Cloning directly into
   the app root (instead of a separate `repository/` folder cPanel deploys
   *from*) means a "Deploy" simply updates the live files in place — no
   separate copy step.
3. If cPanel warns the directory isn't empty, that's fine — Setup Python App
   only put a placeholder `passenger_wsgi.py` and a `tmp/` folder there, and
   the clone will just add the rest of the project's files.

This repo already includes a **`.cpanel.yml`** file. cPanel automatically
runs the commands under `deployment.tasks` in it every time you click
**Deploy HEAD Commit** — that's what makes Part B a one-click operation. It:

1. Installs/updates dependencies from `requirements.txt` into the app's
   virtualenv
2. Runs `manage.py migrate`
3. Runs `manage.py collectstatic`
4. Touches `tmp/restart.txt` so Passenger reloads the new code

Open `.cpanel.yml` and fill in the `DEPLOYPATH`/virtualenv paths for your
account (they're placeholders — see the comments in the file).

### A5. First deploy

In cPanel → Git Version Control → manage the repo → **Pull or Deploy** tab →
**Update from Remote**, then **Deploy HEAD Commit**. Watch the task output;
the first run will fail at the `.env`-dependent steps until you complete A6
below, which is expected.

### A6. Create the production `.env`

`.env` is intentionally gitignored, so it never lands on the server via git.
Create it once, directly on the server, via cPanel **File Manager** (or the
Terminal) at `/home/<cpanel-user>/digitanddata/.env`:

```
SECRET_KEY=<a long random string — generate one, don't reuse the dev one>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=mysql
DB_NAME=youruser_digitanddata
DB_USER=youruser_dbuser
DB_PASSWORD=<the db user's password>
DB_HOST=localhost
DB_PORT=3306
```

Then re-run **Deploy HEAD Commit** (or just the migrate/collectstatic
commands manually in Terminal) so the app picks it up.

### A7. Create an admin user

In cPanel Terminal, using the "enter virtualenv" command from A2:

```bash
source /home/<user>/virtualenv/digitanddata/<py-version>/bin/activate
cd /home/<user>/digitanddata
python manage.py createsuperuser
```

### A8. (Optional) Bring over existing local data

If your local `db.sqlite3` already has real content (leads, testimonials,
curricula) you want on production MySQL:

```bash
# locally
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission > data.json

# upload data.json to the server, then on the server:
python manage.py loaddata data.json
```

### A9. SSL

cPanel → **SSL/TLS Status** → run **AutoSSL** (GoDaddy issues a free
Let's Encrypt certificate for the domain automatically). Confirm the site
loads over `https://`.

### A10. Verify

Visit the domain. Check `/admin/` logs in with the superuser from A7, and
spot-check a couple of pages that hit the database.

---

## Part B — Deploying future changes (no hassle)

Once Part A is done, every future change follows the same two steps:

1. **Locally**, commit and push as usual:

   ```bash
   git add -A
   git commit -m "Describe the change"
   git push origin main
   ```

2. **On GoDaddy**, cPanel → Git Version Control → your repo → **Pull or
   Deploy** → **Update from Remote** → **Deploy HEAD Commit**.

That single click re-runs `.cpanel.yml`: it pulls your new commit into the
live app directory, reinstalls any changed dependencies, migrates the
database, regenerates static files, and restarts Passenger. No manual SSH
session needed for routine changes.

### B1. If your plan gives you SSH access

If SSH is enabled on the account (Settings → SSH Access in cPanel, or ask
GoDaddy support to enable it), you can skip the cPanel UI entirely and
deploy from your terminal in one command. Add this to the project (adjust
the placeholders for your account) and run it after every `git push`:

```bash
#!/usr/bin/env bash
# deploy.sh — push + deploy in one step, requires SSH access on the plan.
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
```

Save it as `deploy.sh`, `chmod +x deploy.sh`, and from then on:

```bash
git add -A && git commit -m "..." && ./deploy.sh
```

does the entire push-and-release cycle.

### B2. Rolling back

If a deploy breaks something:

```bash
git revert <bad-commit-sha>
git push origin main
```

then Deploy HEAD Commit (or `./deploy.sh`) again — this keeps history
linear and avoids force-pushes to the branch the server tracks. For an
emergency rollback without waiting on a revert commit, you can also check
out the previous commit directly on the server via cPanel's Git Version
Control UI ("Manage" → checkout a specific SHA) and redeploy.

### B3. Things that need a manual step (not covered by `.cpanel.yml`)

- **New environment variables**: edit `.env` on the server directly (File
  Manager or Terminal) — it's gitignored on purpose, so it's never
  overwritten by a deploy.
- **New third-party services / one-off data migrations**: run via cPanel
  Terminal as in A7.
- **Static file cache issues after a deploy**: WhiteNoise's
  `CompressedManifestStaticFilesStorage` fingerprints filenames by content
  hash, so browsers won't serve stale assets — no manual cache-busting
  needed.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| 500 error, blank page | Check `DEBUG=False` masks the real error — temporarily set `DEBUG=True` in the server `.env`, reload, then set it back |
| "No module named X" | `pip install -r requirements.txt` didn't run inside the app's virtualenv — re-run A2's activate command, then reinstall |
| Static files 404 | `collectstatic` wasn't run, or `STATIC_ROOT`/`STATICFILES_DIRS` paths don't match — re-run the deploy |
| DB connection errors | Double-check the cPanel-prefixed DB name/user in `.env` (A1) match exactly, and that the user was added to the database with privileges |
| Changes not showing after deploy | Passenger wasn't restarted — confirm `tmp/restart.txt` was touched, or click "Restart" in Setup Python App |
