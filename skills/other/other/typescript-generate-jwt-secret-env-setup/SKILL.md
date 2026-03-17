---
name: generate-jwt-secret-env
description: Generate, repair, or verify a cryptographically secure JWT_SECRET in .env for Node.js and NestJS projects when code under src/ references JWT_SECRET and the active .env value is missing, empty, or set to change-me-in-production. Use when fixing JWT auth startup failures, hardening environment configuration, standardizing .env secrets, or repairing placeholder JWT_SECRET values.
---

# Generate JWT_SECRET in .env

## Workflow

1. Resolve target files and preconditions.

   - Require a repository root with a readable `src/` directory.
   - Require a writable `.env` file; create `.env` only if it is missing and the task asks to initialize environment values.
   - Preferred reference check:
     - `rg -n --glob "src/**" "JWT_SECRET"`
   - Accept reference patterns such as:
     - `config.get('JWT_SECRET')`
     - `ConfigService.get('JWT_SECRET')`
     - `process.env.JWT_SECRET`
   - Stop without editing `.env` if no `src/` reference exists.

2. Inspect `.env` and determine whether generation is needed.

   - Parse lines and locate active (non-comment) `JWT_SECRET=` entries.
   - Generate only if:
     - Key is absent, or
     - Value is empty (`JWT_SECRET=`, `JWT_SECRET=""`, `JWT_SECRET=''`), or
     - Value is exactly `change-me-in-production` (with or without quotes).
   - Do not overwrite any other non-placeholder value.
   - If multiple active keys exist, update only the first eligible active key by default.

3. Generate a cryptographically secure secret.

   - Preferred Node command:
     - `node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`
   - Accept equivalent secure output formats (`hex` is also valid) when randomness comes from a cryptographically secure source.

4. Update `.env` safely.

   - If an active `JWT_SECRET=` line exists and is empty/placeholder, replace only its value.
   - If no active key exists, append `JWT_SECRET=<generated>` in a sensible auth/env section.
   - Preserve unrelated lines, comments, spacing style, and key order.
   - If duplicate active keys exist, update only the first active eligible key and leave the rest unchanged unless the task explicitly asks for cleanup.

5. Perform security checks.

   - Confirm `.env` is ignored by git (`.gitignore` or equivalent ignore rules).
   - Confirm no command output, logs, or summaries expose the generated secret value.
   - Never print the generated secret in summaries unless the user explicitly asks for it.
   - If `.env` is tracked by git and the task is to harden security, recommend rotating the leaked secret after ignore rules are fixed.

6. Run deterministic verification gates.

   - Re-scan `src/` references and confirm they still resolve to `JWT_SECRET`.
   - Confirm `.env` now has an active `JWT_SECRET=` entry with a non-empty, non-placeholder value.
   - Report one of these outcomes:
     - `updated` (secret generated and written),
     - `unchanged-valid` (existing non-placeholder secret kept),
     - `skipped-no-reference` (no `src/` usage),
     - `blocked` (missing permissions/files or other hard blocker with exact cause).

Use detailed parsing and edge-case behavior from [reference.md](reference.md).
