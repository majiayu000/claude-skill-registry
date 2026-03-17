---
name: project-architecture
description: Understand the Orient monorepo architecture for making technical decisions. Use this skill when onboarding, adding new features, modifying services, or evaluating design choices. Covers packages, bots, agents, MCP servers, mini-apps, and Docker deployment.
---

# Orient Architecture

## System Overview

Orient is a **pnpm monorepo** implementing an AI-powered project management system. The architecture features a **multi-MCP-server pattern** with pluggable bot frontends (Slack, WhatsApp) connected to a shared AI/Agent infrastructure.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Messaging Frontends                             │
│   ┌─────────────────┐                         ┌─────────────────┐           │
│   │  WhatsApp Bot   │                         │   Slack Bot     │           │
│   │ (@orientbot/bot-wp)│                         │ (@orientbot/bot-sl)│           │
│   └────────┬────────┘                         └────────┬────────┘           │
│            └──────────────────┬────────────────────────┘                     │
│                               ▼                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      Agent Registry                                  │   │
│   │   (@orientbot/agents) - Context resolution, tool permissions, skills   │   │
│   └──────────────────────────────┬──────────────────────────────────────┘   │
│                                  ▼                                           │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                   OpenCode Server (AI Processing)                    │   │
│   │    ├── coding-server  (MCP for dev tasks)                           │   │
│   │    ├── assistant-server (MCP for Slack, WhatsApp, Google, Docs)     │   │
│   │    └── core-server (MCP for skills, system, agents)                 │   │
│   └──────────────────────────────┬──────────────────────────────────────┘   │
│                                  ▼                                           │
│   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│   │   SQLite DB     │ │ Object Storage  │ │ External APIs   │               │
│   │ (Drizzle ORM)   │ │ (MinIO / R2)    │ │ (Atlassian, Google) │           │
│   └─────────────────┘ └─────────────────┘ └─────────────────┘               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Monorepo Structure

```
orient/
├── packages/
│   ├── agents/                # Agent registry, prompts, skills, permissions
│   ├── apps/                  # Mini-apps system (manifests, edit sessions)
│   ├── mcp-servers/           # MCP server types and configs
│   ├── mcp-tools/             # MCP tool definitions and registry
│   ├── core/                  # Shared utilities, config, logging, types
│   ├── database/              # Drizzle ORM schemas (SQLite)
│   ├── database-services/     # DB service implementations
│   ├── integrations/          # External integrations (GitHub, Google, Linear)
│   ├── bot-whatsapp/          # WhatsApp bot (Baileys) - integrated into Dashboard
│   ├── bot-slack/             # Slack bot (Bolt)
│   ├── api-gateway/           # REST API, webhooks, schedulers
│   ├── dashboard/             # React admin dashboard + WhatsApp API
│   └── test-utils/            # Test factories, mocks
├── src/                       # DEPRECATED - Do not write new code here
├── apps/                      # Standalone mini-apps (e.g., meeting-scheduler)
├── data/                      # Seeds, migrations
├── docker/                    # Docker configs and compose files
├── tests/                     # Cross-package tests (e2e, integration)
├── skills/                    # Global skill definitions
└── pnpm-workspace.yaml
```

## Package Descriptions

| Package                     | Status        | Description                                                                |
| --------------------------- | ------------- | -------------------------------------------------------------------------- |
| `@orient/core`              | ✅ Stable     | Config loading, logging (`winston`), base types                            |
| `@orient/database`          | ✅ Stable     | Drizzle ORM schemas, SQLite client                                         |
| `@orient/database-services` | ✅ Stable     | `MessageDatabase`, `SlackDatabase`, `SchedulerDatabase`, `WebhookDatabase` |
| `@orient/agents`            | ✅ Stable     | Agent registry, skills service, prompts, tool permissions                  |
| `@orient/apps`              | ✅ Stable     | Mini-apps manifests, types, validation, edit sessions                      |
| `@orient/mcp-servers`       | 🚧 Types Only | MCP server type definitions (impl in `src/mcp-servers/`)                   |
| `@orient/mcp-tools`         | ✅ Stable     | MCP tool registry & definitions                                            |
| `@orient/integrations`      | ✅ Stable     | GitHub, Google (Sheets, Slides, Gmail, Calendar), Linear, Gemini           |
| `@orient/bot-whatsapp`      | ✅ Stable     | WhatsApp bot using Baileys (integrated into Dashboard)                     |
| `@orient/bot-slack`         | ✅ Stable     | Slack bot using Bolt                                                       |
| `@orient/api-gateway`       | ✅ Stable     | REST API, webhooks                                                         |
| `@orient/dashboard`         | ✅ Stable     | Admin dashboard (React + Express) + WhatsApp API routes                    |
| `@orient/test-utils`        | ✅ Stable     | Test factories, mocks, DB helpers                                          |

## Multi-MCP-Server Architecture

Orient implements three specialized MCP servers, replacing the legacy monolithic server:

| Server               | Purpose              | Key Tools                                                    |
| -------------------- | -------------------- | ------------------------------------------------------------ |
| **coding-server**    | Development tasks    | `ai_first_slides_*`, `ai_first_create_app`, Agent tools      |
| **assistant-server** | Full PM capabilities | Slack/WhatsApp, Google (Calendar, Gmail), Sheets             |
| **core-server**      | System & skills      | `ai_first_list_skills`, `ai_first_health_check`, Agent tools |

All servers share the `discover_tools` tool for dynamic capability discovery.

**CLI Usage:**

```bash
# Start specific server
npm run start:mcp:coding
npm run start:mcp:assistant
npm run start:mcp:core
```

## Agent Registry

Agents are managed via the **Dashboard UI** and stored in SQLite. The `@orientbot/agents` package provides the runtime.

```
┌─────────────────────────────────────────┐
│           Dashboard UI                  │
│   (Agents Tab - CRUD operations)        │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│         Agent Registry                  │
│  - Context resolution (platform, chat)  │
│  - Skills assignment                    │
│  - Tool allow/ask/deny patterns         │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│          SQLite Tables                  │
│   agents | agent_skills | agent_tools   │
│   context_rules                         │
└─────────────────────────────────────────┘
```

### Default Agents

| Agent          | Description                                       |
| -------------- | ------------------------------------------------- |
| `pm-assistant` | Primary agent for meetings and project management |
| `communicator` | Slack/WhatsApp messaging with proper formatting   |
| `scheduler`    | Calendar management, reminders                    |
| `explorer`     | Fast codebase exploration, documentation lookup   |
| `app-builder`  | Create Mini-Apps via PR workflow                  |
| `onboarder`    | Guides new users through setup                    |

### Agent Mentions

In Slack or WhatsApp, prefix message with `@agent-id` to override default agent:

```
@explorer find the auth config
```

## Mini-Apps System (`@orientbot/apps`)

Allows generating small React apps via AI prompts, managed through Git worktrees.

**Key Tools:**

- `ai_first_create_app` - Generate a new app from a prompt
- `ai_first_list_apps` - List existing apps
- `ai_first_get_app` - Get app details
- `ai_first_update_app` - Update an existing app
- `ai_first_share_app` - Generate a shareable link

**Edit Session Flow:**

1. Create Git worktree for isolated development
2. Scaffold app or load existing
3. Create OpenCode session
4. Send prompt to AI for code generation
5. Auto-commit changes
6. Build app (`npm install && npm run build`)
7. Track commit history for rollback

> **Note**: This feature is under active development. See `TODO.md`.

## Data Flow (Incoming Message)

```
1. Message received (WhatsApp/Slack)
        │
        ├── Check permission (read_only, read_write, ignored)
        │   └── ignored: Drop message
        │   └── read_only: Store message, don't respond
        │   └── read_write: Store message, process
        │
        ▼
2. Resolve Agent (AgentRegistry → context rules → default)
        │
        ▼
3. Send to OpenCode server (MCP) for AI processing
        │
        ▼
4. OpenCode uses MCP tools (Atlassian, Slides, etc.)
        │
        ▼
5. Return response to user
        │
        ▼
6. Store outgoing message in SQLite
```

## Docker Deployment

Uses per-package Dockerfiles with multi-stage builds.

```bash
# Local Development (v2 compose)
docker compose -f docker/docker-compose.v2.yml -f docker/docker-compose.local.yml up -d

# Production
USE_V2_COMPOSE=1 ./deploy-server.sh deploy
# Or manually:
docker compose -f docker/docker-compose.v2.yml \
  -f docker/docker-compose.prod.yml \
  -f docker/docker-compose.r2.yml up -d
```

## Key CLI Commands

```bash
# Development
npm run dev:slack           # Run Slack bot in dev mode
npm run dev:whatsapp        # Run WhatsApp bot in dev mode
npm run dev:mcp             # Run coding MCP server in dev mode
npm run dev:infra           # Start Docker infrastructure (MinIO, Nginx)

# Database
pnpm --filter @orientbot/database run db:push:sqlite  # Push schema
pnpm run db:seed:all        # Seed all data
pnpm run agents:seed        # Seed default agents

# Testing
npm run test                # Run all tests
npm run test:e2e            # Run E2E tests
npm run test:unit           # Run unit tests only
npm run test:docker:build   # Test Docker builds

# Build
npm run build               # TypeScript compile
npm run build:all           # Build packages + root + dashboard
```

## Architectural Decisions

### When to Create a New Package

**Create a new package when:**

- Functionality is distinct and reusable across the system
- Has its own lifecycle (startup/shutdown)
- Could be published as a standalone npm package

**Extend existing package when:**

- Functionality is tightly coupled to existing code
- Only used in one context

### Adding New Features

1. **New Agent**: Add via Dashboard UI, seed via `data/seeds/agents.ts`
2. **New MCP Tool**: Add to `packages/mcp-tools/` or `src/tools/`
3. **New Integration**: Add to `@orientbot/integrations`
4. **New Bot Platform**: Follow `bot-whatsapp` / `bot-slack` pattern

### Database Schema Patterns

- Use platform-specific tables: `messages` / `slack_messages`
- SQLite for all structured data, Object Storage for media
- Drizzle ORM for type-safe queries
