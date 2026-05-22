---
name: agent-registry
description: Guide for managing the Agent Registry - database-backed agent configuration system. Use when asked to "configure agents", "manage skills", "set tool permissions", "create context rules", or when working with agent assignments per platform/chat. Covers dashboard UI, API endpoints, CLI commands, and MCP tools.
---

# Agent Registry Management

## Overview

The Agent Registry is a database-backed system for managing AI agent configurations. It replaces file-based configuration with a centralized, dynamic approach that supports:

- **Agent definitions** - Name, model, base prompt, enabled status
- **Skill assignments** - Which skills each agent has access to
- **Tool permissions** - Allow/deny patterns for MCP tools
- **Context rules** - Agent selection based on platform, chat, environment

## Quick Reference

### Dashboard UI

Access the Agents tab in the dashboard at `http://localhost/` → Management → Agents

Features:

- View all agents with stats (total, enabled, skills, context rules)
- Edit agent details (name, description, model, prompt)
- Manage skills (checkbox list of available skills)
- Configure tool patterns (allow/deny lists)
- View agent details with all configurations

### CLI Commands

```bash
# Sync database config to filesystem (for OpenCode)
npm run agents:sync

# Sync with verbose output
npm run agents:sync -- --verbose

# Dry run (show what would change)
npm run agents:sync -- --dry-run

# Sync for specific environment
npm run agents:sync -- --env prod

# Seed default agents
npm run agents:seed

# Force re-seed (overwrites existing)
npm run agents:seed:force

# Run database migration
npm run db:migrate
```

### MCP Tools

Two MCP tools are available for agents to self-discover their capabilities:

**ai_first_get_agent_context**

```json
{
  "platform": "whatsapp",
  "chatId": "123456789",
  "environment": "local"
}
```

Returns: Agent role, enabled skills, allowed tools, base prompt

**ai_first_list_agents**

```json
{
  "includeDetails": true
}
```

Returns: All registered agents with optional skill/tool details

## Database Schema

### Tables

| Table           | Purpose                                                   |
| --------------- | --------------------------------------------------------- |
| `agents`        | Core agent definitions (id, name, model, prompt, enabled) |
| `agent_skills`  | Skills assigned to each agent                             |
| `agent_tools`   | Tool allow/deny patterns per agent                        |
| `context_rules` | Rules for agent selection by context                      |

### Context Types

| Type          | Context ID                     | Purpose                                  |
| ------------- | ------------------------------ | ---------------------------------------- |
| `default`     | null                           | Fallback agent when no other rules match |
| `platform`    | whatsapp/slack/opencode/cursor | Platform-specific agent                  |
| `chat`        | Chat/Channel ID                | Chat-specific agent assignment           |
| `channel`     | Slack channel name             | Channel-specific agent                   |
| `environment` | local/prod                     | Environment-specific skill overrides     |

## Default Agents

| Agent        | Mode        | Skills                                                                                         | Description                                     |
| ------------ | ----------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| pm-assistant | primary     | jira-management, workflow-management, presentation-updates, message-scheduling, tool-discovery | JIRA, meetings, workflows, project management   |
| communicator | specialized | slack-formatting, whatsapp-messages                                                            | Slack/WhatsApp messaging with proper formatting |
| scheduler    | specialized | message-scheduling, tool-discovery                                                             | Calendar management, reminders                  |
| explorer     | specialized | project-architecture, tool-discovery                                                           | Fast codebase exploration                       |

## API Endpoints

All endpoints require authentication via JWT token.

### Agent CRUD

| Method | Endpoint                 | Description             |
| ------ | ------------------------ | ----------------------- |
| GET    | `/api/agents`            | List all agents         |
| GET    | `/api/agents/stats`      | Get registry statistics |
| GET    | `/api/agents/:id`        | Get agent with details  |
| POST   | `/api/agents`            | Create new agent        |
| PATCH  | `/api/agents/:id`        | Update agent            |
| DELETE | `/api/agents/:id`        | Delete agent            |
| POST   | `/api/agents/:id/toggle` | Toggle enabled status   |

### Skills

| Method | Endpoint                       | Description               |
| ------ | ------------------------------ | ------------------------- |
| GET    | `/api/agents/:id/skills`       | Get agent's skills        |
| PUT    | `/api/agents/:id/skills`       | Replace agent's skills    |
| GET    | `/api/agents/available-skills` | List all available skills |

### Tools

| Method | Endpoint                | Description                  |
| ------ | ----------------------- | ---------------------------- |
| GET    | `/api/agents/:id/tools` | Get agent's tool patterns    |
| PUT    | `/api/agents/:id/tools` | Set tool allow/deny patterns |

### Context Rules

| Method | Endpoint                        | Description            |
| ------ | ------------------------------- | ---------------------- |
| GET    | `/api/agents/context-rules`     | List all context rules |
| POST   | `/api/agents/context-rules`     | Create context rule    |
| DELETE | `/api/agents/context-rules/:id` | Delete context rule    |

### Operations

| Method | Endpoint                      | Description               |
| ------ | ----------------------------- | ------------------------- |
| POST   | `/api/agents/sync`            | Trigger filesystem sync   |
| POST   | `/api/agents/resolve-context` | Resolve agent for context |

## Context Resolution

When resolving an agent for a request:

1. Get all context rules sorted by priority (highest first)
2. Match rules against context (platform, chat, environment)
3. Apply skill overrides from matching rules
4. Return agent with effective skills and tools

Priority order: chat-specific > channel-specific > platform-specific > environment > default

## Filesystem Sync

For OpenCode/Cursor compatibility, agent configurations are synced to:

- `.claude/skills/` - Skill directories for enabled skills
- `opencode.json` - Model configuration (future)

The sync runs:

- On demand via `npm run agents:sync`
- Before OpenCode starts (in Docker entrypoint)
- Via dashboard "Sync" button

## Extending

### Adding a New Agent

1. Via Dashboard: Agents tab → Add New Agent
2. Via API: POST `/api/agents` with agent definition
3. Via Seed: Update `data/seeds/agents.ts`

### Adding Skills to an Agent

1. Via Dashboard: Click agent → Edit Skills → Select skills
2. Via API: PUT `/api/agents/:id/skills` with skill names array

### Creating Context Rules

For chat-specific agent:

```json
{
  "contextType": "chat",
  "contextId": "120363406740668957",
  "agentId": "specialized-agent",
  "priority": 100
}
```

For platform-wide agent:

```json
{
  "contextType": "platform",
  "contextId": "whatsapp",
  "agentId": "communicator",
  "priority": 50
}
```

## Troubleshooting

### Agent not appearing

1. Check if agent is enabled: `GET /api/agents/:id`
2. Verify database connection
3. Check logs for errors

### Skills not syncing

1. Run `npm run agents:sync -- --verbose --dry-run`
2. Check skill source directory exists
3. Verify skill is assigned to agent

### Context not resolving

1. Check context rules: `GET /api/agents/context-rules`
2. Verify rule priorities
3. Test with: `POST /api/agents/resolve-context`
