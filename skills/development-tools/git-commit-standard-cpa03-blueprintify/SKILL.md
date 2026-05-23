---
name: git-commit-standard
description: Generates conventional commits based on file changes. Analyzes diffs and creates properly formatted commit messages.
---

# Git Commit Standard Skill

Generate Conventional Commits based on staged changes.

## Procedure

1. Check current status:

   ```bash
   git status
   ```

2. View staged changes:

   ```bash
   git diff --staged
   ```

3. If nothing staged, view all changes:

   ```bash
   git diff
   ```

4. Analyze changes and determine commit type:

   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Formatting, no code change
   - `refactor`: Code change that neither fixes nor adds feature
   - `perf`: Performance improvement
   - `test`: Adding or correcting tests
   - `chore`: Build process, tooling, etc.

5. Generate commit message format:

   ```
   type(scope): subject

   [optional body]

   [optional footer]
   ```

## Rules

- Subject line max 72 characters
- Use imperative mood ("add" not "added")
- No period at end of subject
- Separate subject from body with blank line
- Body should explain WHAT and WHY

## Example Output

```bash
git commit -m "feat(auth): add OAuth2 support for Google login

- Implemented Google OAuth2 flow
- Added token refresh mechanism
- Updated login page UI

Closes #123"
```
