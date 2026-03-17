---
name: pr
description: PR workflow - validate, branch, commit, push, PR, checkout main, rebase, squash merge. Use when submitting changes.
license: Apache-2.0
metadata:
  author: ahmadawais
  version: "0.0.1"
---

# PR Workflow

## Steps

1. **Validate**: `pnpm build`

2. **Branch**: Ask user or suggest (`fix/`, `feat/`, `refactor/`, `docs/`)
   ```bash
   git checkout -b {branch-name}
   ```

3. **Commit**: Stage specific files, use emoji-log format
   - `FIX:` | `NEW:` | `IMPROVE:` | `DOC:`
   ```bash
   git add {files} && git commit -m "$(cat <<'EOF'
   FIX: Description
   EOF
   )"
   ```

4. **Push**: `git push -u origin {branch}`

5. **PR**:
   ```bash
   gh pr create --title "FIX: Description" --body "$(cat <<'EOF'
   ## Summary
   - Changes

   ## Test plan
   - [ ] Tests
   EOF
   )"
   ```

6. **Main**: `git checkout main && git pull --rebase origin main`

7. **Merge**: Ask user, then:
   ```bash
   gh pr merge {number} --squash --delete-branch
   git pull --rebase origin main
   ```
