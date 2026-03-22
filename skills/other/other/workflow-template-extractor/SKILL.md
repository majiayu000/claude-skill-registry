---
name: workflow-template-extractor
description: "Extract a shareable runnable template under templates/NNN-slug/ from a real project: copy + de-brand + remove secrets + add env examples + docs, with minimal refactors. Use when you have a working project and want to turn it into a template."
---

# Workflow: Template Extractor (Real Project → Template)

Goal: Turn a real project into a **shareable, runnable template** in `templates/` with minimal manual cleanup.

This is intended for “proven projects” you want to reuse as a baseline for future builds.

## Input (pass paths only)

- `source_repo_root`: Path to the real project
- `target_repo_root`: Ship Faster repository root (where `templates/` lives)
- `run_dir`: `runs/template-extractor/active/<run_id>/`
- `extract_spec.md`: What to keep/remove/generalize (brand, copy, assets, integrations, auth gates)

## Output (persisted)

- `03-plans/extract-plan.md`
- `05-final/extract-summary.md`
- `templates/<NNN>-<slug>/` (runnable)

## Workflow

### 0) Initialize

1. Create `run_dir`.
2. Decide `<slug>` and `<NNN>` (next available template number).
3. Copy `source_repo_root` → `templates/<NNN>-<slug>/` (no build outputs, no caches).

### 1) De-secrets + de-brand

Must do:
- Remove secret values from all files (`.env*`, config, hard-coded tokens).
- Replace project IDs (Stripe price IDs, Supabase URLs/keys, webhook secrets) with env var keys.
- Replace branding (names/domains/logos) with neutral placeholders unless the template is intentionally branded.

### 2) Normalize template entry docs

Required files:
- `README.md` (5‑minute runnable)
- `.env.local.example` (keys only)
- `metadata.json` (name + description)

Recommended:
- Ensure scripts exist for `dev`, `build`, `start`
- If lint/typecheck/format are missing and the repo is TS-heavy, add minimal guardrails (avoid heavy governance)

### 3) Verification

Document in `05-final/extract-summary.md`:
- install works
- `dev` starts
- `build` succeeds (or clearly document why it can’t without credentials)

## Constraints

- Never commit secret values.
- Extraction should be “copy + cleanup”, not a refactor project.
