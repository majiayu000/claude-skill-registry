---
name: ca-pr
description: Open a pull request the only sanctioned way — clear every BLOCK-level review finding, then stage the PR. Never a direct write to the default branch.
argument-hint: (none)
---

# $ca-pr — open a pull request

The only permitted path to a pull request. Every change lands through a PR — never a direct write or force-push to the default branch. No PR is drafted while any BLOCK-level review finding stands.

## Flow

Routes to the `finishing-a-development-branch` skill, open-PR path. The orchestrator reads the current
branch, its diff against the base, and the commit log to determine what changed and which reviewers
apply, then:

1. **Confirm the commit gate cleared** this session (`commit-gate` green, or `$ca-commit` completed).
2. **Path matrix** — inspect the diff and dispatch the reviewer agents the change demands:
   - auth / crypto / middleware paths → `auth-crypto-reviewer` + `security-reviewer`
   - migration files → `migration-reviewer`
   - dependency manifests → `dependency-reviewer`
   - all paths → `coverage-auditor`
3. **Run reviewers** in parallel where there are no dependencies.
4. **BLOCK check** — any CRITICAL or HIGH finding STOPs the flow; present it and do not draft the PR.
   The user resolves, re-runs `$ca-commit`, then `$ca-pr`.
5. **Stage the PR** once all BLOCK findings clear: concise title; summary of what changed and why; a
   bulleted test plan; a conflict-hierarchy tradeoff citation for any non-obvious tradeoff; a link to
   any ADR the change implements or contradicts. The PR body is a user-facing deliverable: before
   composing it, load `${CLAUDE_PLUGIN_ROOT}/includes/anti-slop-design/core.md` and the
   `medium-documents` leaf, and apply at least the §3.A em-dash ban and the §3.B copy self-audit to the
   prose. Then `gh pr create`; return the URL.
6. **Auto-attach the babysitter** — resolve the flag with the canonical resolver, never by eyeballing
   the env var (so the accepted `on|true|1` spellings and the dormancy gate can't drift):
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/hooks/babysit.py" --root "<project-root>" || python "${CLAUDE_PLUGIN_ROOT}/hooks/babysit.py" --root "<project-root>"
   ```
   It prints one JSON line, e.g. `{"enabled": true, "on_red": "propose"}`. Only when `enabled` is
   true (the global flag `CODEARBITER_BABYSIT` is on — default off, mirrors `CODEARBITER_PRUNE` — and
   the repo is arbiter-active), attach a CI watcher to the PR just opened, equivalent to
   `$ca-watch <new-PR>`. When `enabled` is false, do nothing here — the user can still run `$ca-watch`
   ad-hoc. Never enable the flag on the user's behalf.

## Routes to

`finishing-a-development-branch` (`${CLAUDE_PLUGIN_ROOT}/routines/finishing-a-development-branch/SKILL.md`),
open-PR path.

## When NOT to use

- Staged changes not yet committed → `$ca-commit`.
- Review a diff without opening a PR → `$ca-review`.
- A pre-implementation security pass → `$ca-threat-model`.

## Hard gate

MUST NOT open a PR while any BLOCK-level (CRITICAL or HIGH) finding is unresolved. MUST NOT skip a
reviewer the path matrix requires. MUST NOT open a PR before the commit gate ran this session. MUST
NOT open a PR, write, or force-push directly to the default branch. MUST NOT auto-attach a CI watcher
unless `CODEARBITER_BABYSIT` is on, and MUST NOT enable that flag on the user's behalf.
