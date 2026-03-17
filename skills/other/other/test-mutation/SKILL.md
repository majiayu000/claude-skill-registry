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

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│                  TEST MUTATE                        │
├─────────────────────────────────────────────────────┤
│  1. Initialize (load or create tracking file)       │
│  2. Detect test command (first run only)            │
│  3. Determine scope (user picks module)             │
│  4. Spawn qa-test-mutator agent                     │
│  5. Update tracking file with results               │
│  6. Present surviving mutations                     │
│  7. User selects which to address                   │
│  8. Spawn SME to write tests                        │
│  9. Verify (new tests pass + re-mutate confirms)    │
│  10. Summary + optional commit                      │
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

What would you like to mutate?
```

**User can:**
- Pick a specific file by name or number
- Resume an in-progress file
- Re-test a completed file (useful after adding tests)
- Say "next" to get the next pending file

**Default:** The next pending module (alphabetical order). If a module is in-progress, suggest resuming it.

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

### 6. Present Surviving Mutations

**If no survivors (100% mutation score):**

```
All N mutations were caught by tests. Mutation score: 100%.

Continue with next module?
```

Proceed to step 10 (summary) or loop back to step 3 if user wants to continue.

**If survivors exist:**

```
## Mutation Results: src/payment.go

Mutation Score: 85% (34/40 killed)

### Surviving Mutations (6 found)

1. [Line 42, arithmetic] `amount + fee` → `amount - fee`
   Context: totalCharge = amount + fee
   Impact: Fee calculation would be wrong

2. [Line 78, relational] `price > 0` → `price >= 0`
   Context: if price > 0 { process() }
   Impact: Zero-price items would be processed

3. [Line 103, logical] `valid && active` → `valid || active`
   Context: if valid && active { allow() }
   Impact: Invalid users could be allowed

...

Select which survivors to write tests for (e.g., "1-3, 5" or "all"):
```

Use `AskUserQuestion` to let the user select. If there are many survivors (>10), present in batches.

### 7. User Selects

Record the user's selection. Group selected items for SME implementation.

### 8. Spawn SME to Write Tests

**Detect the appropriate SME based on project language:**
- Go → `swe-sme-golang`
- Dockerfile → `swe-sme-docker`
- Makefile → `swe-sme-makefile`
- GraphQL → `swe-sme-graphql`
- Ansible → `swe-sme-ansible`
- Zig → `swe-sme-zig`

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

### 9. Verify

**Run the test suite** to confirm new tests pass with the correct (unmutated) code.

**If new tests fail:** Report the failures. Give the SME (or yourself) one chance to fix. If still failing, report to user and let them decide.

**Re-mutate to confirm kills:** For each addressed surviving mutation:

1. Re-apply the specific mutation (Edit)
2. Run the test command
3. Verify tests now FAIL (mutation is killed)
4. Revert (`git restore`)

**If a re-applied mutation still survives:** Report to the user — the new test doesn't actually catch the mutation. The user can decide whether to try again or skip it.

Update the tracking file: mark confirmed kills, update mutation score.

### 10. Summary

```
## Mutation Testing Session Complete

### This Session
- Module tested: src/payment.go
- Mutations applied: 40
- Killed: 37 (including 3 new kills from tests written this session)
- Survived: 3 (user declined to address)
- Mutation score: 92.5%
- Tests added: 3

### Project Progress
- Modules complete: 4/10
- Overall mutation score: 89%

### Files Modified
- src/payment_test.go: Added 3 tests
- .test-mutations.json: Updated

Commit these changes?
```

**If user wants to commit:**

```bash
git add [test files] .test-mutations.json
git commit -m "$(cat <<'EOF'
test: improve mutation coverage for [module]

Mutation score: X% → Y%
- Added tests targeting N surviving mutations
- [brief description of what the new tests verify]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**After summary, ask if user wants to continue with the next module.** If yes, loop back to step 3.

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
- SME fails to write a test (report to user, mark as unaddressed)
- Some re-applied mutations still survive after new tests (report, let user decide)

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

8 modules pending. What would you like to mutate?

1. src/auth.go
2. src/api/handler.go
3. src/payment.go
4. src/models/user.go
5. src/utils/parser.go
6. src/config.go
7. src/middleware.go
8. src/router.go

> 3

Spawning qa-test-mutator for src/payment.go...

## Mutation Results: src/payment.go

Mutation Score: 85% (34/40 killed)

### Surviving Mutations (6 found)

1. [Line 42, arithmetic] `amount + fee` → `amount - fee`
2. [Line 55, relational] `total > 0` → `total >= 0`
3. [Line 78, logical] `valid && active` → `valid || active`
4. [Line 92, constant] `maxRetries = 3` → `maxRetries = 4`
5. [Line 103, statement] removed `audit.Log(transaction)`
6. [Line 118, control_flow] `if err != nil` → `if err == nil`

Address which survivors?
> 1-3, 6

Spawning swe-sme-golang to write tests...
Tests written. Running suite... All pass.

Re-applying mutations to verify...
- Mutation 1 (amount + fee → amount - fee): Now KILLED
- Mutation 2 (total > 0 → total >= 0): Now KILLED
- Mutation 3 (valid && active → valid || active): Now KILLED
- Mutation 6 (err != nil → err == nil): Now KILLED

## Session Complete

- Module: src/payment.go
- Mutation score: 85% → 95%
- Tests added: 4
- Survivors remaining: 2 (user declined)

Project: 1/8 modules complete, score: 95%

Commit?
> Yes

Committed: "test: improve mutation coverage for payment module"

Continue with next module?
> No
```
