---
name: branch-discipline
description: "Enforce one branch per issue, small focused commits, and clean git history. Use with /branch command."
---

# Branch Discipline

Principles for clean git history: one issue per branch, small commits, clear scope.

## Core Principles

### 1. One Branch = One Issue

Every branch addresses exactly ONE issue, feature, or bug fix.

```
✓ feature/123-fix-login-validation
✓ feature/456-add-user-export
✗ feature/misc-fixes              # Too vague
✗ feature/login-and-export        # Two issues
```

### 2. Small, Logical Commits

Each commit is a single logical change that could be reverted independently.

```
✓ "fix(#123): validate email format"
✓ "fix(#123): add error message for invalid email"
✓ "test(#123): add email validation tests"

✗ "fix stuff"
✗ "WIP"
✗ "fix login, add export, refactor auth"
```

### 3. Scope Discipline

If you find another issue while working:
1. **STOP** - don't fix it in this branch
2. **NOTE** - add to issue tracker or notes
3. **BRANCH** - create a separate branch later

```
Working on #123 (login validation)
Found #789 (password reset bug)

✗ Fix both in same branch
✓ Note #789, continue with #123, branch for #789 later
```

### 4. Worktrees for Parallel Work

Use git worktrees when you need to:
- Work on multiple issues simultaneously
- Context switch without stashing
- Run parallel agent tasks

```bash
# Main repo stays on main
/project/              # main branch

# Each issue gets its own worktree
/project-123/          # feature/123 branch
/project-456/          # feature/456 branch
```

## Workflow

### Starting Work

```
/branch [issue-id] [description]      # Create branch + checklist
/branch [issue-id] [description] -w   # + worktree for parallel work
```

**Then immediately:**
```
/mentor review requirements for #[id]: [description]
```

This catches unclear requirements and flawed approaches BEFORE you write code.
Record findings in the checklist.

### During Work

1. **Before each commit**, ask:
   - Is this change related to the issue?
   - Is this the smallest logical unit?
   - Does the commit message reference the issue?

2. **Incorporate mentor advice** from initial review

3. **Check progress:**
   ```
   /branch-status
   ```

4. **Found unrelated issue?**
   - Add to notes, don't fix now
   - Create separate branch later

### Before PR

```
/mentor review my implementation for #[id]
```

This catches blind spots and edge cases before team review.
Record findings in the checklist.

### Completing Work

```
/branch-done    # Verify checklist, create PR
```

## Commit Message Format

```
type(#issue): description

[optional body]
```

**Types:**
- `feat` - new feature
- `fix` - bug fix
- `refactor` - code restructure
- `test` - add/update tests
- `docs` - documentation
- `chore` - maintenance

**Examples:**
```
feat(#123): add email validation to login form
fix(#456): prevent duplicate user exports
refactor(#789): extract auth logic to service
test(#123): add unit tests for email validator
```

## Parallel Agent Work

When using multiple agents simultaneously:

### Setup
```bash
# Create worktrees for each agent/issue
git worktree add ../project-123 -b feature/123-task-a
git worktree add ../project-456 -b feature/456-task-b
git worktree add ../project-789 -b feature/789-task-c
```

### Assign Work
- Agent 1 → `../project-123/` → Issue #123
- Agent 2 → `../project-456/` → Issue #456
- Agent 3 → `../project-789/` → Issue #789

### Benefits
- No branch switching conflicts
- Independent commit histories
- Can merge in any order
- Easy to abandon failed experiments

### Cleanup
```bash
# After merging
git worktree remove ../project-123
git branch -d feature/123-task-a
```

## Anti-Patterns

### Big Bang Commits
```
✗ "implement user management"  # 50 files, 2000 lines
```
Break into:
```
✓ "feat(#100): add user model"
✓ "feat(#100): add user repository"
✓ "feat(#100): add user service"
✓ "feat(#100): add user controller"
✓ "test(#100): add user management tests"
```

### Scope Creep
```
✗ Branch for #123 contains fixes for #456 and #789
```
Keep branches focused:
```
✓ feature/123-login-fix     → only #123 changes
✓ feature/456-export-bug    → only #456 changes
✓ feature/789-auth-refactor → only #789 changes
```

### WIP Commits
```
✗ "WIP"
✗ "fix"
✗ "stuff"
```
Write meaningful messages:
```
✓ "fix(#123): handle null email input"
```

## Checklist Template

Each branch should have a checklist (created by `/branch`):

```markdown
# Issue #[ID]: [Description]

## Scope
- What this branch WILL do
- What this branch will NOT do

## Checklist

### Before Starting
- [ ] Requirements understood
- [ ] Mentor review: `/mentor review requirements for #[ID]`

### During Work
- [ ] Changes limited to scope
- [ ] Mentor advice incorporated
- [ ] Tests added

### Before PR
- [ ] Mentor review: `/mentor review implementation for #[ID]`
- [ ] Tests passing
- [ ] Commits logical (max 3-5)

## Mentor Reviews

### Initial (before starting)
**Findings:** [mentor feedback]
**Action:** [what you changed]

### Final (before PR)
**Findings:** [mentor feedback]
**Action:** [what you changed]

## Commits
| Hash | Message |
|------|---------|

## Out-of-Scope Issues Found
- #XXX: [description] - branch later
```

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/branch [id] [desc]` | Create focused branch + checklist |
| `/branch [id] [desc] -w` | + create worktree |
| `/branch-status` | Check progress on current branch |
| `/branch-done` | Complete branch, create PR |
| `/branch-list` | List all active branches/worktrees |

## Integration

Works with:
- `git-workflow` skill - general git practices
- `git-worktrees` skill - worktree details
- `code-review` skill - before merging
