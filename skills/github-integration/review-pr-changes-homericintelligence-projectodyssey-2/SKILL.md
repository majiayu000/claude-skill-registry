---
name: review-pr-changes
description: "Review PR changes with structured checklist for quality and standards compliance. Use for comprehensive PR code review."
category: review
agent: test-engineer
user-invocable: false
---

# Review PR Changes with Checklist

Perform structured review of PR changes against project quality standards.

## When to Use

- Code review before approving PR
- Detailed evaluation of code quality
- Checking standards compliance (Mojo, Python, documentation)
- Verifying test coverage
- Assessing architectural impact

## Quick Reference

```bash
# Get PR files changed
gh pr diff <pr> --name-only

# View specific file diff
gh pr diff <pr> -- path/to/file.mojo

# Get PR review status
gh pr view <pr> --json reviews

# Check file statistics
gh pr diff <pr> | diffstat

# Get PR body/description
gh pr view <pr> --json body
```

## Review Checklist

**Code Quality**:

- [ ] Code is readable and well-structured
- [ ] Functions/classes have clear purposes
- [ ] Variable names are descriptive
- [ ] Complex logic is commented
- [ ] No code duplication (DRY principle)
- [ ] Follows project naming conventions

**Testing**:

- [ ] Tests present for new functionality
- [ ] Tests are passing (CI shows green)
- [ ] Edge cases covered in tests
- [ ] Test names describe what they test
- [ ] No skipped or xfail tests
- [ ] Adequate coverage for changes

**Documentation**:

- [ ] Docstrings for public APIs
- [ ] README updated if needed
- [ ] Comments for non-obvious code
- [ ] Examples provided for complex features
- [ ] Type hints present (Mojo/Python)

**Standards Compliance**:

- [ ] Mojo code uses v0.26.1+ syntax
- [ ] No deprecated patterns (inout, @value, DynamicVector)
- [ ] Zero compiler warnings
- [ ] Proper indentation and formatting
- [ ] No trailing whitespace
- [ ] Files end with newline

**Mojo-Specific**:

- [ ] Constructors use `out self` not `mut self`
- [ ] Non-copyable returns use `^` transfer operator
- [ ] Proper trait conformances on structs
- [ ] Memory safety validated
- [ ] SIMD used for performance-critical code
- [ ] Ownership patterns correct

**Security & Safety**:

- [ ] No hardcoded secrets/tokens
- [ ] Input validation present
- [ ] No unsafe operations
- [ ] Proper error handling
- [ ] No memory safety issues
- [ ] No type safety violations

**Git & Commit**:

- [ ] PR linked to issue (in description)
- [ ] Commit messages follow conventional commits
- [ ] No unintended files included
- [ ] Branch is up to date with main
- [ ] No merge conflicts

## Review Workflow

1. **Check context**: View PR description and linked issue
2. **Scan changes**: Review file list and statistics
3. **Read code**: Examine actual changes carefully
4. **Run checklist**: Go through each category
5. **Test locally**: Pull and test changes if needed
6. **Create comments**: Flag issues as code comments
7. **Provide verdict**: Approve, request changes, or comment

## Output Format

Report review results with sections:

1. **Summary** - Overall assessment of changes
2. **Strengths** - Well-executed aspects
3. **Issues Found** - Problems that must be fixed
4. **Suggestions** - Optional improvements
5. **Questions** - Clarifications needed
6. **Verdict** - Approve/Request Changes/Comment
7. **Next Steps** - What needs to happen next

## Common Issues to Flag

**Code Issues**:

- Logic errors or off-by-one mistakes
- Missing error handling
- Performance problems
- Unnecessary complexity

**Style Issues**:

- Inconsistent formatting
- Poor naming choices
- Missing comments
- Overly long functions/files

**Test Issues**:

- Missing test coverage
- Flaky tests
- Inadequate assertions
- Wrong expected values

**Documentation Issues**:

- Missing docstrings
- Inaccurate documentation
- Examples that don't work
- Missing type annotations

## Error Handling

| Problem | Solution |
|---------|----------|
| Can't access PR | Check gh auth status |
| Can't understand code | Ask clarifying question in comment |
| Needs local testing | Use worktree-create skill to test |
| Multiple issues | Prioritize critical first, optional second |
| Disagreement on style | Refer to CLAUDE.md for standards |

## Review Standards

Approve when:

- All critical issues fixed
- Code follows project standards
- Tests passing and coverage good
- Documentation complete
- No security/safety concerns

Request changes when:

- Critical issues present
- Standards not followed
- Missing tests
- Significant problems found

Comment when:

- Only minor suggestions
- Questions about approach
- Suggestions for improvement

## References

- See CLAUDE.md for project standards
- See verify-pr-ready for merge readiness check
- See gh-batch-merge-by-labels for batch review workflow
