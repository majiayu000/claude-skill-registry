---
name: dependency-update-safety
skill_api_version: 1
description: |-
  Use when updating dependencies safely with changelog review, small batches, tests, and rollback.
  Triggers:
practices:
- evidence-driven
- supply-chain-integrity
- incremental-change
hexagonal_role: driven-adapter
consumes:
- repo-context
- manifest-and-lockfile
produces:
- dependency-update-report.md
context_rel:
- kind: supplier-to
  with: validate
user-invocable: false
context:
  window: fork
  intent:
    mode: task
  intel_scope: topic
metadata:
  tier: library
  stability: experimental
  category: engineering-quality
  clean_room: true
  owner: agentops
  dependencies:
  - standards
output_contract: 'file: dependency-update-report.md (batches applied, results, rollbacks)'
---
# Library Updater — keep dependencies current without breaking the build

A disciplined loop for upgrading dependencies: audit what is behind, read what
changed, apply in small reversible batches, test between each batch, and roll
back the instant a batch regresses. The build stays green from start to finish.

## ⚠️ Critical Constraints

- **Never bump everything at once.** Batch by risk (patch → minor → major,
  smallest first) and test between batches. **Why:** a single all-in upgrade that
  fails gives you no way to know which package broke it, forcing a full revert.
  - WRONG: `npm update && npm test` (one giant diff, no bisect path)
  - CORRECT: patch batch → test → commit → minor batch → test → commit → ...
- **The lockfile is part of the change.** Always commit the manifest AND the
  lockfile together. **Why:** committing `package.json` without `package-lock.json`
  (or `go.mod` without `go.sum`) ships a non-reproducible build that resolves
  differently on the next machine.
- **Read the changelog before a major bump, every time.** **Why:** majors signal
  breaking changes by convention; upgrading blind turns a 10-minute read into a
  multi-hour debugging session.
- **A clean working tree is the precondition, not a nicety.** Refuse to start with
  uncommitted changes. **Why:** rollback (`git checkout -- <manifest> <lockfile>`)
  is only clean when there is nothing else to lose.
- **Pinned-for-a-reason stays pinned.** Honor existing version pins / ranges and
  any `// pinned: <reason>` comments. **Why:** a deliberate hold (known
  regression, peer-dep conflict, license) is institutional memory; silently
  bumping past it reintroduces a solved problem.

## Why This Exists

Dependency drift is silent until it is expensive: security advisories pile up,
majors stack so high the eventual upgrade is a rewrite, and "just update
everything" upgrades fail with no way to tell which package broke. Agents make
this worse by bumping in one shot and declaring victory before tests run. This
skill enforces the only safe shape — small batches, evidence between each,
clean rollback — so currency never costs the build.

## Quick Start

```bash
# 1. Detect ecosystem + list what is behind (writes outdated.txt)
bash {baseDir}/scripts/audit-deps.sh > outdated.txt

# 2. (after each batch) verify the build still passes for THIS ecosystem
bash {baseDir}/scripts/run-tests.sh   # exit 0 = green, non-zero = roll back

# 3. self-check this skill
bash {baseDir}/scripts/validate.sh
```

## Workflow

### Phase 0 — Preconditions
- Confirm a clean tree: `git status --porcelain` must be empty. If not, stop and
  surface it; do not proceed.
- Identify the baseline test command (CI config, `Makefile`, `package.json`
  scripts). Record it; it is the gate for every batch.
- **Checkpoint:** tree clean AND a known-green test command exists.

### Phase 1 — Audit (current vs latest)
- Run `scripts/audit-deps.sh` to enumerate outdated packages with current →
  wanted → latest and the jump type (patch / minor / major).
- Note any pins, ranges, or `pinned:` comments — these are excluded from bumping.
- **Checkpoint:** `outdated.txt` lists every candidate with its jump type.

### Phase 2 — Plan the batches
- Group candidates into ordered batches: **patch**, then **minor**, then **each
  major individually** (majors are never batched together).
- For every major, read its changelog / release notes and record the breaking
  changes and required code edits before touching anything.
- **Checkpoint:** a written batch plan; every major has a changelog summary.

### Phase 3 — Apply + test, one batch at a time
- Apply exactly one batch (update manifest + regenerate lockfile).
- Run the baseline test command via `scripts/run-tests.sh`.
- **Green:** commit the manifest + lockfile with a scoped message, then continue.
- **Red:** roll back this batch only (`git checkout -- <manifest> <lockfile>` and
  reinstall), record the failure, and either split the batch finer or skip the
  offending package. Never carry a red batch forward.
- **Checkpoint:** after each batch the suite is green and the change is committed.

### Phase 4 — Report
- Write `dependency-update-report.md`: batches applied, packages bumped with
  before→after versions, packages skipped (with reason), rollbacks, and remaining
  majors deferred for follow-up.
- **Checkpoint:** report exists; tree is clean and green.

## Output Specification

- **Filename:** `dependency-update-report.md` (repo root or a path the caller gives).
- **Format:** sections — `Applied` (table: package | from → to | jump | batch),
  `Skipped` (package | reason), `Rolled back` (package | failure), `Deferred`
  (majors needing dedicated work). Each applied batch links its commit SHA.

## Quality Rubric

- Every applied batch has a corresponding green test run AND a commit — no batch
  is committed without a passing suite.
- Manifest and lockfile are committed together in every batch (verifiable in
  `git show <sha> --stat`).
- Every major version bump cites the changelog section that documents its
  breaking changes.
- The report accounts for every outdated package: applied, skipped, rolled back,
  or explicitly deferred — none silently dropped.

## Examples

**npm, mixed jumps.** `audit-deps.sh` finds 6 outdated: 3 patch, 2 minor, 1 major
(`react 18→19`). Batch 1 (patches) → test green → commit. Batch 2 (minors) →
green → commit. Batch 3 (react major): read the v19 migration notes, apply, fix
the two breaking call sites, test → green → commit. Report records all three.

**Rollback path.** A minor batch turns the suite red. Run
`git checkout -- package.json package-lock.json && npm ci`, suite green again.
Bisect: re-apply the minor packages one at a time; `lodash 4.17.20→4.17.21` is
the culprit. Skip it, record "skipped: 4.17.21 breaks <test>", continue.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Tests red after a batch | One package in the batch regressed | Roll back the batch, re-apply packages singly to bisect |
| Lockfile churns with no manifest change | Transitive resolution drift | Commit the lockfile-only change as its own batch; test first |
| `audit-deps.sh` finds no manifest | Unsupported / nested ecosystem | Run from the project root; pass the manifest dir as `$1` |
| Major bump compiles but fails at runtime | Behavioral breaking change | Re-read changelog "Breaking" section; this is a code-edit batch, not a version bump |
| Rollback leaves stale installed deps | Reinstall step skipped | After `git checkout`, rerun the install (`npm ci` / `pip install -r` / `go mod download`) |

## See Also

- `scripts/audit-deps.sh` — **Execute**: lists outdated deps with jump types.
- `scripts/run-tests.sh` — **Execute**: runs the ecosystem's test gate; exit code is the verdict.
- `scripts/validate.sh` — **Execute**: self-checks this skill's structure and scripts.
