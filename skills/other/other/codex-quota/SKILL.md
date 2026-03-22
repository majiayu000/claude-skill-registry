---
name: codex-quota
version: 1.2.1
homepage: https://github.com/odrobnik/codex-quota-skill
description: >
  Check OpenAI Codex CLI rate limit status (daily/weekly quotas) using local
  session logs. Portable Python script.

  Reads ~/.codex/sessions/ for quota data.
  When using --all --yes, it temporarily switches accounts by overwriting
  ~/.codex/auth.json (restored afterwards) to query each account.

  Uses the `codex` CLI for --fresh / --all.
metadata:
  openclaw:
    requires:
      bins: ["python3", "codex"]
---

# Skill: codex-quota

Check OpenAI Codex CLI rate limit status.

## Quick Reference

```bash
# Run the included Python script
./codex-quota.py

# Or if installed to PATH
codex-quota
```

## Options

```bash
codex-quota              # Show current quota (cached from latest session)
codex-quota --fresh      # Ping Codex first for live data
codex-quota --all --yes  # Update all accounts, save to /tmp/codex-quota-all.json
codex-quota --json       # Output as JSON
codex-quota --help       # Show help
```

## Setup

See [SETUP.md](SETUP.md) for prerequisites and setup instructions.

## What It Shows

- **Primary Window** (5 hours) — Short-term rate limit
- **Secondary Window** (7 days) — Weekly rate limit
- Reset times in local timezone with countdown
- Source session file and age

## When to Use

- Before starting heavy Codex work (check weekly quota)
- When Codex seems slow (might be rate-limited)
- Monitoring quota across multiple accounts
