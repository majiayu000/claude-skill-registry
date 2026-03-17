---
name: "cd-permanent"
description: "Change directory permanently within the session (project tree only)"
argument-hint: "[path]"
---

## Instructions

### Step 1: Parse and Validate Path

Parse `$ARGUMENTS` as the target path.

If empty: Show usage: `/cd-permanent <path>`

### Step 2: Check if Path is Within Project

```bash
# Get project root and target real path
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
TARGET_PATH=$(realpath -m "$ARGUMENTS" 2>/dev/null || echo "$ARGUMENTS")
```

Check if `$TARGET_PATH` starts with `$PROJECT_ROOT`:
- If YES: Continue to Step 3
- If NO: Continue to Step 4

### Step 3: Change Directory (Within Project)

```bash
cd "$TARGET_PATH"
pwd
```

Confirm: "Changed directory to: [new path]"

### Step 4: Outside Project

Cannot change directory outside the project tree. Claude Code enforces staying within the base directory where the session started.
