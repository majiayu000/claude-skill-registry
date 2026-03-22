---
name: implementing-issues
description: Implement a GitHub or Linear issue end-to-end with TDD, branch management, and PR creation. Use when implementing an issue, working on a ticket, starting a feature from an issue, or building from issue requirements.
argument-hint: "<issue number, #number, or TEAM-ID>"
---

# Implementing Issues

Work through an issue with TDD, proper branch management, and PR creation.

## Workflow

1. **Auto-detect VCS** -- `jj root` succeeds -> jj, otherwise git
2. **Auto-detect issue tracking** -- numeric/#number -> GitHub (gh), TEAM-ID format -> Linear (linear-cli)
3. **Check working copy status** -- ensure not on main/master/dev
4. **Create feature branch** with proper naming
5. **Read and understand issue requirements**
6. **Review project context** -- spec.md, requirements.md, CLAUDE.md
7. **Follow TDD** -- write tests first
8. **Implement minimal code** to pass tests
9. **Refactor incrementally** while maintaining coverage
10. **Clean up history** -- squash/curate commits
11. **Push with upstream tracking** and create PR
12. **Write complete PR description** with test plan

## Branch Naming

- **GitHub**: `feature/issue-{number}-{short-description}` or `fix/issue-{number}-{description}`
- **Linear**: `feature/{team-id}-{short-description}` or `fix/{team-id}-{description}`

## Branch Safety

**jj**:

```bash
jj log -r @ --no-graph -T 'bookmarks'
# If on main, create new change:
jj new main -m "feat: description"
jj git fetch
```

**git**:

```bash
git branch --show-current
# If on protected branch, create feature branch:
git checkout -b "feature/issue-<number>-<description>"
git fetch origin
```

## Implementation Standards

- Write failing tests first capturing acceptance criteria
- Implement minimal code to make tests pass
- Refactor while maintaining green tests
- Follow project patterns from CLAUDE.md
- Add meaningful comments for complex logic
- Update docs if public APIs change

## Push and PR

**jj**:

```bash
jj squash -m "feat: final commit message"
jj bookmark set <branch> -r @
jj git push --bookmark <branch>
```

**git**:

```bash
git push -u origin HEAD
```

**PR creation**:

```bash
gh pr create --title "[Issue #<number>] Title" --body "$(cat <<'EOF'
## Summary
<bullets>

## Test plan
- [ ] Tests pass
- [ ] Manual verification
EOF
)"
```

## Command Reference

```bash
# GitHub
gh issue view <number> --json title,body,labels,assignees,milestone
gh pr create --title "title" --body "body"

# Linear
linear-cli issues
linear-cli issue <team-id>
```
