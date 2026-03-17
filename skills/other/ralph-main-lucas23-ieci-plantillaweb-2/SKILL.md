---
name: ralph
description: "Autonomous agent loop for completing features. Use when asked to 'use ralph', 'ralph this', or to autonomously implement a feature end-to-end. Creates prd.json with user stories, then executes them one by one until complete."
---

# Ralph - Autonomous Feature Implementation

Ralph is an autonomous loop that implements features by breaking them into small user stories and completing them one at a time. Each iteration is a fresh agent with clean context. Memory persists via git, `progress.txt`, and `prd.json`.

## Quick Start

```bash
# Run ralph in current project (assumes prd.json exists)
~/skills/ralph/scripts/ralph.sh [max_iterations]
```

## Workflow

### Step 1: Understand the Feature

Ask clarifying questions if needed:
- What problem does this solve?
- What are the key user actions?
- What's out of scope?
- How do we know it's done?

### Step 2: Create prd.json

Generate a `prd.json` file in the project root:

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
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
      "notes": ""
    }
  ]
}
```

### Step 3: Run the Loop

```bash
~/skills/ralph/scripts/ralph.sh [max_iterations]
```

Default is 10 iterations.

## Critical Rules for User Stories

### Size: One Context Window

Each story MUST be completable in ONE iteration. If you can't describe it in 2-3 sentences, it's too big.

**Right-sized:**
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

**Too big (split these):**
- "Build the entire dashboard" → schema, queries, UI components, filters
- "Add authentication" → schema, middleware, login UI, session handling

### Order: Dependencies First

1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views

### Acceptance Criteria: Verifiable

**Good:**
- "Add `status` column with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Typecheck passes"

**Bad:**
- "Works correctly"
- "Good UX"

**Always include:**
- `"Typecheck passes"` on every story
- `"Verify in browser using dev-browser skill"` on UI stories

## Example

**User says:** "use ralph to add task priorities"

**You create prd.json:**
```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-priority",
  "description": "Add priority levels (high/medium/low) to tasks",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "description": "As a developer, I need to store task priority.",
      "acceptanceCriteria": [
        "Add priority column: 'high' | 'medium' | 'low' (default 'medium')",
        "Migration runs successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display priority badge on task cards",
      "description": "As a user, I want to see priority at a glance.",
      "acceptanceCriteria": [
        "Colored badge: red=high, yellow=medium, gray=low",
        "Visible without hovering",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**Then say:**
> prd.json created with 2 user stories. Run `~/skills/ralph/scripts/ralph.sh` to start autonomous execution.

## How Ralph Executes

Each iteration, a fresh agent:
1. Reads `prd.json` and `progress.txt`
2. Picks highest priority story where `passes: false`
3. Implements it
4. Runs quality checks (typecheck, lint, test)
5. Commits if passing
6. Updates `prd.json` to mark `passes: true`
7. Appends learnings to `progress.txt`
8. Exits

Loop continues until all stories pass or max iterations hit.

## Files Reference

| File | Purpose |
|------|---------|
| `prd.json` | User stories with pass/fail status |
| `progress.txt` | Append-only learnings for future iterations |
