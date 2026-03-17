---
name: skriptoteket-devops
description: DevOps and server management for Skriptoteket on home server (hemma.hule.education). Branched skill covering deploy, database, users, CLI, security, network, DNS, and troubleshooting.
---

# Skriptoteket DevOps

Compact skill for managing Skriptoteket on home server.

Source of truth for ops in this repo:

- Home server ops: `docs/runbooks/runbook-home-server.md`
- GPU AI ops: `docs/runbooks/runbook-gpu-ai-workloads.md`
- Tabby ops: `docs/runbooks/runbook-tabby-codemirror.md`
- Observability ops: `docs/runbooks/runbook-observability.md`

## ROCm / AMDGPU installer flags (hemma)

- List supported usecases: `ssh hemma "amdgpu-install --list-usecase"`
- ROCm (headless/compute): `ssh hemma "sudo amdgpu-install -y --usecase=rocm"`
- Graphics + ROCm (Mesa + compute): `ssh hemma "sudo amdgpu-install -y --usecase=graphics,rocm"`
- Notes:
  - "Mesa graphics" == `graphics` (open source Mesa 3D + multimedia libs).
  - `workstation` is deprecated (and now maps to Mesa anyway); prefer `graphics`.

## When to Use

Activate when the user:
- Needs to deploy changes to home server
- Wants to manage database (backup/restore/migrations)
- Creates or manages users (bootstrap, provision)
- Troubleshoots errors (502, 307, 500)
- Works with SSL/certificates
- Has DNS/DDNS issues
- Needs to run CLI commands in container
- Wants to seed or sync the script bank

---

## Critical Configuration (Copy-Paste Ready)

### SSH Access (Passwordless)

```bash
ssh hemma              # paunchygent (non-root default)
ssh hemma-root         # root (use only with explicit approval)
ssh hemma-local        # LAN, non-root
ssh hemma-local-root   # LAN, root
```

Notes (hemma):

- Default to non-root (`ssh hemma`); use `ssh hemma-root` only after explicit approval.
- Non-root key: `~/.ssh/hemma-paunchygent_ed25519` (local).
- Health-gated hardware watchdog handles recovery: `/usr/local/bin/health-watchdog.sh` + `health-watchdog.service` pets `/dev/watchdog0` only when health checks pass (sshd/port 22, default route, link up, gateway ping). Boot ordering is pinned via `/etc/systemd/system/health-watchdog.service.d/10-watchdog-order.conf` (starts after `sp5100-tco-watchdog.service`; waits for `/dev/watchdog0` node). systemd watchdog is disabled via `/etc/systemd/system.conf.d/99-watchdog.conf`, and `sp5100_tco` is loaded with `nowayout=1 heartbeat=60` via `/etc/modprobe.d/sp5100_tco.conf`. Reboot persistence: `watchdog.stop_on_reboot=0` in `/etc/default/grub` + `/etc/default/kdump-tools`. Logs in `journalctl -t health-watchdog`.
- Heartbeat log tag: `journalctl -t heartbeat`.
- Host incident/SMART logs: `/root/logs/incident-*.log`, `/root/logs/smart/` (cleanup via `cleanup-smart-logs.timer`).
- Docker commands require `sudo` (passwordless sudo is configured). If you use `sudo -n`, the command fails fast instead of prompting.
- Prefer `rg` (ripgrep) for repo search; if missing: `sudo apt-get install -y ripgrep`.
- For a friendlier CLI on `hemma`, expect `fd`, `bat`, `fzf`, `jq`, `tree`, and `yq` (mikefarah/yq v4). Ubuntu packages name some of these as `fdfind`/`batcat`, so we symlink `fdfind→fd` and `batcat→bat` (see `docs/runbooks/runbook-home-server.md`).
- If any are missing: `sudo apt-get update && sudo apt-get install -y fd-find bat fzf jq tree` (and install `yq` v4 to `/usr/local/bin/yq`).
- If you need UTC timestamps in Python, avoid `datetime.utcnow()` (deprecated on 3.12+); use timezone-aware UTC like `datetime.now(UTC)` instead.
- SSH abuse protection: Fail2ban runs `sshd` + `recidive` (3 strikes within 7d => permaban); see `docs/runbooks/runbook-home-server.md`.
- Edge hardening: nginx-proxy drops common scanner traffic (e.g. `/.env`, `/.git`, `wp-*`, `*.php`, `cgi-bin`, WebDAV methods) at the proxy; see `docs/runbooks/runbook-home-server.md`.
- Observability: Promtail labels nginx-proxy access logs in Loki (`vhost`, `client_ip`, `method`, `status`); see `docs/runbooks/runbook-observability-logging.md`.


### Watchdog / Crash Recovery Guardrails (hemma)

- Separate ISP loss from local SSH/link failure; only count local failures toward reboot unless user explicitly opts in.
- Always verify runtime state before assumptions: `systemctl status ssh-watchdog.timer ssh-watchdog.service` and `/etc/default/ssh-watchdog`.
- Keep the hardware watchdog armed; disable systemd watchdog in the kdump initramfs to avoid petting in the crash kernel.
- Keep watchdog running across warm reboots (especially post-kdump SysRq reboot): `watchdog.stop_on_reboot=0` in `/etc/default/grub` + `/etc/default/kdump-tools`; apply with `update-grub` + reboot and `kdump-config unload && kdump-config load`.
- Run remote commands via script files (no inline quoting) to avoid shell/escape errors.

- Crash-kernel watchdog hardening uses initramfs hooks: `/etc/initramfs-tools/hooks/zz-kdump-disable-watchdog` (disable systemd petting) and `/etc/initramfs-tools/hooks/zz-kdump-watchdog-hardening` (include `sp5100_tco` module + `/etc/modprobe.d/sp5100_tco.conf`). Rebuild kdump initrd after changes.
- Crash-kernel watchdog must be *started* (module load alone isn’t enough): `kdump-watchdog-arm.service` + `/usr/local/sbin/kdump-watchdog-arm` opens `/dev/watchdog0` before `kdump-tools-dump.service`. Verify: `sudo journalctl -b -1 -u kdump-watchdog-arm.service --no-pager` includes `kdump-watchdog-arm: opened ... (state=active ...)`.
### Production Deployment

```bash
# ALWAYS use compose.prod.yaml for production
ssh hemma "cd ~/apps/skriptoteket && git pull && sudo docker compose -f compose.prod.yaml up -d --build"

# With migrations
ssh hemma "cd ~/apps/skriptoteket && git pull && sudo docker compose -f compose.prod.yaml up -d --build"
ssh hemma "sudo docker exec -e PYTHONPATH=/app/src skriptoteket-web pdm run db-upgrade"
```

Note: On `hemma`, systemd units may need absolute docker path (`/snap/bin/docker`) due to PATH differences.

### Background Image Builds (REQUIRED)
Run builds in background, log to `.artifacts/`, and give the user the `tail -f` command.
Template:
`LOG=.artifacts/runner-build-$(date -u +%Y%m%dT%H%M%SZ).log; nohup <build-cmd> > "$LOG" 2>&1 & echo "$LOG"; tail -f <log>`

### Env changes (prod)

```bash
# Edit: ~/apps/skriptoteket/.env (avoid duplicate keys; last wins)

# Apply env/compose changes (restart does NOT re-read .env)
ssh hemma "cd ~/apps/skriptoteket && sudo docker compose -f compose.prod.yaml up -d --no-deps --force-recreate web"
```

### Container Names

| Environment | Web Container | Worker Container | DB Container |
|-------------|---------------|------------------|--------------|
| Production | `skriptoteket-web` | `skriptoteket-worker` | `shared-postgres` (external) |
| Development | `skriptoteket_web` | `skriptoteket_worker` | `skriptoteket-db-1` |

### Database Connection

```bash
# Production DB (shared-postgres on hule-network)
DATABASE_URL=postgresql+asyncpg://skriptoteket:${SKRIPTOTEKET_DB_PASSWORD}@shared-postgres:5432/skriptoteket

# Dev DB (local container)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/skriptoteket

# Connect to prod DB via psql
ssh hemma "sudo docker exec -it shared-postgres psql -U skriptoteket -d skriptoteket"

# Connect to dev DB
ssh hemma "sudo docker exec -it skriptoteket-db-1 psql -U postgres -d skriptoteket"
```

### CLI Command Pattern (ALWAYS USE)

```bash
# The -e PYTHONPATH=/app/src is REQUIRED for all CLI commands (web + worker)
sudo docker exec -e PYTHONPATH=/app/src skriptoteket-web pdm run <command>
sudo docker exec -e PYTHONPATH=/app/src skriptoteket-worker pdm run <command>

# Non-interactive (scripts/CI): add -T
sudo docker exec -T -e PYTHONPATH=/app/src skriptoteket-web pdm run <command>
sudo docker exec -T -e PYTHONPATH=/app/src skriptoteket-worker pdm run <command>

# Interactive (prompts): add -it
sudo docker exec -it -e PYTHONPATH=/app/src skriptoteket-web pdm run <command>
sudo docker exec -it -e PYTHONPATH=/app/src skriptoteket-worker pdm run <command>
```

See also: `docs/runbooks/runbook-home-server.md` (systemd timer patterns use `/snap/bin/docker exec ...`).

### Worker healthcheck

The production worker container exposes a dependency healthcheck (DB + Docker socket + artifacts volume):

```bash
ssh hemma "sudo docker exec -e PYTHONPATH=/app/src skriptoteket-worker pdm run python -m skriptoteket.cli healthcheck-execution-worker"
```

### Admin Credentials (Script Bank Seeding)

```bash
# Default admin for seeding (set in .env on server)
SKRIPTOTEKET_SCRIPT_BANK_ACTOR_EMAIL=admin@hule.education
SKRIPTOTEKET_SCRIPT_BANK_ACTOR_PASSWORD=<from server .env>

# Seed command
ssh hemma "cd ~/apps/skriptoteket && sudo docker compose -f compose.prod.yaml exec -T -e PYTHONPATH=/app/src web pdm run python -m skriptoteket.cli seed-script-bank --actor-email admin@hule.education --actor-password 'PASSWORD'"
```

### Network Configuration

| Network | Purpose | Containers |
|---------|---------|------------|
| `hule-network` | Inter-service (nginx, shared-postgres) | nginx-proxy, skriptoteket-web, shared-postgres |
| `skriptoteket_default` | Compose internal (dev only) | skriptoteket_web, skriptoteket-db-1 |

**Critical:** Production web container must be on `hule-network` for nginx to reach it.

### File Paths on Server

```
~/apps/skriptoteket/           # App repo (git pull here)
~/apps/skriptoteket/.env       # Production secrets (never commit)
~/infrastructure/              # nginx-proxy, certbot
~/backups/                     # Database backups
/srv/storage/                  # Long-term data (HDD; models/data/archives)
/srv/backup/                   # Long-term backups (ext4)
/srv/scratch/                  # Fast ephemeral work (SSD; tmp/build/cache)
/root/logs/incident-*.log      # Incident log captures
/root/logs/smart/              # SMART snapshots
```

---

## Most Used Commands

### Deploy

```bash
# Standard deploy
ssh hemma "cd ~/apps/skriptoteket && git pull && sudo docker compose -f compose.prod.yaml up -d --build"

# With migrations
ssh hemma "sudo docker exec skriptoteket-web pdm run db-upgrade"

# Force recreate (config changes)
ssh hemma "cd ~/apps/skriptoteket && sudo docker compose -f compose.prod.yaml up -d --force-recreate"
```

### Database

```bash
# Backup
ssh hemma "sudo docker exec shared-postgres pg_dump -U skriptoteket skriptoteket > ~/backups/skriptoteket-\$(date +%Y%m%d).sql"

# Migrations
ssh hemma "sudo docker exec skriptoteket-web pdm run db-upgrade"
```

### Edit-ops context probe (dev, docker backend required)

Use this to verify that chat + edit-ops see the same virtual file base hashes.

```bash
# Ensure the dev stack is running (docker compose)
pdm run dev-start

# Run the probe (uses BOOTSTRAP_SUPERUSER_* from .env)
pdm run python scripts/chat_edit_ops_context_probe.py \
  --scenario scripts/edit_ops_scenarios/chat_edit_ops_context_example.json

# Inspect the captured summary + raw payloads
cat .artifacts/chat-edit-ops-context/<timestamp>/capture_summary.json
```

Notes:
- The probe talks to the docker-backed API at `http://127.0.0.1:8000`.
- Captures land under `.artifacts/llm-captures/chat_request_context/` and
  `.artifacts/llm-captures/chat_ops_response/`.

### Cleanup timers (systemd)

We enforce TTL-based cleanup using CLI commands + systemd timers (not cron). Examples:

- Sandbox snapshots cleanup: `cleanup-sandbox-snapshots`
- Login events cleanup (retention): `cleanup-login-events`
- Host log cleanup: `cleanup-smart-logs.timer` (incident + SMART logs, 30-day retention)

Exact unit definitions and schedules: `docs/runbooks/runbook-home-server.md`.

### Users

```bash
# Bootstrap superuser (first time)
ssh hemma "sudo docker exec -it -e PYTHONPATH=/app/src skriptoteket-web pdm run python -m skriptoteket.cli bootstrap-superuser --email admin@hule.education"

# Provision user
ssh hemma "sudo docker exec -T -e PYTHONPATH=/app/src skriptoteket-web pdm run python -m skriptoteket.cli provision-user --actor-email admin@hule.education --actor-password 'ADMIN_PASS' --email user@example.com --password 'USER_PASS' --role contributor"
```

### Logs

```bash
ssh hemma "sudo docker logs -f skriptoteket-web"
ssh hemma "sudo docker logs -f nginx-proxy"

# Host AI services (llama.cpp + tabby)
ssh hemma "sudo systemctl status --no-pager llama-server-rocm.service tabby.service | head -n 60"
ssh hemma "sudo journalctl -u llama-server-rocm.service -n 200 --no-pager"
ssh hemma "sudo journalctl -u tabby.service -n 200 --no-pager"
ssh hemma "curl -s http://127.0.0.1:8082/health"
ssh hemma "curl -s http://127.0.0.1:8083/v1/health"
```

### Status

```bash
ssh hemma "sudo docker ps | grep -E 'skriptoteket|nginx|postgres'"
```

---

## Local Dev (DX)

```bash
# Fast local iteration with log piping
pdm run dev-logs
pdm run fe-dev-logs
pdm run dev-local

# Full dev containers + logs
pdm run dev-start
pdm run dev-containers-logs

# Rebuild containers when deps/reload are flaky
pdm run dev-rebuild
```

---

## GPU Tunnels (Local Workstation)

```bash
~/bin/hemma-gpu-tunnel start        # start llama + tabby tunnels
~/bin/hemma-gpu-tunnel start-llama  # start only llama tunnel (:8082)
~/bin/hemma-gpu-tunnel start-tabby  # start only tabby tunnel (:8083)
~/bin/hemma-gpu-tunnel stop         # stop both tunnels
~/bin/hemma-gpu-tunnel stop-llama   # stop only llama tunnel (:8082)
~/bin/hemma-gpu-tunnel stop-tabby   # stop only tabby tunnel (:8083)
~/bin/hemma-gpu-tunnel status       # show tunnel status
```

---

## Branch Routing

| Task | Branch |
|------|--------|
| Deploy, rebuild, rollback | `branches/deploy.md` |
| PostgreSQL backup/restore | `branches/database.md` |
| Superuser, provision users | `branches/users.md` |
| Script bank seeding | `branches/seed.md` |
| CLI commands in container | `branches/cli.md` |
| SSL certificates, nginx | `branches/security.md` |
| Docker networks, 502 errors | `branches/network.md` |
| DNS, DDNS, Namecheap | `branches/dns-provider.md` |
| Ubuntu, disk, docker system | `branches/server-os.md` |
| All troubleshooting patterns | `branches/troubleshoot.md` |

---

## Quick Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 502 Bad Gateway | Web not on hule-network | `sudo docker network connect hule-network skriptoteket-web` |
| 307 to HTTP | Missing proxy headers | Check `--proxy-headers` in serve command |
| 500 on all routes | Missing migrations | `sudo docker exec skriptoteket-web pdm run db-upgrade` |
| "No module skriptoteket" | Missing PYTHONPATH | Add `-e PYTHONPATH=/app/src` |

---

## Research Documentation

Full research: `docs/reference/reports/ref-devops-skill-research.md`

## Maintenance note

This skill includes deeper branches under `.claude/skills/skriptoteket-devops/branches/`.
Keep those branch docs aligned with the runbooks above when ops patterns change.
