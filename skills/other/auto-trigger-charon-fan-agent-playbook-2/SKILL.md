---
name: auto-trigger
description: Workflow automation hooks for agent-playbook skills. This skill defines automatic triggers between skills - DO NOT use directly, it's a configuration skill that other skills reference.
allowed-tools: Read, Write, Edit
---

# Auto-Trigger Hooks

This skill defines automatic trigger relationships between skills. When a skill completes its workflow, it should automatically trigger the next skill in the chain.

## Hook Definitions

### PRD Creation Chain

```yaml
prd_complete:
  triggers:
    - skill: self-improving-agent
      mode: background
      condition: PRD file exists and is complete
    - skill: session-logger
      mode: auto
      context: "PRD created for {feature_name}"

prd_implemented:
  triggers:
    - skill: session-logger
      mode: auto
      context: "Implemented PRD: {feature_name}"
```

### Implementation Chain

```yaml
implementation_complete:
  triggers:
    - skill: code-reviewer
      mode: ask_first
      message: "Implementation complete. Run code review?"
    - skill: create-pr
      mode: auto
      condition: changes_staged
```

### Session Management

```yaml
session_start:
  auto_triggers:
    - skill: session-logger
      action: create_session_file

session_end:
  auto_triggers:
    - skill: session-logger
      action: update_session_file
```

## Hook Format in Skills

To add auto-trigger capability to a skill, add to its front matter:

```yaml
---
name: my-skill
description: Skill description
allowed-tools: Read, Write, Edit
hooks:
  before_start:
    - trigger: session-logger
      mode: auto
      context: "Start {skill_name}"
  after_complete:
    - trigger: self-improving-agent
      mode: background
    - trigger: session-logger
      mode: auto
  on_error:
    - trigger: self-improving-agent
      mode: background
---
```

## Implementation Guide

When a skill completes its workflow:

1. **Check `hooks`** in its own front matter (`before_start`, `after_complete`, `on_error`, `on_progress`)
2. **For each hook:**
   - If `mode: auto`, trigger immediately
   - If `mode: background`, trigger without waiting
   - If `mode: ask_first`, ask user before triggering
   - If `condition:` exists, check it first
3. **Pass context** to the triggered skill

## Example Integration

### prd-planner should add:

```yaml
---
name: prd-planner
description: Creates PRDs using persistent file-based planning...
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, WebSearch
hooks:
  after_complete:
    - trigger: self-improving-agent
      mode: background
      context: "PRD created at {prd_file}"
    - trigger: session-logger
      mode: auto
      context: "PRD creation complete"
---
```

### self-improving-agent already has:

```yaml
---
name: self-improving-agent
description: Universal self-improvement that learns from all skill experiences...
allowed-tools: Read, Write,Edit, Bash, Grep, Glob, WebSearch
hooks:
  after_complete:
    - trigger: create-pr
      mode: ask_first
      condition: skills_modified
    - trigger: session-logger
      mode: auto
      context: "Self-improvement cycle complete"
  on_error:
    - trigger: self-improving-agent
      mode: background
---
```

### create-pr should add:

```yaml
---
name: create-pr
description: Creates pull requests with bilingual documentation updates...
allowed-tools: Read, Write, Edit, Bash, Grep, AskUserQuestion
hooks:
  after_complete:
    - trigger: session-logger
      mode: auto
      context: "PR created: {pr_title}"
---
```

## Chain Visualization

```
┌──────────────┐
│ prd-planner  │
└──────┬───────┘
       │ after_complete
       ├──→ self-improving-agent (background)
       │         └──→ create-pr (ask_first)
       │                  └──→ session-logger (auto)
       └──→ session-logger (auto)
```

## Error Correction Chain

```yaml
on_error:
  triggers:
    - skill: self-improving-agent
      mode: background
      context: "Error occurred in {skill_name}"
    - skill: session-logger
      mode: auto
      context: "Error captured for {skill_name}"
```

## Important Rules

1. **Don't create infinite loops** - Ensure chains terminate
2. **Ask before major actions** - Use `mode: ask_first` for PRs, deployments
3. **Background tasks** - Use `mode: background` for non-blocking tasks
4. **Pass context** - Always include relevant context to triggered skills
