---
name: ln-222-story-replanner
description: Replans Stories when Epic requirements change. Compares IDEAL vs existing, categorizes operations (KEEP/UPDATE/OBSOLETE/CREATE), executes in Linear.
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Replanner

## Purpose
Replans existing Stories when Epic requirements change. Compares IDEAL plan vs existing Stories, categorizes operations (KEEP/UPDATE/OBSOLETE/CREATE), and executes changes in Linear. Invoked by ln-220-story-coordinator.

Universal replanner worker for updating Stories in Epic when requirements change. Invoked by ln-220-story-coordinator (count ≥ 1).

## When Invoked

**ln-220-story-coordinator REPLAN MODE (Phase 5b):**
- Epic has existing Stories (Linear query count ≥ 1)
- IDEAL plan generated (Phase 3)
- Standards Research completed by ln-001 (Phase 2, may be updated)
- Epic requirements changed (AC modified, features added/removed, standards updated)
- Parameters: `epicData`, `idealPlan`, `standardsResearch`, `existingStoryIds`, `teamId`, `autoApprove`

## Input Parameters

**From ln-220-story-coordinator:**

```javascript
{
  epicData: {id, title, description},
  idealPlan: [{number, title, statement, ac, technicalNotes, estimatedHours, testCounts}],
  standardsResearch: "OAuth 2.0 (RFC 6749)...",  // May differ from existing
  existingStoryIds: ["STORY-123", "STORY-124"],  // Metadata only
  teamId: "team-id",
  autoApprove: true
}
```

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `epicId` | Yes | args, kanban, user | Epic to process |

**Resolution:** Epic Resolution Chain.
**Status filter:** Active (planned/started)

## Tools Config

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider

## Workflow

### Phase 1: Load Existing Stories

**Step 0: Resolve epicId** (standalone only — skip if epicData provided by ln-220 orchestrator):
Run Epic Resolution Chain per guide.

**Progressive Loading for token efficiency:**

**Step 1:** Orchestrator provides Story metadata (ID, title, status)

**Step 2:** Load FULL descriptions ONE BY ONE

**IF task_provider == "linear":**
```javascript
for each story_id:
  get_issue(id=story_id)  // ~5,000 tokens per Story
```

**ELSE (file mode):**
```javascript
for each story_id:
  Read("docs/tasks/epics/epic-{N}-*/stories/us{NNN}-*/story.md")  // ~5,000 tokens per Story
```

**Token Rationale:** 10 Stories × 5,000 = 50,000 tokens. Load sequentially to manage context.

**Step 3:** Parse 9 sections for each Story
- Story Statement (persona, capability, value)
- Context
- Acceptance Criteria (3-5 GWT)
- Implementation Tasks
- Test Strategy
- Technical Notes (**Standards Research** in Library Research subsection)
- Definition of Done
- Dependencies
- Assumptions

**Step 4:** Extract metadata
- ID, number, title, status
- Persona, capability, value
- AC scenarios
- Standards Research (from Technical Notes)

**Output:** Array of N existing Story structures ready for comparison.

### Phase 2: Compare IDEAL vs Existing

**MANDATORY READ:** Load [replan_algorithm_stories.md](references/replan_algorithm_stories.md) for replan algorithm.

**Match by goal, persona, capability:**

For EACH Story in IDEAL:
- Extract: Title, Persona, Capability
- Search existing: Fuzzy match title, check persona/capability overlap
- Result: Match → KEEP/UPDATE | No match → CREATE

For EACH existing Story:
- Extract: Title, Persona, Capability (from Story Statement)
- Search IDEAL: Fuzzy match
- Result: Match → KEEP/UPDATE | No match → OBSOLETE

**Categorize operations:**

| Operation | Criteria | Status Constraint | Action |
|-----------|----------|-------------------|--------|
| **KEEP** | Goal + Persona + Capability + AC + Standards Research same | Any | None |
| **UPDATE** | Match + (AC OR Standards Research OR Technical Notes changed) | Backlog/Todo ✅<br>In Progress/Review ⚠️<br>Done ❌ | `update_issue` |
| **OBSOLETE** | No match + Feature removed | Backlog/Todo ✅<br>In Progress/Review ⚠️<br>Done ❌ | `update_issue(state="Canceled")` |
| **CREATE** | In IDEAL + No match + New requirement | N/A | Generate doc + `create_issue` |

**Edge Cases:**

| Case | Action |
|------|--------|
| **In Progress OBSOLETE** | ⚠️ NO auto-cancel, show warning |
| **Done conflicts** | Preserve Done, CREATE follow-up |
| **Story Split** (1 → 2+) | ⚠️ UPDATE first + CREATE new |
| **Story Merge** (2+ → 1) | ⚠️ UPDATE first + OBSOLETE rest |
| **Ambiguous match** (>70% similarity) | Show all, select highest |

**Details:** [replan_algorithm_stories.md](references/replan_algorithm_stories.md)

### Phase 3: Show Operations Summary

```
REPLAN SUMMARY for Epic 7: OAuth Authentication

IDEAL PLAN:
1. US004: Register OAuth client (Persona: Third-party developer)
2. US005: Request access token ← AC5 ADDED! ← RFC 7636 PKCE ADDED!
3. US006: Validate access token
4. US009: Token scope management (NEW!)

EXISTING STORIES:

✓ US004 - Status: Done - KEEP
⚠ US005 - Status: Todo - UPDATE
   Changes: Add AC5, Add RFC 7636 to Technical Notes, Add 2 Integration tests
   Diff (AC): + AC5 "Given public client, When request with PKCE..."
   Diff (Technical Notes): + RFC 7636 (PKCE)
✗ US008 - Status: Todo - OBSOLETE (feature removed)
+ US009 - NEW (14h, 20 tests, OAuth 2.0 Scope standard)

OPERATIONS: 2 keep, 1 update, 1 cancel, 1 create

WARNINGS:
- ⚠️ US005 (Todo): AC changed, Standards Research updated
- ⚠️ US008 (Todo): Feature removed - check dependencies

Type "confirm" to execute.
```

**Diffs show:**
- AC changes (line-by-line)
- Standards Research changes (added/removed RFCs)
- Test Strategy changes (test counts)

**Warnings for:**
- Status conflicts (In Progress/Review affected)
- Story Split/Merge detected
- Ambiguous matches

### Phase 4: User Confirmation

**If autoApprove=true:** Skip → Phase 5
**Otherwise:** Wait for "confirm"

**Adjustment:** User can request changes → Recategorize → Show updated summary → Loop until "confirm"

### Phase 5: Execute Operations

**Sequence:** UPDATE → OBSOLETE → CREATE → Update kanban

**UPDATE operations:**
1. Generate new Story document (load via Template Loading logic)
2. Validate INVEST (same as ln-221-story-creator Phase 2)
3. **IF task_provider == "linear":** `save_issue({id, description: new_description})`
   **ELSE:** `Edit("docs/tasks/epics/.../stories/us{NNN}-*/story.md")` with new content
4. **IF task_provider == "linear":** `create_comment({issueId, body: "Story updated: ..."})`
   **ELSE:** `Write(".../stories/us{NNN}-*/comments/{ISO-timestamp}.md")` with update note

**OBSOLETE operations:**
1. **IF task_provider == "linear":** `save_issue({id, state: "Canceled"})`
   **ELSE:** `Edit` `**Status:**` line to `**Status:** Canceled` in story.md
2. **IF task_provider == "linear":** `create_comment({issueId, body: "Story canceled: ..."})`
   **ELSE:** `Write(".../comments/{ISO-timestamp}.md")` with cancellation note

**CREATE operations:**
1. Generate Story document (same as ln-221-story-creator Phase 1)
2. Validate INVEST
3. **IF task_provider == "linear":** `save_issue({title, description, project: Epic.id, team: teamId, labels: ["user-story"], state: "Backlog"})`
   **ELSE:** `mkdir -p .../stories/us{NNN}-{slug}/tasks/` + `Write story.md` with file headers

**Update kanban_board.md:**

**DELETE (OBSOLETE):** Remove canceled Story lines, remove task lines if any, remove Epic header if empty

**CREATE (NEW):** Find `### Backlog` → Search Epic group → Add Stories (2-space indent)

**UPDATE Epic Story Counters:** Last Story, Next Story

**Return:**
```
REPLAN EXECUTED for Epic 7

OPERATIONS SUMMARY:
✓ Kept: 2 Stories
✓ Updated: 1 Story (AC/Standards Research changed)
✓ Canceled: 1 Story (feature removed)
✓ Created: 1 Story (new requirement)

UPDATED: [ID: US005](url) - AC5 added, RFC 7636 PKCE added
CANCELED: US008 Custom token formats
NEW: [ID: US009](url) - Token scope management

WARNINGS: US005 (Todo) AC changed

✓ kanban_board.md updated
✓ Standards Research updates: RFC 7636 PKCE added to US005

NEXT STEPS:
1. Review warnings
2. Run ln-310-multi-agent-validator on updated/created Stories
3. Use ln-300-task-coordinator to create/replan tasks
```

## Critical Rules

| Rule | Description |
|------|-------------|
| **Status Constraints** | UPDATE/OBSOLETE: Backlog/Todo ✅, In Progress/Review ⚠️, Done ❌ |
| **Preserve Done** | Never update/cancel Done Stories (CREATE follow-up if conflicts) |
| **Story Split/Merge** | Detect 1→2+ OR 2+→1, show warnings (complex, impacts Tasks) |
| **Clear Diffs** | Show before/after for UPDATE (AC, Standards Research, Technical Notes) |
| **Meaningful Comments** | Explain why updated/canceled (reference removed capabilities) |
| **Conservative Updates** | Prefer CREATE over UPDATE when in doubt |
| **Progressive Loading** | Load Stories ONE BY ONE (not all at once, token efficiency) |

## Definition of Done

**✅ Phase 1:**
- [ ] Existing Story IDs queried (Linear or file mode)
- [ ] FULL descriptions fetched ONE BY ONE
- [ ] 9 sections parsed
- [ ] Metadata extracted (persona, capability, AC, Standards Research)

**✅ Phase 2:**
- [ ] Stories matched by goal/persona/capability
- [ ] Operations categorized (KEEP/UPDATE/OBSOLETE/CREATE)
- [ ] Edge cases detected (Split/Merge, Ambiguous)

**✅ Phase 3:**
- [ ] Operations summary shown
- [ ] Diffs shown for UPDATE (AC, Standards Research, Technical Notes)
- [ ] Warnings shown

**✅ Phase 4:**
- [ ] autoApprove=true OR user confirmed

**✅ Phase 5:**
- [ ] All operations executed (UPDATE/OBSOLETE/CREATE)
- [ ] kanban_board.md updated
- [ ] Summary returned (URLs + warnings)

## Template Loading

**MANDATORY READ:** Load `shared/references/template_loading_pattern.md` for template copy workflow.

**Template:** `story_template.md`
**Local copy:** `docs/templates/story_template.md` (in target project)

## Reference Files

- **MANDATORY READ:** `shared/references/tools_config_guide.md`
- **MANDATORY READ:** `shared/references/storage_mode_detection.md`
- **Template loading:** `shared/references/template_loading_pattern.md`
- **Linear creation workflow:** `shared/references/linear_creation_workflow.md`
- **Replan algorithm:** `shared/references/replan_algorithm.md`

### replan_algorithm_stories.md

**Location:** `references/` (owned by this skill)
**Purpose:** Detailed comparison logic for REPLAN mode (Story level)
**Contents:** KEEP/UPDATE/OBSOLETE/CREATE rules, Match criteria, Status constraints, Edge cases, Examples
**Usage:** Applied in Phase 2

### story_template.md

**Location:** `shared/templates/story_template.md` (centralized)
**Local Copy:** `docs/templates/story_template.md` (in target project)
**Purpose:** Universal Story template (9 sections)
**Usage:** Load via Template Loading logic when generating updated Story documents for UPDATE/CREATE operations

## Integration

**Called by:** ln-220-story-coordinator (Phase 5b, count ≥ 1)

**Returns:**
- Success: Operations summary + URLs + warnings
- Error: "Story USXXX violates INVEST: [details]"

**Worker does NOT:**
- Query Linear for Epic (already in context)
- Analyze Epic complexity (orchestrator Phase 3)
- Research standards (orchestrator Phase 2)
- Build IDEAL plan (receives from orchestrator)

---

**Version:** 3.0.0
**Last Updated:** 2025-12-23
