---
name: reviewing-pull-requests
description: Review a pull request against issue requirements and coding best practices, then submit structured feedback. Use when reviewing a PR, checking a pull request, doing code review, or providing PR feedback.
argument-hint: "<PR number or URL>"
---

# Reviewing Pull Requests

Review pull requests against issue requirements and good coding practices.

## Workflow

1. **Auto-detect tracking system** -- GitHub PR (gh CLI) or Linear-linked PR (linear-cli)
2. **Read the pull request** -- changes, scope, implementation approach
3. **Find related issue/ticket** for acceptance criteria and original requirements
4. **Ensure latest code context** -- pull changes and verify working directory state
5. **Review project documentation** -- check `docs/`, `spec.md`, `requirements.md`, `CLAUDE.md`
6. **Analyze implementation quality** -- code structure, patterns, maintainability
7. **Verify test coverage** -- ensure complete testing of new functionality
8. **Check style compliance** -- validate against project guidelines
9. **Assess scope adherence** -- confirm changes are minimal and focused
10. **Determine review action** -- self-authored (comment) vs external (formal review)
11. **Submit structured feedback**

## Review Framework

### Requirements Alignment

- All acceptance criteria met
- No scope creep beyond original ticket
- Edge cases and error handling covered

### Code Quality

- Follows established patterns from codebase
- Single Responsibility, DRY compliance
- Adequate comments for complex logic
- No obvious performance bottlenecks

### Test Coverage

- All new functionality has corresponding tests
- Error scenarios and edge cases tested
- Integration with existing system validated

### Implementation Standards

- Clean commit history
- Smallest necessary changes
- No breaking changes without justification
- Input validation, no credentials exposure

## Review Output

### Requirements Coverage

- What criteria are met, partially met, or missing

### Code Quality

- Architecture adherence, pattern consistency, docs, performance

### Test Assessment

- Coverage verification, edge case testing, integration validation

### Final Recommendation

- **Approve**: Ready for merge
- **Request Changes**: Specific issues listed
- **Comment**: Self-authored PR feedback

## Command Reference

```bash
# View PR with full details
gh pr view <number> --json title,body,author,commits,files,comments,reviews

# Get diff
gh pr diff <number>

# View related issue
gh issue view <number> --json title,body,labels,assignees

# Submit review
gh pr review <number> --approve|--request-changes|--comment

# Linear integration
linear-cli issues
linear-cli issue <team-id>
```
