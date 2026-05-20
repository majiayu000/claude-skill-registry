---
name: implementation
description: Implements GitHub issues that have approved implementation plans. Use when you need to implement an issue, create a branch, write code, and submit a PR. Requires a clear implementation plan in the issue comments.
---

# Issue Implementation

## Project Board

All issues are tracked on the **Anubis Issue Tracker** project board:
- **Project URL:** https://github.com/users/forrestthewoods/projects/8
- **Project Number:** 8
- **Owner:** forrestthewoods

## Board Status Workflow

| Status | Description |
|--------|-------------|
| **Backlog** | Future ideas or deferred work; not ready for action yet |
| **Triage** | New issues not yet added to the project board |
| **Needs Agent Review** | Issues ready for agent to review and categorize |
| **Needs Human Review** | Agent has questions; waiting for human clarification |
| **Ready to Implement** | Agent reviewed, wrote plan, no questions remaining |
| **Needs Code Review** | Implementation in progress (has active branch) |
| **Done** | Closed and completed (automatic via GitHub) |

**Important:** Issues in **Backlog** should be **completely ignored** by this skill. These are deferred tasks that are not ready for implementation.

## Purpose

This skill guides the implementation of GitHub issues that have been reviewed and have an approved implementation plan. It ensures:

1. The issue has a clear, actionable implementation plan
2. All questions have been answered before implementation begins
3. Branch naming conventions are followed
4. Code is properly committed and pushed
5. The project board status is updated appropriately

## Prerequisites

Before implementing an issue, verify:
- Issue is in **Ready to Implement** status on the project board
- Issue has a clear implementation plan in the comments
- No unanswered questions remain on the issue
- The issue has a difficulty label (`difficulty: easy`, `medium`, or `hard`)

## Instructions

### Step 1: Fetch Issue Details and Comments

```bash
# Get the issue with all comments
gh issue view <number> --json number,title,body,labels,comments,state

# Get just the comments for easier reading
gh issue view <number> --comments
```

### Step 2: Analyze the Implementation Plan

Look for the most recent comment containing an **Implementation Plan**. The plan should have:

1. **Overview** - Brief description of the approach
2. **Steps** - Numbered implementation steps
3. **Files to Modify** - List of files that need changes
4. **Testing** - Test cases to verify the implementation
5. **Considerations** - Edge cases or concerns

**CRITICAL: Before proceeding, verify:**

| Check | Action if Failed |
|-------|------------------|
| Has implementation plan? | Stop. Use issue-review skill to create one |
| Plan is clear and complete? | Stop. Ask clarifying questions |
| All questions answered? | Stop. Wait for human response |
| You understand the plan? | Stop. Ask clarifying questions |
| Plan is technically feasible? | Stop. Raise concerns as questions |

**If ANY of these checks fail, do NOT proceed with implementation.** Post your questions as a comment and move the issue to "Needs Human Review".

### Step 3: Ask Questions if Needed

If you have ANY questions or uncertainties about the implementation:

```bash
# Write questions to temp file
mkdir -p ./.anubis-temp/github
```

Write to `./.anubis-temp/github/issue-<number>-questions.md`:
```markdown
## Implementation Questions

Before proceeding with implementation, I need clarification on the following:

1. [Specific question about the plan]
2. [Question about expected behavior]
3. [Question about edge cases]

Once these are answered, I'll proceed with the implementation.
```

```bash
# Post the questions
gh issue comment <number> --body-file ./.anubis-temp/github/issue-<number>-questions.md
```

**After posting questions, STOP. Do not proceed with implementation until questions are answered.**

### Step 4: Create Implementation Branch

Use the branch naming convention defined in the branch-naming skill:

**For Claude sessions:**
```
claude/<issue-number>-<short-description>-<session-id>
```

**Standard pattern:**
```
<issue-number>-<short-description>
```

```bash
# Create and checkout the branch
git checkout -b claude/<issue-number>-<short-description>-<session-id>

# Example:
git checkout -b claude/42-build-caching-Abc12
```

**Branch naming rules:**
- Start with the issue number
- Use lowercase letters and hyphens only
- Keep descriptions short (2-4 words)
- Include session ID for Claude branches (ensures uniqueness)

### Step 5: Implement the Changes

Follow the implementation plan step by step:

1. **Read existing code first** - Understand the codebase before making changes
2. **Make incremental changes** - Don't try to do everything at once
3. **Follow existing patterns** - Match the code style of the surrounding code
4. **Write tests** - Add tests as specified in the implementation plan
5. **Verify as you go** - Run tests after significant changes

**Implementation guidelines:**
- Prefer editing existing files over creating new ones
- Keep changes minimal and focused on the issue
- Don't refactor unrelated code
- Don't add features not specified in the plan
- Add comments only where the logic isn't self-evident

### Step 6: Run Tests and Build

```bash
# Run the test suite
cargo test

# Build the project
cargo build --release
```

**If tests fail:**
1. Fix the failing tests
2. If the failure reveals a flaw in the plan, stop and ask questions
3. Do not proceed with a PR if tests are failing

### Step 7: Commit Changes

Create meaningful commits with issue references:

```bash
# Stage changes
git add <files>

# Commit with issue reference
git commit -m "$(cat <<'EOF'
Brief description of change

Detailed explanation if needed.

Refs #<issue-number>
EOF
)"
```

**Commit message guidelines:**
- Use present tense ("Add feature" not "Added feature")
- First line is a brief summary (50 chars max)
- Include detailed explanation if the change is complex
- Reference the issue with `Refs #N` or `Fixes #N`
- Use `Fixes #N` only if this commit fully resolves the issue

### Step 8: Push the Branch

```bash
# Push with upstream tracking
git push -u origin <branch-name>

# Example:
git push -u origin claude/42-build-caching-Abc12
```

**If push fails due to network errors, retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s).**

### Step 9: Create Pull Request

```bash
# Create temp file for PR body
mkdir -p ./.anubis-temp/github
```

Write PR description to `./.anubis-temp/github/pr-<issue-number>.md`:
```markdown
## Summary

[Brief description of what this PR implements]

- [Key change 1]
- [Key change 2]
- [Key change 3]

Fixes #<issue-number>

## Implementation Notes

[Any important details about the implementation approach]

## Test Plan

- [ ] Run `cargo test` - all tests pass
- [ ] Run `cargo build --release` - builds successfully
- [ ] [Specific test from implementation plan]
- [ ] [Another specific test]

## Checklist

- [ ] Code follows existing patterns
- [ ] Tests added/updated as needed
- [ ] No unrelated changes included
```

```bash
# Create the PR
gh pr create --title "<Brief description> (#<issue-number>)" \
  --body-file ./.anubis-temp/github/pr-<issue-number>.md
```

### Step 10: Update Project Board

After creating the PR, the issue should move to "Needs Code Review":

```bash
# Get project and field IDs
gh project view 8 --owner forrestthewoods --format json

# Get item ID for the issue
gh project item-list 8 --owner forrestthewoods --format json | jq '.items[] | select(.content.number == <issue-number>)'

# Update status to "Needs Code Review"
gh project item-edit --project-id <project-id> --id <item-id> --field-id <status-field-id> --single-select-option-id <needs-code-review-option-id>
```

## Workflow Summary

```
1. Fetch issue and comments
2. Find implementation plan
3. Verify plan is complete and understood
   ├── Questions? → Post questions, STOP
   └── No questions? → Continue
4. Create branch (following naming convention)
5. Implement changes per plan
6. Run tests and build
   ├── Failures? → Fix or ask questions
   └── Success? → Continue
7. Commit with issue references
8. Push branch
9. Create PR
10. Update project board status
```

## When to STOP and Ask Questions

Do NOT proceed with implementation if:

- The implementation plan is missing or incomplete
- You don't understand part of the plan
- The plan seems technically infeasible
- You discover issues not addressed in the plan
- Edge cases aren't covered
- The plan conflicts with existing code patterns
- Dependencies are missing or unclear
- Test requirements are unclear

**When in doubt, ask.** It's better to clarify than to implement incorrectly.

## Example: Full Implementation Flow

**Issue #42: Add build result caching**

```bash
# Step 1: Fetch issue
gh issue view 42 --json number,title,body,labels,comments,state

# Step 2: Review - Found implementation plan in comments:
# - Overview: Cache compilation results to disk
# - Steps: 1) Create cache module, 2) Add hash computation, 3) Integrate with job system
# - Files: src/cache.rs (new), src/job_system.rs, src/anubis.rs
# - Testing: Unit tests for cache, integration test for build caching

# Step 3: No questions - plan is clear and complete

# Step 4: Create branch
git checkout -b claude/42-build-caching-Xyz99

# Step 5: Implement changes per plan
# ... make code changes ...

# Step 6: Run tests
cargo test
cargo build --release

# Step 7: Commit
git add src/cache.rs src/job_system.rs src/anubis.rs
git commit -m "$(cat <<'EOF'
Add build result caching

Implement file-based caching for compilation results to avoid
redundant recompilation of unchanged source files.

Fixes #42
EOF
)"

# Step 8: Push
git push -u origin claude/42-build-caching-Xyz99

# Step 9: Create PR
gh pr create --title "Add build result caching (#42)" \
  --body-file ./.anubis-temp/github/pr-42.md

# Step 10: Update board status
# ... update to "Needs Code Review" ...
```

## Example: Stopping for Questions

**Issue #15: Add ARM64 support**

```bash
# Step 1: Fetch issue
gh issue view 15 --comments

# Step 2: Found implementation plan but unclear on:
# - Which ARM64 targets (Linux? macOS? Windows?)
# - Cross-compilation requirements
# - CI testing approach

# Step 3: Post questions
mkdir -p ./.anubis-temp/github
cat > ./.anubis-temp/github/issue-15-questions.md << 'EOF'
## Implementation Questions

Before proceeding with ARM64 support implementation, I need clarification:

1. **Target platforms:** Which ARM64 platforms should be supported initially?
   - Linux ARM64 (aarch64-unknown-linux-gnu)
   - macOS ARM64 (aarch64-apple-darwin)
   - Windows ARM64 (aarch64-pc-windows-msvc)

2. **Cross-compilation:** Should this support cross-compiling TO ARM64 from x64 hosts, or only native ARM64 compilation?

3. **CI testing:** Do we have access to ARM64 CI runners, or should tests be skipped/emulated?

Once these are clarified, I'll proceed with the implementation.
EOF

gh issue comment 15 --body-file ./.anubis-temp/github/issue-15-questions.md

# STOP - Do not proceed until questions are answered
```

## Guidelines

- **Never implement without a clear plan** - If the plan is missing or unclear, stop and ask
- **Follow the plan exactly** - Don't add unrequested features or refactoring
- **Ask questions early** - It's cheaper to clarify before implementing
- **Keep changes focused** - One issue = one focused PR
- **Test before pushing** - Ensure all tests pass before creating a PR
- **Use temp files for GitHub content** - Avoid inline `--body` with special characters
- **Reference issues in commits** - Use `Refs #N` or `Fixes #N`
- **Update the project board** - Keep status accurate

## Branch Naming Quick Reference

```
# Claude sessions (include session ID for uniqueness)
claude/<issue>-<description>-<session>
Examples:
  claude/42-build-caching-Abc12
  claude/15-arm64-support-Xyz99

# Standard (human developers)
<issue>-<description>
Examples:
  42-build-caching
  15-arm64-support
```

## Commit Message Quick Reference

```
# Simple commit
Add cache module

Refs #42

# Commit that closes issue
Implement build caching

Add file-based caching for compilation results.

Fixes #42

# Partial work
Extract cache utilities

Move caching logic to dedicated module.

Refs #42
```

## Detecting if Implementation is Needed

Before starting, verify the issue needs implementation:

```bash
# Check issue status on board
gh project item-list 8 --owner forrestthewoods --format json | jq '.items[] | select(.content.number == <issue-number>) | .status'

# Check for existing branches
git ls-remote --heads origin | grep -i "<issue-number>"

# Check for existing PRs
gh pr list --search "#<issue-number>" --state all
```

| Situation | Action |
|-----------|--------|
| Status is "Ready to Implement" | Proceed with implementation |
| Status is "Needs Agent Review" | Use issue-review skill first |
| Status is "Needs Human Review" | Wait for human response |
| Status is "Needs Code Review" | Implementation already in progress |
| Already has open PR | Review existing PR instead |
| Already has branch | Check branch status, continue or start fresh |
