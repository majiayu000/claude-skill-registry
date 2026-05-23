---
name: clean-project
description: Perform a "hard reset" of the development environment. Use when dependencies are corrupted, lockfiles are out of sync, or environment tools (Trunk/pnpm) are in an inconsistent state.
---

# Clean Project (Hard Reset)

This skill provides a destructive but thorough way to repair a "broken" development environment by removing all cached artifacts and re-initializing from scratch.

## When to Use

- `pnpm install` fails repeatedly with checksum or resolution errors.
- `trunk` reports internal errors that persist after `trunk install`.
- "Ghost" errors occur (failures that don't match the current code).

## Workflow

1. **Clean Dependencies**:
   - Recursively delete `node_modules`: `find . -name "node_modules" -type d -prune -exec rm -rf '{}' +`.
   - Remove global lockfile: `rm pnpm-lock.yaml`.

2. **Clean Tooling Cache**:
   - Clear Trunk cache: `trunk clean`.
   - Prune pnpm store: `pnpm store prune`.

3. **Re-initialize Environment**:
   - Invoke the `setup-dev-env` skill to reinstall everything.

4. **Verify Health**:
   - Invoke the `verifier` subagent ([../../agents/verifier.md](../../agents/verifier.md)) to ensure the project is back to a clean, working state.

## Safety Note

This process is destructive to the local environment but safe for the repository. It will require a full download of all dependencies, which may take several minutes depending on network speed.

## Resources

- [pnpm Commands for Node.js](../common-references/pnpm-commands.md): Common pnpm maintenance commands.
- [Trunk CLI Reference](../common-references/trunk-commands.md): Commands for managing Trunk artifacts.
