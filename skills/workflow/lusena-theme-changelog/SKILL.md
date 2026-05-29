---
name: lusena-theme-changelog
description: Workflow for maintaining the LUSENA Shopify Dawn theme. Use when making substantial theme changes (Liquid/JSON/CSS/JS, templates, theme settings, cart/PDP UX) to ensure changes are validated, committed, and documented in docs/THEME_CHANGES.md.
---

# LUSENA theme changelog workflow

## Context (this repo)

- Base theme: Shopify **Dawn** (official).
- Goal: adapt Dawn for **LUSENA** (PL-first, premium feel, proof-first messaging).
- Brand source of truth: `docs/LUSENA_BrandBook_v1.md`.
- Engineering changelog: `docs/THEME_CHANGES.md` (commit-linked, semi-detailed).

## Workflow (for “bigger” changes)

### 1) Implement the change set

- Keep copy PL-first and aligned to the brandbook.
- Avoid “fixing” known baseline `shopify theme check` warnings listed in `AGENTS.md`.

### 2) Validate

- Run `shopify theme check` and ensure only the known baseline warnings remain.
- If you changed theme settings (schema/data), ensure schema constraints are respected (ranges, steps, defaults).

### 3) Commit (Git)

- Stage only the files relevant to the change set.
- Use a clear commit message (recommended: Conventional Commits):
  - `feat(lusena): …` for new UX/features
  - `fix(lusena): …` for bug fixes
  - `docs: …` for documentation only
  - `chore: …` for meta/infrastructure

### 4) Update `docs/THEME_CHANGES.md`

- Add a new entry with:
  - commit hash + commit message
  - goal (1–2 sentences)
  - “what changed” (bullets)
  - key files touched (high-signal list)

Template snippet to copy:

```md
### <hash> — <commit message>

**Goal:** …

**What changed**
- …

**Key files**
- `path/to/file`
```

### 5) Sanity check in dev

- Smoke test flows impacted by the change (PDP → add to cart, cart drawer, /cart, etc.).
