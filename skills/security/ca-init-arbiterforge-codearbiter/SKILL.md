---
name: ca-init
description: Opt this repo into codeArbiter — scaffold the root-level .codearbiter/ state store.
argument-hint: "(none) | --stage N | --check"
---

# $ca-init — first-run scaffold

Stand up the root-level `.codearbiter/` project-state store that opts a repo into arbiter
management. This is the v2 replacement for vendoring/`init-vendor`: no symlinks, no shims, no dual
root. It writes the activation flag and the empty state files, then hands off to the populator.

`.codearbiter/CONTEXT.md` frontmatter `arbiter: enabled` is the single activation flag — it gates
the SessionStart persona injection. The scaffolded
`CONTEXT.md` is a **stub** (no initialization sentinel), so after scaffolding the project still needs
populating before normal operation.

## Procedure

1. Run the scaffolder against the repo's git toplevel (resolved by the script):

   ```
   python "${CLAUDE_PLUGIN_ROOT}/hooks/init-codearbiter.py"
   ```

   It is idempotent and refuses if `.codearbiter/CONTEXT.md` already exists — it never overwrites
   state. Pass `--stage N` to set the initial maturity value (default `1`). Use `--check` to report
   state without creating anything.

2. It creates `.codearbiter/` with: `CONTEXT.md` (`arbiter: enabled`, `stage: N`, stub body),
   `open-tasks.md`, `open-questions.md`, `overrides.log` (audit header), and `last-checkpoint` (`0`).

3. **Then route to the populator** — the stub is not yet usable:
   - **Source code already exists** in the repo → route to `$ca-create-context` (brownfield: scouts
     read the codebase and synthesize the full context, writing the initialization sentinel).
   - **Greenfield** (no meaningful source) → route to `$ca-decompose` (layered interview).

   The populator is **mandatory, not optional**: it authors `tech-stack.md`, `coding-standards.md`,
   and `security-controls.md` (and writes the initialization sentinel). The pipeline gates BLOCK on
   reading those files — `writing-plans` and `tdd` need `tech-stack.md`, the security gates need
   `security-controls.md` — so `$ca-feature` run on a freshly-scaffolded stub will STOP at pre-flight
   until the populator has run. `session-start` surfaces this as `NOT INITIALIZED` every session.

4. Report what was created and which populator you are routing to.

## When NOT to use

- `.codearbiter/` already scaffolded → the scaffolder refuses; run `$ca-create-context` or
  `$ca-decompose` to populate, or `$ca-status` to see state.
- You only want to re-check detection state → run the scaffolder with `--check`.

## Hard gate

MUST NOT hand-author `.codearbiter/CONTEXT.md` frontmatter — the scaffolder is the sanctioned path so
the activation flag and state-file shapes match what the hook parses. MUST NOT mark a
stub initialized; only the populator writes the initialization sentinel.
