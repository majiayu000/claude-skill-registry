---
name: edit-skill
description: View, edit, or create Claude Code skills. Lists available skills, shows skill structure, and helps modify skill instructions.
allowed-tools: Read, Glob, Grep, Write, Edit, TodoWrite, AskUserQuestion
---

# Edit Skill - Skill Editor

**View, edit, or create Claude Code skills with guidance on structure and best practices.**

---

## Phase 1: Understand the Request

Parse the user's input to determine the action:

| Action | Triggers |
|--------|----------|
| **List** | "list skills", "show skills", "what skills exist" |
| **View** | "show skill X", "view skill X", "read skill X" |
| **Edit** | "edit skill X", "update skill X", "modify skill X" |
| **Create** | "create skill X", "new skill X", "add skill X" |

If no specific action, ask the user what they want to do.

---

## Phase 2: List Available Skills

When listing skills, scan the skills directory:

```
.claude/skills/*/skill.md
.claude/skills/*/SKILL.md
```

For each skill, extract and display:
- **Name**: from frontmatter `name` field
- **Description**: from frontmatter `description` field
- **Location**: file path

Present as a formatted table:

```markdown
## Available Skills

| Skill | Description | Path |
|-------|-------------|------|
| task | Execute complex tasks with planning... | .claude/skills/task/SKILL.md |
| feature | Execute complete feature development... | .claude/skills/feature/skill.md |
```

---

## Phase 3: View a Skill

When viewing a skill:

1. Read the skill file
2. Display the full content to the user
3. Explain the structure:
   - Frontmatter (name, description, allowed-tools)
   - Skill phases/sections
   - Key patterns used

---

## Phase 4: Edit a Skill

When editing a skill:

1. **Read current content** - Show the user what exists
2. **Ask what to change** - Use AskUserQuestion for clarity:

```
AskUserQuestion(
  questions: [
    {
      question: "What aspect of the skill do you want to modify?",
      header: "Edit Target",
      options: [
        { label: "Description", description: "Update the skill description in frontmatter" },
        { label: "Allowed Tools", description: "Change which tools the skill can use" },
        { label: "Instructions", description: "Modify the skill's workflow or phases" },
        { label: "Add Section", description: "Add a new section to the skill" }
      ],
      multiSelect: true
    }
  ]
)
```

3. **Make the edit** - Use Edit tool for targeted changes
4. **Show the result** - Display the updated section

---

## Phase 5: Create a New Skill

When creating a new skill:

### Step 1: Gather Requirements

Use AskUserQuestion to understand:

```
AskUserQuestion(
  questions: [
    {
      question: "What type of skill is this?",
      header: "Skill Type",
      options: [
        { label: "Orchestrator", description: "Spawns subagents, coordinates work, never does work directly" },
        { label: "Worker", description: "Does the actual implementation work, called by other skills" },
        { label: "Research", description: "Explores codebase, gathers information, no code changes" },
        { label: "Utility", description: "Simple task automation, single-purpose" }
      ],
      multiSelect: false
    }
  ]
)
```

### Step 2: Determine Tools

Based on skill type, recommend tools:

| Type | Recommended Tools |
|------|-------------------|
| Orchestrator | Task, TodoWrite, TaskOutput |
| Worker | Read, Grep, Glob, Write, Edit, Bash, TodoWrite |
| Research | Task, TodoWrite, TaskOutput, Read, Glob, Grep |
| Utility | Depends on use case |

### Step 3: Create Skill File

Create the skill at: `.claude/skills/<name>/skill.md`

Use this template:

```markdown
---
name: <skill-name>
description: <1-2 sentence description of what the skill does and when to use it>
allowed-tools: <comma-separated list>
---

# <Skill Name> Skill

**<One-line summary of the skill's purpose>**

---

## Overview

<Brief description of what this skill does>

---

## Phase 1: <First Phase>

<Instructions for the first phase>

---

## Phase 2: <Second Phase>

<Instructions for the second phase>

---

## Output Format

<Expected output structure>

---

## Key Principles

1. **Principle 1** - explanation
2. **Principle 2** - explanation
```

### Step 4: Write and Confirm

1. Write the skill file
2. Show the user the created skill
3. Explain how to invoke it: `/skill-name`

---

## Skill Structure Reference

### Frontmatter (Required)

```yaml
---
name: skill-name           # lowercase, hyphenated
description: Brief desc    # When to use this skill
allowed-tools: Tool1, Tool2 # Comma-separated
---
```

### Common Allowed Tools

| Tool | Use Case |
|------|----------|
| Read | Reading files |
| Glob | Finding files by pattern |
| Grep | Searching file contents |
| Write | Creating new files |
| Edit | Modifying existing files |
| Bash | Running commands |
| Task | Spawning subagents |
| TaskOutput | Getting subagent results |
| TodoWrite | Tracking progress |
| AskUserQuestion | User interaction |

### Skill Patterns

**Orchestrator Pattern** (for complex multi-step work):
- Spawns subagents with Task tool
- Never reads files or runs commands directly
- Tracks progress with TodoWrite
- Collects results with TaskOutput

**Worker Pattern** (for actual implementation):
- Reads and edits files directly
- Runs commands (build, lint, test)
- Creates commits
- Returns structured output to orchestrator

**Research Pattern** (for exploration):
- Uses Explore subagent type
- Gathers information without changes
- Returns findings for decision-making

---

## Progress Tracking

Use TodoWrite for multi-step operations:

```yaml
todos:
  - content: "List available skills"
    activeForm: "Listing available skills"
    status: completed
  - content: "Read target skill"
    activeForm: "Reading target skill"
    status: in_progress
  - content: "Make requested edits"
    activeForm: "Making requested edits"
    status: pending
```

---

## Key Principles

1. **Show before edit** - Always display current content before modifying
2. **Ask for clarity** - Use AskUserQuestion when intent is unclear
3. **Preserve structure** - Maintain consistent skill format
4. **Explain changes** - Show what was modified
5. **Validate frontmatter** - Ensure required fields are present
