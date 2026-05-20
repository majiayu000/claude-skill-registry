---
name: bmad-workflow-orchestration-rules
description: 'BMAD workflow orchestration: When and how to use bmad_workflow and sprint-status tools to stay coordinated. Know the 4 core rules, usage patterns, and anti-patterns. Use when starting story development or transitioning between stories. Agent Behavior category skill.'
metadata:
  category: Agent Behavior
  priority: high
  is-built-in: true
  session-guardian-id: builtin_bmad_workflow_orchestration_rules
---

# BMAD Workflow Orchestration Rules

This skill documents **when and how** to use the `bmad_workflow` tool and `sprint-status.yaml` to keep your work coordinated with the broader team and project roadmap.

## Core Orchestration Rules

The following 4 rules keep agents aligned and prevent duplicate or misdirected work:

### Rule 1: Always Call suggest_next After Completing a Story

**When:** Immediately after a story is marked complete via `bmad_workflow:complete_story`

**Why:** The system needs to determine the next logical work unit. Manual searching is error-prone and wastes time.

**How:**

```typescript
// After completing story 19-8
bmad_workflow({
  action: 'suggest_next',
  epicId: 'epic-19',
  currentStoryId: '19-8-create-orchestration-skill',
});
```

**Expected Response:**

- Next actionable story (with preloaded context)
- Epic completion status
- Retrospective recommendation if epic is done
- Related story dependencies

### Rule 2: Never Manually Look for Next Work

**What NOT to do:**

- ❌ Reading sprint-status.yaml manually to find incomplete stories
- ❌ Guessing which story should be next based on your intuition
- ❌ Picking a story that "seems important" without workflow guidance

**Why:** The workflow tool considers:

- Story dependencies and blocking relationships
- Epic progress and phase alignment
- Recommended implementation order
- Risk and complexity factors
- Current project phase

**What TO do:**

- ✅ Always use `bmad_workflow:suggest_next`
- ✅ Follow the recommended story it returns
- ✅ Use preloaded context for story understanding
- ✅ If you disagree with suggestion, escalate to sprint manager

### Rule 3: When Directed to a Story, Always Use story_id Parameter

**When:** Loading a story file, understanding requirements, or starting development

**Why:** The story_id ensures proper context tracking and metrics collection

**How:**

```typescript
// Load story 19-3 with full context
bmad_workflow({
  action: 'get_item',
  itemId: 'create-ceremony-skill', // story_id format
});
```

**Used in:**

- Accessing story file content
- Loading acceptance criteria
- Understanding epic context
- Preloading related skills
- Tracking story completion time

### Rule 4: Before Marking Done, Validate with story-completion-ceremony Skill

**When:** Planning to call `bmad_workflow:complete_story`

**Why:** Incomplete work creates debt and blocks downstream stories

**How:**

1. Review the [story-completion-ceremony](../story-completion-ceremony/SKILL.md) skill
2. Follow its 7-step ceremony
3. Gather validation evidence (tests, coverage, review status)
4. Only then call complete_story with full evidence

```typescript
bmad_workflow({
  action: 'complete_story',
  storyId: 'your-story-id',
  validationEvidence: {
    testsPassed: 25,
    testsFailed: 0,
    coveragePercent: 85,
    codeReviewApproved: true,
    notes: 'All AC verified, tests passing',
  },
});
```

---

## Usage Examples

### Example 1: Complete a Story and Find Next Work

```typescript
// Step 1: Verify with story-completion-ceremony skill
// (follow 7 steps)

// Step 2: Complete the story
const completeResult = await bmad_workflow({
  action: 'complete_story',
  storyId: '19-5-implement-context-preloading-service',
  validationEvidence: {
    testsPassed: 18,
    testsFailed: 0,
    coveragePercent: 89,
    codeReviewApproved: true,
    notes:
      'Context service implemented and tested. Integration tests verify preloading of 8 skill types and story metadata.',
  },
});

// Step 3: Get next work
const nextWork = await bmad_workflow({
  action: 'suggest_next',
  epicId: 'epic-19',
  currentStoryId: '19-5-implement-context-preloading-service',
});

// Output expects:
// {
//   nextStoryId: '19-4-update-dev-story-workflow',
//   status: 'in-progress',
//   epicProgress: '6/8 stories complete',
//   preloadedContext: { ... },
//   recommendation: 'Proceed with story 19-4 (no blocking issues)'
// }
```

### Example 2: Handle Epic Completion Recommendation

```typescript
const nextWork = await bmad_workflow({
  action: 'suggest_next',
  epicId: 'epic-19',
  currentStoryId: '19-7-enhance-webview-story-actions',
});

// If all epic stories are done:
// {
//   epicComplete: true,
//   recommendation: 'run_retrospective',
//   retrospectiveLocation: 'workflows/retrospective/workflow.yaml'
// }

// THEN: Trigger retrospective workflow
// DON'T: Start work on next epic manually
```

### Example 3: Handle Retrospective Routing

When epic is complete and retrospective is recommended:

```typescript
// After receiving 'run_retrospective' recommendation
const retrospective = await bmad_workflow({
  action: 'suggest_next',
  epicId: 'epic-19',
  retrospectiveRequested: true,
});

// Executes retrospective workflow which:
// - Reviews epic outcomes vs. goals
// - Documents lessons learned
// - Updates team wiki with insights
// - Recommends improvements for next epic
// - Routes to next epic or sprint planning
```

---

## Integration Points

### Which Workflows Use These Tools

| Workflow        | Uses                                                        | Decision Point               |
| --------------- | ----------------------------------------------------------- | ---------------------------- |
| `dev-story`     | `complete_story`, `suggest_next`                            | After story completion       |
| `code-review`   | `get_item` (for context), `complete_story` (after approval) | Story load + review approval |
| `retrospective` | `suggest_next`, `get_item` (for epic context)               | Epic completion              |
| `sprint-status` | Query entire sprint (read-only)                             | Sprint planning              |

### Agent vs. System Decision Points

| Decision                 | Who Decides                 | Tool Used                     |
| ------------------------ | --------------------------- | ----------------------------- |
| Work is truly complete   | **Agent** (via ceremony)    | Validation evidence           |
| What story is next       | **System** (bmad_workflow)  | suggest_next                  |
| Epic is complete         | **System** (workflow logic) | Detected during suggest_next  |
| When to do retrospective | **System** (recommend)      | Sent in suggest_next response |

### Handoff Protocol: Dev → Code Review → Done

```
┌─────────────────────────────────────────────────┐
│           Dev Agent (dev-story workflow)         │
│  - Implement code                               │
│  - Write tests (≥80% coverage)                  │
│  - Run local tests (all passing)                │
│  - Call: complete_story with evidence           │
│  - Call: suggest_next → get code-review story   │
│  - Mark: story as "in-review" status            │
└──────────────┬────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│        Code Review Agent (code-review workflow) │
│  - Review code quality across 5 facets          │
│  - Approve or request changes                   │
│  - If approved: mark story "review-approved"    │
│  - Call: complete_story (review_approved=true)  │
│  - Call: suggest_next (find next story)         │
└──────────────┬────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│           Story → DONE                          │
│  Status updated in sprint-status.yaml           │
│  Work awaits next epic phase                    │
└─────────────────────────────────────────────────┘
```

---

## Anti-Patterns (What NOT To Do)

### ❌ Anti-Pattern 1: Not Following suggest_next Results

**Wrong:**

```typescript
// System recommends story 19-4
// But you decide to work on 19-7 because "it's more interesting"
await startWorkOn('19-7-enhance-webview-story-actions');
```

**Why it breaks:**

- Story 19-7 blocks on 19-1 and 19-2 (missing dependencies)
- You'll waste time on work that can't be completed
- The system made recommendations based on dependency analysis

**Right:**

```typescript
// System recommends 19-4 → accept it
const next = await suggest_next('epic-19', currentStory);
// Returns: '19-4-update-dev-story-workflow'
await implementStory(next.storyId); // Always
```

### ❌ Anti-Pattern 2: Skipping Validation Steps

**Wrong:**

```typescript
// Stories complete but ceremony was skipped
await complete_story({
  storyId: '19-5',
  validationEvidence: {}, // Empty! No tests run!
});
```

**Why it breaks:**

- Downstream stories inherit technical debt
- Code reviews fail later (rework needed)
- Quality standards erode

**Right:**

```typescript
// Follow all 7 steps
// - Verify AC: ✅
// - Write tests: ✅ (25 tests added)
// - Run tests: ✅ (all passing)
// - Edge cases: ✅ (tested null, empty, max cases)
// - Code review: ✅ (peer approved)
// - Update status: ✅ (sprint-status.yaml updated)
// - Call tool: ✅ (with full evidence)
await complete_story({
  storyId: '19-5',
  validationEvidence: {
    testsPassed: 25,
    testsFailed: 0,
    coveragePercent: 87,
    codeReviewApproved: true,
    notes: 'Full ceremony complete',
  },
});
```

### ❌ Anti-Pattern 3: Manually Updating sprint-status Without Tools

**Wrong:**

```yaml
# Direct edit to sprint-status.yaml
19-4-update-dev-story-workflow: done # Manual change!
```

**Why it breaks:**

- No validation evidence captured
- Metrics are inaccurate (time, effort tracking)
- Blocks epic orchestration (system doesn't know it's complete)
- Retrospective can't analyze real data

**Right:**

```typescript
// Use the tool which updates status AND captures evidence
await bmad_workflow({
  action: 'complete_story',
  storyId: '19-4-update-dev-story-workflow',
  validationEvidence: {
    /* full evidence */
  },
});
// System automatically updates sprint-status.yaml
```

### ❌ Anti-Pattern 4: Ignoring Blocking Dependencies

**Wrong:**

```typescript
// You start story 19-7 before 19-1 and 19-2 are complete
await startWorkOn('19-7-enhance-webview-story-actions');
// Gets stuck: can't implement webview without the tool enhancements!
```

**Why it breaks:**

- You'll implement features that conflict with tool changes
- Work gets thrown away or requires major rework
- Frustration and wasted effort

**Right:**

```typescript
// Always ask suggest_next
const next = await suggest_next('epic-19', currentStory);
// Returns: '19-4' (which depends on 19-1 and 19-2)
// Only 19-4 is returned because 19-1 and 19-2 are already done
// System prevents blocking scenarios
```

### ❌ Anti-Pattern 5: Running Retrospective Mid-Epic

**Wrong:**

```typescript
// After story 19-3 completes, trigger retrospective
await runRetrospective('epic-19'); // Epic is only 3/8 done!
```

**Why it breaks:**

- Retrospective is meant for completed epics
- Stopping mid-epic loses momentum
- Insights are incomplete (haven't finished the work)
- Next epic planning won't have full context

**Right:**

```typescript
// Only when suggest_next says epicComplete: true
const next = await suggest_next('epic-19', lastStory);
if (next.epicComplete) {
  // Now safe to retrospect
  console.log(next.recommendation); // 'run_retrospective'
}
```

---

## Related Skills

- **story-completion-ceremony**: The 7-step validation process before calling complete_story
- **code-review-mode**: Self-review checklist for code quality
- **test-driven-development**: Write tests before code
- **always-plan-first**: Plan changes before implementation
- **explain-decisions**: Document your reasoning for code choices
- **use-sub-agents**: When to delegate work to other agents

---

## Real-World Examples from SessionGuardian

### Complete Example: Story 19-5 Implementation Lifecycle

```
🟦 START: receive suggest_next → story 19-5

🔧 PHASE 1: Development
   - Read story file (19-5-implement-context-preloading-service.md)
   - Load preloaded context (dependencies, related skills)
   - Implement StoryContextPreloadingService
   - Write 18 unit tests
   - Run tests (all pass)
   - Coverage: 89%

✅ PHASE 2: Completion Ceremony
   - Verify all 4 AC: ✅
   - Tests + coverage: ✅ (18 tests, 89%)
   - Edge cases: ✅ (null, empty, max limits)
   - Self-review: ✅
   - Update sprint-status.yaml: ✅

📋 PHASE 3: Call complete_story
   bmad_workflow({
     action: 'complete_story',
     storyId: '19-5-implement-context-preloading-service',
     validationEvidence: {
       testsPassed: 18,
       testsFailed: 0,
       coveragePercent: 89,
       codeReviewApproved: true,
       notes: 'Implements 3 public methods + 2 private helpers. Preloads skills and story metadata based on epic context.'
     }
   });

🎯 PHASE 4: Get next work
   const next = await suggest_next('epic-19', '19-5');
   // Returns: {
   //   nextStoryId: '19-4-update-dev-story-workflow',
   //   status: 'ready',
   //   description: 'Now that context service exists,...'
   // }

➡️  PHASE 5: Continue with 19-4
```

### How to Recognize When You're NOT Following Orchestration Rules

You'll notice:

- Failing tests in stories that depend on YOUR changes
- Asking "what should I work on next?" repeatedly
- Manual edits to sprint-status.yaml
- Rework because dependencies weren't obvious
- Confusion about which stories are truly complete

---

## Integration with session_guardian

Use Session Guardian to **request confirmation** before:

- Marking a story as complete (especially code stories)
- Escalating a blocked story to sprint manager
- Deviating from suggest_next recommendation

```typescript
session_guardian({
  title: 'Story Completion Request',
  question:
    '✅ Story 19-5: Implementation complete. Validation evidence gathered. Ready to mark complete?',
  // User confirms → proceed with complete_story
  // User declines → address issues, rerun ceremony
});
```

---

## Troubleshooting

### "suggest_next says work on story X but it seems blocked"

**Solution:** Return to suggest_next response and check `blockedBy` field. Escalate to sprint manager if true blocking issue exists.

### "I disagree with the suggested story"

**Solution:** Check the recommendation reason in suggest_next response. If it doesn't match your context, escalate to sprint manager rather than choosing different work.

### "Sprint-status.yaml is out of sync with actual completion"

**Solution:** Always use `bmad_workflow:complete_story` instead of manual edits. It keeps status synchronized.

### "Retrospective triggered too early"

**Solution:** This only happens if suggest_next says epicComplete=true. Check if all stories are actually done in sprint-status.yaml.

---

## Summary

**Remember these 4 core rules:**

1. ✅ **Always call suggest_next** after completing a story
2. ✅ **Never manually search** for next work
3. ✅ **Use story_id parameter** when working with stories
4. ✅ **Validate with ceremony skill** before calling complete_story

**The orchestration system works when agents follow these rules. Breaking them creates debt, confusion, and delays.**
