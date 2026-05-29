---
name: maintain-clash-mihomo-config
description: Maintain and update this Clash/Mihomo configuration repo (mihomo.yaml, mihomo.js, rules/*.list, *Merged.list, force_ttl_rules.txt). Use when editing proxy groups, rule providers, DNS/TTL rules, or regenerating merged lists in this project.
---

# Maintain Clash Mihomo Config

## Overview

Keep the Mihomo/Clash config, custom rules, and generated lists consistent in this repo, following the project guardrails.

## Key files

- `mihomo.yaml`: primary Mihomo/Clash config (providers, DNS, proxy groups, rule providers, rules)
- `mihomo.js`: JS config generator; keep group and rule names identical to `mihomo.yaml`
- `rules/*.list`: custom rule lists in Clash classical text format
- `*Merged.list`: generated/merged rule lists with source headers
- `force_ttl_rules.txt`: generated PaoPaoDNS rules
- `scripts/update_dns.py`: regenerate `force_ttl_rules.txt` (requires network and `requests`)
- `scripts/update_dns_rules.sh`: server-side updater for PaoPaoDNS
- Chinese-named directories: ImmortalWrt build notes and ACL4SSR archive (treat as notes/vendor data)

## Update workflows

### Custom rules

- Edit the relevant file in `rules/`.
- Ensure the rule list is referenced in `mihomo.yaml` or `mihomo.js`.
- Keep one rule per line using Clash keywords `DOMAIN`, `DOMAIN-SUFFIX`, `DOMAIN-KEYWORD`, `IP-CIDR`, `IP-CIDR6` with optional `,no-resolve`.

### Mihomo config

- Keep proxy group names and rule targets identical across `mihomo.yaml` and `mihomo.js`.
- Keep placeholders `__MEIYING_URL__` and `__YUNDONG_URL__` intact unless updating subscription URLs.

### PaoPaoDNS rules

- Run `python scripts/update_dns.py` to refresh `force_ttl_rules.txt`.
- Expect network access and the `requests` package to be available.

### Merged lists

- Regenerate from the sources listed in each file header.
- Preserve headers and metadata; avoid manual edits unless regenerating.

## Validation

- Validate YAML syntax for `mihomo.yaml`.
- Validate JS syntax for `mihomo.js`.
- Verify rule list formatting (one rule per line, valid Clash keywords).
