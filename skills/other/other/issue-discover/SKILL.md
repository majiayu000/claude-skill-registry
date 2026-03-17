---
name: issue-discover
description: Unified issue discovery and creation. Create issues from GitHub/text, discover issues via multi-perspective analysis, or prompt-driven iterative exploration. Triggers on "issue:new", "issue:discover", "issue:discover-by-prompt", "create issue", "discover issues", "find issues".
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, mcp__ace-tool__search_context, mcp__exa__search
---

# Issue Discover

Unified issue discovery and creation skill covering three entry points: manual issue creation, perspective-based discovery, and prompt-driven exploration.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Issue Discover Orchestrator (SKILL.md)                          │
│  → Action selection → Route to phase → Execute → Summary         │
└───────────────┬─────────────────────────────────────────────────┘
                │
                ├─ ASK_USER: Select action
                │
    ┌───────────┼───────────┬───────────┐
    ↓           ↓           ↓           │
┌─────────┐ ┌─────────┐ ┌─────────┐   │
│ Phase 1 │ │ Phase 2 │ │ Phase 3 │   │
│  Create │ │Discover │ │Discover │   │
│   New   │ │  Multi  │ │by Prompt│   │
└─────────┘ └─────────┘ └─────────┘   │
     ↓           ↓           ↓          │
  Issue      Discoveries  Discoveries   │
(registered)  (export)    (export)      │
     │           │           │          │
     │           ├───────────┤          │
     │           ↓                      │
     │     ┌───────────┐               │
     │     │  Phase 4  │               │
     │     │Quick Plan │               │
     │     │& Execute  │               │
     │     └─────┬─────┘               │
     │           ↓                      │
     │     .task/*.json                 │
     │           ↓                      │
     │     Direct Execution             │
     │           │                      │
     └───────────┴──────────────────────┘
                  ↓ (fallback/remaining)
          issue-resolve (plan/queue)
                  ↓
            /issue:execute
```

## Key Design Principles

1. **Action-Driven Routing**: ASK_USER selects action, then load single phase
2. **Progressive Phase Loading**: Only read the selected phase document
3. **CLI-First Data Access**: All issue CRUD via `ccw issue` CLI commands
4. **Auto Mode Support**: `-y` flag skips action selection with auto-detection
5. **Subagent Lifecycle**: Explicit lifecycle management with spawn_agent → wait → close_agent
6. **Role Path Loading**: Subagent roles loaded via path reference in MANDATORY FIRST STEPS

## Auto Mode

When `--yes` or `-y`: Skip action selection, auto-detect action from input type.

## Usage

```
issue-discover <input>
issue-discover [FLAGS] "<input>"

# Flags
-y, --yes              Skip all confirmations (auto mode)
--action <type>        Pre-select action: new|discover|discover-by-prompt

# Phase-specific flags
--priority <1-5>       Issue priority (new mode)
--perspectives <list>  Comma-separated perspectives (discover mode)
--external             Enable Exa research (discover mode)
--scope <pattern>      File scope (discover/discover-by-prompt mode)
--depth <level>        standard|deep (discover-by-prompt mode)
--max-iterations <n>   Max exploration iterations (discover-by-prompt mode)

# Examples
issue-discover https://github.com/org/repo/issues/42                              # Create from GitHub
issue-discover "Login fails with special chars"                                    # Create from text
issue-discover --action discover src/auth/**                                       # Multi-perspective discovery
issue-discover --action discover src/api/** --perspectives=security,bug            # Focused discovery
issue-discover --action discover-by-prompt "Check API contracts"                   # Prompt-driven discovery
issue-discover -y "auth broken"                                                    # Auto mode create
```

## Execution Flow

```
Input Parsing:
   └─ Parse flags (--action, -y, --perspectives, etc.) and positional args

Action Selection:
   ├─ --action flag provided → Route directly
   ├─ Auto-detect from input:
   │   ├─ GitHub URL or #number → Create New (Phase 1)
   │   ├─ Path pattern (src/**, *.ts) → Discover (Phase 2)
   │   ├─ Short text (< 80 chars) → Create New (Phase 1)
   │   └─ Long descriptive text (≥ 80 chars) → Discover by Prompt (Phase 3)
   └─ Otherwise → ASK_USER to select action

Phase Execution (load one phase):
   ├─ Phase 1: Create New          → phases/01-issue-new.md
   ├─ Phase 2: Discover            → phases/02-discover.md
   └─ Phase 3: Discover by Prompt  → phases/03-discover-by-prompt.md

Post-Phase:
   └─ Summary + Next steps recommendation
```

### Phase Reference Documents

| Phase | Document | Load When | Purpose |
|-------|----------|-----------|---------|
| Phase 1 | [phases/01-issue-new.md](phases/01-issue-new.md) | Action = Create New | Create issue from GitHub URL or text description |
| Phase 2 | [phases/02-discover.md](phases/02-discover.md) | Action = Discover | Multi-perspective issue discovery (bug, security, test, etc.) |
| Phase 3 | [phases/03-discover-by-prompt.md](phases/03-discover-by-prompt.md) | Action = Discover by Prompt | Prompt-driven iterative exploration with Gemini planning |
| Phase 4 | [phases/04-quick-execute.md](phases/04-quick-execute.md) | Post-Phase = Quick Plan & Execute | Convert high-confidence findings to tasks and execute directly |

## Core Rules

1. **Action Selection First**: Always determine action before loading any phase
2. **Single Phase Load**: Only read the selected phase document, never load all phases
3. **CLI Data Access**: Use `ccw issue` CLI for all issue operations, NEVER read files directly
4. **Content Preservation**: Each phase contains complete execution logic from original commands
5. **Auto-Detect Input**: Smart input parsing reduces need for explicit --action flag
6. **⚠️ CRITICAL: DO NOT STOP**: Continuous multi-phase workflow. After completing each phase, immediately proceed to next
7. **Progressive Phase Loading**: Read phase docs ONLY when that phase is about to execute
8. **Explicit Lifecycle**: Always close_agent after wait completes to free resources

## Input Processing

### Auto-Detection Logic

```javascript
function detectAction(input, flags) {
  // 1. Explicit --action flag
  if (flags.action) return flags.action;

  const trimmed = input.trim();

  // 2. GitHub URL → new
  if (trimmed.match(/github\.com\/[\w-]+\/[\w-]+\/issues\/\d+/) || trimmed.match(/^#\d+$/)) {
    return 'new';
  }

  // 3. Path pattern (contains **, /, or --perspectives) → discover
  if (trimmed.match(/\*\*/) || trimmed.match(/^src\//) || flags.perspectives) {
    return 'discover';
  }

  // 4. Short text (< 80 chars, no special patterns) → new
  if (trimmed.length > 0 && trimmed.length < 80 && !trimmed.includes('--')) {
    return 'new';
  }

  // 5. Long descriptive text → discover-by-prompt
  if (trimmed.length >= 80) {
    return 'discover-by-prompt';
  }

  // Cannot auto-detect → ask user
  return null;
}
```

### Action Selection (ASK_USER)

```javascript
// When action cannot be auto-detected
const answer = ASK_USER([{
  id: "action",
  type: "select",
  prompt: "What would you like to do?",
  options: [
    {
      label: "Create New Issue (Recommended)",
      description: "Create issue from GitHub URL, text description, or structured input"
    },
    {
      label: "Discover Issues",
      description: "Multi-perspective discovery: bug, security, test, quality, performance, etc."
    },
    {
      label: "Discover by Prompt",
      description: "Describe what to find — Gemini plans the exploration strategy iteratively"
    }
  ]
}]);  // BLOCKS (wait for user response)

// Route based on selection
const actionMap = {
  "Create New Issue": "new",
  "Discover Issues": "discover",
  "Discover by Prompt": "discover-by-prompt"
};
```

## Data Flow

```
User Input (URL / text / path pattern / descriptive prompt)
    ↓
[Parse Flags + Auto-Detect Action]
    ↓
[Action Selection] ← ASK_USER (if needed)
    ↓
[Read Selected Phase Document]
    ↓
[Execute Phase Logic]
    ↓
[Summary + Next Steps]
    ├─ After Create → Suggest issue-resolve (plan solution)
    └─ After Discover → Suggest export to issues, then issue-resolve
```

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

// Check completion status
if (result.status[agentId].completed) {
  const output = result.status[agentId].completed;
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
Continue with plan generation.
`
})
```

### close_agent

Clean up subagent resources (irreversible).

```javascript
close_agent({ id: agentId })
```

## Core Guidelines

**Data Access Principle**: Issues files can grow very large. To avoid context overflow:

| Operation | Correct | Incorrect |
|-----------|---------|-----------|
| List issues (brief) | `ccw issue list --status pending --brief` | `Read('issues.jsonl')` |
| Read issue details | `ccw issue status <id> --json` | `Read('issues.jsonl')` |
| Create issue | `echo '...' \| ccw issue create` | Direct file write |
| Update status | `ccw issue update <id> --status ...` | Direct file edit |

**ALWAYS** use CLI commands for CRUD operations. **NEVER** read entire `issues.jsonl` directly.

## Error Handling

| Error | Resolution |
|-------|------------|
| No action detected | Show ASK_USER with all 3 options |
| Invalid action type | Show available actions, re-prompt |
| Phase execution fails | Report error, suggest manual intervention |
| No files matched (discover) | Check target pattern, verify path exists |
| Gemini planning failed (discover-by-prompt) | Retry with qwen fallback |
| Agent lifecycle errors | Ensure close_agent in error paths to prevent resource leaks |

## Post-Phase Next Steps

After successful phase execution, recommend next action:

```javascript
// After Create New (issue created)
ASK_USER([{
  id: "next_after_create",
  type: "select",
  prompt: "Issue created. What next?",
  options: [
    { label: "Plan Solution", description: "Generate solution via issue-resolve" },
    { label: "Create Another", description: "Create more issues" },
    { label: "View Issues", description: "Review all issues" },
    { label: "Done", description: "Exit workflow" }
  ]
}]);  // BLOCKS (wait for user response)

// After Discover / Discover by Prompt (discoveries generated)
ASK_USER([{
  id: "next_after_discover",
  type: "select",
  prompt: `Discovery complete: ${findings.length} findings, ${executableFindings.length} executable. What next?`,
  options: [
    { label: "Quick Plan & Execute (Recommended)", description: `Fix ${executableFindings.length} high-confidence findings directly` },
    { label: "Export to Issues", description: "Convert discoveries to issues" },
    { label: "Plan Solutions", description: "Plan solutions for exported issues via issue-resolve" },
    { label: "Done", description: "Exit workflow" }
  ]
}]);  // BLOCKS (wait for user response)
// If "Quick Plan & Execute" → Read phases/04-quick-execute.md, execute
```

## Related Skills & Commands

- `issue-resolve` - Plan solutions, convert artifacts, form queues, from brainstorm
- `issue-manage` - Interactive issue CRUD operations
- `/issue:execute` - Execute queue with DAG-based parallel orchestration
- `ccw issue list` - List all issues
- `ccw issue status <id>` - View issue details
