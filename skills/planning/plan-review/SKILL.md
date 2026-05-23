---
name: plan-review
description: "Reviews and adjusts PRD plans based on research findings. Use after completing research to evaluate story modifications. Triggers on: review plan, adjust stories, update prd based on research."
---

# Plan Review Skill

Evaluate research findings and decide whether to adjust upcoming stories in the PRD.

---

## The Job

1. Read the research report for the current story
2. Evaluate if findings impact the current or future stories
3. Decide on plan modifications (if any)
4. Update `prd.json` with changes
5. Document all changes in `changeLog`
6. Ensure plan remains coherent and achievable

---

## When to Modify the Plan

**MODIFY stories when research reveals:**

- A better technical approach than originally planned
- Missing prerequisite steps
- Stories that should be split (too large for one context)
- Stories that can be combined (too small, tightly coupled)
- Changed dependencies requiring reordering
- New edge cases requiring additional acceptance criteria

**DO NOT modify when:**

- The finding is interesting but doesn't affect implementation
- Changes would invalidate already-completed stories
- The modification is scope creep (outside original PRD goals)

---

## Types of Plan Modifications

### 1. Modify Existing Story

Update acceptance criteria, description, or research topics.

```json
{
  "timestamp": "2026-01-29T12:00:00Z",
  "storyId": "US-002",
  "action": "modified",
  "reason": "Research found that existing badge component supports priority colors, simplifying implementation",
  "changes": {
    "acceptanceCriteria": {
      "removed": ["Create new PriorityBadge component"],
      "added": ["Reuse Badge component with priority color variant"]
    }
  }
}
```

### 2. Add New Story

Insert a prerequisite or follow-up story.

```json
{
  "timestamp": "2026-01-29T12:00:00Z",
  "storyId": "US-001.5",
  "action": "added",
  "reason": "Research revealed need for database index on priority column for filter performance",
  "insertAfter": "US-001"
}
```

### 3. Split Story

Break a story into smaller pieces.

```json
{
  "timestamp": "2026-01-29T12:00:00Z",
  "storyId": "US-003",
  "action": "split",
  "reason": "Story too large - separating dropdown component from save logic",
  "splitInto": ["US-003a", "US-003b"]
}
```

### 4. Reorder Stories

Change priority/order based on new dependencies.

```json
{
  "timestamp": "2026-01-29T12:00:00Z",
  "storyId": "US-004",
  "action": "reordered",
  "reason": "URL state management needed before filter implementation",
  "newPriority": 2,
  "previousPriority": 4
}
```

### 5. Remove Story

Mark a story as unnecessary (cannot remove completed stories).

```json
{
  "timestamp": "2026-01-29T12:00:00Z",
  "storyId": "US-005",
  "action": "removed",
  "reason": "Research found this functionality already exists in the codebase"
}
```

---

## Plan Review Process

### Step 1: Read Research Report

Load the research report from `scripts/aha-loop/research/[story-id]-research.md`

Focus on:
- Implementation recommendations
- Alternatives comparison (if recommendation differs from plan)
- Follow-up research needs
- Gotchas discovered

### Step 2: Evaluate Impact

For each finding, ask:

1. **Does this affect the current story?**
   - Update acceptance criteria if needed
   - Add implementation notes

2. **Does this affect future stories?**
   - Check if dependencies changed
   - Check if new prerequisites needed
   - Check if any stories can be simplified/removed

3. **Does this reveal scope issues?**
   - Story too big? Split it.
   - Story too small? Combine with related story.
   - Missing stories? Add them.

### Step 3: Draft Changes

Before modifying `prd.json`:

1. List all proposed changes
2. Verify no completed stories are affected
3. Ensure changes maintain logical story order
4. Check that all stories remain achievable in one context window

### Step 4: Update prd.json

**Backup first** (automatic via aha-loop.sh, but verify).

Apply changes to `prd.json`:

```javascript
// Example: Adding a story
{
  "id": "US-001.5",
  "title": "Add database index for priority filtering",
  "description": "As a developer, I need an index on priority column for efficient filtering.",
  "acceptanceCriteria": [
    "Create index on tasks.priority column",
    "Migration runs without errors",
    "Typecheck passes"
  ],
  "priority": 1.5,  // Will be normalized later
  "passes": false,
  "researchTopics": [],
  "researchCompleted": true,  // No research needed for simple index
  "learnings": "",
  "implementationNotes": "Discovered during US-001 research that filter queries will need this index",
  "notes": ""
}
```

**Add to changeLog:**

```javascript
{
  "changeLog": [
    // ... existing entries
    {
      "timestamp": "2026-01-29T12:00:00Z",
      "storyId": "US-001.5",
      "action": "added",
      "reason": "Research for US-001 revealed need for index to support efficient priority filtering (US-004)",
      "researchSource": "scripts/aha-loop/research/US-001-research.md"
    }
  ]
}
```

### Step 5: Normalize Priorities

After modifications, ensure priorities are sequential:

```javascript
// Before: [1, 1.5, 2, 3, 4]
// After:  [1, 2, 3, 4, 5]
```

---

## Safety Rules

### NEVER:

- Delete or modify stories where `passes: true`
- Add scope beyond original PRD goals
- Create circular dependencies between stories
- Make changes without documenting in `changeLog`

### ALWAYS:

- Document the reason for every change
- Reference the research source
- Maintain dependency order (schema → backend → UI)
- Keep stories small enough for one context window

---

## Review Report Template

After plan review, append to `progress.txt`:

```markdown
## Plan Review - [Date/Time]

### Research Analyzed
- [Story ID]: [Research report path]

### Changes Made

**[Action Type]: [Story ID]**
- Reason: [Why this change was needed]
- Impact: [What this affects]

### No Changes Made (If Applicable)
- Research findings do not require plan modifications
- Reason: [Why no changes needed]

### Updated Story Order
1. US-001: [Title] ✓ (completed)
2. US-001.5: [Title] (new)
3. US-002: [Title]
...

---
```

---

## Example: Complete Plan Review

**Scenario:** Research for US-001 (Add priority to database) revealed:
1. An index is needed for filter performance
2. The existing Badge component can be reused
3. URL state management patterns already exist in codebase

**Changes:**

1. **Add US-001.5** - Create index on priority column
   - Reason: Filter queries (US-004) will be slow without index
   
2. **Modify US-002** - Update acceptance criteria
   - Remove: "Create PriorityBadge component"
   - Add: "Reuse Badge component with 'priority' variant prop"
   
3. **Modify US-004** - Add implementation note
   - Note: "Use existing useUrlState hook from src/hooks/"

**No reordering needed** - dependencies unchanged.

---

## Checklist

Before completing plan review:

- [ ] Research report fully analyzed
- [ ] All impacted stories identified
- [ ] No completed stories modified
- [ ] Changes documented in `changeLog`
- [ ] Priorities normalized
- [ ] Dependencies still valid
- [ ] All stories achievable in one context window
- [ ] Review summary added to `progress.txt`
