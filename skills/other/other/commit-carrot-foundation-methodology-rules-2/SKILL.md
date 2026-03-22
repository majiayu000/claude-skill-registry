---
name: 'Commit Changes'
description: 'Stage files and create a conventional commit with a well-formed message.'
---

1. **Review changes**: Run `git status` and `git diff` to understand what changed.

2. **Run quality checks**: Before committing, ensure `pnpm lint:affected`, `pnpm ts:affected`, and `pnpm test:affected` all pass.

3. **Stage specific files**: Add files individually by name. Never use `git add .` or `git add -A` to avoid accidentally staging sensitive or unrelated files.

4. **Write a conventional commit message** following this format:

   ```
   <type>(<scope>): <description>
   ```

   - **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `revert`
   - **Scopes**: `nx`, `rule`, `shared`, `script`
   - Use imperative mood, lowercase, no trailing period, max 100 characters
   - Examples:
     - `feat(rule): add vehicle definition validation`
     - `fix(shared): prevent racing of requests`
     - `refactor(rule): extract helper for document matching`

5. **Create the commit**: Use `git commit -m "<message>"`. If a pre-commit hook fails, fix the issue and create a new commit (do not amend).
