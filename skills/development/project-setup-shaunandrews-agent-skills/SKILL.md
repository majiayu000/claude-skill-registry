# Project Setup Skill

Use this skill when creating a new project. It establishes a consistent structure across all projects.

## When to Use

- Starting a new project
- User asks to "set up a project" or "create a new project"
- Bootstrapping a workspace for a new initiative

## Project Location

All projects live in: `~/Developer/Projects/{project-name}/`

Use kebab-case for project names (e.g., `site-editor-navigation`, `wp-cowork-plugin`).

## Standard Structure

```
{project-name}/
├── .git/                 # Initialized git repo
├── .gitignore            # Standard ignores (see below)
├── README.md             # Project overview, quick start
├── CLAUDE.md             # Guidance for Claude Code / AI agents
├── docs/                 # Documentation
│   └── (project docs)
└── logs/                 # Session logs, dev notes (git-ignored)
    └── (daily logs)
```

## File Templates

### README.md

```markdown
# {Project Name}

{One-line description}

## Overview

{Brief explanation of what this project does and why it exists}

## Quick Start

```bash
cd ~/Developer/Projects/{project-name}
# Add setup commands here
```

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/](docs/) | Project documentation |

## Structure

```
{project-name}/
├── docs/          # Documentation
├── logs/          # Development logs (git-ignored)
└── README.md      # This file
```

## Related

- {Links to related issues, PRs, projects}
```

### CLAUDE.md

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

{One-line description of what this project is and its goal}

## Development

```bash
# Add common commands here
```

## Architecture

{Brief description of tech stack, key patterns, important files}

## Documentation

The `/docs/` folder contains:
- {List key docs}

## Scope

- **In scope**: {What this project covers}
- **Out of scope**: {What it doesn't cover}
```

### .gitignore

```gitignore
# Logs - development session logs, not for version control
logs/

# Dependencies
node_modules/
vendor/
.venv/
__pycache__/

# Build outputs
dist/
build/
*.egg-info/

# Environment
.env
.env.local
.env*.local

# IDE / Editor
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Package manager locks (uncomment if not needed)
# package-lock.json
# pnpm-lock.yaml
# composer.lock
```

## Setup Procedure

1. **Create project directory**
   ```bash
   mkdir -p ~/Developer/Projects/{project-name}
   cd ~/Developer/Projects/{project-name}
   ```

2. **Create folder structure**
   ```bash
   mkdir -p docs logs
   ```

3. **Create .gitignore** (use template above)

4. **Create README.md** (use template above, fill in project details)

5. **Create CLAUDE.md** (use template above, fill in project details)

6. **Initialize git**
   ```bash
   git init
   git add -A
   git commit -m "Initial project setup"
   ```

7. **Report to user**
   - Confirm project location
   - List created files
   - Suggest next steps (e.g., "Ready for docs, or should I scaffold something specific?")

## Optional Additions

Depending on project type, may also create:

- **package.json** — For Node.js projects
- **requirements.txt** — For Python projects
- **composer.json** — For PHP projects
- **Makefile** — For projects with build steps
- **docker-compose.yml** — For containerized projects

Ask the user if they want any of these, or infer from context.

## Logs Convention

The `logs/` folder is for development session notes:
- Format: `YYYY-MM-DD-{topic}.md` or `YYYY-MM-DD-HHMM.md`
- Git-ignored so they don't clutter history
- Useful for tracking decisions, debugging sessions, progress

## After Setup

Once project is created:
1. Update Moneypenny (`~/Developer/Projects/moneypenny/projects.json`) if it's a tracked project
2. Add to memory if significant
3. Proceed with project-specific work
