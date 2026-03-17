---
name: commit
description: Commit staged changes with an auto-generated bulleted commit message. Run /stage first to stage files.
disable-model-invocation: true
---

When the user asks to commit changes, follow this workflow. The user's tool approval prompts serve as the approval gates -- do NOT ask extra confirmation questions.

## Step 1: Check what's staged

Run `git diff --cached --name-status` to see what is currently staged.

If nothing is staged, tell the user to run `/stage` first and stop. Do not proceed.

## Step 2: Match commit style

Run `git log -5 --oneline` to understand the repository's commit message style.

## Step 3: Draft and run commit

1. Draft a commit message:
   - Clear, concise summary line (under 70 characters)
   - Bulleted list of changes (maximum 10 bullets)
   - Focus on WHAT changed and WHY, not implementation details
   - Group related changes to stay under 10 bullets
   - Format:

     ```
     Brief summary of changes

     - First change
     - Second change
     - Third change

     Co-Authored-By: Claude Code (commit) <noreply@anthropic.com>
     ```

2. Present the proposed commit message, then run the commit command. The user sees and approves this command via the tool approval prompt.

   ```bash
   git commit -m "$(cat <<'EOF'
   <commit message here>

   Co-Authored-By: Claude Code (commit) <noreply@anthropic.com>
   EOF
   )"
   ```

3. Run `git status` after to verify success.

## Handle failures

- If pre-commit hooks fail, fix the issues and create a NEW commit (never amend unless explicitly asked)
- If there is nothing to commit, inform the user

## Important Rules

- NEVER amend commits unless explicitly requested
- NEVER skip hooks or use --no-verify
- NEVER commit without the co-authored-by line
- DO NOT push unless explicitly asked
- Keep bullets concise and action-oriented
- Group related changes to stay under 10 bullets
- Do NOT ask extra approval questions -- the tool approval prompts are the gates

## Example Invocations

- `/commit`
- "commit staged changes"
- "commit with a message"
