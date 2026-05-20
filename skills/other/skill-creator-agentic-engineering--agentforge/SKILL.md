---
name: skill-creator
description: Built-in skill for creating, managing, and discovering AgentForge skills. Allows agents to generate new skills from natural language descriptions.
version: 1.0.0
tags:
  - utility
  - meta
  - creation
---

# Skill Creator

**Built-in AgentForge Skill** — Create, manage, and discover skills for your agents.

## Overview

The Skill Creator is a default skill that ships with every AgentForge project. It allows you to:

1. **Create new skills** from natural language descriptions
2. **Browse available skills** in the AgentForge registry
3. **Validate skills** to ensure they follow the Agent Skills Specification

## How to Create a Skill

When a user asks you to create a skill:

1. Ask for the skill name (kebab-case), description, and tags
2. Generate the SKILL.md with proper frontmatter and instructions
3. Create supporting files in references/ and scripts/ directories
4. Save to the workspace/skills/ directory

### Skill Structure

Every AgentForge skill follows the Agent Skills Specification:

```
skills/
  my-skill/
    SKILL.md          # Instructions and metadata (frontmatter)
    references/       # Supporting documentation (optional)
    scripts/          # Executable scripts (optional)
    assets/           # Images and other files (optional)
```

### SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does
version: 1.0.0
tags:
  - category1
  - category2
---

# My Skill

Instructions for the agent on how to use this skill.

## Steps
1. Step one
2. Step two
```

## CLI Commands

```bash
# Create a new skill interactively
agentforge skills create

# Install a skill from the registry
agentforge skills install <name>

# List installed skills
agentforge skills list

# Browse the registry
agentforge skills list --registry

# Search for skills
agentforge skills search <query>

# Get skill details
agentforge skills info <name>

# Remove a skill
agentforge skills remove <name>
```

## Categories

Skills are organized by tags:

| Tag | Description | Examples |
|-----|-------------|---------|
| `web` | Web interaction | HTTP requests, web search, scraping |
| `files` | File operations | Read, write, organize files |
| `data` | Data processing | CSV parsing, data analysis |
| `development` | Dev tools | Code review, git workflow, linting |
| `api` | API interaction | REST testing, API integration |
| `utility` | General-purpose | Calculator, text processing |

## Guidelines

- Skills are instruction-based — they teach agents HOW to do things
- The Mastra Workspace provides the tools (filesystem, sandbox, search)
- Skills provide the knowledge and procedures
- Follow the Agent Skills Specification for compatibility
