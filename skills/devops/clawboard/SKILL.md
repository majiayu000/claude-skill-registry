---
name: clawboard
description: "Install and operate Clawboard with OpenClaw. Use for scripted/manual/agentic install, token setup, Docker startup, logger plugin wiring, and validation."
---

# Clawboard

## Status

- ClawHub: **not available yet**.
- Install path today: scripted bootstrap or manual repo install.
- If OpenClaw is missing and user wants Chutes provider, start with [`add_chutes.sh`](../../inference-providers/add_chutes.sh) after creating a `https://chutes.ai` account.

## Current Architecture Snapshot

- `web` (Next.js): `http://localhost:3010`
- `api` (FastAPI + SQLite): `http://localhost:8010`
- `classifier` (async stage-2 worker): topic/task classification loop
- `qdrant` (vector index): dense retrieval backend on internal Docker network
- `clawboard-logger` plugin: stage-1 firehose logging + response-time context extension

Retrieval/search stack:

- Dense vectors + BM25 + lexical matching
- Reciprocal rank fusion + reranking
- Qdrant primary, SQLite embeddings mirror/fallback

## Goal

Get a user to a working Clawboard install where:

1. Clawboard web/api/classifier are running.
2. `clawboard-logger` plugin is installed and enabled.
3. Token flow is configured correctly (required for writes + non-localhost reads).
4. OpenClaw gateway is restarted and logging into Clawboard.

## Hard Rules (Repo vs Installed Skill)

- Repo copy (version controlled): `$CLAWBOARD_DIR/skills/clawboard`
- Installed skill path (what OpenClaw reads): `$HOME/.openclaw/skills/clawboard`
- **Default install mode is symlink** (`~/.openclaw/skills/clawboard -> $CLAWBOARD_DIR/skills/clawboard`).
- Detect mode deterministically at runtime:

```bash
if [ -L "$HOME/.openclaw/skills/clawboard" ]; then
  echo "symlink"
else
  echo "copy"
fi
```

- In **symlink mode** (default), repo edits are immediately visible to OpenClaw.
- In **copy mode**, repo edits do not update OpenClaw until you sync/copy again. After skill file changes (SKILL.md, `agents/`, `references/`, `scripts/`), sync into OpenClaw:

```bash
cd "$CLAWBOARD_DIR"
bash scripts/sync_openclaw_skill.sh --to-openclaw --apply --force
```

- If you changed files under `~/.openclaw/skills/clawboard` while in copy mode, sync them back before committing:

```bash
cd "$CLAWBOARD_DIR"
bash scripts/sync_openclaw_skill.sh --to-repo --apply
```

## Workspace + Runtime Assumptions (for coding tasks)

- Typical repo locations for Clawboard code:
  - `~/[agent_name]/clawboard`
  - `~/[agent_name]/projects/clawboard`
- For scripted installs, bootstrap auto-detects OpenClaw workspace conventions and usually lands in one of those layouts.
- When asked to work on Clawboard frontend/backend, prefer the active git repo copy under those locations, not `~/.openclaw/skills/*`.
- After typical bootstrap, assume Docker services are running:
  - `CLAWBOARD_WEB_HOT_RELOAD=1`: `web-dev` is used for Next.js hot reload (`web` is stopped).
  - `CLAWBOARD_WEB_HOT_RELOAD=0`: production-style `web` service is used.
- Fast runtime check commands:
  - `docker compose ps`
  - `echo "$CLAWBOARD_WEB_HOT_RELOAD"` (or read from `$CLAWBOARD_DIR/.env`)
  - `curl -s http://localhost:8010/api/health`
- Parity rules while editing:
  - Skill path mode should be checked first (`test -L ~/.openclaw/skills/clawboard`).
  - If symlink mode: edit repo files directly (`$CLAWBOARD_DIR/skills/clawboard/**`).
  - If copy mode: sync to OpenClaw after edits (`bash scripts/sync_openclaw_skill.sh --to-openclaw --apply --force`).
  - Logger plugin edits (`extensions/clawboard-logger/**`) must be reinstalled/enabled in OpenClaw:
    - `openclaw plugins install -l "$CLAWBOARD_DIR/extensions/clawboard-logger"`
    - `openclaw plugins enable clawboard-logger`
  - `~/.openclaw/skills/clawboard-logger` is optional and may not exist by default. If your environment has it, keep it synced with its repo copy explicitly.

## Install Modes

### 1) Quick Scripted Install (recommended)

Use:

```bash
curl -fsSL https://raw.githubusercontent.com/sirouk/clawboard/main/scripts/bootstrap_openclaw.sh | bash
```

What the script does:

- Clones/updates repo by auto-detecting your OpenClaw workspace. If it finds a `projects/` (or `project/`) convention, it installs there; otherwise it falls back to `~/clawboard`.
  - Override with `--dir <path>`, `CLAWBOARD_DIR=<path>`, or `CLAWBOARD_PARENT_DIR=<path>` (installs to `<parent>/clawboard`).
- Generates a token if missing and writes `.env` with `CLAWBOARD_TOKEN`.
- Detects browser access URLs (Tailscale if available, else localhost) and writes `.env` `CLAWBOARD_PUBLIC_API_BASE` and `CLAWBOARD_PUBLIC_WEB_URL`.
- Builds and starts Docker services.
- Ensures `web` + `api` + `classifier` + `qdrant` are running.
- Installs skill at `$HOME/.openclaw/skills/clawboard` (default: symlink to repo skill; optional copy mode).
- Installs/enables `clawboard-logger` plugin.
- Writes plugin config (`baseUrl`, `token`, `enabled`) via `openclaw config set`.
- Ensures OpenClaw OpenResponses endpoint is enabled (`POST /v1/responses`) for attachments.
- Restarts OpenClaw gateway.
- Sets `/api/config` title + integration level.

If `openclaw` CLI is not installed yet, the script still deploys Clawboard and prints follow-up instructions.
It now also offers to run the Chutes fast path automatically when `openclaw` is missing.

Useful flags:

- `--integration-level full|write|manual` (default `write`)
- `--no-backfill` (same as `manual`)
- `--api-url http://localhost:8010`
- `--web-url http://localhost:3010`
- `--web-hot-reload` / `--no-web-hot-reload`
- `--public-api-base https://api.example.com`
- `--public-web-url https://clawboard.example.com`
- `--token <token>`
- `--title "<name>"`
- `--skill-symlink` (default)
- `--skill-copy` (fallback if you do not want symlink mode)
- `--update`

### 2) Human Manual Install

Prereqs:

- `git`, `docker` (+ compose), `openclaw` CLI
- Docker Desktop on macOS

Steps:

1. Clone repo:

```bash
CLAWBOARD_PARENT_DIR="${CLAWBOARD_PARENT_DIR:-}"
CLAWBOARD_DIR="${CLAWBOARD_DIR:-${CLAWBOARD_PARENT_DIR:+$CLAWBOARD_PARENT_DIR/clawboard}}"
CLAWBOARD_DIR="${CLAWBOARD_DIR:-$HOME/clawboard}"
git clone https://github.com/sirouk/clawboard "$CLAWBOARD_DIR"
cd "$CLAWBOARD_DIR"
```

2. Create token and env:

```bash
cp .env.example .env
openssl rand -hex 32
```

Set `CLAWBOARD_TOKEN=<value>` in `$CLAWBOARD_DIR/.env`.
Set `CLAWBOARD_PUBLIC_API_BASE=<browser-reachable-api-url>` in `$CLAWBOARD_DIR/.env`.
Optional: set `CLAWBOARD_PUBLIC_WEB_URL=<browser-reachable-ui-url>` in `$CLAWBOARD_DIR/.env`.
Examples:

- local: `http://localhost:8010`
- tailscale: `http://100.x.y.z:8010`
- custom domain: `https://api.example.com`

3. Start Clawboard:

```bash
docker compose up -d --build
```

4. Install skill:

```bash
mkdir -p "$HOME/.openclaw/skills"
rm -rf "$HOME/.openclaw/skills/clawboard"
ln -s "$CLAWBOARD_DIR/skills/clawboard" "$HOME/.openclaw/skills/clawboard"
```

If you explicitly want copy mode instead of symlink:

```bash
mkdir -p "$HOME/.openclaw/skills"
rm -rf "$HOME/.openclaw/skills/clawboard"
cp -R "$CLAWBOARD_DIR/skills/clawboard" "$HOME/.openclaw/skills/clawboard"
```

If user keeps skills elsewhere, use that path instead of `$HOME/.openclaw/skills`.

5. Install + enable logger plugin:

```bash
openclaw plugins install -l "$CLAWBOARD_DIR/extensions/clawboard-logger"
openclaw plugins enable clawboard-logger
```

6. Configure plugin (writes into OpenClaw config):

```bash
# contextMode options: auto | cheap | full | patient
openclaw config set plugins.entries.clawboard-logger.config --json '{
  "baseUrl":"http://localhost:8010",
  "token":"YOUR_TOKEN",
  "enabled":true,
  "contextMode":"auto",
  "contextFallbackMode":"cheap",
  "contextFetchTimeoutMs":1200,
  "contextTotalBudgetMs":2200,
  "contextMaxChars":2200
}'
openclaw config set plugins.entries.clawboard-logger.enabled --json true
```

7. Enable OpenResponses (recommended for attachments):

```bash
openclaw config set gateway.http.endpoints.responses.enabled --json true
```

8. Restart gateway:

```bash
openclaw gateway restart
```

Notes:

- OpenClaw config is stored at `$HOME/.openclaw/openclaw.json`.
- Keep plugin `token` aligned with API server `CLAWBOARD_TOKEN`.

### 3) Agentic Install (copy/paste into OpenClaw)

Use this exact prompt:

```md
Install Clawboard for me end-to-end. ClawHub is not available yet, so choose one of these:

1) Scripted install (preferred):
- Run: curl -fsSL https://raw.githubusercontent.com/sirouk/clawboard/main/scripts/bootstrap_openclaw.sh | bash

2) Manual install:
- Clone repo to `$CLAWBOARD_DIR`
- Create `CLAWBOARD_TOKEN` and write `$CLAWBOARD_DIR/.env`
- Set `CLAWBOARD_PUBLIC_API_BASE` (local/Tailscale/custom domain) in `$CLAWBOARD_DIR/.env`
- Set `CLAWBOARD_PUBLIC_WEB_URL` (local/Tailscale/custom domain) in `$CLAWBOARD_DIR/.env`
- Start docker compose
- Symlink skill to $HOME/.openclaw/skills/clawboard (default; copy only if explicitly requested)
- Install/enable clawboard-logger plugin
- Set plugin config (baseUrl + token) in OpenClaw config
- Restart gateway

After install, validate:
- http://localhost:8010/api/health
- http://localhost:8010/api/config
- plugin enabled + gateway restarted
- send one test message and confirm it appears in Clawboard logs

Ask me before choosing local vs Tailscale API base URL.
```

Security reminder for all methods:

- `CLAWBOARD_TOKEN` is required for all writes and all non-localhost reads.
- Localhost reads can run tokenless (read-only default posture).
- Keep network boundaries strict (localhost/firewall/Tailscale ACLs; avoid Funnel/public exposure unless explicitly intended).
- Compose defaults keep vector/db/cache services off host ports; use the API as the supported read/write/delete interface.

## Validation Checklist

Run:

```bash
curl -s http://localhost:8010/api/health
curl -s http://localhost:8010/api/config
openclaw plugins list | rg clawboard-logger
curl -s "http://localhost:8010/api/search?q=continuity"
```

Expect:

- API health is `ok`.
- `tokenRequired` is `true`.
- `tokenConfigured` is `true`.
- Logger plugin is enabled.
- Search endpoint returns mode/details (and will include qdrant mode when vectors are available).
- New OpenClaw message appears in Clawboard Logs.

## Optional Helpers

- Local memory setup script:
  - `$CLAWBOARD_DIR/skills/clawboard/scripts/setup-openclaw-local-memory.sh`
- **Curated memory cloud backup (GitHub private repo):**
  - Setup (interactive):
    - `$CLAWBOARD_DIR/skills/clawboard/scripts/setup-openclaw-memory-backup.sh`
  - Backup run (safe for automation; commits/pushes only when changed):
    - `$CLAWBOARD_DIR/skills/clawboard/scripts/backup_openclaw_curated_memories.sh`
  - Includes optional full Clawboard state export (config/topics/tasks/logs + optional attachments).
  - Stores config at:
    - `$HOME/.openclaw/credentials/clawboard-memory-backup.json` (chmod 600)
- Chutes provider helper:
  - `curl -fsSL https://raw.githubusercontent.com/sirouk/clawboard/main/inference-providers/add_chutes.sh | bash`

## References

- `references/clawboard-api.md`
- `references/openclaw-hooks.md`
- `references/openclaw-memory-local.md`
