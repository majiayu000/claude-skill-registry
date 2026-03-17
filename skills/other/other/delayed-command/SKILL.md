---
argument-hint: <duration> <command>
context: fork
disable-model-invocation: false
name: delayed-command
user-invocable: true
description: This skill should be used when the user asks to "run npm test after 30 minutes", "git commit after 1 hour", "wait 2h then deploy", "sleep 45m and run build", "after 10m run prettier", or provides a duration followed by a shell command to execute later.
---

# Delayed Command Execution

Wait for a specified duration, then execute a Bash command.

## Arguments

- **duration**: Time to wait before execution (e.g., `30s`, `5m`, `1h`, `1h30m`)
- **command**: The Bash command to run after the delay

## Duration Format

| Format   | Example   | Meaning           |
| -------- | --------- | ----------------- |
| `Xs`     | `30s`     | 30 seconds        |
| `Xm`     | `5m`      | 5 minutes         |
| `Xh`     | `1h`      | 1 hour            |
| `XhYm`   | `1h30m`   | 1 hour 30 minutes |
| `XhYmZs` | `1h5m30s` | 1 hour 5 min 30 s |

## Workflow

### 1. Parse Duration

Convert the duration argument to seconds:

- Extract hours (`h`), minutes (`m`), and seconds (`s`) components
- Calculate total seconds: `hours * 3600 + minutes * 60 + seconds`

**Parsing logic:**

```bash
duration="$1"
seconds=0

# Extract hours
if [[ $duration =~ ([0-9]+)h ]]; then
  seconds=$((seconds + ${BASH_REMATCH[1]} * 3600))
fi

# Extract minutes
if [[ $duration =~ ([0-9]+)m ]]; then
  seconds=$((seconds + ${BASH_REMATCH[1]} * 60))
fi

# Extract seconds
if [[ $duration =~ ([0-9]+)s ]]; then
  seconds=$((seconds + ${BASH_REMATCH[1]}))
fi
```

### 2. Execute with Delay

For durations **up to 10 minutes** (600 seconds):

Run synchronously using the Bash tool with appropriate timeout:

```bash
sleep <seconds> && <command>
```

Set the Bash tool's `timeout` parameter to at least `(seconds + 60) * 1000` milliseconds.

For durations **over 10 minutes**:

Run in background using `run_in_background: true`:

```bash
sleep <seconds> && <command>
```

Inform the user the command is running in background and provide the task ID for checking status.

### 3. Report Result

After execution completes:

- Display command output
- Report exit status
- Note total elapsed time

## Examples

### Short Delay (Synchronous)

User: `/delayed-command 5m npm test`

1. Parse: 5 minutes = 300 seconds
2. Execute: `sleep 300 && npm test` (timeout: 360000ms)
3. Report test results

### Long Delay (Background)

User: `/delayed-command 1h git commit -m "auto-commit"`

1. Parse: 1 hour = 3600 seconds
2. Execute in background: `sleep 3600 && git commit -m "auto-commit"`
3. Return task ID for status checking

### Combined Duration

User: `/delayed-command 1h30m ./deploy.sh`

1. Parse: 1h30m = 5400 seconds
2. Execute in background (>600s): `sleep 5400 && ./deploy.sh`
3. Inform user of background task

## Error Handling

| Error                    | Response                                     |
| ------------------------ | -------------------------------------------- |
| Invalid duration format  | Show supported formats and examples          |
| Missing command argument | Prompt for the command to execute            |
| Command not found        | Report error after delay completes           |
| Duration exceeds 24h     | Warn user and suggest alternative (cron, at) |
