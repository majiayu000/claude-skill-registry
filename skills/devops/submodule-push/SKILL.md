---
name: submodule-push
description: Push submodule changes to its fork. Use when you've made changes inside a submodule (hive or core-geth) and need to push them.
argument-hint: "[submodule-name]"
disable-model-invocation: true
---

# Push Submodule Changes

Push changes from a submodule to its remote fork.

## Arguments

- `$0`: Submodule name (`hive` or `core-geth`)

## Authorized Repositories

These are the forks we can push to:

- `IstoraMandiri/hive` (Hive fork)
- `IstoraMandiri/core-geth` (core-geth fork)

## Workflow

1. Navigate into the submodule directory specified by `$0`
2. Check git status to confirm there are commits to push
3. Determine the current branch name
4. Push to origin: `git push -u origin <branch>`
5. Return to the parent directory
6. Remind user to update the parent repo's submodule reference if needed:
   ```bash
   git add $0
   git commit -m "Update $0 submodule reference"
   ```

## Example Usage

```
/submodule-push hive
/submodule-push core-geth
```
