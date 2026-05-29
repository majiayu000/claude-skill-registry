---
name: aico-pm-story-acceptance
description: |
  Verify and close stories after frontend/backend tasks are completed. Check ALL related task files, update story acceptance criteria checkboxes.

  UNIQUE VALUE: Ensures BOTH frontend AND backend tasks are verified before closing story. Prevents premature story closure.

  Use this skill when:
  - Frontend or backend notifies "task completed, please verify"
  - User asks to "verify story", "accept story", "close story", "mark story done"
  - Need to check if a story can be marked as complete
  - User asks "is story X done?", "can we close story X?"

  CRITICAL: Must check BOTH frontend tasks (docs/reference/frontend/tasks/) AND backend tasks (docs/reference/backend/tasks/) before closing.
  Output: Update story file checkboxes from `- [ ]` to `- [x]`
---

# Story Acceptance

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Identify the story**: Get story ID (e.g., S-001) from notification or user
2. **Read the story**: Load `docs/reference/pm/stories/{story-id}.md`
3. **Find related tasks** (use Strategy 1 if available, fallback to Strategy 2):
   - **Strategy 1 (Preferred)**: Read "Related Tasks" section from story file
     - Story file should contain task list created by task-breakdown
     - Directly read the listed task files
   - **Strategy 2 (Fallback)**: Pattern matching in task directories
     - Extract story name from story filename (e.g., "user-profile" from "user-profile.md")
     - Search `docs/reference/frontend/tasks/` for `story-{story-name}-*.md`
     - Search `docs/reference/backend/tasks/` for `story-{story-name}-*.md`
4. **Verify all tasks completed**:
   - Read each task file's `> **Status**:` field
   - All task statuses should be `completed`
   - No `pending` or `in_progress` tasks remaining
5. **Update story**:
   - If ALL tasks completed → Update acceptance criteria `- [ ]` to `- [x]`
   - If partial → Report progress, list incomplete tasks

## Verification Checklist

```markdown
## Story: S-XXX

### Frontend Tasks

- [x] docs/reference/frontend/tasks/s-xxx.md - All completed

### Backend Tasks

- [x] docs/reference/backend/tasks/s-xxx.md - All completed

### Result: ✅ Ready to close / ⏳ Waiting for tasks
```

## Task Status Mapping

| Task Status      | Meaning           |
| ---------------- | ----------------- |
| `✅ completed`   | Task done         |
| `🔄 in_progress` | Currently working |
| `⏳ pending`     | Not started       |

## Story Update Format

When all tasks are complete, update the story file:

```markdown
## Acceptance Criteria

- [x] Criterion 1 (was `- [ ]`)
- [x] Criterion 2 (was `- [ ]`)
- [x] Criterion 3 (was `- [ ]`)
```

## Decision Logic

```
Has frontend tasks? ──Yes──> Check frontend/tasks/{story}.md
        │                            │
        No                     All completed?
        │                       │        │
        ▼                      Yes       No
Has backend tasks? ──Yes──> Check backend/tasks/{story}.md
        │                            │
        No                     All completed?
        │                       │        │
        ▼                      Yes       No
All checks passed? ─────────────┘        │
        │                                │
       Yes                              No
        │                                │
        ▼                                ▼
Update story checkboxes          Report incomplete tasks
```

## Key Rules

- MUST check BOTH frontend and backend tasks before closing
- ONLY update story when ALL related tasks are completed
- ALWAYS report which tasks are still pending if not ready to close
- Use exact checkbox format: `- [x]` for completed, `- [ ]` for pending

## Output Examples

### All Complete

```
## Story S-001 Acceptance Result

✅ **Ready to Close**

### Task Check
- Frontend: 3/3 completed
- Backend: 2/2 completed

Story acceptance criteria updated.
```

### Partial Complete

```
## Story S-001 Acceptance Result

⏳ **Waiting for Tasks**

### Task Check
- Frontend: 3/3 completed ✅
- Backend: 1/2 completed ⏳

### Incomplete Tasks
- [ ] Backend Task 2: Implement API endpoint
```

## Common Mistakes

- ❌ Close story with pending tasks → ✅ Check ALL related tasks first
- ❌ Only check frontend OR backend → ✅ Check BOTH if story has both
- ❌ Forget to update checkboxes → ✅ Always update `- [ ]` to `- [x]`
