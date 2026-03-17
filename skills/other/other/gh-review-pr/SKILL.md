---
name: gh-review-pr
description: "Comprehensively review a pull request including code changes, CI status, and adherence to project standards. Use when asked to review a PR."
category: github
agent: code-review-orchestrator
---

# Review Pull Request

Evaluate PR quality and provide structured feedback.

## When to Use

- Reviewing a PR before merge
- Evaluating code quality and standards
- Checking CI status and test coverage
- Providing feedback to contributors

## Quick Reference

```bash
# View PR details
gh pr view <pr>

# Check diff
gh pr diff <pr> | less

# View CI status
gh pr checks <pr>

# See review comments
gh api repos/OWNER/REPO/pulls/PR/comments
```

## Review Checklist

- [ ] Code follows project standards (CLAUDE.md)
- [ ] All CI checks passing
- [ ] Tests are present and passing
- [ ] PR is linked to issue
- [ ] Commit messages follow conventional commits
- [ ] No security vulnerabilities
- [ ] Documentation updated if needed
- [ ] No unintended files included

## Workflow

1. **Get PR info**: `gh pr view <pr>`
2. **Review diff**: `gh pr diff <pr>`
3. **Check CI**: `gh pr checks <pr>`
4. **Analyze code**: Focus on quality, standards, tests
5. **Assess security**: Look for vulnerabilities
6. **Verify docs**: Check if documentation updated
7. **Provide feedback**: Comment with findings

## Review Focus Areas

**Code Quality**:

- Clean, readable, maintainable
- Follows CLAUDE.md guidelines
- Proper error handling
- No code duplication

**Testing**:

- Tests present for new code
- Tests passing
- Adequate coverage
- Edge cases covered

**Documentation**:

- API documentation updated
- Complex logic explained
- README updated if needed
- Examples provided if applicable

**Standards Compliance**:

- Mojo syntax correct (for Mojo code)
- No warnings or unused variables
- Proper formatting
- Conventional commit messages

## Output Format

Provide review with sections:

1. **Summary** - Overall assessment
2. **Strengths** - What's done well
3. **Issues** - Problems that must be fixed
4. **Suggestions** - Optional improvements
5. **Verdict** - Approve / Request Changes / Comment

## Error Handling

| Problem | Solution |
|---------|----------|
| PR not found | Verify PR number |
| Auth failure | Check `gh auth status` |
| CI pending | Note review based on current state |

## References

- See CLAUDE.md for project standards
- See CLAUDE.md for Mojo syntax requirements
- See CLAUDE.md for zero-warnings policy
