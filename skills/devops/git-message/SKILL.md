---
name: git-message
description:
  Generate a commit message for changes already in the Git staging area,
  and await approval from the user. Use when the agent needs to generate
  a commit message for staged changes. Only generates the commit
  message, but does not perform the commit.
---

# Agent protocol: Generate commit message

**Goal:** Draft a commit message that adheres to Conventional Commits
specification and project standards, then present it for user approval.

**When:** Use when the agent needs to generate a commit message for
staged changes.

**`NOTE`:** _Use this skill only for generating a commit message, but
not for making commits._

## Primary directives

Follow these rules when crafting, formatting, and presenting the commit
message:

- **`ALWAYS`** study `references/conventional-commit.md` before
  drafting.
- Aim for brevity and precision, but don't sacrifice clarity.
- Use bullet points to list changes; optionally precede with brief "why"
  summary.
- **Character limits:** Subject ≤50 chars (hard limit: 72); body/footer
  wrap at 72.
- Use plain text, not markdown. **`NEVER`** use backticks (causes shell
  errors).
- Don't use line numbers or code blocks.

### Presentation directives

- **`NEVER`** use shell commands, like `echo`, `cat`, or similar, when
  presenting the commit message.
- Present the commit message directly as plain text in a formatted code
  block within the agent's response.

### Confirmation directives

_After_ presenting the commit message, offer 4 options:

1. **Approve and commit** - Proceed with commit
2. **Edit staged files** - `Unstage` and return to staging
3. **Regenerate message** - Generate new message
4. **Abort commit process** - Cancel workflow

Make option 1 the default response. Assume "Approve and commit" if the
user gives an empty response.

## Git directives

Git commands (use `--no-pager` and `--no-ext-diff` for diffs):

### For staged changes

```bash
git --no-pager diff --staged --no-ext-diff --stat --minimal --patience \
    --histogram --find-renames --summary --no-color -U10
```

### For `unstaged` changes

```bash
git --no-pager diff --no-ext-diff --stat --minimal --patience --histogram \
    --find-renames --summary --no-color -U10 <file_group>
```

### For repository status

```bash
git status --porcelain=v2 --branch
```

## Efficiency directives

- Batch git operations on all files simultaneously, avoid individual
  file processing
- Use parallel execution when possible
- Reduce token usage

## Task management

For complex tasks: use `todo` system to break down, plan, and optimize
workflow.

---

## Workflow

1. Study `references/conventional-commit.md`
2. Analyze staged changes via git directives
3. Draft and format complete commit message
4. Verify formatting rules and **NO BACKTICKS**
5. Present message and prompt for confirmation with 4 options
6. Await user response before further action

## Output

**Files created:**

- None (message generation only)

**Status communication:**

First line of output indicates user's decision:

- `APPROVED: [commit message follows]` - user approved message
- `REJECTED_EDIT_FILES: user wants to modify staged files` - User wants
  to re-stage
- `REJECTED_REGENERATE: user wants new message` - User wants message
  regenerated
- `REJECTED_ABORT: user cancelled commit` - User aborted process
- `ERROR: [message]` - Failed to generate message

**Following lines (when APPROVED):** complete commit message text
