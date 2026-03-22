---
name: api2cli
description: "Generate a CLI + AgentSkill from any REST API. Use when: user says 'create a CLI for X', 'wrap this API', 'make a skill for X', 'publish my CLI', 'publish to npm', 'push to github'. Handles discovery, scaffolding, resource implementation, building, linking, skill generation, npm publishing, and GitHub publishing."
---

# api2cli

Turn any REST API into a standardized, agent-ready CLI.

Always use `npx api2cli` to run commands. Always use `--json` when calling generated CLIs programmatically.

## Prerequisites

```bash
bun --version || curl -fsSL https://bun.sh/install | bash
```

## Workflow

Follow all steps in order — do not skip any.

### 1. Discover the API

Find the API docs or OpenAPI spec. Identify: base URL, auth type, auth header, all resources and endpoints.

### 2. Create the scaffold

```bash
npx api2cli create <app> --base-url <url> --auth-type bearer
```

See [references/create.md](references/create.md) for all flags and what gets generated.

### 3. Implement resources

Create `~/.cli/<app>-cli/src/resources/<resource>.ts` for each API resource. Register in `src/index.ts`.

See [references/resource-patterns.md](references/resource-patterns.md) for the CRUD template and library API.

### 4. Build, link, and test

```bash
npx api2cli bundle <app>
npx api2cli link <app>
<app>-cli --help
<app>-cli <resource> list --json
```

`api2cli link` adds `~/.local/bin` to PATH automatically. No `export PATH` needed.

### 5. Finalize skill and README

Replace all `{{...}}` placeholders in `skills/<app>-cli/SKILL.md` and `README.md` with actual values, then symlink skill to agent directories.

See [references/skill-generation.md](references/skill-generation.md) for the template, format, and symlink instructions.

To also link skills for OpenClaw:

```bash
npx api2cli link <app> --openclaw
```

See [references/openclaw.md](references/openclaw.md) for the one-prompt setup, ClawHub publishing, API key auto-detection, and custom `--skills-path` usage.

Also available on ClawHub: `npx clawhub install api2cli`

### 6. Publish (when user asks)

Before any publish target, run these pre-flight checks:

1. **Verify `gh` CLI is authenticated**: run `gh auth status`. If not logged in, ask the user to run `gh auth login` first. **Stop and wait.**
2. **Check if the CLI is already on GitHub**: run `git remote get-url origin` in the CLI directory.
   - If no remote exists → the CLI is not on GitHub yet. **Automatically run the GitHub publish flow first** (see below) before proceeding to npm or registry publish.
   - If a remote exists → already on GitHub, continue.

#### To GitHub

Push the CLI to a public GitHub repo.

See [references/publish-to-github.md](references/publish-to-github.md) for pre-flight checks, repo creation, and push workflow.

#### To npm

Requires the CLI to be on GitHub first (for `repository` field in package.json). If not on GitHub, run the GitHub publish flow above first.

Publish the CLI to the npm registry so users can `npm i -g <name>` or `npx <name>`.

See [references/publish-to-npm.md](references/publish-to-npm.md) for auth, package.json validation, build, verify, and publish workflow. Also see [references/package-checklist.md](references/package-checklist.md) for the field-by-field package.json reference.

#### To ClawHub

Publish the generated skill to ClawHub so OpenClaw users can discover and install it.

1. **Auth**: run `npx clawhub login`. If not authenticated, ask the user to complete login first. **Stop and wait.**
2. **Push the skill**: run `npx clawhub publish <cli-dir>/skills/<app>-cli --slug <app>-cli`
3. After publish, users can install with:
   ```bash
   npx clawhub install <app>-cli
   ```

See [references/openclaw.md](references/openclaw.md) for the full OpenClaw setup workflow.

#### To Sundial Hub

Publish the generated skill to the Sundial Hub so any agent (Claude Code, Cursor, Codex, etc.) can install it.

1. **Auth**: run `npx sundial-hub auth status`. If not authenticated, ask the user to run `npx sundial-hub auth login` first. **Stop and wait.**
2. **Push the skill**: run `npx sundial-hub push <cli-dir>/skills/<app>-cli --visibility public --categories coding`
3. After publish, users can install with:
   ```bash
   npx sundial-hub add <sundial-username>/<app>-cli
   ```

#### To api2cli.dev registry

Requires the CLI to be on GitHub first. If not on GitHub, run the GitHub publish flow above first.

Register on api2cli.dev so others can install with `npx api2cli install <name>`.

See [references/publish.md](references/publish.md) for the registry publish workflow.

## Conventions

```
<app>-cli <resource> <action> [flags]
<app>-cli auth set|show|remove|test
```

`--json` returns: `{ "ok": true, "data": [...], "meta": { "total": 42 } }`

Other flags: `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`

Exit codes: 0 = success, 1 = API error, 2 = usage error

Tokens: `~/.config/tokens/<app>-cli.txt` (chmod 600)
