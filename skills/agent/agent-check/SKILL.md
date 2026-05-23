---
name: agent-check
description: Use when mapping audit targets to appropriate config or domain agents. Analyzes file types, patterns, and content to determine which agents should audit each file/target. Returns agents[] needed for audit workflow.
---

# Agent Check Skill

**Purpose:** Analyze audit targets and map them to the appropriate domain or config agents needed.

**Input:** `targets` (string[]) - File paths or target repositories from scope-check

**Output:** `agents: string[]` - List of agent names needed (e.g., `["eslint-agent", "typescript-agent", "react-component-agent"]`)

---

## How to Execute

This is a FILE CLASSIFICATION task - analyze target files and determine which agents are needed:

1. Scan each target file/directory for file patterns and content indicators
2. Match patterns to agent mapping tables below
3. Collect all matching agents into array
4. Remove duplicates
5. Return ONLY: `agents: [...]`
6. Complete in under 300 tokens

**Expected output format:**

```
agents: ["eslint-agent", "prettier-agent", "typescript-agent"]
```

---

## File Pattern Matching

### Step 1: Detect File Types

Scan target files for these patterns and map to agents:

| File Pattern | Agent | Category |
| ------------ | ----- | -------- |
| `eslint.config.js`, `.eslintrc*`, `eslint.json` | `eslint-agent` | Config |
| `prettier.config.*`, `.prettierrc*`, `.prettierignore` | `prettier-agent` | Config |
| `tsconfig.json`, `tsconfig.*.json` | `typescript-agent` | Config |
| `vitest.config.*`, `vitest.workspace.*` | `vitest-agent` | Config |
| `vite.config.*` | `vite-agent` | Config |
| `turbo.json` | `turbo-config-agent` | Config |
| `tailwind.config.*` | `tailwind-agent` | Config |
| `docker-compose.yml`, `docker-compose.yaml` | `docker-compose-agent` | Config |
| `Dockerfile`, `.dockerignore` | `dockerignore-agent` | Config |
| `.editorconfig` | `editorconfig-agent` | Config |
| `commitlint.config.*` | `commitlint-agent` | Config |
| `.gitignore`, `.gitattributes` | `gitignore-agent`, `gitattributes-agent` | Config |
| `.github/workflows/*.yml`, `.github/workflows/*.yaml` | `github-workflow-agent` | Config |
| `.husky/`, `husky.config.*` | `husky-agent` | Config |
| `nodemon.json`, `nodemon.config.*` | `nodemon-agent` | Config |
| `.npmrc.template`, `.npmrc` | `npmrc-template-agent` | Config |
| `.nvmrc` | `nvmrc-agent` | Config |
| `CLAUDE.md`, `.claude/` | `claude-md-agent` | Config |
| `.repomixignore`, `repomix.json` | `repomix-config-agent` | Config |
| `package.json` (root) | `root-package-json-agent` | Config |
| `README.md` (root) | `readme-agent` | Config |
| `pnpm-workspace.yaml` | `pnpm-workspace-agent` | Config |
| `.vscode/`, `vscode.json` | `vscode-agent` | Config |

---

### Step 2: Detect Code Content

For code files (`.ts`, `.tsx`, `.js`, `.jsx`), scan content patterns:

| Pattern | Agent | Trigger |
| ------- | ----- | ------- |
| React hooks, JSX, `.tsx` files | `react-component-agent` | `useState`, `useEffect`, `JSX`, `export const Component` |
| Service files, API routes | `data-service-agent` | `Service`, `Repository`, `@POST`, `@GET`, `route`, `handler` |
| Prisma schema references | `prisma-database-agent` | `import.*Prisma`, `prisma.`, `schema.prisma` |
| Test files | `unit-test-agent` | `.test.ts`, `.test.js`, `describe`, `it(`, `test(` |
| Integration test patterns | `integration-test-agent` | `integration.test.ts`, `db.test.ts`, `api.test.ts` |
| E2E test patterns | `e2e-test-agent` | `e2e.test.ts`, `cypress`, `playwright`, `browser`, `page.` |

---

### Step 3: Detect Domain Context

Analyze repository structure and content for domain indicators:

| Context | Agent | Detection |
| ------- | ----- | --------- |
| Monorepo workspace setup | `monorepo-setup-agent` | `pnpm-workspace.yaml` presence + multiple packages |
| React app structure | `react-app-agent` | `pages/`, `components/`, `App.tsx`, app router patterns |
| API service setup | `data-service-agent` | `controllers/`, `services/`, `repositories/`, API decorators |
| Database setup | `prisma-database-agent` | `prisma/schema.prisma`, `migrations/` directory |

---

## Agent Mapping Reference

### Config Agents (28 total)

**Build Tools (8):**
- `docker-compose-agent`, `dockerignore-agent`, `pnpm-workspace-agent`
- `postcss-agent`, `tailwind-agent`, `turbo-config-agent`, `vite-agent`, `vitest-agent`

**Code Quality (3):**
- `editorconfig-agent`, `eslint-agent`, `prettier-agent`

**Version Control (5):**
- `commitlint-agent`, `gitattributes-agent`, `github-workflow-agent`
- `gitignore-agent`, `husky-agent`

**Workspace (12):**
- `claude-md-agent`, `env-example-agent`, `monorepo-root-structure-agent`
- `nodemon-agent`, `npmrc-template-agent`, `nvmrc-agent`, `readme-agent`
- `repomix-config-agent`, `root-package-json-agent`, `scripts-agent`
- `typescript-agent`, `vscode-agent`

### Domain Agents (12 total)

**Backend (2):**
- `data-service-agent`, `integration-service-agent`

**Database (1):**
- `prisma-database-agent`

**Frontend (5):**
- `react-app-agent`, `react-component-agent`, `mfe-host-agent`
- `mfe-remote-agent`, `shadcn-component-agent`

**Testing (3):**
- `unit-test-agent`, `integration-test-agent`, `e2e-test-agent`

**Monorepo (1):**
- `monorepo-setup-agent`

---

## Selection Algorithm

```
agents = []

FOR each target file/directory:
    1. Check file patterns (Step 1) -> add matching agents
    2. If code file: check content patterns (Step 2) -> add matching agents
    3. Check domain context (Step 3) -> add matching agents

REMOVE duplicates from agents array
RETURN agents
```

---

## Examples

### Example 1: ESLint Config File

```
Target: /home/user/code/metasaver-com/eslint.config.js

Analysis:
  - File pattern: "eslint.config.js" -> eslint-agent
  - Content: ESLint config -> code-quality context

Output: ["eslint-agent"]
```

### Example 2: React Component Files

```
Target: /home/user/code/metasaver-com/src/components/

Analysis:
  - Files: *.tsx files with JSX/React hooks
  - Content patterns: useState, useEffect, export const Component
  - Domain: React component library

Output: ["react-component-agent", "typescript-agent", "eslint-agent"]
```

### Example 3: Full Package Audit

```
Target: /home/user/code/multi-mono/packages/utils/

Analysis:
  - tsconfig.json -> typescript-agent
  - eslint.config.js -> eslint-agent
  - *.test.ts files -> unit-test-agent
  - package.json -> root-package-json-agent
  - pnpm-workspace.yaml (parent) -> pnpm-workspace-agent

Output: ["typescript-agent", "eslint-agent", "unit-test-agent", "root-package-json-agent", "pnpm-workspace-agent"]
```

### Example 4: Prisma Database Setup

```
Target: /home/user/code/metasaver-com/prisma/

Analysis:
  - schema.prisma -> prisma-database-agent
  - migrations/ directory -> prisma-database-agent
  - Database service files -> data-service-agent

Output: ["prisma-database-agent", "data-service-agent"]
```

### Example 5: Multi-Domain Repository

```
Target: /home/user/code/metasaver-com/ (full repo)

Analysis:
  - Root configs: eslint.config.js, tsconfig.json, prettier.config.js
  - App structure: React components in src/components
  - API routes: src/app/api/
  - Database: prisma/schema.prisma
  - Tests: src/**/*.test.ts

Output: [
  "eslint-agent", "typescript-agent", "prettier-agent",
  "react-component-agent", "data-service-agent",
  "prisma-database-agent", "unit-test-agent"
]
```

---

## Special Cases

| Case | Logic |
| ---- | ----- |
| Root package.json | Always include `root-package-json-agent` (not consumed by workspace agents) |
| Monorepo workspace | Include `pnpm-workspace-agent` for workspace configuration |
| Config-only target | Return only config agents (ESLint, Prettier, TypeScript, etc.) |
| Code-only target | Include code-domain agents + code-quality agents (ESLint, TypeScript) |
| Mixed target | Include ALL matching agents (config + domain) |
| Empty/no matches | Return empty array `[]` |

---

## Integration

This skill is referenced by:

- `agent-check-agent` - Intelligent routing to appropriate agents for audit workflow
- `/audit` command - Phase 2 (agent selection) uses this skill output
- `/build` command - Feature/component building phase uses this skill

The output `agents[]` is used to spawn multiple agents in parallel for comprehensive audit coverage.
