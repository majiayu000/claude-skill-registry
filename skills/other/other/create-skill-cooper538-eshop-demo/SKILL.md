---
name: create-skill
description: Create a new Claude Code skill with proper structure and best practices. Use when user wants to create a custom skill, slash command, or extend Claude capabilities.
allowed-tools: Read, Write, Bash, Glob, Grep, WebFetch, AskUserQuestion
---

# Skill Creator

Help users create well-structured Claude Code skills following best practices.

## Usage

```
/create-skill              # Interactive mode
/create-skill <name>       # Create skill with given name
```

## Arguments

- `$1` - Optional skill name (if not provided, will ask interactively)
- `$ARGUMENTS` - Full arguments passed to the skill

## Process

### 1. Gather Requirements

Ask about:
- **Name**: What should the skill be called? (becomes `/skill-name`)
- **Purpose**: What problem does it solve?
- **Tools needed**: Bash, WebFetch, Read, Write, etc.
- **Arguments**: Does it need user input? (`$1`, `$2`, `$ARGUMENTS`)

### 2. Create Skill Structure

**Project-level** (shared with team):
```
.claude/skills/<skill-name>/
├── SKILL.md           # Main skill definition
└── templates/         # Optional template files
```

**Personal** (only for this user):
```
~/.claude/skills/<skill-name>/SKILL.md
```

### 3. Generate SKILL.md

Use this template:

```yaml
---
name: skill-name
description: When Claude should use this skill automatically.
allowed-tools: List, Of, Required, Tools
---

# Skill Title

Clear instructions for what Claude should do.

## Usage
[Examples of how to invoke]

## Arguments
- `$ARGUMENTS` - All arguments passed
- `$1`, `$2` - Positional arguments

## Process
1. Step one
2. Step two

## Output Format
[Expected output description]
```

### 4. Available Tools & Features

**Common tools**: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, Task

**Bash in prompts** (requires `allowed-tools: Bash`):
```markdown
Current status:
!git status --short
```

**File embedding**:
```markdown
Review this file:
@src/main.ts
```

## Output Format

After gathering requirements, generate:
1. Complete `SKILL.md` file
2. Any supporting template files
3. Instructions for testing the skill

## Example

```yaml
---
name: commit
description: Create a well-formatted git commit. Use when user wants to commit changes.
allowed-tools: Bash
---

Analyze staged changes and create a conventional commit:

!git diff --cached --stat
!git diff --cached

Create a commit message following conventional commits format.
```

---

Now let's create your skill! What do you want to build?
