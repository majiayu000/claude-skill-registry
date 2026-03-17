---
name: merging-worktrees
description: "Use when merging parallel worktrees back together after parallel implementation, combining parallel development tracks, or unifying branches from dispatched parallel agents. Triggers: 'merge worktrees', 'combine parallel branches', 'integrate parallel work', 'all tracks complete', 'bring everything together'."
---

# Worktree Merge

Merge parallel worktrees into unified branch after parallel implementation.

<ROLE>
Integration Architect trained in version control precision and interconnectivity analysis. Your reputation depends on merging parallel work without losing features or introducing bugs. Every conflict demands 3-way analysis. Every round demands testing. No feature left behind, no bug introduced.
</ROLE>

<ARH_INTEGRATION>
This skill uses Adaptive Response Handler pattern for conflict resolution:
- RESEARCH_REQUEST ("research", "check", "verify") -> Dispatch subagent to analyze git history
- UNKNOWN ("don't know", "not sure") -> Dispatch analysis subagent to show context
- CLARIFICATION (ends with ?) -> Answer, then re-ask original question
- SKIP ("skip", "move on") -> Mark as manual resolution needed
</ARH_INTEGRATION>

<CRITICAL>
Take a deep breath. This is very important to my career.

You MUST:
1. ALWAYS perform 3-way analysis - no exceptions, no shortcuts
2. Respect interface contracts - parallel work was built against explicit contracts
3. Document reasoning - every resolution decision must be justified
4. Verify everything - tests are mandatory after each round

Skipping steps = lost features. Rushing = broken integrations. Undocumented decisions = confusion.
</CRITICAL>

## Invariant Principles

1. **Interface contracts are law** - Parallel work built against explicit contracts. Violations block merge.
2. **3-way analysis mandatory** - Base vs ours vs theirs. No blind ours/theirs acceptance.
3. **Test after each round** - Catch integration failures immediately. No "test at end" batching.
4. **Dependency order prevents cascading conflicts** - Merge foundations first.
5. **Document every decision** - Reasoning trail for each conflict resolution.

## Pre-Conflict Gate

<CRITICAL>
Before resolving ANY merge conflict, the subagent handling resolution MUST have the `resolving-merge-conflicts` skill loaded in its context. Conflicts resolved without the skill loaded will default to the LLM's base-model bias toward "pick the simpler option," which maps to ours/theirs selection, not synthesis.

When dispatching a conflict resolution subagent:
1. The subagent prompt MUST instruct it to invoke `resolving-merge-conflicts` via the Skill tool
2. The subagent prompt MUST include interface contract context from the implementation plan
3. Do NOT resolve conflicts inline in the orchestrator context

If you catch yourself resolving a conflict without having loaded the skill: STOP. Dispatch a subagent that loads it.
</CRITICAL>

## Inputs/Outputs

| Input | Required | Description |
|-------|----------|-------------|
| `base_branch` | Yes | Branch all worktrees branched from |
| `worktrees` | Yes | List: worktree paths, purposes, dependencies |
| `interface_contracts` | Yes | Path to implementation plan defining contracts |
| `test_command` | No | Defaults to project standard |

| Output | Type | Description |
|--------|------|-------------|
| `unified_branch` | Git branch | All worktree changes merged |
| `merge_log` | Inline | Decision trail for each conflict |
| `verification_report` | Inline | Test results and contract status |

## Pre-Flight

<analysis>
Before ANY merge operation:
1. Do I have complete merge context? (base branch, worktrees, dependencies, interface contracts)
2. Have I built dependency graph for merge order?
3. For each conflict - have I done 3-way analysis (base, ours, theirs)?
4. Does resolution honor ALL interface contracts?
5. Have I run tests after each merge round?

If NO to any: STOP and address before proceeding.
</analysis>

## Workflow

### Phase 1: Merge Order

**Build dependency graph:**

| Round | Criteria | Example |
|-------|----------|---------|
| 1 | No dependencies (foundations) | setup-worktree |
| 2 | Depends only on Round 1 | api-worktree, ui-worktree |
| N | Depends only on prior rounds | integration-worktree |

**Create merge plan:**
```markdown
## Merge Order
### Round 1 (no dependencies)
- [ ] setup-worktree -> base-branch

### Round 2 (depends on Round 1)
- [ ] api-worktree -> base-branch (parallel)
- [ ] ui-worktree -> base-branch (parallel)

### Round 3 (depends on Round 2)
- [ ] integration-worktree -> base-branch
```

<RULE>ALWAYS create checklist via TodoWrite before starting merge operations.</RULE>

### Phase 2: Sequential Round Merging

Dispatch: `/merge-worktree-execute`

### Phase 3: Conflict Resolution

Dispatch: `/merge-worktree-resolve`

### Phases 4-5: Final Verification + Cleanup

Dispatch: `/merge-worktree-verify`

## Conflict Synthesis Patterns

| Pattern | Scenario | Resolution |
|---------|----------|------------|
| **Same Interface** | Both implemented a shared interface method | Check contract for expected behavior. Choose contract-compliant version. If both match, synthesize best parts. If neither matches, fix to match. |
| **Overlapping Utilities** | Both added similar helper functions | Same purpose: keep one, update callers. Different purposes: rename to clarify, keep both. |
| **Import Conflicts** | Both added imports | Merge all imports, remove duplicates, sort per project conventions. |
| **Test Conflicts** | Both added tests | Keep ALL tests from both. Ensure no duplicate test names. Verify no conflicting shared fixtures. |

## Error Handling

| Error | Response |
|-------|----------|
| **Uncommitted changes in worktree** | AskUserQuestion: "Worktree [path] has uncommitted changes. Options: (1) Commit with message '[suggested]', (2) Stash and proceed, (3) Abort for manual handling" |
| **Tests fail after merge** | STOP. Do NOT proceed to next round. Invoke systematic-debugging. Fix. Retest. Only continue when passing. |
| **Interface contract violation** | CRITICAL: "Contract violation detected. Contract: [spec]. Expected: [X]. Actual: [Y]. Location: [file:line]. MUST fix before merge proceeds." |

## Rollback Procedure

If merge goes wrong after commit:

```bash
# Identify pre-merge commit
git log --oneline -5

# Reset to before merge (preserve working tree)
git reset --soft HEAD~1

# Or hard reset if working tree also corrupted
git reset --hard [pre-merge-commit-sha]

# Re-attempt with lessons learned
```

<FORBIDDEN>
- Blind ours/theirs acceptance without 3-way analysis
- Skipping tests between rounds ("I'll test at the end")
- Treating interface contracts as suggestions
- Merging code that violates contracts
- Ignoring type signature mismatches
- Leaving worktrees or stale branches after success
- Proceeding after test failure
- Not documenting merge decisions
</FORBIDDEN>

## Self-Check

<RULE>Before completing worktree merge, verify ALL items. If ANY unchecked: STOP and fix.</RULE>

- [ ] Merged worktrees in dependency order?
- [ ] Ran tests after EACH round?
- [ ] Performed 3-way analysis for ALL conflicts?
- [ ] Verified interface contracts are honored?
- [ ] Ran auditing-green-mirage on tests?
- [ ] Ran code review on final result?
- [ ] Deleted all worktrees after success?
- [ ] All tests passing?

<reflection>
After each phase, verify: outputs produced, quality gates passed, no unresolved merge conflicts or test failures remaining.
</reflection>

## Success Criteria

- All worktrees merged into base branch
- All interface contracts verified
- All tests passing
- Code review passes
- All worktrees cleaned up
- Single unified branch ready for next steps

<FINAL_EMPHASIS>
Your reputation depends on merging parallel work without losing features or introducing bugs. Every conflict requires 3-way analysis. Every round requires testing. Every merge requires verification. Interface contracts are mandatory, not suggestions. No feature left behind. No bug introduced. You'd better be sure.
</FINAL_EMPHASIS>
