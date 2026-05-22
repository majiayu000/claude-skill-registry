---
name: git
description: Git workflow and safety rules for this workspace.
---

# Git Skill

Use this skill when performing git operations or handling file changes.

## File and Git Operations

- Delete unused or obsolete files when your changes make them irrelevant
  (refactors, feature removals, etc.), and revert files only when the change is
  yours or explicitly requested. If a git operation leaves you unsure about
  other agents' in-flight work, stop and coordinate instead of deleting.
- **Before attempting to delete a file to resolve a local type/lint failure,
  stop and ask the user.** Other agents are often editing adjacent files;
  deleting their work to silence an error is never acceptable without explicit
  approval.
- NEVER edit `.env` or any environment variable files—only the user may change
  them.
- Coordinate with other agents before removing their in-progress edits—don't
  revert or delete work you didn't author unless everyone agrees.
- Moving/renaming and restoring files is allowed.
- ABSOLUTELY NEVER run destructive git operations (e.g., `git reset --hard`,
  `rm`, `git checkout`/`git restore` to an older commit) unless the user gives
  an explicit, written instruction in this conversation. Treat these commands
  as catastrophic; if you are even slightly unsure, stop and ask before
  touching them. *(When working within Cursor or Codex Web, these git
  limitations do not apply; use the tooling's capabilities as needed.)*
- Never use `git restore` (or similar commands) to revert files you didn't
  author—coordinate with other agents instead so their in-progress work stays
  intact.
- Always double-check git status before any commit.
- Keep commits atomic: commit only the files you touched and list each path
  explicitly. For tracked files run `git commit -m "<scoped message>" --
  path/to/file1 path/to/file2`. For brand-new files, use the one-liner `git
  restore --staged :/ && git add "path/to/file1" "path/to/file2" && git commit
  -m "<scoped message>" -- path/to/file1 path/to/file2`.
- Commit message format: Use Conventional Commits specification with
  parentheses for scope (e.g., `fix(profiler): correct ProcedureCall type`,
  `feat(client,zerospin): add batch support`). Format:
  `<type>(<scope>): <description>`. See
  `.cursor/rules/conventional-commits.mdc` for full specification.
- Quote any git paths containing brackets or parentheses (e.g.,
  `src/app/[candidate]/**`) when staging or committing so the shell does not
  treat them as globs or subshells.
- When running `git rebase`, avoid opening editors—export `GIT_EDITOR=:` and
  `GIT_SEQUENCE_EDITOR=:` (or pass `--no-edit`) so the default messages are used
  automatically.
- Never amend commits unless you have explicit written approval in the task
  thread.

## Commit Message Format

Use the Conventional Commits specification format for all commit messages:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Format Details

- **Type** (required): One of the conventional commit types:
  - `fix`: A bug fix
  - `feat`: A new feature
  - `docs`: Documentation only changes
  - `style`: Changes that do not affect the meaning of the code
  - `refactor`: A code change that neither fixes a bug nor adds a feature
  - `perf`: A code change that improves performance
  - `test`: Adding missing tests or correcting existing tests
  - `build`: Changes that affect the build system or external dependencies
  - `ci`: Changes to CI configuration files and scripts
  - `chore`: Other changes that don't modify src or test files
  - `revert`: Reverts a previous commit

- **Scope** (optional): Enclosed in parentheses `()`. The scope should indicate
  the area of the codebase affected:
  - Use package/app names when applicable (e.g., `profiler`, `zerospin`,
    `client`, `cloudflare`)
  - Examples: `fix(profiler):`
  - If all the changes are in a specific package folder, obviously use that
    package for scope. Same goes for an app.

- **Description** (required): A short, imperative-mood description of the change
  (max 72 characters recommended)

- **Body** (optional): Provide additional contextual information about the
  change

- **Footer** (optional): Reference issue numbers, breaking changes, etc.

### Examples

```
fix(profiler): correct ProcedureCall type inference
feat(client): add OPFSAdapter support
```

### Important Notes

- Always use parentheses `()` for scope, not square brackets `[]`
- The scope is optional—omit the parentheses entirely if no scope is needed:
  `fix: resolve memory leak`
- Keep the description concise and in imperative mood ("fix bug" not "fixed bug"
  or "fixes bug")
