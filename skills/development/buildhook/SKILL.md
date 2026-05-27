---
name: BuildHook
description: "Create and validate module hooks. USE WHEN create hook, new hook, write hook, scaffold hook, validate hook, check hook, hook conventions, hook events, hook structure."
version: 0.1.0
---

# BuildHook

Create and validate hook scripts for forge modules. Hooks are bash scripts triggered by Claude Code events, routed through the `dispatch` binary.

## Workflow Routing

| Workflow | Trigger | Section |
|----------|---------|---------|
| **Create** | "create hook", "new hook", "scaffold hook" | [Create Workflow](#create-workflow) |
| **Validate** | "validate hook", "check hook" | [Validate Workflow](#validate-workflow) |

## Hook Conventions

### Events and Output Modes

Every hook handles one of 9 Claude Code events. Each event has a fixed output mode that determines how module output is handled:

| Event | Mode | Behaviour |
|-------|------|-----------|
| `SessionStart` | Concatenate | All module outputs combined and emitted to AI context |
| `PreCompact` | Concatenate | All module outputs combined and emitted to AI context |
| `PreToolUse` | Gate | Exit 2 blocks the tool call; exit 0 allows |
| `Stop` | Gate | Exit 2 blocks session exit; exit 0 allows |
| `SubagentStop` | Gate | Exit 2 blocks subagent exit; exit 0 allows |
| `PostToolUse` | Passive | Output discarded; runs for side effects only |
| `SessionEnd` | Passive | Output discarded; runs for side effects only |
| `UserPromptSubmit` | Passive | Output discarded; runs for side effects only |
| `Notification` | Passive | Output discarded; runs for side effects only |

### Output Mode Decision Table

Use this when choosing which event to hook:

| Goal | Event | Mode | Notes |
|------|-------|------|-------|
| Inject context at session start | `SessionStart` | Concatenate | Emit markdown to stdout |
| Block a tool call (access control) | `PreToolUse` | Gate | Exit 2 to block, 0 to allow |
| Enforce rules before exit | `Stop` | Gate | Exit 2 to block, 0 to allow |
| React to a tool result | `PostToolUse` | Passive | Side effects only, output discarded |
| Clean up after session | `SessionEnd` | Passive | Side effects only, output discarded |
| Inject context before compaction | `PreCompact` | Passive | Emit markdown to stdout |

### File Naming

Hook scripts use **PascalCase** matching the event name:

| Event | Filename |
|-------|----------|
| `SessionStart` | `hooks/SessionStart.sh` |
| `PreToolUse` | `hooks/PreToolUse.sh` |
| `PostToolUse` | `hooks/PostToolUse.sh` |
| `Stop` | `hooks/Stop.sh` |
| `PreCompact` | `hooks/PreCompact.sh` |

### Dual-Mode Preamble

Every hook script starts with this template. It resolves the module root from either forge-core dispatch or standalone plugin context:

```bash
#!/usr/bin/env bash
set -euo pipefail

MODULE_ROOT="${FORGE_MODULE_ROOT:-${CLAUDE_PLUGIN_ROOT:-$(command cd "$(dirname "$0")/.." && pwd)}}"
```

### Stdin JSON

Claude Code pipes a JSON payload to hook scripts on stdin. The schema varies by event:

- **PreToolUse / PostToolUse**: `{"tool_name":"...", "tool_input":{...}}`
- **Stop**: `{"stop_reason":"...", ...}`
- **SessionStart**: empty or `{}`

Read stdin once: `INPUT=$(cat)`. Parse with `yq -p json` or a compiled binary.

### Registration Chain

For dispatch to find a hook:

1. Hook file exists at `hooks/<EventName>.sh` and is executable
2. `module.yaml` lists the event in `events:` (Tier 1 check)
3. Module is listed in project `defaults.yaml` under `modules:` (Tier 0)

The 3-tier event check: `config.yaml` override (authoritative) > `module.yaml` events > hook file existence (fallback).

### Exit Code Conventions

| Mode | Exit 0 | Exit 2 | Other |
|------|--------|--------|-------|
| Gate | Allow | Block | Treated as allow |
| Concatenate | Success | N/A | Output included regardless |
| Passive | Success | N/A | Output discarded regardless |

Gate hooks that cannot build or run should exit 0 (graceful degradation — never block Claude on infrastructure failure).

---

## Create Workflow

### Step 1: Determine event and output mode

Ask the user:
1. What should trigger this hook? (Use the Output Mode Decision Table above)
2. What should the hook do? (Inject context, block an action, or run a side effect?)

### Step 2: Scaffold the hook script

Create `hooks/<EventName>.sh` with:

```bash
#!/usr/bin/env bash
# <EventName> hook: <brief description>.
set -euo pipefail

MODULE_ROOT="${FORGE_MODULE_ROOT:-${CLAUDE_PLUGIN_ROOT:-$(command cd "$(dirname "$0")/.." && pwd)}}"

INPUT=$(cat)

# Gate: exit 2 to block, 0 to allow | Concatenate: emit context to stdout
```

For Gate hooks, add exit code logic. For Passive hooks, add the side effect. For Concatenate hooks, emit context to stdout.

Make the script executable: `chmod +x hooks/<EventName>.sh`

### Step 3: Register the event

Add the event to `module.yaml`:
```yaml
events:
  - <EventName>
```

### Step 4: Add standalone hooks.json entry (optional)

If the module also works as a standalone Claude Code plugin, add the event to `hooks/hooks.json`:
```json
{
  "hooks": {
    "<EventName>": [
      {"hooks": [{"type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/<EventName>.sh"}]}
    ]
  }
}
```

### Step 5: Add hook config to defaults.yaml (optional)

If the hook needs configurable settings:
```yaml
hooks:
    HookName:
        key: value
```

Read with `yq '.hooks.HookName.key' "$MODULE_ROOT/defaults.yaml"`. Override via `config.yaml`.

### Step 6: Verify

Run the hook manually to test:
```bash
echo '{"tool_name":"TestTool"}' | bash hooks/<EventName>.sh
```

---

## Validate Workflow

### Step 1: Read the target hook

Read the hook script and `module.yaml`.

### Step 2: Check structure

- [ ] File exists at `hooks/<EventName>.sh`
- [ ] File is executable (`chmod +x`)
- [ ] Starts with `#!/usr/bin/env bash`
- [ ] Has `set -euo pipefail`
- [ ] Dual-mode MODULE_ROOT resolution present
- [ ] Uses `command` prefix for `cd`, `cp`, `mv`, `rm`

### Step 3: Check registration

- [ ] Event listed in `module.yaml` `events:` array
- [ ] Module listed in project `defaults.yaml` `modules:` array
- [ ] If standalone: `hooks/hooks.json` references correct filename

### Step 4: Check output mode compliance

- [ ] Gate hooks: uses exit 2 to block, exit 0 to allow
- [ ] Gate hooks: exits 0 on build/infrastructure failure (graceful degradation)
- [ ] Concatenate hooks: emits useful markdown to stdout
- [ ] Passive hooks: does not depend on stdout being visible

### Step 5: Report

**COMPLIANT** -- all checks pass.

**NON-COMPLIANT** -- list failures with specific fixes. Offer to fix automatically.

## Constraints

- Hook filenames MUST use PascalCase matching the event name: `SessionStart.sh`, not `session-start.sh`
- Shell scripts MUST use `set -euo pipefail` and `command` prefix for aliased commands
- Gate hooks MUST exit 0 on infrastructure failure — never block Claude due to a broken hook
- Stdin is consumed once — read it into a variable (`INPUT=$(cat)`) before processing
- Output is mode-dependent — Passive hooks cannot communicate back to the AI
