---
name: claude-print
description: "Run a non-interactive Claude Code print-mode call from Codex. Use when the user asks to \"claude print\", \"ask claude\", \"run claude\", \"consult claude\", or when a Codex Turbo skill needs Claude as an independent peer reviewer."
---

# Claude Print

Run a non-interactive Claude Code CLI print-mode call from Codex. This is the Codex edition's low-level Claude bridge for one-shot review and consultation prompts.

## Step 1: Choose Permission Scope

Default to read-only review:

```bash
claude -p --permission-mode dontAsk --allowedTools="Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),Bash(git status:*),Bash(git rev-parse:*),Bash(git ls-files:*)" "<prompt>" < /dev/null
```

The Bash allow-list is restricted to read-only git subcommands so peer review cannot mutate the working tree, branches, or remotes. Use broader permissions only when the user explicitly asks Claude to perform write-capable work.

## Step 2: Shape the Prompt

Keep the prompt compact and explicit:

- State that Claude is an independent reviewer.
- Include the exact scope: diff command, files, plan/spec path, or inline artifact text.
- Include the required output contract.
- Tell Claude to verify codebase claims by reading files before reporting findings.
- Tell Claude not to modify files unless the current task explicitly requests write-capable work.

For large context, write the context to `.turbo/claude/<tag>-ctx.txt` and pipe it:

```bash
mkdir -p .turbo/claude
cat .turbo/claude/<tag>-ctx.txt | claude -p --permission-mode dontAsk --allowedTools="Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),Bash(git status:*),Bash(git rev-parse:*),Bash(git ls-files:*)" "<prompt>"
```

## Step 3: Run Synchronously

Run Claude as a foreground command and wait for the result. Treat a returned `session_id` from the Codex shell harness as the still-running foreground command; keep polling that session until Claude exits, reaches a clear error, or has had roughly an hour for normal review work.

Do not background Claude print-mode calls, give up during quiet periods, or classify the run as empty while the shell session is still active. The parent workflow needs the complete output before evaluation.

## Step 4: Interpret Results

Treat Claude's output as a review signal, not as an authority. Cross-check actionable findings against the codebase before applying fixes.

Then update or check the active plan and proceed to any remaining task.

## Rules

- Read-only operation is the default.
- Do not enable `--dangerously-skip-permissions` for peer review.
- Use `.turbo/claude/` for temporary prompt/context files.
- Redirect stdin with `< /dev/null` for non-piped invocations.
