---
name: run-issues
description: Autonomous issue management - fetches open GitHub issues, analyzes priorities, detects dependencies, spawns parallel subagents, and verifies results. Triggers: /run-issues, autonomous issues, batch issues, parallel issue processing.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Run Issues Skill

Autonomous workflow for processing multiple GitHub issues in parallel with priority-based scheduling and verification.

## Overview

This skill orchestrates the complete lifecycle of issue processing:
1. Fetch open issues from GitHub
2. Analyze and prioritize (P0 > P1 > P2)
3. Detect dependencies between issues
4. Spawn subagents for parallel execution
5. Verify all results before reporting

## When to Use

Use this skill when:
- User invokes `/run-issues`
- User requests batch processing of issues
- User wants autonomous issue handling
- Multiple issues need parallel processing

## Workflow

### Phase 0: Pre-Flight Check

**IMPORTANT**: Before starting, check if AWK principal workflow is active.

```bash
# Check for active AWK workflow
if [ -f ".ai/state/kickoff.lock" ]; then
    echo "⚠️ WARNING: AWK principal workflow is active"
fi
```

If `.ai/state/kickoff.lock` exists:
1. **Warn the user**:
   ```
   ⚠️ AWK principal workflow 正在執行中。
   同時執行 /run-issues 可能導致：
   - 同一 issue 被重複處理
   - 產生重複的 branch 或 PR
   - Merge conflicts

   建議：等待 AWK workflow 完成後再執行。
   確定要繼續嗎？(yes/no)
   ```
2. Only proceed if user explicitly confirms with "yes"
3. If user says "no", abort gracefully

If lock file does not exist, proceed to Phase 1.

### Phase 1: Fetch Issues

```bash
gh issue list --state open --json number,title,body,labels,assignees --limit 50
```

Parse the JSON output to get all open issues.

### Phase 2: Analyze Issues

**Read** `phases/analyze.md` for detailed priority analysis rules.

For each issue:
1. Extract priority from labels (P0/P1/P2)
2. Parse dependencies from issue body
3. Calculate priority score
4. Build dependency graph

### Phase 3: Plan Parallel Execution

**Read** `phases/parallelize.md` for parallelization strategy.

1. Group issues by dependency chains
2. Identify independent issue sets
3. Determine optimal subagent count (max 3 concurrent)
4. Create execution batches

### Phase 4: Execute

For each batch of independent issues:

1. Spawn subagents using Task tool:
   ```
   Task tool parameters:
   - subagent_type: general-purpose
   - description: "Work on Issue #<number>: <title>"
   - prompt: |
       Complete Issue #<number>. Requirements: <body excerpt>.

       CRITICAL - Follow .ai/rules/_kit/git-workflow.md strictly:

       Commit format:
       - Format: [type] subject
       - Subject MUST be lowercase (e.g., "add feature" not "Add feature")
       - NO colon after bracket
       - Valid types: feat, fix, docs, style, refactor, perf, test, chore

       Examples:
       ✅ [docs] update api reference
       ✅ [feat] add user authentication
       ❌ [Docs] Update API reference (uppercase = WRONG)
       ❌ docs: update api reference (colon = WRONG)

       PR requirements:
       - PR body MUST include: Closes #<number>
       - PR target: develop branch (or as specified)
   ```

2. Wait for all subagents in batch to complete

3. Move to next batch (respecting dependencies)

### Phase 5: Verify Results

**Read** `phases/verify.md` for verification checklist.

For each completed issue:
1. Check if PR was created
2. Validate commit format
3. Verify tests pass
4. Confirm branch is up-to-date

### Phase 6: Report

Generate summary table:

```markdown
| Issue | Title | Priority | Status | PR | Notes |
|-------|-------|----------|--------|-----|-------|
| #123  | Fix bug | P0 | Completed | #456 | Tests pass |
| #124  | Add feature | P1 | Completed | #457 | Ready for review |
| #125  | Update docs | P2 | Failed | - | Test failures |
```

## Error Handling

- If a subagent fails, log the error and continue with other issues
- Failed issues are marked in the final report
- Dependencies of failed issues are skipped with note

## Self-Check

On each phase entry, output:
```
[RUN-ISSUES] <timestamp> | <phase> | loaded: <filename>
```

## Integration with AWK Workflow

**⚠️ WARNING**: Do NOT run `/run-issues` and `awkit kickoff` simultaneously.

This skill processes GitHub issues independently of AWK's spec-driven workflow.
- AWK uses `tasks.md` specs → `awkit dispatch-worker`
- This skill fetches from GitHub → Task subagents

**Recommended workflow:**
```
/create-issues → issues created
        ↓
    Choose ONE:
        ├─ awkit kickoff (structured, spec-driven)
        └─ /run-issues (autonomous, batch processing)  ← this skill
```

## Quick Reference

| Phase | Action | File |
|-------|--------|------|
| Pre-Flight | Check AWK workflow not active | (inline) |
| Analyze | Determine priorities and dependencies | `phases/analyze.md` |
| Parallelize | Plan execution batches | `phases/parallelize.md` |
| Verify | Check completed work | `phases/verify.md` |
