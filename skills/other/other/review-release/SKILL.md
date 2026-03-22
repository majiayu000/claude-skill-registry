---
name: review-release
description: Pre-release readiness review. Scans for debug artifacts, version mismatches, changelog gaps, git hygiene issues, breaking changes, and license compliance. Runs tests and build verification. Presents consolidated findings for human review before release.
model: opus
---

# Release Review - Pre-Release Readiness Check

Pre-flight checklist before cutting a release. Spawns a scanner agent for static analysis, runs execution-based checks (tests, build, doc freshness), then presents consolidated findings for human review. Runs all checks without interruption, then presents the full picture for decision-making.

## Philosophy

**Surface issues, don't silently fix them.** A release is a commitment to users. Every issue deserves human review before shipping. The only auto-fixes offered are mechanical debug artifact removals.

**Run everything, then report.** Run all checks — static analysis, tests, build, doc freshness — without interruption. Present the full picture at the end so the user can make informed decisions with complete information.

**Err toward reporting.** A false positive costs seconds. A missed issue ships to users.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────┐
│                     RELEASE REVIEW                       │
├──────────────────────────────────────────────────────────┤
│  1. Determine release context                            │
│  2. Spawn qa-release-engineer agent (static analysis)    │
│  3. Run test suite                                       │
│  4. Run build verification                               │
│  5. Check documentation freshness                        │
│  6. Present full consolidated report                     │
│  7. User selects which items to address                  │
│  8. Implement selected fixes                             │
│  9. Re-verify affected checks                            │
│ 10. Final summary with release recommendation            │
└──────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Release Context

**Detect automatically:**
- Last tag: `git describe --tags --abbrev=0` (if no tags, note this)
- Project type and language from manifest files
- Test command (detect from Makefile, package.json, go.mod, Cargo.toml, pyproject.toml, etc.)
- Build command (detect from Makefile, package.json, go.mod, Cargo.toml, pyproject.toml, etc.)

**Ask the user two questions:**

1. "What version are you releasing?" (Optional — enables version consistency checking against a target. If the user skips this, still check that all discovered versions agree with each other.)

2. "Any checks you want to skip?" Present options:
   - **Run everything** (Recommended)
   - **Skip build verification** (if no build step, or build is very slow)
   - **Skip doc freshness check**
   - **Skip license compliance**

### 2. Spawn qa-release-engineer Agent

**Prompt:**
```
Perform a release readiness scan of this codebase.
Last tag: [tag or "none"]
Target version: [version if provided, else "not specified"]
Scope: entire codebase

Scan for: debug artifacts, version consistency, changelog coverage,
git hygiene, breaking changes, license compliance.

Return structured findings with severity levels (BLOCKER/WARNING/INFO).
```

### 3. Run Test Suite

**Detect test command** (try in order):
1. `Makefile` with `test` target → `make test`
2. `package.json` with `test` script → `npm test`
3. `go.mod` present → `go test ./...`
4. `Cargo.toml` → `cargo test`
5. `pyproject.toml` or `setup.py` → `pytest` or `python -m pytest`
6. If none detected, ask the user

**Run the test command.** Report:
- PASS → add as INFO: "Test suite: all tests pass"
- FAIL → add as BLOCKER with failure summary (which tests failed, error output)

### 4. Run Build Verification

**Skip if user opted out in step 1.**

**Detect build command** (try in order):
1. `Makefile` with `build` target → `make build`
2. `package.json` with `build` script → `npm run build`
3. `go.mod` present → `go build ./...`
4. `Cargo.toml` → `cargo build --release`
5. `pyproject.toml` with build config → detect build tool (`python -m build`, `poetry build`, etc.)
6. If none detected, skip with INFO: "No build command detected, skipping build verification"

**Run the build command.** Report:
- PASS → add as INFO: "Build: clean build successful"
- FAIL → add as BLOCKER with error output

### 5. Check Documentation Freshness

**Skip if user opted out in step 1.**

**Spawn `doc-maintainer` agent** in assessment-only mode:

```
Perform a documentation freshness assessment only. DO NOT make any changes.
Review all documentation files (README, CHANGELOG, CLAUDE.md, doc/, etc.)
for staleness relative to the current codebase.
Report which documents appear outdated and what specifically seems wrong.
```

**Add findings as WARNINGs.** Include a note: "Run `/review-doc` to update documentation before release."

### 6. Present Full Consolidated Report

Merge all findings from steps 2-5 into a single numbered list:

```
## Release Readiness Report

Target: v1.3.0 (from v1.2.3, 47 commits)

### BLOCKERS (3)
1. [GIT] src/auth.go:42 — Merge conflict markers
2. [DEBUG] src/api/handler.go:15 — console.log("debug request body")
3. [TESTS] 2 test failures: TestPaymentFlow, TestAuthRefresh

### WARNINGS (4)
4. [CHANGELOG] Not updated since v1.2.3
5. [DEBUG] TODO markers in 3 files
6. [LICENSE] New dependency 'foo-lib' — unknown license
7. [DOCS] README.md references removed function parseConfig()

### PASSED
- Version consistency: All manifests agree (1.3.0)
- Build: Clean build successful
- Git hygiene: No large binaries, no tracked secrets
- Breaking changes: No undocumented API changes

Select items to address (e.g., "1-3", "all blockers", "all"):
```

**Use `AskUserQuestion`** with multi-select. Support shortcuts: "all blockers", "all warnings", "all", or specific numbers.

### 7. Implement Selected Fixes

Group selected items by type and handle appropriately:

#### Debug artifact removal (auto-fixable)
Handle directly as orchestrator. Remove the debug statement/line. Show the user what was removed.

#### TODO/FIXME markers (auto-fixable if selected)
Remove the marker comment. Show what was removed. The user selected these knowing they'd be deleted.

#### Merge conflict markers
Cannot auto-fix — the user must resolve conflicts manually. Report the file and conflicting content. Skip.

#### Test failures
Cannot auto-fix from here. Suggest: "Test failures require investigation. Fix manually or use `/implement` to address."

#### Build failures
Cannot auto-fix from here. Report the error and suggest investigating.

#### Changelog gaps
Cannot auto-generate meaningful entries. Offer to scaffold a changelog entry by listing commits since last tag, organized by type (features, fixes, etc.). The user fills in the details.

#### Version mismatches
If the user provided a target version, offer to update version numbers in manifest files to match. This is mechanical and safe for manifests. For source code constants, show the file and line — the user confirms.

#### License issues
Report only. The user must decide whether the dependency is acceptable.

#### Doc staleness
Suggest running `/review-doc`. Do not attempt fixes.

#### Breaking changes
Report only. The user must decide whether to document, revert, or accept.

### 8. Re-verify Affected Checks

After implementing fixes, re-verify only the checks that were affected:

- Debug artifacts removed → quick Grep to confirm none remain
- Version numbers updated → re-check consistency
- If nothing else changed, skip re-verification

Do NOT re-run the full test suite or build at this step (the user can do that separately). Only re-verify the fast, static checks.

### 9. Final Summary

```
## Release Review Complete

### Status
- BLOCKERS resolved: 2/3 (1 requires manual fix)
- WARNINGS addressed: 2/4
- Items skipped: 3 (user declined)

### Changes Made
- Removed 1 console.log statement (src/api/handler.go:15)
- Removed 3 TODO markers

### Remaining Issues
- [BLOCKER] Merge conflict markers in src/auth.go — manual resolution needed
- [WARNING] CHANGELOG.md not updated
- [WARNING] New dependency 'foo-lib' license unverified

### Recommendation
HOLD — 1 unresolved BLOCKER remains
```

**Recommendation logic:**
- **HOLD**: Any unresolved BLOCKERs
- **PROCEED WITH CAUTION**: Only WARNINGs remain
- **READY TO RELEASE**: No BLOCKERs or WARNINGs

**If changes were made**, ask the user if they want to commit:

```bash
git add [specific files modified]
git commit -m "$(cat <<'EOF'
chore: pre-release cleanup

[Brief description of what was removed/fixed]
EOF
)"
```

## Agent Coordination

**Sequential execution:**
- One agent at a time
- Wait for completion before spawning next

**Agents used:**
- `qa-release-engineer`: Static analysis scan (step 2)
- `doc-maintainer`: Documentation freshness assessment only (step 5)

**State to maintain (as orchestrator):**
- Release context (last tag, target version, skipped checks)
- Agent findings (from qa-release-engineer)
- Execution check results (tests, build, docs)
- Consolidated finding list with numbering
- User selections
- Fix results
- Running totals for summary

## Abort Conditions

**Abort workflow:**
- User interrupts
- Not a git repository
- No permission to run test/build commands

**Do NOT abort for:**
- No tags found (use initial commit as baseline, note in report)
- Individual check failures (report and continue)
- Agent finding no issues (exit gracefully — "Release looks clean")
- Test or build failures (report as BLOCKERs, continue with other checks)

## Test/Build Command Detection

**Test commands** (try in order):
1. `Makefile` with `test` target → `make test`
2. `package.json` with `test` script → `npm test`
3. `go.mod` → `go test ./...`
4. `Cargo.toml` → `cargo test`
5. `pyproject.toml` or `setup.py` → `pytest`
6. Ask user if none detected

**Build commands** (try in order):
1. `Makefile` with `build` target → `make build`
2. `package.json` with `build` script → `npm run build`
3. `go.mod` → `go build ./...`
4. `Cargo.toml` → `cargo build --release`
5. `pyproject.toml` with build config → `python -m build`
6. Skip with INFO if none detected

## Example Session

```
> /review-release

What version are you releasing?
> 2.0.0

Any checks to skip?
> Run everything

Spawning qa-release-engineer agent for static analysis...
Running tests: go test ./...
Running build: make build
Checking documentation freshness...

## Release Readiness Report

Target: v2.0.0 (from v1.9.2, 89 commits)

### BLOCKERS (2)
1. [DEBUG] src/api/handler.go:15 — fmt.Println debug statement
2. [VERSION] Version not bumped to 2.0.0 (currently 1.9.2)

### WARNINGS (4)
3. [CHANGELOG] Not updated since v1.9.2
4. [BREAKING] Removed ParseConfig() — not in changelog
5. [DEBUG] TODO markers in 2 files
6. [DOCS] README.md references removed ParseConfig()

### PASSED
- Tests: All pass
- Build: Clean
- Git hygiene: Clean
- License: Compatible

Select items to address:
> 1, 2, 5

Removing debug statement from src/api/handler.go:15... done.
Updating version to 2.0.0 in package.json... done.
Updating version to 2.0.0 in src/version.go... done.
Removing TODO markers from src/migrate.go:12, src/config.go:55... done.

Re-verifying... no debug artifacts remain, versions consistent.

## Release Review Complete

### Status
- BLOCKERS resolved: 2/2
- WARNINGS addressed: 1/4
- Items skipped: 3 (user declined)

### Changes Made
- Removed 1 debug statement (src/api/handler.go:15)
- Updated version to 2.0.0 in package.json, src/version.go
- Removed 2 TODO markers

### Remaining Issues
- [WARNING] CHANGELOG.md not updated
- [WARNING] Removed ParseConfig() not documented as breaking change
- [WARNING] README.md references removed function (run /review-doc)

### Recommendation
PROCEED WITH CAUTION — 3 warnings remain

Commit changes?
> Yes

Committed: "chore: pre-release cleanup for v2.0.0"
```
