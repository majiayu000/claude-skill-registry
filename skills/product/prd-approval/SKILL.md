---
name: plan-approval
description: Human validation of complete plan (PRD + Stories + Execution Plan) before execution. User sees full picture then approves or requests changes. Required for complexity ≥15.
---

# Plan Approval Skill

> **ROOT AGENT ONLY** - Uses AskUserQuestion, runs only from root agent.

**Purpose:** Get human approval of complete plan AFTER design phase
**Trigger:** After design-phase completes (stories extracted, architect annotated, PM planned)
**Input:** prdPath, storiesFolder, storyFiles, executionPlan, complexity
**Output:** Approval status

---

## Why Approval Happens Here (Not Earlier)

User gets to see the **full picture** before committing:

1. ✅ PRD (requirements document)
2. ✅ User stories (broken down by functional capability)
3. ✅ Architecture annotations (on each story)
4. ✅ Execution plan (waves, parallelization, dependencies)

This is more useful than approving just the PRD, because:

- PRD alone doesn't show HOW implementation will happen
- Stories show actual work breakdown and parallelization
- Execution plan shows time investment and agent assignments
- User can catch issues with story granularity before execution

---

## When to Use

| Complexity | Use Plan Approval? |
| ---------- | ------------------ |
| <15        | No (skip)          |
| ≥15        | **Yes**            |

---

## Workflow

1. **Present complete plan to user:**
   - Summary of PRD (link to file)
   - List of user stories with brief descriptions
   - Execution plan summary (waves, parallelization %)
   - Estimated agent count

2. **Ask for approval:**

   ```
   PLAN SUMMARY
   ════════════════════════════════════════

   PRD: docs/epics/in-progress/msm-feature/prd.md

   User Stories (9 total):
   - Wave 1 (parallel): msm-feat-001, msm-feat-002
   - Wave 2 (parallel): msm-feat-003, msm-feat-004, msm-feat-005, msm-feat-006
   - Wave 3 (parallel): msm-feat-007, msm-feat-008
   - Wave 4: msm-feat-009

   Parallelization: 65% (vs 0% if stories were per-package)
   Max concurrent agents: 4

   Ready to execute?
   ```

   - **YES** → Continue to execution-phase
   - **NO** → Ask what changes needed → Go to step 3

3. **If changes requested:**
   - Identify which component needs revision (PRD, stories, or plan)
   - Spawn appropriate agent (BA for PRD/stories, PM for plan)
   - Update files
   - Loop back to step 1 (max 2 iterations)

4. **Continue to execution-phase** with approved plan

---

## Output Format

```json
{
  "status": "approved",
  "prdPath": "docs/epics/in-progress/msm-feature/prd.md",
  "storiesFolder": "docs/epics/in-progress/msm-feature/user-stories/",
  "storyFiles": ["msm-feat-001-database-schema.md", "msm-feat-002-contracts-types.md", "msm-feat-003-workflow-scaffolding.md", "msm-feat-004-height-weight-parser.md", "msm-feat-005-team-fuzzy-matching.md", "msm-feat-006-major-entity-parser.md", "msm-feat-007-validation-upsert.md", "msm-feat-008-api-layer.md", "msm-feat-009-frontend.md"],
  "executionPlan": "docs/epics/in-progress/msm-feature/execution-plan.md",
  "iterations": 1
}
```

---

## Revision Scenarios

| User Feedback                              | Action                                      |
| ------------------------------------------ | ------------------------------------------- |
| "Stories too coarse"                       | BA re-extracts with finer granularity       |
| "Wrong architecture approach"              | Architect revises annotations               |
| "Too many waves, can we parallelize more?" | PM revises execution plan                   |
| "Missing acceptance criteria"              | BA updates specific story files             |
| "PRD scope changed"                        | BA updates PRD, re-extract stories, re-plan |

---

## Integration

**Called by:** /audit, /build, /ms (complexity ≥15)
**Calls:** business-analyst agent (revise), architect agent (revise), project-manager agent (revise), AskUserQuestion
**Previous phase:** design-phase (stories extracted, annotated, planned)
**Next phase:** execution-phase
