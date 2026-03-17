---
description: >-
  Ensures the project has comprehensive, accurate development setup instructions
  in the README for human developers. Detects tech stack, external services,
  environment config, and generates step-by-step "how to run everything in dev
  mode" instructions. Audits existing instructions against actual project state.
  Use after /optimus:init or standalone when onboarding docs feel incomplete.
  Handles single projects, monorepos, and multi-repo workspaces.
disable-model-invocation: true
---

# Development Setup Documentation

Ensure the project has accurate, whole-project-scope "how to run in development mode" instructions in the README — covering prerequisites, installation, external services, environment config, and run commands. Detect existing instructions and audit them against actual project state. Create or update with user approval.

## Step 1: Detect Full Project Context

Build a comprehensive understanding of the project — enough to write accurate setup instructions.

**Read shared references for detection:**
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` — workspace detection
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/project-detection.md` — monorepo/single-project detection
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/tech-stack-detection.md` — manifest → tech stack + package manager

**Shortcut when init was already run:** If `.claude/.optimus-version` exists, read `.claude/CLAUDE.md` for pre-detected tech stack, package manager, commands, and project structure. Still read manifests directly to verify and to capture details init doesn't store (engine constraints, dependency versions, service configs). If `.claude/.optimus-version` is absent, do full detection from manifests using the shared references above.

**Detect tech stack and package manager** using the `tech-stack-detection.md` tables. Extract: project name, tech stack(s), build/test/lint/dev commands from manifest scripts, runtime version constraints (e.g., `engines.node` in package.json, `python_requires` in pyproject.toml, `rust-version` in Cargo.toml, `environment.sdk` in pubspec.yaml).

**Detect project structure** using `project-detection.md` and `multi-repo-detection.md`. Determine: single project, monorepo (with subproject list and per-subproject tech stacks), or multi-repo workspace (with repo list).

**Detect external services and dependencies** — read `$CLAUDE_PLUGIN_ROOT/skills/dev-setup/references/dev-setup-sections.md` for the signal-to-section mapping table. Scan for:

- `docker-compose.yml` / `compose.yml`: parse `services` for databases (postgres, mysql, mongo, redis, elasticsearch), message queues (rabbitmq, kafka), caches, and other infrastructure. Note which services have `build:` (app services) vs image-only (infrastructure services).
- `Dockerfile` / `Dockerfile.dev`: indicates Docker-based dev workflow.
- `Makefile` / `Justfile`: scan for targets like `dev`, `start`, `setup`, `run`, `serve`, `up`, `docker-up`.
- `Procfile` / `Procfile.dev`: process runner (foreman, overmind, honcho).
- `.env.example` / `.env.sample` / `.env.template`: environment variable templates — read to understand required config variables.
- Database config: `database.yml`, `prisma/schema.prisma`, `alembic.ini`, `knexfile.*`, `ormconfig.*`, migration directories.
- Private registry indicators: `.npmrc` (registry config), `pip.conf`, `.pypirc`, Maven `settings.xml` references.
- System tool requirements from configs: `nvm`/`.nvmrc`/`.node-version`, `pyenv`/`.python-version`, `rustup`/`rust-toolchain.toml`, `.tool-versions` (asdf).
- Code generation: protobuf configs, `openapi-generator`, `build_runner` in Dart dev_dependencies, `sqlc.yaml`, GraphQL codegen configs (`codegen.ts`, `.graphqlrc.*`).
- For monorepos: aggregate all services and dependencies across subprojects.
- For multi-repo workspaces: gather context per repo, then synthesize a whole-workspace view (all repos' services, shared infrastructure, cross-repo dependencies).

### Step 1 Checkpoint

Print a **Context Summary** to the user:

- **Tech stack(s)** and **package manager(s)**
- **Project structure** (single / monorepo with subprojects / multi-repo with repos)
- **External services detected** (list with source — e.g., "PostgreSQL (docker-compose.yml), Redis (docker-compose.yml)")
- **Environment config files found** (`.env.example`, etc.)
- **Runtime version constraints** (e.g., "Node.js >=18 (engines.node), Python >=3.11 (python_requires)")
- **Dev workflow signals** (Docker-based, Makefile-based, script-based, process runner, etc.)

Give the user a chance to correct misdetections before proceeding.

## Step 2: Scan Existing Dev Instructions

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/readme-section-detection.md` for the detection algorithm.

**Read the following documentation files** (skip any that don't exist):
- Root `README.md`
- `CONTRIBUTING.md`
- `docs/development.md`, `docs/setup.md`, `docs/getting-started.md`

For each file that exists, read its full content, then apply the detection algorithm from the reference above.

For monorepos: focus on the root README (whole-project scope). Individual subproject READMEs are NOT the target — the goal is instructions to run everything together.

For multi-repo workspaces: scan workspace root `README.md` if it exists.

**Classify each aspect** as: **Found & accurate**, **Found but outdated**, **Partial**, or **Missing**.

Aspects to check:
- **Prerequisites** — runtimes, system tools, version managers
- **Installation** — dependency install commands
- **External Services** — databases, queues, caches, how to start them
- **Environment Config** — `.env` setup, required variables
- **Running in Dev Mode** — start commands, expected URLs/ports
- **Building** — production build command
- **Testing** — test command, coverage

## Step 3: Present Assessment and Plan

Present findings as a table with status per aspect (use the classification from Step 2).

**If all aspects are "Found & accurate":** Report to user — no action needed. Skip to Step 6 (report only).

**If outdated items found:** Show current content vs proposed correction for each.

**Caution rule:** For existing content that seems intentionally unusual or whose purpose is beyond what the codebase reveals — **flag explicitly and ask** rather than silently changing. Err on the side of caution. Examples: custom startup scripts with non-obvious flags, environment variables with no clear source, instructions referencing external systems not visible in the codebase.

Use `AskUserQuestion` — header "Dev Setup Documentation", question "How would you like to proceed?":
- **Create/Update** — "Generate dev setup instructions (I'll show you before writing)"
- **Skip** — "No changes needed"

If user selects **Skip**, jump to Step 6 (report only).

## Step 4: Generate Dev Setup Content

Read `$CLAUDE_PLUGIN_ROOT/skills/dev-setup/references/dev-setup-sections.md` for section templates and the signal-to-section mapping.

Generate only applicable sections, in this order:

1. **Prerequisites** — runtime versions (from manifest constraints, not guesses), system tools (docker, make, etc.), version managers (nvm, pyenv, rustup) if config files detected
2. **Installation** — clone command, install dependencies (correct PM and prefix), post-install steps (code generation, database migrations, asset compilation)
3. **External Services** — how to start required infrastructure. When `docker-compose.yml` / `compose.yml` exists, use `docker compose up -d` as the recommended approach. Otherwise describe manual setup. Include: what services are needed, how to start them, how to verify they're running, default ports from compose config. For credentials, note that the service uses defaults from docker-compose — never copy actual password values into the README.
4. **Environment Setup** — copy `.env.example` → `.env`, describe required variables (read from the example file), any service-specific configuration
5. **Running in Development** — the primary dev command(s), what URL/port to expect, how to verify it works. For monorepos: how to run specific subprojects AND how to run everything together. For docker-only setups (Dockerfile + docker-compose + no obvious local-run scripts): Docker-based instructions as the primary path.
6. **Building** — production build command (only if different from dev)
7. **Running Tests** — test command, coverage command if available
8. **Common Issues** — only if clear signals exist (e.g., `.nvmrc` → mention `nvm use`; docker services → mention `docker compose up -d` must run first; private registry → mention authentication)

**Content principles:**
- Direct, imperative instructions ("Install dependencies:" not "You should install dependencies")
- Exact commands with detected package manager (from `tech-stack-detection.md` prefix rules)
- Version numbers from manifest constraints only — never guess versions
- Commands ordered as a new developer would run them (prerequisites → install → services → env → run)
- For monorepos: workspace-level install first, then per-subproject run instructions
- For docker-only dev setups: Docker-based instructions as primary path, bare-metal as secondary if discernible

## Step 5: Place Content (with user approval)

**Show the user the exact proposed changes before writing anything.** Full content for new files, section diff for updates. Wait for approval.

### Placement rules by topology

**Single project:** Insert or update a "Development" section in root `README.md`. If no `README.md` exists, create a minimal one (project name from manifest + one-line description if available + dev setup sections). Place the section after the project description, before a contributing section if one exists.

**Monorepo:** Insert or update in root `README.md`. The section covers the whole-project dev experience — workspace-level install, how to start shared services, how to run specific subprojects, how to run everything together.

**Multi-repo workspace:** Create a `README.md` at the workspace root. Direct-to-the-point content: repo map (name, path, purpose), how to clone all repos, shared prerequisites, how to start shared external services, how to run the full system. This file is not version-controlled (the workspace root has no `.git`).

### Cautious editing rules

- **Never delete** existing content outside the dev-setup section being inserted/updated.
- If a "Development", "Getting Started", or similar section already exists, propose replacing **just that section** — preserve everything else.
- Preserve all other sections, formatting, badges, images, and links.
- If the README structure is too unusual to safely insert a section (no clear heading hierarchy, HTML-heavy layout), show the generated content to the user and ask where to place it manually.
- If dev instructions are found in `CONTRIBUTING.md` but not in `README.md`, use `AskUserQuestion` — header "Existing Instructions", question "Dev setup instructions were found in CONTRIBUTING.md but not in README.md. How should we handle this?":
  - **Summary + link** — "Add a brief 'Development' section in README.md linking to CONTRIBUTING.md"
  - **Move to README** — "Move the full instructions to README.md"
  - **Leave as-is** — "Keep instructions only in CONTRIBUTING.md"

## Step 6: Verify and Report

If no files were modified (skip or no-action path), skip verification and proceed directly to the report.

- Read back the modified or created file(s).
- **Verify:** all commands use the correct package manager prefix, prerequisite versions match manifest constraints, directory paths match the actual filesystem, external service names match docker-compose service definitions, environment variable names match `.env.example`.
- **If any check fails:** show the correction to the user, wait for approval, apply it, then re-verify.

**Report** to the user: what was created or updated, which sections were included, and any aspects that were intentionally skipped (with reason).

**Recommend next skill:**
- If `/optimus:init` has not been run (no `.claude/.optimus-version`): recommend `/optimus:init` for AI-assisted development setup.
- If test instructions were thin or absent: recommend `/optimus:unit-test` to establish test coverage.
- Otherwise: recommend `/optimus:tdd` for new feature work.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
