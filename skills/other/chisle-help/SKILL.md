---
name: chisle-help
description: >
  Quick-reference card for Chisle commands. One-shot
  display, not a persistent mode. Use when the user says "chisle help", "how do I
  use chisle", "what chisle commands", or invokes /chisle-help.
---

# Chisle quick reference

**What it is:** maximum-efficiency dev mode. Zero-fluff prose + YAGNI-first code, always on together.

## Commands

| Command | Effect |
|---------|--------|
| `/chisle` | Activate |
| `/chisle-audit [path]` | Audit a diff/file/repo for both code bloat AND prose verbosity |
| `/chisle-review` | Review the current diff for over-engineering |
| `stop chisle` / `normal mode` | Deactivate |

Natural language works: "activate chisle", "chisle mode", "chislify this".

## The code ladder

YAGNI → reuse → stdlib → native → installed dep → one line → minimum code.

## Statusline

`[CHISLE]` is shown while active. Configure via
`hooks/chisle-statusline.sh` (or `.ps1` on Windows).

## Never minimal about

Input validation, error handling that prevents data loss, security,
accessibility, anything you explicitly asked for.
