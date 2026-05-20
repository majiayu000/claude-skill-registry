---
name: noir-sync-update
description: Perform necessary follow-on updates as a result of updating the noir git submodule.
---

# Noir Sync Update

## Steps

After each step, verify with `git status` and commit the results before proceeding.

## Critical Verification Rules

**ALWAYS verify file changes with `git status` after any modification step before marking it complete.** Command output showing "updating" does not guarantee the file was written to disk.

**IMPORTANT:** Always run `git status` from the repository root directory, not from subdirectories. Running `git status noir-projects/` from inside `noir-projects/` will fail silently.

### 1. Ensure submodule is pulled

Run `./bootstrap.sh` in `noir` to ensure that the new submodule commit has been pulled. This shouldn't produce changes that need committing.

### 2. Update `Cargo.lock` in `avm-transpiler`

**Before updating**, determine the expected noir version:
1. Read `noir/noir-repo/.release-please-manifest.json` to find the expected version (e.g., `1.0.0-beta.18`)
2. Check the current version in `avm-transpiler/Cargo.lock` by searching for `acir` or similar noir packages

**To update the lock file**, run `cargo update` in `avm-transpiler` with **only noir-repo packages**:

```bash
cd avm-transpiler
cargo update -p acir -p acir_field -p acvm -p acvm_blackbox_solver -p bn254_blackbox_solver -p brillig -p brillig_vm -p fm -p iter-extended -p noirc_abi -p noirc_arena -p noirc_artifacts -p noirc_errors -p noirc_evaluator -p noirc_frontend -p noirc_printable_type -p noirc_span
```

**IMPORTANT:** Do NOT use `cargo update` without `-p` flags—this will update ALL dependencies, not just noir-repo packages.

**After updating**, verify:
1. Run `git status avm-transpiler/` to confirm `Cargo.lock` was modified
2. Run `cargo check` to ensure it still builds
3. Grep `Cargo.lock` for `acir` to verify the version matches the expected version from `.release-please-manifest.json`

It's possible that changes in dependencies result in `avm-transpiler` no longer building.
  - If transient dependency mismatches mean changes to the dependency tree are necessary, then the `Cargo.lock` file in `avm-transpiler` should be modified. **DO NOT MODIFY `noir/noir-repo`**.
  - If updates are necessary due to changes in exports from `noir/noir-repo` packages, then perform the necessary updates to import statements, etc.

### 3. Update `yarn.lock` in `yarn-project`

Run `yarn install` in `yarn-project` to update the `yarn.lock` file.

**After running**, verify with `git status yarn-project/yarn.lock` that the file was modified before committing.

### 4. Format `noir-projects`

Run `./bootstrap.sh format` in `noir-projects`.

This is necessary as the updates to the noir compiler may result in the formatter handling the same code differently.

Failing to run the formatter will result in a CI failure.

**After running**, check `git status noir-projects/` for any formatting changes that need to be committed.
