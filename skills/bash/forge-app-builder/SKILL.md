---
name: forge-app-builder
description: Guides building, deploying, troubleshooting, and installing Atlassian Forge apps — custom extensions built with the Forge CLI (forge create, forge deploy, forge install). Use when the user wants to create a Forge app (issue panels, dashboard gadgets, Confluence macros, global pages), is encountering Forge CLI errors or deployment issues (e.g. forge install failures, environment errors), or needs help with Forge-specific concepts like resolvers, UI Kit, manifest scopes, or developer spaces. Do not use for general Jira configuration, automation rules, JQL queries, or Atlassian REST API usage outside of a Forge app context.
license: Apache-2.0
labels:
  - confluence
  - jira
  - bitbucket
  - atlassian
  - forge
maintainer: amoore
namespace: cloud
---
# Forge App Builder

**When building a Forge app, the agent MUST complete this workflow in order. Do not skip steps. Do not substitute manual instructions for running the scripts below.**

## Critical Rules

1. **Always use `forge create`** to scaffold apps — it registers the app and generates a valid app ID
2. **Never manually scaffold** — apps without valid app IDs cannot be deployed
3. **If `forge create` fails, STOP** — inform the user and provide the manual command
4. **Never ask for API tokens in chat** — direct users to run `forge login` in their terminal and enter credentials there
5. **Always ask the user to choose** when multiple options exist (developer spaces, sites) — never pick on their behalf
6. **Always ask the user for their Atlassian site URL during installation** — never try to discover it from other apps, environment variables, or any other source
7. **Always run the deploy script for deploy and install** — do not give the user only manual `forge deploy` / `forge install` commands as the primary outcome; run `scripts.deploy_forge_app.py` yourself

## MCP Server Prerequisites

This skill works best with the following MCP servers. The scripts and CLI workflow function without them, but the agent will lack access to up-to-date Forge documentation for template selection, module configuration, and code patterns.


| MCP Server    | Required?            | Purpose                                                                   |
| ------------- | -------------------- | ------------------------------------------------------------------------- |
| **Forge MCP** | Strongly recommended | Template lookup, module discovery, manifest syntax, UI Kit/backend guides |
| **ADS MCP**   | Optional             | Atlaskit component/token/icon lookup (Custom UI apps only)                |


If MCP servers are not connected, inform the user that code guidance may be based on the model's training data and could be outdated. Recommend they verify against [developer.atlassian.com/platform/forge](https://developer.atlassian.com/platform/forge/).
                                                             |

## Agent Workflow

**Complete steps 0–5 in order. Run the scripts yourself; do not only instruct the user to run them.**

### Step 0: Prerequisites (Install Automatically If Missing)

**Before any other steps**, call the `forge-development-guide` tool to get the current Node.js version requirement and CLI setup instructions. Then check and install prerequisites:

1. **Node.js** — Run `node -v`. If missing or below the version specified in the development guide:
  - **macOS (Homebrew):** `brew install node`
  - **nvm:** `nvm install <version>` then `nvm use <version>`
  - **fnm:** `fnm install <version>` then `fnm use <version>`
  - **Other:** [https://nodejs.org](https://nodejs.org) (LTS)
2. **Forge CLI** — Run `forge --version`. If missing:
  ```bash
   npm install -g @forge/cli
  ```
3. **Forge login** — Run `forge whoami`. If not logged in:
  - **Never ask for or accept API tokens in chat** — tokens are sensitive; the user must enter them only in their terminal
  - Direct the user to create an API token: [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
  - Tell the user to run `forge login` **in their own terminal** (not via the agent). The CLI will prompt for:
    - Atlassian email
    - API token (paste only in the terminal when prompted)
  - Example message: *"You need to log in to Forge. Create an API token at [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens), then run `forge login` in your terminal. Enter your email and token when prompted — do not paste them here."*
  - After the user confirms they've logged in, retry the workflow

Install in order: Node.js first (required for npm), then Forge CLI, then login. Retry the workflow after installing.

### Step 1: Discover Developer Spaces

```bash
forge developer-spaces list --json
```

### Step 2: Ask User to Choose Developer Space

**Do not proceed to Step 3 until the user has selected a developer space.** Present the list from Step 1 (names and IDs) and ask which space to use. If only one space exists, you may use it and briefly inform the user. Never pick one of multiple spaces on the user's behalf.

### Step 3: Create App

All `python3 -m scripts.`* commands must be run from the skill directory (the directory containing this SKILL.md file). Derive it from the SKILL.md path provided in the system prompt. Use `python3` on macOS if `python` is not available.

Run from the skill directory. The `--directory` flag sets the **parent directory** under which the app folder (named after `--name`) will be created. The script `cd`s into that directory before running `forge create`, so the app appears as a subdirectory (e.g. `<parent-directory>/<app-name>/`). If omitted, the app is created under the current directory.

```bash
python3 -m scripts.create_forge_app \
  --template <template> \
  --name <app-name> \
  --dev-space-id <selected-id> \
  --directory <parent-directory>
```

To find the right template for the user's needs:

- Call `list-forge-modules` to identify the appropriate module type
- Call `search-forge-docs` with a query like "template for " to find the matching template name

Validate a template: `python3 -m scripts.list_templates --validate <name>`
List all templates: `python3 -m scripts.list_templates --list`

### Step 4: Customize Code

After `forge create` succeeds:

```bash
cd <app-name>
npm install
```

#### UI Kit vs Custom UI — Choose the Right Tools

Before writing any UI code, determine which approach the app uses. **Getting this wrong causes import errors and broken builds.**

- **UI Kit** (most `forge create` templates): manifest uses `render: native` or code imports from `@forge/react`. Use `forge-ui-kit-developer-guide` as the ONLY UI reference. Do NOT suggest `@atlaskit/`* imports — they won't work.
- **Custom UI**: manifest has `resource` pointing to a `static/` directory. Use ADS MCP tools (`ads_plan`, `ads_get_components`, `ads_get_all_icons`) for component discovery. Do NOT use `forge-ui-kit-developer-guide` — it describes a different API.

#### Knowledge tools for implementation

- `forge-ui-kit-developer-guide` — Frontend components (**UI Kit only**)
- `ads_plan` / `ads_get_components` — Component and token lookup (**Custom UI only**)
- `forge-backend-developer-guide` — Backend resolvers and APIs
- `forge-app-manifest-guide` — Manifest configuration
- `search-forge-docs` — Search for specific APIs or props

### Step 5: Deploy and Install (run the deploy script)

**You MUST run the deploy script** — do not only paste manual `forge deploy` / `forge install` commands for the user to run. Execute the script from the skill directory.

- **If you have the user's Atlassian site URL** (e.g. they provided it earlier or in the request), run in one go:

```bash
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --site <site-url> \
  --product <jira|confluence>
```

- **If you do not have the site URL yet:** run deploy only, then ask for the site, then run again to install:

```bash
# 1) Deploy only
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --product <jira|confluence> \
  --deploy-only

# 2) Ask the user: "What is your Atlassian site URL (e.g. yourcompany.atlassian.net)?"

# 3) After they reply, run again with their site to complete install
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --site <site-url> \
  --product <jira|confluence> \
  --skip-deps
```

**Always ask the user for their site URL** when needed for install; never try to discover it. If scopes changed from a previous install, add `--upgrade` to the install (or run the script again with `--site` and the script will handle it; for manual upgrade use `forge install ... --upgrade`).

#### Cross-product installation

When an app uses scopes from multiple products (e.g. a Confluence macro that also reads Jira data), the deploy script **automatically detects** the required products from the manifest scopes and installs on all of them. The `--product` flag sets the primary product; the script adds any additional products found in the scopes.

If you need to install manually, run `forge install` once per product:

```bash
forge install --non-interactive --site <site-url> --product confluence -e development
forge install --non-interactive --site <site-url> --product jira -e development
```

## Handling `forge create` Failures

When `forge create` fails, **never attempt workarounds or manual scaffolding**.


| Error                                      | Action                                                                                                                                            |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Prerequisites missing (Node.js, Forge CLI) | Run Step 0 install commands, then retry                                                                                                           |
| "Prompts can not be meaningfully rendered" | Ask user to run `forge create` in an interactive terminal                                                                                         |
| "No developer spaces found"                | Direct user to [https://developer.atlassian.com/console/](https://developer.atlassian.com/console/)                                               |
| "directory already exists"                 | A folder named `<app-name>` already exists inside the parent directory. Choose a different name or remove the existing folder                     |
| Network/auth issues, not logged in         | Direct user to [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens), then run `forge login` in their terminal |
| Any other error                            | Show error, ask user for guidance                                                                                                                 |


Example response when it fails:

```
forge create needs an interactive terminal. Please run:

  forge create --template jira-dashboard-gadget my-app-name

Once created, let me know and I'll help customize it.
```

## Module Selection

Call `list-forge-modules` for a comprehensive, up-to-date list of all available modules organized by product. Then use `search-forge-docs` with the module name for configuration details and YAML examples.

## Scripts


| Script                        | Purpose                                                                                                                                                                                               |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/create_forge_app.py` | Create app with dev space selection and template validation. `--directory` sets the parent dir (script cd's into it). Run: `python3 -m scripts.create_forge_app`                                      |
| `scripts/list_templates.py`   | List/validate all Forge templates from Atlassian registry. Run: `python3 -m scripts.list_templates`                                                                                                   |
| `scripts/deploy_forge_app.py` | Deploy and install app (prerequisites check, npm install, lint, deploy, install). Auto-detects cross-product scopes and installs on all required products. Run: `python3 -m scripts.deploy_forge_app` |


## Completion checklist

Before considering the workflow done, confirm:

- User selected developer space when more than one existed (or only one existed)
- App was created via `create_forge_app` (or user ran `forge create` after a failure)
- Code was customized and `npm install` run in the app directory
- **Deploy script was executed by the agent** (not only manual commands given to the user)
- If install was needed, user was asked for site URL and the script was run with `--site` (or user provided site and install completed)
- If the app uses cross-product scopes (e.g. Confluence app reading Jira data), it was installed on **all** required products (the deploy script handles this automatically)

## Common agent mistakes (avoid these)

- **Picking a developer space when multiple exist** — always ask the user to choose.
- **Skipping the deploy script** — giving only "run `forge deploy` and `forge install`" instructions instead of running `deploy_forge_app.py` yourself.
- **Not asking for site URL** — when install is required, ask the user for their Atlassian site URL; do not guess or skip install.
- **Proceeding to create app before user chooses a developer space** — wait for their selection when there are multiple spaces.

## Troubleshooting

For CLI commands, debugging techniques, and common error patterns, call `forge-development-guide`. For quick checks:

- **Not logged in / auth failed**: Create API token at [id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens), then run `forge login` in your terminal (never paste token in chat)
- **App not appearing after install**: Check `forge logs -e development --limit 50`, verify manifest with `forge lint`, re-install with `--upgrade` if scopes changed
- **"forge: command not found"**: `npm install -g @forge/cli`

