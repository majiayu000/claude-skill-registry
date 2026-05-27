---
name: docs-stories
description: Complete CRUD for SDLC documentation (stories, tasks, context retrieval). Use when creating/managing stories, creating/managing tasks, updating task state, or retrieving full context for any user story via index (<3min restoration).
---

# docs-stories Skill

## Purpose

Provide complete CRUD operations for SDLC documentation in the Bestays project. This skill handles all story/task management and context retrieval operations.

**Single Interface:** Anytime you need to read/write anything about the codebase in terms of documenting, use this skill.

## When to Use This Skill

**CREATE:**
- Creating new user stories
- Creating new tasks for stories

**READ:**
- Finding stories by domain or keywords
- Listing tasks for a story
- Getting current active task
- **Retrieving full context for a user story** (via index)
- **Finding all files/commits/decisions for a story** (via index)

**UPDATE:**
- Updating task state (NOT_STARTED, IN_PROGRESS, COMPLETED)
- Updating task phase (RESEARCH, PLANNING, IMPLEMENTATION, TESTING, VALIDATION)
- Adding commits to task record
- Adding modified files to task record
- Setting current active task

**DELETE:**
- Not implemented (stories/tasks are permanent audit trail)

## Available Scripts

All scripts located in: `.claude/skills/docs-stories/scripts/`

### Story Management

#### `story_create.py` - Create New User Story

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/story_create.py <domain> <feature> <scope>
```

**Arguments:**
- `domain`: Story category (auth, booking, admin, infrastructure, etc.)
- `feature`: Main feature name (login, signup, dashboard, etc.)
- `scope`: Specific scope (admin, user, validation, etc.)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/story_create.py auth login admin
# Creates: .sdlc-workflow/stories/auth/US-001-auth-login-admin.md
```

**What it does:**
1. Scans existing stories to find next story number
2. Creates story file from template
3. Replaces placeholders with provided values
4. Returns story ID and file path

---

#### `story_find.py` - Find Existing Stories

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/story_find.py [domain] [--status STATUS]
```

**Arguments:**
- `domain` (optional): Filter by domain (auth, booking, etc.)
- `--status` (optional): Filter by status (READY, IN_PROGRESS, COMPLETED)

**Examples:**
```bash
# Find all stories
python3 .claude/skills/docs-stories/scripts/story_find.py

# Find all auth stories
python3 .claude/skills/docs-stories/scripts/story_find.py auth

# Find all completed stories
python3 .claude/skills/docs-stories/scripts/story_find.py --status COMPLETED

# Find completed auth stories
python3 .claude/skills/docs-stories/scripts/story_find.py auth --status COMPLETED
```

**What it does:**
1. Scans `.sdlc-workflow/stories/` for story files
2. Parses story metadata (status, domain, title)
3. Filters by criteria
4. Returns list of matching stories

---

### Task Management

#### `task_create.py` - Create New Task

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_create.py <story_id> <task_number> <semantic_name>
```

**Arguments:**
- `story_id`: Parent story ID (e.g., US-001)
- `task_number`: Task number (1, 2, 3, etc.)
- `semantic_name`: Semantic slug (2-3 words, lowercase, hyphens)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_create.py US-001 1 clerk-mounting
# Creates: .claude/tasks/TASK-001/
# With STATE.json: {"story": "US-001", "semantic_name": "clerk-mounting", ...}
```

**What it does:**
1. Creates task folder at `.claude/tasks/TASK-{number}/`
2. Creates phase subfolders (research/, planning/, etc.)
3. Creates STATE.json with metadata
4. Creates README.md from template
5. Returns task ID and folder path

---

#### `task_list.py` - List Tasks for Story

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_list.py <story_id>
```

**Arguments:**
- `story_id`: Story ID to list tasks for (e.g., US-001)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_list.py US-001
# Returns:
# TASK-001 (clerk-mounting): IN_PROGRESS, PLANNING phase
# TASK-002 (login-tests): NOT_STARTED, RESEARCH phase
```

**What it does:**
1. Scans `.claude/tasks/` for tasks with matching story
2. Reads STATE.json for each task
3. Returns list with status and phase

---

#### `task_get_current.py` - Get Current Active Task

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_get_current.py
```

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_get_current.py
# Returns: TASK-001 (US-001, clerk-mounting)
```

**What it does:**
1. Checks current git branch for TASK-XXX reference
2. Reads task STATE.json
3. Returns current task details

---

#### `task_set_current.py` - Set Current Active Task

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_set_current.py <task_id>
```

**Arguments:**
- `task_id`: Task ID to make active (e.g., TASK-001)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_set_current.py TASK-001
# Switches to task branch or updates tracking
```

**What it does:**
1. Validates task exists
2. Updates tracking (implementation depends on approach)
3. Returns confirmation

---

#### `task_update_state.py` - Update Task Status

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_update_state.py <task_id> <status>
```

**Arguments:**
- `task_id`: Task ID (e.g., TASK-001)
- `status`: New status (NOT_STARTED, IN_PROGRESS, COMPLETED)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_update_state.py TASK-001 IN_PROGRESS
# Updates STATE.json: {"status": "IN_PROGRESS", ...}
```

**What it does:**
1. Reads task STATE.json
2. Updates status field
3. Updates timestamp
4. Writes back to STATE.json

---

#### `task_update_phase.py` - Update Task Phase

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_update_phase.py <task_id> <phase>
```

**Arguments:**
- `task_id`: Task ID (e.g., TASK-001)
- `phase`: New phase (RESEARCH, PLANNING, IMPLEMENTATION, TESTING, VALIDATION)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_update_phase.py TASK-001 PLANNING
# Updates STATE.json: {"phase": "PLANNING", ...}
```

**What it does:**
1. Reads task STATE.json
2. Updates phase field
3. Updates timestamp
4. Writes back to STATE.json

---

#### `task_add_commit.py` - Add Commit to Task Record

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_add_commit.py <task_id> <commit_hash>
```

**Arguments:**
- `task_id`: Task ID (e.g., TASK-001)
- `commit_hash`: Git commit hash

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_add_commit.py TASK-001 abc123def
# Updates STATE.json: {"commits": ["abc123def"], ...}
```

**What it does:**
1. Reads task STATE.json
2. Appends commit hash to commits array
3. Writes back to STATE.json

---

#### `task_add_file_modified.py` - Add Modified File to Task Record

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/task_add_file_modified.py <task_id> <file_path>
```

**Arguments:**
- `task_id`: Task ID (e.g., TASK-001)
- `file_path`: Path to modified file (relative to project root)

**Example:**
```bash
python3 .claude/skills/docs-stories/scripts/task_add_file_modified.py TASK-001 apps/server/core/clerk.py
# Updates STATE.json: {"files_modified": ["apps/server/core/clerk.py"], ...}
```

**What it does:**
1. Reads task STATE.json
2. Appends file path to files_modified array (no duplicates)
3. Writes back to STATE.json

---

### Context Indexing and Retrieval

#### `context_index.py` - Index All SDLC Artifacts

**Status:** To be implemented (US-001D)

**Usage:**
```bash
python3 .claude/skills/docs-stories/scripts/context_index.py [--story-id US-XXX] [--output PATH]
```

**Arguments:**
- `--story-id` (optional): Index specific story only
- `--output` (optional): Output path (default: `.sdlc-workflow/.index/sdlc-index.json`)

**Example:**
```bash
# Index all stories
python3 .claude/skills/docs-stories/scripts/context_index.py

# Index specific story
python3 .claude/skills/docs-stories/scripts/context_index.py --story-id US-001

# Custom output path
python3 .claude/skills/docs-stories/scripts/context_index.py --output /tmp/index.json
```

**What it does:**
1. Scans `.sdlc-workflow/stories/` for story files
2. Scans `.claude/tasks/` for task folders
3. Parses git log for commits with story/task references
4. Parses file headers for design patterns and trade-offs
5. Builds structured JSON index with bidirectional cross-references
6. Outputs: `.sdlc-workflow/.index/sdlc-index.json`

**Index Schema:**
```json
{
  "metadata": {
    "generated": "2025-11-07T10:30:00Z",
    "total_stories": 5,
    "total_tasks": 12
  },
  "stories": {
    "US-001": {
      "id": "US-001",
      "title": "Login Flow Validation",
      "file": ".sdlc-workflow/stories/auth/US-001-...",
      "tasks": ["TASK-001-file-headers"],
      "commits": ["abc123"],
      "implementation_files": ["apps/frontend/tests/..."]
    }
  },
  "tasks": {
    "TASK-001-file-headers": {
      "story": "US-001",
      "folder": ".claude/tasks/TASK-001/",
      "decisions": "...",
      "files_modified": ["..."]
    }
  },
  "commits": {...},
  "files": {...}
}
```

---

## Retrieving Full Context for a Story

Once the index is built, retrieve full context:

### Step 1: Read the Index

```python
import json
with open('.sdlc-workflow/.index/sdlc-index.json') as f:
    index = json.load(f)
```

### Step 2: Query by Story ID

```python
story = index['stories']['US-001']
# Returns: title, file, tasks, commits, files, acceptance_criteria
```

### Step 3: Traverse Cross-References

```python
# Get all tasks for story
tasks = [index['tasks'][task_id] for task_id in story['tasks']]

# Get all commits for story
commits = [index['commits'][commit_hash] for commit_hash in story['commits']]

# Get all files for story
files = [index['files'][file_path] for file_path in story['implementation_files']]
```

### Common Query Templates

#### Query: "Full context for US-001"

**Steps:**
1. Read index
2. Get story metadata (title, acceptance criteria)
3. Get all tasks (semantic names, decisions, subagents)
4. Get all commits (timeline)
5. Get all files (design patterns, trade-offs)
6. Format output for readability

**Expected Output:**
```markdown
# Full Context: US-001 - Login Flow Validation

## Story
- Title: Login Flow Validation
- Status: COMPLETED
- Acceptance Criteria:
  - Valid credentials authenticate user
  - Invalid credentials rejected
  - E2E tests passing

## Tasks
1. TASK-001-file-headers
   - Decision: Add file headers with design patterns for instant context
   - Trade-offs: Maintenance overhead vs clarity
   - Subagent: dev-backend-fastapi

## Timeline
- 2025-10-16: feat: add file headers (abc123)
- 2025-10-20: test: add E2E login tests (def456)

## Files Modified
- apps/server/core/clerk.py
  - Design Pattern: Singleton
  - Architecture Layer: Core Service
  - Trade-offs: Vendor lock-in vs faster development

## Time to Context: < 3 minutes
```

---

#### Query: "Files changed in US-001"

**Steps:**
1. Read index
2. Get story['implementation_files']
3. For each file, get metadata (design pattern, layer, trade-offs)
4. Format as list

**Expected Output:**
```
Files changed in US-001:
- apps/server/core/clerk.py (Singleton, Core Service)
- apps/server/api/clerk_deps.py (Dependency Injection, API Layer)
- apps/frontend/tests/e2e/login.spec.ts (Test, E2E Layer)
```

---

#### Query: "Timeline for US-001"

**Steps:**
1. Read index
2. Get story['commits']
3. Sort by date
4. Format chronologically

**Expected Output:**
```
Timeline for US-001:
- 2025-10-16 14:30: feat: add file headers to backend deps (abc123)
  Files: clerk.py, deps.py
  Task: TASK-001-file-headers

- 2025-10-20 10:15: test: add E2E login tests (def456)
  Files: login.spec.ts
  Task: TASK-002-login-tests
```

---

#### Query: "Decisions for US-001"

**Steps:**
1. Read index
2. Get all tasks for story
3. Extract decisions field from each task
4. Format as list

**Expected Output:**
```
Decisions for US-001:

TASK-001-file-headers:
- Chose Clerk over Auth0 for authentication
- Trade-offs: Vendor lock-in vs faster development
- Added file headers with design patterns for instant context

TASK-002-login-tests:
- Chose Playwright over Cypress for E2E tests
- Trade-offs: Newer tool vs more examples available
```

---

#### Query: "Trade-offs for authentication"

**Steps:**
1. Read index
2. Search files for "authentication" or "auth" keywords
3. Extract trade-offs sections from file headers
4. Format as list

**Expected Output:**
```
Trade-offs for authentication:

apps/server/core/clerk.py (Singleton):
- Pro: Shared Clerk client reduces memory usage
- Con: Vendor lock-in to Clerk
- When to revisit: If Clerk pricing becomes prohibitive

apps/server/api/clerk_deps.py (Dependency Injection):
- Pro: Easy to mock for testing
- Con: Extra indirection layer
```

---

## Performance Expectations

**Indexing:**
- Time: < 10 seconds for 20 stories, 50 tasks, 150 commits
- Memory: < 500MB
- Output: < 2MB JSON file

**Retrieval:**
- Full context for any story: **< 3 minutes** (vs 30-60 minutes manual)
- Files changed query: < 30 seconds
- Timeline query: < 30 seconds
- Decisions query: < 30 seconds

---

## Integration with Other Skills

**sdlc-orchestrator skill:**
- Orchestrator uses docs-stories to update task state during phase transitions
- Example: After completing planning phase, orchestrator calls `task_update_phase.py TASK-001 IMPLEMENTATION`

**planning-quality-gates skill:**
- Quality gates reference docs-stories for creating planning artifacts
- Example: Create `planning/quality-gate-checklist.md` via task folder structure

**Memory MCP:**
- Coordinator loads SDLC patterns from Memory MCP before using docs-stories
- Example: Load "Task Folder System" entity to understand structure

---

## Best Practices

**For Coordinators:**
1. Always use docs-stories for story/task CRUD operations (don't manually create files)
2. Update task state after each phase transition
3. Run context_index.py periodically (after completing stories)
4. Use retrieval queries to restore context in new sessions

**For Subagents:**
1. Read task STATE.json to understand current task context
2. Add commits and files_modified after implementation
3. Reference task folder for implementation spec and decisions
4. Save reports to task folder (subagent-reports/)

**For Both:**
- Never bypass docs-stories scripts (maintain consistency)
- Always use semantic task names (self-documenting)
- Document decisions and trade-offs in task folders
- Update STATE.json after significant progress

---

## Troubleshooting

**Problem:** `story_create.py` fails with "Not in a project with .claude/"
**Solution:** Run from project root or any subdirectory containing `.claude/`

**Problem:** `task_create.py` fails with "Task already exists"
**Solution:** Use different task number or delete existing task folder

**Problem:** Index is outdated after new commits
**Solution:** Re-run `context_index.py` to rebuild index

**Problem:** Context retrieval returns no results for recent story
**Solution:** Ensure story file exists and index has been built

---

## Future Enhancements (Out of Scope)

- Delete operations (story/task archival)
- Story/task templates with variants
- Incremental indexing (only scan changed files)
- Web UI for browsing index
- Full-text search across decisions and reports
- Automated index rebuild on git commit (hook)

---

**Skill Version:** 1.0
**Last Updated:** 2025-11-07
**Maintained By:** Bestays SDLC Team
