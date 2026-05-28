---
name: new-feature
description: Start a new feature by creating an isolated project copy. This is the high-level workflow that orchestrates fork-project and provides setup instructions.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# New Feature

High-level workflow to start working on a new feature in an isolated project copy.

## What it does

This is a **workflow** that orchestrates the `/fork-project` skill and provides complete setup instructions.

1. Runs the fork-project script to create an isolated copy
2. Shows the user exactly how to start working in the copy
3. Lists all currently active copies for reference

## Usage

```
/new-feature <feature-name>
```

Examples:
```
/new-feature auth-refactor
/new-feature new-dashboard
/new-feature fix-memory-leak
```

## How to execute

### Step 1: Create the fork

```bash
bash .claude/skills/fork-project/scripts/fork-project.sh "<feature-name>"
```

### Step 2: List active copies

After the fork is created, list all active copies so the user can see what's active:

```bash
PROJECT_DIR="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
PARENT_DIR="$(dirname "$PROJECT_DIR")"
echo "Active copies:"
ls -d "${PARENT_DIR}/${PROJECT_NAME}_copy_"* 2>/dev/null | while read -r dir; do
  echo "  - $(basename "$dir") -> $dir"
done
```

### Step 3: Provide next steps to the user

After everything completes, tell the user:

```
Feature copy ready!

To start working:
  1. Open a NEW terminal
  2. cd <copy-path>
  3. Run: claude

You now have a fully isolated environment. Work freely with any number of agents.

When done, return here and run:
  /finish-feature <feature-name>
```

## Important

- The feature name should be descriptive but short (used in directory and branch names)
- Each feature copy is fully isolated - agents in one copy cannot affect another
- You can have multiple features in progress simultaneously
- The copy is created in the parent directory of the current project
