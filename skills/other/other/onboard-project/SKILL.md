---
name: onboard-project
description: Guide onboarding a new project to the Jocko Fuel platform
user-invocable: true
---

You are helping the user onboard a new project to the Jocko Fuel Claude Code platform.

Follow these steps:

### Step 1: Gather Project Info

Ask the user:
- **Project name** — what should the directory be called?
- **Purpose** — what does this project do?
- **Category** — Operations, Marketing, Sales, Finance, Engineering, HR, or Executive?
- **Data sources** — Snowflake, Shopify, external APIs, or none?
- **Agents needed** — how many specialized agents are expected?

### Step 2: Create Directory Structure

Set up the standard project structure at `/Users/gd/Documents/Agents/ClaudeCode/{project-name}/`:

```
{project-name}/
├── CLAUDE.md                    # Claude Code rules (references @AGENTS.md)
├── AGENTS.md                    # Navigation hub
├── .claude/
│   ├── agents/                  # Agent definitions
│   ├── hooks/
│   │   └── hooks.json           # Event hooks
│   └── settings.json            # Permission and status line config
├── docs/                        # Deep documentation
├── scripts/                     # Automation scripts
├── sql/                         # SQL files (if Snowflake)
└── tests/                       # Test files
```

### Step 3: Generate CLAUDE.md

Create a minimal CLAUDE.md that:
- Has an ABOUTME header
- References `@AGENTS.md`
- Inherits rules from `../CLAUDE.md`
- Lists project-specific rules if any

### Step 4: Generate AGENTS.md

Create an AGENTS.md with:
- Purpose section
- Directory structure
- Decision tree for common tasks
- Agent listing (even if empty initially)
- Data sources table
- Build and test commands

### Step 5: Configure Settings

Create `.claude/settings.json` with:
- Status line configuration
- Appropriate permission defaults

### Step 6: Register in Root AGENTS.md

Remind the user to add the project to `/Users/gd/Documents/Agents/ClaudeCode/AGENTS.md` in the appropriate category table.

### Step 7: Initialize Git

If not already a git repo:
- Initialize git
- Create `.gitignore` (exclude `.env`, `.venv/`, `node_modules/`, `*.pyc`)
- Make initial commit

### Step 8: Verify

Run `/jf-platform-tools:project-health` on the new project to confirm it passes all checks.

### Error Handling

- If the directory already exists, ask before overwriting
- If the project name conflicts with an existing project, suggest alternatives
- If the user is unsure about category, suggest based on the project purpose
