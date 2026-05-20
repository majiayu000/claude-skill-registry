---
name: ln-221-story-creator
description: "Creates Story documents with 9-section structure and INVEST validation in Linear. Use when Epic has an IDEAL plan ready for Story generation."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Story Creator

## Purpose
Creates Story documents in Linear from IDEAL plan (CREATE mode) or appends user-requested Stories to existing Epic (ADD mode). Invoked by ln-220-story-coordinator.

Universal factory worker for creating Stories. Supports two modes:
- **CREATE MODE**: Epic has no Stories → create from IDEAL plan (5-10 Stories)
- **ADD MODE**: Epic has Stories → append new Story(s) from user request

Invoked by ln-220-story-coordinator (Phase 5a for CREATE, Phase 5c for ADD).

## When Invoked

**1. ln-220-story-coordinator CREATE MODE (Phase 5a):**
- Epic has NO existing Stories (Linear query count = 0)
- IDEAL plan generated (Phase 3)
- Standards Research completed by ln-220 inline (Phase 2)
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
      orchestratorBrief: {tech, keyFiles, approach, complexity},
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

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `epicId` | Yes | args, kanban, user | Epic to process |

**Resolution:** Epic Resolution Chain.
**Status filter:** Active (planned/started)

## Tools Config

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider

## Quality Criteria

**MANDATORY READ:** Load `shared/references/creation_quality_checklist.md` §Story Creation Checklist for validation criteria that ln-310 will enforce.

## Workflow

> [!NOTE]
> **ADD MODE (appendMode: true)**: When adding Stories to existing Epic, workflow is simplified:
> - Phase 1: Generate only requested Story(s) from `newStoryDescription`
> - Skip full IDEAL plan comparison
> - Standards Research is focused only on new Story topics
> - Other phases proceed normally (INVEST, Preview, Create)

### Phase 1: Generate Story Documents

**Step 0: Resolve epicId** (standalone only — skip if epicData provided by ln-220 orchestrator):
Run Epic Resolution Chain per guide.

**Step 1: Generate Documents**

Load story template (see "Template Loading" section) and use 9 sections.

**Template Discipline (MANDATORY):** Story documents contain EXACTLY 9 sections from the template: Story, Context, Acceptance Criteria, Implementation Tasks, Test Strategy, Technical Notes, Definition of Done, Dependencies, Assumptions. Do NOT add extra sections (e.g., "User Scenarios", "Industry Benchmark", "API Design"). Content that does not fit the 9 sections is either Technical Notes material or out of scope.

For EACH Story in IDEAL plan:

| Section | Content |
|---------|---------|
| **1. Story** | As a [persona] / I want [capability] / So that [value] |
| **2. Context** | Current Situation (from Epic Scope Out) / Desired Outcome (from Epic Success Criteria) |
| **3. Acceptance Criteria** | Copy AC from idealPlan (3-5 GWT scenarios) |
| **4. Implementation Tasks** | Placeholder: "Tasks created via ln-300-task-coordinator after ln-310-multi-agent-validator" |
| **5. Test Strategy** | Copy test counts from idealPlan, Risk-Based Testing note |
| **6. Technical Notes** | **INSERT Orchestrator Brief** from `idealPlan[i].orchestratorBrief` (markers `<!-- ORCHESTRATOR_BRIEF_START/END -->`). **INSERT Standards Research** in Library Research subsection |
| **7. Definition of Done** | Standard checklist from template |
| **8. Dependencies** | Empty OR "Depends On: US00X" if ordering implies dependency |
| **9. Assumptions** | Extract from Technical Notes + AC: FEASIBILITY (infra), DEPENDENCY (APIs), DATA (format), SCOPE (exclusions). Default confidence: MEDIUM |

**Output:** Array of N complete Story documents (5-10) with Standards Research inserted.

### Phase 2: Validate INVEST

For EACH Story, check:

| Criterion | Check | Pass | Fail |
|-----------|-------|------|------|
| **Independent** | No circular dependencies | ✅ | ❌ STOP |
| **Negotiable** | AC focus on WHAT user observes, not HOW system works. ACs with system internals (lookup priority, cache layers, endpoint URLs, architecture) → move to Technical Notes | ✅ | ❌ STOP |
| **Valuable** | Clear "So that" value | ✅ | ❌ STOP |
| **Estimable** | Size within checklist #9 range | ✅ | ❌ STOP |
| **Small** | AC/hours/tests per checklist #9 | ✅ | ❌ STOP |
| **Testable** | Measurable AC (GWT format) | ✅ | ❌ STOP |

**Error if ANY Story fails** → Report to orchestrator, stop execution.

**AC Count Gate:** If any Story has >5 ACs → STOP. Report to orchestrator: "Story USXXX has N ACs (limit: 5). Split required." Do not proceed with creation.

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

### Phase 5: Create Stories + Update Kanban

**Create Stories (provider-dependent):**

**IF task_provider == "linear":**
```javascript
for each Story:
  save_issue({
    title: Story.number + ": " + Story.title,
    description: Story.generated_document,
    project: epicData.id,
    team: teamId,
    labels: ["user-story"],
    state: "Backlog"
  })
```

**ELSE (file mode):**
```javascript
for each Story:
  mkdir -p docs/tasks/epics/epic-{N}-{slug}/stories/us{NNN}-{story-slug}/tasks/
  Write("docs/tasks/epics/epic-{N}-{slug}/stories/us{NNN}-{story-slug}/story.md")
  // Include file headers: **Status:** Backlog, **Epic:** Epic {N}, **Labels:** user-story, **Created:** {date}
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
1. Run ln-310-multi-agent-validator to validate Stories (Backlog → Todo)
2. Use ln-300-task-coordinator to create tasks
```

## Critical Rules

| Rule | Description |
|------|-------------|
| **Standards Research Insertion** | MUST insert in EVERY Story Technical Notes → Library Research (prevents outdated library choices causing rework in ln-400) |
| **INVEST Validation** | All Stories must pass before creation (stop if ANY fails) |
| **Template Ownership** | This skill owns story_template_universal.md in references/ |
| **Epic Grouping** | Reuse Epic header if exists (search by Epic number), don't duplicate |
| **Story Numbering** | Sequential across ALL Epics (read Next Story from kanban_board.md) |
| **No Code** | Descriptions contain approach ONLY, not code |
| **Template Discipline** | Story documents contain EXACTLY 9 template sections. No extra sections (User Scenarios, Industry Benchmark, etc.). Non-template content → Technical Notes or discard |
| **AC Purity** | ACs describe observable user behavior only. System internals (architecture, endpoint design, cache layers) → Technical Notes |

## Definition of Done

**✅ Phase 1:**
- [ ] All N Stories have 9 sections
- [ ] Standards Research inserted in Technical Notes → Library Research

**✅ Phase 2:**
- [ ] All Stories pass INVEST validation

**✅ Phase 3:**
- [ ] Preview shown (summaries, totals, Standards Research, ordering)

**✅ Phase 4:**
- [ ] autoApprove=true OR user confirmed

**✅ Phase 5:**
- [ ] All N Stories created (Linear or file mode) (project=Epic, labels=user-story, state=Backlog)
- [ ] kanban_board.md updated (Backlog + Epic Story Counters)
- [ ] Summary returned (URLs + next steps)

## Template Loading

**MANDATORY READ:** Load `shared/references/template_loading_pattern.md` for template copy workflow.

**Template:** `story_template.md`
**Local copy:** `docs/templates/story_template.md` (in target project)

## Reference Files

- **MANDATORY READ:** `shared/references/tools_config_guide.md`
- **MANDATORY READ:** `shared/references/storage_mode_detection.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Template loading:** `shared/references/template_loading_pattern.md`
- **Linear creation workflow:** `shared/references/linear_creation_workflow.md`

### story_template.md

**Location:** `shared/templates/story_template.md` (centralized)
**Local Copy:** `docs/templates/story_template.md` (in target project)
**Purpose:** Universal Story template (9 sections)
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
- Research standards (orchestrator Phase 2 runs inline)
- Build IDEAL plan (receives from orchestrator)

---

**Version:** 3.0.0
**Last Updated:** 2025-12-23
