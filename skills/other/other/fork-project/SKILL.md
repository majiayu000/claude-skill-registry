---
name: fork-project
description: Create an isolated copy of the current project for parallel feature development. Use when the user wants to work on a feature in isolation with multiple agents.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Fork Project

Creates a fully isolated copy of the current project for parallel development.

## What it does

1. **Clones** the project to `../<projectName>_copy_<feature-name>/` using `git clone --no-hardlinks` (fully isolated `.git`)
2. **Creates** branch `work/<feature-name>` in the copy
3. **Installs** dependencies (`pnpm install`)
4. **Reports** the path and next steps

## Usage

```
/fork-project <feature-name>
```

## How to execute

Run the fork script:

```bash
bash .claude/skills/fork-project/scripts/fork-project.sh "<feature-name>"
```

Where `<feature-name>` is the name provided by the user (e.g., `auth-refactor`, `new-dashboard`, `fix-perf`).

## Important

- The copy is created in the **parent directory** of the current project
- The copy has a **completely isolated `.git`** - no shared state with the original
- The original project remote is removed from the copy to prevent accidental pushes
- Always inform the user of the full path to the copy so they can open Claude Code there
