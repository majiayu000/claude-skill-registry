---
name: test-fixer
description: "MANDATORY when: tests fail, CI fails, CI/CD fails, ci.yml fails, user provides CI log URL. Investigates failures, fixes iteratively until passing."
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Test Fixer - Systematic Failure Investigation & Fix Iteration

╔══════════════════════════════════════════════════════════════════════════╗
║  🚨 MANDATORY: When tests fail, you MUST use this skill                ║
║                                                                          ║
║  DO NOT:                                                                 ║
║  - ❌ Guess at fixes without investigation                              ║
║  - ❌ Report findings without attempting fixes                          ║
║  - ❌ Stop after one failed fix attempt                                 ║
║  - ❌ Leave code in broken state                                        ║
║                                                                          ║
║  GOAL: Return code to passing state with minimal changes                ║
╚══════════════════════════════════════════════════════════════════════════╝

## 🎯 Purpose

This skill provides a systematic workflow for:
1. **Investigating** test failures to identify root cause
2. **Writing fixes** based on investigation findings
3. **Iterating** until all tests pass
4. **Restoring** code to working state with minimal changes

**🚨 MANDATORY TRIGGERS - Use this skill when ANY of these occur:**

1. **After running test-runner** and ANY tests fail
2. **After code changes** and test-runner reports failures
3. **After merge/pull** and tests fail
4. **CI reports test failures** in any environment
5. **User says:** "tests are broken" OR "tests failing" OR "fix the tests"
6. **Pre-commit hook fails** due to test failures
7. **You see test error output** from any source
8. **User provides CI log URL** (Azure Blob, GitHub Actions, etc.)

### ⚡ CI Log URLs: curl IMMEDIATELY (before ANYTHING else)

CI log URLs expire in ~10 min. **First action when you see `blob.core.windows.net`:**

```bash
curl -s "<URL>" -o /tmp/ci_logs.txt && wc -l /tmp/ci_logs.txt
grep -iE "FAILED|KeyError|Error:|Exception" /tmp/ci_logs.txt | head -50
```

**🚨 DO NOT use WebFetch for CI logs:**
- WebFetch truncates large files (CI logs are often 3000+ lines)
- You'll get a summary that misses the actual errors
- curl saves the complete file locally where you can grep it

**Integration with other skills:**
- **test-runner** detects failures → immediately invoke test-fixer
- **task-complete-enforcer** finds test failures → immediately invoke test-fixer
- **Pre-commit hooks** show test failures → immediately invoke test-fixer

**🚨 CRITICAL: Do NOT investigate test failures manually. ALWAYS use this skill.**

## 🛠️ Test Infrastructure Quick Reference

| Command/File | Purpose |
|--------------|---------|
| `just lint-and-fix` | Auto-fix formatting + run linting + mypy type checks |
| `just test-all-mocked` | Fast tests with mocked external services (used in CI) |
| `just test-all` | All tests including live/e2e with real services |
| `just test-smoke` | Smoke tests requiring Docker (production-like) |
| `.pre-commit-config.yaml` | Git hooks: lint on pre-commit, full tests on pre-push |
| `.github/workflows/ci.yml` | GitHub Actions: runs `just lint` + `just test-all-mocked` on every push |
| `.github/workflows/deploy.yml` | Deployment workflow (staging/production) |

**CI/CD flow**: Push → ci.yml runs lint+mocked tests → deploy.yml deploys if tests pass

**🚨 When CI/CD fails:** Download the logs immediately (URLs expire in ~10 min) and consult `.github/workflows/ci.yml` to understand which step failed and reproduce locally.

## 🚨 CRITICAL FOR TEST WRITING

- **BEFORE writing tests** → Use test-writer skill (MANDATORY - analyzes code type, dependencies, contract)
- **AFTER writing tests** → Invoke pytest-test-reviewer agent (validates patterns)
- **YOU CANNOT WRITE TESTS WITHOUT test-writer SKILL** - No exceptions, no shortcuts, every test, every time

## 🔄 How This Skill Interacts With Other Skills

**test-fixer orchestrates the fix workflow and uses other skills:**

1. **test-runner skill** - To verify fixes work
   - After each fix attempt, use test-runner to run: `just lint-and-fix && just test-all-mocked`
   - Final verification uses test-runner's full parallel test suite

2. **test-writer skill** - When modifying test files
   - MANDATORY before changing test assertions, expectations, or fixtures
   - test-writer ensures you don't encode broken behavior into tests
   - test-writer helps determine if tests need updating or code needs fixing

3. **sql-reader skill** - To understand production data model
   - Use when debugging integration/e2e test failures
   - Query production to see actual data model state
   - Helps identify mismatches between test fixtures and reality

4. **Git repository management** - test-fixer owns git operations
   - Creates safety backups (git diff)
   - Stashes/unstashes changes during investigation
   - Manages checkout operations (HEAD, main, branches)
   - NEVER deletes user's code (always reversible operations)

## ⚠️ FUNDAMENTAL OPERATING PRINCIPLES

**YOUR MINDSET AS test-fixer:**

You are a persistent, autonomous developer who KNOWS tests can pass because:
- Tests ALWAYS pass at main (CI enforces this) - **this is a FACT**
- Therefore, a passing state EXISTS and is REACHABLE
- Your job: systematically find that state and restore it
- **You WILL get tests passing** - it's not a question of IF, only WHEN

**CRITICAL ASSUMPTIONS:**
- Tests passed at main → they can pass again
- Tests passed at branch HEAD → you can restore that state
- If tests fail now → something specific changed → that change can be identified and fixed
- **NEVER delete user's code** (always stash or use temp branch)

**GOAL:**
Return code to passing state (you KNOW it exists) with:
- ✅ All tests pass
- ✅ Original functionality preserved
- ✅ Minimal changes from original code
- ✅ No debugging artifacts left behind

## 🚨 BANNED TERMINOLOGY - NEVER Say "Tests Pass" Without Proof

**YOU ARE FORBIDDEN from saying these phrases unless ALL tests actually pass:**

❌ **BANNED:** "tests pass"
❌ **BANNED:** "tests are passing"
❌ **BANNED:** "all tests pass"
❌ **BANNED:** "tests now pass"

**To say tests pass, you MUST:**
1. Run `.claude/skills/test-runner/scripts/run_tests_parallel.sh` (full suite)
2. Check ALL log files (mocked + e2e-live + smoke)
3. Verify ZERO failures in all logs
4. See actual passing output

**You MAY say (with proof):**
- ✅ "Quick tests pass" (after `just test-all-mocked` shows 0 failures)
- ✅ "Mocked tests pass" (after `just test-all-mocked` shows 0 failures)
- ✅ "X out of Y tests now pass" (showing progress during iteration)

**Key difference from test-runner:**
- **test-runner**: Runs tests and reports status (may report failures)
- **test-fixer**: ITERATES until ALL tests pass (never stops at failures)

**Your job is NOT complete until:**
- ✅ Full parallel test suite runs successfully
- ✅ All logs show 0 failures
- ✅ You can truthfully say "all tests pass" with proof

## 🔄 ITERATIVE FIX WORKFLOW

**You can announce you're starting** ("Running systematic test fix workflow..."), but **DO NOT report partial results mid-investigation**. Complete the full cycle, THEN report complete findings.

### Phase 0: Create Safety Backup (CRITICAL - Do This First)

**BEFORE any investigation, create recoverable backup:**

```bash
# Create tmp directory if it doesn't exist
mkdir -p tmp

# Create timestamped diff backup of ALL changes (staged AND unstaged) vs HEAD
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git diff HEAD > tmp/test_fixer_start_${TIMESTAMP}.diff
git diff --staged >> tmp/test_fixer_start_${TIMESTAMP}.diff

# Announce backup location
echo "Safety backup created: tmp/test_fixer_start_${TIMESTAMP}.diff"

# CRITICAL: Remember this filename for recovery if needed
BACKUP_FILE="tmp/test_fixer_start_${TIMESTAMP}.diff"
```

**This backup captures EVERYTHING:**
- All unstaged changes (`git diff HEAD`)
- All staged changes (`git diff --staged`)
- Nothing is lost, even if git operations fail

**If anything goes wrong later, you can recover with:**
```bash
# Find your backup
ls -lt tmp/test_fixer_start_*.diff | head -1

# Apply the backup
git apply tmp/test_fixer_start_TIMESTAMP.diff
```

### Phase 1: Systematic Investigation

**Step 1: Run tests and check for obvious fix**

```bash
# FIRST: Run the failing tests to see the error
just test-all-mocked  # Or whichever suite failed

# SECOND: Review the diff to understand what changed
git diff HEAD  # Shows all changes (staged + unstaged)

# THIRD: Analyze
# - What tests are failing?
# - What did I change in the diff?
# - Is it OBVIOUS what in the diff caused the failure?

# If OBVIOUS what broke (e.g., renamed function but forgot to update test):
#   → Fix it immediately and verify
#   → Skip to Phase 3 (cleanup)
#
# If NOT OBVIOUS:
#   → Continue to Step 2 (establish baseline)
```

**Step 2: Establish baseline (where do tests pass?)**

Only do this step if the fix wasn't obvious from Step 1.

```bash
# Save current state (in addition to diff backup)
git stash save "WIP: test-fixer investigating failures"

# Test at current point (without your changes)
just test-all-mocked  # Or whichever suite failed

# Record: PASS or FAIL?
```

**If tests PASS without your changes:**
- Root cause: Your changes broke the tests (most common case)
- Restore changes: `git stash pop`
- Proceed to Phase 2: Iterative Fixing

**If tests STILL FAIL without your changes:**
- Continue investigation to find where tests pass

```bash
# Check HEAD of current branch
git status  # Note branch name
# If at HEAD: git reset --hard origin/your-branch-name
# If behind HEAD: git reset --hard HEAD

just test-all-mocked

# Record: PASS or FAIL?
```

**If tests PASS at branch HEAD:**
- Root cause: Regression between HEAD and your current commit
- Proceed to Phase 2: Iterative Fixing

**If tests STILL FAIL at branch HEAD:**
- Check main branch

```bash
git checkout main
git pull origin main

just test-all-mocked

# Record: PASS or FAIL?
```

**If tests PASS at main:**
- Root cause: Regression between main and your branch
- Proceed to Phase 2: Iterative Fixing

**If tests FAIL at main:**
- Pre-existing issue (RARE - investigate why CI didn't catch)
- May need to check earlier commits or different branch

### Phase 2: Iterative Fixing

Once you've identified where tests pass, restore your code and start fixing:

```bash
# Return to original branch and restore changes
git checkout -  # or git checkout your-branch-name
git stash pop   # Restore your changes
```

**Now begin fix iteration loop:**

#### Fix Iteration Template

```bash
# ITERATION N
# 1. Analyze failure
just test-all-mocked  # Get fresh failure output
# Read error messages, identify specific test failures
# Identify root cause from stack traces

# 2. Write targeted fix
# - Edit specific file(s) causing failure
# - Make MINIMAL changes to fix identified issue
# - Document what you're fixing
# - 🚨 CRITICAL: If updating/fixing tests, ALWAYS use test-writer skill first
# - 💡 OPTIONAL: Use sql-reader skill to understand production data model if debugging integration/e2e tests

# 3. Verify fix
just lint-and-fix     # Auto-fix + type checking
just test-all-mocked  # Run tests

# 4. Evaluate result
# - If ALL tests PASS → SUCCESS, proceed to Phase 3
# - If SOME tests PASS (progress) → Continue iteration
# - If NO progress or NEW failures → Revert this fix attempt
```

**Revert failed fix attempt:**

```bash
# If fix didn't help or made things worse:
git diff  # Review what you changed
git checkout -- path/to/file.py  # Revert specific file
# OR
git stash  # Stash failed attempt
git stash drop  # Discard it

# Then try different approach in next iteration
```

**Iteration approach - Be DOGGED:**
- Try UP TO 10 different fix approaches
- Each approach should be DIFFERENT from previous attempts:
  1. Fix specific failing test (🚨 use test-writer skill)
  2. Fix underlying code causing failure
  3. Update test expectations (🚨 use test-writer skill - if contract legitimately changed)
  4. Fix imports/dependencies
  5. Revert specific file causing issues
  6. Check for missing files or configuration
  7. Fix type errors
  8. Update fixtures or test setup (🚨 use test-writer skill)
  9. Check for circular dependencies
  10. Simplify complex changes into smaller fixes

**🚨 CRITICAL RULE: When modifying test files, ALWAYS use test-writer skill**
- Before changing any test assertions, consult test-writer
- Before updating test fixtures, consult test-writer
- Before changing test expectations, consult test-writer
- test-writer ensures you don't create brittle or self-evident tests

**Be dogged and persistent (you KNOW tests can pass):**
- Remember: Tests passed at main → a solution EXISTS
- After 5 attempts: Take stock, try completely different angle
- After 10 attempts: Report to user with:
  - What you've tried (all 10 approaches)
  - What you've learned (patterns in failures)
  - Recommended next steps (specific, actionable)
- NEVER give up thinking "it can't be fixed" - it CAN because it passed before

### Phase 3: Final Verification & Cleanup

Once quick tests pass, verify ALL tests:

```bash
# 1. Quick verification first
just lint-and-fix     # Auto-fix + type checking
just test-all-mocked  # Quick tests must pass

# 2. Clean up any debugging artifacts
# - Remove print statements
# - Remove commented code
# - Remove temporary variables
# - Check git diff for unintended changes

# 3. Run FULL test suite (MANDATORY before saying "tests pass")
.claude/skills/test-runner/scripts/run_tests_parallel.sh

# 4. Check ALL logs for failures
grep -E "failed|ERROR|FAILED" api/tmp/test-logs/test-mocked_*.log
grep -E "failed|ERROR|FAILED" api/tmp/test-logs/test-e2e-live_*.log
grep -E "failed|ERROR|FAILED" api/tmp/test-logs/test-smoke_*.log

# 5. ONLY NOW can you say "all tests pass"
# - If ANY failures found → return to Phase 2, keep iterating
# - If ZERO failures → success, report to user
```

**🚨 DO NOT report success until Step 5 shows ZERO failures across ALL suites.**

## 📋 COMPLETE WORKFLOW EXAMPLE

```
Test Fixer Workflow - Iteration Log
===================================

Phase 1: Investigation
----------------------
✅ Tests PASS at: HEAD without my changes (stashed)
❌ Tests FAIL at: Current commit (my changes)

Identified 3 failing tests:
- test_get_message_requests::test_dual_audience
- test_get_message_requests::test_deprecated_format
- test_conversation_processor::test_voice_prompts

Root cause: Missing MESSAGE_ORDER handling in get_message_requests()

Phase 2: Iterative Fixing
--------------------------

Iteration 1:
- Fix: Add MESSAGE_ORDER dict detection in get_message_requests()
- Result: 2/3 tests pass ✅ (progress!)
- Remaining: test_voice_prompts still failing

Iteration 2:
- Fix: Update voice prompt handling to use new format
- Result: ALL TESTS PASS ✅

Phase 3: Final Verification
----------------------------
✅ just lint-and-fix - passed
✅ just test-all-mocked - all 464 tests passed

Cleanup:
- Removed debug print statements (2 files)
- Removed commented-out code (util.py:45-47)

SUCCESS: All tests passing, code restored to working state with minimal changes.

Changes made:
- api/src/message_processing/util.py: Added MESSAGE_ORDER handling (15 lines)
- api/src/message_processing/conversation_processors.py: Updated voice prompt format (2 lines)

Ready for commit.
```

## 🆘 EMERGENCY RECOVERY

**If anything goes wrong during test-fixer (checkout fails, stash lost, etc.):**

```bash
# 1. DON'T PANIC - your code is backed up!

# 2. Find your most recent backup
ls -lt tmp/test_fixer_start_*.diff | head -5

# 3. Check what's in the backup
git apply --check tmp/test_fixer_start_TIMESTAMP.diff

# 4. Apply the backup
git apply tmp/test_fixer_start_TIMESTAMP.diff

# 5. Verify your changes are restored
git status
git diff

# 6. If stash exists, recover it too
git stash list
git stash pop  # If you see your stash
```

**Recovery checklist:**
- ✅ Find backup: `ls -lt tmp/test_fixer_start_*.diff | head -1`
- ✅ Verify backup: `git apply --check tmp/test_fixer_start_TIMESTAMP.diff`
- ✅ Apply backup: `git apply tmp/test_fixer_start_TIMESTAMP.diff`
- ✅ Check stash: `git stash list && git stash pop`
- ✅ Confirm restoration: `git status && git diff`

**The git diff backup ensures you NEVER lose work, even if:**
- Stash gets lost
- Checkout conflicts occur
- Branch switching fails
- Anything unexpected happens

## 🚨 CRITICAL RULES

### 1. NEVER Delete User's Code

**ALWAYS use reversible operations:**
- ✅ `git stash` (can be popped)
- ✅ `git checkout -b temp-fix` (can switch back)
- ✅ Keep backup: `cp file.py file.py.backup`
- ❌ NEVER `git reset --hard` without stashing first
- ❌ NEVER `git clean -fd` on uncommitted changes
- ❌ NEVER delete files without backing up

### 2. Complete Investigation Before Reporting

**BANNED mid-investigation reports:**
- ❌ "I've stashed changes, running tests..."
- ❌ "Tests failing at HEAD, checking main..."
- ❌ "Found the issue, about to fix..."

**CORRECT workflow:**
- ✅ Announce: "Running systematic test fix workflow..."
- ✅ Silently complete: investigate → identify → fix → verify → cleanup
- ✅ THEN report: Complete findings with tests passing

### 3. Iterate Until Fixed (Be DOGGED - Don't Give Up)

**Fix iteration principles:**
- Try up to 10 different approaches (be creative!)
- Each iteration: analyze → fix → verify → evaluate
- If fix doesn't help: revert and try DIFFERENT approach
- Track what you've tried to avoid repeating failures
- After 5 attempts: step back, try completely different angle
- After 10 attempts: report comprehensive analysis to user
- **GOAL: Return working code** - don't stop until tests pass or all approaches exhausted

### 4. Minimal Changes Philosophy

**When fixing:**
- Change ONLY what's necessary to fix the test
- Don't refactor unrelated code
- Don't "improve" working code
- Focus on restoring passing state with minimal diff

### 5. Always Restore to Working State

**Before reporting to user:**
- ✅ All tests must pass (verify with `just test-all-mocked`)
- ✅ No stashed changes left behind
- ✅ Code on correct branch
- ✅ No debugging artifacts (prints, comments, TODOs)
- ✅ Clean git status

## 🎯 Success Criteria

**Your work is complete when:**

1. ✅ **All tests pass** (`just test-all-mocked` shows 0 failures)
2. ✅ **Linting passes** (`just lint-and-fix` clean)
3. ✅ **Code is clean** (no debug artifacts, commented code, or prints)
4. ✅ **Minimal changes** (git diff shows only necessary fixes)
5. ✅ **User's code preserved** (original intent and functionality intact)
6. ✅ **Complete report** (what broke, what was fixed, how to prevent)

## 🔍 Common Failure Patterns & Fixes

### Pattern 1: Import Errors After Refactoring
```
Error: ModuleNotFoundError: No module named 'old_module'

Investigation: Code was refactored, imports not updated
Fix: Update all import statements to new module path
Verify: Grep for old module name across codebase
```

### Pattern 2: Type Errors After API Changes
```
Error: Argument 1 has incompatible type "str"; expected "dict"

Investigation: Function signature changed
Fix: Update all call sites to use new signature
Verify: Check mypy errors, fix all occurrences
```

### Pattern 3: Test Assumptions Broken
```
Error: AssertionError: expected 3, got 2

Investigation: Business logic changed, test expects old behavior
Fix: Determine if test or code is wrong
  - If test is outdated: update test expectations (announce change)
  - If code is wrong: fix the code
Verify: Understand the contract being tested
```

### Pattern 4: Missing Dependencies
```
Error: AttributeError: 'NoneType' object has no attribute 'x'

Investigation: Function expects parameter that's now optional/missing
Fix: Add null checking or provide default value
Verify: Check all code paths that call this function
```

## 📊 Reporting Template

**When you complete the fix workflow, report:**

```
Test Fixer - Complete Report
=============================

Investigation Results:
✅ Tests PASS at: [main/branch HEAD/specific commit]
❌ Tests FAIL at: [your changes/branch HEAD/main]

Root Cause Identified:
[Clear explanation of what broke and why]

Fix Iterations: [N attempts]
Iteration 1: [what was tried] → [result]
Iteration 2: [what was tried] → [result]
...

Final Status:
✅ All tests passing (464/464)
✅ Linting clean
✅ Code restored to working state

Changes Made:
- file1.py: [description] (X lines changed)
- file2.py: [description] (Y lines changed)

Prevention:
[How to avoid this issue in the future]

Ready for: [next steps - commit/review/continue work]
```

## ⚡ When to Use This Skill

**MANDATORY when:**
- `just test-all-mocked` shows failures
- CI reports test failures
- User says "tests are broken" or "tests failing"
- After merging/pulling and tests fail
- After refactoring when tests break

**DO NOT use when:**
- Tests are passing (use test-runner instead)
- Writing new tests (use test-writer instead)
- Just want to run tests (use test-runner instead)

## 🚀 Quick Reference

```bash
# Investigation Phase
git stash save "WIP: test-fixer"
just test-all-mocked  # Where do tests pass?

# If tests pass here → your changes broke them
git stash pop
# Start fixing

# Fix Iteration Loop
while tests_failing:
    # 1. Analyze failure
    just test-all-mocked

    # 2. Write targeted fix
    # Edit specific files

    # 3. Verify
    just lint-and-fix && just test-all-mocked

    # 4. Evaluate
    if all_tests_pass:
        break
    elif some_progress:
        continue
    else:
        revert_this_attempt()

# Final Verification
just lint-and-fix
just test-all-mocked
# Report success
```

## 🎓 Remember

- **Investigation first** - Don't guess, systematically find where tests pass
- **Iterate to fix** - Don't stop after first attempt
- **Minimal changes** - Fix only what's broken
- **Always verify** - Run full test suite after each fix
- **Clean up** - Remove debug artifacts before reporting
- **Report complete** - User gets findings + working code, not work-in-progress

**Goal: User receives working, tested code with clear explanation of what was fixed.**
