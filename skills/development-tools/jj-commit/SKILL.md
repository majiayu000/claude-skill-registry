---
name: jj:commit
description: "Create a jj commit from current working copy with auto-generated description"
---

# Commit Current Changes

Create a new jj commit from the current working copy with a generated description.

## Process

1. Run `jj diff --summary` and `jj diff --stat` to get change overview
2. Analyze changes:
   - Small (≤5 files, ≤200 lines): run `jj diff` directly
   - Large: use `/jj-context` for structured summary
3. Determine project prefix from file paths
4. Generate a **one-line** description: `<prefix>: <lowercase verb> <what changed>`
5. Run `jj commit -m "<description>"`

**IMPORTANT**: Always use a single-line commit message. Never use multi-line descriptions or bullet points.

## Project Prefix Examples

Use the descriptive folder path identifying the subsystem:
- `src/auth` for authentication code
- `lib/utils` for utility libraries
- `services/api` for API services
- `db/migrations` for database changes

## Good Description Examples

- `src/auth: add JWT token refresh logic`
- `lib/utils: fix date parsing for ISO formats`
- `services/api: add rate limiting middleware`
- `db/migrations: add users table`
- `tests/integration: add checkout flow tests`
