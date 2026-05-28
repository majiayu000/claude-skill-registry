---
name: summarize-changes
description: Structured workflow for summarizing code changes after completing tasks. Creates clear, actionable summaries of what was changed, why, and what to verify.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep, Bash]
best_practices:
  - Always summarize after non-trivial coding tasks
  - Focus on the "what" and "why", not just listing files
  - Include verification steps for reviewers
  - Note any breaking changes or migration needs
  - Keep summaries concise but complete
error_handling: graceful
streaming: supported
---

<identity>
Change Summarization Specialist - Creates clear, structured summaries of code changes for documentation and review.
</identity>

<capabilities>
- Generating structured change summaries
- Identifying affected components and dependencies
- Creating verification checklists
- Documenting breaking changes
- Writing commit message suggestions
- Producing PR description content
</capabilities>

<instructions>

## When to Use

Invoke this skill:

- After completing any non-trivial coding task
- Before committing changes
- When preparing PR descriptions
- After think-about-whether-you-are-done confirms completion

## Change Summary Workflow

### Step 1: Gather Change Information

Collect information about what changed:

1. **Modified Files**: List all files that were changed
2. **Change Types**: Categorize changes (new, modified, deleted, renamed)
3. **Scope**: Identify affected components/modules

```bash
# If using git, gather diff summary
git status
git diff --stat
```

### Step 2: Analyze Change Impact

For each significant change, document:

1. **What Changed**: Specific modification made
2. **Why It Changed**: Reason/motivation for the change
3. **Impact**: What this affects (functionality, performance, API)

### Step 3: Generate Summary

Use this template:

```markdown
## Changes Summary

### Overview

[1-2 sentence high-level description of what was accomplished]

### Changes Made

#### New Files

| File              | Purpose                            |
| ----------------- | ---------------------------------- |
| `path/to/file.ts` | Description of what this file does |

#### Modified Files

| File                  | Changes                  |
| --------------------- | ------------------------ |
| `path/to/existing.ts` | What was changed and why |

#### Deleted Files

| File             | Reason                    |
| ---------------- | ------------------------- |
| `path/to/old.ts` | Why this file was removed |

### Technical Details

**Key Implementation Decisions**:

- Decision 1 and rationale
- Decision 2 and rationale

**Dependencies Added/Removed**:

- Added: `package-name@version` - reason
- Removed: `old-package` - reason

### Breaking Changes

[List any breaking changes or "None"]

### Migration Required

[Any steps needed to adopt these changes or "None"]

### Verification Checklist

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed
- [ ] Documentation updated
- [ ] No console errors
- [ ] Performance acceptable

### Related Issues/Tasks

- Fixes #123
- Related to #456
```

### Step 4: Commit Message Suggestion

Generate a conventional commit message:

```
<type>(<scope>): <description>

<body - what and why>

<footer - breaking changes, issues>
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation only
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example**:

```
fix(auth): resolve login timeout error

Increased timeout from 5s to 30s for login requests.
The previous timeout was insufficient for users on slow connections.

Fixes #123
```

### Step 5: PR Description (if applicable)

If changes are for a PR, expand the summary:

```markdown
## Summary

[Brief description of what this PR does]

## Changes

[List of key changes]

## Testing

[How this was tested]

## Screenshots

[If UI changes]

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

</instructions>

<examples>
<usage_example>
**After fixing a bug**:

```markdown
## Changes Summary

### Overview

Fixed the search timeout error that occurred when users had slow connections.

### Changes Made

#### Modified Files

| File                     | Changes                          |
| ------------------------ | -------------------------------- |
| `src/api/search.ts`      | Increased timeout from 5s to 30s |
| `src/api/search.test.ts` | Added test for timeout handling  |

### Technical Details

**Key Implementation Decisions**:

- Used 30s timeout as it covers 99th percentile of actual search times
- Added retry logic with exponential backoff for transient failures

**Dependencies Added/Removed**:

- None

### Breaking Changes

None

### Verification Checklist

- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing performed
- [x] No console errors

### Commit Message
```

fix(search): increase timeout to handle slow connections

Increased search API timeout from 5s to 30s and added retry logic.
Users on slow connections were experiencing frequent timeout errors.

Fixes #456

```

```

</usage_example>

<usage_example>
**After adding a new feature**:

```markdown
## Changes Summary

### Overview

Added user email validation with real-time feedback on the registration form.

### Changes Made

#### New Files

| File                               | Purpose                    |
| ---------------------------------- | -------------------------- |
| `src/utils/emailValidator.ts`      | Email validation utilities |
| `src/utils/emailValidator.test.ts` | Tests for email validation |

#### Modified Files

| File                                  | Changes                         |
| ------------------------------------- | ------------------------------- |
| `src/components/RegistrationForm.tsx` | Added validation to email field |
| `src/i18n/en.json`                    | Added validation error messages |

### Technical Details

**Key Implementation Decisions**:

- Used RFC 5322 compliant regex for validation
- Validation runs on blur to avoid interrupting typing
- Debounced validation (300ms) for performance

**Dependencies Added/Removed**:

- None (used built-in regex)

### Breaking Changes

None - additive change only

### Verification Checklist

- [x] Unit tests pass (15 test cases for validation)
- [x] Integration tests pass
- [x] Manual testing performed
- [x] Works with screen readers (a11y tested)

### Commit Message
```

feat(registration): add email validation with real-time feedback

Added RFC 5322 compliant email validation to registration form.
Validation runs on blur with debouncing for smooth UX.

Closes #789

```

```

</usage_example>
</examples>

<integration>
**Related Skills**:
- `thinking-tools` - Use before summarizing to validate completion
- `git-expert` - For commit and PR workflows
- `commit-message-guidelines` - For conventional commits
</integration>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
