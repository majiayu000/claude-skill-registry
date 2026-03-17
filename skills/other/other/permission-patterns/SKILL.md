---
name: permission-patterns
description: Rules for evaluating, classifying, and deduplicating AI tool permissions
version: "1.0.0"
author: "JacobPEvans"
---

# Permission Patterns

<!-- markdownlint-disable-file MD013 -->

Unified patterns for permission safety classification and deduplication. Use these rules to evaluate permissions consistently.

## Safety Classification

Classification rules for evaluating permission safety. Use these criteria to categorize permissions consistently.

### Classification Rules

#### ALLOW - Read-Only and Safe Operations

Keywords: `list`, `ls`, `show`, `info`, `view`, `get`, `describe`, `inspect`, `status`, `doctor`, `ping`, `check`, `--version`, `--help`

Safe domains: github.com, docker.com, kubernetes.io, python.org, npmjs.com, official documentation sites

#### ASK - Modifications and Risky Operations

Keywords: `update`, `set`, `edit`, `patch`, `modify`, `apply`, `rm`, `delete`, `remove`, `prune`, `clean`, `exec`, `run`, `eval`, `push`, `publish`, `deploy`, `kill`, `stop`

Requires user confirmation before execution.

#### DENY - Irreversible Damage or Security Bypass

Keywords: `sudo`, `chmod 777`, `dd`, file patterns like `**/.env`, `**/*_rsa`, `**/*.key`, `**/*secret*`

Local addresses: `localhost`, `127.0.0.1`, private IP ranges

### Decision Criteria

1. **Read-only query + no secrets** → ALLOW
2. **Modifies resources + reversible** → ASK
3. **Irreversible or security risk** → DENY
4. **Uncertain** → ASK (conservative default)

### Domain Coverage

Claude Code's `WebFetch(domain:X)` uses **exact host matching** — subdomains are NOT covered by a root domain entry:

- **`github.com`** does NOT cover `api.github.com` or `docs.github.com` — each needs its own entry
- **`github.io`** does NOT cover `github.github.io` — separate entry required
- **`githubusercontent.com`** and `raw.githubusercontent.com` are separate entries (different hostnames)
- **`localhost`** is separate from `localhost:3000` (ports are distinct)

Each hostname that needs to be fetched must be listed explicitly.

Local/private addresses always DENY:

- `localhost`, `127.0.0.1`, `192.168.x.x`, `10.x.x.x` ranges

---

## Pattern Deduplication

Rules for detecting when a specific permission is already covered by a broader existing pattern.

### Coverage Rules

#### WebFetch Domains

Each hostname must be listed exactly — there is no wildcard or subdomain coverage. Ports are also distinct:

- `localhost` does NOT cover `localhost:3000`

#### File Paths

Broader wildcards cover more specific patterns:

- `Read(**)` covers any Read permission
- `Glob(**/*)` covers `Glob(**/*.js)`, `Glob(**/package.json)`

### Hostname Recommendations

Since `WebFetch` uses exact host matching, list each hostname explicitly. When multiple hostnames share a
common vendor, add all needed hostnames individually rather than assuming a root domain covers them.

### Related Permission Suggestions

When discovering a safe permission, suggest related safe commands in the same family:

- `docker volume ls` → suggest `docker volume inspect`
- `aws s3 ls` → suggest `aws s3 sync --dryrun`
- `npm list` → suggest `npm outdated`, `npm audit`

---

## Commands Using This Skill

- `permissions-analyzer` agent - Uses classification and deduplication to filter permissions during discovery
- `/sync-permissions` command - Indirectly uses this skill through the permissions-analyzer agent
