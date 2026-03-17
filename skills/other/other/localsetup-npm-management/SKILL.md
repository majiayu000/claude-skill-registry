---
name: localsetup-npm-management
description: Manage Nginx Proxy Manager (NPM) reverse proxy hosts via its REST API using the native Python client npm_api.py. Use when creating, modifying, diagnosing, removing, or cleaning up proxy hosts, or when coordinating Docker service deployments with NPM routing.
metadata:
  version: "1.0"
---

# Nginx Proxy Manager (NPM) management

## Purpose

Give an AI agent the ability to manage reverse proxy configuration in Nginx Proxy Manager from the terminal. Covers create, modify, diagnose, remove, cleanup, and backup/restore workflows for proxy hosts, with coordinated Docker operations.

## When to use

- User asks to expose a new service via NPM (create proxy host).
- User asks to update, disable, enable, or reconfigure an existing proxy host.
- User asks to troubleshoot a 502, SSL error, WebSocket failure, or unreachable service.
- User asks to remove or decommission a service.
- User asks to prune orphan proxy hosts or unused Docker resources.
- User asks to backup or restore NPM configuration.

Do not use for NPM access lists, TCP/UDP streams, or redirection hosts (extend as needed).

## Tooling (framework standard)

The framework default is **Python 3.10+**. This skill uses `npm_api.py`, a native Python client that talks directly to the NPM REST API using only Python standard library (`urllib`, `json`, `configparser`). No Bash, no curl, no jq, no third-party packages required.

`npm_api.py` handles:
- Config loading from `npm-api.conf` with hostile-input sanitization.
- Token fetch and cache (auto-refreshes when less than 1 hour remains).
- All proxy host operations (list, search, show, create, update, enable, disable, delete).
- Backup of proxy hosts, users, settings, access lists, and certificates.
- Structured GFM output for agent and human consumption.
- Actionable STDERR errors with source context per INPUT_HARDENING_STANDARD.md.

## Prerequisites

- Python 3.10+ on the target machine (no other dependencies).
- Docker and Docker Compose running.
- NPM deployed in a container; admin API reachable (default: `http://127.0.0.1:81`).
- A shared Docker network (e.g. `npm_default`) that NPM and all public-facing containers are attached to.
- NPM admin credentials.

## Directory layout

```
<TOOLS_DIR>/npm-api/
    npm_api.py          # Native Python client (primary tool)
    npm-api.conf        # Local config (gitignored, chmod 600)
    npm-api.conf.example  # Template (safe to commit)
    data/               # Token cache and backup directory (auto-created)
```

Default `<TOOLS_DIR>`: `~/.localsetup/tools`. Adapt to environment.

## Config file (npm-api.conf)

```bash
NGINX_IP=127.0.0.1
NGINX_PORT=81
API_USER=admin@example.com
API_PASS=yourpassword
DATA_DIR=<TOOLS_DIR>/npm-api/data   # optional; defaults to data/ next to script
```

Set permissions: `chmod 600 <TOOLS_DIR>/npm-api/npm-api.conf`. Gitignore this file.

`npm_api.py` loads the config, fetches a bearer token, and caches it under `data/<IP_PORT>/token/`. Token refresh is automatic.

## Architecture rule

Every container that needs public HTTP/HTTPS access:
- Is attached to `<NPM_NETWORK>` (default: `npm_default`).
- Does NOT publish host ports 80 or 443.
- Has an NPM proxy host pointing to it by **Docker container name** (not IP).

NPM listens on 80/443 and forwards by hostname. Docker DNS resolves container names within the shared network.

Removing a service = delete NPM proxy host + stop/remove containers. Creating a service = deploy container on `<NPM_NETWORK>` + create NPM proxy host.

## Proxy host default template

| Parameter | Default |
|-----------|---------|
| forward_scheme | `http` |
| ssl_forced | `true` |
| http2_support | `true` |
| hsts_enabled | `false` |
| caching_enabled | `false` |
| block_exploits | `true` |
| allow_websocket_upgrade | `false` |
| access_list_id | `0` (none) |
| advanced_config | (empty) |

Use `forward_scheme: https` only when the container's internal port actually speaks TLS. Enable `allow_websocket_upgrade` only for apps that use WebSockets. Use `advanced_config` only for nginx-level tuning (e.g. `client_max_body_size 1000M`).

## Key commands

All commands are run as `python3 npm_api.py <flag> [args]`. No interactive prompts are ever shown.

| Action | Command |
|--------|---------|
| Check connectivity / token | `python3 npm_api.py --info` |
| List all proxy hosts | `python3 npm_api.py --host-list` |
| Search by domain | `python3 npm_api.py --host-search <domain>` |
| Show one host | `python3 npm_api.py --host-show <id>` |
| Create proxy host | `python3 npm_api.py --host-create <domain> -i <container> -p <port> [options]` |
| Update a field | `python3 npm_api.py --host-update <id> key=value [key=value ...]` |
| Enable | `python3 npm_api.py --host-enable <id>` |
| Disable | `python3 npm_api.py --host-disable <id>` |
| Delete | `python3 npm_api.py --host-delete <id>` |
| Backup | `python3 npm_api.py --backup` |

Optional flags for `--host-create`:

| Flag | Effect |
|------|--------|
| `--scheme https` | Use HTTPS to reach backend (default: http) |
| `--websocket` | Enable WebSocket upgrade |
| `--no-ssl-force` | Do not redirect HTTP to HTTPS |
| `--no-http2` | Disable HTTP/2 |
| `--hsts` | Enable HSTS header |
| `--caching` | Enable NPM caching |
| `--no-block-exploits` | Disable exploit blocking |
| `--access-list-id N` | Apply NPM access list N |
| `--advanced-config "..."` | Raw nginx config block |

Proxy host IDs are integers assigned by NPM. Always fetch a fresh list before modify, delete, or enable/disable. Do not reuse IDs from memory.

## Workflows

### Create (deploy service + expose via NPM)

1. Define the stack: attach public-facing containers to `<NPM_NETWORK>`. Do not publish ports 80 or 443.
2. Deploy: `docker compose up -d`
3. For each public container, gather: domain_names, forward_host (container name), forward_port, forward_scheme, WebSocket need.
4. Create proxy host: `python3 npm_api.py --host-create <domain> -i <container> -p <port> [options]`. Prompt user to attach an SSL certificate.
5. Optional: create the matching DNS record using `localsetup-cloudflare-dns`.
6. Verify: `python3 npm_api.py --host-search <domain>` and test the public URL.

### Modify (destructive, double confirmation required)

Safety gates:
1. User states intent.
2. Agent shows: proxy host ID(s), domain(s), container name(s), and a concise summary of what will change. Waits.
3. User must confirm with a phrase **containing the word "modify"** (e.g. "confirm modify"). Vague replies are not accepted.

Steps: identify current state (`python3 npm_api.py --host-list` and `docker inspect`), show changes, wait for confirmation, apply Docker-side changes, then update NPM proxy host if needed:

```
python3 npm_api.py --host-update <id> forward_host=<new_name>
python3 npm_api.py --host-update <id> forward_port=<new_port>
python3 npm_api.py --host-update <id> forward_scheme=https
```

### Diagnose (inspect and troubleshoot)

1. Get overview: `docker ps -a`, `docker network inspect <NPM_NETWORK>`, `python3 npm_api.py --host-list`, `python3 npm_api.py --info`.
2. Per service: check container logs, network membership (`docker inspect`), and proxy host config (`python3 npm_api.py --host-search <domain>`).
3. Common failure modes:

| Symptom | Check |
|---------|-------|
| 502 Bad Gateway | Container not on `<NPM_NETWORK>`, wrong port, container stopped |
| SSL errors | Certificate missing/expired, domain mismatch |
| Redirect loop | ssl_forced=true on backend that also redirects to HTTPS |
| WebSocket failure | allow_websocket_upgrade not enabled |
| "Not found" / wrong app | forward_host or forward_port wrong |
| DNS not resolving | DNS record missing or not propagated |

4. Connectivity test from NPM container: `docker exec <npm_container> curl -s http://<backend>:<port>/`

### Remove (destructive, double confirmation required)

Safety gates:
1. User states intent.
2. Agent shows: proxy host ID, domain, container name. For multiple items: numbered list, user selects by number, agent echo-backs selection. Waits.
3. User must confirm with a phrase **containing the word "remove"** (e.g. "confirm remove").

Steps:
1. `python3 npm_api.py --host-list` to identify targets.
2. Apply multi-item selection protocol if multiple candidates.
3. `python3 npm_api.py --host-delete <id>` for each confirmed target.
4. Stop and remove containers. Warn before removing volumes (irreversible).

### Cleanup (destructive, double confirmation required)

Removes orphan NPM proxy hosts (no running backend) and unused Docker resources.

Safety gates: same double confirmation as Remove; second confirmation must include "cleanup".

1. Build candidate list: `python3 npm_api.py --host-list` then check each host's backend with `docker ps`. List stopped containers, dangling images, unused networks.
2. Present numbered list. User selects by number. Agent echoes back selection.
3. After "confirm cleanup": `python3 npm_api.py --host-delete <id>` for each orphan, then targeted Docker prune commands.

Warn separately before `docker volume prune` (data loss risk).

### Backup and Restore

Backup is non-destructive; no double confirmation required.

Restore is destructive: show exactly what will be overwritten, require double confirmation with phrase containing "restore".

Backup:
1. `python3 npm_api.py --backup` (writes proxy hosts, users, settings, access lists, and certificates to `DATA_DIR/<ip_port>/backups/<timestamp>/`).
2. Copy compose/stack files to `~/.localsetup/backups/compose/`.

Restore: NPM does not expose a REST restore endpoint. Re-import from backup by re-running the Create workflow for each proxy host using the saved `proxy_hosts.json`. For certificates, re-attach via NPM UI.

## Agent behavior rules

- Confirm NPM API is reachable before any workflow: `python3 npm_api.py --info`.
- Know `<NPM_NETWORK>` for the target environment before running Create or Modify.
- Always use Docker container name as `forward_host` for containers on `<NPM_NETWORK>`. Never use container IPs.
- After creating a proxy host, always prompt user about SSL certificate attachment.
- For multi-item destructive operations: numbered list, user selection by number, echo-back, named confirmation phrase.
- If `npm_api.py` exits non-zero, the STDERR message is actionable; surface it to the user verbatim.
- If the API token is stale, `npm_api.py` auto-refreshes. If that fails, the error message will specify which config field to check (NGINX_IP, NGINX_PORT, API_USER, or API_PASS).
- Set `LOCALSETUP_DEBUG=1` before the command for full HTTP trace output when diagnosing connectivity issues.
- Warn if a container is not found on `<NPM_NETWORK>` when creating a proxy host.

## Placeholders reference

| Placeholder | Meaning | Example |
|-------------|---------|---------|
| `<TOOLS_DIR>` | Root of tools directory | `~/.localsetup/tools` |
| `<NPM_API>` | Path to npm_api.py | `~/.localsetup/tools/npm-api/npm_api.py` |
| `<NPM_NETWORK>` | Shared Docker network name | `npm_default` |
| `<BACKUP_DIR>` | Backup directory for compose files | `~/.localsetup/backups/compose` |

## Security

- `npm-api.conf` is gitignored; permissions must be `600`.
- NPM admin port (81) must not be exposed to the internet.
- Use a strong NPM admin password.
- The `data/` backup directory may contain SSL private keys; restrict permissions accordingly.

## Reference

- scripts/npm_api.py - Native Python client (source of truth)
- references/npm-api-conf-example.md - Config file template and field reference
- references/proxy-host-template.md - Full default template with all fields
- https://github.com/NginxProxyManager/nginx-proxy-manager - NPM project (API source)
- https://github.com/NginxProxyManager/nginx-proxy-manager/tree/develop/backend/schema - NPM API schema
