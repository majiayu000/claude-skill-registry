---
name: dialogue-log-observation
description: Log an observation (measurement, state, or event). Use when recording factual observations during work execution. Triggers on "log observation", "record observation", "note finding", "capture state".
allowed-tools: Bash
---

# Dialogue: Observation Logger

Log an observation to the observation log.

## When to Use

Use this skill when you need to record:
- A measurement (quantitative data)
- A state observation (system/process state)
- An event (something that occurred)

## How to Log an Observation

Execute the following bash command:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-observation/scripts/log-observation.sh <type> <observer> <subject> <value> [context] [tags]
```

### Required Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `type` | `MEASUREMENT`, `STATE`, or `EVENT` | Category of observation |
| `observer` | `ai:claude` or `human:<id>` | Who made the observation |
| `subject` | text | Brief description of what was observed |
| `value` | text | The observed data, state, or event details |

### Optional Parameters

| Parameter | Description |
|-----------|-------------|
| `context` | Additional surrounding situation |
| `tags` | Comma-separated categorisation tags |

## Observation Types

| Type | Use For | Example |
|------|---------|---------|
| `MEASUREMENT` | Quantitative data | "3 tests failed, 47 passed" |
| `STATE` | System/process state | "Build pipeline is broken" |
| `EVENT` | Occurrences | "User requested code review" |

## Examples

### Measurement Observation
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-observation/scripts/log-observation.sh MEASUREMENT "ai:claude" "Test results" "3 failed, 47 passed" "After applying fix to auth module" "testing,ci"
```

### State Observation
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-observation/scripts/log-observation.sh STATE "ai:claude" "Build status" "Pipeline failing on lint stage" "Since commit abc123" "ci,blocking"
```

### Event Observation
```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-log-observation/scripts/log-observation.sh EVENT "ai:claude" "User action" "Requested implementation of feature X" "During planning session" "requirements"
```

## Output

The script returns the generated observation ID (e.g., `OBS-20260113-143000`).

## Sharing

**Always commit and push immediately after logging an observation.** This ensures team visibility and supports transactive memory—others need to see observations promptly to maintain shared situational awareness.

```bash
git add .dialogue/logs/observations/ && git commit -m "OBS-YYYYMMDD-HHMMSS: <subject>" && git push
```
