---
name: 'Finish Work'
description: 'Run quality gates, commit changes, push branch, and create a pull request.'
---

1. **Run quality gates**: Execute each check and fix any failures before proceeding.
   ```bash
   pnpm lint:affected
   pnpm ts:affected
   pnpm test:affected
   ```

2. **Fix failures**: If any check fails, fix the issue and re-run. Do not skip or ignore failures.

3. **Stage and commit**:
   - Run `git status` and `git diff` to review changes
   - Stage specific files by name (never use `git add .` or `git add -A`)
   - Write a conventional commit message: `<type>(<scope>): <description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `revert`
   - Scopes: `nx`, `rule`, `shared`, `script`

4. **Push the branch**: Run `git push -u origin <branch-name>` to push and set the upstream.

5. **Create the pull request**:
   ```bash
   gh pr create \
     -a @me \
     -r @carrot-foundation/developers \
     --label <label> \
     -R carrot-foundation/methodology-rules \
     -t "<type>(<scope>): <title>"
   ```
   - Labels: `feature`, `bug`, `chore`, `docs`, `refactoring`
   - Include a summary of changes in the PR body

6. **Verify**: Confirm the PR was created successfully and share the PR URL.
