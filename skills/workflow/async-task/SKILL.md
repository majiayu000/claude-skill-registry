# OpenClaw Async Task

## Description

Execute long-running tasks without HTTP timeouts. Use when you need to:
- Run commands that may take more than 5 seconds
- Analyze large files or codebases
- Perform multi-step operations
- Call external APIs with unpredictable latency

**IMPORTANT**: When a task might timeout, you MUST use this skill to avoid `empty response from server` errors.

Triggers: "async task", "long running", "timeout", "background task", "push result"

## Installation

```bash
# Clone and link globally
git clone https://github.com/Enderfga/openclaw-async-task.git
cd openclaw-async-task
npm link

# Or just copy async-task.js to your PATH
chmod +x async-task.js
cp async-task.js /usr/local/bin/async-task
```

## Commands

```bash
async-task start "<description>"  # Start task, returns immediately
async-task done "<result>"        # Complete task, push result to user
async-task fail "<error>"         # Task failed, push error message
async-task push "<message>"       # Push message directly (no start needed)
async-task status                 # Show current task status
```

## Usage Flow (MUST follow strictly)

1. **Start**: `async-task start "Scanning files..."`
2. **Execute**: Run your actual commands
3. **Push result**: `async-task done "Found 42 files"`

## Example

User asks: "Count all TypeScript files in this project"

```bash
# Step 1: Acknowledge immediately
async-task start "Counting TypeScript files..."

# Step 2: Do the actual work
count=$(find . -name "*.ts" | wc -l)

# Step 3: Push the result
async-task done "Found $count TypeScript files"
```

## How It Works

1. `start` saves task state and returns confirmation immediately
2. You execute whatever commands needed
3. `done`/`fail` uses OpenClaw/Clawdbot CLI to push result to the active session

**Zero configuration required** - automatically detects active session via `openclaw sessions` or `clawdbot sessions`.

## Advanced: Custom Push Endpoint

For custom webchat or notification systems:

```bash
export ASYNC_TASK_PUSH_URL="https://your-server.com/api/push"
export ASYNC_TASK_AUTH_TOKEN="your-token"
```

The endpoint receives:
```json
{
  "sessionId": "session-id",
  "content": "message",
  "role": "assistant"
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENCLAW_SESSION` | No | Target session (auto-detected) |
| `ASYNC_TASK_PUSH_URL` | No | Custom HTTP push endpoint |
| `ASYNC_TASK_AUTH_TOKEN` | No | Auth token for custom endpoint |

## Requirements

- Node.js 16+
- OpenClaw or Clawdbot CLI installed

## Critical Rules

- **MUST** pair `start` with `done` or `fail`
- **NEVER** start without completing
- **NEVER** say "will push later" then forget

## Links

- [GitHub](https://github.com/Enderfga/openclaw-async-task)
- [OpenClaw](https://openclaw.ai)
