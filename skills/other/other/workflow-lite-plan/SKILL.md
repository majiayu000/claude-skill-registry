---
name: workflow-lite-plan
description: Lightweight planning and execution skill - route to lite-plan or lite-execute with prompt enhancement. Triggers on "workflow:lite-plan", "workflow:lite-execute".
allowed-tools: Skill, Task, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow Lite-Plan

Unified lightweight planning and execution skill. Routes to lite-plan (planning pipeline) or lite-execute (execution engine) based on trigger, with prompt enhancement for both modes.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│  SKILL.md (Router + Prompt Enhancement)              │
│  → Detect mode → Enhance prompt → Dispatch to phase │
└──────────────────────┬──────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           ↓                       ↓
     ┌───────────┐           ┌───────────┐
     │ lite-plan │           │lite-execute│
     │ Phase 1   │           │ Phase 2    │
     │ Plan+Exec │─direct──→│ Standalone │
     └───────────┘           └───────────┘
```

## Mode Detection & Routing

```javascript
const args = $ARGUMENTS
const mode = detectMode()

function detectMode() {
  if (skillName === 'workflow:lite-execute') return 'execute'
  return 'plan'  // default: workflow:lite-plan
}
```

**Routing Table**:

| Trigger | Mode | Phase Document | Description |
|---------|------|----------------|-------------|
| `workflow:lite-plan` | plan | [phases/01-lite-plan.md](phases/01-lite-plan.md) | Full planning pipeline (explore → plan → confirm → execute) |
| `workflow:lite-execute` | execute | [phases/02-lite-execute.md](phases/02-lite-execute.md) | Standalone execution (in-memory / prompt / file) |

## Interactive Preference Collection

Before dispatching, collect workflow preferences via AskUserQuestion:

```javascript
// ★ 统一 auto mode 检测：-y/--yes 从 $ARGUMENTS 或 ccw 传播
const autoYes = /\b(-y|--yes)\b/.test($ARGUMENTS)

if (autoYes) {
  // 自动模式：跳过所有询问，使用默认值
  workflowPreferences = { autoYes: true, forceExplore: false }
} else if (mode === 'plan') {
  const prefResponse = AskUserQuestion({
    questions: [
      {
        question: "是否跳过所有确认步骤（自动模式）？",
        header: "Auto Mode",
        multiSelect: false,
        options: [
          { label: "Interactive (Recommended)", description: "交互模式，包含确认步骤" },
          { label: "Auto", description: "跳过所有确认，自动执行" }
        ]
      },
      {
        question: "是否强制执行代码探索阶段？",
        header: "Exploration",
        multiSelect: false,
        options: [
          { label: "Auto-detect (Recommended)", description: "智能判断是否需要探索" },
          { label: "Force explore", description: "强制执行代码探索" }
        ]
      }
    ]
  })
  workflowPreferences = {
    autoYes: prefResponse.autoMode === 'Auto',
    forceExplore: prefResponse.exploration === 'Force explore'
  }
} else if (mode !== 'plan') {
  // Execute mode (standalone, not in-memory)
  const prefResponse = AskUserQuestion({
    questions: [
      {
        question: "是否跳过所有确认步骤（自动模式）？",
        header: "Auto Mode",
        multiSelect: false,
        options: [
          { label: "Interactive (Recommended)", description: "交互模式，包含确认步骤" },
          { label: "Auto", description: "跳过所有确认，自动执行" }
        ]
      }
    ]
  })
  workflowPreferences = {
    autoYes: prefResponse.autoMode === 'Auto',
    forceExplore: false
  }
}
```

**workflowPreferences** is passed to phase execution as context variable, referenced as `workflowPreferences.autoYes` and `workflowPreferences.forceExplore` within phases.

## Prompt Enhancement

After collecting preferences, enhance context and dispatch:

```javascript
// Step 1: Check for project context files
const hasProjectTech = fileExists('.workflow/project-tech.json')
const hasProjectGuidelines = fileExists('.workflow/project-guidelines.json')

// Step 2: Log available context
if (hasProjectTech) {
  console.log('Project tech context available: .workflow/project-tech.json')
}
if (hasProjectGuidelines) {
  console.log('Project guidelines available: .workflow/project-guidelines.json')
}

// Step 3: Dispatch to phase (workflowPreferences available as context)
if (mode === 'plan') {
  // Read phases/01-lite-plan.md and execute
} else {
  // Read phases/02-lite-execute.md and execute
}
```

## Execution Flow

### Plan Mode

```
1. Collect preferences via AskUserQuestion (autoYes, forceExplore)
2. Enhance prompt with project context availability
3. Read phases/01-lite-plan.md
4. Execute lite-plan pipeline (Phase 1-5 within the phase doc)
5. lite-plan Phase 5 directly reads and executes Phase 2 (lite-execute) with executionContext
```

### Execute Mode

```
1. Collect preferences via AskUserQuestion (autoYes)
2. Enhance prompt with project context availability
3. Read phases/02-lite-execute.md
4. Execute lite-execute pipeline (input detection → execution → review)
```

## Usage

Plan mode and execute mode are triggered by skill name routing (see Mode Detection). Workflow preferences (auto mode, force explore) are collected interactively via AskUserQuestion before dispatching to phases.

**Plan mode**: Task description provided as arguments → interactive preference collection → planning pipeline
**Execute mode**: Task description, file path, or in-memory context → interactive preference collection → execution pipeline

## Phase Reference Documents

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-lite-plan.md](phases/01-lite-plan.md) | Complete planning pipeline: exploration, clarification, planning, confirmation, handoff |
| 2 | [phases/02-lite-execute.md](phases/02-lite-execute.md) | Complete execution engine: input modes, task grouping, batch execution, code review |
