---
name: git-investigate
description: Code investigation knowledge base. Covers code history tracking, issue introduction analysis, root cause diagnosis.
allowed-tools: Bash(git:*), Read, Grep, Glob
---

# Git Investigate Skill

## Trigger

- Keywords: code history, git blame, track changes, who wrote this, when was it changed, root cause, code archaeology

## When NOT to Use

- Code review (use codex-review)
- Feature development (use feature-dev)
- Just want to read code (use Read directly)

## Command

```bash
/git-investigate src/service/xxx.ts:123      # Specific line
/git-investigate processToken                 # Function name
/git-investigate "error message"              # Keyword
```

## Workflow

```
Locate code -> git blame -> find commit -> trace history -> analyze changes -> report
```

## Investigation Framework

| Question           | Method                        |
| ------------------ | ----------------------------- |
| Who wrote it?      | `git blame`                   |
| When was it changed?| `git log --follow`           |
| Why was it changed?| commit message + PR           |
| What was missed?   | `git diff` compare original vs problematic version |

## Common Patterns

| Pattern            | Symptom              | Root Cause                    |
| ------------------ | -------------------- | ----------------------------- |
| Type removed       | Enum value deleted   | Assumed no longer needed      |
| Condition simplified| If conditions reduced| Missed during refactoring    |
| Rename             | Partially unchanged  | Incomplete search-and-replace |
| Boundary ignored   | Only handles main flow| Edge cases not considered    |

## Verification

- Report includes: investigation target, author info, timeline, original vs problematic code
- Root cause has clear analysis
- Fix recommendation is specific and actionable

## References

- `references/commands.md` - Git command reference + report template

## Examples

```
Input: Who changed this line of code?
Action: git blame -> find commit -> trace PR -> output report
```

```
Input: When was this bug introduced?
Action: git log -p -S -> locate introduction point -> analyze cause -> output report
```
