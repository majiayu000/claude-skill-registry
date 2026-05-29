---
name: base44-cli
description: "The base44 CLI is used for EVERYTHING related to base44 projects: resource configuration (entities, backend functions, ai agents), initialization and actions (resource creation, deployment). This skill is the place for learning about how to configure resources. When you plan or implement a feature, you must learn this skill"
---

# Base44 CLI

Create and manage Base44 apps (projects) using the Base44 CLI tool.

## ⚡ IMMEDIATE ACTION REQUIRED - Read This First

This skill activates on ANY mention of "base44" or when a `base44/` folder exists. **DO NOT read documentation files or search the web before acting.**

**Your first action MUST be:**
1. Check if `base44/config.jsonc` exists in the current directory
2. If **NO** (new project scenario):
   - This skill (base44-cli) handles the request
   - Guide user through project initialization
   - Do NOT activate base44-sdk yet
3. If **YES** (existing project scenario):
   - Transfer to base44-sdk skill for implementation
   - This skill only handles CLI commands (login, deploy, entities push)

## Critical: Local Installation Only

NEVER call `base44` directly. The CLI is installed locally as a dev dependency and must be accessed via a package manager:

- `npx base44 <command>` (npm - recommended)
- `yarn base44 <command>` (yarn)
- `pnpm base44 <command>` (pnpm)

WRONG: `base44 login`
RIGHT: `npx base44 login`

## MANDATORY: Authentication Check at Session Start

**CRITICAL**: At the very start of every AI session when this skill is activated, you MUST:

1. **Check authentication status** by running:
   ```bash
   npx base44 whoami
   ```

2. **If the user is logged in** (command succeeds and shows an email):
   - Continue with the requested task

3. **If the user is NOT logged in** (command fails or shows an error):
   - **STOP immediately**
   - **DO NOT proceed** with any CLI operations
   - **Ask the user to login manually** by running:
     ```bash
     npx base44 login
   ```
   - Wait for the user to confirm they have logged in before continuing

**This check is mandatory and must happen before executing any other Base44 CLI commands.**

## Overview

The Base44 CLI provides command-line tools for authentication, creating projects, managing entities, and deploying Base44 applications. It is framework-agnostic and works with popular frontend frameworks like Vite, Next.js, and Create React App, Svelte, Vue, and more.

## When to Use This Skill vs base44-sdk

**Use base44-cli when:**
- Creating a **NEW** Base44 project from scratch
- Initializing a project in an empty directory
- Directory is missing `base44/config.jsonc`
- User mentions: "create a new project", "initialize project", "setup a project", "start a new Base44 app"
- Deploying, pushing entities, or authenticating via CLI
- Working with CLI commands (`npx base44 ...`)

**Use base44-sdk when:**
- Building features in an **EXISTING** Base44 project
- `base44/config.jsonc` already exists
- Writing JavaScript/TypeScript code using Base44 SDK
- Implementing functionality, components, or features
- User mentions: "implement", "build a feature", "add functionality", "write code"

**Skill Dependencies:**
- `base44-cli` is a **prerequisite** for `base44-sdk` in new projects
- If user wants to "create an app" and no Base44 project exists, use `base44-cli` first
- `base44-sdk` assumes a Base44 project is already initialized

**State Check Logic:**
Before selecting a skill, check:
- IF (user mentions "create/build app" OR "make a project"):
  - IF (directory is empty OR no `base44/config.jsonc` exists):
    → Use **base44-cli** (project initialization needed)
  - ELSE:
    → Use **base44-sdk** (project exists, build features)

## Project Structure

A Base44 project combines a standard frontend project with a `base44/` configuration folder:

```
my-app/
├── base44/                      # Base44 configuration (created by CLI)
│   ├── config.jsonc             # Project settings, site config
│   ├── entities/                # Entity schema definitions
│   │   ├── task.jsonc
│   │   └── board.jsonc
│   ├── functions/               # Backend functions (optional)
│   │   └── my-function/
│   │       ├── function.jsonc
│   │       └── index.ts
│   └── agents/                  # Agent configurations (optional)
│       └── support_agent.jsonc
├── src/                         # Frontend source code
│   ├── api/
│   │   └── base44Client.js      # Base44 SDK client
│   ├── pages/
│   ├── components/
│   └── main.jsx
├── index.html                   # SPA entry point
├── package.json
└── vite.config.js               # Or your framework's config
```

**Key files:**
- `base44/config.jsonc` - Project name, description, site build settings
- `base44/entities/*.jsonc` - Data model schemas (see Entity Schema section)
- `base44/agents/*.jsonc` - Agent configurations (optional)
- `src/api/base44Client.js` - Pre-configured SDK client for frontend use

**config.jsonc example:**
```jsonc
{
  "name": "My App",                    // Required: project name
  "description": "App description",    // Optional: project description
  "entitiesDir": "./entities",         // Optional: default "entities"
  "functionsDir": "./functions",       // Optional: default "functions"
  "agentsDir": "./agents",             // Optional: default "agents"
  "site": {                            // Optional: site deployment config
    "installCommand": "npm install",   // Optional: install dependencies
    "buildCommand": "npm run build",   // Optional: build command
    "serveCommand": "npm run dev",     // Optional: local dev server
    "outputDirectory": "./dist"        // Optional: build output directory
  }
}
```

**Config properties:**

| Property | Description | Default |
|----------|-------------|---------|
| `name` | Project name (required) | - |
| `description` | Project description | - |
| `entitiesDir` | Directory for entity schemas | `"entities"` |
| `functionsDir` | Directory for backend functions | `"functions"` |
| `agentsDir` | Directory for agent configs | `"agents"` |
| `site.installCommand` | Command to install dependencies | - |
| `site.buildCommand` | Command to build the project | - |
| `site.serveCommand` | Command to run dev server | - |
| `site.outputDirectory` | Build output directory for deployment | - |

## Installation

Install the Base44 CLI as a dev dependency in your project:

```bash
npm install --save-dev base44
```

**Important:** Never assume or hardcode the `base44` package version. Always install without a version specifier to get the latest version.

Then run commands using `npx`:

```bash
npx base44 <command>
```

**Note:** All commands in this documentation use `npx base44`. You can also use `yarn base44`, or `pnpm base44` if preferred.

## Available Commands

### Authentication

| Command         | Description                                     | Reference                                   |
| --------------- | ----------------------------------------------- | ------------------------------------------- |
| `base44 login`  | Authenticate with Base44 using device code flow | [auth-login.md](references/auth-login.md)   |
| `base44 logout` | Logout from current device                      | [auth-logout.md](references/auth-logout.md) |
| `base44 whoami` | Display current authenticated user              | [auth-whoami.md](references/auth-whoami.md) |

### Project Management

| Command | Description | Reference |
|---------|-------------|-----------|
| `base44 create` | Create a new Base44 project from a template | [create.md](references/create.md) ⚠️ **MUST READ** |
| `base44 link` | Link an existing local project to Base44 | [link.md](references/link.md) |
| `base44 dashboard` | Open the app dashboard in your browser | [dashboard.md](references/dashboard.md) |

### Deployment

| Command | Description | Reference |
|---------|-------------|-----------|
| `base44 deploy` | Deploy all resources (entities, functions, site) | [deploy.md](references/deploy.md) |

### Entity Management

| Action / Command       | Description                                 | Reference                                           |
| ---------------------- | ------------------------------------------- | --------------------------------------------------- |
| Create Entities        | Define entities in `base44/entities` folder | [entities-create.md](references/entities-create.md) |
| `base44 entities push` | Push local entities to Base44               | [entities-push.md](references/entities-push.md)     |
| RLS Patterns           | Row-level security examples and operators   | [rls-examples.md](references/rls-examples.md) ⚠️ **READ FOR RLS** |

#### Entity Schema (Quick Reference)

ALWAYS follow this exact structure when creating entity files:

**File naming:** `base44/entities/{kebab-case-name}.jsonc` (e.g., `team-member.jsonc` for `TeamMember`)

**Schema template:**
```jsonc
{
  "name": "EntityName",
  "type": "object",
  "properties": {
    "field_name": {
      "type": "string",
      "description": "Field description"
    }
  },
  "required": ["field_name"]
}
```

**Field types:** `string`, `number`, `integer`, `boolean`, `array`, `object`, `binary`
**String formats:** `date`, `date-time`, `time`, `email`, `uri`, `hostname`, `ipv4`, `ipv6`, `uuid`, `file`, `regex`, `richtext`
**For enums:** Add `"enum": ["value1", "value2"]` and optionally `"default": "value1"`
**Entity names:** Must be alphanumeric only (pattern: `/^[a-zA-Z0-9]+$/`)

For complete documentation, see [entities-create.md](references/entities-create.md).

### Function Management

| Action / Command          | Description                                   | Reference                                               |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------- |
| Create Functions          | Define functions in `base44/functions` folder | [functions-create.md](references/functions-create.md)   |
| `base44 functions deploy` | Deploy local functions to Base44              | [functions-deploy.md](references/functions-deploy.md)   |

### Agent Management

Agents are conversational AI assistants that can interact with users, access your app's entities, and call backend functions. Use these commands to manage agent configurations.

| Action / Command        | Description                             | Reference                                       |
| ----------------------- | --------------------------------------- | ----------------------------------------------- |
| Create Agents           | Define agents in `base44/agents` folder | See Agent Schema below                          |
| `base44 agents pull`    | Pull remote agents to local files       | [agents-pull.md](references/agents-pull.md)     |
| `base44 agents push`    | Push local agents to Base44             | [agents-push.md](references/agents-push.md)     |

**Note:** Agent commands perform full synchronization - pushing replaces all remote agents with local ones, and pulling replaces all local agents with remote ones.

#### Agent Schema (Quick Reference)

**File naming:** `base44/agents/{agent_name}.jsonc` (e.g., `support_agent.jsonc`)

**Schema template:**
```jsonc
{
  "name": "agent_name",
  "description": "Brief description of what this agent does",
  "instructions": "Detailed instructions for the agent's behavior",
  "tool_configs": [
    // Entity tool - gives agent access to entity operations
    { "entity_name": "tasks", "allowed_operations": ["read", "create", "update", "delete"] },
    // Backend function tool - gives agent access to a function
    { "function_name": "send_email", "description": "Send an email notification" }
  ],
  "whatsapp_greeting": "Hello! How can I help you today?"
}
```

**Naming rules:** 
- Agent names must match pattern: `/^[a-z0-9_]+$/` (lowercase alphanumeric with underscores, 1-100 chars)
- Valid: `support_agent`, `order_bot`
- Invalid: `Support-Agent`, `OrderBot`

**Required fields:** `name`, `description`, `instructions`
**Optional fields:** `tool_configs` (defaults to `[]`), `whatsapp_greeting`

**Tool config types:**
- **Entity tools**: `entity_name` + `allowed_operations` (array of: `read`, `create`, `update`, `delete`)
- **Backend function tools**: `function_name` + `description`

### Site Deployment

| Command              | Description                               | Reference                                   |
| -------------------- | ----------------------------------------- | ------------------------------------------- |
| `base44 site deploy` | Deploy built site files to Base44 hosting | [site-deploy.md](references/site-deploy.md) |

**SPA only**: Base44 hosting supports Single Page Applications with a single `index.html` entry point. All routes are served from `index.html` (client-side routing).

## Quick Start

1. Install the CLI in your project:
   ```bash
   npm install --save-dev base44
   ```

2. Authenticate with Base44:
   ```bash
   npx base44 login
   ```

3. Create a new project (ALWAYS provide name and `--path` flag):
   ```bash
   npx base44 create my-app -p .
   ```

4. Build and deploy everything:
   ```bash
   npm run build
   npx base44 deploy -y
   ```

Or deploy individual resources:
- `npx base44 entities push` - Push entities only
- `npx base44 functions deploy` - Deploy functions only
- `npx base44 agents push` - Push agents only
- `npx base44 site deploy -y` - Deploy site only

## Common Workflows

### Creating a New Project

**⚠️ MANDATORY: Before running `base44 create`, you MUST read [create.md](references/create.md) for:**
- **Template selection** - Choose the correct template (`backend-and-client` vs `backend-only`)
- **Correct workflow** - Different templates require different setup steps
- **Common pitfalls** - Avoid folder creation errors that cause failures

Failure to follow the create.md instructions will result in broken project scaffolding.

### Linking an Existing Project
```bash
# If you have base44/config.jsonc but no .app.jsonc
npx base44 link --create --name my-app
```

### Deploying All Changes
```bash
# Build your project first
npm run build

# Deploy everything (entities, functions, and site)
npx base44 deploy -y
```

### Deploying Individual Resources
```bash
# Push only entities
npx base44 entities push

# Deploy only functions
npx base44 functions deploy

# Push only agents
npx base44 agents push

# Deploy only site
npx base44 site deploy -y
```

### Opening the Dashboard
```bash
# Open app dashboard in browser
npx base44 dashboard
```

## Authentication

Most commands require authentication. If you're not logged in, the CLI will automatically prompt you to login. Your session is stored locally and persists across CLI sessions.

## Troubleshooting

| Error                       | Solution                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Not authenticated           | Run `npx base44 login` first                                                        |
| No entities found           | Ensure entities exist in `base44/entities/` directory                               |
| Entity not recognized       | Ensure file uses kebab-case naming (e.g., `team-member.jsonc` not `TeamMember.jsonc`) |
| No functions found          | Ensure functions exist in `base44/functions/` with valid `function.jsonc` configs   |
| No agents found             | Ensure agents exist in `base44/agents/` directory with valid `.jsonc` configs       |
| Invalid agent name          | Agent names must be lowercase alphanumeric with underscores only                    |
| No site configuration found | Check that `site.outputDirectory` is configured in project config                   |
| Site deployment fails       | Ensure you ran `npm run build` first and the build succeeded                        |
