---
name: unikit-commit
description: Create conventional commit messages for {{engine_name}} projects by analyzing staged changes. Handles engine-specific concerns like companion file pairing, binary assets, and plan task references. ALWAYS use this skill when the user asks to commit, save changes, or create a commit — in any language. Trigger phrases include "commit", "create commit", "save changes", "сделай коммит", "закоммить", "коммит", "сохрани изменения". Even if the user simply says "commit this" or asks you to commit after finishing a task — invoke this skill, do NOT commit manually via git.
argument-hint: "[scope or context]"
allowed-tools:
  - Read
  - Bash(git *)
  - Glob
  - Grep
  - AskUserQuestion
---

# {{engine_name}} Commit Generator

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification, with {{engine_name}}-specific safety checks.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Workflow

1. **Analyze Changes**
   - Run `git status` to see staged files
   - Run `git diff --cached` to see staged changes
   - If nothing staged, show warning and suggest staging

2. **{{engine_name}} Safety Checks**

   Run these checks before generating the commit message. Report findings as `WARN` or `ERROR`.

   **a) Engine companion files**
   Some engines require companion/metadata files for every asset.
   Read `.unikit/DESCRIPTION.md` to determine if the current engine has such a mechanism. If yes:
   - If a new file is staged, its companion is also staged (and vice versa)
   - If a file is deleted, its companion is also deleted (and vice versa)
   - Orphaned companion files (no matching asset) → `ERROR`, suggest staging the missing counterpart or removing the orphan
   - Missing companion for a new asset → `ERROR`, suggest staging it
   If the engine has no companion file mechanism — skip this check.

   **b) Engine-ignored directories**
   If any staged file matches a path that should be ignored by the engine (check the project's `.gitignore`) → `ERROR`. These are engine-generated directories that should never be committed. Suggest unstaging them.

   **c) Binary asset awareness**
   Run `git diff --cached --numstat` — files shown as `-	-	<path>` are binary.
   If staged changes include binary files, warn the user about binary content in the commit. These files don't diff well — just note their presence so the user is aware.

   **d) Secrets check**
   Never commit files that likely contain secrets (`.env`, `credentials.json`, API keys in config files). If detected → `ERROR`.

3. **Context Check (Read-Only)**
   - Read `.unikit/ARCHITECTURE.md` (if present) to verify staged changes don't violate module boundaries or dependency rules defined there
   - Read `.unikit/ROADMAP.md` (if present) to check milestone alignment — for `feat`/`fix`/`perf` commits, check if changes relate to an unchecked milestone and suggest mentioning it in the commit body
   - Read `.unikit/skill-context/unikit-commit/SKILL.md` (if present) — project-specific rules accumulated by `/unikit-evolve`. Treat as overrides: skill-context wins over general rules on conflict
   - Missing optional files (`ROADMAP.md`) are `WARN`, not blockers
   - These are lightweight checks — flag only clear violations as `WARN`, don't block the commit
   - Never modify these files

4. **Plan Task Linkage**
   - Check if `.unikit/plans/` contains an active plan (look for `TASKS.md`)
   - If a plan exists and staged changes clearly relate to a planned task, suggest referencing the phase/task number in the commit message body (e.g., "Phase 8, tasks 8.1-8.3")
   - This is optional — suggest it, don't require it

5. **Determine Commit Type**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Code style (formatting, semicolons)
   - `refactor`: Code change that neither fixes a bug nor adds a feature
   - `perf`: Performance improvement
   - `test`: Adding or modifying tests
   - `build`: Build system or dependencies
   - `ci`: CI configuration
   - `chore`: Maintenance tasks

6. **Identify Scope**
   - Derive from file paths using the project's module/folder structure (see `.unikit/ARCHITECTURE.md`):
     - Module directories → module name in kebab-case (e.g., `Wallets/` → `wallets`, `MiniGames/` → `mini-games`)
     - Feature directories → feature name (e.g., `Gameplay/` → `gameplay`, `Application/` → `app`)
   - Use argument as scope if provided
   - Omit scope if changes span multiple unrelated areas

7. **Generate Message**
   - Keep subject line under 72 characters
   - Conventional Commits prefix (`type(scope):`) is always in English — only the description text after the colon uses the configured language
   - Use imperative mood ("add" / "добавить" — not "added" / "добавлено")
   - Don't capitalize first letter after type
   - No period at end of subject

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Examples

**Simple feature:**
```
feat(wallets): add currency conversion system
```

**Bug fix with body:**
```
fix(mini-games): handle null item reference in slider game

The slider mini-game could crash when item config was missing
the difficulty curve. Added null check with fallback to default.

Fixes #42
```

**Refactor with plan reference:**
```
refactor(characters): extract customer behavior into state machine

Migrated customer logic from monolithic Update to NodeCanvas FSM.
Phase 3, tasks 3.1-3.4
```

**Breaking change:**
```
feat(inventory)!: migrate to Opsive UIS item categories

BREAKING CHANGE: item definitions now use CategoryID instead of TypeEnum
```

## Behavior

When invoked:

1. Check for staged changes
2. Run {{engine_name}} safety checks (meta pairing, ignored dirs, binary assets, secrets)
3. Run lightweight context checks against `.unikit/` docs
4. If errors found — list them and ask user whether to proceed or fix first
5. Propose a commit message
6. Confirm with the user before committing:

   ```
   AskUserQuestion: 💾 Proposed commit message:

   <type>(<scope>): <subject>

   Options:
   1. Commit as is
   2. Edit message
   3. Cancel
   ```

   Based on choice:
   - Commit as is → proceed to step 7
   - Edit message → ask the user for the corrected message via `AskUserQuestion`, then return to step 6 with the new message
   - Cancel → do NOT commit → **STOP**

7. Execute `git commit` with the confirmed message
8. **Post-commit push handling**:
   - **If `git.skip_push_after_commit = true` in `.unikit/config.yaml`**:
     - Skip push prompt entirely
     - End workflow after successful local commit
   - **Otherwise** (default behavior), offer to push:
     - Show branch/ahead status: `git status -sb`
     - If the branch has no upstream, use: `git push -u origin <branch>`
     - Otherwise: `git push`

     ```
     AskUserQuestion: Push to remote?

     Options:
     1. 🔄 Push now
     2. Skip push
     ```

     - **Push now** → execute push command based on upstream status:
       - if branch has no upstream → `git push -u origin <branch>`
       - otherwise → `git push`
     - **Skip push** → end the workflow

If argument provided (e.g., `/unikit-commit wallets`):
- Use it as the scope
- Or as context for the commit message

## Splitting Unrelated Changes

If staged changes contain unrelated work (e.g., a feature + a bugfix, or changes to independent modules), suggest splitting into separate commits:
1. Show which files/hunks belong to which commit
2. Confirm split plan with the user:

   ```
   AskUserQuestion: Split into separate commits?

   Options:
   1. ✅ Yes, split as suggested
   2. No, commit everything together
   3. Let me adjust the grouping
   ```

   Based on choice:
   - Yes, split as suggested → proceed to step 3
   - No, commit everything together → proceed to step 4 (propose single commit message)
   - Let me adjust the grouping → ask the user for the adjusted grouping via `AskUserQuestion`, then return to step 2 with the new plan

3. Unstage all: `git reset HEAD`
4. Stage and commit each group separately using `git add <files>` + `git commit`
5. After all commits are done, run Post-commit push handling (Step 8) — respects `git.skip_push_after_commit`

## Important

- Review large diffs carefully before committing
- Treat `.unikit/ARCHITECTURE.md` as read-only context
- NEVER add `Co-Authored-By` or any other trailer attributing authorship to the AI. Commits must not contain AI co-author lines
- Conventional Commits prefix (`type(scope):`) is always in English; the subject and body text use the language from `.unikit/config.yaml` (`language.artifacts`)
