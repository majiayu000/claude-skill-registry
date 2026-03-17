---
name: update-gpui
description: Update GPUI submodule to the latest commit. Use when asked to update, bump, or upgrade the gpui dependency.
user_invocable: true
---

## Instructions

Update the GPUI git submodule and all related Cargo.toml references to the latest commit on `origin/main`.

### Steps

1. **Fetch latest from remote**:
   ```bash
   cd vendor/gpui && git fetch origin
   ```

2. **Identify target commit**: Use the latest commit on `origin/main` (or a specific commit/branch if the user provides one via `$ARGUMENTS`).
   ```bash
   git log --oneline origin/main -5
   ```

3. **Update submodule pointer**:
   ```bash
   git -C vendor/gpui checkout <commit-hash>
   ```

4. **Update `Cargo.toml`**: Find all `rev = "..."` entries pointing to the gpui git repo in the workspace `Cargo.toml` and update them to the new commit hash. The entries look like:
   ```toml
   gpui = { git = "https://github.com/BumpyClock/gpui", rev = "<old-hash>", ... }
   gpui_platform = { git = "https://github.com/BumpyClock/gpui", rev = "<old-hash>", ... }
   ```
   Update both `rev` values to the new short commit hash (first 10 chars).

5. **Build and verify**:
   ```bash
   cargo build
   ```

6. **If build fails**: Inspect errors and fix any breaking API changes in the codebase. Common issues:
   - Borrow checker issues from upstream tree-sitter/API changes
   - New/removed/renamed methods in gpui APIs
   - Changed trait signatures

7. **Run clippy**:
   ```bash
   cargo clippy -- --deny warnings
   ```

8. **Report summary**: Show old commit, new commit, what changed (list new commits), and whether build/clippy passed.

### Notes

- The submodule is at `vendor/gpui` and tracks `https://github.com/BumpyClock/gpui`.
- The `Cargo.toml` at the workspace root has `[workspace.dependencies]` entries for `gpui` and `gpui_platform` that pin to a specific `rev`.
- Always update both the submodule pointer AND the Cargo.toml rev in lockstep.
- If `$ARGUMENTS` contains a specific commit hash or branch, use that instead of `origin/main`.
