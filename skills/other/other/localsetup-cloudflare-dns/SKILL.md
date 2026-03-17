---
name: localsetup-cloudflare-dns
description: Manage Cloudflare DNS records (list, create, modify, delete) and run zone surveys via the flarectl CLI and a Python wrapper. Use when adding, changing, or removing DNS records, surveying zones, or scheduling automated DNS snapshots.
metadata:
  version: "1.0"
---

# Cloudflare DNS management

## Purpose

Give an AI agent the ability to manage DNS records in a Cloudflare account from the terminal. Covers list, create, modify, and delete operations across multiple zones, plus zone surveys and automated survey scheduling.

All operations use a Python wrapper around `flarectl` (the official Cloudflare CLI). No browser or Cloudflare UI is required.

## When to use

- User asks to add, update, or remove a DNS record.
- User asks to list or inspect DNS records for a domain.
- User asks to run a DNS zone survey or snapshot.
- User asks to schedule automated DNS refreshes.
- Natural follow-on after creating an NPM proxy host (to create the matching A/CNAME record).

Do not use for Cloudflare Pages, Workers, or any Cloudflare service beyond DNS.

## Tooling (framework standard)

The framework default is **Python 3.10+**. The wrapper script (`cf_dns.py`) is written in Python and replicates all behaviors described in the PRD: token loading, binary resolution, argument pass-through, error surfacing. Shell scripts referenced in the PRD (cf-dns.sh) are replaced by this Python implementation; functionality is identical.

Dependencies: `requests` (for survey), `pyyaml` (for YAML survey output, optional). Install with `pip3 install requests pyyaml`.

External binary: `flarectl` (Go binary). The Python wrapper locates it alongside itself or on PATH. See references/flarectl-install.md for install methods.

## Inputs required

- Cloudflare API token with "Edit zone DNS" permission stored in `<TOOLS_DIR>/cf-dns/cf-dns.conf` as `CF_API_TOKEN=<value>` (or set in environment).
- For all operations: zone (domain name).
- For create: record name, type, content; optionally proxied flag.
- For modify/delete: record ID (fetched via list at operation time, never reused from memory).

## Directory layout

```
<TOOLS_DIR>/cf-dns/
    cf_dns.py              # Python wrapper (primary tool)
    cf-dns.conf            # API token config (gitignored)
    cf-dns.conf.example    # Example/template (safe to commit)
    flarectl               # Binary (local copy, OR resolved from PATH)
    survey_dns_zones.py    # Zone survey script
    setup_survey_schedule.py  # Scheduling wrapper
    README.md
```

Default `<TOOLS_DIR>`: `~/.localsetup/tools`. Adapt to environment as needed.

## Workflow

### 1. Setup (first time)

1. Install flarectl (see `references/flarectl-install.md`).
2. Create `<TOOLS_DIR>/cf-dns/cf-dns.conf` with `CF_API_TOKEN=<your_token>`. Set permissions `600`. Gitignore this file.
3. Create the optional convenience symlink: `<TOOLS_DIR>/bin/cf-dns` pointing to `cf_dns.py`.
4. Verify: `python3 cf_dns.py dns list --zone=example.com`

### 2. List records

```python
# Equivalent shell call:
# python3 cf_dns.py dns list --zone=<domain>
```

- Do not assume a default zone. Always ask the user which domain to list or infer from context.
- Present output as a table: name, type, content, proxied, ID.
- Record IDs are required for modify and delete; capture from this output.

### 3. Create record

Parameters to gather: `zone`, `name` (subdomain or `@` for apex), `type` (A/AAAA/CNAME/MX/TXT), `content`, and whether proxied.

```
python3 cf_dns.py dns create --zone=<domain> --name=<name> --type=<type> --content=<content> [--proxy]
```

After creation: confirm by showing output or re-listing the zone.

### 4. Modify record (destructive, double confirmation required)

Safety gates (mandatory):
1. User states intent.
2. Agent lists the record(s) that will change (zone, name, type, current content, proposed new content, record ID). Waits.
3. User must confirm with a phrase **containing the word "modify"** (e.g. "confirm modify"). Vague replies ("yes", "ok") are not accepted.

Steps:
1. List zone to get live record ID.
2. Show details and wait for second confirmation.
3. Apply update: `python3 cf_dns.py dns update --zone=<domain> --id=<record_id> --content=<new_content> [--proxy|--no-proxy]`
4. Re-list to confirm.

Note: run `flarectl dns --help` to verify exact flags for the installed version.

### 5. Delete record (destructive, double confirmation required)

Safety gates (mandatory):
1. User states intent.
2. Agent shows exactly what will be deleted (zone, name, type, content, record ID). Waits.
3. User must confirm with a phrase **containing the word "delete"** (e.g. "confirm delete").

Steps:
1. List zone to get live record ID.
2. Show full record detail and wait for second confirmation.
3. Delete: `python3 cf_dns.py dns delete --zone=<domain> <record_id>`
4. Confirm removal (re-list optional).

### 6. Zone survey

Runs `survey_dns_zones.py` to snapshot all zones and their DNS records via the Cloudflare REST API. Marks each A record `points_to_this_host: true` if it points to this machine's public IP.

Output files (default: `~/.localsetup/context/dns/`):
- `cloudflare_dns_survey.json` (always written)
- `cloudflare_dns_survey.yaml` (written if PyYAML is installed)

Usage: `python3 survey_dns_zones.py [output_dir]`

The agent may read the survey for read-only context (e.g. "what records point to this host"), but must always use a live `dns list` call for any modify or delete to get current record IDs.

### 7. Schedule survey

`setup_survey_schedule.py` schedules `survey_dns_zones.py` daily (default 03:15 local time). Prefers cron; falls back to systemd user timer. Idempotent.

Usage: `python3 setup_survey_schedule.py`

## Agent behavior rules

**Multi-zone (mandatory):**
- Never assume a single domain. Always ask for or infer the zone before running any command.
- Always pass `--zone=<domain>` explicitly.
- When the account has multiple zones, do not default to any one of them.

**Record IDs:**
- Always fetch the current record list before modify or delete. Do not guess or reuse IDs from a previous session.

**Error handling:**
- Surface non-zero flarectl exits to the user with the full error output.
- If the token is missing or authentication fails, direct the user to check `cf-dns.conf` and the token's IP restrictions.

**Security:**
- `cf-dns.conf` must be gitignored and permissions set to `600`.
- Token should have only "Edit zone DNS" permission and an IP restriction for the machine's public IP.
- Survey output files contain record IDs and content; store in a gitignored location.

## Reference

- references/flarectl-install.md - flarectl install methods (Go, Homebrew, manual build)
- references/api-token-setup.md - Cloudflare API token creation guide
- references/survey-schema.md - Zone survey output schema
