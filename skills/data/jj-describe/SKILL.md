---
name: jj:describe
description: "Generate and set a commit description for a commit in jj"
---

# Describe a Commit

Generate and set a commit description. Defaults to `@` (working copy), but typically used on `@-` (parent) when working copy is empty.

## Process

1. Run `jj show <rev> --summary` and `jj diff -r <rev> --stat` to get change overview (use `@-` for parent)
2. Analyze changes:
   - Small (≤5 files, ≤200 lines): run `jj diff -r <rev>` directly
   - Large: use `/jj-context` for structured summary
3. Determine project prefix from file paths
4. Generate a **one-line** description: `<prefix>: <lowercase verb> <what changed>`
5. Run `jj describe <rev> -m "<description>"` (e.g., `jj describe @- -m "..."`)

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
