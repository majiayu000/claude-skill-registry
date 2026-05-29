---
name: agent-ops-focus-scan
description: "Analyze issues to identify the next work item and update focus.md. Enforces issue-first workflow and confidence-based batch limits."
category: state
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: []
state_files:
  read: [issues/index.md, issues/critical.md, issues/critical-*.md, issues/high.md, issues/high-*.md, issues/medium.md, issues/medium-*.md, issues/low.md, issues/low-*.md, issues/backlog.md, issues/backlog-*.md, focus.md, constitution.md]
  write: [focus.md]
---

# Focus Scan

## Purpose
Align session focus with the highest priority pending issue. **Enforces that all work is tracked as issues and respects confidence-based batch limits.**

## Context Optimization

**Read `index.md` first** for quick issue overview. Only load full priority files when selecting specific issues to work on.

```
1. Read .agent/issues/index.md (compact summary)
2. Identify target priority level from index
3. Load only that priority file for full details
```

## CLI Commands

**Works with or without `aoc` CLI installed.** Focus scanning can be done via direct file reading.

### File-Based Priority Scan (Default)

```
1. Read .agent/issues/index.md (compact summary)
2. Identify target priority level from index
3. Load only that priority file for full details
4. Filter for status: todo or open
5. Select first actionable issue (respecting depends_on)
```

### Focus Update (File-Based)

1. Read current `.agent/focus.md`
2. Update "Doing now" section with selected issue
3. Update "Next" section with immediate step

### CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Command | Purpose |
|---------|---------|
| `aoc issues list --status todo,open --priority critical` | Find critical actionable issues |
| `aoc issues list --status todo,open --priority high` | Find high priority issues |
| `aoc issues list --status blocked` | Find blocked issues |
| `aoc issues show <ID>` | Check issue details |
| `aoc issues summary` | Quick status overview |

## Confidence-Based Batch Limits

| Confidence | Max Issues per Iteration | Rationale |
|------------|-------------------------|-----------|
| LOW | 1 (hard limit) | High uncertainty requires focused human oversight |
| NORMAL | Up to 3 | Standard workflow with reasonable batching |
| HIGH | Up to 5 | Well-understood work can be batched |

**Enforcement:**
- Read confidence from constitution or current task
- If LOW confidence, select EXACTLY 1 issue — no batching
- Present batch to user for confirmation if confidence is not HIGH

## Issue-First Enforcement

Before starting any work:

1. **Check for existing issue**: Is there an issue for the requested work?
   - Yes → proceed to priority scan
   - No → prompt to create issue first

2. **If user requests work without an issue**:
   ```
   ⚠️ No issue found for this work.
   
   All work should be tracked for auditability.
   
   Create an issue first?
   [Y]es, create and start / [N]o, work without tracking
   
   Suggested: {TYPE}-{next}@{hash} — "{inferred title}"
   ```

3. **Even simple chores need issues**:
   - "Fix typo" → `CHORE` issue
   - "Update dependency" → `CHORE` issue  
   - "Add comment" → `DOCS` issue
   - "Quick refactor" → `REFAC` issue (needs permission anyway)

## Procedure

1. **Check confidence level** (from constitution or task):
   - Determine batch size limit
   - Note if LOW confidence (special handling)

2. **Scan priority files in order** (stop when actionable issue found):
   - `.agent/issues/critical.md` (scan first — highest priority)
   - `.agent/issues/high.md`
   - `.agent/issues/medium.md`
   - `.agent/issues/low.md` (only if nothing higher)
   - **SKIP** `.agent/issues/backlog.md` — backlog items need triage first

3. **Identify** the highest priority issue where:
   - Status is `todo` or `in_progress`
   - All `depends_on` dependencies are `done` (or list is empty)
   - Issue is not marked as `blocked`, `cancelled`, or `dropped`

4. **Apply batch limit** based on confidence:

   *For LOW confidence:*
   ```
   🎯 LOW CONFIDENCE MODE — Single Issue Focus
   
   Selected: {ISSUE-ID} — {title}
   
   Batch size: 1 (hard limit for low confidence)
   
   This issue will receive:
   - Mandatory interview before planning
   - Extensive implementation details
   - Hard stop after implementation for human review
   - ≥90% test coverage requirement
   
   Proceed with this issue? [Y]es / [N]o, select different
   ```

   *For NORMAL confidence:*
   ```
   📋 Selected {N} issues for this iteration (max 3):
   
   1. {ISSUE-ID-1} — {title}
   2. {ISSUE-ID-2} — {title}
   
   Proceed? [Y]es / [M]odify selection / [S]ingle issue only
   ```

   *For HIGH confidence:*
   - Proceed with selection (up to 5), report only

5. **Action based on findings**:

   *If an actionable issue is found:*
   - Read `.agent/focus.md`
   - Update `Doing now` to reflect this issue (include issue ID)
   - Update `Next` with the immediate practical step
   - Example:
     ```markdown
     ## Doing now
     - Working on FEAT-0012@a3f2c1: Add user authentication
     
     ## Next
     - Review existing auth patterns in codebase
     - Create implementation plan
     ```

   *If all issues are blocked:*
   - Identify the specific blockers
   - Update focus to indicate blockers need resolution
   - Suggest resolving dependencies or creating new issues

   *If no prioritized issues exist but backlog has items:*
   - Prompt user:
     ```
     📋 No prioritized issues, but {N} items in backlog.
     
     1. Triage backlog (/agent-task triage)
     2. Create new issue (/agent-task)
     3. Run discovery (/agent-baseline, /agent-review)
     ```

   *If no issues exist at all:*
   - Update focus to indicate planning/discovery needed
   - Prompt user:
     ```
     📋 No issues anywhere. What would you like to do?
     
     1. Create new issues (/agent-task)
     2. Run discovery to find work (/agent-baseline, /agent-review)
     3. Describe what you want to work on (I'll create an issue)
     ```
