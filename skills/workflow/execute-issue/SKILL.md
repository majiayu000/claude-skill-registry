---
name: execute-issue
description: Execute a single sub-task with context priming. Supports both Linear and Jira backends via progressive disclosure. Use when ready to implement a refined issue, when the user mentions "execute", "implement", or "work on" an issue.
invocation: /execute
---

<objective>
Execute EXACTLY ONE sub-task from a refined issue, then STOP. This skill is designed to run in a loop where each invocation completes one sub-task.

Key behavior:
- Find ONE ready sub-task (no unresolved blockers)
- Implement it completely
- Verify with tests/typecheck/lint
- Commit and push
- Update issue status
- Report completion and STOP IMMEDIATELY

**CRITICAL**: After completing one sub-task (or determining none are ready), you MUST stop and end your response. Do NOT continue to the next sub-task. The calling loop will invoke you again for the next sub-task.
</objective>

<one_subtask_rule>
**THIS SKILL EXECUTES EXACTLY ONE SUB-TASK PER INVOCATION**

The workflow for each invocation:
1. Find the next ready sub-task
2. If none ready -> output STATUS and STOP
3. If found -> implement, verify, commit, push
4. Update issue status
5. Output completion STATUS and STOP

**NEVER**:
- Process multiple sub-tasks in one invocation
- Ask "should I continue to the next task?"
- Loop through remaining sub-tasks
- Suggest running the skill again

The loop script handles iteration. This skill handles ONE task.
</one_subtask_rule>

<backend_detection>
**FIRST**: Detect the backend from mobius config before proceeding.

Read `~/.config/mobius/config.yaml` or `mobius.config.yaml` in the project root:

```yaml
backend: linear  # or 'jira'
```

**Default**: If no backend is specified, default to `linear`.

The detected backend determines which MCP tools to use throughout this skill. All subsequent tool references use the backend-specific tools from the `<backend_context>` section below.
</backend_detection>

<backend_context>
<linear>
**MCP Tools for Linear**:

- **Fetch issue**: `mcp__plugin_linear_linear__get_issue`
  - Parameters: `id` (issue ID), `includeRelations` (boolean)
  - Returns: Issue with status, description, blockedBy relations

- **List sub-tasks**: `mcp__plugin_linear_linear__list_issues`
  - Parameters: `parentId`, `includeArchived`
  - Returns: Array of child issues

- **Update status**: `mcp__plugin_linear_linear__update_issue`
  - Parameters: `id`, `state` (e.g., "In Progress", "Done")
  - Transitions: Backlog -> In Progress -> Done

- **Add comment**: `mcp__plugin_linear_linear__create_comment`
  - Parameters: `issueId`, `body` (markdown)
  - Use for: Work started, completion notes, progress updates
</linear>

<jira>
**MCP Tools for Jira**:

- **Fetch issue**: `mcp_plugin_atlassian_jira__get_issue`
  - Parameters: `issueIdOrKey` (e.g., "PROJ-123")
  - Returns: Issue with status, description, links (blocking relationships)

- **List sub-tasks**: `mcp_plugin_atlassian_jira__list_issues`
  - Parameters: `jql` (e.g., "parent = PROJ-123")
  - Returns: Array of child issues

- **Update status**: `mcp_plugin_atlassian_jira__transition_issue`
  - Parameters: `issueIdOrKey`, `transitionId` or `transitionName`
  - Transitions: To Do -> In Progress -> Done

- **Add comment**: `mcp_plugin_atlassian_jira__add_comment`
  - Parameters: `issueIdOrKey`, `body` (markdown or Jira wiki markup)
  - Use for: Work started, completion notes, progress updates
</jira>
</backend_context>

<context>
This skill is the execution phase of the issue workflow:

1. **define-issue** - Creates well-defined issues with acceptance criteria
2. **refine-issue** - Breaks issues into single-file-focused sub-tasks with dependencies
3. **execute-issue** (this skill) - Implements ONE sub-task, then stops

**Loop-Based Execution Model**:
This skill is designed to be called repeatedly by a loop script (e.g., `mobius loop`). Each invocation:
1. Finds the NEXT ready sub-task
2. Executes it completely
3. Reports completion
4. STOPS (does not continue to next sub-task)

The loop script will call this skill again for the next sub-task. This ensures:
- Fresh context for each sub-task
- Clear boundaries between tasks
- Predictable execution behavior
- Easy progress monitoring

Each sub-task is designed to:
- Target a single file (or source + test pair)
- Fit within one context window
- Have clear acceptance criteria
- Have explicit blocking relationships
</context>

<checkpoint_system>
**Checkpoint system enables recovery from interruptions** by saving structured state after each major phase.

Checkpoints are only used for **non-trivial tasks** (estimated >5 minutes or involving multiple verification cycles). Skip checkpoints for simple single-file changes.

<checkpoint_definitions>
### Checkpoint 1: Context Priming Complete
**Phase**: After loading parent issue, finding ready subtask, and loading dependency context
**Marker**: `CHECKPOINT:PRIMED`
**Saves**:
- Parent issue ID and title
- Selected subtask ID and title
- Target file path
- Completed dependency summaries (not full content)
- Key patterns identified for implementation
**Recovery**: Skip context loading, proceed directly to implementation

### Checkpoint 2: Implementation Complete
**Phase**: After implementing changes but before verification
**Marker**: `CHECKPOINT:IMPLEMENTED`
**Saves**:
- List of modified files
- Summary of changes made (not full diffs)
- Staged files ready for verification
- Implementation approach taken
**Recovery**: Skip implementation, proceed to verification

### Checkpoint 3: Verification Complete
**Phase**: After all verification passes, ready to commit
**Marker**: `CHECKPOINT:VERIFIED`
**Saves**:
- Verification results (typecheck, tests, lint)
- Files ready to commit
- Draft commit message
**Recovery**: Skip verification, proceed directly to commit
</checkpoint_definitions>

<checkpoint_thresholds>
**When to create checkpoints**:
- Task description > 5 sentences
- Multiple acceptance criteria (>3)
- Target file > 200 lines
- Previous attempt was interrupted (detected via existing checkpoint)

**When to skip checkpoints**:
- Simple single-criterion tasks
- Small file changes (<50 lines)
- Tasks marked as "quick fix" or "trivial"
</checkpoint_thresholds>

<save_checkpoint>
**Add checkpoint comment to issue** after completing each phase.

Use the backend-appropriate comment tool:
- **Linear**: `mcp__plugin_linear_linear__create_comment`
- **Jira**: `mcp_plugin_atlassian_jira__add_comment`

**Checkpoint comment format** (structured for parsing):

```markdown
## Checkpoint: {CHECKPOINT_MARKER}

**Timestamp**: {ISO-8601 timestamp}
**Agent**: {agent-id or session-id if available}

### State Summary
{phase-specific state data as key-value pairs}

### Files Involved
- `{file1}` - {status: read/modified/staged}
- `{file2}` - {status: read/modified/staged}

### Next Phase
{description of what the next phase should do}

---
CHECKPOINT:{MARKER}:{subtask-id}:{timestamp}
```

**Example checkpoint comments**:

```markdown
## Checkpoint: PRIMED

**Timestamp**: 2024-01-15T14:30:00Z
**Agent**: execute-loop-1

### State Summary
- parent_id: PROJ-100
- subtask_id: PROJ-125
- target_file: src/contexts/ThemeContext.tsx
- change_type: Create
- dependencies_loaded: PROJ-124

### Files Involved
- `src/types/theme.ts` - read (from dependency)

### Next Phase
Implement ThemeContext provider with light/dark/system modes

---
CHECKPOINT:PRIMED:PROJ-125:2024-01-15T14:30:00Z
```

**Important**:
- Append new checkpoints; never delete previous ones (audit trail)
- Include machine-parseable marker line at the end
- Keep state summaries concise - metadata only, not full content
</save_checkpoint>

<resume_from_checkpoint>
**Detect and resume from interrupted work** at the start of execution.

**Detection steps**:
1. After loading the subtask, list recent comments
2. Search for comments containing `CHECKPOINT:` marker
3. Parse the most recent checkpoint marker line

**Checkpoint marker format**:
```
CHECKPOINT:{MARKER}:{subtask-id}:{timestamp}
```

**Resume logic by marker**:

| Marker | Resume Action |
|--------|---------------|
| `PRIMED` | Skip context loading, read state summary, proceed to implementation |
| `IMPLEMENTED` | Skip implementation, verify files from state, proceed to verification |
| `VERIFIED` | Skip verification, use saved commit message, proceed to commit |

**Resume validation**:
Before resuming, validate the checkpoint is still valid:
1. Check that mentioned files still exist
2. Verify git status matches expected state (staged files, no unexpected changes)
3. If validation fails, discard checkpoint and start fresh

**Resume comment** (add when resuming):
```markdown
## Resuming from Checkpoint

**Previous checkpoint**: {MARKER} at {timestamp}
**Validation**: PASSED
**Skipping phases**: {list of skipped phases}

Continuing from {phase name}...
```

**When NOT to resume**:
- Checkpoint is >24 hours old
- Files mentioned in checkpoint were modified outside this workflow
- Subtask description has changed since checkpoint
- User explicitly requests fresh start
</resume_from_checkpoint>
</checkpoint_system>

<quick_start>
<invocation>
Pass an issue ID (either parent or subtask):

```
/execute PROJ-123    # Parent issue - finds next ready subtask
/execute PROJ-124    # Subtask - executes this specific task
```

When running in parallel mode, each agent receives a specific subtask ID to prevent race conditions.
</invocation>

<workflow>
1. **Detect backend** - Read backend from config (linear or jira)
2. **Detect issue type** - Check if passed ID is a subtask (has parent) or parent issue
3. **Load parent issue** - Get high-level context and acceptance criteria
4. **Find ready sub-task** - If parent was passed, find first ready subtask (skip if subtask was passed)
5. **Mark In Progress** - Move sub-task to "In Progress" immediately before starting work
6. **Prime context** - Load completed dependent tasks for implementation context
7. **Implement changes** - Execute the single-file-focused work
8. **Verify standard** - Run tests, typecheck, and lint
9. **Fix if needed** - Attempt automatic fixes on verification failures
10. **Verify sub-task** - Execute `### Verify` command from sub-task if present (with safety checks)
11. **Commit and push** - Create commit with conventional message, push
12. **Update status** - Move sub-task to "Done" if all criteria met
13. **Report completion** - Show what was done and what's next
</workflow>
</quick_start>

<context_priming_phase>
<detect_issue_type>
**FIRST**: Determine if the passed issue ID is a subtask or a parent issue.

Use the backend-appropriate fetch tool:
- **Linear**: `mcp__plugin_linear_linear__get_issue` with `includeRelations: true`
- **Jira**: `mcp_plugin_atlassian_jira__get_issue`

**Check the `parent` field in the response**:

1. **If `parent` field EXISTS** -> This is a **SUBTASK**
   - The passed ID is the specific subtask to execute (e.g., "PROJ-124")
   - Skip the "find ready subtask" phase entirely
   - Use this subtask directly for implementation
   - Load the parent issue for context (the `parent.id` from response)

2. **If `parent` field is NULL/MISSING** -> This is a **PARENT ISSUE**
   - The passed ID is the parent (e.g., "PROJ-123")
   - Continue with the "find ready subtask" flow below
   - This is the fallback for backward compatibility

**Why this matters**: When running in parallel mode (`mobius loop PROJ-123 --parallel=3`), each agent receives a specific subtask ID to prevent race conditions. The orchestrator assigns tasks upfront, so each agent should execute exactly the task it was given.
</detect_issue_type>

<load_parent_issue>
If the issue is a subtask, fetch its parent for high-level context.
If the issue is a parent, this is the issue itself.

Use the backend-appropriate fetch tool to get:
- **Goal**: What the overall feature/fix achieves
- **Acceptance criteria**: High-level success conditions
- **Context**: Any technical notes or constraints
- **Related issues**: For broader understanding
</load_parent_issue>

<find_ready_subtask>
**Skip this section if executing a specific subtask (issue had `parent` field).**

If a parent issue was passed, list all sub-tasks:
- **Linear**: `mcp__plugin_linear_linear__list_issues` with `parentId`
- **Jira**: `mcp_plugin_atlassian_jira__list_issues` with JQL `parent = {issue-key}`

For each sub-task, check:
1. State is not "Done" or "Canceled"
2. All blocking issues are in "Done" state

Select the FIRST sub-task where all blockers are resolved.

**STOP CONDITIONS** (report and end immediately):

1. **All sub-tasks are Done**:
   ```
   STATUS: ALL_COMPLETE
   All N sub-tasks of {parent-id} are complete.
   Parent issue is ready for review.
   ```

2. **All remaining sub-tasks are blocked**:
   ```
   STATUS: ALL_BLOCKED
   N sub-tasks remain, but all are blocked.
   Waiting on: {list of blocking issues}
   ```

3. **No sub-tasks exist**:
   ```
   STATUS: NO_SUBTASKS
   Issue {parent-id} has no sub-tasks.
   Consider running /refine first.
   ```

If any stop condition is met, output the status message and STOP. Do not continue.
</find_ready_subtask>

<mark_in_progress>
**IMMEDIATELY** after selecting a sub-task to work on, move it to "In Progress":

- **Linear**: `mcp__plugin_linear_linear__update_issue` with `state: "In Progress"`
- **Jira**: `mcp_plugin_atlassian_jira__transition_issue` to "In Progress"

Add a comment indicating work has started using the backend-appropriate comment tool.

**Why this matters**: Moving to "In Progress" immediately ensures:
- Other agents (in parallel mode) won't pick up the same task
- The TUI/dashboard shows accurate real-time status
- If the agent crashes or times out, the task remains "In Progress" for the next loop
</mark_in_progress>

<load_dependency_context>
For each completed blocker of the selected sub-task, fetch the issue details.

Extract from each completed dependency:
- **What was implemented**: Summary of changes
- **Files modified**: To understand current state
- **Patterns used**: To maintain consistency
- **Any notes**: Implementation decisions or gotchas

Compile into a context brief for the current task.
</load_dependency_context>

<context_brief_format>
Build context brief for implementation:

```markdown
# Execution Context

## Parent Issue: {ID} - {Title}
{Parent description and acceptance criteria}

## Current Sub-task: {ID} - {Title}
**Target file**: {file path}
**Change type**: {Create/Modify}
{Sub-task description and acceptance criteria}

## Completed Dependencies
### {Dep-1 ID}: {Title}
- Modified: {files}
- Summary: {what was done}

### {Dep-2 ID}: {Title}
- Modified: {files}
- Summary: {what was done}

## Implementation Notes
- Follow patterns from: {relevant completed tasks}
- Key imports needed: {based on dependency analysis}
- Test file: {expected test location}
```
</context_brief_format>
</context_priming_phase>

<implementation_phase>
<read_target_file>
Before making changes, read the target file(s):

- If **Create**: Check directory exists, understand sibling file patterns
- If **Modify**: Read current file content completely

Also read:
- Related type definitions (from completed dependencies)
- Test file if it exists
- Any files imported by the target
</read_target_file>

<implement_changes>
Execute the implementation following:

1. **Match existing patterns** - Use same style as similar files
2. **Single file focus** - Only modify the target file(s) specified
3. **Meet acceptance criteria** - Each criterion should be addressed
4. **Add/update tests** - If target is source file, update corresponding test

Use Edit tool for modifications, Write tool for new files.

**Implementation checklist**:
- [ ] All acceptance criteria addressed
- [ ] Follows existing code patterns
- [ ] Proper imports added
- [ ] Types are correct
- [ ] Test coverage for new code
</implement_changes>

<scope_discipline>
**Stay within scope**:
- Only modify files specified in the sub-task
- Don't refactor unrelated code
- Don't add features not in acceptance criteria
- Don't fix unrelated issues discovered during work

If you discover issues outside scope:
- Note them for later
- Don't fix them now
- Can mention in completion report
</scope_discipline>
</implementation_phase>

<tdd_option>
**Test-Driven Development workflow is optional** and should be used when explicitly requested or when sub-tasks have highly testable acceptance criteria.

<when_to_use>
**Use TDD when ANY of these apply**:

1. **Explicit directive**: Sub-task description contains "Use TDD" or "TDD workflow"
2. **Complex business logic**: Algorithm implementations, data transformations, validation rules
3. **Refactoring existing code**: When changing implementation while preserving behavior
4. **Bug fixes with reproducible steps**: Write test that reproduces bug first
5. **Well-defined input/output**: Functions with clear contracts and edge cases

**Skip TDD when**:
- Simple configuration changes
- UI/layout modifications without logic
- Adding imports or wiring up existing components
- Documentation-only changes
- Sub-task explicitly says "Do NOT use TDD"

**Detection heuristic**: If sub-task has >3 specific, testable acceptance criteria (not just "implement X"), consider TDD.
</when_to_use>

<tdd_workflow>
When TDD is appropriate, follow the **red-green-refactor** cycle instead of the standard implementation flow:

### Red Phase: Write Failing Tests First

1. **Analyze acceptance criteria** - Convert each criterion to a test case
2. **Create/update test file** - Write tests that define expected behavior
3. **Run tests to confirm failure** - Tests MUST fail (proves tests are meaningful)
4. **Commit failing tests** (optional) - Some teams prefer this for traceability

```bash
# Example: Run tests to verify they fail
just test-file {test-file-pattern}
# Expected: Tests should FAIL at this point
```

**Red phase checklist**:
- [ ] Each acceptance criterion has a corresponding test
- [ ] Tests cover edge cases mentioned in sub-task
- [ ] Tests are isolated and independent
- [ ] Tests fail for the right reason (missing implementation, not syntax errors)

### Green Phase: Implement Minimal Code to Pass

1. **Focus on passing tests** - Write just enough code to make tests green
2. **Don't optimize prematurely** - Correctness first, elegance later
3. **Run tests after each change** - Verify progress incrementally
4. **All tests must pass** before proceeding

```bash
# Verify tests pass
just test-file {test-file-pattern}
# Expected: All tests should PASS
```

**Green phase checklist**:
- [ ] All previously failing tests now pass
- [ ] No new test failures introduced
- [ ] Implementation addresses acceptance criteria
- [ ] Code compiles without type errors

### Refactor Phase: Improve Code Quality

1. **Clean up implementation** - Remove duplication, improve naming
2. **Maintain passing tests** - Run tests after each refactor step
3. **Apply code patterns** - Match existing codebase conventions
4. **Don't add new behavior** - Only restructure existing code

```bash
# Verify tests still pass after refactoring
just test-file {test-file-pattern}
# Expected: All tests should still PASS
```

**Refactor phase checklist**:
- [ ] Code follows project patterns and conventions
- [ ] No code duplication
- [ ] Clear naming and structure
- [ ] All tests still pass
- [ ] Typecheck passes
</tdd_workflow>

<tdd_vs_standard_flow>
**When to use each approach**:

| Scenario | Approach | Why |
|----------|----------|-----|
| "Use TDD" in description | TDD | Explicit request |
| Algorithm implementation | TDD | Complex logic benefits from test-first |
| Bug fix with repro steps | TDD | Test captures the bug |
| UI component wiring | Standard | Tests come after implementation |
| Config/env changes | Standard | Not meaningfully testable |
| >3 testable criteria | Consider TDD | High specificity suggests test-first value |

**Switching mid-task**: If you start with standard flow and realize TDD would help, you can switch. Write tests for remaining criteria, verify they fail, then continue with green-refactor.
</tdd_vs_standard_flow>

<tdd_commit_strategy>
**Commit points in TDD workflow**:

Option A: Single commit at end (recommended for small sub-tasks)
- Complete full red-green-refactor cycle
- Single commit with all changes

Option B: Multiple commits (for larger sub-tasks)
- Commit 1: Failing tests (optional, documents intent)
- Commit 2: Passing implementation + refactored code

**Commit message for TDD**:
```
feat(scope): implement feature using TDD

Red: Added tests for {criteria}
Green: Implemented {functionality}
Refactor: {what was cleaned up}

Implements: {sub-task-id}
Part-of: {parent-issue-id}
```
</tdd_commit_strategy>

<tdd_anti_patterns>
**Avoid these TDD mistakes**:

- **Testing implementation details**: Test behavior, not internal structure
  - BAD: `expect(obj._privateMethod).toBeCalled()`
  - GOOD: `expect(result).toEqual(expectedOutput)`

- **Writing tests that can't fail**: Tests must be meaningful
  - BAD: `expect(true).toBe(true)`
  - GOOD: `expect(calculate(input)).toBe(expectedResult)`

- **Skipping the refactor phase**: Refactoring is essential for maintainability
  - BAD: Green tests → commit immediately
  - GOOD: Green tests → refactor → verify still green → commit

- **Over-testing**: Don't test framework behavior or trivial code
  - BAD: Testing that React renders a div
  - GOOD: Testing that component displays correct data

- **Forcing TDD on unsuitable tasks**: Not everything benefits from test-first
  - BAD: TDD for a CSS color change
  - GOOD: Standard flow for styling, TDD for logic
</tdd_anti_patterns>
</tdd_option>

<verification_phase>
<full_validation>
Run all three verification steps:

**1. Type checking**:
```bash
just typecheck
```

**2. Tests**:
```bash
just test-file {pattern matching target file}
```

Or if new functionality spans multiple test files:
```bash
just test
```

**3. Lint** (if available):
```bash
just lint
# or
bun run lint
```
</full_validation>

<handle_failures>
If any verification fails:

**Attempt automatic fix**:
1. Read the error output carefully
2. Identify the root cause
3. Apply targeted fix to resolve the issue
4. Re-run the failing verification
5. Repeat up to 3 times

**Common fixes**:
- Type errors: Add missing types, fix type mismatches
- Test failures: Update test expectations, fix logic errors
- Lint errors: Apply auto-fix if available, manual fix otherwise

**If fix attempts fail after 3 tries**:
- Stop execution immediately
- Do NOT ask user questions (this skill runs in an automated loop)
- Output failure status and terminate:

```markdown
STATUS: VERIFICATION_FAILED

## Sub-task Failed: {sub-task-id}

### Error Summary
{type of failure: typecheck/tests/lint}

### Last Error Output
```
{truncated error output, last 50 lines}
```

### Attempted Fixes
1. {fix attempt 1}
2. {fix attempt 2}
3. {fix attempt 3}

### Files Modified (uncommitted)
- {file1}
- {file2}

The loop will stop. Review the errors and either:
- Fix manually and run `/execute {parent-id}` again
- Or rollback with `git checkout -- .`
```

**CRITICAL**: After outputting this failure report, STOP. Do not continue trying.
</handle_failures>

<verification_success>
All checks must pass before proceeding:

```markdown
## Verification Results
- Typecheck: PASS
- Tests: PASS (X tests, Y assertions)
- Lint: PASS

Ready for sub-task verify command (if present).
```
</verification_success>

<subtask_verify_command>
**After standard verification passes**, check for and execute a `### Verify` command from the sub-task description.

<parse_verify_block>
Extract the verify command from the sub-task description:

1. Look for `### Verify` section in the sub-task description
2. Extract the bash code block immediately following the header
3. The command is the content between ` ```bash ` and ` ``` ` markers

**Example sub-task description**:
```markdown
### Verify

```bash
grep -q "export function" src/utils/helpers.ts && \
npm test -- --grep "helpers" && \
echo "PASS: Helper function verified"
```
```

**Extraction result**: The bash command to execute.
</parse_verify_block>

<verify_command_safety>
**CRITICAL**: Before executing any verify command, check for dangerous patterns.

**Block these patterns** (do NOT execute, report as unsafe):
- `rm -rf` or `rm -r` with wildcards or root paths
- `sudo` commands
- Commands writing to system paths (`/etc`, `/usr`, `/var`)
- `chmod 777` or overly permissive permission changes
- `curl | bash` or `wget | sh` piping to shell
- `dd if=` disk operations
- `mkfs` or filesystem formatting
- `:(){:|:&};:` or other fork bombs
- `> /dev/` device writes
- Commands containing `$()` or backticks with destructive operations

**Safety check implementation**:
```bash
# Patterns to block (regex)
DANGEROUS_PATTERNS=(
  "rm\s+(-[rf]+\s+)*(/|~|\*|\.\.|\\$)"
  "sudo\s+"
  "chmod\s+777"
  "curl.*\|\s*(ba)?sh"
  "wget.*\|\s*(ba)?sh"
  "dd\s+if="
  "mkfs"
  ">\s*/dev/"
  ":\(\)\s*\{.*\}.*;"
)
```

If a dangerous pattern is detected:
```markdown
## Verify Command Blocked

**Reason**: Command contains potentially dangerous pattern: `{pattern}`
**Command**: `{command}`

The verify command was not executed for safety reasons.
Proceeding to commit phase without sub-task verification.

**Note**: Review the verify command in the sub-task description.
```
</verify_command_safety>

<execute_verify_command>
If the verify command passes safety checks, execute it:

```bash
# Execute the extracted verify command
{extracted_verify_command}
```

**Timeout**: Verify commands have a 60-second timeout to prevent hanging.

**On success** (exit code 0):
```markdown
## Sub-task Verify Command
- Command: `{command_summary}`
- Result: PASS
- Output: {last few lines of output}

Verify command passed. Ready to commit.
```

**On failure** (non-zero exit code):
The verify command failure triggers an implementation review loop:

1. Read the error output to understand what failed
2. Review the implementation against the sub-task requirements
3. Attempt to fix the issue (similar to handling test failures)
4. Re-run the verify command
5. Repeat up to 3 times

If verify command still fails after 3 attempts:
```markdown
STATUS: VERIFICATION_FAILED

## Sub-task Failed: {sub-task-id}

### Error Summary
Sub-task verify command failed after 3 attempts

### Verify Command
```bash
{command}
```

### Last Error Output
```
{error output}
```

### Attempted Fixes
1. {fix attempt 1}
2. {fix attempt 2}
3. {fix attempt 3}

### Files Modified (uncommitted)
- {file1}
- {file2}

The loop will stop. Review the verify command and implementation.
```

**CRITICAL**: After outputting this failure report, STOP.
</execute_verify_command>

<verify_command_fallback>
**If no `### Verify` section exists** in the sub-task description:

- This is normal and expected for older sub-tasks
- Proceed directly to commit phase after standard verification passes
- Include note in completion report:

```markdown
## Verification Results
- Typecheck: PASS
- Tests: PASS
- Lint: PASS
- Sub-task verify: N/A (no verify block in sub-task)

Ready to commit.
```

**Fallback behavior ensures**:
- Backward compatibility with existing sub-tasks
- Standard tests/typecheck/lint still required
- No failure if verify block is missing
</verify_command_fallback>
</subtask_verify_command>
</verification_phase>

<commit_phase>
<commit_message>
Create conventional commit message:

Format:
```
{type}({scope}): {description}

{body with details}

Implements: {sub-task-id}
Part-of: {parent-issue-id}
```

**Type mapping**:
- New file created -> `feat`
- Bug fix -> `fix`
- Modification/enhancement -> `feat` or `refactor`
- Test only -> `test`
- Types only -> `types`

**Example**:
```
feat(theme): add ThemeContext provider

- Create ThemeProvider with light/dark/system modes
- Persist theme preference to localStorage
- Add useTheme hook for consuming context

Implements: PROJ-125
Part-of: PROJ-100
```
</commit_message>

<git_operations>
Execute git operations:

```bash
# Stage only the files we modified
git add {target-file} {test-file-if-applicable}

# Commit with conventional message
git commit -m "{commit message}"

# Push to current branch
git push
```

**Important**:
- Only stage files explicitly modified for this sub-task
- Don't use `git add -A` or `git add .`
- Verify staged files match expected scope before commit
</git_operations>

<commit_verification>
After push, verify:

```bash
git log -1 --oneline
git status
```

Confirm:
- Commit created successfully
- Push completed without errors
- Working directory is clean
</commit_verification>
</commit_phase>

<status_update_phase>
<update_subtask_status_done>
After successful commit with all acceptance criteria met, move sub-task to "Done":

- **Linear**: `mcp__plugin_linear_linear__update_issue` with `state: "Done"`
- **Jira**: `mcp_plugin_atlassian_jira__transition_issue` to "Done"

**Criteria for moving to "Done"**:
- All acceptance criteria from the sub-task are implemented
- All verification checks pass (typecheck, tests, lint)
- Changes are committed and pushed
- No outstanding work remains for this sub-task
</update_subtask_status_done>

<add_completion_comment>
Add comment documenting the implementation using the backend-appropriate comment tool:

```markdown
## Implementation Complete

**Commit**: {commit-hash}
**Files modified**:
- {file1}
- {file2}

**Changes**:
{brief summary of what was implemented}

**Verification**:
- Typecheck: PASS
- Tests: PASS
- Lint: PASS

**Acceptance Criteria**:
- [x] {criterion 1}
- [x] {criterion 2}
- [x] {criterion 3}
```
</add_completion_comment>

<partial_completion_handling>
If the agent must wrap up before completing all work (context limits, time constraints, or blocking issues discovered), keep the task "In Progress" and add a detailed progress comment:

```markdown
## Partial Progress - Continuing Next Loop

**Progress Made**:
- {what was accomplished}
- {files modified so far}

**Remaining Work**:
- {what still needs to be done}
- {specific acceptance criteria not yet met}

**Current State**:
- Committed: {yes/no - if yes, include commit hash}
- Verification: {status of typecheck/tests/lint}

**Blockers/Issues Discovered** (if any):
- {any issues that need attention}

**Next Steps**:
- {what the next loop iteration should focus on}
```

**CRITICAL**: Do NOT move to "Done" if:
- Some acceptance criteria are not yet implemented
- Tests are failing
- There are uncommitted changes that need more work
- The implementation is incomplete

Leave the task "In Progress" so the next loop iteration can continue the work.
</partial_completion_handling>
</status_update_phase>

<completion_report>
<report_format>
After successful execution, report and STOP:

```markdown
# Sub-task Completed

STATUS: SUBTASK_COMPLETE

## {Sub-task ID}: {Title}
**Status**: Moved to Done
**Commit**: {hash} on {branch}

### Files Modified
- `{file1}` - {change summary}
- `{file2}` - {change summary}

### Acceptance Criteria
- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

### Verification
- Typecheck: PASS
- Tests: PASS
- Lint: PASS
- Sub-task verify: {PASS/N/A}

---

## Progress
**Completed**: {X of Y sub-tasks}
**Ready next**: {list of now-unblocked sub-tasks, or "none" if all blocked/done}
**Still blocked**: {count of sub-tasks still waiting}

---
EXECUTION_COMPLETE: {sub-task-id}
```

**CRITICAL**: After outputting this report, STOP IMMEDIATELY. Do not:
- Start working on the next sub-task
- Ask if the user wants to continue
- Suggest what to do next
- Make any further tool calls

The loop script will invoke this skill again for the next sub-task.
</report_format>

<partial_completion_report>
If wrapping up with incomplete work, output this report instead:

```markdown
# Sub-task Partial Progress

STATUS: SUBTASK_PARTIAL

## {Sub-task ID}: {Title}
**Status**: In Progress (continuing next loop)
**Commit**: {hash if any, or "uncommitted changes"}

### Progress Made
- {what was accomplished}
- {files modified}

### Remaining Work
- [ ] {uncompleted criterion 1}
- [ ] {uncompleted criterion 2}

### Current State
- Typecheck: {PASS/FAIL/NOT_RUN}
- Tests: {PASS/FAIL/NOT_RUN}
- Lint: {PASS/FAIL/NOT_RUN}
- Sub-task verify: {PASS/FAIL/NOT_RUN/N/A}

### Why Stopping
{reason - e.g., "context limit reached", "blocking issue discovered", "time constraint"}

### Notes for Next Loop
{specific guidance for continuation}

---
EXECUTION_PARTIAL: {sub-task-id}
```

This status keeps the task "In Progress" for the next loop iteration to continue.
</partial_completion_report>

<discovered_issues>
If issues were discovered during implementation but not addressed:

```markdown
### Out-of-Scope Issues Discovered
- {Issue 1}: {brief description} in {file}
- {Issue 2}: {brief description} in {file}

Consider creating separate issues for these.
```
</discovered_issues>
</completion_report>

<examples>
<execution_example>
**Input**: `/execute PROJ-100`

**Flow**:

1. Detect backend from config (e.g., `linear`)
2. Load PROJ-100 (parent: "Add dark mode support")
3. Find sub-tasks:
   - PROJ-124: Define types (Done)
   - PROJ-125: Create ThemeProvider (blockedBy: PROJ-124) <- **Ready**
   - PROJ-126: Add useTheme hook (blockedBy: PROJ-125) - Blocked
   - PROJ-127: Update Header (blockedBy: PROJ-126) - Blocked

4. Select PROJ-125 (first ready task)

5. **Immediately mark PROJ-125 as "In Progress"** and add start comment

6. Load context from PROJ-124:
   - Created `src/types/theme.ts`
   - Exports: `Theme`, `ThemeMode`, `ThemeContextValue`

7. Implement PROJ-125:
   - Create `src/contexts/ThemeContext.tsx`
   - Import types from completed dependency
   - Follow existing context patterns in codebase

8. Verify:
   - `just typecheck` -> PASS
   - `just test-file ThemeContext` -> PASS
   - `just lint` -> PASS

9. Commit and push:
   ```
   feat(theme): create ThemeProvider context

   - Add ThemeProvider component with light/dark/system modes
   - Persist preference to localStorage
   - Detect system preference changes

   Implements: PROJ-125
   Part-of: PROJ-100
   ```

10. Update status:
    - PROJ-125 -> "Done" (all criteria met)
    - Add completion comment with commit hash and acceptance criteria

11. Report and STOP:
    ```
    STATUS: SUBTASK_COMPLETE

    ## PROJ-125: Create ThemeProvider
    **Status**: Moved to Done
    Completed: 2 of 4 sub-tasks
    Ready next: PROJ-126

    EXECUTION_COMPLETE: PROJ-125
    ```

12. **STOP** - Do not continue to PROJ-126. The loop will invoke again.
</execution_example>
</examples>

<anti_patterns>
**Don't continue to next sub-task** (MOST IMPORTANT):
- BAD: "Sub-task A complete. Now let me work on sub-task B..."
- BAD: "Should I continue to the next sub-task?"
- BAD: Processing multiple sub-tasks in one invocation
- GOOD: Complete ONE sub-task, output STATUS, STOP

**Don't skip context priming**:
- BAD: Jump straight into coding without understanding dependencies
- GOOD: Load parent issue and completed blockers first

**Don't expand scope**:
- BAD: Fix unrelated issues discovered during work
- GOOD: Note them and stay focused on the sub-task

**Don't skip verification**:
- BAD: Commit without running tests
- GOOD: Full validation (tests, typecheck, lint) before every commit

**Don't commit unrelated files**:
- BAD: `git add -A` to stage everything
- GOOD: Stage only files specified in sub-task

**Don't ignore failures**:
- BAD: Push despite test failures
- GOOD: Fix issues or output VERIFICATION_FAILED and stop

**Don't forget status updates**:
- BAD: Complete work but leave sub-task in Backlog
- GOOD: Update status and add completion comment

**Don't misuse status transitions**:
- BAD: Leave task in Backlog while working on it
- BAD: Move to Done before all acceptance criteria are met
- BAD: Move to Done when tests are failing
- GOOD: Move to "In Progress" immediately when starting work
- GOOD: Move to "Done" only after successful commit with all criteria met
- GOOD: Keep "In Progress" with progress comment if wrapping up incomplete

**Don't ask user questions**:
- BAD: Using AskUserQuestion during automated loop execution
- GOOD: Make reasonable decisions or output failure STATUS and stop
</anti_patterns>

<success_criteria>
A successful execution achieves:

- [ ] Backend detected from config
- [ ] Parent issue context loaded and understood
- [ ] Correct ready sub-task selected (no unresolved blockers)
- [ ] Sub-task moved to "In Progress" immediately when starting work
- [ ] Context from completed dependencies incorporated
- [ ] Implementation addresses all acceptance criteria
- [ ] Only specified files modified (scope discipline)
- [ ] Typecheck passes
- [ ] Tests pass
- [ ] Lint passes
- [ ] Sub-task verify command passes (if present in description)
- [ ] Commit created with conventional message
- [ ] Changes pushed to remote
- [ ] Sub-task moved to "Done" (if fully complete)
- [ ] Or: Sub-task kept "In Progress" with progress comment (if partial)
- [ ] Completion comment added to sub-task
- [ ] Completion report output with STATUS marker
- [ ] **STOPPED after one sub-task** (no continuation)
</success_criteria>

<termination_signals>
The skill outputs these status markers for loop script parsing:

| Status | Meaning | Loop Action |
|--------|---------|-------------|
| `STATUS: SUBTASK_COMPLETE` | Sub-task fully implemented, moved to Done | Continue loop |
| `STATUS: SUBTASK_PARTIAL` | Partial progress made, stays In Progress | Continue loop |
| `STATUS: ALL_COMPLETE` | All sub-tasks are done | Exit loop |
| `STATUS: ALL_BLOCKED` | Remaining sub-tasks are blocked | Exit loop |
| `STATUS: NO_SUBTASKS` | No sub-tasks exist | Exit loop |
| `STATUS: VERIFICATION_FAILED` | Tests/typecheck failed after retries | Exit loop |

Each invocation outputs exactly ONE status and then terminates.
</termination_signals>
