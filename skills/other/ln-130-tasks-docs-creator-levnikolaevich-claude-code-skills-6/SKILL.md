---
name: ln-130-tasks-docs-creator
description: Creates task management documentation (docs/tasks/README.md + kanban_board.md). L2 Worker in ln-100-documents-pipeline. Sets up Linear integration and task tracking rules.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Tasks Documentation Creator

This skill creates task management documentation: docs/tasks/README.md (task management system rules) and docs/tasks/kanban_board.md (Linear integration with Epic Story Counters).

## Purpose

Create and validate task management documentation (docs/tasks/). Generates README.md with workflow rules and kanban_board.md with Linear integration, including interactive setup for team UUID/Key configuration.

## When to Use This Skill

**This skill is a L2 WORKER** invoked by **ln-100-documents-pipeline** orchestrator OR used standalone.

Use this skill when:
- Creating task management documentation (docs/tasks/)
- Setting up Linear integration and kanban board
- Validating existing task documentation structure and content
- Configuring Linear team settings (Team Name, UUID, Key)

**Part of workflow**: ln-100-documents-pipeline → ln-110-project-docs-coordinator → ln-120-reference-docs-creator → **ln-130-tasks-docs-creator** → ln-140-test-docs-creator (optional) → ln-150-presentation-creator

## Workflow

The skill follows a **3-phase workflow**: CREATE → VALIDATE STRUCTURE → VALIDATE CONTENT.

**Phase 1: CREATE** - Create tasks/README.md from template with SCOPE tags, workflow rules, Linear integration
**Phase 2: VALIDATE STRUCTURE** - Auto-fix structural violations (SCOPE tags, sections, Maintenance, POSIX)
**Phase 3: VALIDATE CONTENT** - Validate semantic content + special Linear Configuration handling (placeholder detection, UUID/Team Key validation, interactive user prompts)

---

## Phase 1: Create tasks/README.md

**Objective**: Create task management system documentation from template.

**When to execute**: Always (first phase)

**Process**:

1. **Check if tasks/README.md exists**:
   - Use Glob tool: `pattern: "docs/tasks/README.md"`
   - If file exists:
     - Skip creation
     - Log: `✓ docs/tasks/README.md already exists (preserved)`
     - Proceed to Phase 2
   - If NOT exists:
     - Continue to step 2

2. **Create tasks directory**:
   - Create the `docs/tasks/` directory if it doesn't exist

3. **Create tasks/README.md from template**:
   - Copy template: `references/tasks_readme_template.md` (v2.0.0) → `docs/tasks/README.md`
   - Replace placeholders:
     - `{{DATE}}` → current date (YYYY-MM-DD)
   - Template contains:
     - SCOPE tags: `<!-- SCOPE: Task tracking system workflow and rules ONLY -->`
     - Story-Level Test Task Pattern
     - Kanban Board Structure (Epic Grouping Pattern)
     - Linear Integration (MCP methods)
     - Maintenance section

4. **Notify user**:
   - If created: `✓ Created docs/tasks/README.md with task management rules`
   - If skipped: `✓ docs/tasks/README.md already exists (preserved)`

**Output**: docs/tasks/README.md (created or existing)

---

## Phase 2: Validate Structure

**Objective**: Ensure tasks/README.md and kanban_board.md comply with structural requirements. Auto-fix violations.

**When to execute**: After Phase 1 completes (files exist or created)

**Process**:

### 2.1 Validate SCOPE tags

**Files to check**: docs/tasks/README.md, docs/tasks/kanban_board.md (if exists)

For each file:
1. Read first 5 lines
2. Check for `<!-- SCOPE: ... -->` tag
3. Expected values:
   - tasks/README.md: `<!-- SCOPE: Task tracking system workflow and rules ONLY -->`
   - kanban_board.md: `<!-- SCOPE: Quick navigation to active tasks in Linear -->`
4. **If missing:**
   - Use Edit tool to add SCOPE tag after first heading
   - Log: `⚠ Auto-fixed: Added missing SCOPE tag to {filename}`

### 2.2 Validate required sections

**Load validation spec**:
- Read `references/questions.md`
- Extract section names from questions

**For tasks/README.md**:
- Required sections (from questions.md):
  - "Linear Integration" OR "Core Concepts" (Linear MCP methods)
  - "Task Workflow" OR "Critical Rules" (state transitions)
  - "Task Templates" (template references)
- For each section:
  - Check if section header exists (case-insensitive)
  - **If missing:**
    - Use Edit tool to add section with placeholder content
    - Log: `⚠ Auto-fixed: Added missing section '{section}' to tasks/README.md`

**For kanban_board.md** (if exists):
- Required sections:
  - "Linear Configuration" (Team Name, UUID, Key)
  - "Work in Progress" OR "Epic Tracking" (Kanban sections)
- For each section:
  - Check if section header exists
  - **If missing:**
    - Use Edit tool to add section with placeholder
    - Log: `⚠ Auto-fixed: Added missing section '{section}' to kanban_board.md`

### 2.3 Validate Maintenance section

**Files to check**: docs/tasks/README.md, docs/tasks/kanban_board.md (if exists)

For each file:
1. Search for `## Maintenance` header in last 20 lines
2. **If missing:**
   - Use Edit tool to add at end of file:
     ```markdown
     ## Maintenance

     **Update Triggers:**
     - When Linear workflow changes
     - When task templates are added/modified
     - When label taxonomy changes

     **Last Updated:** {current_date}
     ```
   - Log: `⚠ Auto-fixed: Added Maintenance section to {filename}`

### 2.4 Validate POSIX line endings

**Files to check**: docs/tasks/README.md, docs/tasks/kanban_board.md (if exists)

For each file:
1. Check if file ends with single newline character
2. **If missing:**
   - Use Edit tool to add final newline
   - Log: `⚠ Auto-fixed: Added POSIX newline to {filename}`

### 2.5 Report validation summary

Log summary:
```
✓ Structure validation completed:
  tasks/README.md:
    - SCOPE tag: [added/present]
    - Required sections: [count] sections [added/present]
    - Maintenance section: [added/present]
    - POSIX endings: [fixed/compliant]
  kanban_board.md:
    - SCOPE tag: [added/present/skipped - file not exists]
    - Required sections: [count] sections [added/present/skipped]
    - Maintenance section: [added/present/skipped]
    - POSIX endings: [fixed/compliant/skipped]
```

If violations found: `⚠ Auto-fixed {total} structural violations`

**Output**: Structurally valid task management documentation

---

## Phase 3: Validate Content

**Objective**: Ensure each section answers its validation questions with meaningful content. Special handling for Linear Configuration (placeholder detection, user prompts, UUID/Team Key validation).

**When to execute**: After Phase 2 completes (structure valid, auto-fixes applied)

**Process**:

### 3.1 Load validation spec

1. Read `references/questions.md`
2. Parse document sections and questions
3. Extract validation heuristics for each section

### 3.2 Validate kanban_board.md → Linear Configuration (Special Handling)

**Question**: "What is the Linear team configuration?"

**Step 3.2.1: Check if kanban_board.md exists**:
- Use Glob tool: `pattern: "docs/tasks/kanban_board.md"`
- If NOT exists:
  - Log: `ℹ kanban_board.md not found - skipping Linear Configuration validation`
  - Skip to Step 3.3
- If exists:
  - Continue to Step 3.2.2

**Step 3.2.2: Read Linear Configuration section**:
- Read `docs/tasks/kanban_board.md`
- Locate `## Linear Configuration` section
- Extract Team Name, Team UUID, Team Key values

**Step 3.2.3: Placeholder Detection**:

Check for placeholders:
```
Pattern: [TEAM_NAME], [TEAM_UUID], [TEAM_KEY]
If ANY placeholder present → Interactive Setup Mode
If NO placeholders present → Validation Mode
```

**Interactive Setup Mode** (if placeholders detected):

1. **Prompt user for Team Name**:
   - Question: "What is your Linear Team Name?"
   - Validation: Non-empty string
   - Example: "My Project Team"

2. **Prompt user for Team UUID**:
   - Question: "What is your Linear Team UUID?"
   - Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - Validation Regex: `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/`
   - **If invalid:**
     - Show error: "Invalid UUID format. Expected: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (lowercase hex)"
     - Re-prompt user
   - Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

3. **Prompt user for Team Key**:
   - Question: "What is your Linear Team Key (2-4 uppercase letters)?"
   - Format: 2-4 uppercase letters
   - Validation Regex: `/^[A-Z]{2,4}$/`
   - **If invalid:**
     - Show error: "Invalid Team Key format. Expected: 2-4 uppercase letters (e.g., PROJ, WEB, API)"
     - Re-prompt user
   - Example: "PROJ"

4. **Replace placeholders**:
   - Use Edit tool to replace in kanban_board.md:
     - `[TEAM_NAME]` → `{user_team_name}`
     - `[TEAM_UUID]` → `{user_team_uuid}`
     - `[TEAM_KEY]` → `{user_team_key}`
     - `[WORKSPACE_URL]` → `https://linear.app/{workspace_slug}` (if placeholder exists)

5. **Set initial counters** (if table exists):
   - Set "Next Epic Number" → 1
   - Set "Next Story Number" → 1

6. **Update Last Updated date**:
   - Replace `[YYYY-MM-DD]` → `{current_date}` in Maintenance section

7. **Save updated kanban_board.md**

8. **Log success**:
   ```
   ✓ Linear configuration updated:
     - Team Name: {user_team_name}
     - Team UUID: {user_team_uuid}
     - Team Key: {user_team_key}
     - Next Epic Number: 1
     - Next Story Number: 1
   ```

**Validation Mode** (if real values present, no placeholders):

1. **Extract existing values**:
   - Extract Team UUID from line matching: `Team UUID: {value}` or in table
   - Extract Team Key from line matching: `Team Key: {value}` or in table

2. **Validate formats**:
   - UUID: `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/`
   - Team Key: `/^[A-Z]{2,4}$/`

3. **If validation fails**:
   ```
   ⚠ Invalid format detected in Linear Configuration:
     - Team UUID: {uuid} (expected: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
     - Team Key: {key} (expected: 2-4 uppercase letters)

   Fix manually or re-run skill to replace with correct values.
   ```
   - Mark as invalid but continue (don't block)

4. **If validation passes**:
   ```
   ✓ Linear Configuration valid (Team: {name}, UUID: {uuid}, Key: {key})
   ```

### 3.3 Validate tasks/README.md sections

**Parametric loop for 3 questions** (from questions.md):

For each question in:
1. "How is Linear integrated into the task management system?"
2. "What are the task state transitions and review criteria?"
3. "What task templates are available and how to use them?"

**Validation process**:
1. Extract validation heuristics from questions.md
2. Read corresponding section content from tasks/README.md
3. Check if **ANY** heuristic passes:
   - Contains keyword X → pass
   - Has pattern Y → pass
   - Length > N words → pass
4. If ANY passes → Section valid
5. If NONE passes → Log warning: `⚠ Section may be incomplete: {section_name}`

**Example validation (Question 1: Linear Integration)**:
```
Heuristics:
- Contains "Linear" or "MCP" → pass
- Mentions team ID or UUID → pass
- Has workflow states (Backlog, Todo, In Progress) → pass
- Length > 100 words → pass

Check content:
- ✓ Contains "Linear" → PASS
→ Section valid
```

**No auto-discovery needed** (workflow is standardized in template)

### 3.4 Validate kanban_board.md → Epic Tracking

**Question**: "Are Epics being tracked in the board?"

**If kanban_board.md exists**:

**Validation heuristics**:
```
- Has "Epic" or "Epics Overview" section header → pass
- Has table with columns: Epic, Name, Status, Progress → pass
- OR has placeholder: "No active epics" → pass
- Length > 20 words → pass
```

**Action**:
1. Read Epic Tracking or Epics Overview section
2. Check if ANY heuristic passes
3. If passes → valid
4. If none pass → log warning: `⚠ Epic Tracking section may be incomplete`

**If kanban_board.md does NOT exist**:
- Skip validation
- Log: `ℹ Epic Tracking validation skipped (kanban_board.md not found)`

### 3.5 Report content validation summary

Log summary:
```
✓ Content validation completed:
  tasks/README.md:
    - ✓ Linear Integration: valid (contains "Linear", "MCP", workflow states)
    - ✓ Task Workflow: valid (contains state transitions)
    - ✓ Task Templates: valid (contains template references)
  kanban_board.md:
    - ✓ Linear Configuration: {status} (Team: {name}, UUID: {uuid}, Key: {key})
    - ✓ Epic Tracking: valid (table present or placeholder)
```

**Output**: Validated and potentially updated task management documentation with Linear configuration

---

## Complete Output Structure

```
docs/
└── tasks/
    ├── README.md                     # Task management system rules
    └── kanban_board.md               # Linear integration (optional, created manually or by other skills)
```

**Note**: Kanban board updated by ln-301-task-creator, ln-302-task-replanner, ln-400-story-executor (Epic Grouping logic).

---

## Reference Files

### Templates

**Tasks README Template**:
- `references/tasks_readme_template.md` (v2.0.0) - Task management system rules with:
  - SCOPE tags (task management ONLY)
  - Story-Level Test Task Pattern (tests in final Story task, NOT scattered)
  - Kanban Board Structure (Epic Grouping Pattern with Status → Epic → Story → Tasks hierarchy)
  - Linear Integration (MCP methods: create_project, create_issue, update_issue, list_issues)
  - Maintenance section (Update Triggers, Verification, Last Updated)

**Kanban Board Template**:
- `references/kanban_board_template.md` (v3.0.0) - Linear integration template with:
  - Linear Configuration table (Team Name, UUID, Key, Workspace URL)
  - Epic Story Counters table (Next Epic Number, Story counters per Epic)
  - Kanban sections: Backlog, Todo (✅ APPROVED), In Progress, To Review, To Rework, Done (Last 5 tasks), Postponed
  - Epic Grouping Pattern format (Epic header → 📖 Story → Task with indentation)
  - Placeholders for Epic/Story/Task entries

### Validation Specification

**questions.md**:
- `references/questions.md` (v1.0) - Validation questions for task management documentation:
  - 5 sections (3 for tasks/README.md, 2 for kanban_board.md)
  - Question format: Question → Expected Content → Validation Heuristics → Auto-Discovery Hints → MCP Ref Hints
  - Special handling section for Linear Configuration (placeholder detection, UUID/Team Key validation)

---

## Best Practices

- **Story-Level Test Task Pattern**: Tests consolidated in final Story task, NOT scattered across implementation tasks
- **Epic Grouping Pattern**: Epic context always visible, 0/2/4 space indentation (Epic → Story → Tasks)
- **Linear MCP**: All task operations use Linear MCP methods (create_project, create_issue, update_issue)
- **SCOPE Tags**: Include in first 3-5 lines of all documentation files
- **Idempotent**: Can be invoked multiple times - checks file existence, preserves existing files, re-validates on each run

### Documentation Standards
- **NO_CODE Rule:** Task docs describe workflows, not implementations
- **Stack Adaptation:** References must match project stack
- **Format Priority:** Tables (states, transitions) > Lists > Text

---

## Prerequisites

**Orchestrator**: ln-110-documents-pipeline (invokes this worker in Phase 3, Step 3.3)

**Standalone usage**: Creating task docs, re-validating, setting up Linear Configuration

**Idempotent**: Yes - checks file existence, re-validates, auto-fixes, updates Linear Configuration if placeholders detected

---

## Critical Rules

- **Idempotent:** Checks file existence before creation; preserves existing files; safe to re-run
- **Linear UUID validation:** Team UUID must match `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/`; Team Key must match `/^[A-Z]{2,4}$/`
- **Placeholder detection:** If `[TEAM_NAME]`, `[TEAM_UUID]`, or `[TEAM_KEY]` found in kanban_board.md, enter interactive setup mode and prompt user
- **SCOPE tags required:** Both README.md and kanban_board.md must have `<!-- SCOPE: ... -->` in first 5 lines
- **Story-Level Test Task Pattern:** Tests consolidated in final Story task, not scattered across implementation tasks

## Definition of Done

Before completing work, verify ALL checkpoints:

### Phase 1: CREATE

**✅ tasks/README.md:**
- [ ] `docs/tasks/` directory created (if didn't exist)
- [ ] `docs/tasks/README.md` created from template (if didn't exist) OR preserved (if existed)
- [ ] All `{{DATE}}` placeholders replaced with current date
- [ ] Template contains SCOPE tags, Story-Level Test Task Pattern, Kanban Board Structure, Linear Integration, Maintenance section
- [ ] User notified: created OR preserved

### Phase 2: VALIDATE STRUCTURE

**✅ tasks/README.md:**
- [ ] SCOPE tag present in first 5 lines OR auto-fixed
- [ ] Required sections present (Linear Integration/Core Concepts, Task Workflow/Critical Rules, Task Templates) OR auto-fixed
- [ ] Maintenance section present at end OR auto-fixed
- [ ] POSIX line ending present OR auto-fixed
- [ ] Validation summary logged

**✅ kanban_board.md (if exists):**
- [ ] SCOPE tag present OR auto-fixed
- [ ] Required sections present (Linear Configuration, Work in Progress/Epic Tracking) OR auto-fixed
- [ ] Maintenance section present OR auto-fixed
- [ ] POSIX line ending present OR auto-fixed
- [ ] Validation summary logged

### Phase 3: VALIDATE CONTENT

**✅ tasks/README.md:**
- [ ] Linear Integration section validated (contains "Linear" OR "MCP" OR team ID OR workflow states OR length > 100 words)
- [ ] Task Workflow section validated (contains workflow states OR review criteria OR length > 60 words)
- [ ] Task Templates section validated (contains "template" OR Epic/Story/Task OR links OR length > 40 words)
- [ ] Validation summary logged

**✅ kanban_board.md (if exists):**
- [ ] Linear Configuration section validated:
  - [ ] If placeholders detected ([TEAM_NAME], [TEAM_UUID], [TEAM_KEY]):
    - [ ] User prompted for Team Name (non-empty validation)
    - [ ] User prompted for Team UUID (regex validation: `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/`)
    - [ ] User prompted for Team Key (regex validation: `/^[A-Z]{2,4}$/`)
    - [ ] Placeholders replaced with user input
    - [ ] Next Epic Number set to 1
    - [ ] Next Story Number set to 1
    - [ ] Last Updated date updated
  - [ ] If real values present:
    - [ ] Team UUID format validated
    - [ ] Team Key format validated
    - [ ] Validation result logged (valid OR invalid with warning)
- [ ] Epic Tracking section validated (has "Epic" header OR table OR placeholder OR length > 20 words)
- [ ] Validation summary logged

**✅ Overall:**
- [ ] Summary message displayed: "✓ Task management documentation validated (3-phase complete)"
- [ ] User informed about any auto-fixes applied
- [ ] User informed about Linear Configuration status (if applicable)

**Output:** docs/tasks/README.md + optionally kanban_board.md (validated, auto-fixed where needed, Linear Configuration set up if placeholders found)

---

**Version:** 7.1.0
**Last Updated:** 2025-01-12
