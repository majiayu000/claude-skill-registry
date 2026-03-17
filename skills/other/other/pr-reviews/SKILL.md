---
name: pr-reviews
description: Comprehensive pull request review using specialized agents covering code quality, test coverage, error handling, type design, comment accuracy, and code simplification. Use when reviewing PRs, checking code before committing, validating changes before creating PRs, or when the user asks to "review my PR", "check the code", "review changes", "analyze test coverage", "check error handling", "review types", or "simplify the code". Supports targeted reviews (tests, errors, types, comments, code, simplify) or full review (all aspects).
---

# PR Reviews

Run comprehensive pull request reviews using specialized agents, each analyzing a different aspect of code quality.

## Review Aspects

| Aspect | Agent | Focus |
|--------|-------|-------|
| `code` | code-reviewer | Project guidelines, bugs, code quality |
| `tests` | test-analyzer | Test coverage quality and completeness |
| `errors` | silent-failure-hunter | Silent failures, error handling |
| `types` | type-design-analyzer | Type encapsulation and invariants |
| `comments` | comment-analyzer | Comment accuracy and maintainability |
| `simplify` | code-simplifier | Clarity and maintainability |
| `all` | All applicable | Full review (default) |

## Workflow

1. **Determine scope** - Check `git diff --name-only` for changed files
2. **Select aspects** - Parse user request or default to all applicable
3. **Launch agents** - Sequential (default) or parallel (if requested)
4. **Aggregate results** - Combine findings by severity
5. **Provide action plan** - Prioritized fixes

## Usage

**Full review:**
```
/pr-reviews
```

**Targeted reviews:**
```
/pr-reviews tests errors    # Test coverage and error handling only
/pr-reviews comments        # Comment accuracy only
/pr-reviews simplify        # Code simplification only
```

**Parallel execution:**
```
/pr-reviews all parallel    # Launch all agents simultaneously
```

## Applicability by Change Type

| Change Type | Applicable Agents |
|-------------|-------------------|
| Any code | code-reviewer (always) |
| Test files | test-analyzer |
| Comments/docs | comment-analyzer |
| Error handling | silent-failure-hunter |
| New/modified types | type-design-analyzer |
| After passing review | code-simplifier |

## Output Format

```markdown
# PR Review Summary

## Critical Issues (X found)
- [agent-name]: Issue description [file:line]

## Important Issues (X found)
- [agent-name]: Issue description [file:line]

## Suggestions (X found)
- [agent-name]: Suggestion [file:line]

## Strengths
- What's well-done in this PR

## Recommended Action
1. Fix critical issues first
2. Address important issues
3. Consider suggestions
4. Re-run review after fixes
```

## Agent Details

See references for detailed agent specifications:
- [code-reviewer.md](references/code-reviewer.md) - Guidelines compliance and bug detection
- [test-analyzer.md](references/test-analyzer.md) - Behavioral coverage analysis
- [silent-failure-hunter.md](references/silent-failure-hunter.md) - Error handling audit
- [type-design-analyzer.md](references/type-design-analyzer.md) - Type invariant analysis
- [comment-analyzer.md](references/comment-analyzer.md) - Comment accuracy verification
- [code-simplifier.md](references/code-simplifier.md) - Code clarity refinement

## Workflow Integration

**Before committing:**
1. Write code
2. Run: `/pr-reviews code errors`
3. Fix critical issues
4. Commit

**Before creating PR:**
1. Stage changes
2. Run: `/pr-reviews all`
3. Address critical and important issues
4. Re-run targeted reviews
5. Create PR

**After PR feedback:**
1. Make requested changes
2. Run targeted reviews based on feedback
3. Verify issues resolved
4. Push updates

## Tips

- **Run early** - Review before creating PR, not after
- **Focus on changes** - Agents analyze git diff by default
- **Address critical first** - Fix high-priority issues before lower priority
- **Re-run after fixes** - Verify issues are resolved
- **Use targeted reviews** - Focus on specific aspects when you know the concern
