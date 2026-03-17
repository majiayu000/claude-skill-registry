---
name: workflow-composer
description: >
  Chain Vibery commands, skills, and agents into repeatable automated workflows.
  Outputs: Executable workflow files, hook configurations, CI/CD integration.
  Use when user has repetitive multi-step processes to automate.
  Triggers: create workflow, automate this process, chain these commands, /workflow
---

# Workflow Composer

Transform repetitive multi-step processes into one-command automations.

## Purpose

Users manually run the same sequence of commands repeatedly. This skill captures those patterns and outputs executable workflows using Vibery hooks, custom commands, or CI/CD configurations.

## Available Workflow Types

```
1. Hooks (event-triggered):
   - PostToolUse: After Claude edits files
   - PreToolUse: Before Claude runs commands
   - Stop: When conversation ends

2. Custom Commands (.claude/commands/*.md):
   - User-triggered via /command-name
   - Can include $ARGUMENTS

3. GitHub Actions (.github/workflows/*.yml):
   - Triggered by git events
   - Full CI/CD capabilities

4. Shell Scripts:
   - Direct automation
   - Can combine multiple tools
```

---

## Process

### Phase 1: Workflow Discovery

#### Entry Check

```
IF user described: repetitive process + trigger condition
    → Proceed to Phase 2
ELSE
    → Discover workflow first
```

#### Discovery Questions

| Question                                 | Purpose                      |
| ---------------------------------------- | ---------------------------- |
| "Walk me through what you do repeatedly" | Capture full sequence        |
| "What triggers this process?"            | Determines workflow type     |
| "Any variations or conditions?"          | Identifies branching logic   |
| "How often do you do this?"              | Prioritizes automation value |

#### Workflow Trigger → Type Mapping

```
IF trigger = "after I edit code"
    → Hook (PostToolUse)

IF trigger = "before running a command"
    → Hook (PreToolUse)

IF trigger = "when I finish a session"
    → Hook (Stop)

IF trigger = "when I type a command"
    → Custom Command

IF trigger = "on git push/PR"
    → GitHub Action

IF trigger = "manually, but want one command"
    → Shell Script or Custom Command
```

---

### Phase 2: Workflow Analysis

#### Entry Check

```
IF workflow discovered:
    → Analyze and structure
ELSE
    → Return to Phase 1
```

#### Step Extraction

```
FOR each step in user's process:
    Identify:
    - Action: What happens
    - Tool: Which Vibery component
    - Input: What it needs
    - Output: What it produces
    - Condition: When to skip/branch
```

#### Workflow Structure

```markdown
## Workflow: [Name]

### Trigger

[When this runs]

### Steps

| #   | Action   | Tool               | Condition |
| --- | -------- | ------------------ | --------- |
| 1   | [action] | [vibery component] | [if any]  |
| 2   | [action] | [vibery component] | [if any]  |

### Variables

- [var1]: [source]
- [var2]: [source]

### Error Handling

- If [step] fails: [action]
```

---

### Phase 3: Workflow Generation

#### Entry Check

```
IF workflow analyzed:
    → Generate appropriate format
ELSE
    → Return to Phase 2
```

#### Hook Generation

```yaml
# hooks/[workflow-name].yaml
name: [workflow-name]
description: [what it does]

triggers:
  - type: PostToolUse # or PreToolUse, Stop
    tools: [Write, Edit] # which tools trigger

actions:
  - name: [step-1-name]
    command: [command to run]
    condition: [optional condition]

  - name: [step-2-name]
    command: [command to run]
```

**Install command:**

```bash
npx vibery install hook:[workflow-name]
# Or copy to .claude/hooks/
```

#### Custom Command Generation

```markdown
# .claude/commands/[workflow-name].md

[Description of what this workflow does]

## Steps

1. First, I'll [action 1]
2. Then, [action 2]
3. Finally, [action 3]

## Input

$ARGUMENTS

## Execution

[Detailed instructions for Claude to follow]

### Step 1: [Name]

[Instructions]

### Step 2: [Name]

[Instructions]

### Confirmation

Before completing, verify:

- [ ] [check 1]
- [ ] [check 2]
```

#### GitHub Action Generation

```yaml
# .github/workflows/[workflow-name].yml
name: [Workflow Name]

on:
  [trigger]: [conditions]

jobs:
  [job-name]:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: [Step 1]
        run: [command]

      - name: [Step 2]
        run: [command]
```

#### Shell Script Generation

```bash
#!/bin/bash
# [workflow-name].sh
# [Description]

set -e  # Exit on error

# Step 1: [Name]
echo "→ [Description]"
[command]

# Step 2: [Name]
echo "→ [Description]"
[command]

echo "✓ Workflow complete"
```

---

### Phase 4: Integration & Testing

#### Entry Check

```
IF workflow generated:
    → Add integration and test instructions
ELSE
    → Return to Phase 3
```

#### Integration Instructions

````markdown
## Installation

### Option 1: Vibery Install (if published)

```bash
npx vibery install [workflow-name]
```
````

### Option 2: Manual Install

```bash
# Copy to appropriate location:
cp [file] [destination]

# Make executable (if script):
chmod +x [file]
```

## Testing

### Dry Run

[Commands to test without side effects]

### Verification

After running, check:

- [ ] [expected outcome 1]
- [ ] [expected outcome 2]

## Troubleshooting

### Common Issues

| Issue   | Cause   | Fix   |
| ------- | ------- | ----- |
| [issue] | [cause] | [fix] |

````

---

### Phase 5: Output Delivery

#### Output Format
```markdown
# Workflow: [Name]

## Overview
[One sentence description]

## Trigger
[When this runs]

## Installation
[Copy-paste commands]

## Configuration
[File content to create]

## Usage
[How to run/trigger]

## Customization
[What can be modified]

## Related Workflows
[Suggest complementary automations]
````

---

## Common Workflow Templates

### Feature Development Workflow

```
Trigger: /feature [name]
Steps:
1. Create branch: git checkout -b feature/[name]
2. Generate spec: /spec-writer
3. Plan architecture: architect-planner
4. Create files: Based on plan
5. Generate tests: /generate-tests
6. Create PR: /create-pr
```

### Code Review Workflow

```
Trigger: PostToolUse on Edit
Steps:
1. Lint: Run project linter
2. Type check: Run tsc/mypy
3. Test affected: Run related tests
4. Format: Auto-format on save
```

### Release Workflow

```
Trigger: /release [version]
Steps:
1. Run full test suite
2. Update version in package.json
3. Generate changelog
4. Create git tag
5. Push with tags
6. Create GitHub release
```

### Documentation Workflow

```
Trigger: /docs
Steps:
1. Scan for undocumented functions
2. Generate JSDoc/docstrings
3. Update README if needed
4. Generate API docs
```

---

## Self-Check (Read before every response)

□ Is the trigger clear and specific?
→ Vague triggers = unexpected executions

□ Are steps atomic and ordered?
→ Each step should do one thing

□ Did I include error handling?
→ Workflows fail; handle gracefully

□ Is output copy-paste ready?
→ User shouldn't need to modify

□ Did I include testing instructions?
→ Untested workflows = broken workflows

□ Is the workflow actually saving time?
→ Automation overhead vs manual time

□ Can it be undone if something goes wrong?
→ Include rollback instructions for risky steps

---

## Integration with Vibery

```
SUGGEST after workflow created:
    - "Publish to Vibery: npx vibery publish"
    - "Share with team: Add to project .claude/"
    - "Combine with: [related workflows]"
```
