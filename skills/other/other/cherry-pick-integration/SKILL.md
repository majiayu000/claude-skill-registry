---
name: vibe-cherry-pick-integration
description: Safely integrates commits from parallel agent branches using sequential cherry-pick. Use after parallel work completes in isolated branches or worktrees.
user-invocable: true
---

# vibe-cherry-pick-integration

Parallel agents produce parallel branches. This skill integrates them safely without merge conflicts destroying work.

## When to Use This Skill

- Multiple agents completed work in isolated branches/worktrees
- Need to combine parallel work onto a single integration branch
- After `vibe-parallel-task-decomposition` dispatched work

## When NOT to Use This Skill

- Single branch with sequential work (just push)
- Merge conflicts are expected and desired for resolution
- The parallel work was all in the same files (this won't help — resolve manually)

## Steps

1. **Inventory branches** — List all branches with completed work:
   ```bash
   git branch --list 'worktree-*' 'feature/*'
   ```

2. **Determine integration order** — Cherry-pick in dependency order:
   - Independent tasks first (any order within batch)
   - Dependent tasks after their dependencies

3. **For each branch**:
   a. Identify commits to cherry-pick: `git log main..branch-name --oneline`
   b. Cherry-pick onto integration branch: `git cherry-pick <commit-hash>`
   c. If conflict:
      - Examine both sides
      - Resolve keeping the semantic intent of both
      - `git cherry-pick --continue`
   d. Run tests after each cherry-pick: `[test command]`
   e. If tests fail: fix before proceeding to next branch

4. **Verify integration** — Run full test suite after all cherry-picks

5. **Clean up** — Remove integrated branches if desired

## Output Format

### Cherry-Pick Integration

**Branches integrated**: X
**Commits cherry-picked**: Y
**Conflicts resolved**: Z
**Tests**: PASS/FAIL after integration

| Branch | Commits | Conflicts | Tests After |
|--------|---------|-----------|------------|
| worktree-abc | 3 | 0 | PASS |
| worktree-def | 2 | 1 | PASS |

### Conflict Resolutions
1. [File]: [How it was resolved]

### Final Status
- All tests passing: Yes/No
- Integration branch: [name]
- Ready to merge: Yes/No
