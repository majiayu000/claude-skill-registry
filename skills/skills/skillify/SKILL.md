---
name: skillify
description: Turn a transcript summary into a reusable Claude skill. Researches the topic and creates a skill file.
user_invocable: true
---

# Skillify - Convert Summaries to Claude Skills

This command takes a transcript summary, researches the topic deeply, and creates a reusable Claude skill that captures that knowledge.

## Workflow

### Step 1: Select a Summary

Ask the user:
> Which summary would you like to turn into a skill?
>
> Options:
> 1. **Paste a summary** - Copy/paste content from a summary file
> 2. **Pick from summaries/** - I'll list available summaries for you to choose
> 3. **Use a transcript** - Pick from transcripts/ directory

If they choose to pick from files, list available summaries:
```bash
ls -la summaries/*/*.md 2>/dev/null || echo "No summaries yet"
ls -la transcripts/*.txt 2>/dev/null || echo "No transcripts yet"
```

### Step 2: Analyze the Content

Read the selected summary/transcript and identify:
- **Main topic**: What is this about?
- **Key concepts**: What specific techniques, tools, or ideas are discussed?
- **Actionable patterns**: What can someone DO with this knowledge?

### Step 3: Web Research

Use web search to deepen understanding of the topic:

1. Search for the main concepts mentioned
2. Find best practices and additional context
3. Look for related tools, techniques, or resources
4. Gather examples and use cases

Research queries to run:
- "{main topic} best practices"
- "{key concept} tutorial"
- "{technique mentioned} examples"
- "how to {actionable pattern}"

### Step 4: Ask for Skill Destination

Ask the user:
> Where would you like to save this skill?
>
> Examples:
> - `~/.claude/skills/` - Your global skills (available in all projects)
> - `./.claude/skills/` - This project only
> - Custom path

Also ask:
> What should the skill be named? (kebab-case)
>
> Example: `agentic-engineering` or `context-window-management`

### Step 5: Create the Skill

Create the skill directory and SKILL.md file:

```
{destination}/{skill-name}/
└── SKILL.md
```

The SKILL.md should follow this structure:

```markdown
---
name: {skill-name}
description: {One-line description}. Use when {trigger conditions}.
user_invocable: false
---

# {Skill Title}

## Overview
{2-3 sentence summary of what this skill covers}

## Key Concepts

### {Concept 1}
{Explanation with examples}

### {Concept 2}
{Explanation with examples}

## When to Apply

Use this knowledge when:
- {Situation 1}
- {Situation 2}
- {Situation 3}

## Best Practices

1. **{Practice 1}**: {Explanation}
2. **{Practice 2}**: {Explanation}
3. **{Practice 3}**: {Explanation}

## Examples

### Example 1: {Title}
{Concrete example with code/steps if applicable}

### Example 2: {Title}
{Another example}

## Common Mistakes

- **{Mistake 1}**: {Why it's wrong and how to fix}
- **{Mistake 2}**: {Why it's wrong and how to fix}

## Related Topics

- {Related topic 1}
- {Related topic 2}

## Sources

- {Source from web research}
- {Original video URL}
```

### Step 6: Confirm Creation

After creating the skill, report:
- Skill location
- Skill name
- Brief summary of what was captured
- How to use/reference the skill

---

## Example

User: `/skillify`

Claude: Which summary would you like to turn into a skill?

User: Use the agentic-engineering summary

Claude:
1. [Reads summary]
2. [Identifies key concepts: planning phase, agent-first setup, validation loops]
3. [Searches web for best practices]
4. [Asks where to save]

User: Save to ~/.claude/skills/ as "agentic-engineering"

Claude:
1. [Creates ~/.claude/skills/agentic-engineering/SKILL.md]
2. [Populates with researched content]
3. [Reports success]

---

## Output Example

After running `/skillify`, users get a skill file like:

```markdown
---
name: agentic-engineering
description: Best practices for AI-assisted development. Use when planning projects for Claude Code or other AI coding assistants.
user_invocable: false
---

# Agentic Engineering

## Overview
Agentic engineering is an approach to software development that optimizes for AI coding assistants...

## Key Concepts

### 90% Planning, 10% Execution
Most effort should go into research, discovery, and planning before writing code...

### Agent-First Project Setup
Structure projects so AI agents can easily navigate and understand context...

...
```

## Notes

- The skill should capture ACTIONABLE knowledge, not just information
- Include concrete examples whenever possible
- Reference the original video as a source
- Make the skill useful for future Claude Code sessions
