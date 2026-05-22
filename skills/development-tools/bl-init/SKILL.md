---
name: bl-init
description: Initialize git-branchless in the current repository from the current branch
argument-hint: "[--main-branch <branch>] [--no-detach]"
---

# /bl-init - Git-Branchless Repository Initialization

**Category:** Git Workflow

Initialize git-branchless in the current repository, using the current branch as the main branch by default. Automatically detaches HEAD so you're ready to start stacking commits.

## Usage

```
/bl-init [options]
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Initialize using current branch as main, then detach HEAD |
| `--main-branch <branch>` | Specify a different branch as main |
| `--no-detach` | Initialize without detaching HEAD |

## Examples

```bash
# Initialize with current branch as main
/bl-init

# Initialize with a specific branch as main
/bl-init --main-branch develop
```

## Execution

This command delegates to the `bl-init-expert` agent:

```
Task(subagent_type="git-workflow:bl-init-expert",
     prompt="Initialize git-branchless: <options>")
```

## Execution Instructions

1. **Check Prerequisites**
   - Verify this is a git repository
   - Check if git-branchless is installed
   - Check if already initialized

2. **Determine Main Branch**
   - Use current branch if no `--main-branch` specified
   - Validate the branch exists

3. **Initialize Git-Branchless**
   - Run `git branchless init --main-branch <branch>`
   - Configure recommended settings

4. **Detach HEAD** (unless `--no-detach`)
   - Run `git checkout --detach`
   - This prepares you for the stacked commits workflow

5. **Verify Installation**
   - Run `git sl` to confirm working
   - Show current state with detached HEAD

6. **Provide Next Steps**
   - Explain basic commands (`git sl`, `git sync`, `git submit`)

## Interactive Flow

```
User: /bl-init

Agent: Initializing git-branchless...

Current branch: main
Repository: /path/to/project

Checking prerequisites...
✓ Git repository detected
✓ git-branchless is installed (v0.9.0)
✗ Not yet initialized

Initializing with main branch: main

$ git branchless init --main-branch main
Created config file at .git/branchless/config
Installed hooks at .git/hooks/
branchless: processing 1 update: main

Detaching HEAD for stacked workflow...
$ git checkout --detach

✓ Git-branchless initialized successfully!

Current state:
◆ abc1234 (main) Latest commit message
┃
● abc1234 (HEAD)  ← You are here (detached)

Ready to stack commits! Next steps:
1. Use `git record -m "msg"` to create commits
2. Use `git sl` to see your commit stack
3. Use `git sync --pull` to sync with remote
4. Use `git submit` to create/update PRs
```

```
User: /bl-init
(already initialized)

Agent: Checking git-branchless status...

✓ Git-branchless is already initialized in this repository.

Current main branch: main
Config file: .git/branchless/config

Current state:
◆ abc1234 (main) Latest commit
┃
◯ def5678 Your feature commit

To reinitialize with different settings:
1. Remove: rm -rf .git/branchless .git/hooks/post-*
2. Run: /bl-init again
```

```
User: /bl-init --main-branch develop

Agent: Initializing git-branchless with develop as main...

$ git branchless init --main-branch develop
Created config file at .git/branchless/config
Installed hooks at .git/hooks/
branchless: processing 1 update: develop

Detaching HEAD for stacked workflow...
$ git checkout --detach

✓ Git-branchless initialized with main branch: develop
```

```
User: /bl-init --no-detach

Agent: Initializing git-branchless (without detaching)...

$ git branchless init --main-branch main
Created config file at .git/branchless/config
Installed hooks at .git/hooks/
branchless: processing 1 update: main

✓ Git-branchless initialized successfully!

Current state:
◆ abc1234 (main) Latest commit message

Note: HEAD is still attached to main.
When ready to stack commits, run: git checkout --detach
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Not a git repository | Run `git init` first |
| git-branchless not installed | Install with `brew install git-branchless` or `cargo install git-branchless` |
| Branch does not exist | List available branches, suggest correct one |
| Already initialized | Show current config, offer reinit instructions |
