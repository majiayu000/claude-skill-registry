---
name: agent-selection
description: Single source of truth for MetaSaver agent selection and subagent_type mapping
---

# Agent Selection Skill

Complete reference for selecting the correct MetaSaver agents and their `subagent_type` values.

## Core Principle

**When MetaSaver plugin is active, ALWAYS use MetaSaver agents over core Claude Code agents.**

## Core Agent Replacement

**In MetaSaver repos, prefer MetaSaver agents over core Claude Code agents:**

| Core Agent        | Use Instead     | Why                            | subagent_type                              |
| ----------------- | --------------- | ------------------------------ | ------------------------------------------ |
| `Explore`         | `code-explorer` | Uses Serena, repomix, memories | `core-claude-plugin:generic:code-explorer` |
| `Plan`            | `architect`     | Knows MetaSaver patterns       | `core-claude-plugin:generic:architect`     |
| `general-purpose` | Task-specific   | Specialized knowledge          | See tables below                           |

**In MetaSaver repos:**

- `Explore` → use `core-claude-plugin:generic:code-explorer`
- `Plan` → use `core-claude-plugin:generic:architect`
- `general-purpose` → use task-specific MetaSaver agent

---

## Analysis Agents (1)

**Minimal-tool agents** for prompt classification. These specify `tools: TodoWrite` to avoid inheriting MCP tools (~37k tokens each). Results are returned inline in the Task response.

| Task Type            | Agent Name        | subagent_type                                  |
| -------------------- | ----------------- | ---------------------------------------------- |
| Scope identification | scope-check-agent | `core-claude-plugin:generic:scope-check-agent` |

**Used by:** analysis-phase skill (first phase of /ms, /audit, /build commands)

---

## Generic Agents (15)

High-level workers for orchestration, implementation, and quality.

| Task Type                | Agent Name             | subagent_type                                       |
| ------------------------ | ---------------------- | --------------------------------------------------- |
| Codebase exploration     | code-explorer          | `core-claude-plugin:generic:code-explorer`          |
| Agent/skill authoring    | agent-author           | `core-claude-plugin:generic:agent-author`           |
| Architecture decisions   | architect              | `core-claude-plugin:generic:architect`              |
| Requirements analysis    | business-analyst       | `core-claude-plugin:generic:business-analyst`       |
| Code implementation      | coder                  | `core-claude-plugin:generic:coder`                  |
| Backend development      | backend-dev            | `core-claude-plugin:generic:backend-dev`            |
| Testing                  | tester                 | `core-claude-plugin:generic:tester`                 |
| Code review              | reviewer               | `core-claude-plugin:generic:reviewer`               |
| Multi-agent coordination | project-manager        | `core-claude-plugin:generic:project-manager`        |
| Quality validation       | code-quality-validator | `core-claude-plugin:generic:code-quality-validator` |
| Debugging/investigation  | root-cause-analyst     | `core-claude-plugin:generic:root-cause-analyst`     |
| Security analysis        | security-engineer      | `core-claude-plugin:generic:security-engineer`      |
| Performance optimization | performance-engineer   | `core-claude-plugin:generic:performance-engineer`   |
| DevOps/infrastructure    | devops                 | `core-claude-plugin:generic:devops`                 |
| Azure DevOps             | azure-devops-agent     | `core-claude-plugin:generic:azure-devops-agent`     |

---

## Domain Agents (12)

Specialized agents for specific technical domains.

### Backend (2)

| Domain              | Agent Name                | subagent_type                                                 |
| ------------------- | ------------------------- | ------------------------------------------------------------- |
| Data Service API    | data-service-agent        | `core-claude-plugin:domain:backend:data-service-agent`        |
| Integration Service | integration-service-agent | `core-claude-plugin:domain:backend:integration-service-agent` |

### Database (1)

| Domain          | Agent Name            | subagent_type                                              |
| --------------- | --------------------- | ---------------------------------------------------------- |
| Prisma Database | prisma-database-agent | `core-claude-plugin:domain:database:prisma-database-agent` |

### Frontend (5)

| Domain                | Agent Name             | subagent_type                                               |
| --------------------- | ---------------------- | ----------------------------------------------------------- |
| React App Scaffolding | react-app-agent        | `core-claude-plugin:domain:frontend:react-app-agent`        |
| React Components      | react-component-agent  | `core-claude-plugin:domain:frontend:react-component-agent`  |
| MFE Host              | mfe-host-agent         | `core-claude-plugin:domain:frontend:mfe-host-agent`         |
| MFE Remote            | mfe-remote-agent       | `core-claude-plugin:domain:frontend:mfe-remote-agent`       |
| shadcn Components     | shadcn-component-agent | `core-claude-plugin:domain:frontend:shadcn-component-agent` |

### Testing (3)

| Domain            | Agent Name             | subagent_type                                              |
| ----------------- | ---------------------- | ---------------------------------------------------------- |
| Unit Tests        | unit-test-agent        | `core-claude-plugin:domain:testing:unit-test-agent`        |
| Integration Tests | integration-test-agent | `core-claude-plugin:domain:testing:integration-test-agent` |
| E2E Tests         | e2e-test-agent         | `core-claude-plugin:domain:testing:e2e-test-agent`         |

### Monorepo (1)

| Domain         | Agent Name           | subagent_type                                             |
| -------------- | -------------------- | --------------------------------------------------------- |
| Monorepo Setup | monorepo-setup-agent | `core-claude-plugin:domain:monorepo:monorepo-setup-agent` |

---

## Config Agents (28)

Configuration file specialists for auditing and building configs.

### Build Tools (8)

| Config Type    | Agent Name           | subagent_type                                                              |
| -------------- | -------------------- | -------------------------------------------------------------------------- |
| Docker Compose | docker-compose-agent | `core-claude-plugin:config:build-tools:docker-compose-agent`               |
| Dockerignore   | dockerignore-agent   | `core-claude-plugin:config:build-tools:dockerignore-agent`                 |
| pnpm Workspace | pnpm-workspace-agent | `core-claude-plugin:config:build-tools:pnpm-workspace-configuration-agent` |
| PostCSS        | postcss-agent        | `core-claude-plugin:config:build-tools:postcss-agent`                      |
| Tailwind       | tailwind-agent       | `core-claude-plugin:config:build-tools:tailwind-agent`                     |
| Turbo          | turbo-config-agent   | `core-claude-plugin:config:build-tools:turbo-config-agent`                 |
| Vite           | vite-agent           | `core-claude-plugin:config:build-tools:vite-agent`                         |
| Vitest         | vitest-agent         | `core-claude-plugin:config:build-tools:vitest-agent`                       |

### Code Quality (3)

| Config Type  | Agent Name         | subagent_type                                                         |
| ------------ | ------------------ | --------------------------------------------------------------------- |
| EditorConfig | editorconfig-agent | `core-claude-plugin:config:code-quality:editorconfig-agent`           |
| ESLint       | eslint-agent       | `core-claude-plugin:config:code-quality:eslint-agent`                 |
| Prettier     | prettier-agent     | `core-claude-plugin:config:code-quality:prettier-configuration-agent` |

### Version Control (5)

| Config Type     | Agent Name            | subagent_type                                                     |
| --------------- | --------------------- | ----------------------------------------------------------------- |
| Commitlint      | commitlint-agent      | `core-claude-plugin:config:version-control:commitlint-agent`      |
| Gitattributes   | gitattributes-agent   | `core-claude-plugin:config:version-control:gitattributes-agent`   |
| GitHub Workflow | github-workflow-agent | `core-claude-plugin:config:version-control:github-workflow-agent` |
| Gitignore       | gitignore-agent       | `core-claude-plugin:config:version-control:gitignore-agent`       |
| Husky           | husky-agent           | `core-claude-plugin:config:version-control:husky-git-hooks-agent` |

### Workspace (12)

| Config Type             | Agent Name                    | subagent_type                                                        |
| ----------------------- | ----------------------------- | -------------------------------------------------------------------- |
| CLAUDE.md               | claude-md-agent               | `core-claude-plugin:config:workspace:claude-md-configuration-agent`  |
| .env.example            | env-example-agent             | `core-claude-plugin:config:workspace:env-example-agent`              |
| Monorepo Root Structure | monorepo-root-structure-agent | `core-claude-plugin:config:workspace:monorepo-root-structure-agent`  |
| Nodemon                 | nodemon-agent                 | `core-claude-plugin:config:workspace:nodemon-agent`                  |
| .npmrc.template         | npmrc-template-agent          | `core-claude-plugin:config:workspace:npmrc-template-agent`           |
| .nvmrc                  | nvmrc-agent                   | `core-claude-plugin:config:workspace:nvmrc-agent`                    |
| README                  | readme-agent                  | `core-claude-plugin:config:workspace:readme-agent`                   |
| Repomix                 | repomix-config-agent          | `core-claude-plugin:config:workspace:repomix-config-agent`           |
| Root package.json       | root-package-json-agent       | `core-claude-plugin:config:workspace:root-package-json-agent`        |
| Scripts                 | scripts-agent                 | `core-claude-plugin:config:workspace:scripts-agent`                  |
| TypeScript              | typescript-agent              | `core-claude-plugin:config:workspace:typescript-configuration-agent` |
| VS Code                 | vscode-agent                  | `core-claude-plugin:config:workspace:vscode-agent`                   |

---

## Agent Spawning Pattern

Tell agents to READ their own instruction file:

```
[MODE] for [path/scope].
You are [Agent Name].
READ YOUR INSTRUCTIONS at .claude/agents/[category]/[agent-name].md
Follow YOUR rules, invoke YOUR skills, use YOUR output format.
```

**Example:**

```
Task(
  subagent_type: "core-claude-plugin:config:build-tools:eslint-agent",
  prompt: `
    AUDIT MODE for /path/to/eslint.config.js
    You are the ESLint Agent.
    READ YOUR INSTRUCTIONS at .claude/agents/config/code-quality/eslint-agent.md
    Follow YOUR rules, invoke YOUR skill, use YOUR output format.
    Report violations and recommendations.
  `
)
```

Results are returned inline.

---

## Quick Reference by Task

| I need to...          | Use this agent         | subagent_type                                                        |
| --------------------- | ---------------------- | -------------------------------------------------------------------- |
| Explore codebase      | code-explorer          | `core-claude-plugin:generic:code-explorer`                           |
| Design architecture   | architect              | `core-claude-plugin:generic:architect`                               |
| Write code            | coder                  | `core-claude-plugin:generic:coder`                                   |
| Write tests           | tester                 | `core-claude-plugin:generic:tester`                                  |
| Review code           | reviewer               | `core-claude-plugin:generic:reviewer`                                |
| Coordinate agents     | project-manager        | `core-claude-plugin:generic:project-manager`                         |
| Validate quality      | code-quality-validator | `core-claude-plugin:generic:code-quality-validator`                  |
| Debug issues          | root-cause-analyst     | `core-claude-plugin:generic:root-cause-analyst`                      |
| Audit ESLint          | eslint-agent           | `core-claude-plugin:config:code-quality:eslint-agent`                |
| Audit TypeScript      | typescript-agent       | `core-claude-plugin:config:workspace:typescript-configuration-agent` |
| Build React component | react-component-agent  | `core-claude-plugin:domain:frontend:react-component-agent`           |
| Build API service     | data-service-agent     | `core-claude-plugin:domain:backend:data-service-agent`               |
| Setup Prisma          | prisma-database-agent  | `core-claude-plugin:domain:database:prisma-database-agent`           |

---

## Integration

This skill is referenced by:

- `/ms` - MetaSaver intelligent router
- `/audit` - Configuration and code auditing
- `/build` - Feature and component building

All commands should use this skill as the single source of truth for agent selection.
