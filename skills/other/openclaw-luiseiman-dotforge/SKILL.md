---
name: forge
description: "dotforge configuration factory — audit, sync, status, insights across projects from any channel"
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["claude"],"env":["DOTFORGE_DIR"]}}}
---

# /forge — dotforge bridge for OpenClaw

Execute dotforge configuration management commands from any OpenClaw channel (WhatsApp, Telegram, Slack, etc.).

## How it works

This skill bridges OpenClaw to dotforge by running `claude` CLI in the target project directory. All `/forge` subcommands are available.

## Environment

- `DOTFORGE_DIR` — path to dotforge repo (required)
- Default project: uses `DOTFORGE_DIR` itself if no project specified

## Command format

```
/forge <command> [project:<name>]
```

If `project:<name>` is provided, look up the project path from `$DOTFORGE_DIR/registry/projects.yml` and execute in that directory.
If no project specified, use current context or ask the user.

## Available commands

### Read-only (safe from any channel)

| Command | What it does |
|---------|-------------|
| `status` | Multi-project dashboard with scores and trends |
| `version` | Show dotforge version |
| `pipeline` | Practices lifecycle status |
| `inbox` | List pending practices |

### Per-project (require project context)

| Command | What it does |
|---------|-------------|
| `audit` | Score project configuration 0-10 |
| `diff` | Show pending changes since last sync |
| `insights` | Analyze past sessions |
| `rule-check` | Detect inert rules |

### Mutation (ask for confirmation before executing)

| Command | What it does |
|---------|-------------|
| `sync` | Update project config against template |
| `bootstrap` | Initialize .claude/ in a project |
| `capture "text"` | Record a practice in inbox |
| `update` | Process practices pipeline |
| `watch` | Check for upstream changes |
| `scout` | Review curated repos |
| `reset` | Restore .claude/ from template |
| `benchmark` | Compare full vs minimal config |

## Execution

### Step 1: Parse command

Extract:
- `subcommand` — the forge action (audit, status, sync, etc.)
- `project` — optional project name from `project:<name>` suffix
- `args` — any remaining arguments

### Step 2: Resolve project path

If a project name is provided:

```bash
# Look up path from registry
python3 -c "
import yaml
reg = yaml.safe_load(open('$DOTFORGE_DIR/registry/projects.yml'))
for p in reg['projects']:
    if p['name'].lower() == '<project_name>'.lower():
        print(p['path'])
        break
"
```

If no project and command requires one, list available projects from registry and ask user to choose.

### Step 3: Execute

For read-only commands, execute directly:

```bash
cd <project_path>
claude --print "/forge <subcommand>" 2>&1
```

For mutation commands, show what will happen and ask for confirmation before executing.

### Step 4: Format response

Keep responses concise for mobile channels:
- Tables → use compact format
- Long outputs → summarize, offer "more details?" follow-up
- Scores → include emoji indicators (🟢 ≥9, 🟡 ≥7, 🔴 <7)
- Errors → show error + suggested fix

## Examples

User: `/forge status`
→ Execute `claude --print "/forge status"` in DOTFORGE_DIR
→ Return the multi-project dashboard

User: `/forge audit project:SOMA`
→ Look up SOMA path from registry
→ Execute `claude --print "/forge audit"` in SOMA directory
→ Return score + gaps

User: `/forge capture "hooks should validate JSON before writing settings.json"`
→ Execute `claude --print '/forge capture "hooks should validate JSON before writing settings.json"'` in DOTFORGE_DIR
→ Confirm: "Practice captured in inbox"

## Constraints

- NEVER run `sync`, `reset`, or `bootstrap` without explicit user confirmation
- NEVER expose file paths or system details in channel responses (security)
- If `claude` CLI is not available, respond: "Claude Code CLI not found. Install from https://docs.anthropic.com/en/docs/claude-code"
- If `DOTFORGE_DIR` is not set, respond: "Set DOTFORGE_DIR to your dotforge directory"
- Timeout: 60 seconds per command. If exceeded, report partial output.
