---
name: plan-guideline
description: Create comprehensive implementation plans with detailed file-level changes and test strategies
---

# Make a Plan

This skill instructs AI agents on how to create comprehensive implementation plans
for new features, refactoring, or bug fixes. The plan should be thorough enough to
serve as a blueprint for implementation, with concrete file-level details and
quantified complexity estimates.

## Planning Philosophy

A good plan is:
- **Concrete**: Specifies exact files to modify/create, not vague "audit the codebase" steps
- **Quantified**: Uses lines of code instead of time estimates
- **Design-first TDD**: Follows strict ordering: Documentation → Tests → Implementation
- **Interface-driven**: Documents API/interface changes before implementation
- **Actionable**: Can be directly used to create a GitHub issue with `open-issue` skill

### Development Workflow Order

**CRITICAL**: All implementation plans **MUST** follow this strict ordering:

1. **Documentation first** - Update all relevant documentation and design documents
2. **Tests second** - Write or update test cases that verify the behavior
3. **Implementation last** - Write the actual implementation code

This design-first test-driven development (TDD) style ensures:
- Clear design before coding
- Testable requirements
- No implementation without tests
- Living documentation that stays in sync

## Inputs

The plan-guideline skill takes the following inputs:
- User's goal or requirement (either from conversation or a markdown file)
- Current codebase context (will be explored by the agent)
- Existing architecture patterns and conventions

## Planning Process

The AI agent **MUST** follow this systematic process when creating a plan:

### 1. Goal Understanding Phase

**Objective**: Deeply understand what the user wants to achieve.

Actions:
- Read and analyze the user's requirements thoroughly
- Identify the core problem or feature request
- Clarify ambiguous requirements using `AskUserQuestion` if needed
- Determine the scope: is this a new feature, bug fix, refactoring, or improvement?

Output signals:
- Clear problem statement in 1-2 sentences
- Success criteria (what does "done" look like?)
- Out of scope items (what are we explicitly NOT doing?)

### 2. Codebase Audit Phase

**Objective**: Thoroughly explore the codebase to understand current implementation.

**CRITICAL**: The audit happens DURING planning, not as a step IN the plan.
The plan must contain audit RESULTS, not "TODO: audit the codebase" steps.

Actions:
- Use `Glob` to find relevant files by pattern
- Use `Grep` to search for related functionality
- Read existing implementations of similar features
- Identify architectural patterns and conventions
- Map out dependencies between modules

Output from this phase:
- List of files that will be modified (with line ranges if possible)
- List of files that will be created (with purpose)
- List of files that may be deleted
- Current architecture understanding

**Example of GOOD audit results in plan:**
```
Files to modify:
- `claude/skills/commit-msg/SKILL.md:15-45` - Add milestone commit logic
- `tests/test_git_commit.sh:23-67` - Update test cases for milestones

Files to create:
- `docs/milestone-workflow.md` - Document milestone commit process
```

**Example of BAD (do not include this):**
```
1. Audit the codebase to find relevant files
2. Determine which files need changes
```

### 3. Interface Design Phase

**Objective**: Design the public interfaces, APIs, and documentation changes.

Actions:
- Design new function/class signatures
- Plan changes to existing interfaces (breaking vs. non-breaking)
- Identify documentation files that need updates
- Design configuration or input formats if applicable
- Consider backward compatibility

Output:
- New interfaces to be created (with signatures)
- Modified interfaces (showing before/after)
- Documentation structure (what goes in which doc file)
- Configuration schema if applicable

**Example:**
```
New interfaces:
- Function: `create_milestone_commit(files: list, message: str, test_status: str)`
- Config: Add `milestone.allow_no_verify` to project settings

Modified interfaces:
- Function: `git_commit()` - add optional parameter `is_milestone: bool = False`

Documentation updates:
- `docs/git-msg-tags.md:15-20` - Add milestone tag explanation
- `claude/skills/commit-msg/SKILL.md:40-60` - Add milestone section
```

### 4. Test Strategy Design Phase

**Objective**: Design comprehensive test coverage before writing implementation code.

**CRITICAL**: Testing is not an afterthought. Design tests that validate:
- Happy path scenarios
- Edge cases and error conditions
- Integration with existing functionality
- Backward compatibility if applicable

Actions:
- Identify existing test files that need updates
- Design new test files for new functionality
- Specify what each test validates
- Consider test data requirements
- Plan test execution order (unit -> integration -> e2e)

Output:
- Test files to modify (with specific test cases to add/update)
- New test files to create (with purpose of each)
- Test data or fixtures needed
- Expected test coverage metrics

**Example:**
```
Test modifications:
- `tests/test_git_commit.sh:45-67` - Update to verify milestone flag handling
  - Test case: Verify `--no-verify` used only for milestone commits
  - Test case: Verify milestone commit message format

New test files:
- `tests/test_milestone_workflow.sh` - Test complete milestone workflow
  - Test case: Create milestone commit on dev branch (should succeed)
  - Test case: Attempt milestone commit on main (should fail)
  - Test case: Verify test status included in commit message
  - Estimated complexity: ~80 lines
```

### 5. Implementation Plan Phase

**Objective**: Create a step-by-step implementation plan with complexity estimates.

**CRITICAL**: Use lines of code (LOC) to estimate complexity, NOT time durations.

Complexity guidelines:
- Trivial: 1-20 LOC (simple config changes, single function additions)
- Small: 21-50 LOC (new function with basic logic, simple test cases)
- Medium: 51-150 LOC (new feature module, moderate refactoring)
- Large: 151-400 LOC (significant feature, multiple file changes)
- Very large: 401+ LOC (major refactoring, new subsystem)

**MANDATORY ORDERING**: Implementation steps **MUST** follow this sequence:

**Phase 1: Documentation (always first)**
- Update interface documentation
- Add/update design documents
- Update API references
- Add usage examples

**Phase 2: Test Cases (always second)**
- Create new test files
- Update existing test cases
- Add test fixtures/data
- Document test scenarios

**Phase 3: Implementation (always last)**
- Write the actual code
- Implement the logic
- Integrate with existing code

Actions:
- **NEVER** put implementation before documentation or tests
- Group documentation updates into Step 1 (or Steps 1-N for large features)
- Group test case work into the next step(s)
- Only after docs and tests, begin implementation steps
- For each step, specify:
  - Exact files to change (with line ranges if known)
  - What changes to make
  - Estimated lines of code
  - Dependencies on previous steps
- Break down steps larger than 400 LOC into substeps
- Consider milestone commits for features beyond 800 LOC total

**Understanding Milestone Commits:**

Milestone commits are for incremental progress on large features. They allow bypassing
pre-commit hooks, but this does NOT mean skipping tests:

- **Tests are ALWAYS run** - even for milestone commits
- **Temporarily accept incomplete test passage** - e.g., "35/42 tests passed"
- **Track progress mile-by-mile** - each milestone shows test progress
- **Work toward full passage** - continue until all tests pass
- **Only merge when complete** - all tests must pass before merging to main

Example milestone progression:
- Milestone 1: Documentation complete, tests created (0/8 tests pass)
- Milestone 2: Basic implementation (3/8 tests pass)
- Milestone 3: Edge cases handled (6/8 tests pass)
- Delivery commit: All tests pass (8/8), ready to merge

Output format:
```
Step N: [Brief description] (Estimated: X LOC)
- File 1: Specific change description
- File 2: Specific change description
Dependencies: [List steps that must complete first]
```

**Example (following Design-first TDD ordering):**
```
Step 1: Update documentation for milestone commits (Estimated: 60 LOC)
- `docs/git-msg-tags.md:15-20` - Add milestone tag definition and usage
- `claude/skills/commit-msg/SKILL.md:14-20` - Add milestone to inputs section
- `claude/skills/commit-msg/SKILL.md:40-60` - Add milestone commit section with examples
Dependencies: None

Step 2: Create test cases for milestone functionality (Estimated: 90 LOC)
- `tests/test_git_commit.sh:45-67` - Add milestone flag tests
  - Test: Verify `--no-verify` used only for milestone commits
  - Test: Verify milestone commit message format
- `tests/test_milestone_message.sh` - New test file for message validation
  - Test: Validate milestone commit on dev branch succeeds
  - Test: Validate milestone commit on main fails
Dependencies: Step 1 (documentation must be complete first)

Step 3: Implement milestone detection and handling logic (Estimated: 100 LOC)
- `claude/skills/commit-msg/SKILL.md:25-35` - Add milestone input handling
- `claude/skills/commit-msg/SKILL.md:85-88` - Add pre-commit bypass logic
Dependencies: Step 2 (tests must exist before implementation)

Total estimated complexity: 250 LOC (Medium-Large feature)
Recommended approach: Implement in single development session
Note: Follows Design-first TDD: Docs (Step 1) → Tests (Step 2) → Implementation (Step 3)
```

## Plan Output Format

The final plan should be structured as follows:

```markdown
# Implementation Plan: [Feature/Goal Name]

## Goal
[1-2 sentence problem statement]

**Success criteria:**
- [Criterion 1]
- [Criterion 2]

**Out of scope:**
- [What we're not doing]

## Codebase Analysis

**Files to modify:**
- `path/to/file1:lines` - Purpose
- `path/to/file2:lines` - Purpose

**Files to create:**
- `path/to/new/file1` - Purpose (Estimated: X LOC)
- `path/to/new/file2` - Purpose (Estimated: X LOC)

**Files to delete:**
- `path/to/deprecated/file` - Reason

**Current architecture notes:**
[Key observations about existing code]

## Interface Design

**New interfaces:**
- [Interface signatures and descriptions]

**Modified interfaces:**
- [Before/after comparisons]

**Documentation changes:**
- [Doc files to update with sections]

## Test Strategy

**Test modifications:**
- `test/file1:lines` - What to test
  - Test case: Description
  - Test case: Description

**New test files:**
- `test/new_file` - Purpose (Estimated: X LOC)
  - Test case: Description
  - Test case: Description

**Test data required:**
- [Fixtures, sample data, etc.]

## Implementation Steps

**Step 1: [Description]** (Estimated: X LOC)
- File changes
Dependencies: None

**Step 2: [Description]** (Estimated: X LOC)
- File changes
Dependencies: Step 1

...

**Total estimated complexity:** X LOC ([Complexity level])
**Recommended approach:** [Single session / Milestone commits / etc.]
```

## Integration with Other Skills

After creating a plan, the AI agent should:

1. **Present to user for approval**
   - Display the complete plan
   - Ask for confirmation or revisions

2. **Create GitHub issue** (once approved)
   - Use the `open-issue` skill
   - The plan becomes the "Proposed Solution" section
   - Add appropriate `[plan][tag]` prefix

3. **Begin implementation** (after issue created)
   - Use the `fork-dev-branch` skill to create a development branch
   - Follow the step-by-step plan
   - Use `commit-msg` skill for commits (milestone commits if needed)
   - Use `open-pr` skill when implementation is complete

## Examples

### Example 1: Small Feature Addition

**User request:** "Add support for milestone commits in the commit-msg skill"

**Plan excerpt:**
```markdown
# Implementation Plan: Milestone Commit Support

## Goal
Add milestone commit functionality to allow work-in-progress commits that can
bypass pre-commit hooks on development branches.

**Success criteria:**
- Milestone commits work only on development branches (not main)
- Milestone commits include test status in message
- Pre-commit hooks can be bypassed with explicit milestone flag

**Out of scope:**
- Automatic milestone detection
- Milestone progress tracking UI

## Codebase Analysis

**Files to modify:**
- `claude/skills/commit-msg/SKILL.md:14-20` - Add milestone input handling
- `claude/skills/commit-msg/SKILL.md:40-88` - Add milestone message format
- `tests/test_git_commit.sh:45-67` - Add milestone tests

**Files to create:**
- None required

**Current architecture notes:**
- Commit skill currently supports only delivery commits
- Pre-commit hook validation is mandatory for all commits
- Branch detection logic already exists in workflow

## Implementation Steps

**Step 1: Update documentation** (Estimated: 60 LOC)
- `docs/git-msg-tags.md:15-20` - Add milestone tag definition and usage rules
- `claude/skills/commit-msg/SKILL.md:14-20` - Add milestone to inputs section
- `claude/skills/commit-msg/SKILL.md:40-60` - Add milestone message format section
Dependencies: None

**Step 2: Create test cases** (Estimated: 85 LOC)
- `tests/test_git_commit.sh:45-67` - Add milestone-specific tests
  - Test: Milestone commits bypass hooks on dev branches
  - Test: Milestone commits fail on main branch
  - Test: Milestone message includes test status
- `tests/test_milestone_format.sh` - New test for message validation
Dependencies: Step 1 (documentation must define behavior first)

**Step 3: Implement milestone commit logic** (Estimated: 95 LOC)
- `claude/skills/commit-msg/SKILL.md:25-35` - Add milestone input processing
- `claude/skills/commit-msg/SKILL.md:85-88` - Add pre-commit bypass logic
Dependencies: Step 2 (tests must exist to validate implementation)

**Total estimated complexity:** 240 LOC (Medium feature)
**Recommended approach:** Single development session following Docs → Tests → Implementation
```

### Example 2: Large Refactoring

**User request:** "Refactor the SDK initialization to validate directories"

**Plan excerpt:**
```markdown
# Implementation Plan: SDK Init Directory Validation

## Goal
Add comprehensive directory validation to SDK initialization to prevent
initialization in invalid locations and provide clear error messages.

**Success criteria:**
- Validate target directory exists and is writable
- Check for conflicting files before initialization
- Provide actionable error messages
- Support both init and update modes

**Out of scope:**
- Automatic directory creation
- Backup/rollback functionality

## Codebase Analysis

**Files to modify:**
- `Makefile:45-67` - Add validation before template copying
- `docs/OPTIONS.md:25-40` - Document validation behavior

**Files to create:**
- `scripts/validate_target_dir.sh` - Directory validation logic (Est: 120 LOC)
- `tests/test_directory_validation.sh` - Validation tests (Est: 180 LOC)

## Test Strategy

**New test files:**
- `tests/test_directory_validation.sh` (Estimated: 180 LOC)
  - Test case: Valid empty directory (should pass)
  - Test case: Non-existent directory (should fail with error)
  - Test case: Directory with conflicting files (should fail with list)
  - Test case: Non-writable directory (should fail with permission error)
  - Test case: Init mode vs update mode differences

## Implementation Steps

**Step 1: Update documentation** (Estimated: 60 LOC)
- `docs/OPTIONS.md:25-40` - Document validation behavior and error messages
- `docs/OPTIONS.md:50-65` - Add examples of valid/invalid target directories
Dependencies: None

**Step 2: Create test cases** (Estimated: 180 LOC)
- `tests/test_directory_validation.sh` - New comprehensive validation test suite
  - Test: Valid empty directory initialization
  - Test: Non-existent directory rejection
  - Test: Conflicting files detection
  - Test: Permission error handling
  - Test: Init vs update mode differences
Dependencies: Step 1 (documentation defines expected behavior)

**Step 3: Implement validation script** (Estimated: 120 LOC)
- `scripts/validate_target_dir.sh` - New validation script with all checks
  - Directory existence check
  - Write permission validation
  - Conflict detection logic
  - Mode-specific validation rules
Dependencies: Step 2 (tests define all edge cases)

**Step 4: Integrate validation into Makefile** (Estimated: 60 LOC)
- `Makefile:45-67` - Add validation call before template copying
- `Makefile:70-85` - Add error handling and user feedback
Dependencies: Step 3 (validation script must exist)

**Total estimated complexity:** 420 LOC (Large feature)
**Recommended approach:** Use milestone commits for incremental progress

**Milestone strategy:**
- Milestone 1 (after Step 2): Documentation and tests complete (0/5 tests pass)
  - All tests exist but implementation not started yet
- Milestone 2 (after Step 3): Validation script implemented (3/5 tests pass)
  - Basic validation working, edge cases still failing
- Delivery commit (after Step 4): Full integration complete (5/5 tests pass)
  - All tests pass, ready for PR

**Note:** Follows Design-first TDD strictly: Docs (Step 1) → Tests (Step 2) → Implementation (Steps 3-4)
Tests are run at each milestone; failing tests are accepted temporarily as progress checkpoints.
```

## Important Notes

1. **MANDATORY ordering - Design-first TDD**: Implementation steps **MUST** follow this order:
   - Step 1 (or Steps 1-N): Documentation updates
   - Step 2 (or Steps N+1-M): Test case creation/updates
   - Step 3+ (or Steps M+1-end): Implementation code

   **NEVER** put implementation before documentation or tests. This is non-negotiable.

2. **No vague audit steps**: The plan must contain concrete file names and line ranges,
   not "audit the codebase" tasks. Auditing happens during planning.

3. **Quantify with LOC**: Always use lines of code estimates, never time-based estimates
   like "2 hours" or "3 days".

4. **Test-first mindset**: Design tests before implementation details. Tests clarify
   requirements and prevent scope creep. Tests must exist before writing implementation.

5. **Break down large steps**: If a single step exceeds 400 LOC, break it into substeps.
   Consider milestone commits for features exceeding 800 LOC total.

6. **Document interfaces early**: Interface design comes before implementation planning.
   Changes to interfaces affect multiple files and should be designed carefully.

7. **Use existing patterns**: During audit, identify and follow existing architectural
   patterns and naming conventions in the codebase.

8. **Be specific**: Prefer "Modify `file.py:45-67` to add parameter validation" over
   "Update the validation logic". The more specific, the better.

9. **Dependencies reflect ordering**: Each step's dependencies should enforce the ordering:
   - Tests depend on documentation
   - Implementation depends on tests
   - Never skip the dependency chain

10. **Milestone commits run tests**: When planning features that require milestone commits:
    - Tests are ALWAYS run at each milestone (not skipped)
    - Bypassing pre-commit hooks means accepting incomplete test passage temporarily
    - Each milestone must report test status (e.g., "15/20 tests passed")
    - Work incrementally until all tests pass
    - Only merge to main when all tests pass (100% passage required)
