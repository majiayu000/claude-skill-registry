---
name: milestone
description: Drive implementation forward incrementally with automatic progress tracking, LOC monitoring, and milestone checkpoint creation
---

# Milestone Skill

This skill instructs AI agents on how to drive implementation forward incrementally, tracking LOC count, running tests, and creating milestone checkpoints when the 800 LOC threshold is reached without completion.

## Skill Purpose

The milestone skill enables AI agents to implement large features step-by-step in manageable increments. It:

- **Implements incrementally**: Works in chunks of 100-200 LOC per iteration
- **Tracks progress**: Monitors total LOC count across the session
- **Runs tests continuously**: Executes tests after each implementation chunk
- **Creates checkpoints**: Generates milestone documents at 800 LOC threshold
- **Signals completion**: Returns success when all tests pass

This skill is the core implementation driver used by `/issue-to-impl` and `/miles2miles` commands.

## Philosophy

- **Incremental progress over big bang**: Small, testable chunks beat large rewrites
- **Test-driven validation**: Run tests frequently to catch issues early
- **Transparent checkpoints**: Milestone documents provide clear progress visibility
- **Fail-fast on errors**: Stop and create milestone when blocked rather than pushing forward blindly
- **LOC-based pacing**: Use lines of code (not time) to determine when to checkpoint

---

## Inputs

The milestone skill takes the following inputs (extracted from context):

1. **Current branch context**
   - Branch name (extracted from: `git branch --show-current`)
   - Must be a development branch matching pattern: `issue-{N}-{brief-title}`
   - Issue number extracted from branch name

2. **Plan reference**
   - **First invocation**: Read plan from GitHub issue using `gh issue view {N}`
   - **Resume invocation**: Read from latest milestone document in `.milestones/issue-{N}-milestone-*.md`
   - Plan contains: implementation steps, file changes, LOC estimates, test strategy

3. **Starting LOC count** (optional, for resume scenarios)
   - When resuming from a milestone, start from the LOC count in that milestone
   - When starting fresh (first milestone), start from 0

4. **Current test status** (determined by running tests)
   - Total test count
   - Passed test count
   - Failed test count (with failure details)

---

## LOC Tracking Mechanism

The AI agent **MUST** track LOC count accurately to determine when to create milestones.

### How to Track LOC

Use `git diff --stat` to measure code changes:

```bash
# Get stats for uncommitted changes
git diff --stat

# Example output:
#  claude/skills/milestone/SKILL.md | 156 ++++++++++++++++++++++++++++++++++++++
#  docs/milestone-workflow.md       | 187 ++++++++++++++++++++++++++++++++++++++++++
#  2 files changed, 343 insertions(+)
```

### LOC Calculation

Extract the total LOC count from the summary line:
- Pattern: `X files changed, Y insertions(+), Z deletions(-)`
- **Total LOC = Y (insertions) + Z (deletions)**
- Example: `343 insertions(+), 25 deletions(-)` → **Total LOC = 368**

### Accumulation Across Chunks

**CRITICAL**: Track cumulative LOC across multiple implementation chunks:

```python
# Pseudocode for LOC tracking
cumulative_loc = starting_loc  # From milestone or 0
while not all_tests_pass:
    implement_next_chunk()  # Implement 100-200 LOC
    current_chunk_loc = get_git_diff_stat()
    cumulative_loc += current_chunk_loc

    run_tests()
    test_status = parse_test_results()

    # Check stopping condition
    if cumulative_loc >= 800 and not all_tests_pass:
        create_milestone(cumulative_loc, test_status)
        stop_and_inform_user()
        break

    if all_tests_pass:
        signal_completion()
        break
```

### Stop Threshold

- **Stop when**: `cumulative_loc >= 800` AND tests are not all passing
- **Continue if**: `cumulative_loc < 800` OR all tests pass (nearing completion)
- **Exception**: If very close to completion (> 750 LOC and > 90% tests pass), continue to finish

---

## Implementation Loop

The AI agent **MUST** follow this implementation loop:

### 1. Read Plan or Milestone Context

**First invocation** (from issue):
```bash
gh issue view {issue-number} --json body --jq '.body'
```
- Extract "Proposed Solution" section (contains the plan)
- Identify implementation steps from the plan
- Note files to modify/create with LOC estimates

**Resume invocation** (from milestone):
```bash
# Find latest milestone
ls -1 .milestones/issue-{N}-milestone-*.md | sort -V | tail -n 1
```
- Read the latest milestone file
- Extract "Work Remaining" section
- Extract "Next File Changes" section
- Extract "Test Status" to understand current state

### 2. Determine Next Work

From the plan or milestone:
- Identify the next incomplete implementation step
- Determine which files need changes
- Understand what to implement in the next chunk

**Chunk size guideline**: Aim for 100-200 LOC per chunk
- If a step is > 200 LOC, break it into substeps
- Implement one substep per iteration

### 3. Implement the Chunk

Implement the next logical piece of functionality:

```
Agent: Implementing [description of what's being implemented]

[Uses Edit/Write tools to modify code]

Agent: Changes made:
- path/to/file1.py: Added feature X logic (~120 LOC)
- path/to/file2.py: Updated helper functions (~45 LOC)
```

**Best practices:**
- Focus on one logical unit per chunk
- Write clean, readable code
- Follow existing code patterns and conventions
- Add comments where logic is not self-evident

### 4. Check LOC Count

After implementing the chunk:

```bash
git diff --stat
```

Parse the output and add to cumulative count:
```
Agent: Chunk complete: ~165 LOC added
Agent: Cumulative LOC: 615 (starting from 450)
```

### 5. Run Tests

Execute the test suite after each chunk:

```bash
# If project has Makefile with test target
make test

# Or run specific test files mentioned in the plan
bash tests/test-feature.sh

# Or run all tests
bash tests/test-all.sh
```

**Capture test output** for parsing:
```
Agent: Running tests...
[test output]
Agent: Test results: 5/8 tests passed
```

### 6. Parse Test Results

Extract test status from output:

**Passed tests** (look for success markers):
- `✓` symbol
- "passed" keyword
- "OK" status
- Exit code 0 for individual tests

**Failed tests** (look for failure markers):
- `✗` symbol
- "failed" keyword
- "ERROR" or "FAILED" status
- Exit code non-zero

**Example parsing:**
```
Test output:
  ✓ Test 1: Feature initialization
  ✓ Test 2: Config loading
  ✗ Test 3: Edge case handling
  ✓ Test 4: Error recovery
  ✗ Test 5: Integration test
  ✓ Test 6: Cleanup

Parsed status:
  Passed: Tests 1, 2, 4, 6 (4 tests)
  Failed: Tests 3, 5 (2 tests)
  Total: 6 tests
  Percentage: 67% (4/6)
```

### 7. Check Stopping Conditions

After running tests, evaluate:

**Condition A: All tests pass**
```
if test_pass_percentage == 100%:
    signal_completion()
    return SUCCESS
```
→ Implementation is complete, ready for PR

**Condition B: LOC threshold reached without completion**
```
if cumulative_loc >= 800 and test_pass_percentage < 100%:
    create_milestone()
    inform_user_to_run_miles2miles()
    return MILESTONE_CREATED
```
→ Checkpoint needed, stop for user intervention

**Condition C: Continue implementation**
```
if cumulative_loc < 800 and test_pass_percentage < 100%:
    continue_loop()  # Go back to step 2
```
→ Keep implementing next chunk

**Condition D: Near completion exception**
```
if cumulative_loc >= 750 and cumulative_loc < 850 and test_pass_percentage >= 90%:
    continue_loop()  # Push to finish
```
→ Close enough to completion, don't create milestone

---

## Milestone Creation Logic

When the stop threshold is reached (Condition B), create a milestone document.

### Step 1: Determine Milestone Number

```bash
# Count existing milestones for this issue
ls -1 .milestones/issue-{N}-milestone-*.md 2>/dev/null | wc -l
```

Milestone number = count + 1

### Step 2: Extract Work Remaining

From the original plan (in issue), identify which steps are not yet complete:

**Original plan:**
```
Step 1: Update documentation (150 LOC) ✓ DONE
Step 2: Create tests (100 LOC) ✓ DONE
Step 3: Implement core logic (250 LOC) ← IN PROGRESS (partial)
Step 4: Add edge case handling (150 LOC) ← NOT STARTED
Step 5: Integration (100 LOC) ← NOT STARTED
```

**Work Remaining section:**
```markdown
## Work Remaining

- Step 3: Implement core logic (Estimated: ~100 LOC remaining)
  - File: src/core.py - Complete validation logic
  - File: src/utils.py - Add helper methods
- Step 4: Add edge case handling (Estimated: 150 LOC)
  - File: src/core.py - Handle edge cases
  - File: tests/test_edge_cases.sh - Verify edge case handling
- Step 5: Integration (Estimated: 100 LOC)
  - File: src/main.py - Integrate with existing system
```

### Step 3: Estimate Next File Changes

Based on current implementation state and remaining work:

```markdown
## Next File Changes (Estimated LOC for Next Milestone)

- `src/core.py`: Complete validation logic and add edge case handling (~180 LOC)
- `src/utils.py`: Add helper methods for validation (~45 LOC)
- `tests/test_edge_cases.sh`: Verify edge case handling (~60 LOC)

**Total estimated for next milestone:** ~285 LOC
```

### Step 4: Document Test Status

List all tests with their current status:

```markdown
## Test Status

**Passed Tests:**
- test-agentize-modes.sh: All 6 tests passed
- test-c-sdk.sh: All tests passed
- test-feature.sh: 4/6 tests passed
  - Test 1: Feature initialization
  - Test 2: Config loading
  - Test 4: Error recovery
  - Test 6: Cleanup

**Not Passed Tests:**
- test-feature.sh: 2/6 tests failing
  - Test 3: Edge case handling (FAILED)
    - Error: Validation logic incomplete
  - Test 5: Integration test (FAILED)
    - Error: Integration code not yet implemented
```

### Step 5: Write Milestone Document

Create the file `.milestones/issue-{N}-milestone-{M}.md`:

```markdown
# Milestone {M} for Issue #{N}

**Branch:** issue-{N}-{brief-title}
**Created:** {current-datetime}
**LOC Implemented:** ~{cumulative_loc} lines
**Test Status:** {passed}/{total} tests passed

[Work Remaining section from Step 2]

[Next File Changes section from Step 3]

[Test Status section from Step 4]
```

**IMPORTANT**: This milestone document is for local checkpoint tracking only. It should NOT be committed to git (it's already excluded via `.gitignore`).

### Step 6: Create Milestone Commit

Use the `commit-msg` skill with milestone flag:

**CRITICAL**: Only commit implementation changes (code, tests, docs), NOT the milestone report file.

**Invoke commit-msg skill with:**
- Purpose: milestone
- Staged files: all implementation changes (code, tests, documentation)
  - EXCLUDE: `.milestones/issue-{N}-milestone-{M}.md` (keep this local only)
- Issue number: {N}
- Test status: "{passed}/{total} tests passed"

The commit-msg skill will:
- Create commit message with `[milestone][tag]` prefix
- Include test status in message
- Use `git commit --no-verify` to bypass pre-commit hooks
- Reference the issue number

**Example commit message:**
```
[milestone][agent.skill]: Milestone 2 for issue #42

claude/skills/milestone/SKILL.md: Implement LOC tracking and test parsing logic
docs/milestone-workflow.md: Add workflow documentation

Milestone progress: 820 LOC implemented, 5/8 tests passed.
Tests failing: edge case handling, integration tests.

NOTE: Milestone document (.milestones/issue-42-milestone-2.md) is NOT committed - it remains local for resumption.
```

### Step 7: Inform User

Display message to user:

```
Milestone {M} created at {cumulative_loc} LOC ({passed}/{total} tests passed).

Next steps:
1. Start a new session
2. Run /miles2miles to resume implementation from this checkpoint

Work remaining: ~{estimated_remaining_loc} LOC
```

---

## Completion Signal

When all tests pass (Condition A), signal completion:

```
All tests passed ({total}/{total})!

Implementation complete:
- Total LOC: ~{cumulative_loc}
- All {total} tests passing
- Ready for PR creation

Next steps:
1. Review the changes
2. Use /open-pr to create a pull request
```

**Do NOT create a milestone** when all tests pass - this indicates completion.

The final commit should be a **delivery commit** (not a milestone):
- Use commit-msg skill with purpose: delivery
- No `--no-verify` flag
- Normal pre-commit hooks will run
- All tests must pass for commit to succeed

---

## Error Handling

### Not on Development Branch

```bash
git branch --show-current
```

If branch does not match pattern `issue-{N}-*`:

```
Error: Not on a development branch.

Current branch: {branch-name}

You must be on a development branch (issue-{N}-{brief-title}) to use the milestone skill.

Please run /issue-to-impl to start implementation on a proper development branch.
```

Stop execution.

### No Plan Found

If unable to find plan in issue or milestone:

```
Error: No implementation plan found.

Checked:
- GitHub issue #{N}: No "Proposed Solution" section
- Milestone files: No .milestones/issue-{N}-milestone-*.md found

Please ensure:
1. The issue has a plan created with /make-a-plan
2. You're running /issue-to-impl to start implementation

Cannot proceed without a plan.
```

Stop execution.

### Tests Fail Critically (Syntax Errors)

If tests fail to run due to syntax errors or import errors:

```bash
# Test output indicates syntax error
make test
# Output: SyntaxError: invalid syntax...
```

Create milestone with error notes:

```markdown
## Test Status

**Critical Errors:**
- Syntax error in src/core.py:45
- Import error: module 'utils' not found

**Test Execution:** Failed to run tests due to critical errors.

**Next Steps:**
1. Fix syntax errors
2. Resolve import issues
3. Resume with /miles2miles
```

Then stop and inform user:

```
Critical errors detected. Milestone {M} created with error notes.

Errors:
- Syntax error in src/core.py:45
- Import error: module 'utils' not found

Please fix these errors and run /miles2miles to resume.
```

### Milestone File Creation Fails

If unable to create milestone file:

```
Error: Failed to create milestone file at .milestones/issue-{N}-milestone-{M}.md

Possible causes:
- .milestones/ directory does not exist
- Permission issues

Please ensure .milestones/ directory exists and is writable.
```

Try to create the directory:
```bash
mkdir -p .milestones
```

Then retry creating the milestone file.

If still fails, stop and report error to user.

---

## Examples

### Example 1: First Milestone (Fresh Start)

**Context:** User runs `/issue-to-impl 42` for a feature with 8 test cases.

**Agent behavior:**

```
Agent: Starting implementation for issue #42...
Agent: Reading plan from issue...
Agent: Plan loaded: 5 implementation steps, estimated 950 LOC total

Agent: Step 1 complete: Documentation updated
Agent: Step 2 complete: Test cases created (8 tests)
Agent: Creating Milestone 1...
Agent: Milestone 1 created (0/8 tests passed)

Agent: Starting implementation loop...
Agent: Implementing Step 3: Core logic...
  [implements chunk 1: ~180 LOC]
Agent: Cumulative LOC: 180
Agent: Running tests... 2/8 tests passed
Agent: Implementing Step 3: Validation logic...
  [implements chunk 2: ~150 LOC]
Agent: Cumulative LOC: 330
Agent: Running tests... 3/8 tests passed
Agent: Implementing Step 4: Edge cases...
  [implements chunk 3: ~200 LOC]
Agent: Cumulative LOC: 530
Agent: Running tests... 5/8 tests passed
Agent: Implementing Step 4: Error handling...
  [implements chunk 4: ~180 LOC]
Agent: Cumulative LOC: 710
Agent: Running tests... 6/8 tests passed
Agent: Implementing Step 5: Integration...
  [implements chunk 5: ~140 LOC]
Agent: Cumulative LOC: 850
Agent: Running tests... 6/8 tests passed
Agent: LOC threshold reached (850 >= 800), creating Milestone 2...

Milestone 2 created at 850 LOC (6/8 tests passed).

Work remaining: ~100 LOC (Step 5 partial completion)
Tests failing: Integration test, Performance test

Next steps:
1. Start a new session
2. Run /miles2miles to resume from Milestone 2
```

### Example 2: Resume from Milestone

**Context:** User runs `/miles2miles` after Milestone 2 was created.

**Agent behavior:**

```
Agent: Finding latest milestone for current branch...
Agent: Found: .milestones/issue-42-milestone-2.md
Agent: Loading context...

Resuming from Milestone 2 for Issue #42:
- LOC implemented: 850
- Test status: 6/8 tests passed
- Work remaining: ~100 LOC

Agent: Reading work remaining from milestone...
Agent: Next work: Complete Step 5 integration

Agent: Implementing integration logic...
  [implements chunk: ~85 LOC]
Agent: Cumulative LOC: 935 (850 + 85)
Agent: Running tests... 7/8 tests passed
Agent: Implementing performance optimization...
  [implements chunk: ~45 LOC]
Agent: Cumulative LOC: 980 (935 + 45)
Agent: Running tests... 8/8 tests passed!

All tests passed (8/8)!

Implementation complete:
- Total LOC: ~980
- All 8 tests passing
- Ready for PR creation

Next steps:
1. Review the changes
2. Use /open-pr to create a pull request
```

### Example 3: Near Completion Exception

**Context:** At 780 LOC with 7/8 tests passing (87.5%).

**Agent behavior:**

```
Agent: Cumulative LOC: 780
Agent: Running tests... 7/8 tests passed (87.5%)

Agent: Near completion detected:
- LOC: 780 (close to threshold)
- Tests: 87.5% passing
- Estimated remaining: ~50 LOC

Agent: Continuing to push for completion instead of creating milestone...

Agent: Implementing final test fix...
  [implements chunk: ~35 LOC]
Agent: Cumulative LOC: 815
Agent: Running tests... 8/8 tests passed!

All tests passed (8/8)!

Implementation complete:
- Total LOC: ~815
- All 8 tests passing
- Ready for PR creation
```

**Note:** Even though cumulative LOC exceeded 800, the agent continued because:
- Started at 780 (close to threshold)
- Test pass percentage was high (87.5%)
- Estimated remaining work was minimal (~50 LOC)
- Better to complete than create another milestone for trivial remaining work

---

## Integration with Other Skills

### With `commit-msg` Skill

The milestone skill invokes the `commit-msg` skill for:

**Milestone commits:**
- Purpose: milestone
- Test status: included in commit message
- Uses `--no-verify` to bypass pre-commit hooks

**Delivery commits:**
- Purpose: delivery (when all tests pass)
- No test status needed (all tests pass)
- Normal pre-commit hooks run

### With `fork-dev-branch` Skill

The `/issue-to-impl` command uses `fork-dev-branch` to create the development branch before invoking the milestone skill.

### With `open-pr` Skill

After milestone skill signals completion, user can invoke `/open-pr` to create a pull request.

---

## Important Notes

1. **Always run tests**: Tests must be run after each chunk to track progress accurately

2. **LOC is cumulative**: Track total LOC across all chunks, not just the current chunk

3. **Milestone commits are temporary**: They allow bypassing hooks but should never be merged to main with incomplete tests

4. **Chunk size matters**: Keep chunks at 100-200 LOC for manageable progress and frequent test validation

5. **Parse test output carefully**: Accurate test status tracking is critical for milestone documents and decision-making

6. **Handle errors gracefully**: If tests fail critically, create milestone with error notes rather than continuing blindly

7. **Near-completion judgment**: Use discretion when close to 800 LOC with high test passage - sometimes better to finish than checkpoint

8. **Milestone documents are immutable**: Once created, milestone documents are snapshots in time - never edit them, only create new ones

9. **Trust the process**: The 800 LOC threshold is a guideline based on context window limits and maintainability - don't try to game it

10. **Test status is gold**: Milestone documents exist primarily to track test progress toward completion

11. **Milestone documents are local-only**: Milestone files in `.milestones/` are excluded from git (via `.gitignore`) and should NEVER be committed. They exist only as local checkpoints for resuming work.
