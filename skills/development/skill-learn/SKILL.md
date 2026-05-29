---
name: skill-learn
description: Scan codebase for FIX:/NOTE:/TODO: tags and create structured tasks with interactive selection. Invoke for /learn command.
allowed-tools: Bash, Grep, Read, Write, Edit, AskUserQuestion
---

# Learn Skill (Direct Execution)

Direct execution skill for scanning files, presenting findings interactively, and creating user-selected tasks. Replaces the previous delegation-based approach with synchronous execution and AskUserQuestion prompts.

**Key behavior**: Users always see tag scan results BEFORE any tasks are created. Users select which task types to create via interactive prompts.

## Context References

Reference (do not load eagerly):
- Path: `@specs/TODO.md` - Current task list
- Path: `@specs/state.json` - Machine state

---

## Execution

### Step 1: Parse Arguments

Extract paths from command input:

```bash
# Parse from command input
paths="$ARGUMENTS"

# Default to project root if no paths specified
if [ -z "$paths" ]; then
  paths="."
fi
```

**Note**: The `--dry-run` flag is no longer supported. The interactive flow is inherently "preview first" - users always see findings before any tasks are created.

### Step 2: Generate Session ID

Generate session ID for tracking:

```bash
session_id="sess_$(date +%s)_$(od -An -N3 -tx1 /dev/urandom | tr -d ' ')"
```

### Step 3: Execute Tag Extraction

Scan for tags using file-type-specific patterns. Use Bash with grep for consistent output parsing.

#### 3.1: Extract FIX: Tags

**Lua files (Neovim config)**:
```bash
grep -rn --include="*.lua" "-- FIX:" $paths 2>/dev/null || true
```

**LaTeX files**:
```bash
grep -rn --include="*.tex" "% FIX:" $paths 2>/dev/null || true
```

**Markdown files**:
```bash
grep -rn --include="*.md" "<!-- FIX:" $paths 2>/dev/null || true
```

**Python/Shell/YAML files**:
```bash
grep -rn --include="*.py" --include="*.sh" --include="*.yaml" --include="*.yml" "# FIX:" $paths 2>/dev/null || true
```

#### 3.2: Extract NOTE: Tags

Same patterns as above, replacing `FIX:` with `NOTE:`.

#### 3.3: Extract TODO: Tags

Same patterns as above, replacing `FIX:` with `TODO:`.

#### 3.4: Parse Results

For each grep match, extract:
- File path
- Line number
- Tag type (FIX, NOTE, TODO)
- Tag content (text after the tag)

Example raw output:
```
nvim/lua/plugins/telescope.lua:67:-- TODO: Add custom picker for git worktrees
docs/KEYMAPS.md:89:<!-- FIX: Update keymap table with new bindings -->
```

Categorize into three arrays:
- `fix_tags[]` - All FIX: tags
- `note_tags[]` - All NOTE: tags
- `todo_tags[]` - All TODO: tags

### Step 4: Display Tag Summary

Present findings to user BEFORE any selection:

```
## Tag Scan Results

**Files Scanned**: {paths}
**Tags Found**: {total_count}

### FIX: Tags ({count})
- `{file}:{line}` - {content}
- ...

### NOTE: Tags ({count})
- `{file}:{line}` - {content}
- ...

### TODO: Tags ({count})
- `{file}:{line}` - {content}
- ...
```

### Step 5: Handle Edge Cases

#### No Tags Found

If no tags found:
```
## No Tags Found

Scanned files in: {paths}
No FIX:, NOTE:, or TODO: tags detected.

Nothing to create.
```

Exit gracefully without prompts.

#### Only Certain Tag Types

Only show task type options for tag types that exist:
- FIX: tags exist -> offer "fix-it task"
- NOTE: tags exist -> offer "fix-it task" AND "learn-it task"
- TODO: tags exist -> offer "TODO tasks"

### Step 6: Task Type Selection

If tags were found, prompt user to select task types:

```json
{
  "question": "Which task types should be created?",
  "header": "Task Types",
  "multiSelect": true,
  "options": [
    {
      "label": "fix-it task",
      "description": "Combine {N} FIX:/NOTE: tags into single task"
    },
    {
      "label": "learn-it task",
      "description": "Update context from {N} NOTE: tags"
    },
    {
      "label": "TODO tasks",
      "description": "Create tasks for {N} TODO: items"
    }
  ]
}
```

**Important**: Only include options where the tag type exists:
- Include "fix-it task" only if FIX: or NOTE: tags exist
- Include "learn-it task" only if NOTE: tags exist
- Include "TODO tasks" only if TODO: tags exist

If user selects nothing, exit gracefully:
```
No task types selected. No tasks created.
```

### Step 7: Individual TODO Selection

If "TODO tasks" was selected AND there are TODO: tags:

#### Standard Case (<=20 TODOs)

```json
{
  "question": "Select TODO items to create as tasks:",
  "header": "TODO Selection",
  "multiSelect": true,
  "options": [
    {
      "label": "{content truncated to 50 chars}",
      "description": "{file}:{line}"
    },
    ...
  ]
}
```

#### Large Number of TODOs (>20)

Add a "Select all" option at the top:

```json
{
  "question": "Select TODO items to create as tasks:",
  "header": "TODO Selection (many items)",
  "multiSelect": true,
  "options": [
    {
      "label": "Select all ({N} items)",
      "description": "Create a task for every TODO tag"
    },
    {
      "label": "{content truncated to 50 chars}",
      "description": "{file}:{line}"
    },
    ...
  ]
}
```

If "Select all" is chosen, include all TODOs. Otherwise, only selected items.

### Step 7.5: Topic Grouping for TODO Items

**Condition**: User selected "TODO tasks" AND selected more than 1 TODO item

If only 1 TODO item was selected, skip to Step 8 (no grouping benefit).

#### 7.5.1: Extract Topic Indicators

For each selected TODO item, extract topic indicators:

**Key Terms**: Extract significant words from the TODO content (nouns, verbs). Ignore stop words (the, a, is, to, for, etc.).

**File Section**: Group by file path prefix (e.g., `Logos/Layer1/` vs `Logos/Shared/`).

**Action Type**: Identify common action patterns:
- "Add/Implement/Create" → implementation tasks
- "Fix/Handle/Correct" → fix tasks
- "Document/Update docs" → documentation tasks
- "Test/Verify" → testing tasks
- "Refactor/Optimize" → improvement tasks

Example extraction:
```
TODO: "Add custom picker for worktrees" at nvim/lua/plugins/telescope.lua:67
  → key_terms: ["picker", "worktrees", "telescope"]
  → file_section: "nvim/lua/plugins/"
  → action_type: "implementation"

TODO: "Add preview window for worktrees" at nvim/lua/plugins/telescope.lua:89
  → key_terms: ["preview", "worktrees", "telescope"]
  → file_section: "nvim/lua/plugins/"
  → action_type: "implementation"

TODO: "Optimize lazy loading" at nvim/lua/config/lazy.lua:23
  → key_terms: ["optimize", "lazy", "loading"]
  → file_section: "nvim/lua/config/"
  → action_type: "improvement"
```

#### 7.5.2: Cluster TODOs by Shared Terms

Group TODOs that share **2 or more significant terms** or share **file section + action type**.

**Clustering algorithm**:
1. Start with first TODO as initial group
2. For each remaining TODO:
   - If shares 2+ key terms with existing group → add to group
   - If shares file_section AND action_type with existing group → add to group
   - Otherwise → start new group
3. Generate topic label from most common shared terms in group

**Example clustering**:
```
Group 1: "Telescope Worktrees" (shared: worktrees, telescope, nvim/lua/plugins/, implementation)
  - Add custom picker for worktrees
  - Add preview window for worktrees

Group 2: "Config Optimization" (shared: nvim/lua/config/, improvement)
  - Optimize lazy loading
```

**Single-item groups**: If a TODO doesn't cluster with others, it becomes its own single-item group.

#### 7.5.3: Store Grouped Topics

Store the topic groups for use in Step 7.5.4:

```
topic_groups = [
  {
    label: "Telescope Worktrees",
    items: [
      {file: "nvim/lua/plugins/telescope.lua", line: 67, content: "Add custom picker for worktrees"},
      {file: "nvim/lua/plugins/telescope.lua", line: 89, content: "Add preview window for worktrees"}
    ],
    shared_terms: ["worktrees", "telescope"],
    action_type: "implementation"
  },
  {
    label: "Config Optimization",
    items: [
      {file: "nvim/lua/config/lazy.lua", line: 23, content: "Optimize lazy loading"}
    ],
    shared_terms: [],
    action_type: "improvement"
  }
]
```

### Step 7.5.4: Topic Group Confirmation

**Condition**: topic_groups contains at least one group with 2+ items

If all groups have only 1 item, skip to Step 8 (no grouping benefit).

Present topic groups via AskUserQuestion:

```json
{
  "question": "How should TODO items be grouped into tasks?",
  "header": "TODO Topic Grouping",
  "multiSelect": false,
  "options": [
    {
      "label": "Accept suggested topic groups",
      "description": "Creates {N} grouped tasks: {group_summaries}"
    },
    {
      "label": "Keep as separate tasks",
      "description": "Creates {M} individual tasks (one per TODO item)"
    },
    {
      "label": "Create single combined task",
      "description": "Creates 1 task containing all {M} TODO items"
    }
  ]
}
```

Where:
- `{N}` = number of topic groups
- `{M}` = total number of selected TODO items
- `{group_summaries}` = comma-separated list like "S5 Theorems (2 items), Utility Optimization (1 item)"

**Store user choice**: `grouping_mode = "grouped" | "separate" | "combined"`

### Step 8: Create Selected Tasks

For each selected task type, create the task. **Important**: When NOTE: tags exist and both fix-it and learn-it tasks are selected, create learn-it FIRST so fix-it can depend on it.

#### 8.1: Get Next Task Number

```bash
next_num=$(jq -r '.next_project_number' specs/state.json)
```

#### 8.2: Dependency-Aware Task Creation Order

**Check for NOTE: dependency condition**:
```
has_note_dependency = (NOTE: tags exist) AND (user selected both "fix-it task" AND "learn-it task")
```

**If has_note_dependency is TRUE**:
- Create learn-it task FIRST (Step 8.2a)
- Store learn-it task number as `learn_it_task_num`
- Create fix-it task SECOND with dependency (Step 8.2b)

**If has_note_dependency is FALSE**:
- Create fix-it task first (if selected)
- Create learn-it task second (if selected)
- No dependency relationship

#### 8.2a: Learn-It Task (when created first for dependency)

**Condition**: has_note_dependency is TRUE

```json
{
  "title": "Update context files from NOTE: tags",
  "description": "Update {N} context files based on learnings:\n\n{grouped by target context}",
  "language": "meta",
  "effort": "1-2 hours"
}
```

Store the task number: `learn_it_task_num = next_num`
Increment: `next_num = next_num + 1`

#### 8.2b: Fix-It Task (with dependency when has_note_dependency)

**Condition**: User selected "fix-it task" AND (FIX: or NOTE: tags exist)

**When has_note_dependency is TRUE**:
```json
{
  "title": "Fix issues from FIX:/NOTE: tags",
  "description": "Address {N} items from embedded tags:\n\n{list of items with file:line references}\n\n**Important**: When making changes, remove the FIX: and NOTE: tags from the source files. Leave TODO: tags untouched (they create separate tasks).",
  "language": "{predominant language from source files}",
  "effort": "2-4 hours",
  "dependencies": [learn_it_task_num]
}
```

**When has_note_dependency is FALSE**:
```json
{
  "title": "Fix issues from FIX:/NOTE: tags",
  "description": "Address {N} items from embedded tags:\n\n{list of items with file:line references}\n\n**Important**: When making changes, remove the FIX: and NOTE: tags from the source files. Leave TODO: tags untouched (they create separate tasks).",
  "language": "{predominant language from source files}",
  "effort": "2-4 hours"
}
```

**Language Detection**:
```
if majority of tags from .lean files -> "lean"
elif majority from .tex files -> "latex"
elif majority from .claude/ files -> "meta"
else -> "general"
```

#### 8.3: Learn-It Task (when created without dependency)

**Condition**: User selected "learn-it task" AND NOTE: tags exist AND has_note_dependency is FALSE

```json
{
  "title": "Update context files from NOTE: tags",
  "description": "Update {N} context files based on learnings:\n\n{grouped by target context}",
  "language": "meta",
  "effort": "1-2 hours"
}
```

#### 8.4: Todo-Tasks (if selected)

**Condition**: User selected "TODO tasks" AND user selected specific TODO items

**Check grouping_mode** (from Step 7.5.4, defaults to "separate" if Step 7.5.4 was skipped):

##### 8.4.1: Grouped Mode (grouping_mode == "grouped")

For each topic group in `topic_groups`:

```json
{
  "title": "{topic_label}: {item_count} TODO items",
  "description": "Address TODO items related to {topic_label}:\n\n{item_list}\n\n---\n\nShared context: {shared_terms_description}",
  "language": "{detected from majority file type in group}",
  "effort": "{scaled_effort}"
}
```

Where:
- `{topic_label}` = generated label (e.g., "Telescope Worktrees")
- `{item_count}` = number of items in group
- `{item_list}` = formatted list of items:
  ```
  - [ ] {content} (`{file}:{line}`)
  - [ ] {content} (`{file}:{line}`)
  ```
- `{shared_terms_description}` = brief description of why items are grouped (e.g., "Related to telescope worktree functionality")

**Effort Scaling Formula**:
```
base_effort = 1 hour
scaled_effort = base_effort + (30 min * (item_count - 1))

Examples:
  1 item  → 1 hour
  2 items → 1.5 hours (1h + 30min)
  3 items → 2 hours (1h + 60min)
  4 items → 2.5 hours (1h + 90min)
```

##### 8.4.2: Combined Mode (grouping_mode == "combined")

Create single task containing all selected TODO items:

```json
{
  "title": "Address {item_count} TODO items",
  "description": "Combined TODO items from scan:\n\n{all_items_list}\n\n---\n\nFiles: {unique_files_list}",
  "language": "{detected from majority file type}",
  "effort": "{scaled_effort}"
}
```

Where:
- `{item_count}` = total number of selected TODO items
- `{all_items_list}` = formatted list of all items with checkboxes
- `{unique_files_list}` = comma-separated list of unique files involved

**Effort Scaling**: Same formula as grouped mode.

##### 8.4.3: Separate Mode (grouping_mode == "separate" or default)

For each selected TODO item individually:

```json
{
  "title": "{tag content, truncated to 60 chars}",
  "description": "{full tag content}\n\nSource: {file}:{line}",
  "language": "{detected from file type}",
  "effort": "1 hour"
}
```

**Language Detection for Todo-Task** (all modes):
```
.lua (nvim/) -> "neovim"
.tex  -> "latex"
.md   -> "markdown"
.py/.sh -> "general"
.claude/* -> "meta"
```

### Step 9: Update State Files

For each task created:

#### 9.1: Update state.json

Read current state, add new task entry, increment next_project_number:

```bash
# Create slug from title
slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd 'a-z0-9_' | cut -c1-50)

# Read current state
current=$(cat specs/state.json)

# Add task using jq (use two-step pattern to avoid escaping issues)
# Step 1: Write task data to temp file
# Step 2: Use jq with slurpfile
```

**For fix-it task when has_note_dependency is TRUE**, include dependencies array:
```json
{
  "project_number": {N},
  "project_name": "{slug}",
  "status": "not_started",
  "language": "{language}",
  "dependencies": [learn_it_task_num]
}
```

**For all other tasks**, no dependencies field needed.

#### 9.2: Update TODO.md

Prepend new task entry to `## Tasks` section (new tasks at top):

**Standard format (no dependency)**:
```markdown
### {N}. {Title}
- **Effort**: {estimate}
- **Status**: [NOT STARTED]
- **Language**: {language}
- **Started**: {timestamp}

**Description**: {description}

---
```

**Fix-it task format when has_note_dependency is TRUE**:
```markdown
### {N}. {Title}
- **Effort**: {estimate}
- **Status**: [NOT STARTED]
- **Language**: {language}
- **Dependencies**: {learn_it_task_num}
- **Started**: {timestamp}

**Description**: {description}

---
```

### Step 10: Display Results

Show summary of created tasks:

```
## Tasks Created from Tags

**Tags Processed**: {N} across scanned files

### Created Tasks

| # | Type | Title | Language |
|---|------|-------|----------|
| {N} | fix-it | Fix issues from FIX:/NOTE: tags | {lang} |
| {N+1} | learn-it | Update context files from NOTE: tags | meta |
| {N+2} | todo | {title} | {lang} |

---

**Next Steps**:
1. Review tasks in TODO.md
2. Run `/research {first_task}` to begin
3. Progress through /research -> /plan -> /implement cycle
```

### Step 11: Git Commit (Postflight)

If tasks were created, commit changes:

```bash
task_count={number of tasks created}
git add specs/TODO.md specs/state.json
git commit -m "learn: create $task_count tasks from tags

Session: $session_id

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Error Handling

### Path Access Errors

When paths don't exist or can't be accessed:
1. Log warning for each invalid path
2. Continue with valid paths
3. If no valid paths remain, report and exit

### No Tags Found

This is NOT an error condition:
- Report informatively
- Exit without prompts

### state.json Update Failure

If jq fails:
1. Log error with command and output
2. Try two-step jq pattern
3. If still failing, report partial success (tags found but tasks not created)

### TODO.md Parse Error

If TODO.md format is corrupted:
1. Log error
2. Skip TODO.md update
3. State.json update may still succeed
4. Report partial success

### Git Commit Failure

Non-blocking:
1. Log the failure
2. Tasks are still created successfully
3. Report that commit failed but tasks exist

---

## Standards Reference

This skill implements the multi-task creation pattern. See `.claude/docs/reference/standards/multi-task-creation-standard.md` for the complete standard.

**Compliance Level**: Full (all required components)

| Component | Status | Notes |
|-----------|--------|-------|
| Discovery | Yes | Tag scanning (FIX:, NOTE:, TODO:) |
| Selection | Yes | AskUserQuestion with multiSelect |
| Grouping | Yes | Topic clustering (Step 7.5) |
| Dependencies | Partial | Internal only (learn-it -> fix-it in Step 8.2) |
| Ordering | No | Sequential creation |
| Visualization | No | Not implemented |
| Confirmation | Yes | Implicit via selection |
| State Updates | Yes | Atomic updates (Step 9) |

**Limitation**: External dependencies (TODO tasks depending on existing tasks) not implemented. Consider as future enhancement.
