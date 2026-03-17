---
name: workflow-validate-plan
description: This skill should be used when validating that an implementation plan was correctly executed. It verifies success criteria, runs tests, identifies deviations, and presents structured completion options including MR creation or discard.
---

# Validate Plan Workflow

## Overview

Validate that an implementation plan was correctly executed, verifying all success criteria and identifying any deviations or issues. Present structured completion options after verification passes.

**Type:** RIGID - Follow verification steps exactly. Don't skip test verification or present options before tests pass.

**Output:** Validation report with structured completion options.

## When to Use

Use this workflow when:
- Implementation phase is complete and needs verification
- Checking if plan tasks were executed correctly
- Preparing for merge request creation
- Validating work before handoff

**Announce at start:** "I'm using the validate-plan workflow to verify the implementation."

## Core Principles

From verification-before-completion skill:
- **Evidence before claims** - Run fresh verification before reporting anything as "done" or "passing"
- **Verify tests BEFORE options** - Don't present completion options until tests pass
- **Structured completion choices** - Present exactly 3 options when work is validated
- **Typed confirmation** - Require typed "discard" for destructive actions

## Initial Setup

When invoked:

### 1. Determine Context

Are you in an existing conversation or starting fresh?
- If existing: Review what was implemented in this session
- If fresh: Need to discover what was done through git and codebase analysis
- Check which worktree you're in: `git worktree list`

### 2. Locate the Plan

- If plan path provided, use it
- If not, look for the `./plan.md` file and use it if present
- Otherwise, search recent commits or ask user

### 3. Gather Implementation Evidence

```bash
# Check recent commits
git log --oneline -n 20
git diff HEAD~N..HEAD  # Where N covers implementation commits
git status
git worktree list      # Show all worktrees
```

### 4. CRITICAL: Verify Tests FIRST

**Before presenting any completion options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with completion validation until tests pass.
```

**STOP here. Don't proceed to Step 5.**

**If tests pass:** Continue to validation process.

## Validation Process

### Step 1: Context Discovery

If starting fresh or need more context:

1. **Read the implementation plan** completely
2. **Identify what should have changed**:
   - List all files that should be modified
   - Note all success criteria (automated and manual)
   - Identify key functionality to verify

3. **Spawn parallel research tasks** to discover implementation:
   ```
   Task 1 - Verify database changes:
   Research if migration [N] was added and schema changes match plan.
   Check: migration files, schema version, table structure
   Return: What was implemented vs what plan specified

   Task 2 - Verify code changes:
   Find all modified files related to [feature].
   Compare actual changes to plan specifications.
   Return: File-by-file comparison of planned vs actual

   Task 3 - Verify test coverage:
   Check if tests were added/modified as specified.
   Run test commands and capture results.
   Return: Test status and any missing coverage
   ```

### Step 2: Systematic Validation

For each phase in the plan:

1. **Check completion status**:
   - Look for checkmarks in the plan (- [x])
   - Verify the actual code matches claimed completion
   - Confirm worktree context is correct

2. **Run automated verification**:
   - Execute each command from "Automated Verification"
   - Document pass/fail status
   - If failures, investigate root cause

3. **Assess manual criteria**:
   - List what needs manual testing
   - Provide clear steps for user verification

4. **Think deeply about edge cases**:
   - Were error conditions handled?
   - Are there missing validations?
   - Could the implementation break existing functionality?
   - Will this work correctly in bare monorepo context?

### Step 3: Generate Validation Report

Create comprehensive validation summary:

```markdown
## Validation Report: [Plan Name]

### Implementation Status
- Phase 1: [Name] - Fully implemented
- Phase 2: [Name] - Fully implemented
- Phase 3: [Name] - Partially implemented (see issues)

### Automated Verification Results
- Build passes: `make build`
- Tests pass: `make test`
- Linting issues: `make lint` (3 warnings)

### Code Review Findings

#### Matches Plan:
- Database migration correctly adds [table]
- API endpoints implement specified methods
- Error handling follows plan

#### Deviations from Plan:
- Used different variable names in [file:line]
- Added extra validation in [file:line] (improvement)

#### Potential Issues:
- Missing index on foreign key could impact performance
- No rollback handling in migration

### Manual Testing Required:
1. UI functionality:
   - [ ] Verify [feature] appears correctly
   - [ ] Test error states with invalid input

2. Integration:
   - [ ] Confirm works with existing [component]
   - [ ] Check performance with large datasets

### Recommendations:
- Address linting warnings before merge
- Consider adding integration test for [scenario]
- Document new API endpoints
```

### Step 4: Present Completion Options

**Only present these options AFTER all verification passes.**

Present **exactly these 3 options:**

```
Implementation complete and verified. What would you like to do?

1. Push and create a Merge Request
2. Keep the branch as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute User's Choice

Based on user's selection (1-3), execute the appropriate workflow:

**Note:** When working with worktrees, ensure you're in the correct directory context before executing git commands.

#### Option 1: Push and Create Merge Request

Use `mr-generator` skill to generate intelligent MR descriptions from commits:

```bash
# Push worktree's branch
git push -u origin <feature-branch>

# Generate MR description with mr-generator
python3 <skill-path>/mr-generator/scripts/mr_generator.py --create --jira <ticket-id>

# Or manually create MR with description:
glab mr create --title "<title>" --description "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps from validation report>
EOF
)"
```

After MR creation, use `mr-tracker` skill to monitor review activity:
```bash
./scripts/mr_tracker.sh watch <mr-iid> 30  # Check every 30 seconds
```

#### Option 2: Keep As-Is

Report: "Keeping worktree <name>. All changes remain for later handling."

**Don't make any git changes.**

#### Option 3: Discard

**Confirm first:**
```
This will permanently delete:
- Worktree <name>
- Branch <name>
- All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
# Navigate to main repository (not the worktree)
cd $(git rev-parse --show-toplevel)/..

# Remove the worktree and its branch
git worktree remove <worktree-path> --force
git branch -D <feature-branch>
```

## Working with Existing Context

If you were part of the implementation:
- Review the conversation history
- Check your todo list for what was completed
- Focus validation on work done in this session
- Be honest about any shortcuts or incomplete items
- Use `git worktree list` to identify the current worktree

## Important Guidelines

1. **Be thorough but practical** - Focus on what matters
2. **Run all automated checks** - Don't skip verification commands
3. **Document everything** - Both successes and issues
4. **Think critically** - Question if the implementation truly solves the problem
5. **Consider maintenance** - Will this be maintainable long-term?
6. **Evidence before claims** - Always show test/lint output before reporting status

## Red Flags - STOP

If you catch yourself:
- Reporting "done" without running verification
- Assuming tests pass from earlier runs
- Offering completion options when tests failed
- Using "should pass" or "looks good"
- Not showing verification command output

**STOP and run the verification commands first.**

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Skipping test verification | Ship broken code | Run tests BEFORE presenting options |
| Presenting open-ended next step | User doesn't know options | Present exactly 3 structured choices |
| Auto-deleting work | Lost progress | Require typed "discard" confirmation |
| Merging without verifying | Breaks base branch | Run tests on merged result |
| Wrong CLI tool (gh vs glab) | MR creation fails | Use `glab` for GitLab |

## Validation Checklist

Always verify:
- [ ] All phases marked complete are actually done
- [ ] Automated tests pass
- [ ] Code follows existing patterns
- [ ] No regressions introduced
- [ ] Error handling is robust
- [ ] Documentation updated if needed
- [ ] Manual test steps are clear
- [ ] Using correct Git repository/worktree context
- [ ] If creating MR (Option 1): Used `mr-generator` skill for description
- [ ] If MR created: Use `mr-tracker` skill to monitor review activity

## Related Skills

These skills complement this workflow:

### mr-generator
Generates intelligent GitLab merge request descriptions from git commits. Use when creating MRs (Option 1) to automatically generate professional descriptions with proper commit categorization and Jira integration.

### verification-before-completion
Core discipline underlying this workflow. Enforces evidence-before-claims by requiring fresh verification output before any success assertions.

### mr-tracker
Monitors GitLab merge request activity after MR creation. Use for watching MR comments, checking approval status, and tracking review feedback.

### jira-ticket-creator
Use when work items need Jira ticket creation for traceability.

### jira-ticket-fetcher
Fetches Jira ticket content by ID or text search. Useful for referencing related tickets in MR descriptions.
