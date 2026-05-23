---
name: flow-coordinator
description: Template-driven workflow coordinator with minimal state tracking. Executes command chains from workflow templates with slash-command execution (mainprocess/async). Triggers on "flow-coordinator", "workflow template", "orchestrate".
allowed-tools: Task, AskUserQuestion, Read, Write, Bash, Glob, Grep
---

# Flow Coordinator

Lightweight workflow coordinator that executes command chains from predefined templates, supporting slash-command execution with mainprocess (blocking) and async (background) modes.

## Architecture

```
User Task → Select Template → status.json Init → Execute Steps → Complete
     ↑                                                │
     └──────────────── Resume (from status.json) ─────┘

Step Execution:
  execution mode?
    ├─ mainprocess  → SlashCommand (blocking, main process)
    └─ async        → ccw cli --tool claude --mode write (background)
```

## Core Concepts

**Template-Driven**: Workflows defined as JSON templates in `templates/`, decoupled from coordinator logic.

**Execution Type**: `slash-command` only
- ALL workflow commands (`/workflow:*`) use `slash-command` type
- Two execution modes:
  - `mainprocess`: SlashCommand (blocking, main process)
  - `async`: CLI background (ccw cli with claude tool)

**Dynamic Discovery**: Templates discovered at runtime via Glob, not hardcoded.

---

## Execution Flow

```javascript
async function execute(task) {
  // 1. Discover and select template
  const templates = await discoverTemplates();
  const template = await selectTemplate(templates);

  // 2. Init status
  const sessionId = `fc-${timestamp()}`;
  const statusPath = `.workflow/.flow-coordinator/${sessionId}/status.json`;
  const status = initStatus(template, task);
  write(statusPath, JSON.stringify(status, null, 2));

  // 3. Execute steps based on execution config
  await executeSteps(status, statusPath);
}

async function executeSteps(status, statusPath) {
  for (let i = status.current; i < status.steps.length; i++) {
    const step = status.steps[i];
    status.current = i;

    // Execute based on step mode (all steps use slash-command type)
    const execConfig = step.execution || { type: 'slash-command', mode: 'mainprocess' };

    if (execConfig.mode === 'async') {
      // Async execution - stop and wait for hook callback
      await executeSlashCommandAsync(step, status, statusPath);
      break;
    } else {
      // Mainprocess execution - continue immediately
      await executeSlashCommandSync(step, status);
      step.status = 'done';
      write(statusPath, JSON.stringify(status, null, 2));
    }
  }

  // All steps complete
  if (status.current >= status.steps.length) {
    status.complete = true;
    write(statusPath, JSON.stringify(status, null, 2));
  }
}
```

---

## Template Discovery

**Dynamic query** - never hardcode template list:

```javascript
async function discoverTemplates() {
  // Discover all JSON templates
  const files = Glob('*.json', { path: 'templates/' });

  // Parse each template
  const templates = [];
  for (const file of files) {
    const content = JSON.parse(Read(file));
    templates.push({
      name: content.name,
      description: content.description,
      steps: content.steps.map(s => s.cmd).join(' → '),
      file: file
    });
  }

  return templates;
}
```

---

## Template Selection

User chooses from discovered templates:

```javascript
async function selectTemplate(templates) {
  // Build options from discovered templates
  const options = templates.slice(0, 4).map(t => ({
    label: t.name,
    description: t.steps
  }));

  const response = await AskUserQuestion({
    questions: [{
      question: 'Select workflow template:',
      header: 'Template',
      options: options,
      multiSelect: false
    }]
  });

  // Handle "Other" - show remaining templates or custom input
  if (response.template === 'Other') {
    return await selectFromRemainingTemplates(templates.slice(4));
  }

  return templates.find(t => t.name === response.template);
}
```

---

## Status Schema

**Creation**: Copy template JSON → Update `id`, `template`, `goal`, set all steps `status: "pending"`

**Location**: `.workflow/.flow-coordinator/{session-id}/status.json`

**Core Fields**:
- `id`: Session ID (fc-YYYYMMDD-HHMMSS)
- `template`: Template name
- `goal`: User task description
- `current`: Current step index
- `steps[]`: Step array from template (with runtime `status`, `session`, `taskId`)
- `complete`: All steps done?

**Step Status**: `pending` → `running` → `done` | `failed` | `skipped`

---

## Extended Template Schema

**Templates stored in**: `templates/*.json` (discovered at runtime via Glob)

**TemplateStep Fields**:
- `cmd`: Full command path (e.g., `/workflow:lite-plan`, `/workflow:execute`)
- `args?`: Arguments with `{{goal}}` and `{{prev}}` placeholders
- `unit?`: Minimum execution unit name (groups related commands)
- `optional?`: Can be skipped by user
- `execution`: Type and mode configuration
  - `type`: Always `'slash-command'` (for all workflow commands)
  - `mode`: `'mainprocess'` (blocking) or `'async'` (background)
- `contextHint?`: Natural language guidance for context assembly

**Template Example**:
```json
{
  "name": "rapid",
  "steps": [
    {
      "cmd": "/workflow:lite-plan",
      "args": "\"{{goal}}\"",
      "unit": "quick-implementation",
      "execution": { "type": "slash-command", "mode": "mainprocess" },
      "contextHint": "Create lightweight implementation plan"
    },
    {
      "cmd": "/workflow:lite-execute",
      "args": "--in-memory",
      "unit": "quick-implementation",
      "execution": { "type": "slash-command", "mode": "async" },
      "contextHint": "Execute plan from previous step"
    }
  ]
}
```

---

## Execution Implementation

### Mainprocess Mode (Blocking)

```javascript
async function executeSlashCommandSync(step, status) {
  // Build command: /workflow:cmd -y args
  const cmd = buildCommand(step, status);
  const result = await SlashCommand({ command: cmd });

  step.session = result.session_id;
  step.status = 'done';
  return result;
}
```

### Async Mode (Background)

```javascript
async function executeSlashCommandAsync(step, status, statusPath) {
  // Build prompt: /workflow:cmd -y args + context
  const prompt = buildCommandPrompt(step, status);

  step.status = 'running';
  write(statusPath, JSON.stringify(status, null, 2));

  // Execute via ccw cli in background
  const taskId = Bash(
    `ccw cli -p "${escapePrompt(prompt)}" --tool claude --mode write`,
    { run_in_background: true }
  ).task_id;

  step.taskId = taskId;
  write(statusPath, JSON.stringify(status, null, 2));

  console.log(`Executing: ${step.cmd} (async)`);
  console.log(`Resume: /flow-coordinator --resume ${status.id}`);
}
```

---

## Prompt Building

Prompts are built in format: `/workflow:cmd -y args` + context

```javascript
function buildCommandPrompt(step, status) {
  // step.cmd already contains full path: /workflow:lite-plan, /workflow:execute, etc.
  let prompt = `${step.cmd} -y`;

  // Add arguments (with placeholder replacement)
  if (step.args) {
    const args = step.args
      .replace('{{goal}}', status.goal)
      .replace('{{prev}}', getPreviousSessionId(status));
    prompt += ` ${args}`;
  }

  // Add context based on contextHint
  if (step.contextHint) {
    const context = buildContextFromHint(step.contextHint, status);
    prompt += `\n\nContext:\n${context}`;
  } else {
    // Default context: previous session IDs
    const previousContext = collectPreviousResults(status);
    if (previousContext) {
      prompt += `\n\nPrevious results:\n${previousContext}`;
    }
  }

  return prompt;
}

function buildContextFromHint(hint, status) {
  // Parse contextHint instruction and build context accordingly
  // Examples:
  // "Summarize IMPL_PLAN.md" → read and summarize plan
  // "List test coverage gaps" → analyze previous test results
  // "Pass session ID" → just return session reference

  return parseAndBuildContext(hint, status);
}
```

### Example Prompt Output

```
/workflow:lite-plan -y "Implement user registration"

Context:
Task: Implement user registration
Previous results:
- None (first step)
```

```
/workflow:execute -y --in-memory

Context:
Task: Implement user registration
Previous results:
- lite-plan: WFS-plan-20250130 (planning-context.md)
```

---

## User Interaction

### Step 1: Select Template

```
Select workflow template:

○ rapid      lite-plan → lite-execute → test-cycle-execute
○ coupled    plan → plan-verify → execute → review → test
○ bugfix     lite-fix → lite-execute → test-cycle-execute
○ tdd        tdd-plan → execute → tdd-verify
○ Other      (more templates or custom)
```

### Step 2: Review Execution Plan

```
Template: coupled
Steps:
  1. /workflow:plan (slash-command mainprocess)
  2. /workflow:plan-verify (slash-command mainprocess)
  3. /workflow:execute (slash-command async)
  4. /workflow:review-session-cycle (slash-command mainprocess)
  5. /workflow:review-cycle-fix (slash-command mainprocess)
  6. /workflow:test-fix-gen (slash-command mainprocess)
  7. /workflow:test-cycle-execute (slash-command async)

Proceed? [Confirm / Cancel]
```

---

## Resume Capability

```javascript
async function resume(sessionId) {
  const statusPath = `.workflow/.flow-coordinator/${sessionId}/status.json`;
  const status = JSON.parse(Read(statusPath));

  // Find first incomplete step
  status.current = status.steps.findIndex(s => s.status !== 'done');
  if (status.current === -1) {
    console.log('All steps complete');
    return;
  }

  // Continue executing steps
  await executeSteps(status, statusPath);
}
```

---

## Available Templates

Templates discovered from `templates/*.json`:

| Template | Use Case | Steps |
|----------|----------|-------|
| rapid | Simple feature | /workflow:lite-plan → /workflow:lite-execute → /workflow:test-cycle-execute |
| coupled | Complex feature | /workflow:plan → /workflow:plan-verify → /workflow:execute → /workflow:review-session-cycle → /workflow:test-fix-gen |
| bugfix | Bug fix | /workflow:lite-fix → /workflow:lite-execute → /workflow:test-cycle-execute |
| tdd | Test-driven | /workflow:tdd-plan → /workflow:execute → /workflow:tdd-verify |
| test-fix | Fix failing tests | /workflow:test-fix-gen → /workflow:test-cycle-execute |
| brainstorm | Exploration | /workflow:brainstorm-with-file |
| debug | Debug with docs | /workflow:debug-with-file |
| analyze | Collaborative analysis | /workflow:analyze-with-file |
| issue | Issue workflow | /workflow:issue:plan → /workflow:issue:queue → /workflow:issue:execute |

---

## Design Principles

1. **Minimal fields**: Only essential tracking data
2. **Flat structure**: No nested objects beyond steps array
3. **Step-level execution**: Each step defines how it's executed
4. **Resumable**: Any step can be resumed from status
5. **Human readable**: Clear JSON format

---

## Reference Documents

| Document | Purpose |
|----------|---------|
| templates/*.json | Workflow templates (dynamic discovery) |
