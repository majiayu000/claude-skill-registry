---
name: convex-feature-spec
description: Generate a complete Convex-first feature specification for a repo, including data model, API surface, rollout, and verification. Use when the user wants a new feature plan or architecture spec centered on Convex contracts. Do not use for audits of the existing implementation; use convex-audit for that.
---

# Convex Feature Spec

Use this skill for green-field or breaking-change-tolerant feature planning where the output is a complete implementation spec.

## Workflow

1. Read the repo `AGENTS.md`.
2. Run `/home/bjorn/.codex/skill-support/bin/convex-scan inventory --cwd <repo> --out <json>` to ground the current backend surface.
3. Read `references/feature-spec.md`.
4. Read `references/components.md` if the feature may use existing Convex components or reusable backend patterns.
5. Read `references/rollout-and-migration.md` before finalizing any spec that changes schema, auth, or rollout order.
6. Research the active APIs before locking any non-trivial design.
7. Output an implementation-ready spec with task order, interfaces, risks, and verification.

## Use When

- The user asks for a new feature spec, a Convex-first architecture plan, or a complete backend-driven design.
- The repo uses Convex and the planning output must include schema and function contracts.

## Do Not Use When

- The task is reviewing or fixing the current implementation.
- The task is just docs alignment or dependency work.

## Outputs

- feature objective
- schema and function contract changes
- rollout and migration plan
- ordered implementation and verification steps

