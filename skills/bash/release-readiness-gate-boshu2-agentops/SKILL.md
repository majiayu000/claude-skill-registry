---
name: release-readiness-gate
description: |-
  Use when preparing releases with versioning, changelog, artifacts, smoke tests, tags, and go/no-go.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
context:
  window: inherit
  intent:
    mode: task
metadata:
  tier: execution
  stability: stable
  category: engineering-quality
  maturity: source
  clean_room: true
  owner: agentops
  dependencies: []
  primary_artifacts:
  - release-readiness report
  - signed release artifacts
  - annotated version tag
output_contract: 'release_readiness_report with sections: version, changelog, artifacts, smoke, gates, decision.'
---

# Release Preparations

Use this skill to take a candidate build from "the work is merged" to a recorded
**go / no-go** decision, by running a fixed pre-release sequence and capturing
evidence at each step. The deliverable is a release-readiness report, not a vibe.

## ⚠️ Critical Constraints

- **Nothing leaves the building before the go decision.** No tag push, no
  artifact upload, no announcement until the decision section says GO.
  **Why:** a release is irreversible in practice — users pull it, mirrors cache
  it, downstreams pin it. Order is: decide, *then* publish.
  - WRONG: `git push --tags && gh release create` while smoke tests are running.
  - CORRECT: gates green + smoke green → record GO → then tag and publish.
- **The version comes from the change set, not the calendar.** Read what changed
  and apply semver: breaking → MAJOR, feature → MINOR, fix-only → PATCH.
  **Why:** a PATCH that hides a breaking change silently breaks every consumer
  who trusted the number when they pinned it.
  - WRONG: bumping `1.4.3 → 1.4.4` for a release that removed a CLI flag.
  - CORRECT: `1.4.3 → 2.0.0` because a public flag was removed.
- **Build and tag from a clean, committed tree.** No uncommitted edits, no local
  patches in the artifact. **Why:** an artifact built from a dirty tree is
  unreproducible — you can never rebuild the exact bytes you shipped.
  - WRONG: `git status` shows modified files, build anyway.
  - CORRECT: tree clean at the candidate commit, then build.
- **Every readiness claim cites a command + exit code.** "Tests pass" is not
  evidence; `go test ./... → exit 0` is. **Why:** self-report skims; the gate is
  the source of truth, and the report must be re-verifiable by the next person.

## Why This Exists

Releases fail not because the code was wrong but because a step was skipped under
the pressure of shipping: the version got bumped wrong, the changelog lagged, the
artifact was built dirty, a gate was assumed green. Each skip is invisible until
a user hits it. This skill makes the pre-release sequence the same every time, so
the decision rests on evidence and the failure modes are caught before publish,
not after. It is the discipline that turns "I think it's ready" into "here is why
it is ready, step by step."

## Quick Start

```bash
# From the candidate commit, with a clean tree:
git status --porcelain             # MUST be empty
git log --oneline LAST_TAG..HEAD   # the change set you are releasing
# Run validate.sh after authoring the report to self-check this skill:
bash scripts/validate.sh
```

Work the six phases below in order. Do not advance past a red phase — fix it or
record it as a blocker. Write the result of each phase into the readiness report.

## Workflow

### Phase 1 — Version (semver)
Read the change set since the last tag (`git log LAST_TAG..HEAD`, merged PRs,
closed issues). Classify the highest-impact change and bump accordingly:
- **MAJOR** — any breaking change (removed/renamed public API, flag, schema,
  changed default, dropped platform).
- **MINOR** — backward-compatible new capability.
- **PATCH** — backward-compatible fixes only.
Pre-1.0 (`0.y.z`): treat MINOR as the breaking lane. Record the chosen version
and the one change that forced it.
**Checkpoint:** the version is written down with its justifying change.

### Phase 2 — Changelog finalize
Move the `[Unreleased]` block into a dated, versioned section. Confirm entries
are user-facing (outcomes, not commit subjects), grouped (Added / Changed /
Fixed / Removed), and that any breaking change is flagged. The version heading
must equal the version chosen in Phase 1.
**Checkpoint:** changelog top section matches the chosen version and date.

### Phase 3 — Build & sign artifacts
Confirm the tree is clean and at the candidate commit, then build the release
artifacts with the project's release tooling. Generate checksums and sign per the
project's signing policy. Capture the build command and its exit code.
**Checkpoint:** artifacts exist, checksums computed, signatures verify.

### Phase 4 — Smoke tests
Exercise the built artifact the way a user would — install/run it, hit the
primary path, confirm `--version` reports the chosen version. Smoke tests run the
*shipped* artifact, not the source tree. Capture commands and exit codes.
**Checkpoint:** the artifact runs and reports the correct version.

### Phase 5 — Run the gates
Run the project's full gate suite (tests, lint, type-check, security scan, and
any repo-specific bundle — run the whole bundle or its script, not a remembered
subset). Record each gate's command and exit code. A non-zero exit is a blocker.
**Checkpoint:** every gate reported with command + exit code.

### Phase 6 — Tag & go/no-go
With all phases green, record the **GO** decision, then create the annotated tag
at the candidate commit (`git tag -a vX.Y.Z`). If any phase is red, record
**NO-GO** with the specific blocker and the fix needed. Publishing (tag push,
artifact upload, announcement) happens only after GO is recorded.
**Checkpoint:** the decision section names a verdict and, for NO-GO, the blocker.

## Output Specification

Write a `release-readiness report` (filename `RELEASE-READINESS.md` or inline in
the release issue) with these sections, in order:

- **version** — chosen `vX.Y.Z`, the bump level, and the change that forced it.
- **changelog** — confirmation the section is finalized and matches the version.
- **artifacts** — what was built/signed, checksums, the build command + exit.
- **smoke** — what was exercised on the artifact, commands + exit codes.
- **gates** — each gate, its command, and its exit code.
- **decision** — `GO` or `NO-GO`; NO-GO lists each blocker and its fix.

## Quality Rubric

- [ ] The version is justified by a named change and follows semver.
- [ ] Every gate and smoke result shows its command and a real exit code (no
      "passed" without evidence).
- [ ] The tree was clean and the tag points at the exact built commit.
- [ ] The decision is explicit; a NO-GO names blockers and their fixes.

## Examples

**GO (patch release).** Change set is two bug fixes → `1.4.3 → 1.4.4`. Changelog
`Fixed` section finalized. `make build && make sign` → exit 0, checksums verify.
`./dist/app --version` → `1.4.4`. `make test lint` → exit 0. Decision: **GO** →
`git tag -a v1.4.4`.

**NO-GO (caught at gates).** Feature release `2.1.0 → 2.2.0`, changelog ready,
artifact built. Smoke green, but `make security` → exit 1 (a new dependency has a
known CVE). Decision: **NO-GO** — blocker: vulnerable dependency in lockfile; fix:
bump or replace, re-run from Phase 3. No tag created.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `git status` not empty at build | uncommitted edits | commit or stash, rebuild from clean tree |
| `--version` shows wrong number | version not propagated to build | wire version from the tag/source, rebuild |
| Gate "passed" but no exit code | self-report, not evidence | re-run the gate, capture the exit code |
| Breaking change in a PATCH | semver misread in Phase 1 | reclassify to MAJOR, redo version + changelog |
| Signature verify fails | wrong key / corrupted artifact | re-sign with the release key, recompute checksums |

## See Also

- `changelog-md-workmanship` — finalize the changelog block in Phase 2.
- `gh-actions` — automate the build/sign/publish steps once the decision is GO.
