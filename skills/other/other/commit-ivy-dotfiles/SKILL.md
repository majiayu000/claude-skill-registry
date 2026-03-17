---
name: commit
description: Use when committing code changes. Enforces intentional file selection, conventional commits, and why-focused messages.
argument-hint: "[message | --amend | files...]"
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git show:*)
---

# Git Commit

## Arguments
```
$ARGUMENTS
```

## Constraints

**Never use `git -C <path>`** — always run git commands from the current working directory. The `-C` flag rewrites the command in a way that doesn't match `allowed-tools` patterns, forcing unnecessary user approval. Plain `git status`, `git log`, etc. already operate on the repo you're in.

## Instructions

### 1. Assess Current State

Run in parallel:
- `git status` — see staged/unstaged/untracked files
- `git diff --cached` — see what's staged
- `git diff` — see unstaged changes
- `git log --oneline -5` — recent commit style reference

### 2. File Selection (CRITICAL)

**Never use `git add -A` or `git add .`** — be intentional about every file.

Decision tree:
- **Arguments include specific files** → stage those files
- **Files already staged** → verify they're the intended changes
- **Nothing staged** → infer from conversation context which files to stage

Use `git diff --name-only` to review changed files. Include only:
- Files modified during this conversation
- Files directly relevant to the logical change

Exclude:
- Unrelated changes (stage separately)
- Generated files (unless intentional)
- Sensitive files (.env, credentials)

### 3. Craft Commit Message

**Format:** Conventional Commits

```
<type>(<scope>): <subject>

[optional body explaining WHY]
```

**Types:** `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`

**Rules:**
- Subject line ≤72 characters (including mood emoji)
- Present tense ("add" not "added")
- Focus on WHY, not WHAT (the diff shows what)
- Body lines ≤80 characters

**Message source:**
- **Arguments provide message** → use it (adjust format if needed)
- **No message** → draft based on staged changes, explain reasoning

**Mood emoji:** End every subject line with a GitHub emoji that reflects the vibe of the conversation or task. Intuit mood from context — the ticket being worked on, the user's tone, frustration level, excitement, etc.

Palette (use these or any GitHub emoji that fits):

| Emoji | Shortcode | Mood |
|-------|-----------|------|
| :sparkles: | `:sparkles:` | excited about something new |
| :tada: | `:tada:` | celebration, milestone |
| :fire: | `:fire:` | on a roll, crushing it |
| :bug: | `:bug:` | squashing something annoying |
| :face_with_spiral_eyes: | `:face_with_spiral_eyes:` | confused, dizzy, "what even is this" |
| :rage: | `:rage:` | frustrated, fighting the tools |
| :relieved: | `:relieved:` | finally fixed, weight off shoulders |
| :broom: | `:broom:` | tidying up, chores |
| :thinking: | `:thinking:` | exploratory, not sure yet |
| :coffin: | `:coffin:` | killing dead code, removing things |
| :rocket: | `:rocket:` | shipping, deploying, launching |
| :nail_care: | `:nail_care:` | polish, aesthetics, making it pretty |

### 4. Execute Commit

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line here :emoji:

Optional body explaining why this change was made.
EOF
)"
```

### 5. Verify

Run `git status` to confirm clean state or show remaining changes.

## Amend Mode

If arguments include `--amend`:
1. Show current HEAD commit with `git show --stat HEAD`
2. Stage additional changes if specified
3. Run `git commit --amend`

**Warning:** Only amend unpushed commits.

## Examples

```
/commit                           → assess changes, draft message, commit
/commit fix login redirect        → stage relevant files, commit with message
/commit --amend                   → amend previous commit
/commit src/auth.ts src/login.ts  → stage specific files, draft message, commit
```

Example commit messages with mood:
```
feat(auth): add OAuth2 login flow :sparkles:
fix(auth): resolve login redirect loop :relieved:
chore(deps): bump mise tool versions :broom:
refactor(cli): remove dead argument parser :coffin:
```
