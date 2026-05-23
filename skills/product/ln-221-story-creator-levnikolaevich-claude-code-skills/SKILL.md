---
name: ln-221-story-creator
description: Creates Stories from IDEAL plan (CREATE) or appends user-requested Stories (ADD). Generates 8-section documents, validates INVEST, creates in Linear. Invoked by ln-220.
---

# Story Creator

Universal factory worker for creating Stories. Supports two modes:
- **CREATE MODE**: Epic has no Stories → create from IDEAL plan (5-10 Stories)
- **ADD MODE**: Epic has Stories → append new Story(s) from user request

Invoked by ln-220-story-coordinator (Phase 5a for CREATE, Phase 5c for ADD).

## When Invoked

**1. ln-220-story-coordinator CREATE MODE (Phase 5a):**
- Epic has NO existing Stories (Linear query count = 0)
- IDEAL plan generated (Phase 3)
- Standards Research completed by ln-001 (Phase 2)
- Parameters: `epicData`, `idealPlan`, `standardsResearch`, `teamId`, `autoApprove`

**2. ln-220-story-coordinator ADD MODE (Phase 5c):**
- Epic HAS existing Stories, user wants to ADD more (not replan)
- Single Story or few Stories from user request
- Parameters: `epicData`, `appendMode: true`, `newStoryDescription`, `standardsResearch`, `teamId`

## Input Parameters

**For CREATE MODE (from ln-220-story-coordinator Phase 5a):**

```javascript
{
  epicData: {id, title, description},
  idealPlan: [
    {
      number: "US004",
      title: "Register OAuth client",
      statement: {persona, capability, value},
      ac: [GWT scenarios],
      technicalNotes: {architecture, integrations, performance},
      estimatedHours: 12,
      testCounts: {e2e: 2, integration: 5, unit: 11}
    }
  ],
  standardsResearch: "OAuth 2.0 (RFC 6749)...",
  teamId: "team-id",
  autoApprove: true
}
```

**For ADD MODE (from ln-220-story-coordinator Phase 5c with appendMode):**

```javascript
{
  epicData: {id, title, description},
  appendMode: true,                    // Signals ADD MODE - append to existing
  newStoryDescription: "User's request for new Story",
  standardsResearch: "Focused research for new Story only",
  teamId: "team-id",
  autoApprove: false                   // User confirmation recommended
}
```

- **appendMode**: `true` signals ADD MODE - append to existing Stories
- **newStoryDescription**: User's request for new Story(s) to add
- **NO idealPlan** - creates only what user requested (single Story or few)

## Workflow

> [!NOTE]
> **ADD MODE (appendMode: true)**: When adding Stories to existing Epic, workflow is simplified:
> - Phase 1: Generate only requested Story(s) from `newStoryDescription`
> - Skip full IDEAL plan comparison
> - Standards Research is focused only on new Story topics
> - Other phases proceed normally (INVEST, Preview, Create)

### Phase 1: Generate Story Documents

Load story template (see "Template Loading" section) and use 8 sections.

For EACH Story in IDEAL plan:

| Section | Content |
|---------|---------|
| **1. Story Statement** | As a [persona] / I want [capability] / So that [value] |
| **2. Context** | Current Situation (from Epic Scope Out) / Desired Outcome (from Epic Success Criteria) |
| **3. AC** | Copy AC from idealPlan (3-5 GWT scenarios) |
| **4. Tasks** | Placeholder: "Tasks created via ln-300-task-coordinator after ln-310-story-validator" |
| **5. Test Strategy** | Copy test counts from idealPlan, Risk-Based Testing note |
| **6. Technical Notes** | **INSERT Standards Research** in Library Research subsection |
| **7. DoD** | Standard checklist from template |
| **8. Dependencies** | Empty OR "Depends On: US00X" if ordering implies dependency |

**Output:** Array of N complete Story documents (5-10) with Standards Research inserted.

### Phase 2: Validate INVEST

For EACH Story, check:

| Criterion | Check | Pass | Fail |
|-----------|-------|------|------|
| **Independent** | No circular dependencies | ✅ | ❌ STOP |
| **Negotiable** | AC focus on WHAT not HOW | ✅ | ❌ STOP |
| **Valuable** | Clear "So that" value | ✅ | ❌ STOP |
| **Estimable** | 6-20 hours | ✅ | ❌ STOP |
| **Small** | 3-5 AC, 10-28 tests | ✅ | ❌ STOP |
| **Testable** | Measurable AC (GWT format) | ✅ | ❌ STOP |

**Error if ANY Story fails** → Report to orchestrator, stop execution.

### Phase 3: Show Preview

```
STORY CREATION PREVIEW for Epic 7: OAuth Authentication

Will create 5 Stories:

1. US004: Register OAuth client
   Persona: Third-party developer | Capability: Register app, get credentials
   Value: Can integrate with API | AC: 4 | Estimate: 12h | Tests: 18

2. US005: Request access token
   Persona: API client | Capability: Exchange credentials for token
   Value: Authenticate to API | AC: 5 | Estimate: 18h | Tests: 24

... (3 more)

Total: 5 Stories, 62h, 90 tests

Standards Research: OAuth 2.0 (RFC 6749), RFC 7636 (PKCE), RFC 7009 (Revocation)
Story ordering: Dependency-aware (US004 → US005 → US006)
INVEST validation: ✓

Type "confirm" to create.
```

### Phase 4: User Confirmation

**If autoApprove=true:** Skip confirmation → Phase 5
**Otherwise:** Wait for "confirm"

### Phase 5: Create in Linear + Update Kanban

**Create Linear Issues:**
```javascript
for each Story:
  create_issue({
    title: Story.number + ": " + Story.title,
    description: Story.generated_document,
    project: epicData.id,
    team: teamId,
    labels: ["user-story"],
    state: "Backlog"
  })
```

**Update kanban_board.md:**

**Epic Grouping Algorithm:**
1. Find `### Backlog`
2. Search `**Epic {epicNumber}: {epicTitle}**`
   - Found: use existing Epic group
   - NOT found: create `**Epic N: Epic Title**`
3. Add Stories under Epic (2-space indent, 📖 emoji)

**Format:**
```markdown
**Epic 7: OAuth Authentication**

  📖 [ID: US004 Register OAuth client](url)
    _(tasks not created yet)_
  📖 [ID: US005 Request access token](url)
    _(tasks not created yet)_
```

**Update Epic Story Counters table:**
- Last Story: US008
- Next Story: US009

**Return:**
```
STORIES CREATED for Epic 7: OAuth Authentication

✓ Created 5 Stories in Linear:
  1. [ID: US004 Register OAuth client](url)
  2. [ID: US005 Request access token](url)
  3. [ID: US006 Validate access token](url)
  4. [ID: US007 Refresh expired token](url)
  5. [ID: US008 Revoke token](url)

✓ kanban_board.md updated (Backlog + Epic Story Counters)
✓ Standards Research included: OAuth 2.0, RFC 7636 PKCE, RFC 7009 Revocation

Total: 5 Stories, 62h, 90 tests

NEXT STEPS:
1. Run ln-310-story-validator to validate Stories (Backlog → Todo)
2. Use ln-300-task-coordinator to create tasks
```

## Critical Rules

| Rule | Description |
|------|-------------|
| **Standards Research Insertion** | MUST insert in EVERY Story Technical Notes → Library Research |
| **INVEST Validation** | All Stories must pass before creation (stop if ANY fails) |
| **Template Ownership** | This skill owns story_template_universal.md in references/ |
| **Epic Grouping** | Reuse Epic header if exists (search by Epic number), don't duplicate |
| **Story Numbering** | Sequential across ALL Epics (read Next Story from kanban_board.md) |
| **No Code** | Descriptions contain approach ONLY, not code |

## Definition of Done

**✅ Phase 1:**
- [ ] All N Stories have 8 sections
- [ ] Standards Research inserted in Technical Notes → Library Research

**✅ Phase 2:**
- [ ] All Stories pass INVEST validation

**✅ Phase 3:**
- [ ] Preview shown (summaries, totals, Standards Research, ordering)

**✅ Phase 4:**
- [ ] autoApprove=true OR user confirmed

**✅ Phase 5:**
- [ ] All N Stories created in Linear (project=Epic, labels=user-story, state=Backlog)
- [ ] kanban_board.md updated (Backlog + Epic Story Counters)
- [ ] Summary returned (URLs + next steps)

## Template Loading

**Template:** `story_template.md`

**Loading Logic:**
1. Check if `docs/templates/story_template.md` exists in target project
2. IF NOT EXISTS:
   a. Create `docs/templates/` directory if missing
   b. Copy `shared/templates/story_template.md` → `docs/templates/story_template.md`
   c. Replace placeholders in the LOCAL copy:
      - `{{TEAM_ID}}` → from `docs/tasks/kanban_board.md`
      - `{{DOCS_PATH}}` → "docs" (standard)
3. Use LOCAL copy (`docs/templates/story_template.md`) for all operations

**Rationale:** Templates are copied to target project on first use, ensuring:
- Project independence (no dependency on skills repository)
- Customization possible (project can modify local templates)
- Placeholder replacement happens once at copy time

## Reference Files

### story_template.md

**Location:** `shared/templates/story_template.md` (centralized)
**Local Copy:** `docs/templates/story_template.md` (in target project)
**Purpose:** Universal Story template (8 sections)
**Template Version:** 9.0.0

## Integration

**Called by:** ln-220-story-coordinator
- Phase 5a (CREATE MODE, count = 0) - full IDEAL plan
- Phase 5c (ADD MODE, count ≥ 1, appendMode) - user-requested Story(s)

**Returns:**
- Success: Story URLs + summary + next steps
- Error: "Story USXXX violates INVEST: [details]"

**Worker does NOT:**
- Query Linear for Epic (already in context)
- Analyze Epic complexity (orchestrator Phase 3)
- Research standards (orchestrator Phase 2 delegates to ln-001)
- Build IDEAL plan (receives from orchestrator)

---

**Version:** 3.0.0
**Last Updated:** 2025-12-23
