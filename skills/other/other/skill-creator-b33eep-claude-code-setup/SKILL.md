---
name: skill-creator
description: This skill guides users through creating custom skills for claude-code-setup. Use when users want to create a new command or context skill.
type: command
source: Inspired by https://github.com/AJBcoding/claude-skill-eval
---

# Skill Creator

Guide users through creating high-quality custom skills for claude-code-setup.

## Overview

Skills extend Claude's capabilities with specialized knowledge and workflows. This skill helps users create their own custom skills stored in `~/.claude/custom/skills/`.

**Skill types:**
- **Command skills**: Invoked explicitly with `/skill-name`
- **Context skills**: Auto-loaded based on project's Tech Stack

## Creation Flow

Follow these steps in order. Use conversational interaction - ask one question at a time.

### Step 1: Determine Skill Type

Ask the user:

```
What type of skill do you want to create?

1. **Command skill** - Invoked explicitly with /skill-name
   Example: /deploy-staging, /generate-report

2. **Context skill** - Auto-loads based on project's tech stack
   Example: Company coding standards, API conventions
```

### Step 2: Gather Concrete Examples

This is the most important step for quality. Ask based on skill type:

**For command skills:**
```
Give me 2-3 concrete examples of how you'd use this skill.
Format: "I say X and expect Y"

Example:
- "Deploy to staging" → push code, SSH to server, run deploy script
- "Generate weekly report" → gather metrics, format as markdown, save to docs/
```

**For context skills:**
```
Give me 2-3 concrete examples of how this skill should guide Claude.
Format: "When doing X, Claude should Y"

Example:
- When writing API endpoints, use our standard response format
- When handling errors, use our custom exception classes
- When writing tests, follow our naming convention
```

### Step 3: Analyze and Suggest

Based on the examples, identify:

1. **Name suggestion** (kebab-case)
2. **Patterns/workflows** in the examples
3. **For context skills**: Suggest `applies_to` values based on mentioned technologies

Present the analysis:

```
Based on your examples, I see a [pattern description].

Suggested name: [name]
[For context skills only:]
Suggested applies_to: [tech1, tech2, ...]

Want to add more tech stacks? (comma-separated, or continue)
```

### Step 4: Generate or Review Content

Ask the user:

```
Should I generate the skill content based on your examples,
or do you want to provide the instructions yourself?

1. Generate for me
2. I'll provide it
```

**If generating:**
- Create clear, actionable instructions based on the examples
- Structure with headers for different workflows/scenarios
- Include relevant details from the examples

**If user provides:**
- Ask them to paste or describe the content
- Review their content and suggest improvements:
  - Missing details that would help Claude
  - Unclear instructions
  - Missing examples
- Ask: "Should I incorporate these suggestions?"

### Step 5: Review and Refine

Present the complete SKILL.md draft:

```markdown
---
name: [name]
description: [1-2 sentence description]
type: [command|context]
[applies_to: [tech1, tech2, ...]]  # Only for context skills
[file_extensions: [".ext1", ".ext2"]]  # Only for context skills with file mappings
---

# [Title]

[Content...]
```

Ask: "Does this look good? Any changes needed?"

Iterate until the user approves.

### Step 6: Save the Skill

1. Create directory: `~/.claude/custom/skills/[name]/`
2. Write the SKILL.md file
3. Confirm creation with usage instructions:

**For command skills:**
```
Created: ~/.claude/custom/skills/[name]/SKILL.md

To use: /[name]
To edit: Modify the SKILL.md file directly
```

**For context skills:**
```
Created: ~/.claude/custom/skills/[name]/SKILL.md

This skill will auto-load when your project's Tech Stack includes:
[tech1], [tech2], or [tech3]

To edit: Modify the SKILL.md file directly
```

## Skill Format Reference

### Command Skill

```yaml
---
name: skill-name
description: Brief description of what this skill does
type: command
---

# Skill Title

Instructions for Claude to follow when this skill is invoked.
```

### Context Skill

```yaml
---
name: skill-name
description: Brief description of what this skill provides
type: context
applies_to: [python, fastapi, django]
file_extensions: [".py"]
---

# Skill Title

Standards or guidelines that Claude should follow automatically.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (kebab-case, e.g., `deploy-staging`) |
| `description` | Yes | What the skill does (1-2 sentences, third person) |
| `type` | Yes | `command` or `context` |
| `applies_to` | Context only | List of tech stacks that trigger auto-load |
| `file_extensions` | Context only | File extensions that trigger task-based loading (e.g., `[".py"]`) |

### Common `applies_to` Values

Languages: `python`, `typescript`, `javascript`, `rust`, `go`, `java`
Frameworks: `fastapi`, `django`, `flask`, `react`, `nextjs`, `express`
Tools: `docker`, `kubernetes`, `terraform`, `aws`, `gcp`

## Quality Guidelines

When generating or reviewing skill content:

1. **Be specific** - Vague instructions lead to inconsistent results
2. **Include examples** - Show what good output looks like
3. **Structure clearly** - Use headers, lists, tables
4. **Stay focused** - One skill per domain/workflow
5. **Test mentally** - Would Claude know what to do with these instructions?

## Output Location

All custom skills are saved to:

```
~/.claude/custom/skills/[skill-name]/
└── SKILL.md
```

This location is separate from the base installation (`~/.claude/skills/`) and survives upgrades.
