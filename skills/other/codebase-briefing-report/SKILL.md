---
name: codebase-briefing-report
description: |-
  Use when producing a shareable architecture, module, metrics, and health report for a codebase.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
hexagonal_role: supporting
consumes: []
produces:
- codebase-briefing-report
context:
  window: fork
metadata:
  tier: knowledge
  stability: experimental
  dependencies: []
output_contract: docs/reports/CODEBASE-REPORT.md
user-invocable: false
---

# codebase-briefing-report — a shareable snapshot of a codebase's current state

Turns exploration of an unfamiliar or evolving repository into one self-contained Markdown
document: what the system is, how it is structured, what its numbers say, and where the risk
sits. The output is meant to be read cold by a new team member or a non-author stakeholder —
not a running log of your investigation.

## ⚠️ Critical Constraints

- **Evidence, not impressions.** Every architectural claim must trace to a file, directory, or
  command output. **Why:** a report read cold becomes the reader's mental model; an unsourced
  guess propagates as fact across the whole team.
- **Snapshot, not history.** Report the state at one commit (record the SHA in the header). Do
  not narrate how you found things. **Why:** a stakeholder wants the current map, not your
  search path — investigation logs belong in scratch notes, not the deliverable.
- **Risks are named and rated, never buried.** A health section that only says "looks good" is a
  failure. Each risk gets a one-line statement + Low/Med/High rating + a concrete next action.
  **Why:** the point of handing this to a stakeholder is to surface what they cannot see; a
  flattering summary defeats the purpose.
- **No fabricated metrics.** If you cannot compute a number, write "not measured" — do not
  estimate. **Why:** a made-up test-coverage or LOC figure is worse than an absent one because
  it reads as authoritative. WRONG: `Coverage: ~70%`. CORRECT: `Coverage: not measured (no run)`.
- **One commit, one artifact.** Write a single file at the path in `output_contract`; do not
  scatter findings across many files. **Why:** the deliverable is shareable precisely because it
  is one link.

## Why This Exists

Onboarding and stakeholder updates default to either a verbal tour (lost the moment it ends) or
a sprawling wiki nobody maintains. Neither is a single artifact you can hand someone. This skill
forces a fixed shape and an evidence discipline so the report is trustworthy, comparable across
repos, and cheap to regenerate when the codebase moves.

## Quick Start

```bash
# From the repo root you are reporting on:
git rev-parse --short HEAD                 # the SHA for the header
git log -1 --format='%cd' --date=short     # last-change date
```

Then walk the four phases below and emit `docs/reports/CODEBASE-REPORT.md`.

## Workflow

### Phase 1 — Orient (what is this?)

Establish the system's identity before touching internals.

- Read the entry docs: `README*`, `CONTRIBUTING*`, top-level `*.md`, `package.json` /
  `go.mod` / `Cargo.toml` / `pyproject.toml` description fields.
- Detect languages and the build/run system (look for `Makefile`, CI config, lockfiles).
- State in one paragraph: what the system does, who uses it, and how it runs.

**Checkpoint:** you can name the system's purpose in one sentence without quoting marketing copy.
If not, keep reading entry docs before proceeding.

### Phase 2 — Map (how is it structured?)

Build the module map — the spine of the report.

- Enumerate top-level directories and the role each plays (`ls -d */`, then sample each).
- Identify entry points (`main`, server bootstrap, CLI root, exported package surface).
- Trace the dependency direction between modules (who imports whom). Note any obvious layering
  (e.g. domain / adapters / transport) or its absence.
- Produce a table: one row per significant module — name, responsibility, key files, depends-on.

**Checkpoint:** every top-level source directory appears in the module table exactly once.

### Phase 3 — Measure (what do the numbers say?)

Compute the metrics you can, mark the rest "not measured".

- Size: file count, LOC by language (`scripts/collect-metrics.sh` does this where tools exist).
- Activity: commit count, contributors, last-change date, hottest files (most-churned).
- Tests: count test files; run the suite if it is fast and safe; otherwise record "not run".
- Tooling signals: lint/typecheck config presence, CI pipeline steps, dependency counts.

**Checkpoint:** every number in the report came from a command, not a guess.

### Phase 4 — Assess (where is the risk?)

Turn observation into a health/risk summary the reader can act on.

- For each risk: a one-line statement, a **Low / Med / High** rating, and a concrete next action.
- Cover at least: test coverage gaps, single-points-of-failure (one file/person owns a domain),
  dependency staleness/security, undocumented load-bearing areas, and any layering violations.
- End with a short "if you read nothing else" list: the 3–5 things a new owner must know.

**Checkpoint:** no risk is rated without a next action attached.

## Output Specification

Write one file: **`docs/reports/CODEBASE-REPORT.md`** (override path per the calling repo's
conventions; record the chosen path). Required sections, in order:

1. **Header** — repo name, commit SHA, date generated, author/agent.
2. **What It Is** — one-paragraph purpose + run model (from Phase 1).
3. **Architecture Overview** — prose + an ASCII or Mermaid diagram of module relationships.
4. **Module Map** — the table from Phase 2.
5. **Metrics** — the numbers from Phase 3 (mark gaps "not measured").
6. **Health & Risk Summary** — the rated risk list from Phase 4.
7. **If You Read Nothing Else** — the 3–5 must-knows.

## Quality Rubric

- **Sourced:** every architectural claim cites a path or command; spot-check three at random.
- **Complete map:** the Module Map covers every top-level source directory, no orphans.
- **Actionable risk:** every risk row has a rating AND a next action — no bare observations.
- **Self-contained:** a reader who has never seen the repo understands it from the file alone.
- **Honest metrics:** no estimated numbers; gaps are explicitly marked "not measured".

## Examples

**Onboarding a new engineer:** run all four phases on the service they will own, hand them the
file on day one; the Module Map + "If You Read Nothing Else" replace a 90-minute verbal tour.

**Stakeholder/handoff update:** regenerate at a new SHA, diff against the prior report's risk
section to show what moved — staleness and new risks surface as table-row changes.

**Pre-acquisition / due-diligence read:** the Health & Risk summary becomes the technical-debt
ledger; "not measured" rows flag where deeper inspection is required.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Report reads like a search log | Narrated investigation instead of state | Rewrite Phase-by-Phase as present-tense findings; delete "I then looked at…". |
| Module Map has gaps | Skipped a top-level dir | Re-run `ls -d */`; reconcile against the table — one row per dir. |
| Metrics section empty | Tooling absent and not noted | Mark each missing number "not measured"; never leave blank or estimate. |
| Health section is all green | Risk discipline skipped | Force at least the five risk categories in Phase 4; rate each. |
| Diagram out of sync with table | Edited one, not the other | Regenerate the diagram from the Module Map as the single source. |

## See Also

- `codebase-archaeology` — deeper exploration when you do not yet understand the repo enough to
  report on it; run it first, then this.
- `codebase-audit` — domain-parameterized quality auditing when you need findings to fix, not a
  state snapshot to share.
