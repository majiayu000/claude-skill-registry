---
name: gobby-spec
description: This skill should be used when the user asks to "/gobby-spec", "create spec", "plan feature", "write specification". Guide users through structured specification planning and task creation.
version: "1.0"
---

# /gobby-spec - Specification Planning Skill

Guide users through structured requirements gathering, specification writing, and task creation.

## Workflow Overview

1. **Requirements Gathering** - Ask questions to understand the feature
2. **Draft Spec** - Write structured specification document
3. **User Approval** - Present spec for review
4. **Task Creation** - Create tasks from approved spec
5. **Verification** - Update spec with task refs

## Step 1: Requirements Gathering

Ask the user:
1. "What is the name/title for this feature or project?"
2. "What is the high-level goal? (1-2 sentences)"
3. "Are there any constraints or requirements I should know about?"
4. "What are the unknowns or risks?"

## Step 2: Draft Spec Structure

Create a specification with:
- **Epic title**: The overall feature name
- **Phases**: Logical groupings of work (e.g., "Foundation", "Core Implementation", "Polish")
- **Tasks**: Atomic units of work under each phase
- **Dependencies**: Which tasks block which (use notation: `depends: #N` or `depends: Phase N`)

## Step 3: Write Spec Document

Write to `.gobby/specs/{kebab-name}.md`:

```markdown
# {Epic Title}

## Overview
{Goal and context from Step 1}

## Constraints
{Constraints from Step 1}

## Phase 1: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 1 title
- [ ] Task 2 title (depends: Task 1)
- [ ] Task 3 title (parallel)

## Phase 2: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 4 (depends: Phase 1)
- [ ] Task 5 (parallel with Task 4)

## Task Mapping

<!-- Updated after task creation -->
| Spec Item | Task Ref | Status |
|-----------|----------|--------|
```

## Step 4: User Approval

Present the spec to the user:
- Show the full spec document
- Ask: "Does this spec look correct? Would you like any changes before I create tasks?"
- Make changes if requested
- Once approved, proceed to task creation

## Step 5: Task Creation

Build a JSON tree from the spec structure and call `build_task_tree`:

```python
call_tool("gobby-tasks", "build_task_tree", {
    "tree": {
        "title": "{Epic Title}",
        "task_type": "epic",
        "description": "See spec: .gobby/specs/{name}.md",
        "children": [
            {
                "title": "Phase 1: {Phase Name}",
                "children": [
                    {"title": "Task 1", "category": "code"},
                    {"title": "Task 2", "category": "code", "depends_on": ["Task 1"]}
                ]
            },
            {
                "title": "Phase 2: {Phase Name}",
                "children": [
                    {"title": "Task 3", "category": "code", "depends_on": ["Phase 1: {Phase Name}"]},
                    {"title": "Task 4", "category": "document"}
                ]
            }
        ]
    },
    "session_id": "<your_session_id>"
})
```

The tool returns:
- `task_refs`: All created task refs (["#42", "#43", ...])
- `epic_ref`: The root epic ref ("#42")
- `tasks_created`: Total count

**Update spec doc** with task refs:
- Fill in Task Mapping table with created task refs (#N)
- Use Edit tool to update `.gobby/specs/{name}.md`

## Step 6: Verification

After creating all tasks:
1. Show the created task tree (call `list_tasks` with `parent_task_id`)
2. Confirm task count matches spec items
3. Show the updated spec doc with task refs

## Task Granularity Guidelines

Each task should be:
- **Atomic**: Completable in one session (< 2 hours work)
- **Testable**: Has clear pass/fail criteria
- **Verb-led**: Starts with action verb (Add, Create, Implement, Update, Remove)
- **Scoped**: References specific files/functions when possible

Good: "Add TaskEnricher class to src/gobby/tasks/enrich.py"
Bad: "Implement enrichment" (too vague)

## TDD Compatibility (IMPORTANT)

The /gobby-spec skill creates **coarse-grained tasks** knowing that:
1. `expand_task` decomposes them into subtasks
2. `apply_tdd` transforms code tasks into test->implement->refactor triplets

**DO NOT manually create:**
- "Write tests for: ..."
- "Implement: ..."
- "Refactor: ..."
- "Test ..." (as first word)
- Separate test tasks alongside implementation tasks

**DO create:**
- High-level feature tasks (e.g., "Add user authentication")
- Set `category: "code"` for tasks that will get TDD treatment
- Set `category: "document"` for docs (skips TDD)
- Set `category: "config"` for config changes (gets TDD)

**Example - What the skill creates:**
```json
{"title": "Add database schema", "category": "code"}
{"title": "Create API endpoint", "category": "code", "depends_on": ["Add database schema"]}
{"title": "Write API documentation", "category": "document"}
```

**After expand_task + apply_tdd, this becomes:**
- Add database schema (parent)
  - Write tests for: Add database schema
  - Implement: Add database schema
  - Refactor: Add database schema
- Create API endpoint (parent)
  - Write tests for: Create API endpoint
  - Implement: Create API endpoint
  - Refactor: Create API endpoint
- Write API documentation (no TDD - it's a document)

## Example Usage

User: `/gobby-spec`
Agent: "What feature would you like to plan?"
User: "Add dark mode support to the app"
Agent: [Asks clarifying questions]
Agent: [Writes spec to .gobby/specs/dark-mode.md]
Agent: "Here's the spec. Does this look correct?"
User: "Yes, create the tasks"
Agent: [Creates epic + phases + tasks]
Agent: "Created 12 tasks under epic #47. The spec has been updated with task refs."
