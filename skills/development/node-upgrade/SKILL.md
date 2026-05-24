---
name: node-upgrade
description: Safely upgrade Node.js dependencies in pnpm workspaces. Use when asked to "upgrade dependencies", "update packages", "check for updates", or fix version mismatches.
---

# Safe Node.js Dependency Upgrade

This skill provides a structured process for safely upgrading Node.js dependencies, ensuring project stability through pre-upgrade health checks and post-upgrade validation.

## 1. Preparation & Health Check

Before making any changes, verify the current state of the project:

1. **Baseline Health Check**:
   - Run an audit: `pnpm audit`.
   - Run the test suite: `pnpm test`.
   - _Constraint_: If the baseline tests fail, resolve those issues before proceeding with upgrades.
2. **Backup**:
   - Backup `package.json` and the lockfile: `cp pnpm-lock.yaml pnpm-lock.yaml.bak`.

## 2. Upgrade Execution

Choose the appropriate upgrade path based on the user's request. Refer to [../common-references/pnpm-commands.md](../common-references/pnpm-commands.md) for pnpm-specific commands.

### Targeted Upgrade (Recommended)

Use this when the user specifies a package or a small set of packages.

1. **Upgrade**: Run the targeted upgrade command (e.g., `pnpm update <package>`).
2. **Verify**: Check `package.json` to ensure the version has been updated.

### Full Upgrade (Maintenance)

Use this for general dependency maintenance.

1. **Upgrade**: Run the full upgrade command (e.g., `pnpm update`).
2. **Check for Breaking Changes**: Review the lockfile changes and check for major version bumps.

## 3. Validation & Verification

After the upgrade, ensure the project remains stable by delegating to the project verifier:

1. **Invoke Verifier**: Use the `verifier` subagent ([../../agents/verifier.md](../../agents/verifier.md)) to run the full build, lint, and test cycle.
2. **Handle Failure**: If the `verifier` reports persistent issues it cannot fix, analyze the breaking changes and apply manual fixes or roll back.
3. **Final Audit**: Once the verifier passes, run `pnpm audit` again to ensure no new vulnerabilities were introduced.

## 4. Finalization

1. **Commit**: Create a commit with the updated `package.json` and lockfile.
   - _Message Suggestion_: `chore(deps): upgrade dependencies`
2. **Cleanup**: Remove backup files: `rm *.bak`.

## Rollback Plan

If validation fails and cannot be easily fixed:

1. **Restore**: `mv package.json.bak package.json` and `mv <lockfile>.bak <lockfile>`.
2. **Re-install**: Run `pnpm install` to restore the environment.
3. **Report**: Notify the user of the failure and the reasons (e.g., specific breaking changes).
