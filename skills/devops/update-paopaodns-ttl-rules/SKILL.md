---
name: update-paopaodns-ttl-rules
description: Refresh PaoPaoDNS force TTL rules by running scripts/update_dns.py and updating force_ttl_rules.txt, or adjusting scripts/update_dns_rules.sh for server-side updates. Use when DNS rule sources or outputs need updates in this repo.
---

# Update PaoPaoDNS TTL Rules

## Overview

Regenerate `force_ttl_rules.txt` from upstream rule sources using the local Python script and keep the server-side updater aligned.

## Local regeneration

- Run `python scripts/update_dns.py` from the repo root.
- Ensure network access and the Python `requests` package are available.
- Confirm the output file `force_ttl_rules.txt` is updated with a fresh header (timestamp, count, DNS, source URLs).

## Source and DNS settings

- Adjust `SOURCE_URLS`, `PRIMARY_DNS`, or `FALLBACK_DNS` in `scripts/update_dns.py` only when required.
- Keep `OUTPUT_FILE` pointing to `force_ttl_rules.txt`.

## Server-side updater

- Use `scripts/update_dns_rules.sh` on the server to pull the latest `force_ttl_rules.txt` from GitHub.
- Update `REMOTE_URL`, `LOCAL_FILE`, and `RESTART_CMD` only if deployment paths or service names change.

## Quick checks

- Verify the output is non-empty and begins with the expected header block.
- Avoid manual edits to `force_ttl_rules.txt` unless regenerating.
