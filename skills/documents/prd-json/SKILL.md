---
name: prd-json
description: "Convert PRDs to prd.json format for the brave-core-bot autonomous agent system. Use when you have an existing PRD and need to convert it to prd.json format. Triggers on: convert this prd, turn this into prd.json, create prd.json from this."
---

# PRD to prd.json Converter

Converts existing PRDs to the prd.json format that brave-core-bot uses for autonomous execution.

---

## The Job

Take a PRD (markdown file or text) and convert it to `prd.json` in your brave-core-bot directory.

---

## Output Format

```json
{
  "project": "[Project Name]",
  "repository": "[owner/repo]",
  "description": "[Feature description from PRD title/intro]",
  "config": {
    "workingDirectory": "[Git repo path, e.g., src/brave]",
    "testExecutionRequired": true
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2",
        "Tests pass"
      ],
      "priority": 1,
      "status": "pending",
      "branchName": null,
      "prNumber": null,
      "prUrl": null,
      "lastActivityBy": null
    }
  ]
}
```

---

## Story Size: The Number One Rule

**Each story must be completable in ONE iteration (one context window).**

The bot spawns a fresh Claude instance per iteration with no memory of previous work. If a story is too big, the LLM runs out of context before finishing and produces broken code.

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

Each criterion must be something the bot can CHECK, not something vague.

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

### For test fixes, determine test location DURING prd.json creation:

**IMPORTANT:** When converting a test fix PRD to prd.json, you MUST determine the test location first and write the correct acceptance criteria directly.

**Before writing the prd.json:**
1. Run `git grep TestClassName ../src/brave` and `git grep TestClassName ../src`
2. Based on where the test is found, write the specific test command

**For Brave tests (found in `../src/brave`):**
```json
"acceptanceCriteria": [
  "Fix the failing test condition",
  "Run npm run build from src/brave (must pass)",
  "Run npm run test -- brave_browser_tests --gtest_filter=TestName (must pass 5 consecutive times)"
]
```

**For Chromium tests (found in `../src/chrome` or similar):**
```json
"acceptanceCriteria": [
  "Fix the failing test condition",
  "Run npm run build from src/brave (must pass)",
  "Run npm run test -- browser_tests --gtest_filter=TestName (must pass 5 consecutive times)"
]
```

**Do NOT use conditional criteria** like `[For Brave tests only]` - write the exact command based on your research.

Test fixes are NOT complete until the specific test passes consistently (5 times).

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order, then document order (lower number = higher priority)
4. **All stories start as**: `status: "pending"`, `branchName: null`, `prNumber: null`, `prUrl: null`, `lastActivityBy: null`
5. **Always add**: Test execution commands to every story's acceptance criteria

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

**Output prd.json:**
```json
{
  "project": "TaskApp",
  "repository": "owner/task-app",
  "description": "Task Status Feature - Track task progress with status indicators",
  "config": {
    "workingDirectory": ".",
    "testExecutionRequired": true
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Tests pass"
      ],
      "priority": 1,
      "status": "pending",
      "branchName": null,
      "prNumber": null,
      "prUrl": null,
      "lastActivityBy": null
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Tests pass"
      ],
      "priority": 2,
      "status": "pending",
      "branchName": null,
      "prNumber": null,
      "prUrl": null,
      "lastActivityBy": null
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Tests pass"
      ],
      "priority": 3,
      "status": "pending",
      "branchName": null,
      "prNumber": null,
      "prUrl": null,
      "lastActivityBy": null
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Tests pass"
      ],
      "priority": 4,
      "status": "pending",
      "branchName": null,
      "prNumber": null,
      "prUrl": null,
      "lastActivityBy": null
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

**The run.sh script handles this automatically** when you run it, but if you are manually updating prd.json between runs, archive first.

---

## Checklist Before Saving

Before writing prd.json, verify:

- [ ] **Previous run archived** (if prd.json exists with different branchName, archive it first)
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema to backend to UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify in browser using dev-browser skill" as criterion
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
