---
name: issue-resolve
description: Unified issue resolution pipeline with source selection. Plan issues via AI exploration, convert from artifacts, import from brainstorm sessions, form execution queues, or export solutions to task JSON. Triggers on "issue:plan", "issue:queue", "issue:convert-to-plan", "issue:from-brainstorm", "export-to-tasks", "resolve issue", "plan issue", "queue issues", "convert plan to issue".
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Issue Resolve (Codex Version)

Unified issue resolution pipeline that orchestrates solution creation from multiple sources and queue formation for execution.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Issue Resolve Orchestrator (SKILL.md)                           │
│  → Source selection → Route to phase → Execute → Summary         │
└───────────────┬─────────────────────────────────────────────────┘
                │
                ├─ ASK_USER: Select issue source
                │
    ┌───────────┼───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓           │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│ Phase 1 │ │ Phase 2 │ │ Phase 3 │ │ Phase 4 │   │
│ Explore │ │ Convert │ │  From   │ │  Form   │   │
│ & Plan  │ │Artifact │ │Brainstorm│ │  Queue  │   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘   │
     ↓           ↓           ↓           ↓          │
  Solutions   Solutions   Issue+Sol   Exec Queue    │
  (bound)     (bound)     (bound)    (ordered)      │
     │           │           │                       │
     └─────┬─────┘───────────┘                       │
           ↓ (optional --export-tasks)               │
    .task/TASK-*.json                                 │
                                                     │
                    ┌────────────────────────────────┘
                    ↓
              /issue:execute
```

## Key Design Principles

1. **Source-Driven Routing**: ASK_USER selects workflow, then load single phase
2. **Progressive Phase Loading**: Only read the selected phase document
3. **CLI-First Data Access**: All issue/solution CRUD via `ccw issue` CLI commands
4. **Auto Mode Support**: `-y` flag skips source selection (defaults to Explore & Plan)

## Subagent API Reference

### spawn_agent
Create a new subagent with task assignment.

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/{agent-type}.md (MUST read first)
2. Read: {projectRoot}/.workflow/project-tech.json
3. Read: {projectRoot}/.workflow/project-guidelines.json

## TASK CONTEXT
${taskContext}

## DELIVERABLES
${deliverables}
`
})
```

### wait
Get results from subagent (only way to retrieve results).

```javascript
const result = wait({
  ids: [agentId],
  timeout_ms: 600000  // 10 minutes
})

if (result.timed_out) {
  // Handle timeout - can continue waiting or send_input to prompt completion
}
```

### send_input
Continue interaction with active subagent (for clarification or follow-up).

```javascript
send_input({
  id: agentId,
  message: `
## CLARIFICATION ANSWERS
${answers}

## NEXT STEP
Continue with updated analysis.
`
})
```

### close_agent
Clean up subagent resources (irreversible).

```javascript
close_agent({ id: agentId })
```

## Auto Mode

When `--yes` or `-y`: Skip source selection, use Explore & Plan for issue IDs, or auto-detect source type for paths.

## Usage

```
codex -p "@.codex/prompts/issue-resolve.md <task description or issue IDs>"
codex -p "@.codex/prompts/issue-resolve.md [FLAGS] \"<input>\""

# Flags
-y, --yes              Skip all confirmations (auto mode)
--source <type>        Pre-select source: plan|convert|brainstorm|queue
--batch-size <n>       Max issues per agent batch (plan mode, default: 3)
--issue <id>           Bind to existing issue (convert mode)
--supplement           Add tasks to existing solution (convert mode)
--queues <n>           Number of parallel queues (queue mode, default: 1)
--export-tasks         Export solution tasks to .task/TASK-*.json (task-schema.json format)

# Examples
codex -p "@.codex/prompts/issue-resolve.md GH-123,GH-124"                              # Explore & plan issues
codex -p "@.codex/prompts/issue-resolve.md --source plan --all-pending"                 # Plan all pending issues
codex -p "@.codex/prompts/issue-resolve.md --source convert \".workflow/.lite-plan/my-plan\""  # Convert artifact
codex -p "@.codex/prompts/issue-resolve.md --source brainstorm SESSION=\"BS-rate-limiting\""   # From brainstorm
codex -p "@.codex/prompts/issue-resolve.md --source queue"                              # Form execution queue
codex -p "@.codex/prompts/issue-resolve.md -y GH-123"                                  # Auto mode, plan single issue
```

## Execution Flow

```
Input Parsing:
   └─ Parse flags (--source, -y, --issue, etc.) and positional args

Source Selection:
   ├─ --source flag provided → Route directly
   ├─ Auto-detect from input:
   │   ├─ Issue IDs (GH-xxx, ISS-xxx) → Explore & Plan
   │   ├─ SESSION="..." → From Brainstorm
   │   ├─ File/folder path → Convert from Artifact
   │   └─ No input or --all-pending → Explore & Plan (all pending)
   └─ Otherwise → ASK_USER to select source

Phase Execution (load one phase):
   ├─ Phase 1: Explore & Plan    → phases/01-issue-plan.md
   ├─ Phase 2: Convert Artifact  → phases/02-convert-to-plan.md
   ├─ Phase 3: From Brainstorm   → phases/03-from-brainstorm.md
   └─ Phase 4: Form Queue        → phases/04-issue-queue.md

Post-Phase:
   ├─ Export to Task JSON (optional, with --export-tasks flag)
   │   ├─ For each solution.tasks[] → write .task/TASK-{T-id}.json
   │   └─ Generate plan.json (plan-overview-base-schema) from exported tasks
   └─ Summary + Next steps recommendation
```

### Phase Reference Documents

| Phase | Document | Load When | Purpose |
|-------|----------|-----------|---------|
| Phase 1 | [phases/01-issue-plan.md](phases/01-issue-plan.md) | Source = Explore & Plan | Batch plan issues via issue-plan-agent |
| Phase 2 | [phases/02-convert-to-plan.md](phases/02-convert-to-plan.md) | Source = Convert Artifact | Convert lite-plan/session/markdown to solutions |
| Phase 3 | [phases/03-from-brainstorm.md](phases/03-from-brainstorm.md) | Source = From Brainstorm | Convert brainstorm ideas to issue + solution |
| Phase 4 | [phases/04-issue-queue.md](phases/04-issue-queue.md) | Source = Form Queue | Order bound solutions into execution queue |

## Core Rules

1. **Source Selection First**: Always determine source before loading any phase
2. **Single Phase Load**: Only read the selected phase document, never load all phases
3. **CLI Data Access**: Use `ccw issue` CLI for all issue/solution operations, NEVER read files directly
4. **Content Preservation**: Each phase contains complete execution logic from original commands
5. **Auto-Detect Input**: Smart input parsing reduces need for explicit --source flag
6. **DO NOT STOP**: Continuous multi-phase workflow. After completing each phase, immediately proceed to next
7. **Explicit Lifecycle**: Always close_agent after wait completes to free resources

## Input Processing

### Auto-Detection Logic

```javascript
function detectSource(input, flags) {
  // 1. Explicit --source flag
  if (flags.source) return flags.source;

  // 2. Auto-detect from input content
  const trimmed = input.trim();

  // Issue IDs pattern (GH-xxx, ISS-xxx, comma-separated)
  if (trimmed.match(/^[A-Z]+-\d+/i) || trimmed.includes(',')) {
    return 'plan';
  }

  // --all-pending or empty input → plan all pending
  if (flags.allPending || trimmed === '') {
    return 'plan';
  }

  // SESSION="..." pattern → brainstorm
  if (trimmed.includes('SESSION=')) {
    return 'brainstorm';
  }

  // File/folder path → convert
  if (trimmed.match(/\.(md|json)$/) || trimmed.includes('.workflow/')) {
    return 'convert';
  }

  // Cannot auto-detect → ask user
  return null;
}
```

### Source Selection (ASK_USER)

```javascript
// When source cannot be auto-detected
const answer = ASK_USER([{
  id: "source",
  type: "select",
  prompt: "How would you like to create/manage issue solutions?",
  options: [
    {
      label: "Explore & Plan (Recommended)",
      description: "AI explores codebase and generates solutions for issues"
    },
    {
      label: "Convert from Artifact",
      description: "Convert existing lite-plan, workflow session, or markdown to solution"
    },
    {
      label: "From Brainstorm",
      description: "Convert brainstorm session ideas into issue with solution"
    },
    {
      label: "Form Execution Queue",
      description: "Order bound solutions into execution queue for /issue:execute"
    }
  ]
}]);  // BLOCKS (wait for user response)

// Route based on selection
const sourceMap = {
  "Explore & Plan": "plan",
  "Convert from Artifact": "convert",
  "From Brainstorm": "brainstorm",
  "Form Execution Queue": "queue"
};
```

## Data Flow

```
User Input (issue IDs / artifact path / session ID / flags)
    ↓
[Parse Flags + Auto-Detect Source]
    ↓
[Source Selection] ← ASK_USER (if needed)
    ↓
[Read Selected Phase Document]
    ↓
[Execute Phase Logic]
    ↓
[Summary + Next Steps]
    ├─ After Plan/Convert/Brainstorm → Suggest /issue:queue or /issue:execute
    └─ After Queue → Suggest /issue:execute

(Optional) Export to Task JSON (when --export-tasks flag is set):
    ├─ For each solution.tasks[] entry:
    │   ├─ solution.task.id             → id (prefixed as TASK-{T-id})
    │   ├─ solution.task.title          → title
    │   ├─ solution.task.description    → description
    │   ├─ solution.task.action         → action
    │   ├─ solution.task.scope          → scope
    │   ├─ solution.task.modification_points[] → files[]
    │   │   ├─ mp.file                  → files[].path
    │   │   ├─ mp.target                → files[].target
    │   │   └─ mp.change                → files[].changes[]
    │   ├─ solution.task.acceptance     → convergence
    │   │   ├─ acceptance.criteria[]    → convergence.criteria[]
    │   │   └─ acceptance.verification[]→ convergence.verification (joined)
    │   ├─ solution.task.implementation → implementation[]
    │   ├─ solution.task.test           → test
    │   ├─ solution.task.depends_on     → depends_on
    │   ├─ solution.task.commit         → commit
    │   └─ solution.task.priority       → priority (1→critical, 2→high, 3→medium, 4-5→low)
    ├─ Output path: .workflow/issues/{issue-id}/.task/TASK-{T-id}.json
    ├─ Each file follows task-schema.json (IDENTITY + CONVERGENCE + FILES required)
    ├─ source.tool = "issue-resolve", source.issue_id = {issue-id}
    │
    └─ Generate plan.json (after all TASK-*.json exported):
        const issueDir = `.workflow/issues/${issueId}`
        const taskFiles = Glob(`${issueDir}/.task/TASK-*.json`)
        const taskIds = taskFiles.map(f => JSON.parse(Read(f)).id).sort()

        // Guard: skip plan.json if no tasks generated
        if (taskIds.length === 0) {
          console.warn('No tasks generated; skipping plan.json')
        } else {

        const planOverview = {
          summary: `Issue resolution plan for ${issueId}: ${issueTitle}`,
          approach: solution.approach || "AI-explored resolution strategy",
          task_ids: taskIds,
          task_count: taskIds.length,
          complexity: taskIds.length > 5 ? "High" : taskIds.length > 2 ? "Medium" : "Low",
          _metadata: {
            timestamp: getUtc8ISOString(),
            source: "issue-plan-agent",
            planning_mode: "agent-based",
            plan_type: "feature",
            schema_version: "2.0"
          }
        }
        Write(`${issueDir}/plan.json`, JSON.stringify(planOverview, null, 2))

        } // end guard
        Output path: .workflow/issues/{issue-id}/plan.json
```

## Task Tracking Pattern

```javascript
// Initialize plan with phase steps
update_plan({
  explanation: "Issue resolve workflow started",
  plan: [
    { step: "Select issue source", status: "completed" },
    { step: "Execute: [selected phase name]", status: "in_progress" },
    { step: "Summary & next steps", status: "pending" }
  ]
})
```

Phase-specific sub-tasks are attached when the phase executes (see individual phase docs for details).

## Core Guidelines

**Data Access Principle**: Issues and solutions files can grow very large. To avoid context overflow:

| Operation | Correct | Incorrect |
|-----------|---------|-----------|
| List issues (brief) | `ccw issue list --status pending --brief` | `Read('issues.jsonl')` |
| Read issue details | `ccw issue status <id> --json` | `Read('issues.jsonl')` |
| Update status | `ccw issue update <id> --status ...` | Direct file edit |
| Bind solution | `ccw issue bind <id> <sol-id>` | Direct file edit |
| Batch solutions | `ccw issue solutions --status planned --brief` | Loop individual queries |

**Output Options**:
- `--brief`: JSON with minimal fields (orchestrator use)
- `--json`: Full JSON (agent use only)

**ALWAYS** use CLI commands for CRUD operations. **NEVER** read entire `issues.jsonl` or `solutions/*.jsonl` directly.

## Error Handling

| Error | Resolution |
|-------|------------|
| No source detected | Show ASK_USER with all 4 options |
| Invalid source type | Show available sources, re-prompt |
| Phase execution fails | Report error, suggest manual intervention |
| No pending issues (plan) | Suggest creating issues first |
| No bound solutions (queue) | Suggest running plan/convert/brainstorm first |

## Post-Phase Next Steps

After successful phase execution, recommend next action:

```javascript
// After Plan/Convert/Brainstorm (solutions created)
ASK_USER([{
  id: "next_action",
  type: "select",
  prompt: "Solutions created. What next?",
  options: [
    { label: "Form Queue", description: "Order solutions for execution (/issue:queue)" },
    { label: "Plan More Issues", description: "Continue creating solutions" },
    { label: "View Issues", description: "Review issue details" },
    { label: "Done", description: "Exit workflow" }
  ]
}]);  // BLOCKS (wait for user response)

// After Queue (queue formed)
// → Suggest /issue:execute directly
```

## Related Commands

- `issue-manage` - Interactive issue CRUD operations
- `/issue:execute` - Execute queue with DAG-based parallel orchestration
- `ccw issue list` - List all issues
- `ccw issue status <id>` - View issue details
