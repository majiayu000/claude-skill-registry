---
name: mutation-testing
description: "This skill should be used when performing AI-powered mutation testing to evaluate and improve unit test quality. It generates targeted code mutants, runs tests to identify surviving mutants, and strengthens or creates tests to kill them. Accepts a file path, directory, or defaults to git diff changed files."
---

# AI-Powered Mutation Testing

Target: $ARGUMENTS

If no argument provided, default to files changed in the current branch (via `git diff`).

This skill implements the mutation testing workflow: generate targeted mutants, filter unproductive ones, run tests to find survivors, and harden the test suite by strengthening or creating tests that kill surviving mutants.

## Step 1: Gather Context

### 1a. Identify Target Files

Determine what to mutate based on `$ARGUMENTS`:

1. **File path** — Mutate the specified source file
2. **Directory** — Mutate source files in the directory (exclude test files)
3. **No argument** — Use git diff to find changed source files:
   ```bash
   git diff --name-only $(git merge-base HEAD main)...HEAD -- '*.ts' '*.tsx' ':!*.spec.*' ':!*.test.*'
   ```

If no target files found, notify the user and stop.

### 1b. Gather Supporting Context

For each target source file, collect:

1. **Source code** — Read the full file contents
2. **Existing tests** — Find corresponding test files (`*.spec.ts`, `*.test.ts`) via naming convention or import analysis
3. **Test coverage** — Run tests with coverage for the target file to identify uncovered lines:
   ```bash
   bun run test -- --coverage --collectCoverageFrom='<target-file>' --silent 2>&1 | tail -20
   ```
4. **Recent git history** — Check for recent defects or frequent changes:
   ```bash
   git log --oneline -10 -- <target-file>
   ```
5. **Risk factors** — Assess which risk factors apply to each file:

| Risk Factor | Indicators |
|---|---|
| Data security / compliance | Handles PII, auth, authorization, encryption, tokens |
| Integrations | External API calls, HTTP clients, webhooks, message queues |
| Code vs data model | Database queries, ORM entities, schema validation |
| Historic defects | Frequent bug-fix commits, complex conditional logic |
| Change impact | Exported utility functions, shared modules, base classes |
| Performance | Loops over large datasets, recursive calls, caching logic |

### 1c. Determine Test Runner

Detect the project's test framework from `package.json` scripts and devDependencies:
- **Jest**: `bun run test`
- **Vitest**: `bun run test`
- Other: adapt accordingly

## Step 2: Generate Mutants

### 2a. Create Experimental Branch

```bash
git stash --include-untracked || true
git checkout -b mutation-testing/$(date +%Y-%m-%d-%H%M%S)
git stash pop || true
```

### 2b. Generate Risk-Factor-Guided Mutants

For each target source file, generate **3-5 mutants** that target the identified risk factors. Apply these mutation operators:

| Operator Type | Examples |
|---|---|
| **Decision mutations** | Change `>` to `>=`, `&&` to `\|\|`, `===` to `!==` |
| **Value mutations** | Change constants, swap string literals, alter numeric values |
| **Statement mutations** | Remove guard clauses, delete error handling, skip validation |
| **Integration mutations** | Remove timeout handling, skip error code checks, bypass retry logic |
| **Security mutations** | Remove auth checks, bypass input validation, expose sensitive data in logs |

For each mutant, produce:

1. **Mutant ID** — Sequential identifier (M001, M002, etc.)
2. **File and line** — Exact location of the change
3. **Mutation description** — What was changed and why
4. **Risk factor** — Which risk factor this targets
5. **The code change** — A minimal, atomic edit to introduce the defect

**Mutant quality criteria** — Each mutant must be:
- **Non-trivial** — Not just whitespace, comments, or formatting
- **Buildable** — The project must still compile/typecheck
- **Realistic** — Simulates a plausible programming error
- **Targeted** — Addresses a specific risk factor
- **Atomic** — Exactly one logical change per mutant

### 2c. Apply and Validate Each Mutant

For each generated mutant, one at a time:

1. **Apply the mutation** — Edit the source file to introduce the defect
2. **Build check** — Run `bun run typecheck` to verify the project still compiles
   - If build fails: discard the mutant, revert the change, log failure reason, continue to next
3. **Commit the mutant** — `git commit -am "mutant: M00X - <description>"`

## Step 3: Filter Mutants

### 3a. Run Tests Against Each Mutant

Process mutants in reverse order (LIFO — latest commit first):

1. **Run relevant tests** against the mutant:
   ```bash
   bun run test -- <test-file-path> --silent 2>&1
   ```
2. **Evaluate result**:
   - **Test fails** (mutant killed) → Revert the mutant commit. Log as killed. Proceed to next mutant.
   - **Test passes** (mutant survived) → The mutant reveals a test gap. Keep it for Step 4.

### 3b. Equivalence Detection for Surviving Mutants

For each surviving mutant, verify it is not semantically equivalent to the original:

1. **AST-level comparison** — Compare the diff. If the change is purely syntactic (reordering independent statements, renaming to equivalent aliases), discard it.
2. **Behavioral analysis** — Reason about whether any input could distinguish the mutant from the original:
   - If no distinguishing input exists → Discard as equivalent
   - If a distinguishing input exists → Keep as a unique actionable mutant
   - If uncertain → Keep and flag for human review

### 3c. Record Mutant Metadata

For each mutant, maintain a record:

```json
{
  "mutant_id": "M001",
  "file": "<source-file>",
  "line": 42,
  "risk_factor": "Data security / compliance",
  "description": "Removed authentication check before data access",
  "status": "survived|killed|equivalent|discarded",
  "commit_hash": "<hash>",
  "tests_run": ["test-file.spec.ts"],
  "equivalence_result": "not_equivalent|equivalent|uncertain"
}
```

Print a summary table after filtering:

```
| Mutant | File | Risk Factor | Status |
|--------|------|-------------|--------|
| M001   | ... | ...          | survived |
| M002   | ... | ...          | killed   |
```

## Step 4: Harden Test Suite

For each **surviving, non-equivalent** mutant:

### 4a. Determine Test Strategy

1. **Existing test covers the mutated region** → Strengthen the existing test
2. **No test covers the mutated region** → Generate a new test

### 4b. Strengthen Existing Test or Generate New Test

**When strengthening an existing test**, modify the test to:
- Add assertions that detect the behavioral difference introduced by the mutant
- Add or modify test inputs that expose the defect in the mutant code
- Preserve the test method name, signature, and overall structure
- Avoid adding trivial or unrelated checks

**When generating a new test**, create a test that:
- Specifically exercises the behavioral difference between original and mutant code
- Uses strong, precise assertions that detect the exact defect
- Focuses on the identified risk factor
- Includes realistic test data that exposes the mutant's flawed behavior
- Follows existing test naming conventions and structure from the codebase

### 4c. Validate Each Test (3-attempt limit)

For each improved or new test, validate with up to 3 attempts:

1. **Revert the mutant** — Switch to original code
2. **Build check** — Ensure the test compiles
3. **Run on original code** — Test must PASS on unmodified code
4. **Re-apply the mutant** — Switch back to mutated code
5. **Run on mutant code** — Test must FAIL on the mutant

If validation fails, refine the test (up to 3 total attempts). If still failing after 3 attempts, flag for manual review.

### 4d. Apply Decision Matrix

Classify each test result:

| Original Code | Mutant Code | Signal | Action |
|---|---|---|---|
| Builds + Passes | Builds + Fails | Strong detection | **Keep** — alert developer |
| Builds + Passes | Builds + Passes | Weak assertion | **Refine** — strengthen assertion |
| Builds + Fails | Builds + Passes | Bad test | **Discard** — generate new test |
| Doesn't build | Any | Broken test | **Discard** — generate new test |
| Builds + Passes | Doesn't build | Untestable mutant | **Discard** — notify developer |
| Builds + Fails | Builds + Fails | Ambiguous signal | **Discard** — generate new test |

### 4e. Finalize Tests

For each validated test:
1. Add an inline comment above the test referencing the mutant:
   ```typescript
   // Test hardened to kill mutant M001 (Risk Factor: Data security / compliance)
   ```
2. Commit the test improvement to the experimental branch

## Step 5: Cleanup and Report

### 5a. Revert All Mutants

Remove all mutant commits from the experimental branch, keeping only test improvements:

```bash
# Revert mutant commits (identified by "mutant:" prefix in commit message)
git log --oneline | grep "^.* mutant:" | awk '{print $1}' | while read hash; do
  git revert --no-commit "$hash"
done
git commit -m "chore: revert all mutants after test hardening"
```

### 5b. Validate Clean State

1. Run full test suite on the clean code with test improvements:
   ```bash
   bun run test 2>&1
   ```
2. All tests must pass. If any fail, investigate and fix.

### 5c. Report Results

Print a comprehensive mutation testing report:

```
## Mutation Testing Report

**Target**: <files tested>
**Date**: <timestamp>
**Branch**: <experimental branch name>

### Summary
- Total mutants generated: X
- Killed by existing tests: X
- Survived (test gaps found): X
- Equivalent (discarded): X
- Build failures (discarded): X
- **Mutation Score**: X% (killed / (total - equivalent))

### Test Improvements
- Tests strengthened: X
- New tests generated: X
- Tests validated successfully: X
- Tests requiring manual review: X

### Surviving Mutants (Unresolved)
| Mutant | File | Line | Risk Factor | Description |
|--------|------|------|-------------|-------------|
| M00X   | ...  | ...  | ...         | ...         |

### Oracle Gap
- Code coverage: X%
- Mutation score: X%
- Oracle gap: X% (coverage - mutation score)

### Risk Factor Coverage
| Risk Factor | Mutants | Killed | Survived | Score |
|---|---|---|---|---|
| Data security | X | X | X | X% |
| Integrations  | X | X | X | X% |
```

### 5d. Present Options

Ask the user:

1. **Merge test improvements** — Cherry-pick test commits to the original branch, delete experimental branch
2. **Keep experimental branch** — For further review before merging
3. **Discard everything** — Delete the experimental branch, no changes kept

If the user chooses to merge:
```bash
git checkout <original-branch>
git cherry-pick <test-improvement-commits>
git branch -D <experimental-branch>
```

## Never

- Modify test files to make them pass on mutants (defeats the purpose)
- Generate mutants in test files (only mutate source code)
- Skip the build check after generating a mutant
- Commit mutants to protected branches (dev, staging, main)
- Leave mutant code in the codebase after completion
- Generate more than 5 mutants per file (diminishing returns)
- Skip equivalence detection for surviving mutants
- Mark a test as valid without running it on both original and mutant code
- Use `--no-verify` with any git command
