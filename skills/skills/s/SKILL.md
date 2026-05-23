---
name: s
description: Discover available skills and subagents. Auto-triggers on: /s, show skills, list skills, available skills, what can you do, help with skills, what agents, list agents
allowed-tools: Bash, Read
---

# Skill Discovery

Dynamically discover all available skills and subagent types.

## Usage

Run the discovery script to list all skills:

```bash
python3 .claude/skills/s/scripts/discover.py
```

## Subagent Types

Subagents are spawned via the **Task tool**. Available types are defined in the Task tool's system description. To see current subagent types, check the `subagent_type` parameter in your Task tool definition.

Common subagent types include:
- **Explore** - Fast codebase exploration, file finding, searches
- **general-purpose** - Complex multi-step tasks, research
- **Bash** - Git operations, command execution
- **Plan** - Architecture decisions, implementation planning

Note: Subagent types are defined by the Task tool, not this skill. Check your tool definitions for the authoritative list.

## How Skills Work

Skills live in `.claude/skills/<name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: What it does AND when to trigger (keywords here!)
allowed-tools: Read, Edit, Write, Task
---
```

- **Triggering**: Skills auto-trigger based on keywords in their `description` field
- **Invocation**: Use `/<skill-name>` or natural language matching trigger keywords
- **Tools**: Each skill declares what tools it can use in `allowed-tools`

## Adding New Skills

Use the skill-creator skill: `/skill-creator <description>`
