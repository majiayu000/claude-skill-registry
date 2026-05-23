---
name: init-session
description: Initialize Contextium session state and verify environment
allowed-tools: Bash, Read, Write
---

# Session Initializer

Initialize the Contextium session environment.

## Execution

Run the initializer agent:

```bash
./agents/initializer.sh
```

## What It Does

1. **Creates state directory** (`.contextium/`)
2. **Verifies tools** - git, jq, and optional Contextium tools
3. **Initializes state.json** - Session ID, repo info, branch
4. **Initializes tasks.json** - Empty task list if not present
5. **Checks git status** - Branch, uncommitted changes

## Output

The initializer outputs a session summary:
```
Session ID: <timestamp>-<pid>
Repository: <repo-name>
Branch: <current-branch>
Status: initialized
```

## Manual State Reset

To reset session state:
```bash
rm -rf .contextium/state.json
./agents/initializer.sh
```
