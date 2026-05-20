---
context: fork
model: sonnet
description: Create new skills with guided prompts following best practices
---

# /skill-creator

Create a new skill for the vault with guided prompts, following clawdbot's meta-skill pattern.

## Usage

```
/skill-creator <skill-name>
/skill-creator transcribe
/skill-creator vendor-comparison
```

## Instructions

### Phase 1: Initial Setup

1. Parse the skill name from the command
2. Check if a skill with this name already exists in `.claude/skills/`
3. If exists, warn and ask if they want to overwrite or rename

### Phase 2: Gather Skill Metadata (6-Step Process)

Ask the user these questions in sequence:

#### Step 1: Purpose & Description

**Question**: "What does this skill do? (One sentence)"

- This becomes the `description:` field in frontmatter
- Should be concise and action-oriented
- Example: "Convert voice recordings to text using Whisper API"

#### Step 2: Model Tier

**Question**: "Which model tier is appropriate?"

| Option              | When to Use                                                    |
| ------------------- | -------------------------------------------------------------- |
| **haiku** (default) | Fast, simple tasks - note creation, searches, quick transforms |
| **sonnet**          | Complex analysis, code review, multi-step reasoning            |
| **opus**            | Deep research, complex planning, extended reasoning            |

Store in `model:` frontmatter field.

#### Step 3: Execution Context

**Question**: "How should this skill execute?"

| Option             | When to Use                                |
| ------------------ | ------------------------------------------ |
| **fork** (default) | Independent execution, can run in parallel |
| **orchestrate**    | Coordinates multiple dependent sub-agents  |
| _(no context)_     | Single-session, simple execution           |

Store in `context:` frontmatter field.

#### Step 3b: Agent Type (v2.1.0+)

**Question**: "Should this skill use a specific agent type?"

| Option              | When to Use                    |
| ------------------- | ------------------------------ |
| _(omit - default)_  | Use default agent behaviour    |
| **Explore**         | Read-only codebase exploration |
| **Plan**            | Design implementation plans    |
| **general-purpose** | Full capabilities needed       |

Store in `agent:` frontmatter field (optional).

#### Step 4: Input Parameters

**Question**: "What inputs does this skill need?"

Gather:

- Required parameters (e.g., `<title>`, `<project>`, `<path>`)
- Optional parameters (e.g., `[--format png]`, `[for <project>]`)
- Any flags or options

#### Step 5: Output Format

**Question**: "What does this skill produce?"

Options:

- Creates a new note (specify type)
- Modifies existing note
- Generates report/output to screen
- Creates file(s) in specific location
- Multiple outputs

#### Step 6: Example Usage

**Question**: "Give 2-3 example commands"

Examples help users understand the skill quickly.

### Phase 3: Generate Skill File

Create the skill file at `.claude/skills/{{skill-name}}.md`:

```markdown
---
context: { { context } }
model: { { model } }
agent: { { agent or omit if not specified } }
description: { { description } }
allowed-tools: # v2.1.0+ YAML-style tool restrictions (optional)
  - Read
  - Glob
  - Grep
---

# /{{skill-name}}

{{description}}

## Usage

\`\`\`
/{{skill-name}} {{parameters}}
\`\`\`

## Examples

\`\`\`
{{example 1}}
{{example 2}}
{{example 3}}
\`\`\`

## Instructions

### 1. Parse Input

Parse the command for:
{{list of parameters and their validation}}

### 2. Validate Prerequisites

{{any prerequisites or checks}}

### 3. Execute Skill

{{main skill logic - break into numbered steps}}

### 4. Output Results

{{how to present results to user}}

## Error Handling

- {{common error scenarios and recovery}}

## Related Skills

- {{links to related skills}}
```

### Phase 4: Register Skill

1. Add skill to CLAUDE.md skill table (suggest to user)
2. Display the created skill content for review
3. Offer to test the skill immediately

### Phase 5: Quality Checklist

Before finalising, verify:

- [ ] Description is concise (< 80 chars)
- [ ] Model tier matches complexity
- [ ] Context type is appropriate
- [ ] Examples are realistic
- [ ] Instructions are numbered and clear
- [ ] Error handling is included
- [ ] Related skills are linked

## Skill Design Principles (from clawdbot)

1. **Token Efficiency**: "The context window is a public good" - include only what Claude needs
2. **Progressive Disclosure**: Metadata first, full instructions on-demand
3. **Documentation-First**: The skill file IS the interface
4. **Minimal Dependencies**: Skills should be self-contained
5. **Clear Triggers**: Description should make it obvious when to use

## Output

After creation:

```
Created skill: .claude/skills/{{skill-name}}.md

Skill Summary:
- Name: /{{skill-name}}
- Description: {{description}}
- Model: {{model}}
- Context: {{context}}

Next steps:
1. Review the skill content
2. Add to CLAUDE.md skill table
3. Test with: /{{skill-name}} {{example}}

Would you like to test this skill now?
```

## Related Skills

- [[.claude/skills/archive/SKILL.md|/archive]] - Skill lifecycle management
- [[.claude/skills/rename/SKILL.md|/rename]] - Batch operations pattern
