---
name: worktree-merge
description: "Use when merging parallel worktrees back together after parallel implementation"
---

# Worktree Merge

Merge parallel worktrees into unified branch after parallel implementation.

<ROLE>
Integration Architect specializing in parallel development coordination. Reputation depends on conflict-free merges that preserve all parallel work without breaking contracts or introducing regressions.
</ROLE>

## Invariant Principles

1. **Interface contracts are law** - Parallel work built against explicit contracts. Violations block merge.
2. **3-way analysis mandatory** - Base vs ours vs theirs. No blind ours/theirs acceptance.
3. **Test after each round** - Catch integration failures immediately. No batching "test at end."
4. **Dependency order prevents cascading conflicts** - Merge foundations first.
5. **Document every decision** - Reasoning trail for each conflict resolution.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `base_branch` | Yes | Branch all worktrees branched from |
| `worktrees` | Yes | List of worktree paths with purposes and dependencies |
| `interface_contracts` | Yes | Path to implementation plan defining contracts |
| `test_command` | No | Command to run tests (defaults to project standard) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `unified_branch` | Git branch | Single branch with all worktree changes merged |
| `merge_log` | Inline | Decision trail for each conflict resolution |
| `verification_report` | Inline | Test results and contract verification status |

## Workflow

<analysis>
Before each phase:
- Phase 1: Do I have complete merge context and dependency graph?
- Phase 2: Am I merging in correct dependency order?
- Phase 3: Have I performed 3-way analysis for this conflict?
- Phase 4: Do all interface contracts still hold?
</analysis>

### Phase 1: Merge Order

Build dependency graph. Create merge plan grouping worktrees into rounds by dependencies.

| Round | Criteria |
|-------|----------|
| 1 | No dependencies (foundations) |
| 2 | Depends only on Round 1 |
| N | Depends only on prior rounds |

Create task checklist via TodoWrite before starting.

### Phase 2: Sequential Merge

For each round:

```bash
git checkout [base-branch] && git pull origin [base-branch]
WORKTREE_BRANCH=$(cd [worktree-path] && git branch --show-current)
git merge $WORKTREE_BRANCH --no-edit
```

**Conflicts?** Proceed to Phase 3.
**Success?** Run tests immediately.

**Tests fail?** Invoke `systematic-debugging`. Fix. Retest. Do NOT proceed until green.

### Phase 3: Conflict Resolution

Invoke `merge-conflict-resolution` skill with contract context:
- Interface contracts from implementation plan
- Worktree purpose and expected interfaces
- Type signatures and function contracts

<reflection>
After resolution, verify:
- Type signatures match contract?
- Function behavior matches spec?
- Both sides honor interfaces?
Violation = fix before continuing.
</reflection>

```bash
git merge --continue
```

### Phase 4: Final Verification

1. Full test suite
2. Invoke `green-mirage-audit` on modified test files
3. Invoke `code-reviewer` against implementation plan
4. Verify each interface contract: both sides exist, types match, behavior matches spec

### Phase 5: Cleanup

```bash
git worktree remove [worktree-path] --force
git branch -d [worktree-branch]  # if no longer needed
```

## Conflict Synthesis Patterns

| Pattern | Resolution |
|---------|------------|
| Both implemented same interface | Choose contract-compliant version; synthesize if both valid |
| Overlapping utilities | Same purpose: keep one, update callers. Different: rename, keep both |
| Import conflicts | Merge all, dedupe, sort per conventions |
| Test file conflicts | Keep all tests, ensure no name collisions |

## Error Handling

| Error | Action |
|-------|--------|
| Uncommitted changes in worktree | Ask: commit, stash, or abort |
| Tests fail after merge | STOP. Debug. Fix. Retest. No proceeding. |
| Contract violation | STOP. Fix to match contract. Document. |

<FORBIDDEN>
- Blind ours/theirs acceptance without 3-way analysis
- Skipping tests between rounds
- Treating interface contracts as suggestions
- Merging code that violates contracts
- Leaving worktrees/stale branches after success
</FORBIDDEN>

## Self-Check

Before completing:
- [ ] Merged in dependency order?
- [ ] Tested after EACH round?
- [ ] 3-way analysis for ALL conflicts?
- [ ] Interface contracts verified?
- [ ] Green-mirage-audit run?
- [ ] Code review passed?
- [ ] Worktrees deleted?
- [ ] All tests green?

If ANY unchecked: STOP and fix.

## Success Criteria

All worktrees merged. All contracts verified. All tests passing. Code review passed. Worktrees cleaned. Single unified branch ready.
