---
name: create-workflow
description: Create new workflows with consistent structure and matching skill integration. Meta-workflow for formalizing patterns into trackable processes.
---

# Create Workflow

Formalize patterns into trackable workflows using `@create-workflow`.

## Quick Start

```bash
kspec workflow start @create-workflow
kspec workflow next --input pattern_source="AGENTS.md:575-607"
```

## Workflow Overview

7 steps to create a well-structured workflow:

1. **Identify Pattern** - What process are you formalizing?
2. **Define Trigger** - When does this workflow start?
3. **Design Steps** - Break down into action/check/decision steps
4. **Create Workflow** - `kspec meta add workflow` + edit YAML for steps
5. **Skill Decision** - Does this need a matching skill?
6. **Test** - Run through the workflow
7. **Commit** - Save to main (skill) and shadow (workflow) branches

## Step Details

### Step 1: Identify the Pattern

Look for processes that are:
- Step-by-step instructions in docs
- Checklists that are easy to skip
- Repeated sequences of commands
- Quality gates with multiple criteria

Good sources: AGENTS.md, existing skills, task notes, session reflections.

### Step 2: Define Trigger & ID

| Trigger | When to Use |
|---------|-------------|
| `manual` | Invoked explicitly via skill or command |
| `session-start` | Beginning of work session |
| `session-end` | End of work session (reflection) |
| `task-complete` | After completing a task |
| `behavior-change` | Before implementing changes |
| `pre-release` | Before creating a release |
| `pr-merge` | Before merging a PR |

ID should be kebab-case: `pr-review-merge`, `task-work-session`

### Step 3: Design Steps

See [Step Design Guide](docs/step-design.md) for detailed guidance on:
- Choosing step types (action, check, decision)
- Writing effective step content
- When to use entry/exit criteria
- Designing step inputs

### Step 4: Create the Workflow

```bash
# Create workflow shell
kspec meta add workflow --id <id> --trigger <trigger> --description "..."

# Edit .kspec/kynetic.meta.yaml to add steps
# (until --steps flag is implemented)
```

### Step 5: Skill Decision

Consider a matching skill when:
- Steps need detailed context beyond what fits in content
- Multiple sub-documents would help (like `/triage` has modes)
- Users need a `/command` entrypoint

Skip a skill when:
- Workflow is self-contained
- Context already exists in AGENTS.md or another skill
- Workflow is internal/automated

### Step 6: Test

```bash
kspec workflow start @workflow-id
kspec workflow next --input key=value --notes "..."
# Repeat through all steps
kspec workflow show @run-id  # Verify inputs/notes captured
```

### Step 7: Commit

```bash
# Main branch (skill files)
git add .claude/skills/<name>/
git commit -m "feat: add <name> skill for workflow integration"

# Shadow branch (workflow definition) - auto-committed by kspec
```

## Workflow Commands

```bash
kspec workflow start @create-workflow    # Start
kspec workflow next --input key=value    # Advance with input
kspec workflow next --notes "..."        # Advance with notes
kspec workflow show                      # Check progress (needs run-ref for now)
kspec workflow pause                     # Pause for later
kspec workflow resume                    # Resume paused run
```
