---
name: copy-agent
description: Copy an agent from Product Forge to user or project level
argument-hint: "[<plugin>:<agent-name>] [--user | --project]"
---

# Copy Agent

Copy an agent from Product Forge plugins to your user-level (`~/.claude/`) or project-level (`.claude/`) directory.

## Usage

```bash
# List available agents
/copy-agent

# Copy to project (default)
/copy-agent product-design:product-architect

# Copy to user level
/copy-agent git-workflow:commit-expert --user

# Explicit project level
/copy-agent python-experts:django-expert --project
```

## Arguments

- `<plugin>:<agent-name>` - The agent to copy in `plugin:name` format
- `--user` - Copy to `~/.claude/{plugin}/agents/{name}.md`
- `--project` - Copy to `.claude/{plugin}/agents/{name}.md` (default)

## What Gets Copied

Agents are single markdown files (`.md`) containing:
- YAML frontmatter with name, description, tools, model, and color
- Agent capabilities and activation triggers
- Autonomous workflow definitions

## Directory Structure

```
# Project-level (default)
.claude/
└── git-workflow/
    └── agents/
        └── commit-expert.md

# User-level (--user)
~/.claude/
└── git-workflow/
    └── agents/
        └── commit-expert.md
```

## Execution Instructions

When the user runs this command:

### No Arguments - List Available Agents

1. **Scan Product Forge plugins cache** for all available agents:
   ```bash
   ls ~/.claude/plugins/cache/product-forge-marketplace/*/agents/*.md 2>/dev/null
   ```

2. **For each plugin with agents**, list them with descriptions:
   - Read agent file frontmatter to get `name`, `description`, and `model`
   - Format as: `{plugin}:{agent-name} ({model}) - {description}`

3. **Display formatted list**:
   ```
   Available agents from Product Forge:

   product-design:
     product-architect (sonnet) - Full product development guidance
     prd-orchestrator (sonnet) - PRD lifecycle management
     qa-tester (sonnet) - Manual QA test procedure creation
     web-debugger (sonnet) - Web application debugging
     ...

   git-workflow:
     commit-expert (haiku) - Git commit specialist
     rebase-expert (haiku) - Git rebase specialist
     code-review-expert (sonnet) - Code review orchestrator
     ...

   python-experts:
     django-expert (sonnet) - Django web application specialist
     fastapi-expert (sonnet) - FastAPI async REST API specialist
     ...

   Usage: /copy-agent <plugin>:<agent-name> [--user | --project]
   ```

### With Arguments - Copy Agent

1. **Parse arguments**:
   - Extract `plugin` and `agent-name` from `<plugin>:<agent-name>` format
   - Determine destination: `--user` or `--project` (default)

2. **Locate source agent**:
   ```bash
   SOURCE=~/.claude/plugins/cache/product-forge-marketplace/{plugin}/agents/{agent-name}.md
   ```
   - If not found, show error with available agents from that plugin

3. **Determine destination path**:
   - `--project`: `.claude/{plugin}/agents/{agent-name}.md`
   - `--user`: `~/.claude/{plugin}/agents/{agent-name}.md`

4. **Check if destination exists**:
   - If exists, use **AskUserQuestion** to prompt:
     ```
     Agent '{agent-name}' already exists at {destination}.

     Options:
     - Overwrite: Replace existing agent
     - Rename: Save as {agent-name}-copy.md
     - Cancel: Abort operation
     ```

5. **Create destination directory structure**:
   ```bash
   mkdir -p {destination_dir}
   ```

6. **Copy agent file**:
   ```bash
   cp {source} {destination}
   ```

7. **Confirm success**:
   ```
   Agent copied successfully!

   Source: ~/.claude/plugins/cache/product-forge-marketplace/{plugin}/agents/{agent-name}.md
   Destination: {destination}

   The agent is now available in your {project|user} configuration.
   ```

## Error Handling

- **Plugin not found**: Show list of available plugins
- **Agent not found**: Show list of agents in that plugin
- **Invalid format**: Show usage example with correct format
- **Copy failed**: Show error and suggest checking permissions
