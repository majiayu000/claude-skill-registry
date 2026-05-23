---
name: gh-implement-issue
description: "End-to-end implementation workflow for a GitHub issue from planning through PR creation. Use when starting work on an issue from scratch."
category: github
agent: implementation-specialist
---

# Implement GitHub Issue

Complete workflow for implementing a GitHub issue from start to finish.

## When to Use

- Starting work on a new issue
- Need structured workflow from branch to PR
- Want to follow best practices end-to-end
- Working on assigned GitHub issue

## Quick Reference

```bash
# 1. Fetch issue and create branch
gh issue view <issue>
git checkout -b <issue>-<description>

# 2. Implement with TDD
# - Write tests first
# - Implement code
# - Run tests: mojo test tests/

# 3. Quality checks
just pre-commit-all

# 4. Commit and PR
git add . && git commit -m "feat: description

Closes #<issue>"
git push -u origin <branch>
gh pr create --issue <issue>
```

## Workflow

1. **Read issue context**: `gh issue view <issue> --comments` - understand requirements, prior context
2. **Create branch**: `git checkout -b <issue>-<description>`
3. **Post start comment**: Document approach on the issue
4. **Write tests first**: TDD approach - tests drive implementation
5. **Implement code**: Build functionality to pass tests
6. **Quality check**: Format code and run pre-commit
7. **Commit**: Create focused commit with issue reference
8. **Push and PR**: Create PR linked to issue
9. **Post completion**: Document summary on the issue
10. **Monitor CI**: Verify all checks pass

## Branch Naming Convention

Format: `<issue-number>-<description>`

Examples:

- `42-add-tensor-ops`
- `73-fix-memory-leak`
- `105-update-docs`

## Commit Message Format

Follow conventional commits:

```text
type(scope): Brief description

Detailed explanation of changes.

Closes #<issue-number>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Code Quality Checklist

Before creating PR:

- [ ] Issue requirements met
- [ ] Tests written and passing
- [ ] Code formatted (pixi run mojo format)
- [ ] Pre-commit hooks pass
- [ ] No warnings or unused variables
- [ ] Documentation updated
- [ ] Commit messages follow convention

## Error Handling

| Problem | Solution |
|---------|----------|
| Issue not found | Verify issue number |
| Branch exists | Use different name or delete old branch |
| Tests fail | Fix code before creating PR |
| CI fails | Address issues before merge |

## Documentation Requirements

Post documentation directly to the GitHub issue:

```bash
# Post implementation started
gh issue comment <issue> --body "$(cat <<'EOF'
## Implementation Started

**Branch**: `<branch-name>`

### Approach
[Brief description of implementation approach]

### Files to Modify
- `path/to/file1.mojo`
- `path/to/file2.mojo`
EOF
)"

# Post completion summary
gh issue comment <issue> --body "$(cat <<'EOF'
## Implementation Complete

**PR**: #<pr-number>

### Summary
[What was implemented]

### Verification
- [x] Tests pass
- [x] Pre-commit passes
EOF
)"
```

## References

- See CLAUDE.md for complete development workflow
- See CLAUDE.md for Mojo syntax standards
- See CLAUDE.md for zero-warnings policy
