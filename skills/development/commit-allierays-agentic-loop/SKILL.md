---
description: Commit code with conventional commit messages tied to task context. Never skips hooks.
---

# Commit Changes

Create a well-structured git commit with a conventional commit message derived from the current task context.

## Rules

- **NEVER use `--no-verify`.** Pre-commit hooks exist for a reason. If hooks fail, fix the issues and retry.
- **NEVER use `git add -A` or `git add .`** unless every changed file is relevant. Stage files by name.
- **NEVER amend a previous commit** unless the user explicitly asks for it.

## Step 1: Understand What Changed

Run these in parallel:

1. `git status` — see all changed, staged, and untracked files
2. `git diff` — see unstaged changes
3. `git diff --cached` — see already-staged changes
4. `git log --oneline -5` — see recent commit style for this repo

Review the changes and identify:
- Which files are related to the current task
- Which files are unrelated noise (editor configs, lock files from unrelated installs, etc.)
- Whether any files contain secrets, `.env` content, or credentials — **never commit those**

## Step 2: Find the Task Context

Look for task context to derive the commit message from. Check in order:

1. **Ralph PRD story** — if there's an active story, check `.ralph/progress.txt` for the current story ID and title. The commit message should reference this.
2. **Recent conversation** — what did the user ask you to do? Use that as the commit description.
3. **The diff itself** — if no other context, derive the purpose from the actual code changes.

## Step 3: Craft the Commit Message

Use **conventional commits** format matching this repo's style:

```
type(scope): concise description of WHY
```

### Types (pick the right one)
| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `chore` | Maintenance, deps, config, version bumps |
| `test` | Adding or fixing tests |
| `docs` | Documentation only |
| `refactor` | Code restructuring, no behavior change |
| `style` | Formatting, whitespace, naming |
| `ci` | CI/CD pipeline changes |

### Scope
- If working on a Ralph story: use the story ID — e.g., `feat(story-3): add user auth`
- If working on a specific module: use the module name — e.g., `fix(loop): handle empty config`
- If broad/cross-cutting: omit scope — e.g., `chore: bump version to 3.28.0`

### Message rules
- Start with **lowercase** after the colon
- Focus on **why**, not what — the diff shows what
- Keep the first line **under 72 characters**
- If more detail is needed, add a blank line and a body paragraph

### Examples from this repo
```
feat: add Working Principles to CLAUDE.md and plansDirectory to settings
feat(story-3): add user authentication with JWT
fix: bash 3.2 unbound variable when run_loop called with no args
chore: bump version to 3.27.1
test(api): add integration tests for /users endpoint
refactor: extract verification into separate modules
```

## Step 4: Stage and Commit

1. **Stage only the relevant files** by name — do NOT use `git add -A` or `git add .`
2. **Show the user** the proposed commit message and list of staged files before committing
3. **Ask if the message looks right** using AskUserQuestion with options:
   - "Looks good, commit it"
   - "Let me edit the message" (then ask for their preferred message)
4. **Run the commit** — use a HEREDOC for the message:

```bash
git commit -m "$(cat <<'EOF'
type(scope): message here
EOF
)"
```

5. **Run `git status`** after to confirm it succeeded

## Step 5: Handle Hook Failures

If pre-commit hooks fail:

1. **Read the hook output** carefully
2. **Fix the issues** the hooks identified (lint errors, secrets detected, etc.)
3. **Re-stage** the fixed files
4. **Commit again** — same message, same process, NO `--no-verify`

If hooks auto-fix files (e.g., prettier, eslint --fix):
1. Review the auto-fixes
2. Stage the auto-fixed files
3. Retry the commit

**If you cannot resolve hook failures after 5 attempts**, stop and explain the issue to the user. Do NOT bypass hooks.

## Notes

- If the user says "just commit it" or similar, still follow the process — just skip the AskUserQuestion confirmation
- If there are no changes to commit, say so and stop
- Group related changes into one commit; suggest splitting if changes are unrelated
- When in doubt about the type, `feat` for new things, `fix` for broken things, `chore` for everything else
