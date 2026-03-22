---
name: vcp-init
description: >
  Initialize VCP configuration for this project. Creates global config (~/.vcp/config.json)
  if it doesn't exist, then creates project config (.vcp/config.json). Detects frameworks, scopes,
  and discovers the plugin path.
  Run this once when setting up VCP for a new project.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash, WebFetch, AskUserQuestion
argument-hint: ""
---

# VCP Project Initialization

Create both a global config (`~/.vcp/config.json`) and a project config (`.vcp/config.json`). The global config stores the standards repository URL and plugin path, shared by all projects. The project config stores project-specific settings.

## Step 1: Check for Existing Configs

Read both `~/.vcp/config.json` and `.vcp/config.json` from the project root.

| Global exists | Project exists | Action |
|:---:|:---:|---|
| Yes | Yes (with pluginRoot) | Show both configs and ask if user wants to reconfigure or keep them. If they want to keep them, stop here. |
| Yes | Yes (no pluginRoot) | Copy `pluginRoot` from global to project config, show what was added, and stop. |
| Yes | No | Skip to Step 3 (project setup), reusing global config values. |
| No | Yes | Create global config (Step 2), then check if project needs `pluginRoot` patched. |
| No | No | Full initialization (Step 2 through Step 6). |

## Step 2: Create Global Config

**Only run this step if `~/.vcp/config.json` does not exist.**

1. Tell the user: "VCP needs a global config at `~/.vcp/config.json`. This stores the standards repository URL and plugin path, shared by all your projects on this machine."

2. Ask via AskUserQuestion: "Do you want to use a custom standards repository, or the default VCP public standards?"
   - **Custom:** Ask for the URL. It must start with `https://` and point to a VCP-compatible `manifest.json`. Validate the URL format.
   - **Default:** Use `https://raw.githubusercontent.com/Z-M-Huang/vcp/main/standards/manifest.json`

3. Discover the VCP plugin path:
   - Use Glob to search `~/.claude/` with pattern `**/vcp/lib/vcp-context-core.ts`
   - If not found there, search the current project root with the same pattern
   - From the found file path, derive the plugin root: the `vcp/` directory containing the `lib/` directory
   - If not found at all, warn the user but continue

4. Optionally ask if the user wants to set global defaults (severity, scopes, compliance, ignore). These become defaults for all projects. If the user declines, use an empty `defaults` object.

5. Write `~/.vcp/config.json` using Bash (`mkdir -p ~/.vcp && ...` to ensure the directory exists):

```json
{
  "$schema": "https://raw.githubusercontent.com/Z-M-Huang/vcp/main/schemas/vcp-global.schema.json",
  "standards_url": "https://raw.githubusercontent.com/Z-M-Huang/vcp/main/standards/manifest.json",
  "pluginRoot": "/home/user/.claude/plugins/vcp",
  "debug": false,
  "defaults": {}
}
```

## Step 3: Scan the Project

Examine the project to understand what frameworks, languages, and tools are in use. Read dependency manifests (package.json, requirements.txt, pyproject.toml, pom.xml, build.gradle, Gemfile, go.mod, Cargo.toml, etc.), browse the directory structure, and look at file types present.

Based on what you find, determine:
1. **Frameworks** — which specific frameworks and tools the project uses (e.g. react, express, postgresql, django)
2. **Scopes** — which VCP scopes apply:
   - `web-frontend`: the project has client-side web code
   - `web-backend`: the project has server-side web code
   - `database`: the project interacts with databases
   - `mobile`: the project targets mobile platforms. Detection hints: `android/` or `ios/` directories, `react-native` / `expo` / `flutter` / `@capacitor` in dependencies, `.swift` or `.kt`/`.java` source files in mobile-specific paths, `Podfile`, `build.gradle` with Android plugin
   - `desktop`: the project builds desktop applications. Detection hints: `electron` or `@electron/` or `tauri` or `@tauri-apps/` in dependencies, `electron-builder` config, `tauri.conf.json`
   - `cli`: the project is a command-line tool. Detection hints: `bin` field in `package.json`, `commander` / `yargs` / `inquirer` / `oclif` in Node.js deps, `argparse` / `click` / `typer` / `fire` in Python deps, `cobra` / `urfave/cli` in Go deps, `clap` in Rust deps
   - `devops`: the project contains infrastructure/deployment configuration. Detection hints: `Dockerfile`, `.github/workflows/` directory, `*.tf` files (Terraform), `k8s/` or `kubernetes/` or `helm/` directories, `docker-compose.yml`, `Jenkinsfile`, `.gitlab-ci.yml`, `pulumi/` directory
   - `agentic-ai`: the project develops AI agents, MCP servers, or multi-agent systems. Detection hints: `@anthropic-ai/claude-agent-sdk` or `@anthropic-ai/sdk` or `claude-code` in dependencies, `mcp` / `@modelcontextprotocol/sdk` in dependencies, `mcpServers` in config files, `agents/` or `mcp-servers/` directories, `.claude/agents/` directory, `langchain` / `langgraph` / `crewai` / `autogen` / `semantic-kernel` in dependencies, files referencing `tool_use` or `tool_call` patterns
3. **Exclude patterns** — which paths should be skipped during scanning (build output, vendored code, generated files)

Use your judgment. Do not rely on a fixed lookup table — understand the project and decide what applies.

## Step 4: Confirm with the User

**Always ask the user to confirm before writing the config.** Present your proposed configuration and ask for approval. Do not write `.vcp/config.json` until the user explicitly confirms.

Show the user:

1. **Standards URL** — Show the URL from global config: "Using standards from: `{url}`". If the user wants a different URL for this specific project, they can override it (rare).
2. **Plugin root** — Show the path from global config: "Plugin path: `{pluginRoot}`"
3. **Scopes** — which scopes you detected and why. Let the user add, remove, or change them. If global config has `defaults.scopes`, use those as the starting point and merge with detected scopes.
4. **Frameworks** — which frameworks you found. Let the user correct the list.
5. **Compliance** — ask if the project needs to comply with regulatory frameworks (GDPR, PCI DSS, HIPAA). Do not assume any are needed.
6. **Exclude patterns** — suggest reasonable defaults for the detected ecosystem. Let the user add or remove patterns.
7. **Severity threshold** — ask what minimum severity to report (critical, high, medium, low). If global config has `defaults.severity`, propose that as the default. Explain that the default `"medium"` reports medium, high, and critical findings.

Note: The config also supports an `ignore` array to suppress specific standards, rules, or CWE patterns. Most projects start with nothing ignored, so don't prompt for it during init — the user can add entries later.

Wait for the user to confirm or adjust before proceeding to Step 5.

## Step 5: Write `.vcp/config.json`

The config must conform to the JSON schema at:
```
https://raw.githubusercontent.com/Z-M-Huang/vcp/main/schemas/vcp.schema.json
```

Generate the config based on the user-confirmed answers. Copy `pluginRoot` from the global config into the project config (so skills can find it). Do NOT copy `standards_url` unless the user explicitly wants a per-project override.

```json
{
  "$schema": "https://raw.githubusercontent.com/Z-M-Huang/vcp/main/schemas/vcp.schema.json",
  "version": "1.0",
  "scopes": {
    "web-frontend": true,
    "web-backend": true,
    "database": false
  },
  "compliance": [],
  "frameworks": ["react", "express", "postgresql"],
  "exclude": [
    "node_modules/**",
    "dist/**",
    "build/**"
  ],
  "severity": "medium",
  "ignore": [],
  "pluginRoot": "/home/user/.claude/plugins/vcp"
}
```

## Step 6: Confirm

Show a summary:
```
VCP initialized for this project.

Standards:   VCP public (https://raw.githubusercontent.com/.../manifest.json)
Scopes:      web-frontend, web-backend
Compliance:  none
Frameworks:  react, express, postgresql
Exclude:     node_modules/**, dist/**, build/**
Severity:    medium+
Plugin root: /home/user/.claude/plugins/vcp

Global config: ~/.vcp/config.json
Project config: .vcp/config.json

Run /vcp-audit, /vcp-dependency-check, or /vcp-pre-commit-review to start.
```
