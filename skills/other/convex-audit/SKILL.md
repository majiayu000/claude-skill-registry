---
name: convex-audit
description: Audit a Convex-backed codebase for schema quality, security, runtime boundaries, migrations, and function-surface risks. Use when the user asks for a Convex review, backend audit, contract analysis, or remediation plan. Do not use for green-field feature-spec generation; use convex-feature-spec for that.
---

# Convex Audit

Use this skill for read-first Convex audits that produce a clear remediation plan before implementation.

## Workflow

1. Read the repo `AGENTS.md`.
2. Run `/home/bjorn/.codex/skill-support/bin/convex-scan inventory --cwd <repo> --out <json>`.
3. Run `/home/bjorn/.codex/skill-support/bin/convex-scan surface --cwd <repo> --out <json>`.
4. Run `/home/bjorn/.codex/skill-support/bin/convex-scan gaps --inventory <json> --out <json>`.
5. Read only the references needed for the active findings:
   - `references/security.md`
   - `references/schema.md`
   - `references/runtime-boundaries.md`
   - `references/migrations.md`
6. Validate non-trivial recommendations against current docs before finalizing.
7. Output a remediation plan with file targets, risk level, and verification steps.

## Use When

- The user asks for a Convex audit, security pass, schema review, or backend remediation plan.
- The repo has Convex and the main task is to assess existing architecture or implementation quality.

## Do Not Use When

- The task is a new feature specification with multiple design options.
- The task is only a dependency upgrade or docs sync.

## Outputs

- A concise audit summary.
- Ranked findings.
- An implementation-ready remediation checklist.

## Resources

- Inventory helpers via `/home/bjorn/.codex/skill-support/bin/convex-scan`
- `references/security.md`
- `references/schema.md`
- `references/runtime-boundaries.md`
- `references/migrations.md`

