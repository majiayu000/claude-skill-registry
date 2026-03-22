---
name: bun-audit
description: "Shared Bun audit/remediation router. Use when auditing a repo for Bun-first correctness, explaining Bun audit findings, listing Bun audit rules, planning safe Bun fixes, applying low-risk remediations, or validating Bun-related changes. This skill delegates to the shared engine in bun-dev/scripts."
---

# Bun Audit

Use this skill as a thin router over the shared Bun audit engine in
`~/.agents/skills/bun-dev/scripts/bun-audit.ts`. Do not duplicate rules or
remediation logic here.

## Commands

- `audit`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts audit --root <repo> --format text`.
- `explain <rule-id>`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts explain --explain <rule-id>`.
- `list-rules`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts list-rules`.
- `plan-fixes`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts plan-fixes --root <repo>`.
- `apply-safe-fixes`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts apply-safe-fixes --root <repo>`.
- `validate`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts validate --root <repo> --fail-on warn`.
- `benchmark`: run `bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts benchmark --root <repo>`.

## Operating Rules

- Treat `bun-dev` as the source of truth for the engine and rule explanations.
- The shared engine owns audit, fix planning, safe fix application, validate,
  benchmark, and release-sync.
- Do not run `audit`, `plan-fixes`, `apply-safe-fixes`, `validate`,
  `benchmark`, or `release-sync` in parallel against the same repo root. The
  shared platform cache uses a single SQLite database under `.bun-platform/`,
  and concurrent write access can trigger `database is locked`.
- By default, creating `.bun-platform/` also ensures `.bun-platform/` is present
  in the repo root `.gitignore`.
- Safe fixes create rollback artifacts under `.bun-platform/rollbacks/`.
- Keep changes minimal and forward-only.
- If a fix is risky or ambiguous, stop at `plan-fixes` and surface the tradeoff.
