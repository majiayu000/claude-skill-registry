---
name: bug-history-summarizer
description: "Summarizes the complete lifecycle of a bug across code versions, tracking its introduction, detection, fixing attempts, and regression history. Use when users need to: (1) Understand how a bug evolved over time, (2) Trace when and how a bug was introduced, (3) Analyze fix attempts and their effectiveness, (4) Identify regression patterns, (5) Generate bug lifecycle reports for documentation or post-mortems. Takes a repository, bug identifier, and version history as input."
---

# Bug History Summarizer

Trace and summarize the complete lifecycle of a bug across code versions.

## Workflow

Follow these steps to generate a comprehensive bug history summary:

### 1. Identify the Bug and Gather Context

Collect essential information:

- **Bug identifier**: Issue number, commit hash, or bug description
- **Repository**: Target codebase with version history
- **Version range**: Specific versions/commits to analyze (or entire history)
- **Related artifacts**: Issue reports, pull requests, commit messages, test results

### 2. Trace Bug Introduction

Identify when and how the bug was introduced:

**Using git blame and bisect:**
- Run `git blame` on affected files to find when problematic lines were added
- Use `git bisect` to pinpoint the exact commit that introduced the bug
- Analyze the introducing commit: author, date, purpose, related changes

**Analyze introduction context:**
- What was the original intent of the change?
- Was it a new feature, refactoring, or bug fix?
- Were there code review comments or warnings?
- What tests existed at the time?

### 3. Track Detection History

Document when and how the bug was discovered:

- **Initial detection**: When was the bug first reported or noticed?
- **Detection method**: User report, automated test, code review, production incident?
- **Time to detection**: How long between introduction and discovery?
- **Severity assessment**: How was the bug initially classified?

### 4. Analyze Fix Attempts

Chronicle all attempts to fix the bug:

**For each fix attempt:**
- Commit hash and date
- Author and reviewer
- Fix approach and code changes
- Test coverage added
- Whether the fix was successful or reverted

**Identify patterns:**
- Multiple fix attempts indicate complexity
- Reverted fixes suggest incomplete understanding
- Test additions show learning from the bug

### 5. Check for Regressions

Identify if the bug reappeared after being fixed:

- Search for related bug reports after the fix
- Check if the fix was reverted or modified
- Look for similar bugs in related code
- Analyze if the bug reoccurred in different contexts

### 6. Generate Summary Report

Create a structured timeline and analysis:

**Timeline format:**
```markdown
## Bug History: [Bug Title/ID]

### Introduction
- **When**: [Date/Commit]
- **Where**: [File:Line]
- **How**: [Description of introducing change]
- **Context**: [Why the change was made]

### Detection
- **Discovered**: [Date]
- **Method**: [How it was found]
- **Time to Detection**: [Duration]
- **Initial Impact**: [Severity/Scope]

### Fix Attempts
1. **Attempt 1** ([Date/Commit])
   - Approach: [Description]
   - Outcome: [Success/Failure/Partial]
   - Tests Added: [Yes/No]

2. **Attempt 2** ([Date/Commit])
   - ...

### Regressions
- **Regression 1** ([Date])
  - Cause: [Why it reappeared]
  - Fix: [How it was resolved]

### Current Status
- [Fixed/Open/Recurring]
- Last modified: [Date]

### Lessons Learned
- [Key insights from the bug's history]
```

## Example

**Input:**
- Repository: `myapp`
- Bug: "Null pointer exception in user login"
- Issue: #456

**Analysis Process:**

1. **Git blame** shows the problematic code was added in commit `abc123` on 2024-01-15
2. **Commit analysis** reveals it was part of a refactoring to improve performance
3. **Issue tracker** shows bug reported on 2024-02-20 (36 days after introduction)
4. **Fix attempts**:
   - First fix (commit `def456`, 2024-02-21): Added null check, but incomplete
   - Second fix (commit `ghi789`, 2024-02-25): Comprehensive fix with tests
5. **Regression check**: No regressions found

**Generated Summary:**

```markdown
## Bug History: Null Pointer Exception in User Login (#456)

### Introduction
- **When**: 2024-01-15 (commit abc123)
- **Where**: src/auth/LoginHandler.java:45
- **How**: Refactoring removed null check during performance optimization
- **Context**: Part of PR #234 to reduce login latency

### Detection
- **Discovered**: 2024-02-20
- **Method**: Production incident report
- **Time to Detection**: 36 days
- **Initial Impact**: High severity - blocking user logins

### Fix Attempts
1. **Attempt 1** (2024-02-21, commit def456)
   - Approach: Added null check for user object
   - Outcome: Partial - fixed main case but missed edge case
   - Tests Added: Yes (1 unit test)

2. **Attempt 2** (2024-02-25, commit ghi789)
   - Approach: Comprehensive null handling with validation
   - Outcome: Success
   - Tests Added: Yes (3 unit tests + 1 integration test)

### Regressions
- None detected

### Current Status
- Fixed (as of 2024-02-25)
- Last modified: commit ghi789

### Lessons Learned
- Performance optimizations should maintain defensive checks
- Initial fix was too narrow - comprehensive testing revealed edge cases
- Added regression tests to prevent reintroduction
```

## Output Format

Provide:

1. **Structured timeline** in Markdown format
2. **Key metrics**:
   - Time to detection
   - Number of fix attempts
   - Time to resolution
   - Regression count
3. **Visual timeline** (optional, using ASCII or Mermaid):
   ```
   2024-01-15: Bug introduced (commit abc123)
        |
        | (36 days)
        |
   2024-02-20: Bug detected (issue #456)
        |
        | (1 day)
        |
   2024-02-21: Fix attempt 1 (partial)
        |
        | (4 days)
        |
   2024-02-25: Fix attempt 2 (success)
   ```
4. **Lessons learned** and recommendations

## Git Commands Reference

Useful commands for bug history analysis:

```bash
# Find when a line was introduced
git blame <file>

# Find the commit that introduced a bug
git bisect start
git bisect bad <bad-commit>
git bisect good <good-commit>

# Search commit messages for bug references
git log --grep="<bug-id>" --oneline

# Show commits that modified a specific file
git log --follow -- <file>

# Show commits in a date range
git log --since="2024-01-01" --until="2024-12-31"

# Find commits by author
git log --author="<name>"

# Show detailed commit information
git show <commit-hash>
```

## Tips for Effective Bug History Analysis

1. **Start with the fix** - Work backwards from the fix commit to understand the bug
2. **Check related files** - Bugs often span multiple files
3. **Read commit messages** - They provide context about intent
4. **Review pull requests** - Comments reveal decision-making
5. **Check test history** - Tests added after bugs show learning
6. **Look for patterns** - Similar bugs may have related causes
7. **Consider context** - Deadlines, team changes, and technical debt affect bug introduction
