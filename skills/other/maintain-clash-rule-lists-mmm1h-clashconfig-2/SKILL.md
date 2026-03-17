---
name: maintain-clash-rule-lists
description: Maintain custom Clash rule lists in rules/*.list for this repo. Use when adding or removing domain/IP rules, adjusting list contents, or wiring rule lists into mihomo.yaml/mihomo.js.
---

# Maintain Clash Rule Lists

## Overview

Keep the custom rule lists in `rules/` consistent and correctly referenced by the Mihomo config.

## Rule list editing

- Edit the appropriate file under `rules/`; one rule per line.
- Use Clash classical keywords: `DOMAIN`, `DOMAIN-SUFFIX`, `DOMAIN-KEYWORD`, `IP-CIDR`, `IP-CIDR6` with optional `,no-resolve`.
- Keep list content focused on its purpose; avoid mixing unrelated categories.

## Wiring into config

- Ensure every custom list you change is referenced in `mihomo.yaml` or `mihomo.js`.
- Keep rule targets and group names aligned across `mihomo.yaml` and `mihomo.js`.

## Guardrails

- Do not manually edit `*Merged.list` files unless you are regenerating them from sources.
- Keep placeholders like `__MEIYING_URL__` and `__YUNDONG_URL__` untouched unless explicitly updating subscription URLs.

## Quick checks

- Scan for invalid keywords or missing commas.
- Confirm the list is still referenced by the config after edits.
