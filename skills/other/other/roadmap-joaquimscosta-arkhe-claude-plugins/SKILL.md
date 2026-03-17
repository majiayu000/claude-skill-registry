---
name: roadmap
description: >
  Synthesize project documentation and codebase into comprehensive roadmap status, gaps analysis,
  and blockers. Use when assessing project health, identifying blockers, tracking progress,
  comparing plan vs reality, documenting risks, or planning next milestones.
  Triggers: "roadmap", "project status", "blockers", "risks", "progress", "next milestone",
  "gaps", "what's done".
argument-hint: status | gaps | next | delta | blockers | risks | update | specs
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Roadmap Analyst

Synthesize project documentation and codebase state into actionable status reports.

## Context Discovery

**Run this protocol before any analysis to understand the project.**

### Priority 1: Explicit Configuration

Read `.arkhe.yaml` from project root. Extract `roadmap:` section:

```yaml
roadmap:
  output_dir: arkhe/roadmap
  context_dir: .arkhe/roadmap
  status_file: docs/PROJECT-STATUS.md
```

### Priority 1b: Johnny Decimal Detection

Check if the project uses Johnny Decimal documentation structure:
1. Read `.jd-config.json` at project root — if present, use its `root` (default: `docs`) and `areas` map
2. If no config, glob for `docs/[0-9][0-9]-*/` — if 2+ matches exist, J.D structure is present

If J.D detected, supplement Priority 4 (Documentation Scan) globs:
- Glob `{jd_root}/[0-9][0-9]-*/**/*.md` to capture all area docs
- Read ALL areas — roadmap analysis requires comprehensive coverage
- Deprioritize `90-*` (archive) — read last, note content may be outdated
- Keep existing non-J.D paths as fallback

### Priority 2: Rich Context

If `{context_dir}` exists, read all `.md` files — especially `documents.md` for the document map and `architecture.md` for module structure.

### Priority 3: Project Identity

Read `CLAUDE.md` and `README.md` to understand project scope and conventions.

### Priority 4: Documentation Scan

Glob for documentation, planning, and status files:

```
docs/**/*.md, plan/**/*.md, specs/**/*.md, arkhe/specs/*/spec.md
```

### Priority 5: Codebase Scan

Detect tech stack from build files, then scan for modules, routes, models, tests, and migrations.

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `status` | Overall dashboard — modules, phases, completion |
| `gaps` | Gap analysis status — open/closed/in-progress |
| `next` | Prioritized next actions |
| `delta` | What changed since last assessment |
| `blockers` | Blocking chain analysis |
| `risks` | Risk register with likelihood/impact |
| `update` | Git-history-aware status document update (Phase A: what shipped + Phase B: full scan) |
| `specs` | Spec pipeline status verification |
| _(none)_ | Full dashboard (combines status + gaps + next) |

## Module Maturity Scale

Rate each module using this shared vocabulary:

| Level | Description |
|-------|-------------|
| **Stub** | Directory/package exists, maybe a placeholder |
| **Domain Started** | Entities/models/types defined |
| **Service Layer** | Business logic implemented |
| **API Ready** | Endpoints/routes exposed |
| **Tested** | Tests covering key paths |
| **Production Ready** | Fully tested, documented, monitoring-ready |

## Mode Execution

### `status`

Produce a status dashboard:

| Module | Backend | Frontend | Maturity |
|--------|---------|----------|----------|

Then detail: What's working, What's planned, What's missing.

After producing the dashboard, check for documentation drift:

1. Find last modification of `{status_file}` via git: `git log -1 --format="%H %ai" -- {status_file}`
2. Count feature/fix commits since: `git log {hash}..HEAD --oneline --no-merges | grep -cE "^[a-f0-9]+ (feat|fix):"`
3. If 3 or more feat/fix commits exist since last update, append a notice at the end of the output:

```
⚠️  Documentation may be stale: {N} feature/fix commits since last status update ({date}).
Run `/roadmap update` to sync.
```

### `gaps`

Cross-reference all gap analysis documents. For each gap: original report, current status (Open/In Progress/Closed), evidence of closure.

### `next`

Prioritized recommendations combining: unclosed gaps, unstarted specs, module maturity imbalances, frontend-backend parity gaps.

### `delta`

Compare the status document against current codebase state. Highlight: new files/modules, closed gaps, new issues, migration count changes.

### `blockers`

Trace blocking chains. For each blocker: what it blocks, who owns it, what's needed to unblock.

### `risks`

Risk register:

| Risk | Likelihood | Impact | Score | Mitigation |
|------|-----------|--------|-------|------------|

### `update`

Generate an updated status document with git-history awareness. Two phases:

#### Phase A: Git History Scan

Before the codebase scan, analyze what changed since the last doc update:

1. Find last modification of `{status_file}`: `git log -1 --format="%H %ai" -- {status_file}`
2. If no previous commit found, skip Phase A (first-time setup — Phase B handles it)
3. List commits since: `git log {hash}..HEAD --oneline --no-merges`
4. Group by PR number (parse `(#NN)` from commit messages) and commit type (`feat:`, `fix:`, `docs:`, etc.)
5. For each feature/fix group, summarize:
   - Scope (new components, routes, hooks, test files — inferred from file paths in the diff)
   - Related specs (cross-reference `arkhe/specs/` changes in the commit range)
   - Related ADRs (new files in `docs/adr/` in the commit range)
6. Present a **"What Shipped"** summary to the user before proceeding to the full scan:

```
## What Shipped Since Last Update (2026-03-09, 10 commits ago)

1. Glossary Management + Dictionary Browser (PR #32, specs 022-025)
   - 6 components, 2 hooks, 5 test files, /dictionary route
2. App Header Unification (PR #33)
   - Refactored navigation components
3. skrebe.app Redirect (1aff903, ADR-0010)
   - New middleware + DNS config
```

This context feeds into Phase B so the codebase scan knows what to look for and can produce more accurate updates.

#### Phase B: Full Codebase Scan + Write (existing behavior, enhanced)

1. Run full context discovery + codebase scan (same as before)
2. Read existing status document
3. Preserve format and structure
4. Update all data points — now informed by the git history from Phase A:
   - Module maturity ratings
   - Phase completion entries (Phase A identifies which phases completed)
   - Spec pipeline entries (Phase A identifies which specs shipped)
   - ADR table entries (Phase A identifies new ADRs)
   - Test coverage section
   - Commit count and date
   - Risk register (close risks for shipped features)
5. Show diff preview and ask for confirmation
6. Write updated file to `{status_file}`
7. Also check CHANGELOG.md — if `[Unreleased]` is missing entries for shipped features from Phase A, suggest adding them after the status update is applied (don't auto-write CHANGELOG without explicit confirmation)
8. Report changes made

### `specs`

Spec pipeline verification:

| Spec | Title | Status | Evidence |
|------|-------|--------|----------|

Verify status against codebase, not just what the spec says.

## Output Rules

- **Evidence-based** — every claim backed by a file path, migration, or component
- **Tabular** — use tables for at-a-glance status; prose for analysis
- **Actionable** — always end with recommended next actions
- **Honest** — distinguish between "verified working" and "files exist but untested"
- `update` writes files after user confirmation; all other modes output to chat

## Lane Discipline

- Do NOT produce user stories or requirements — that's the PM's domain.
- Do NOT produce architecture documents or ADRs — that's the architect's domain.
- Do NOT write source code, tests, or config files.
- Don't confuse planning documents with implementation — a design doc is NOT a built feature.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed discovery and mode workflows
- [EXAMPLES.md](EXAMPLES.md) — Usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
