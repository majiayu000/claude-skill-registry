---
name: agent-ops-guide
description: "Interactive workflow guide. Use when user is unsure what to do next, needs help navigating AgentOps, or wants to understand available tools."
category: utility
invokes: [agent-ops-interview, agent-ops-state]
invoked_by: []
state_files:
  read: [constitution.md, focus.md, issues/*.md, baseline.md, memory.md]
  write: [focus.md]
---

# AgentOps Workflow Guide

## Purpose

Help users navigate the AgentOps workflow by asking diagnostic questions and recommending the appropriate next step.

## When to Use

- User says "help", "what should I do", "where do I start"
- User seems lost or confused about workflow
- User wants to understand available tools
- First time using AgentOps in a project

## Diagnostic Procedure

### Step 1: Assess State Files

First, silently check which state files exist:

```
□ .agent/constitution.md  → Project setup complete?
□ .agent/baseline.md      → Baseline captured?
□ .agent/focus.md         → Has session context?
□ .agent/issues/          → Has defined issues?
□ .agent/memory.md        → Has learned conventions?
```

### Step 2: Ask Situational Question

Ask ONE question to understand user's intent:

> "What brings you here today?"
> 
> **A)** Starting a new project or first time here
> **B)** Returning to continue previous work
> **C)** Have a specific task or feature to implement
> **D)** Something's broken and need to fix it
> **E)** Want to explore or understand the codebase
> **F)** Need to review code quality
> **G)** Wrapping up work, ready to commit
> **H)** Want to create a new Python project
> **I)** Need to review/audit an API

### Step 3: Recommend Based on State + Intent

| Intent | Missing Constitution | Missing Baseline | Has Tasks | Recommendation |
|--------|---------------------|------------------|-----------|----------------|
| A (new) | ✗ | — | — | `/agent-init` then `/agent-constitution` |
| A (new) | ✓ | ✗ | — | `/agent-baseline` |
| B (resume) | — | — | — | Read focus.md, summarize status |
| C (task) | ✗ | — | — | `/agent-constitution` first |
| C (task) | ✓ | ✗ | — | `/agent-baseline` first |
| C (task) | ✓ | ✓ | ✗ | `/agent-task` to define task |
| C (task) | ✓ | ✓ | ✓ | `/agent-plan` for next task |
| D (broken) | — | — | — | `/agent-debug` then `/agent-recover` |
| E (explore) | — | — | — | `/agent-map` or `agent-ops-critical-review` |
| F (review) | — | — | — | `/agent-review` or `/agent-validation` |
| G (finish) | — | ✗ | — | `/agent-baseline` then `/agent-review` |
| G (finish) | — | ✓ | — | `/agent-validation` then `/agent-review` |
| H (python) | — | — | — | `/agent-create-python-project` |
| I (api) | — | — | — | `/agent-api-review` |

### Step 4: Provide Clear Next Step

Format your recommendation as:

```markdown
## Your Situation
[One sentence summary of what I detected]

## Recommended Next Step
**Run:** `/agent-[command]`
**Why:** [Brief reason]

## After That
[What comes next in the workflow]
```

## Decision Trees

### "I'm new here"

```
Has .agent/ folder?
├─ NO → /agent-init
└─ YES
   Has constitution.md with CONFIRMED commands?
   ├─ NO → /agent-constitution
   └─ YES
      Has baseline.md?
      ├─ NO → /agent-baseline
      └─ YES → Ready! Ask what they want to build
```

### "I have a task"

```
Task well-defined (clear acceptance criteria)?
├─ NO → /agent-task (refine it)
└─ YES
   Have baseline?
   ├─ NO → /agent-baseline
   └─ YES
      Have approved plan?
      ├─ NO → /agent-plan
      └─ YES → /agent-implement
```

### "Something's broken"

```
What's broken?
├─ Build fails → /agent-debug then /agent-recover
├─ Tests fail → /agent-debug (compare to baseline)
├─ Agent stuck → Read focus.md, identify blocking issue
├─ Git issues → agent-ops-git skill
└─ Unknown cause → /agent-debug (systematic isolation)
```

### "I want to create a Python project"

```
Have requirements/discussion?
├─ YES → /agent-create-python-project (with input)
└─ NO → /agent-create-python-project (will interview)
```

### "I need to review an API"

```
Has OpenAPI spec?
├─ YES → /agent-api-review
└─ NO 
   Has API endpoints?
   ├─ YES → /agent-api-review (will identify spec gaps)
   └─ NO → Not an API project, use /agent-review
```

### "I'm done"

```
Changes validated?
├─ NO → /agent-validation
└─ YES
   Critical review done?
   ├─ NO → /agent-review
   └─ YES
      Retrospective done?
      ├─ NO → /agent-retrospective
      └─ YES → Ready to commit (with confirmation)
```

## Quick Reference Card

Present this when user asks for overview:

```
┌───────────────────────────────────────────────────────────────┐
│                     AgentOps Workflow                         │
├───────────────────────────────────────────────────────────────┤
│  SETUP          │  WORK             │  FINISH                 │
│─────────────────│───────────────────│─────────────────────────│
│  /agent-init    │  /agent-task      │  /agent-validation      │
│  /agent-const   │  /agent-plan      │  /agent-review          │
│  /agent-base    │  /agent-impl      │  /agent-retrospective   │
├───────────────────────────────────────────────────────────────┤
│  UTILITIES                                                    │
│───────────────────────────────────────────────────────────────│
│  /agent-help        Interactive guide (you are here)          │
│  /agent-map         Understand codebase                       │
│  /agent-testing     Test strategy                             │
│  /agent-spec        Manage requirements                       │
│  /agent-report      View issues and status                    │
│  /agent-version     Versioning and changelog                  │
├───────────────────────────────────────────────────────────────┤
│  SPECIALIZED                                                  │
│───────────────────────────────────────────────────────────────│
│  /agent-debug                Systematic debugging             │
│  /agent-api-review           API contract & behavior audit    │
│  /agent-create-python-project   Scaffold Python project       │
└───────────────────────────────────────────────────────────────┘
```

## Anti-Patterns

- ❌ Overwhelming user with all options at once
- ❌ Recommending steps when prerequisites aren't met
- ❌ Skipping constitution/baseline for "quick" tasks
- ❌ Assuming user knows the workflow

## Output

After guiding user, update `.agent/focus.md`:
```markdown
## Doing now
- Guided user to [recommended step]
- Reason: [why this step]
```
