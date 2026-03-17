---
name: pr-review
description: Comprehensive PR review using specialized agents. Use before creating or merging pull requests.
user-invocable: true
triggers:
  - pr
  - pr-review
  - review-pr
  - code-review
allowed-tools: Bash(gh *), Glob, Grep, Read, Task
model: opus
argument-hint: "[#PR-number] [--comment]"
---

# PR Review

Run comprehensive pull request review using specialized agents.

## Quick Start

```
Say: "review this PR" or "pr-review"
```

## Review Workflow

### 1. Check Review Scope

```bash
# See what changed
git diff --name-only

# Check if PR exists
gh pr view
```

### 2. Launch Review Agents (Parallel)

| Agent | Focus | Model |
|-------|-------|-------|
| **CLAUDE.md Compliance** | Project rules adherence | Sonnet |
| **Bug Hunter** | Logic errors, type issues | Opus |
| **Security Scanner** | Injection, XSS, secrets | Opus |
| **Test Coverage** | Missing test cases | Haiku |

### 3. Filter Results

**Only flag HIGH SIGNAL issues:**
- Code won't compile/parse
- Clear logic errors (wrong results regardless of input)
- Explicit CLAUDE.md violations (quote the rule)
- Security vulnerabilities with exploit path

**DON'T flag:**
- Style preferences
- Potential issues depending on state
- Things linter will catch
- Pre-existing issues

### 4. Report Format

```markdown
# PR Review Summary

## Critical Issues (must fix)
- [agent]: Issue description [file:line]

## Important Issues (should fix)
- [agent]: Issue description [file:line]

## Suggestions (nice to have)
- [agent]: Suggestion [file:line]

## Strengths
- What's well-done in this PR

## Action Plan
1. Fix critical issues first
2. Address important issues
3. Consider suggestions
```

## Usage Examples

**Full review:**
```
pr-review
```

**Review specific PR:**
```
pr-review #123
```

**Post comments to PR:**
```
pr-review --comment
```

## Integration with Other Skills

| When | Also Reference |
|------|----------------|
| Security issues found | `security` |
| Type issues found | `standards` |
| UI changes | `design` |
| Test gaps | `browser-auth` |

## Tips

- **Run before creating PR** - Catch issues early
- **Focus on diff** - Review changes, not entire codebase
- **Trust but verify** - Validate flagged issues before acting
- **Re-run after fixes** - Confirm issues resolved
