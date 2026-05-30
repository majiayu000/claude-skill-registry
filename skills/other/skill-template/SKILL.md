---
name: skill-template
description: Generate custom skill/command from template
user-invocable: true
---

# Skill Template Generator

Generate a custom skill (slash command) based on requirements.

**Usage**: `/skill-template [skill-name] [purpose]`

---

## Templates

| Purpose | Template | Features |
|---------|----------|----------|
| Workflow | Multi-step | Sequential steps |
| Generator | Creator | File creation |
| Checker | Validator | Validation rules |
| Automation | Runner | Command execution |
| Agent-backed | Delegator | Runs as agent |

---

## Process

1. **Gather Requirements**
   - Skill name (lowercase, hyphenated)
   - Purpose
   - Arguments (if any)
   - Workflow steps
   - Context isolation (fork)?
   - Agent backing?
   - Tool restrictions?

2. **Select Template** based on purpose

3. **Generate File** at `.claude/skills/[name]/SKILL.md`

4. **Validate** with `/skill-check`

---

## Frontmatter Reference

```yaml
---
name: skill-name              # Required: lowercase, hyphenated
description: What it does     # Required: shown in / menu
version: 0.1.0                # Optional: semantic version
user-invocable: true          # Optional: appears in / menu (default true)
model: sonnet                 # Optional: inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan
allowed-tools:                # Optional: restrict available tools (YAML list)
  - Read
  - Write
  - Bash
context: fork                 # Optional: isolated context
agent: agent-name             # Optional: delegate to agent (requires context: fork)
argument-hint: "<hint>"       # Optional: hint shown after skill name
# arguments:                  # Optional: structured argument definitions
#   - name: target
#     description: The target to process
#     required: true
# when_to_use: >              # Optional: auto-trigger description (underscore, NOT hyphen)
#   Use when the user asks about deployment or mentions staging.
disable-model-invocation: false  # Optional: prevent programmatic invocation
hooks:                        # Optional: lifecycle hooks
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: echo "Bash used"
  Stop:
    - hooks:
        - type: command
          command: ./scripts/verify.sh
          once: true
---
```

---

## Workflow Template Structure

```markdown
---
name: [name]
description: [What it does]
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
context: fork
argument-hint: "<task-description>"
---

# [Skill Name]

## Workflow
### Step 1: [Name]
### Step 2: [Name]
### Step 3: [Name]

## Arguments
Uses `$ARGUMENTS` for input

## Output
Summary when complete
```

---

## Example

```
/skill-template deploy-staging "deploy to staging"

Output: Created .claude/skills/deploy-staging/SKILL.md

Usage: /deploy-staging
```
