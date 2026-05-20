---
name: dev-buddy-once
description: Run a single task using a specific AI provider and model. Supports subscription, API, and CLI presets.
user-invocable: true
allowed-tools: Read, Bash, Task, TaskOutput, AskUserQuestion, Glob, Grep
---

# One-Shot Task Runner

Run a single arbitrary task using any configured AI provider — no pipeline, no reviews, no orchestration.

**Usage:** `/dev-buddy-once use <provider> [model <model>] <task description>`

**Examples:**
```
/dev-buddy-once use minimax M2.5 model to help me design a new UI
/dev-buddy-once use codex o3 model to refactor the auth module
/dev-buddy-once use anthropic-subscription sonnet model to explain the codebase
/dev-buddy-once use minimax to analyze performance bottlenecks
```

---

## Step 1: Parse Arguments

Extract three pieces from the user's message:
- **Provider name** — the preset name (e.g., "minimax", "codex", "anthropic-subscription")
- **Model** — the model identifier (e.g., "M2.5", "o3", "sonnet")
- **Task** — everything else (the actual work to do)

The user's message follows the skill trigger. Common patterns:
- `use <provider> <model> model to <task>`
- `use <provider> model <model> to <task>`
- `use <provider> to <task>` (model omitted — will default)

---

## Step 2: Resolve Preset

List available presets:

```bash
bun -e "
import { readPresets } from '${CLAUDE_PLUGIN_ROOT}/scripts/preset-utils.ts';
const presets = readPresets();
console.log(JSON.stringify(Object.entries(presets.presets).map(([k,v]) => ({
  name: k, type: v.type, models: v.models || ['haiku','sonnet','opus']
}))));
"
```

**Match the provider name deterministically:**
1. **Exact match** (case-insensitive) → use it
2. **Unique prefix match** (case-insensitive) → use it (e.g., "mini" matches "MiniMax-API" if no other preset starts with "mini")
3. **Multiple matches** → use AskUserQuestion listing the matches, ask user to pick
4. **No matches** → report error with available preset names

**Validate model:**
- If user specified a model, check it exists in the preset's `models[]` list
- If user did NOT specify a model:
  - Subscription presets: default to `sonnet`
  - API/CLI presets: default to `preset.models[0]`
- For subscription presets (no `models[]`), valid models are: `haiku`, `sonnet`, `opus`

---

## Step 3: Route by Provider Type

Read the matched preset's `type` field and route accordingly:

### Subscription (`type: "subscription"`)

Use the Task tool directly — no external process needed:

```
Task(
  subagent_type: "general-purpose",
  model: "<model>",
  prompt: "<task>"
)
```

The subagent works in the project directory with full tool access. Report its output to the user when it completes.

### API (`type: "api"`)

Run the one-shot runner script:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" \
  --type api \
  --preset "<exact_preset_name>" \
  --model "<model>" \
  --cwd "${CLAUDE_PROJECT_DIR}" \
  --task-stdin <<'TASK_EOF'
<task_text>
TASK_EOF
```

Uses `--task-stdin` with heredoc to avoid OS argv size limits and ps exposure.

**Derive timeout:** Read `~/.vcp/ai-presets.json` → find the preset by name → read `timeout_ms` (default: 300000 if not set or lookup fails).

**IMPORTANT:** The Bash tool has a hard max timeout of 600,000ms (10 min). API tasks can run much longer (e.g., 30 min). Always use `run_in_background: true` to prevent the Bash tool from killing the process prematurely.

After launching:
1. Save the returned `task_id` from the Bash tool. If `run_in_background` does not return a `task_id`, report a dispatch failure to the user — do not retry in foreground mode.
2. **CRITICAL — Poll with the correct timeout (NOT the default 30s):**
   ```
   TaskOutput(task_id: "<task_id>", block: true, timeout: min(timeout_ms + 120000, 600000))
   ```
   For a 5-min preset (default 300000ms), this = `min(420000, 600000)` = **420000ms (7 min)**.
   The default TaskOutput timeout is only 30s — far too short for API tasks that typically take 2-5 min.
3. If TaskOutput returns but the task is still running (not complete), repeat `TaskOutput` with `timeout: 600000` until done.

The script:
1. Spawns `api-task-runner.ts` with the preset, model, and task (via stdin)
2. The task runner creates a V2 Agent SDK session, runs the task, and exits
3. Outputs a JSON event to stdout

### CLI (`type: "cli"`)

**Prerequisite:** The CLI preset must have a `one_shot_args_template` configured. This template uses only `{model}`, `{prompt}`, and `{reasoning_effort}` placeholders (no `{output_file}` or `{schema_path}` — those are pipeline-only).

If the preset does not have `one_shot_args_template`, report the error to the user and suggest configuring it via `/dev-buddy-config` or `/dev-buddy-config`.

Run the one-shot runner script:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" \
  --type cli \
  --preset "<exact_preset_name>" \
  --model "<model>" \
  --cwd "${CLAUDE_PROJECT_DIR}" \
  --task-stdin <<'TASK_EOF'
<task_text>
TASK_EOF
```

**Derive timeout:** Read `~/.vcp/ai-presets.json` → find the preset by name → read `timeout_ms` (default: 1200000 for CLI if not set or lookup fails — matches the script's 20-minute default).

**IMPORTANT:** The Bash tool has a hard max timeout of 600,000ms (10 min). CLI tasks can run much longer (e.g., Codex with 20-min timeout). Always use `run_in_background: true` to prevent the Bash tool from killing the process prematurely.

After launching:
1. Save the returned `task_id` from the Bash tool. If `run_in_background` does not return a `task_id`, report a dispatch failure to the user — do not retry in foreground mode.
2. **CRITICAL — Poll with the correct timeout (NOT the default 30s):**
   ```
   TaskOutput(task_id: "<task_id>", block: true, timeout: min(timeout_ms + 120000, 600000))
   ```
   For a 20-min CLI preset (default 1200000ms), this = `min(1320000, 600000)` = **600000ms (10 min)**.
   The default TaskOutput timeout is only 30s — far too short for CLI tasks that typically take 5-20 min.
3. If TaskOutput returns but the task is still running (not complete), repeat `TaskOutput` with `timeout: 600000` until done.

The CLI tool runs directly in the project directory (e.g., Codex `exec --full-auto`). Its output streams to the terminal.

---

## Step 4: Report Results

After the task completes, read the script's stdout JSON output:

### Success (exit code 0)
```json
{"event": "complete", "provider": "minimax", "model": "M2.5", "result": "..."}
```

Report: provider, model used, and a summary of what was accomplished.

### Validation Error (exit code 1)
```json
{"event": "error", "phase": "validation", "error": "..."}
```

Report the validation error (wrong model, missing preset, bad template).

### Execution Error (exit code 2)
```json
{"event": "error", "phase": "api_execution|cli_execution", "error": "..."}
```

Report what went wrong (session failure, CLI not installed, auth error).

### Timeout (exit code 3)
```json
{"event": "error", "phase": "api_execution|cli_execution", "error": "..."}
```

Report that the task timed out. Suggest increasing `timeout_ms` on the preset via `/dev-buddy-config`.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Preset not found | List available presets, suggest `/dev-buddy-config list` |
| Model not in preset | List preset's available models |
| Multiple preset matches | AskUserQuestion with matching names |
| CLI preset missing `one_shot_args_template` | Report error, suggest `/dev-buddy-config` or `/dev-buddy-config` to add it |
| CLI tool not installed | Report error, suggest installing the tool |
| API task runner fails | Report error from script output |
| Task times out | Report timeout, suggest increasing `timeout_ms` |

---

## Anti-Patterns

- Do NOT run a full pipeline — this is a single one-shot task
- Do NOT create pipeline tasks (TaskCreate/TaskUpdate) — no orchestration needed
- Do NOT skip the preset resolution step — always validate provider and model first
- Do NOT guess the preset type — always read it from the presets file
- For subscription: do NOT run the one-shot-runner.ts script — use Task tool directly
- Do NOT fall back to foreground Bash when background TaskOutput returns empty — the task is likely still running. Increase the TaskOutput timeout instead.
- Do NOT retry the same API/CLI task in foreground mode — the Bash tool's 2-minute default timeout is always shorter than the typical task duration (2-5 min for API, 5-20 min for CLI). Foreground mode will always kill the process prematurely.
- Do NOT use the default TaskOutput timeout (30s) for API/CLI tasks — always pass the computed timeout as specified in the polling instructions above.
