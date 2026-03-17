---
name: setup-hooks
description: Set up common Claude Code hooks - auto-formatting after edits, blocking dangerous commands, and notifications. Interactive setup for your project.
disable-model-invocation: true
---

# Setup Hooks

Configure Claude Code hooks for your project. Hooks are deterministic automation that runs before or after Claude's tool calls.

## Usage

`/setup-hooks`

## Background

Claude Code supports these hook events:
- **PreToolUse**: Runs BEFORE a tool call. Can block the call.
- **PostToolUse**: Runs AFTER a tool call completes.
- **Notification**: Runs when Claude sends a notification.
- **Stop**: Runs when Claude finishes its turn.

Hooks are configured in `.claude/settings.json` under the `hooks` key.

## Procedure

### Step 1: Present Hook Options

Show the user available hook patterns:

```
Which hooks would you like to set up?

1. Auto-format after edits — Runs your formatter after every file edit
2. Block dangerous commands — Prevents rm -rf, git push --force, etc.
3. Lint on save — Runs your linter after every file write
4. Custom hook — Define your own

Select one or more (e.g., "1,2"):
```

### Step 2: Configure Selected Hooks

#### Hook 1: Auto-Format After Edits

1. Detect the project's formatter (see detection logic below)
2. Create a PostToolUse hook for the `Edit` and `Write` tools:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "[formatter-command] $CLAUDE_FILE_PATH",
        "timeout": 10000
      }
    ]
  }
}
```

**Formatter detection:**
- Node.js: Check for `prettier` → `npx prettier --write`
- Node.js: Check for `biome` → `npx biome format --write`
- Python: Check for `ruff` → `ruff format`
- Python: Check for `black` → `black`
- Rust: `cargo fmt --`
- Go: `gofmt -w`

#### Hook 2: Block Dangerous Commands

Create a PreToolUse hook for the `Bash` tool:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "node .claude/hooks/block-dangerous.js",
        "timeout": 5000
      }
    ]
  }
}
```

Create the blocking script at `.claude/hooks/block-dangerous.js`:

```javascript
// Block dangerous commands in Claude Code
// Reads tool input from stdin, exits non-zero to block

const fs = require('fs');
const input = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
const cmd = input.tool_input?.command || '';

const BLOCKED_PATTERNS = [
  /rm\s+-rf\s+[\/~]/,           // rm -rf with absolute or home path
  /git\s+push\s+.*--force/,     // force push
  /git\s+reset\s+--hard/,       // hard reset
  /drop\s+table/i,              // SQL drop table
  /drop\s+database/i,           // SQL drop database
  />\s*\/dev\/sd/,              // writing to block devices
  /mkfs\./,                     // formatting filesystems
  /dd\s+if=/,                   // disk destroyer
];

for (const pattern of BLOCKED_PATTERNS) {
  if (pattern.test(cmd)) {
    console.error(`BLOCKED: Command matches dangerous pattern: ${pattern}`);
    process.exit(1);
  }
}

process.exit(0);
```

**Note for Windows**: The script above uses Unix conventions. On Windows, adjust stdin reading:
```javascript
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
```

#### Hook 3: Lint on Save

Similar to auto-format, but runs the linter:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "[lint-command] $CLAUDE_FILE_PATH",
        "timeout": 15000
      }
    ]
  }
}
```

### Step 3: Install Hooks

1. Read the current `.claude/settings.json`
2. Merge the new hooks into the existing configuration (don't overwrite existing hooks)
3. Write the updated settings file
4. If the dangerous-command hook was selected, create the `.claude/hooks/` directory and script

### Step 4: Verify

Tell the user the hooks are installed and how to test them:

```
Hooks installed successfully!

To verify:
- Auto-format: Edit any file and check it gets formatted
- Block dangerous: Try running `rm -rf /` (it will be blocked)
- Lint on save: Write a file and check for lint output

To view all hooks: /hooks
To disable: Remove the hook entry from .claude/settings.json
```
