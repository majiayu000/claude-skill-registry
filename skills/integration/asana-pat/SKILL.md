---
name: asana
description: "Manage Asana tasks, projects, briefs, status updates, custom fields, dependencies, attachments, events, and timelines via Personal Access Token (PAT)."
homepage: https://developers.asana.com/docs/personal-access-token
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["ASANA_PAT"]},"primaryEnv":"ASANA_PAT","homepage":"https://developers.asana.com/docs/personal-access-token"}}
---

# Asana

This skill provides a dependency-free Node.js CLI that calls the Asana REST API (v1) using a **Personal Access Token (PAT)**.

- Script: `{baseDir}/scripts/asana.mjs`
- Auth: `ASANA_PAT` (preferred) or `ASANA_TOKEN`
- Output: **JSON only** (stdout), suitable for agents and automation

## Setup

1. Create an Asana PAT in your Asana account (Developer Console is **not** required for PAT usage).
2. Provide the token to OpenClaw/Clawdbot as `ASANA_PAT`.

### Common injection patterns

- Shell env (local testing):

  `export ASANA_PAT="..."`

- OpenClaw config (recommended): set `skills.entries.asana.apiKey` (or `env.ASANA_PAT`) so the secret is injected only for the agent run.

### Configure via OpenClaw CLI (recommended)

This is the safest way to set the PAT because it keeps secrets out of prompts and ad-hoc shell history.

**Recommended (apiKey → ASANA_PAT):**

```bash
openclaw config set skills.entries.asana.enabled true
openclaw config set skills.entries.asana.apiKey "ASANA_PAT_HERE"
```

`skills.entries.asana.apiKey` is a convenience field: for skills that declare `metadata.openclaw.primaryEnv`, OpenClaw injects `apiKey` into that env var for the agent run (this skill’s primary env is `ASANA_PAT`).

**Alternative (explicit env):**

```bash
openclaw config set skills.entries.asana.enabled true
openclaw config set skills.entries.asana.env.ASANA_PAT "ASANA_PAT_HERE"
```

**Verify what is stored:**

```bash
openclaw config get skills.entries.asana
openclaw config get skills.entries.asana.enabled
openclaw config get skills.entries.asana.apiKey
```

**Remove a stored token:**

```bash
openclaw config unset skills.entries.asana.apiKey
# or
openclaw config unset skills.entries.asana.env.ASANA_PAT
```

#### Important: sandboxed runs

When a session is sandboxed, skill processes run inside Docker and do **not** inherit the host environment. In that case, `skills.entries.*.env/apiKey` applies to host runs only.

Set Docker env via:

- `agents.defaults.sandbox.docker.env` (or per-agent `agents.list[].sandbox.docker.env`)
- or bake the env into your sandbox image

## First calls (sanity + discovery)

- Who am I:

  `node {baseDir}/scripts/asana.mjs me`

- List workspaces:

  `node {baseDir}/scripts/asana.mjs workspaces`

- (Recommended) Set a default workspace once:

  `node {baseDir}/scripts/asana.mjs set-default-workspace --workspace <workspace_gid>`

## ID resolution

When the user provides names (project/task/user), resolve to GIDs using one of:

- `typeahead --workspace <gid> --resource_type project|task|user --query "..."` (fast, best default)
- `projects --workspace <gid> --all` (enumerate)
- `users --workspace <gid> --all` (enumerate)

Avoid guessing a GID when multiple matches exist.

## Core: tasks

### List tasks assigned to a user (personal productivity)

`node {baseDir}/scripts/asana.mjs tasks-assigned --assignee me --workspace <workspace_gid> --all`

### List tasks in a project

`node {baseDir}/scripts/asana.mjs tasks-in-project --project <project_gid> --all`

### Search tasks (Advanced Search API)

Canonical primitive: `search-tasks` (supports many filters; preferred over adding narrow “search helper” commands).

One-liner example (search within a project):

`node {baseDir}/scripts/asana.mjs search-tasks --workspace <gid> --project <project_gid> --text "..." --all`

Useful filters:
- `--assignee me|<gid|email>` (maps to `assignee.any`)
- `--completed true|false`
- `--created_at.after <iso>` / `--modified_at.after <iso>`
- `--due_on.before YYYY-MM-DD` / `--due_at.before <iso>`
- `--is_blocked true|false` / `--is_blocking true|false`

### Create / update / complete

- Create:

  `node {baseDir}/scripts/asana.mjs create-task --workspace <gid> --name "..." --projects <project_gid> --assignee me`

- Update:

  `node {baseDir}/scripts/asana.mjs update-task <task_gid> --name "..." --due_on 2026-02-01`

- Complete:

  `node {baseDir}/scripts/asana.mjs complete-task <task_gid>`

## Project manager workflows

This skill supports the workflows commonly expected from a PM in Asana:

- Keep a **project brief** up to date (`upsert-project-brief`)
- Write **status updates** (`create-status-update`)
- Work with **timelines** (start/due dates) and shift schedules safely
- Use **custom fields** as first-class metadata
- Interpret **blockers** and dependency graphs (`project-blockers`, `dependencies`, `dependents`)

### Project brief

- Read:

  `node {baseDir}/scripts/asana.mjs project-brief <project_gid>`

- Upsert (create or update):

  `node {baseDir}/scripts/asana.mjs upsert-project-brief <project_gid> --title "Project brief" --html_text "<body>...</body>"`

### Status updates

- Create:

  `node {baseDir}/scripts/asana.mjs create-status-update --parent <project_gid> --status_type on_track --text "Weekly update..."`

- List:

  `node {baseDir}/scripts/asana.mjs status-updates --parent <project_gid> --all`

### Sections and moving tasks

- List sections:

  `node {baseDir}/scripts/asana.mjs sections --project <project_gid> --all`

- Create section:

  `node {baseDir}/scripts/asana.mjs create-section --project <project_gid> --name "Blocked"`

#### Add a task to a project

Command: `add-task-to-project`

Calls `POST /tasks/{task_gid}/addProject` and supports optional section placement and ordering.

Examples:

`node {baseDir}/scripts/asana.mjs add-task-to-project <task_gid> --project <project_gid>`

With section + ordering:

`node {baseDir}/scripts/asana.mjs add-task-to-project <task_gid> --project <project_gid> --section <section_gid> --insert_before null --insert_after null`

(`--section`, `--insert_before`, and `--insert_after` are optional; when provided they are passed through in the request body.)

#### Remove a task from a project

Command: `remove-task-from-project`

Calls `POST /tasks/{task_gid}/removeProject`.

Example:

`node {baseDir}/scripts/asana.mjs remove-task-from-project <task_gid> --project <project_gid>`

## Custom fields

Custom fields are critical for reliable PM automation.

- List a project’s custom fields:

  `node {baseDir}/scripts/asana.mjs project-custom-fields <project_gid> --all`

- Read a custom field definition:

  `node {baseDir}/scripts/asana.mjs custom-field <custom_field_gid>`

- Set task custom fields on create/update:

  `node {baseDir}/scripts/asana.mjs update-task <task_gid> --custom_fields '{"<custom_field_gid>":"<value>"}'`

Notes:
- For enums, the value is typically the enum option GID.
- For numbers, send a JSON number.

## Rich text, mentions, and reliability

Asana rich text fields are **XML-valid HTML fragments** wrapped in a `<body>` root element. The API rejects invalid XML or unsupported tags.

Key points:
- Use `html_notes` for task descriptions.
- Use `html_text` for comments/stories and status updates.
- Avoid unsupported tags like `<p>` and `<br>`; prefer literal newlines (`\n`) and `<hr/>` separators.
- For mentions/links, use `<a data-asana-gid="..."></a>` (or a self-closing `<a .../>`).

### Mention notifications

Creating a mention link does **not** guarantee notification delivery if the user is not already assigned or following.

For reliable pings, do one of:
- Assign the user first, then post the comment, OR
- Add the user as a follower, wait a few seconds, then post the comment

This skill supports the “add follower + wait” pattern:

`node {baseDir}/scripts/asana.mjs comment <task_gid> --html_text "<body>Hi <a data-asana-gid=\"<user_gid>\"/>...</body>" --ensure_followers <user_gid> --wait_ms 2500`

Plain text comments (`--text`) do **not** create real @-mentions via the API; they remain plain text.

## Attachments, uploads, and inline images

- Upload a file attachment to a task:

  `node {baseDir}/scripts/asana.mjs upload-attachment --parent <task_gid> --file /path/to/file.png`

- Embed an existing image attachment inline (tasks + project briefs only):

  `node {baseDir}/scripts/asana.mjs append-inline-image --attachment <attachment_gid> --task <task_gid>`

## Activity feed / “inbox-like” workflows

Asana does not provide a single universal “inbox” API for all notifications. The closest stable primitive is the **Events** endpoint scoped to a specific resource (project, task, etc.).

Use:
- `events --resource <gid>` to pull incremental changes on a project (or a user's "My Tasks" project)
- The command stores a sync token locally so subsequent runs fetch only changes

## Timeline shifting

- Shift one task (optionally include subtasks):

  `node {baseDir}/scripts/asana.mjs shift-task-dates <task_gid> --delta_days 7 --dry_run true`

- Shift an entire project’s tasks:

  `node {baseDir}/scripts/asana.mjs shift-project-tasks --project <project_gid> --delta_days -3 --dry_run true --all`

Run with `--dry_run true` first, then re-run with `--dry_run false`.

## Out of scope

- Portfolios (premium) are intentionally omitted.
- “Bot personality” is not embedded here; configure behavior in your agent prompt.
