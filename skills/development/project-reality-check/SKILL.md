---
name: project-reality-check
description: |-
  Use when comparing a project vision to code reality and turning gaps into tracked work.
  Triggers:
practices:
- pragmatic-programmer
- code-complete
hexagonal_role: supporting
consumes:
- codebase
- project-goals
produces:
- reality-check-report
- gap-beads
context_rel:
- kind: customer-of
  with: legacy-codebase-recon
- kind: supplier-to
  with: beads
skill_api_version: 1
context:
  window: fork
metadata:
  tier: judgment
  dependencies:
  - beads
  external_dependencies:
  - codebase-archaeology
  stability: experimental
output_contract: reality-check-report.md
user-invocable: false
---

# project-reality-check — measure the dream against the code, then file the gap

Two passes over a project. **Conformance:** does the code do what the README / goals / open
issues claim? **Ambition:** if it already did, how could it matter more? Both passes end the
same way — not as prose, but as concrete, tracked work items an agent can pick up.

## ⚠️ Critical Constraints

- **A gap that isn't tracked doesn't exist.** Every confirmed gap and every accepted ambition
  idea MUST become a bead (`bd`/`br`), not a paragraph. **Why:** prose findings rot in a report
  nobody re-reads; a bead enters the ready queue and gets done.
  - WRONG: "The README promises a `--json` flag but it's missing. (left in the report only)"
  - CORRECT: `bd create -t bug -p 1 "Implement --json output flag promised in README §Usage"`
- **Claims must be verified by execution, not by reading.** "The code does X" is a hypothesis
  until you run the path. **Why:** a function named `validate_input` may validate nothing; the
  README may describe an aspiration that was never merged.
  - WRONG: grep for `def export_csv` → conclude "CSV export works."
  - CORRECT: run the documented command → observe the actual output → record pass/fail.
- **Separate the two passes; never blend gap-fixing with ambition.** Finish the full
  conformance pass first. **Why:** mixing "this is broken" with "this could be cooler" hides
  real breakage behind shiny ideas and lets a half-built feature get rebranded as a roadmap.
- **The dream is evidence, not gospel.** A documented promise the project no longer wants is a
  *doc bug*, not a feature gap. **Why:** blindly filing work for every stale README line
  generates noise; the call is "make code match docs" OR "make docs match code" — decide per gap.

## Why This Exists

Projects drift. A README is written at peak optimism; the code is written under deadline. Open
issues describe a future that may already be half-built or abandoned. Nobody owns the diff
between *stated intent* and *shipped reality*, so it grows silently until onboarding breaks,
users hit promised-but-missing features, and the roadmap is a guess. This skill makes that diff
explicit and **converts it into the work queue** — the autonomous spec-conformance + roadmap
loop. It is the inverse of writing code: instead of "build to spec," it asks "where has the
build left the spec behind, and where should the spec reach further?"

## Quick Start

```bash
# 1. Gather the dream (intent sources)
ls README* docs/ GOALS* ROADMAP* CHANGELOG* 2>/dev/null
bd ready && bd list --status open   # or: br ready / br list

# 2. Gather reality (what's actually here)
git -C . log --oneline -20
# build + run the documented entrypoint, then exercise each documented claim

# 3. Produce the report, then file beads for every confirmed gap + accepted ambition idea
```

Output lands in `reality-check-report.md`; tracked work lands in the project's issue tracker.

## Methodology

### Phase 1 — Inventory the dream

Collect every **stated** claim, with a source pointer for each:

- **README** — the promise to users (features, flags, install steps, "it just works" claims).
- **GOALS / ROADMAP / PHASE docs** — the promise to the team (where this is going).
- **Open issues / beads** — declared-but-unbuilt intent (`bd list --status open`).
- **CHANGELOG "unreleased"** — claimed-done-but-maybe-not.

Write each as one falsifiable line: *"README §Usage claims `tool sync --dry-run` previews
changes without writing."* If you can't make it falsifiable, it's vibes — drop it.

**Checkpoint:** you have a numbered list of claims, each tagged with its source. Do not proceed
until every major doc has been scanned (use `codebase-archaeology` if the repo is unfamiliar).

### Phase 2 — Verify against reality

For each claim, pick the cheapest verification that actually proves it:

| Claim type | Verification (in order of strength) |
| --- | --- |
| CLI flag / command | **Run it.** Observe real output vs. the documented output. |
| Feature / behavior | Exercise the code path end-to-end; read the impl only to confirm *why* it failed. |
| Install / setup step | Follow it literally in a clean shell; note any undocumented prerequisite. |
| Architecture claim | Trace the actual call graph; confirm the named component exists and is wired. |
| Performance claim | Measure; never accept a number from a doc. |

Record one verdict per claim: **MATCH** (code does what's claimed) · **GAP** (claimed, not
delivered) · **STALE-DOC** (code moved on; the claim is wrong now) · **PARTIAL** (some of it).

**Checkpoint:** every Phase 1 claim has a verdict backed by an observed command or trace — not
a guess.

### Phase 3 — Articulate the gap as work

For each non-MATCH verdict, decide the direction and file a bead:

- **GAP / PARTIAL** → usually `bd create -t bug` (or `feature`) to *make the code match the
  dream*. Title states the exact missing behavior + its source: `"Add `--dry-run` preview
  (README §Usage promises it; command currently writes immediately)"`.
- **STALE-DOC** → `bd create -t chore` to *make the docs match the code*, or close the dream.
- Set priority by user impact: a broken documented happy-path is p0/p1; an aspirational
  roadmap item is p2/p3.
- Link related gaps so the queue shows the real shape of the work.

**Checkpoint:** the report's gap section and the tracker agree — every gap has a bead id.

### Phase 4 — Ambition rounds

Now, and only now, push past conformance. Run N rounds (default 3), each asking a sharper
question about how the project could matter more:

1. **Round 1 — adjacent usefulness:** what would the *current* users want next? (the obvious
   missing flag, the integration they keep asking for).
2. **Round 2 — new audience:** who *can't* use this today, and what one change would let them?
3. **Round 3 — leverage:** what would make this a platform others build on, not just a tool
   (API, plugin surface, machine-readable output, composability)?

Each idea gets the same discipline as a gap: a one-line falsifiable description and, if
accepted, a bead (`-t feature`, lower priority than conformance gaps). **Reject ruthlessly** —
an ambition idea that doesn't survive "would a real user notice?" does not get filed.

**Checkpoint:** ambition beads are tagged distinctly (e.g. `--label ambition`) so they never
crowd out conformance fixes in `bd ready`.

## Output Specification

Write `reality-check-report.md` at the project root with these sections:

1. **Dream inventory** — the numbered claims + sources from Phase 1.
2. **Conformance table** — claim · verdict (MATCH/GAP/STALE-DOC/PARTIAL) · evidence (the command
   run or path traced) · bead id (for non-MATCH).
3. **Gap summary** — count by verdict; the p0/p1 list called out at top.
4. **Ambition rounds** — accepted ideas with bead ids; rejected ideas with the one-line reason.
5. **Filed work** — a flat list of every bead id created, so the report is a manifest.

Every non-MATCH row and every accepted ambition idea MUST carry a real bead id. A report with
gaps and no bead ids is a FAIL.

## Quality Rubric

- **Verified, not asserted:** every MATCH/GAP verdict cites an observed command or trace, never
  "the code looks like it does X."
- **Tracked, not narrated:** count of non-MATCH verdicts == count of filed gap beads (minus any
  explicitly-closed stale dreams); zero orphan findings.
- **Two clean passes:** conformance fully resolved before any ambition idea is filed; ambition
  beads are labeled distinctly from gaps.
- **Direction decided per gap:** each gap states whether the fix is code→docs or docs→code, not
  left ambiguous.

## Examples

**Conformance gap.** README: `myctl deploy --watch tails logs after deploy.` Reality: `--watch`
is an unknown flag (`error: unrecognized argument`). Verdict: **GAP**, p1.
→ `bd create -t feature -p 1 "Implement myctl deploy --watch (README promises log tailing; flag is unrecognized)"`.

**Stale doc.** README: "Config lives in `~/.myctl.toml`." Reality: code reads
`~/.config/myctl/config.toml`; the old path is dead. Verdict: **STALE-DOC**.
→ `bd create -t chore -p 2 "Fix README config path to ~/.config/myctl/config.toml"`.

**Ambition (accepted).** Round 3: the tool prints human tables only; an agent can't consume it.
→ `bd create -t feature -p 3 --label ambition "Add --json output so the tool is scriptable/agent-consumable"`.

**Ambition (rejected).** "Add a TUI dashboard." No user has asked; the CLI is the point.
→ Logged in the report's rejected list with reason; **no bead**.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Every README line becomes a bead | Treating the dream as gospel | Decide direction per gap (code→docs vs docs→code); stale dreams are doc bugs or closures, not features. |
| Report written, nothing filed | Skipped Phase 3/4 filing | A gap not in the tracker doesn't exist; create the bead before the verdict is "done." |
| Verdicts feel hand-wavy | Verified by reading, not running | Re-do Phase 2 by executing the documented path; reading the impl only explains *why* it failed. |
| Ambition ideas drown out fixes | Rounds run before conformance closed | Finish the conformance pass first; label ambition beads so `bd ready` keeps fixes on top. |
| Unfamiliar repo, can't find the dream | No mental model yet | Run `codebase-archaeology` first to map entrypoints and docs, then return here. |

## See Also

- `codebase-archaeology` — build the mental model before reality-checking an unfamiliar repo.
- `beads` — file and track the gap/ambition work this skill produces (`bd`/`br`).
- `codebase-audit` — deeper per-domain audit (security/perf/UX) once the conformance gaps are known.
