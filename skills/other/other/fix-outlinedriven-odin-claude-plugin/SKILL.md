---
name: fix
description: Polymorphic iterative repair loop — accept a verifier failure, structured findings (review/resolve/triage-issue), or a bug description; modify→verify→keep on green, auto-revert on guard regression, until clean or iteration cap. Use when the user says "fix", "make it pass", or "apply the findings", or hands an artifact + repo and expects patches; auto-routes to gh-fix-ci or gh-address-comments when an open PR + gh auth + GH-flavored input is detected.
metadata:
  short-description: Iterative fix loop with auto-revert
---

# Fix

Failure-driven iterative repair. Detect → Prioritize → Fix ONE thing → Commit → Verify → Keep/Revert → Repeat.

## When to Apply / NOT

**Apply:** user says "fix", "make it pass", "apply findings"; input is a verifier failure, findings file, or bug description.

**NOT apply:**
- CI/PR workflows with no local context → use `gh-fix-ci`
- PR review comments → use `gh-address-comments`
- Merge conflicts
- Analysis-only tasks → use `resolve` or `debug`
- Planned change without a failure driver → use `proceed`

## Detected Mode Acknowledgement [LOAD-BEARING]

First output line before ANY edit:

```
detected: <mode> — target=TARGET guard=GUARD scope=SCOPE cap=20
```

Mode values: `gh-route`, `findings`, `verifier-failure`, `bug-spec`. Full classifier: `references/classifier.md`.

## Input Classifier

First-match wins. Full detail: `references/classifier.md`.

| Priority | Mode | Minimum condition |
|----------|------|-------------------|
| 1 | `gh-route` | GH-flavored input + open PR + `gh auth status` clean |
| 2 | `findings` | Path to `*/findings.md`, `*/review/*.md`, or structured findings text |
| 3 | `verifier-failure` | Raw verifier stdout (`FAILED`, `error TS`, `--- FAIL`, etc.) |
| 4 | `bug-spec` | Natural-language description — catch-all fallback |

## Auto-Detect Gate

Auto-infer: target verifier, scope glob, guard command, iteration cap (default 20).

Trigger `AskUserQuestion` (single-select per axis, NEVER `multiSelect`) when:

- `MIXED_MODE`: findings artifact AND verifier-failure output both present
- `GH_PARTIAL`: GH-flavored input but no open PR, or `gh auth status` fails
- `LANG_UNKNOWN`: verifier-failure detected but verifier undetectable
- `SCOPE_AMBIGUOUS`: bug-spec with no module, file, or component reference

## Iterative Loop

Full spec: `references/loop.md`. Key rules:

- One fix per iteration. Apply fix → stage checkpoint commit → run verifiers → **KEEP** on green, revert with `git revert HEAD --no-edit` on red. A commit is *kept* only when the guard passes.
- Decide matrix:
  - `delta > 0` + guard ok → **KEEP**
  - `delta > 0` + guard fail → **REWORK** (max 2 reworks per item; 4th attempt → SKIP)
  - `delta ≤ 0` → **DISCARD** — revert immediately
  - 3 total skips → **HALT** with summary
- Revert: always `git revert HEAD --no-edit`. Never `reset --hard`.
- Cap: 20 iterations default. Print progress every 5 iterations.
- Refuse loop on protected branches (`main`, `master`, `release/*`).
- Override: `iterations: N` or `--iterations N` in invocation.

## Verifier Detection

Repo-native first (use `fd --max-depth 2` to locate):

1. `Justfile` → `just test` (guard: `just check`)
2. `Makefile` → `make test` (guard: `make check`)
3. `package.json` → `npm test` (guard: `tsc --noEmit && eslint .`)
4. `dune-project` → `dune build @runtest` (guard: `dune build`)

Language fallbacks:
- Python: `pytest` + `ruff check . && mypy .`
- TypeScript: `vitest run` + `tsc --noEmit && eslint .`
- Rust: `cargo test` + `cargo clippy -- -D warnings`
- Go: `go test ./...` + `golangci-lint run`
- OCaml: `dune build @runtest` + `dune build`

Full matrix: `references/verifiers.md`.

## GH Auto-Route

When open PR + `gh auth status` clean + GH-flavored input:

| Sub-target | Trigger language |
|------------|-----------------|
| `gh-fix-ci` | "CI", "Actions", "workflow", "checks", Actions run URL |
| `gh-address-comments` | "reviewer said", "address comment", "PR feedback", "requested changes" |

Both sets of language → fire `AMBIGUOUS_GH_ROUTE` (single-select: `gh-fix-ci` vs `gh-address-comments`).
Partial match → `GH_PARTIAL` ambiguity flag.

## Hand-off & Integration

- `debug` upstream: unclear root cause — debug findings become the fix target.
- `triage-issue` upstream: bug-spec mode — triage produces repro + TDD plan first.
- `test-driven` partner: failing test ↔ green flip; delegate RED→GREEN cycle.
- `proceed` complement: planned change without failure → `proceed`; failure-driven → `fix`.
- `resolve` / `review` / `triage-issue` as findings sources: their output paths feed findings mode.

## Failure Modes

- No verifier output: emit warning, raise `LANG_UNKNOWN`.
- 3 strikes on one item: SKIP, add to `blocked.md`, recommend `debug`.
- 3 total skips: HALT with session summary.
- Guard ambiguous: `AskUserQuestion` for guard command.
- Mixed-mode input: raise `MIXED_MODE`.
- Protected branch: REFUSE with message before entering loop.

## Anti-Patterns

- Never `@ts-ignore` / `# type: ignore` / `// eslint-disable` to silence errors.
- Never delete tests to make them pass.
- ONE fix per iteration — no "while I'm here" changes.
- No `git reset --hard`.
- Recursion guard: `--mode <X>` bypasses classifier entirely; `gh-fix-ci` re-entering as `fix --mode verifier-failure` cannot loop back into `gh-fix-ci`.

## Constitutional Rules

- Evidence before claims: run verifiers, read output, then state result.
- Tidy-first: reduce coupling before behavior change.
- Atomic commits: one concern per commit; guard must pass before a loop commit is **kept** (KEEP in decide matrix = tests-pass gate).
- Never skip the guard.
- Full specs: `references/loop.md`, `references/classifier.md`, `references/verifiers.md`.
