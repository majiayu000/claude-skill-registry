---
name: claude-code-starter
description: >
  Intelligent AI-assisted development setup that analyzes a repository's tech stack
  and generates comprehensive .claude/ configuration including CLAUDE.md, skills, agents,
  rules, commands, and settings.json. Use when the user wants to set up Claude Code for
  a project, initialize .claude configuration, bootstrap a new project with Claude,
  generate a CLAUDE.md, or run /claude-code-starter.
---

# Claude Code Starter

Generate a complete `.claude/` configuration for any project by analyzing its tech stack.

## Overview

This skill performs 6 steps:
1. **Detect** the project's tech stack (languages, frameworks, tools)
2. **Check** for existing `.claude/` configuration
3. **Generate** `settings.json` with stack-specific permissions
4. **Generate** skills, agents, rules, and commands from templates
5. **Analyze** the codebase deeply and write `CLAUDE.md`
6. **Summarize** all files created

---

## Step 1: Detect Tech Stack

Analyze the current project root to detect languages, frameworks, and tools.

### Languages

Check for these files and extensions at the project root:

| Language | Detection Files |
|----------|----------------|
| TypeScript | `tsconfig.json`, `tsconfig.base.json`, `typescript` in devDependencies, `.ts`/`.tsx` files |
| JavaScript | `package.json`, `.js`/`.mjs`/`.cjs` files (only if TypeScript not detected) |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `.py` files |
| Go | `go.mod`, `go.sum` |
| Rust | `Cargo.toml`, `Cargo.lock` |
| Ruby | `Gemfile`, `Gemfile.lock` |
| Java | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| Kotlin | `.kt`/`.kts` files |
| C# | `.csproj`/`.sln` files |
| Swift | `Package.swift`, `.swift` files |
| PHP | `composer.json`, `.php` files |
| C/C++ | `.c`/`.cpp`/`.cc`/`.cxx`/`.h`/`.hpp` files |

The first detected language is the **primary language**.

### Frameworks

**JS/TS** (from `package.json` dependencies/devDependencies, order matters — first match wins for frontend):
- Frontend (mutually exclusive, check in order): `next` -> Next.js, `nuxt`/`nuxt3` -> Nuxt, `@sveltejs/kit` -> SvelteKit, `svelte` -> Svelte, `astro` -> Astro, `@remix-run/react` -> Remix, `gatsby` -> Gatsby, `solid-js` -> Solid, `@angular/core` -> Angular, `vue` -> Vue, `react` -> React
- Backend (additive): `@nestjs/core` -> NestJS, `express` -> Express, `fastify` -> Fastify, `hono` -> Hono, `elysia` -> Elysia, `koa` -> Koa
- CSS/UI (additive): `tailwindcss` -> Tailwind, `components.json` file -> shadcn, `@chakra-ui/react` -> Chakra, `@mui/material` -> MUI
- Database/ORM (additive): `prisma`/`@prisma/client` -> Prisma, `drizzle-orm` -> Drizzle, `typeorm` -> TypeORM, `sequelize` -> Sequelize, `mongoose` -> Mongoose

**Python** (from `requirements.txt` or `pyproject.toml`): fastapi, django, flask, starlette, sqlalchemy

**Ruby** (from `Gemfile`): rails, sinatra

**Go** (from `go.mod`): gin-gonic -> Gin, labstack/echo -> Echo, gofiber -> Fiber

**Rust** (from `Cargo.toml`): actix, axum, rocket

**Swift/iOS**: Check `Package.swift` for `vapor`. Check `.xcodeproj`/`.xcworkspace` + Swift files for SwiftUI indicators (`ContentView`, `App.swift`, `@main struct`) and UIKit indicators (`ViewController`, `AppDelegate`, `SceneDelegate`). Scan first 10 Swift files for `import SwiftData`/`@Model` and `import Combine`/`PassthroughSubject`.

**Android/Kotlin** (from `build.gradle`/`build.gradle.kts` including `app/` variants): Check for `com.android`/`android {`, then `compose`/`androidx.compose` -> Jetpack Compose (else Android Views), `room`/`androidx.room` -> Room, `hilt`/`dagger.hilt` -> Hilt, `ktor` -> Ktor. Also check for `spring` -> Spring, `quarkus` -> Quarkus.

### Tools

**Package Manager** (check lock files in order): `bun.lockb`/`bun.lock` -> bun, `pnpm-lock.yaml` -> pnpm, `yarn.lock` -> yarn, `package-lock.json` -> npm, `poetry.lock` -> poetry, `Pipfile.lock`/`requirements.txt` -> pip, `Cargo.lock` -> cargo, `go.sum` -> go, `Gemfile.lock` -> bundler, `pom.xml` -> maven, `build.gradle`/`.kts` -> gradle

**Testing** (from dependencies/config files): vitest, jest, mocha, @playwright/test, cypress, `bun test` in scripts -> bun-test, `pytest.ini`/`conftest.py` -> pytest, `go.mod` -> go-test, `Cargo.toml` -> rust-test, `Gemfile` -> rspec

**Linter** (check config files first, then dependencies): `eslint.config.*`/`.eslintrc*` -> eslint, `biome.json`/`biome.jsonc` -> biome, `ruff.toml`/`.ruff.toml` -> ruff, `.flake8`/`setup.cfg` -> flake8

**Formatter**: `.prettierrc*`/`prettier.config.*` -> prettier, `biome.json`/`biome.jsonc` -> biome, `pyproject.toml` -> black

**Bundler**: `vite.config.*` -> vite, `webpack.config.*` -> webpack, `tsup.config.*` -> tsup, `rollup.config.*` -> rollup, `esbuild*` -> esbuild; from deps: parcel, `@vercel/turbopack` -> turbopack, `@rspack/core` -> rspack

**CI/CD**: `.github/workflows/` dir -> github-actions, `.gitlab-ci.yml` -> gitlab-ci, `.circleci/` dir -> circleci, `.travis.yml` -> travis, `azure-pipelines.yml` -> azure-devops, `Jenkinsfile` -> jenkins

**Docker**: `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`

**Monorepo**: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`, `workspaces` in package.json, `packages/` or `apps/` directories

---

## Step 2: Check Existing Configuration

1. Check if `.claude/` directory exists
2. If it exists, ask the user: **Update** (preserve existing task state) or **Overwrite** (replace all)?
3. If `.claude/state/task.md` exists, **always preserve it** regardless of user choice

---

## Step 3: Generate Settings

Create `.claude/settings.json` using the permission patterns from [settings-patterns.md](references/settings-patterns.md).

1. Start with **base permissions** (always included)
2. Add **language-specific** permissions for each detected language
3. Add **testing framework** permissions
4. Add **linter** and **formatter** permissions
5. Add **Docker** permissions if Docker detected
6. **Deduplicate** the final array

---

## Step 4: Generate Skills, Agents, Rules, Commands

Use the templates from the reference files to generate all applicable files.

### Skills

See [templates-skills.md](references/templates-skills.md) for all skill templates.

**Always generate** (8 core skills):
- `.claude/skills/pattern-discovery.md`
- `.claude/skills/systematic-debugging.md`
- `.claude/skills/testing-methodology.md` (dynamic: uses detected testing framework)
- `.claude/skills/iterative-development.md` (dynamic: uses detected test/lint commands)
- `.claude/skills/commit-hygiene.md`
- `.claude/skills/code-deduplication.md`
- `.claude/skills/simplicity-rules.md`
- `.claude/skills/security.md` (dynamic: JS/TS and Python sections are conditional)

**Conditionally generate** (framework skills):
- `.claude/skills/nextjs-patterns.md` (if Next.js detected)
- `.claude/skills/react-components.md` (if React detected AND Next.js NOT detected)
- `.claude/skills/fastapi-patterns.md` (if FastAPI detected)
- `.claude/skills/nestjs-patterns.md` (if NestJS detected)
- `.claude/skills/swiftui-patterns.md` (if SwiftUI detected)
- `.claude/skills/uikit-patterns.md` (if UIKit detected)
- `.claude/skills/vapor-patterns.md` (if Vapor detected)
- `.claude/skills/compose-patterns.md` (if Jetpack Compose detected)
- `.claude/skills/android-views-patterns.md` (if Android Views detected)

### Agents

See [templates-agents.md](references/templates-agents.md) for agent templates.

**Always generate** (2 agents):
- `.claude/agents/code-reviewer.md` (dynamic: lint command based on detected linter)
- `.claude/agents/test-writer.md` (dynamic: test command based on detected framework)

### Rules

See [templates-rules.md](references/templates-rules.md) for rule templates.

- `.claude/rules/typescript.md` (if TypeScript detected)
- `.claude/rules/python.md` (if Python detected)
- `.claude/rules/code-style.md` (always — references detected formatter/linter)

### Commands

See [templates-commands.md](references/templates-commands.md) for command templates.

**Always generate** (5 commands):
- `.claude/commands/task.md`
- `.claude/commands/status.md`
- `.claude/commands/done.md`
- `.claude/commands/analyze.md`
- `.claude/commands/code-review.md`

### State

- Create `.claude/state/task.md` with empty initial state (**only if it does not already exist**)

---

## Step 5: Deep Codebase Analysis

Perform the full codebase analysis described in [analysis-prompt.md](references/analysis-prompt.md).

This is the most critical step. Follow ALL phases:
1. **Phase 1: Discovery** — Read actual project files to gather specific information
2. **Phase 2: Generate** — Write `.claude/CLAUDE.md` using ONLY discovered information
3. **Phase 3: Verify** — Check quality before finalizing

The CLAUDE.md must include the detected tech stack summary table and reference the generated skills, agents, rules, and commands in its structure. Include actual commands from `package.json` scripts (or equivalent), real file paths, and observed code conventions.

**The CLAUDE.md MUST reference**:
- The project name and description (from package.json/README/equivalent)
- The detected tech stack with specific configuration notes
- Actual directory structure (depth 3)
- Real commands from scripts
- Code conventions observed from reading source files
- The generated skills, agents, and commands

---

## Step 6: Summary

Output a summary to the user:

```
## Claude Code Starter - Setup Complete

### Tech Stack Detected
- **Language**: {primary language}
- **Framework**: {primary framework}
- **Package Manager**: {package manager}
- **Testing**: {testing framework}
- **Linter**: {linter}
- **Formatter**: {formatter}

### Files Created
{list all files created/updated with paths}

### Framework-Specific Skills
{list any conditional skills that were generated}

### Next Steps
1. Review `.claude/CLAUDE.md` and adjust any inaccuracies
2. Review `.claude/settings.json` permissions
3. Try `/task <description>` to start your first task
4. Use `/status` to check progress
5. Use `/done` to mark tasks complete
```

---

## Dynamic Value Reference

### Test Commands

| Testing Framework | Package Manager | Command |
|---|---|---|
| vitest/jest | npm | `npm run test` |
| vitest/jest | bun | `bun test` |
| vitest/jest | pnpm | `pnpm test` |
| vitest/jest | yarn | `yarn test` |
| bun-test | any | `bun test` |
| pytest | any | `pytest` |
| go-test | any | `go test ./...` |
| rust-test | any | `cargo test` |
| fallback | any | `{packageManager} test` |

### Lint Commands

| Linter | Package Manager | Command |
|---|---|---|
| eslint | bun | `bun eslint .` |
| eslint | other | `npx eslint .` |
| biome | bun | `bun biome check .` |
| biome | other | `npx biome check .` |
| ruff | any | `ruff check .` |
| none | any | (omit) |

### State File Initial Content

For **existing projects** (source files detected):

```markdown
# Current Task

## Status: Ready

No active task. Start one with `/task <description>`.

## Project Summary

{project name}{if description: - description}

**Tech Stack:** {summarized tech stack}

## Quick Commands

- `/task` - Start working on something
- `/status` - See current state
- `/analyze` - Deep dive into code
- `/done` - Mark task complete
```

For **new/empty projects**:

```markdown
# Current Task

## Status: In Progress

**Task:** {description or "Explore and set up project"}

## Context

New project - setting up from scratch.

{if framework: **Framework:** formatted name}
{if language: **Language:** formatted name}

## Next Steps

1. Define project structure
2. Set up development environment
3. Start implementation

## Decisions

(None yet - starting fresh)
```
