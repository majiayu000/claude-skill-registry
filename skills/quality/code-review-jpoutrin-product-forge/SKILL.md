---
name: code-review
description: Review code changes between commits for security, logic, performance, and style issues
argument-hint: "[<commit>] [--from <commit>] [--to <commit>]"
---

# code-review

**Category**: Development

## Usage

```bash
/code-review [<commit>] [--from <commit>] [--to <commit>]
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `<commit>` | - | Single commit to review |
| `--from` | merge-base with main | Starting commit reference |
| `--to` | HEAD | Ending commit reference |

## Examples

```bash
# Review all changes in current branch (from merge-base to HEAD)
/code-review

# Review a specific commit
/code-review abc1234

# Review a range of commits
/code-review --from abc1234 --to def5678

# Review changes since a specific commit
/code-review --from HEAD~5

# Review changes up to a specific commit
/code-review --to feature-branch
```

## Execution Method

This command delegates to the `code-review-expert` agent (Haiku model) for fast, cost-effective execution.

**Delegation**: Use the Task tool with:
- `subagent_type`: `"git-workflow:code-review-expert"`
- `model`: `"haiku"`
- `prompt`: Include the commit range and current working directory

Example:
```
Task(subagent_type="git-workflow:code-review-expert", model="haiku", prompt="Review changes from abc1234 to HEAD in /path/to/repo")
```

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Parse Arguments

```
SINGLE_COMMIT = first positional argument (if provided)
FROM = --from value or merge-base with main/master
TO = --to value or HEAD
```

If a single commit is provided:
- Review just that commit: `FROM = <commit>^`, `TO = <commit>`

If no arguments:
- FROM = merge-base with main (or master)
- TO = HEAD

### 2. Validate Commit References

```bash
# Verify commits exist
git rev-parse --verify "$FROM" 2>/dev/null
git rev-parse --verify "$TO" 2>/dev/null
```

If invalid, show error with suggestions.

### 3. Gather Change Information

```bash
# Get overview
git diff --stat $FROM..$TO

# Get commit history
git log --oneline $FROM..$TO

# Get full diff for analysis
git diff $FROM..$TO
```

### 4. Analyze Changes

Review each file's changes for:

**Critical Issues (must fix)**
- Security vulnerabilities (injection, XSS, auth bypass)
- Hardcoded secrets or credentials
- Data exposure risks

**High Priority (should fix)**
- Logic bugs and incorrect behavior
- Missing error handling
- Null reference issues
- Race conditions

**Medium Priority (consider fixing)**
- Performance issues (N+1 queries, inefficient loops)
- Code smells and maintainability issues
- Missing input validation

**Low Priority (optional)**
- Style inconsistencies
- Minor code improvements
- Documentation gaps

**Test Coverage**
- New code without corresponding tests
- Changed behavior without updated tests

### 5. Present Findings

Format output as:

```
Code Review: <from>..<to>
=========================

Files Changed: N (+X, -Y)
Commits: M

## Critical Issues
- [SECURITY] path/file.py:42 - SQL injection via unsanitized input

## High Priority
- [LOGIC] path/file.py:78 - Missing null check on user.profile

## Medium Priority
- [PERFORMANCE] path/file.py:120 - Queries in loop, consider batch fetch

## Low Priority
- [STYLE] path/file.py:15 - Inconsistent naming: userID vs user_id

## Test Coverage
- Missing tests for: new_feature() in path/file.py

## Suggestions
- Consider adding retry logic for external API calls

---
Overall: NEEDS_CHANGES | APPROVED_WITH_COMMENTS | APPROVED
```

### 6. Overall Assessment

- **NEEDS_CHANGES**: Critical or multiple high-priority issues found
- **APPROVED_WITH_COMMENTS**: Only medium/low issues, suggestions provided
- **APPROVED**: No significant issues found

## What to Review

| Category | Look For |
|----------|----------|
| Security | Injection, auth, secrets, data exposure |
| Logic | Bugs, error handling, edge cases |
| Performance | N+1 queries, inefficient algorithms |
| Style | Naming, consistency, complexity |
| Tests | Coverage, quality, edge cases |

## What NOT to Flag

- Subjective style preferences (unless inconsistent)
- Theoretical issues that can't happen in context
- Over-engineering suggestions
- Minor naming bikeshedding

## Error Handling

```
No changes to review
  The commits $FROM and $TO are identical.

Invalid commit reference
  Could not find commit: abc1234
  Try: git log --oneline -20

Not a git repository
  Navigate to a git repository first.
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/commit` | Create commits with conventional format |
| `/rebase` | Rebase local changes on remote |
