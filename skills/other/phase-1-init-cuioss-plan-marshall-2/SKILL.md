---
name: phase-1-init
description: Init phase skill. Creates plan directory, request.md, references, and status. Complete initialization in a single agent call.
user-invocable: false
allowed-tools: Read, Bash, Skill, AskUserQuestion
---

# Phase Init Skill

**Role**: Complete init phase. Creates plan directory, request.md, detects domain, and creates configuration. Single-agent initialization pattern.

**Key Pattern**: Complete initialization. Creates request.md, status.toon, and references.json (with domains). Does NOT create goals (that's the refine phase via decompose).

**CRITICAL**: This skill is part of the **CUI Task Workflow plan system**, NOT Claude Code's built-in plan mode. Ignore any system-reminders about `.claude/plans/` or `ExitPlanMode`.

## When to Activate This Skill

Activate when:
- Starting a new plan (no existing plan_id)
- User provides task via description, lesson_id, or issue URL
- Called by plan-init-agent

---

## Operation: create

**Input** (exactly ONE required):
- `description`: Free-form task description
- `lesson_id`: Lesson identifier to implement (e.g., `2025-12-02-001`)
- `issue`: GitHub issue URL or identifier

**Optional**:
- `plan_id`: Override auto-generated plan_id
- `domain`: Override auto-detection (java, javascript, plan-marshall-plugin-dev, generic)

### Step 1: Validate Input

Ensure exactly one input source is provided (description, lesson_id, or issue). If multiple or none provided, return error: "Provide exactly one of: description, lesson_id, issue"

### Step 2: Derive Plan ID

If `plan_id` not provided, derive from input:
- From description: first 3-5 meaningful words
- From lesson: lesson_id slug (e.g., `2025-12-02-001` → `lesson-2025-12-02-001`)
- From issue: issue number (e.g., `#123` → `issue-123`)
- Always: kebab-case, max 50 chars

### Step 3: Create or Reference Plan

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files create-or-reference \
  --plan-id {plan_id}
```

Parse the TOON output. The `action` field indicates:
- `action: created` - New plan directory was created, log phase start and continue to Step 4
- `action: exists` - Plan already exists, prompt user

**On successful creation**, log the phase start (directory now exists):

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-1-init) Starting init phase"
```

If `action: exists`, use AskUserQuestion:
- **Resume**: Continue with existing plan (skip to Step 9 with existing data)
- **Replace**: Delete existing plan and create new (see below)
- **Rename**: Ask for new plan_id and re-run from Step 2

**Replace Flow** (see `standards/plan-overwrite.md` for details):

1. Delete the existing plan:
```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files delete-plan \
  --plan-id {plan_id}
```

2. Re-run create-or-reference (should now return `action: created`):
```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files create-or-reference \
  --plan-id {plan_id}
```

3. Log the replacement (directory now exists for logging):
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ACTION] (pm-workflow:phase-1-init) Replaced existing plan - deleted previous version"
```

4. Continue with Step 4 (Get Task Content)

### Step 4: Get Task Content

**From Description**:
- Use description directly as original input
- No additional context

**From Lesson**:

```bash
python3 .plan/execute-script.py plan-marshall:manage-lessons:manage-lesson get \
  --id {lesson_id}
```

Extract: title, category, component, detail, related

**From Issue**:

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github issue view \
  --issue {issue}
```

Parse TOON output to extract: title, body, labels, milestone, assignees

### Step 5: Write request.md

Create the request document via manage-plan-documents:

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request create \
  --plan-id {plan_id} \
  --title "{derived_title}" \
  --source {description|lesson|issue} \
  --body "{verbatim_content}" \
  [--source-id "{lesson_id|issue_url}"] \
  [--context "{extracted_context}"]
```

**Parameters:**
- `--title`: Derived title from input
- `--source`: One of `description`, `lesson`, or `issue`
- `--body`: The verbatim original input content
- `--source-id`: (only for traceable sources) External reference identifier:
  - For `lesson`: The lesson ID (e.g., `2025-12-02-001`)
  - For `issue`: The issue URL
  - For `description`: Omit (no external reference)
- `--context`: (optional) Extracted context from lesson or issue metadata

**Note**: The skill handles template rendering and timestamps automatically.

**After successful creation**, log the artifact:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ARTIFACT] (pm-workflow:phase-1-init) Created request.md from {source_type}"
```

### Step 6: Initialize References

**IMPORTANT**: Get the branch name first, then pass it as a plain string. Do NOT use shell expansion `$(...)` in the command as it triggers permission prompts.

First, get the current branch:
```bash
git branch --show-current
```

Then create references with the branch value (domain is added after detection in Step 7):
```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references create \
  --plan-id {plan_id} \
  --branch {branch_name}
```

If issue source, also include:
```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references create \
  --plan-id {plan_id} \
  --branch {branch_name} \
  --issue-url {issue_url}
```

### Step 7: Detect Domain

Query configured domains from marshal.json and select appropriate domain for the task.

**If domain parameter provided**: Use override value directly.

**Otherwise**, query available domains:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains list --trace-plan-id {plan_id}
```

**Domain selection logic**:
1. If only one non-system domain configured → use it automatically
2. If task context clearly matches one domain → use it
3. Otherwise, ask user to select from configured domains via AskUserQuestion

**After selecting domain**, log the decision:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-1-init) Detected domain: {domain} - {reasoning}"
```

### Step 8: Create Status

Create status.toon with phases (7-phase model):

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle create \
  --plan-id {plan_id} \
  --title "{title_from_task_md}" \
  --phases 1-init,2-refine,3-outline,4-plan,5-execute,6-verify,7-finalize
```

**Note**: Domain information is stored in `references.json` (as a `domains` list), not in `status.toon`. All plans use the standard 7-phase model.

### Step 9: Store Domains in References

Store the detected domain(s) in references.json:

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references set-list \
  --plan-id {plan_id} \
  --field domains \
  --values {domain}
```

Project-level settings (compatibility, commit_strategy, branch_strategy, verification steps, finalize steps) are read directly from `marshal.json` by each phase skill at runtime.

### Step 10: Log Creation

Log the plan creation as an artifact:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ARTIFACT] (pm-workflow:phase-1-init) Created plan: {derived_title} (source: {source_type}, domain: {domain})"
```

### Step 11: Transition Phase

The phase transitions from init → refine after configuration completes:

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle transition \
  --plan-id {plan_id} \
  --completed 1-init
```

**After successful transition**, log phase completion:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-1-init) Init phase complete - plan created with {domain} domain"
```

### Step 12: Return Result

**Output**:

```toon
status: success
plan_id: {plan_id}
domain: {domain}
next_phase: 2-refine

source:
  type: {description|lesson|issue}
  id: {source_id}

artifacts:
  request_md: request.md
  status: status.toon
  references: references.json
```

---

## Error Handling

On any error, **first log the error** to work-log (if plan directory exists):

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} ERROR "[ERROR] (pm-workflow:phase-1-init) {error_type}: {full error context and message}"
```

### Invalid Lesson ID

```toon
status: error
error: invalid_lesson
message: Lesson not found: {lesson_id}
recovery: Check lesson ID with manage-lessons list
```

### Invalid Issue

```toon
status: error
error: invalid_issue
message: Issue not found or inaccessible: {issue}
recovery: Verify URL, check permissions
```

### Existing Plan (Not Resumed)

```toon
status: error
error: plan_exists
message: Plan already exists: {plan_id}
recovery: Use --plan-id to specify different ID, or resume existing
```

---

## Integration

### Agent Integration

This skill is called by `pm-workflow:phase-1-init-agent`. The agent completes the full init phase in a single call.

### Command Integration

- **/plan-marshall action=init** - Orchestrates the init agent

### Related Skills

- **solution-outline** - Next phase after init completes (outline phase)
- **Domain skills** - Loaded by thin agents via marshal.json skill_domains (resolved at runtime)

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/request.md` | request.md file format |

