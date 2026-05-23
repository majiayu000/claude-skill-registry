---
description: Download or stream agent logs from GKE. Accepts issue number, session ID, or --all. Default mode downloads JSONL to tmp/agent-logs/.
user_invocable: true
argument_description: "<target> [--stream] [--all] [--thinking] [--raw]"
---

Download or stream agent execution logs from GKE Autopilot K8s Jobs.

The argument `$ARGUMENTS` can be:
- An issue number (e.g. `714`) — finds the latest job for that issue
- A session ID (e.g. `issue-714-step1-firemandecko-3a19c027`) — direct lookup
- `--all` or `all` — all active agent jobs
- `--help` — show usage

## Modes

| Mode | Flag | Behavior |
|------|------|----------|
| **Download** (default) | *(none)* or `--download` | Downloads raw JSONL to `tmp/agent-logs/<session>.jsonl`. Skips if file already exists with content (never clobbers). |
| **Stream** | `--stream` | Streams parsed, color-coded logs in a tmux pane. |

## Instructions

1. If `$ARGUMENTS` is `--help`, display usage and stop — do not run any commands.

2. Parse `$ARGUMENTS` to determine the target and mode:
   - Strip `#` prefix if present
   - If it looks like a session ID (`issue-N-stepS-agent-uuid`), use directly
   - If it's a number, resolve to the latest job via `--issue`
   - If `--all` or `all`, use the --all flow below
   - If `--stream` is present, use stream mode; otherwise default to download mode

### Download mode (default)

3. **For a single target** — download directly:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
node "$REPO_ROOT/infrastructure/k8s/agents/agent-logs.mjs" <target>
```

4. **For `--all`** — download all active jobs:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
kubectl get jobs -n fenrir-agents \
  -o jsonpath='{range .items[?(@.status.active)]}{.metadata.name}{"\n"}{end}' | \
while read job; do
  [ -z "$job" ] && continue
  sid="${job#agent-}"
  node "$REPO_ROOT/infrastructure/k8s/agents/agent-logs.mjs" "$sid"
done
```

5. Report back:
```
Downloaded N agent logs to tmp/agent-logs/
```
Or if no active agents: "No active agent jobs found."

### Stream mode (`--stream`)

3. **For a single target** — spawn one tmux pane:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
node "$REPO_ROOT/infrastructure/k8s/agents/agent-logs.mjs" stream <target> --tools --spawn-pane
```

4. **For `--all`** — get all active jobs and spawn a pane for EACH one using `--spawn-pane`:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
kubectl get jobs -n fenrir-agents \
  -o jsonpath='{range .items[?(@.status.active)]}{.metadata.name}{"\n"}{end}' | \
while read job; do
  [ -z "$job" ] && continue
  sid="${job#agent-}"
  node "$REPO_ROOT/infrastructure/k8s/agents/agent-logs.mjs" stream "$sid" --tools --spawn-pane
done
```

**IMPORTANT:** Do NOT use `--all --tmux` — that blocks the current process. Always loop
with `--spawn-pane` so each agent gets its own non-blocking tmux pane.

5. Report back:
```
Streaming N active agents in tmux panes
```
Or if no active agents: "No active agent jobs found."

## Additional flags (pass through from $ARGUMENTS)

- `--thinking` — include thinking blocks (stream mode)
- `--no-follow` — dump existing logs, don't stream
- `--raw` — show raw JSONL
- `--verbose` — alias for --tools (stream mode)
