---
name: test-mutation
description: Mutation testing workflow. Systematically mutates source code to verify tests actually catch bugs. Multi-session with progress tracking.
model: opus
---

# Test Mutate - Mutation Testing Workflow

Systematically introduces small changes (mutations) to source code, runs the test suite after each, and reports which mutations survive (tests don't catch them). Surviving mutations reveal genuine test coverage gaps that line coverage misses.

## Philosophy

**Mutation score > line coverage.** A test that executes code but doesn't assert on results gives 100% line coverage and 0% mutation score. Mutation testing answers the real question: if a bug were introduced here, would the tests catch it?

**Multi-session by design.** Mutation testing is slow — each mutation requires a full test run. Progress is tracked in `.test-mutations.json` so you can work through a codebase incrementally across sessions.

**Autopilot by default.** After initial setup, the workflow runs unattended through all in-scope modules. It addresses all surviving mutations, commits after each module, and moves on. Human intervention is only needed during setup (scope selection, test command verification) and if an unrecoverable error occurs.

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│                  TEST MUTATE                        │
├─────────────────────────────────────────────────────┤
│  SETUP (interactive)                                │
│  1. Initialize (load or create tracking file)       │
│  2. Detect test command (first run only)            │
│  3. Determine scope (user selects, default: all)    │
│                                                     │
│  EXECUTION (autopilot — no user interaction)        │
│  For each module in scope:                          │
│    4. Spawn qa-test-mutator agent                   │
│    5. Update tracking file with results             │
│    6. Spawn SME to write tests for ALL survivors    │
│    7. Verify (new tests pass + re-mutate confirms)  │
│    8. Commit changes                                │
│  9. Final summary                                   │
└─────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Initialize

Check for `.test-mutations.json` in the project root.

**If the file exists:**
- Load tracking data
- Show progress summary: X/Y modules tested, overall mutation score Z%
- List modules by status (completed, in-progress, pending)
- Proceed to step 3 (scope selection)

**If the file doesn't exist:**
- This is a first run — proceed to step 2 (test command detection)
- After detecting the test command, discover source files (see Module Discovery below)
- Create the tracking file with initial structure
- Ask user: "Should I commit `.test-mutations.json` to version control, or add it to `.gitignore`?"

### 2. Detect Test Command

**Try in order:**

1. `Makefile` with a `test` target → `make test`
2. `package.json` with a `test` script → `npm test`
3. `go.mod` present → `go test ./...`
4. `pyproject.toml` or `pytest.ini` or `setup.cfg` with pytest config → `pytest`
5. `Cargo.toml` → `cargo test`
6. `build.gradle` or `build.gradle.kts` → `gradle test`

**If none detected:** Ask the user: "What command runs your test suite?"

**Verify the command works** by running it once. If it fails, report the error and ask the user for the correct command.

Store the test command in the tracking file.

### Module Discovery

Use Glob to find source files in the project. Exclude:
- Test files (`*_test.go`, `test_*.py`, `*.test.js`, `*.spec.ts`, etc.)
- Vendor/dependency directories (`vendor/`, `node_modules/`, `.venv/`, `target/`)
- Generated files (files with generation markers like `// Code generated`)
- Configuration files, documentation, assets

For each source file, attempt to identify covering test files using naming conventions:
- `auth.go` → `auth_test.go`
- `auth.py` → `test_auth.py` or `auth_test.py`
- `Auth.ts` → `Auth.test.ts` or `Auth.spec.ts`

Store discovered modules in the tracking file with status `pending`.

### 3. Determine Scope

Present the current state to the user:

```
## Mutation Testing Progress

Overall: 3/10 modules tested (mutation score: 87%)

### Completed
- src/auth.go — score: 100% (45 mutations)
- src/config.go — score: 92% (24 mutations, 2 survivors)

### In Progress
- src/payment.go — score: 80% (20/50 mutations tested)

### Pending
- src/api/handler.go
- src/models/user.go
- src/utils/parser.go
- ...

Scope? Enter file names/numbers, or press Enter to test all pending modules.
```

**User can:**
- Pick specific files by name or number (e.g., "1, 3, 5" or "src/auth.go")
- Resume an in-progress file
- Re-test a completed file (useful after adding tests)
- Press Enter / say "all" to test all pending modules (this is the default)

**Default:** All pending modules, processed in alphabetical order. If a module is in-progress, it is processed first.

**After scope is confirmed, the workflow enters autopilot mode. No further user interaction occurs until the run completes or an unrecoverable error is encountered.**

---

### Steps 4-8 repeat for each module in scope (autopilot)

### 4. Spawn Mutator Agent

Spawn a `qa-test-mutator` agent with the selected source file and test command:

```
Apply mutation testing to the following source file:
- Source file: [path]
- Test command: [command]

Systematically mutate the source code, run tests after each mutation,
and report which mutations are killed vs survived.
```

Wait for the agent to complete and collect its results.

### 5. Update Tracking File

Parse the mutator agent's results and update `.test-mutations.json`:

- Set module status to `completed` (or `in_progress` if the agent reported partial coverage)
- Populate `mutations_by_type` with results grouped by mutation type
- Store surviving mutation examples in the `examples` arrays
- Calculate `mutation_score` for the module
- Update `global_statistics` (recalculate totals and overall score)
- Set `last_updated` timestamp

Write the updated tracking file.

### 6. Spawn SME to Write Tests

**If no survivors (100% mutation score):** Log the result and proceed to step 8 (commit).

**If survivors exist:** Write tests for ALL surviving mutations.

**Detect the appropriate SME based on project language:**
- Go → `swe-sme-golang`
- Dockerfile → `swe-sme-docker`
- Makefile → `swe-sme-makefile`
- GraphQL → `swe-sme-graphql`
- Ansible → `swe-sme-ansible`
- Zig → `swe-sme-zig`
- TypeScript → `swe-sme-typescript`
- JavaScript → `swe-sme-javascript`
- HTML → `swe-sme-html`
- CSS → `swe-sme-css`

**For languages without a dedicated SME**, implement the tests directly as orchestrator.

**Prompt the SME with:**

```
Write tests to catch the following surviving mutations in [source file]:

1. Line 42: `amount + fee` → `amount - fee`
   The test must verify that the fee is ADDED, not subtracted.

2. Line 78: `price > 0` → `price >= 0`
   The test must verify behavior when price is exactly 0.

3. Line 103: `valid && active` → `valid || active`
   The test must verify that BOTH conditions are required.

Each test should:
- Target the specific behavior that the mutation would break
- Follow the project's existing test conventions
- Be focused and minimal (one assertion per concern)
- Have a clear name indicating what it verifies
```

### 7. Verify

**Run the test suite** to confirm new tests pass with the correct (unmutated) code.

**If new tests fail:** Give the SME (or yourself) one chance to fix. If still failing, log the failure, revert the failing tests (`git restore`), and continue with the next module.

**Re-mutate to confirm kills:** For each addressed surviving mutation:

1. Re-apply the specific mutation (Edit)
2. Run the test command
3. Verify tests now FAIL (mutation is killed)
4. Revert (`git restore`)

**If a re-applied mutation still survives:** Log it as an unresolved survivor and continue. Do not retry or prompt the user.

Update the tracking file: mark confirmed kills, update mutation score.

### 8. Commit

Automatically commit the changes for this module:

```bash
git add [test files] .test-mutations.json
git commit -m "$(cat <<'EOF'
test: improve mutation coverage for [module]

Mutation score: X% → Y%
- Added tests targeting N surviving mutations
- [brief description of what the new tests verify]
EOF
)"
```

Print a short progress line before moving to the next module:

```
[3/8] src/payment.go — score: 85% → 95%, 4 tests added. Continuing...
```

Then loop back to step 4 with the next module in scope.

### 9. Final Summary

After all modules in scope have been processed:

```
## Mutation Testing Complete

### Modules Tested This Session
| Module             | Before | After | Tests Added | Unresolved |
|--------------------|--------|-------|-------------|------------|
| src/auth.go        | —      | 100%  | 0           | 0          |
| src/payment.go     | —      | 95%   | 4           | 2          |
| src/config.go      | —      | 88%   | 3           | 3          |

### Project Progress
- Modules complete: 8/10
- Overall mutation score: 91%

### Unresolved Survivors
- src/payment.go:92 — `maxRetries = 3` → `maxRetries = 4` (constant)
- src/payment.go:103 — removed `audit.Log(transaction)` (statement deletion)
- src/config.go:45 — `timeout > 0` → `timeout >= 0` (relational)
- ...

### Commits Made
- abc1234 test: improve mutation coverage for auth module
- def5678 test: improve mutation coverage for payment module
- ghi9012 test: improve mutation coverage for config module
```

Report any modules that were skipped due to errors (SME failures, test failures, etc.) and why.

## Tracking File Format

**File:** `.test-mutations.json` in project root.

```json
{
  "version": "1.0",
  "test_command": "go test ./...",
  "last_updated": "2026-02-12T15:30:00Z",
  "modules": {
    "src/auth.go": {
      "status": "completed",
      "covering_tests": ["src/auth_test.go"],
      "last_tested": "2026-02-12T15:30:00Z",
      "mutations_by_type": {
        "arithmetic": {
          "total": 12,
          "killed": 11,
          "survived": 1,
          "examples": [
            {
              "line": 42,
              "original": "count + 1",
              "mutated": "count - 1",
              "result": "survived",
              "test_that_caught_it": null
            }
          ]
        }
      },
      "mutation_score": 91.7,
      "insights": []
    }
  },
  "global_statistics": {
    "total_modules": 10,
    "completed_modules": 3,
    "total_mutations": 150,
    "total_killed": 135,
    "total_survived": 15,
    "overall_score": 90.0
  }
}
```

**Field notes:**
- `examples` should include all surviving mutations (for reporting) and a few representative killed mutations (for insight). Don't store every killed mutation — just survivors and notable kills.
- `insights` are human-readable observations the mutator agent provides (e.g., "Strong error handling coverage" or "No tests for boundary conditions").
- `global_statistics` are recalculated from module data on each update.

## Agent Coordination

**All subagents MUST be executed sequentially — NEVER in parallel.** Mutation testing works by modifying source files and running tests against those modifications. Parallel agents will simultaneously edit the same files, corrupt each other's mutations, and produce meaningless results. This applies to every agent spawn in this workflow: mutator agents, SME agents, and verification steps. One agent at a time, wait for it to finish, then spawn the next.

**State management:**
- Orchestrator maintains the tracking file
- Agent returns structured results
- No state carried between agent invocations

## Abort Conditions

**Abort workflow if:**
- User interrupts
- Test command doesn't work (can't run tests)
- No source files found to mutate
- Git repository is in a dirty state that would prevent `git restore` (warn user, ask them to commit or stash first)

**Do NOT abort for:**
- Individual mutation failures (record and continue)
- Partial completion (save progress, can resume next session)
- SME fails to write a test (log the failure, revert, continue with next module)
- Some re-applied mutations still survive after new tests (log as unresolved, continue)
- New tests fail and cannot be fixed (log, revert, continue with next module)

## Example Session

```
> /test-mutation

No tracking file found. Detecting test command...
Found go.mod — using `go test ./...`
Verified: tests pass.

Discovered 8 source files to mutate.
Created .test-mutations.json

Commit tracking file to git, or add to .gitignore?
> Commit

## Mutation Testing Progress

8 modules pending.

Scope? Enter file names/numbers, or press Enter to test all pending.

1. src/api/handler.go
2. src/auth.go
3. src/config.go
4. src/middleware.go
5. src/models/user.go
6. src/payment.go
7. src/router.go
8. src/utils/parser.go

> [Enter]

Starting autopilot run for 8 modules...

[1/8] Spawning qa-test-mutator for src/api/handler.go...
      Score: 92% (46/50 killed). Writing tests for 4 survivors...
      3 killed, 1 unresolved. Score: 92% → 98%.
      Committed: "test: improve mutation coverage for handler module"

[2/8] Spawning qa-test-mutator for src/auth.go...
      Score: 100% (38/38 killed). No survivors.
      Committed: "test: record mutation coverage for auth module"

[3/8] Spawning qa-test-mutator for src/config.go...
      Score: 88% (21/24 killed). Writing tests for 3 survivors...
      2 killed, 1 unresolved. Score: 88% → 96%.
      Committed: "test: improve mutation coverage for config module"

...

[8/8] Spawning qa-test-mutator for src/utils/parser.go...
      Score: 90% (27/30 killed). Writing tests for 3 survivors...
      3 killed, 0 unresolved. Score: 90% → 100%.
      Committed: "test: improve mutation coverage for parser module"

## Mutation Testing Complete

### Modules Tested This Session
| Module                 | Before | After | Tests Added | Unresolved |
|------------------------|--------|-------|-------------|------------|
| src/api/handler.go     | —      | 98%   | 3           | 1          |
| src/auth.go            | —      | 100%  | 0           | 0          |
| src/config.go          | —      | 96%   | 2           | 1          |
| src/middleware.go      | —      | 94%   | 2           | 1          |
| src/models/user.go     | —      | 100%  | 1           | 0          |
| src/payment.go         | —      | 95%   | 4           | 2          |
| src/router.go          | —      | 91%   | 3           | 2          |
| src/utils/parser.go    | —      | 100%  | 3           | 0          |

### Project Progress
- Modules complete: 8/8
- Overall mutation score: 96%

### Unresolved Survivors (7 total)
- src/api/handler.go:88 — removed `log.Info(request)` (statement deletion)
- src/config.go:45 — `timeout > 0` → `timeout >= 0` (relational)
- ...

### Commits Made (8)
- abc1234 test: improve mutation coverage for handler module
- def5678 test: record mutation coverage for auth module
- ...
```
