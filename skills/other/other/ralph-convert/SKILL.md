---
name: ralph-convert
description: "Convert markdown PRD to prd.json format for Ralph Zero autonomous execution. Validates story structure, checks dependencies, ensures right-sizing, and generates validated JSON. Use when you have a PRD markdown file and need to prepare it for autonomous development."
license: MIT
metadata:
  parent_skill: ralph-zero
  version: "0.1.0"
---

# Ralph Convert: PRD to JSON

Convert markdown Product Requirements Documents into the structured `prd.json` format required by Ralph Zero, with comprehensive validation and story optimization.

## When to Use

Use this skill when:
- User has a markdown PRD and needs prd.json
- User asks to "convert PRD to JSON" or "prepare PRD for Ralph"
- After using the prd generation skill
- Migrating from other PRD formats

## Conversion Workflow

### Step 1: Read the PRD

Ask for the PRD file path:
```
Please provide the path to your PRD markdown file
(e.g., tasks/prd-task-priority.md)
```

Or work with directly provided content.

### Step 2: Extract Information

Parse the PRD to extract:
- **Project name**: From repo name or PRD title
- **Feature name**: From PRD title (for branch name)
- **Description**: Feature summary
- **Requirements**: All user stories or requirements

### Step 3: Generate User Stories

Convert requirements into properly structured user stories.

#### Story Structure

Each story must have:
```json
{
  "id": "US-001",
  "title": "Brief description (max 200 chars)",
  "description": "As a [user], I want [action], so that [benefit]",
  "acceptanceCriteria": [
    "Specific, verifiable criterion 1",
    "Specific, verifiable criterion 2",
    "Typecheck passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": ""
}
```

#### Story Sizing Rules

**CRITICAL: Each story MUST be completable in one iteration (30min - 2hrs)**

✅ **Right-sized stories:**
- "Add status column to database with migration"
- "Create StatusBadge component"
- "Add filter dropdown to header"
- "Update TaskCard to display badge"

❌ **Too large (MUST split):**
- "Build entire dashboard" → Split into 5+ stories
- "Add authentication" → Split into 8+ stories
- "Refactor API" → Split by endpoint/pattern

**Rule of thumb:** If it needs >10 acceptance criteria or >500 char description, split it.

#### Acceptance Criteria Rules

1. **Always include**: `"Typecheck passes"` as final criterion
2. **For UI stories**: `"Verify in browser using dev-browser skill"`
3. **Be specific**: "Badge shows green for done" not "Badge has colors"
4. **Avoid vague terms**: No "works well", "good UX", "fast"

✅ **Good criteria:**
- "Add status column: 'pending' | 'in_progress' | 'done'"
- "Badge colors: gray=pending, blue=in_progress, green=done"
- "Filter dropdown has options: All, Pending, In Progress, Done"
- "Typecheck passes"

❌ **Bad criteria:**
- "Works correctly" (too vague)
- "Good UX" (not verifiable)
- "Handles edge cases" (not specific)

#### Dependency Ordering

Stories execute in priority order. **No forward dependencies allowed.**

**Correct order:**
1. Priority 1: Database schema/migrations
2. Priority 2: Backend logic/API
3. Priority 3: UI components (depend on backend)
4. Priority 4: Dashboards/views

**Wrong:** UI component at priority 1 that depends on API at priority 3

### Step 4: Validate Stories

Before generating prd.json, validate each story:

#### Size Validation
```
if len(acceptanceCriteria) > 10:
    return "Too many criteria - split story"

if len(description) > 500:
    return "Description too long - split story"

complexity_keywords = ['entire', 'complete', 'all', 'full', 'refactor']
if any(keyword in description.lower()):
    return f"Story likely too broad (contains '{keyword}')"
```

#### Criteria Validation
```
if "Typecheck passes" not in acceptanceCriteria:
    return "Missing required 'Typecheck passes' criterion"

vague_phrases = ['works correctly', 'good ux', 'handles edge cases']
for criterion in acceptanceCriteria:
    if any(phrase in criterion.lower()):
        return f"Vague criterion: '{criterion}'"
```

#### Dependency Validation
```
Check that no story depends on features from later priority stories
```

### Step 5: Generate prd.json

Create the JSON structure:

```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-priority",
  "description": "Task Priority System - Track priorities with visual indicators",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to tasks table",
      "description": "As a developer, I need to store task priority in database",
      "acceptanceCriteria": [
        "Add priority column: 'high' | 'medium' | 'low' (default 'medium')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display priority badge on task cards",
      "description": "As a user, I want to see task priority at a glance",
      "acceptanceCriteria": [
        "Each task card shows colored priority badge",
        "Badge colors: red=high, yellow=medium, gray=low",
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

### Step 6: Archive Previous Run (if exists)

Before writing new prd.json, check for existing file:

```python
if prd.json exists and has different branchName:
    date_str = today's date (YYYY-MM-DD)
    old_feature = old branchName without 'ralph/' prefix
    archive_dir = f"archive/{date_str}-{old_feature}"
    
    copy prd.json to archive_dir
    copy progress.txt to archive_dir (if exists)
    reset progress.txt with fresh header
```

### Step 7: Initialize progress.txt

Create fresh progress.txt:

```
================================================================================
RALPH PROGRESS LOG
================================================================================
Project: TaskApp
Branch: ralph/task-priority
Started: 2026-01-18 12:00:00

================================================================================
```

### Step 8: Save and Confirm

Save `prd.json` and inform user:

```
✅ Generated prd.json with [N] user stories
✅ All stories validated successfully  
✅ Initialized progress.txt

Story breakdown:
  - US-001: Add priority field to tasks table
  - US-002: Display priority badge on task cards
  - US-003: Add priority dropdown to task edit
  - US-004: Filter tasks by priority

Ready to run Ralph Zero! Execute:
  ralph-zero run --max-iterations 50

Or via agent:
  Load ralph-zero skill and run autonomous loop
```

## Story Splitting Patterns

When a requirement is too large, use these patterns:

### Pattern 1: By Layer (Backend → Frontend)
```
Original: "Add user authentication"

Split into:
- US-001: Add users table and auth schema
- US-002: Create login/signup API endpoints
- US-003: Add session management middleware
- US-004: Create login UI component
- US-005: Create signup UI component
- US-006: Add protected route handling
```

### Pattern 2: By Component
```
Original: "Build dashboard"

Split into:
- US-001: Create dashboard layout component
- US-002: Add metrics summary card
- US-003: Add recent activity list
- US-004: Add quick actions panel
- US-005: Add filter/search controls
```

### Pattern 3: By User Flow
```
Original: "Add task management"

Split into:
- US-001: Create task (form + API)
- US-002: View task list (query + display)
- US-003: Edit task (modal + API)
- US-004: Delete task (confirmation + API)
- US-005: Bulk operations (select + actions)
```

## Validation Checklist

Before saving prd.json, verify:

- [ ] Each story completable in one iteration
- [ ] Stories ordered by dependency (no forward deps)
- [ ] Every story has "Typecheck passes" in criteria
- [ ] UI stories have "Verify in browser" in criteria
- [ ] All criteria specific and verifiable
- [ ] No story has >10 acceptance criteria
- [ ] Branch name follows format: `ralph/[feature-name]`
- [ ] All story IDs sequential (US-001, US-002, ...)
- [ ] All `passes` fields are `false`
- [ ] All `notes` fields are empty strings

## Error Handling

If validation fails, report clearly:

```
❌ Validation failed:
- US-003 is too large (15 acceptance criteria)
- US-005 depends on feature from US-007
- US-002 missing "Typecheck passes" criterion

Please revise the PRD to address these issues, then try again.
```

## Example Conversion

### Input PRD (markdown)
```markdown
# Task Status Feature

Add ability to mark tasks with different statuses.

## Requirements
- Toggle between pending/in-progress/done
- Filter list by status
- Show status badge on each task
- Persist status in database
```

### Output prd.json
```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-status",
  "description": "Task Status Feature - Track task progress",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list",
      "description": "As a user, I want to change status directly",
      "acceptanceCriteria": [
        "Each row has status dropdown",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter by status",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Related Skills

- **prd**: Generate the markdown PRD
- **ralph-zero**: Run autonomous development loop

## See Also

- [Validation Rules](references/VALIDATION.md)
- [Story Sizing Guide](references/STORY_SIZING.md)
- [Example Conversions](references/EXAMPLES.md)
