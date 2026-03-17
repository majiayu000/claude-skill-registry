---
name: git-commit-assistant
description: Generates commit messages by inspecting staged changes and repo history. Matches existing conventions (Conventional Commits or plain English), leads with intent, and appends the Quest co-author trailer. Use when the user asks for a commit message, help with git commit, or when reviewing staged changes for commit.
---

# Git Commit Assistant

Generate a single commit message from the current staged diff. Output only the final commit message (no markdown, no emojis).

---

## Before Writing

1. Run `scripts/validate-manifest.sh` to check that all Quest files are listed in `.quest-manifest`. If validation fails, **stop and fix the manifest before proceeding**. Do not generate a commit message until validation passes.
2. Run `git diff --cached` to see what actually changed.
3. Run `git log --oneline` (or `git log --oneline -20`) to see existing commit style and conventions.

---

## Rules

### Match the room

- If the repo uses Conventional Commits (`feat:`, `fix:`, `docs:`, etc.), follow that.
- If it uses plain English, use plain English.
- Never impose a new convention on the repository.

### Categorize honestly

- **add** = something new
- **update** = enhancement to existing behavior
- **fix** = broken behavior is now correct
- **refactor** = behavior unchanged
- Do not inflate scope. A typo fix is not a feature.

### Lead with intent, not mechanics

- The diff shows *what* changed.
- The commit message should explain *why*.
- Prefer intent-focused subjects (e.g. "Fix race condition in session cleanup") over implementation details.

### Subject line

- Imperative mood
- ~50–72 characters
- Clear, specific, and accurate

### Body

- Optional. Use only if the intent is not obvious from the subject.
- Explain motivation, constraints, or tradeoffs.
- Wrap lines at ~72 characters.
- Do not speculate or invent context.

### Truthfulness

- Do not fabricate broader motivation.
- If intent is unclear, describe only what is visible in the diff.
- Precise but narrow beats confident but wrong.

---

## Formatting

1. Subject line
2. Blank line (if body exists)
3. Body (optional)
4. Blank line
5. Trailer

### Trailer (required)

Always append this trailer exactly:

```bash

Quest/Co-Authored by Claude Opus 4.6, GPT-5.3 Codex in Collaboration with <github username>

```

Replace:

- **github username** with the repository author's GitHub username (infer from git config, remote URL, or ask if unknown).

Never omit the trailer.

---

## Approval

Always show the intended commit message to the user and wait for explicit approval before executing `git commit`. Do not commit automatically. Present the message as a plain text block and ask the user to confirm.

---

## Output

Output only the final commit message. Do not use markdown. Do not use emojis.
