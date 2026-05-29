---
name: prd-converter
description: "Converts PRDs to prd.json format for Aha Loop autonomous execution. Use when converting existing PRDs to JSON format. Triggers on: convert prd, create prd.json, aha-loop format."
---

# Aha Loop PRD Converter

Converts existing PRDs to the prd.json format that Aha Loop uses for autonomous execution.

---

## The Job

Take a PRD (markdown file or text) and convert it to `prd.json` in the scripts/aha-loop directory.

---

## Output Format (v2)

```json
{
  "version": 2,
  "project": "[Project Name]",
  "branchName": "aha-loop/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "changeLog": [],
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "researchTopics": [
        "Question about technology or best practice",
        "Question about existing patterns"
      ],
      "researchCompleted": false,
      "learnings": "",
      "implementationNotes": "",
      "notes": ""
    }
  ]
}
```

### New v2 Fields Explained

| Field | Purpose |
|-------|---------|
| `version` | Schema version (always 2) |
| `changeLog` | Array of plan modifications made during execution |
| `researchTopics` | Questions to investigate before implementing the story |
| `researchCompleted` | Whether research phase is done for this story |
| `learnings` | Knowledge gained during implementation (filled by Aha Loop) |
| `implementationNotes` | Guidance from research phase for implementation |

---

## Story Size: The Number One Rule

**Each story must be completable in ONE Aha Loop iteration (one context window).**

Aha Loop spawns a fresh AI instance per iteration with no memory of previous work. If a story is too big, the LLM runs out of context before finishing and produces broken code.

### Right-sized stories:
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):
- "Build the entire dashboard" - Split into: schema, queries, UI components, filters
- "Add authentication" - Split into: schema, middleware, login UI, session handling
- "Refactor the API" - Split into one story per endpoint or pattern

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
1. UI component (depends on schema that does not exist yet)
2. Schema change

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something the execution engine can CHECK, not something vague.

### Good criteria (verifiable):
- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "Typecheck passes"
- "Tests pass"

### Bad criteria (vague):
- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include as final criterion:
```
"Typecheck passes"
```

For stories with testable logic, also include:
```
"Tests pass"
```

### For stories that change UI, also include:
```
"Verify in browser using dev-browser skill"
```

Frontend stories are NOT complete until visually verified. Aha Loop will use the dev-browser skill to navigate to the page, interact with the UI, and confirm changes work.

---

## Conversion Rules

1. **Version**: Always set `"version": 2`
2. **Each user story becomes one JSON entry**
3. **IDs**: Sequential (US-001, US-002, etc.)
4. **Priority**: Based on dependency order, then document order
5. **All stories**: `passes: false`, `researchCompleted: false`, empty `notes`, `learnings`, `implementationNotes`
6. **branchName**: Derive from feature name, kebab-case, prefixed with `aha-loop/`
7. **Always add**: "Typecheck passes" to every story's acceptance criteria
8. **researchTopics**: Extract from PRD's Research Topics section, or generate if story involves:
   - Unfamiliar third-party libraries
   - Multiple implementation approaches
   - Performance-sensitive code
   - Complex integrations
9. **changeLog**: Initialize as empty array `[]`

---

## Splitting Large PRDs

If a PRD has big features, split them:

**Original:**
> "Add user notification system"

**Split into:**
1. US-001: Add notifications table to database
2. US-002: Create notification service for sending notifications
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Add mark-as-read functionality
6. US-006: Add notification preferences page

Each is one focused change that can be completed and verified independently.

---

## Example

**Input PRD:**
```markdown
# Task Status Feature

Add ability to mark tasks with different statuses.

## Requirements
- Toggle between pending/in-progress/done on task list
- Filter list by status
- Show status badge on each task
- Persist status in database
```

**Output prd.json (v2):**
```json
{
  "version": 2,
  "project": "TaskApp",
  "branchName": "aha-loop/task-status",
  "description": "Task Status Feature - Track task progress with status indicators",
  "changeLog": [],
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "researchTopics": [
        "Best practices for enum columns in this database",
        "Migration rollback strategies"
      ],
      "researchCompleted": false,
      "learnings": "",
      "implementationNotes": "",
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "researchTopics": [
        "Existing badge components in codebase",
        "Accessible color schemes for status indicators"
      ],
      "researchCompleted": false,
      "learnings": "",
      "implementationNotes": "",
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "researchTopics": [],
      "researchCompleted": false,
      "learnings": "",
      "implementationNotes": "",
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "researchTopics": [
        "URL state management patterns in this codebase"
      ],
      "researchCompleted": false,
      "learnings": "",
      "implementationNotes": "",
      "notes": ""
    }
  ]
}
```

---

## Archiving Previous Runs

**Before writing a new prd.json, check if there is an existing one from a different feature:**

1. Read the current `prd.json` if it exists
2. Check if `branchName` differs from the new feature's branch name
3. If different AND `progress.txt` has content beyond the header:
   - Create archive folder: `archive/YYYY-MM-DD-feature-name/`
   - Copy current `prd.json` and `progress.txt` to archive
   - Reset `progress.txt` with fresh header

**The aha-loop.sh script handles this automatically** when you run it, but if you are manually updating prd.json between runs, archive first.

---

## Checklist Before Saving

Before writing prd.json, verify:

- [ ] **Version set to 2**
- [ ] **Previous run archived** (if prd.json exists with different branchName, archive it first)
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema to backend to UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify in browser using dev-browser skill" as criterion
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
- [ ] Complex stories have relevant `researchTopics`
- [ ] All stories have `researchCompleted: false` initially
- [ ] `changeLog` initialized as empty array

## Research Topics Guidelines

**When to add research topics:**
- Story uses unfamiliar library → "How to use [library] for [task]"
- Multiple approaches possible → "Compare [approach A] vs [approach B]"
- Performance matters → "Performance implications of [approach]"
- Existing patterns unknown → "Existing patterns for [feature] in codebase"

**When to skip research topics:**
- Simple CRUD operations
- Copy-paste from existing similar code
- Well-understood patterns already used in project
- Story builds directly on previous story's learnings
