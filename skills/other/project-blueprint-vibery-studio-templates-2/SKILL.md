---
name: project-blueprint
description: >
  Generate complete project setup recipes combining Vibery templates, MCPs, and configurations.
  Outputs: Install commands, CLAUDE.md, folder structure, workflow setup.
  Use when starting new projects or adding major features to existing ones.
  Triggers: start new project, setup project, project blueprint, /blueprint
---

# Project Blueprint

Generate production-ready project configurations by orchestrating Vibery ecosystem components.

## Purpose

Instead of manually researching which agents, skills, MCPs, and commands to install, this skill analyzes project requirements and outputs a complete setup recipe.

## Available Components

### Vibery Ecosystem (auto-updated)

```
RUN: npx vibery list
TO: Get current available templates

Categories:
- 🤖 Agents: Tech-specific experts (nextjs-developer, stripe-pro, etc.)
- ⚡ Commands: One-shot tasks (create-pr, generate-tests, etc.)
- 🔌 MCPs: External integrations (supabase, github, shopify, etc.)
- 🪝 Hooks: Automation triggers (auto-commit, lint-on-save, etc.)
- ⚙️ Settings: Permission presets (allow-npm, deny-sensitive-files, etc.)
- 🎨 Skills: Complex workflows (frontend-design, mcp-builder, etc.)
```

---

## Process

### Phase 1: Project Classification

#### Entry Check

```
IF user provided: project type + tech stack + scale
    → Proceed to Phase 2
ELSE
    → Classify project first
```

#### Classification Questions

| Question                | Options                                                                        | Why                       |
| ----------------------- | ------------------------------------------------------------------------------ | ------------------------- |
| "What type of project?" | SaaS, E-commerce, API, CLI, Mobile, Landing Page, Chrome Extension, MCP Server | Determines base blueprint |
| "Primary tech stack?"   | [Detect from context or ask]                                                   | Matches agents/skills     |
| "Solo or team?"         | Solo, Small team (2-5), Large team (5+)                                        | Affects workflow setup    |
| "Deploy where?"         | Vercel, Cloudflare, AWS, Railway, Self-hosted                                  | Adds deployment hooks     |

#### Project Type → Base Blueprint Mapping

```
SaaS MVP:
    → nextjs-developer + supabase + stripe-pro
    → Commands: create-pr, generate-tests, security-audit
    → Skills: frontend-design, backend-development

E-commerce:
    → nextjs-developer + shopify OR woocommerce
    → Commands: performance-audit, security-audit
    → Skills: frontend-design

API Service:
    → backend-architect + swagger + postgres-pro
    → Commands: generate-api-documentation, security-audit
    → MCPs: postgresql, redis

CLI Tool:
    → cli-developer + typescript-pro
    → Commands: generate-tests, prepare-release
    → Hooks: conventional-commits

Landing Page:
    → frontend-design + tailwind-pro
    → Commands: performance-audit
    → Hooks: format-on-save

Chrome Extension:
    → typescript-pro + chrome-devtools
    → Skills: frontend-design

MCP Server:
    → mcp-builder + typescript-pro
    → Commands: generate-tests
    → Skills: mcp-management
```

---

### Phase 2: Stack Analysis

#### Entry Check

```
IF project classified:
    → Analyze tech stack requirements
ELSE
    → Return to Phase 1
```

#### Stack Detection

```
IF existing project:
    → Read package.json, requirements.txt, go.mod, Cargo.toml
    → Identify: framework, language, dependencies
    → Suggest components matching existing stack

IF new project:
    → Use classification from Phase 1
    → Recommend optimal stack for project type
```

#### Component Selection Rules

```
FOR each technology in stack:
    → Search: npx vibery search [technology]
    → Select: Most specific agent/skill available
    → Avoid: Generic alternatives if specific exists

Example:
    Next.js project → nextjs-developer (not react-specialist)
    Supabase auth → supabase MCP (not generic postgres)
```

---

### Phase 3: Blueprint Generation

#### Entry Check

```
IF stack analyzed + components selected:
    → Generate blueprint
ELSE
    → Return to Phase 2
```

#### Blueprint Structure

````markdown
# Project Blueprint: [Project Name]

## Quick Start

```bash
# 1. Install Vibery templates
npx vibery install [agent-1]
npx vibery install [agent-2]
npx vibery install [mcp-1]
npx vibery install [command-1]
npx vibery install [hook-1]

# 2. Configure MCP servers (if any)
# [MCP-specific setup commands]

# 3. Verify installation
npx vibery list --installed
```
````

## Components Installed

### Agents

| Agent        | Purpose        | When Used         |
| ------------ | -------------- | ----------------- |
| [agent-name] | [what it does] | [trigger context] |

### MCPs

| MCP        | Purpose               | Setup Required   |
| ---------- | --------------------- | ---------------- |
| [mcp-name] | [what it connects to] | [env vars, auth] |

### Commands

| Command    | Purpose        | Usage         |
| ---------- | -------------- | ------------- |
| /[command] | [what it does] | [when to run] |

### Hooks

| Hook        | Trigger      | Action         |
| ----------- | ------------ | -------------- |
| [hook-name] | [when fires] | [what happens] |

## CLAUDE.md

[Generate project-specific CLAUDE.md - see Phase 4]

## Folder Structure

[Generate recommended structure - see Phase 4]

## Workflows

[Generate common workflows - see Phase 4]

```

---

### Phase 4: Configuration Generation

#### CLAUDE.md Generation
```

BASED ON project type + stack:
→ Generate CLAUDE.md with:

    # Project Context
    - Tech stack summary
    - Architecture overview
    - Key directories

    # Conventions
    - Coding standards for this stack
    - Naming conventions
    - File organization rules

    # Commands
    - Dev, test, build, deploy commands

    # Agent Instructions
    - When to use which installed agent
    - MCP usage patterns

```

#### Folder Structure Generation
```

BASED ON project type:
→ Generate tree structure with:

    - Source code organization
    - Test file locations
    - Config file placements
    - Documentation structure

    Match conventions of chosen framework

```

#### Workflow Generation
```

GENERATE common workflows:

1. Feature Development:
   - Branch naming
   - Which agents to use
   - PR creation with /create-pr

2. Testing:
   - /generate-tests for new features
   - Test organization

3. Deployment:
   - Pre-deploy checks
   - Deploy commands
   - Post-deploy verification

````

---

### Phase 5: Output Delivery

#### Output Format
```markdown
# [Project Name] Blueprint

## Installation (copy-paste ready)
[bash commands]

## Configuration Files

### CLAUDE.md
```markdown
[generated CLAUDE.md content]
````

### .claude/settings.json (if needed)

```json
[settings content]
```

## Project Structure

```
[folder tree]
```

## Development Workflow

[step by step workflow]

## Next Steps

1. Run installation commands
2. Copy CLAUDE.md to project root
3. Create folder structure
4. Start with: [first recommended action]

```

---

## Self-Check (Read before every response)

□ Did I check current Vibery availability?
  → Templates change; verify before recommending

□ Are install commands copy-paste ready?
  → User should not need to modify commands

□ Is CLAUDE.md specific to this project?
  → Generic CLAUDE.md = wasted context

□ Did I include MCP setup instructions?
  → MCPs often need env vars, auth tokens

□ Are workflows actionable?
  → "Use good practices" is not a workflow
  → "Run /create-pr after feature complete" is

□ Did I explain WHY each component?
  → User should understand the choices

---

## Blueprint Templates Reference

See `references/blueprints/` for complete examples:
- `saas-nextjs-supabase.md`
- `api-fastapi-postgres.md`
- `cli-typescript.md`
- `landing-astro.md`
- `extension-chrome.md`
- `mcp-server.md`
```
