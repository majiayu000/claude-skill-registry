---
name: pr-review-loop
description: Manage PR review feedback loops with Gemini Code Assist. Use when pushing changes to a PR, iterating on review feedback, or monitoring CI/review status. Automatically falls back to Claude when Gemini is rate-limited.
license: MIT
environment: claude-code
---

# PR Review Loop

Streamline the push-review-fix cycle for PRs with automated reviewers like Gemini Code Assist.

## CRITICAL: Git Command Restrictions

**YOU DO NOT HAVE PERMISSION TO USE RAW GIT COMMANDS.**

| Forbidden | Use Instead |
|-----------|-------------|
| `git commit` | `commit-and-push.sh "msg"` |
| `git push` | `commit-and-push.sh "msg"` |

All scripts are in `~/.claude/skills/pr-review-loop/scripts/`.

## When to Use

Invoke when user:
- Pushes changes and waits for CI/reviews
- Says "new reviews available" or "check PR feedback"
- Iterates on review feedback from Gemini or other reviewers
- Wants to monitor PR status
- Asks to address reviewer comments

## Core Workflow

```
1. Get unresolved comments (--wait to poll 5 min)
2. For EACH comment: fix OR skip, then REPLY
3. Commit using commit-and-push.sh (NEVER raw git)
4. Trigger next review with trigger-review.sh --wait
5. Repeat until no new issues
6. One final loop, then ask about merge
```

### Step-by-step Commands

**1. Check for comments:**
```bash
~/.claude/skills/pr-review-loop/scripts/summarize-reviews.sh <PR>
~/.claude/skills/pr-review-loop/scripts/get-review-comments.sh <PR> --with-ids --wait
```

**2. Reply to EVERY comment:**
```bash
~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh <PR> <id> "Fixed - description"
~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh <PR> <id> "Won't fix - reason"
```

**3. Commit and push:**
```bash
~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh "fix: description"
```

**4. Trigger next review:**
```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --wait
```

## Be Skeptical of Reviews

**Not all suggestions are good.** Evaluate critically:

- Does this improve the code, or is it pedantic?
- Is this appropriate for the project context?
- Would this add unnecessary complexity?

**Skip suggestions that are:**
- Platform-specific when not applicable
- Overly defensive (excessive null checks)
- Stylistic preferences not matching project
- Documentation for self-explanatory code

When in doubt, ask the user.

## One More Loop Rule

When all comments are resolved:
1. Track in TodoWrite: "Final verification loop"
2. Trigger one more review cycle
3. If no actionable feedback → ask about merge
4. If new fixes needed → remove todo, do fresh "one more" after

## Gemini Rate Limit Fallback

When Gemini hits daily quota, use Claude:

```bash
~/.claude/skills/pr-review-loop/scripts/trigger-review.sh <PR> --claude
# OR
~/.claude/skills/pr-review-loop/scripts/claude-review.sh <PR>
```

Then use Task tool with the generated prompt.

## Scripts Quick Reference

| Script | Purpose |
|--------|---------|
| `commit-and-push.sh "msg"` | **ALWAYS USE** for commits |
| `reply-to-comment.sh <PR> <id> "msg"` | Reply and auto-resolve |
| `get-review-comments.sh <PR> --with-ids --wait` | Fetch comments |
| `trigger-review.sh <PR> --wait` | Trigger review cycle |
| `summarize-reviews.sh <PR>` | Summary by priority/file |
| `claude-review.sh <PR>` | Claude fallback prompt |

See `references/scripts-reference.md` for complete documentation.

## Reply Templates

- **Fixed:** "Fixed - [description]"
- **Won't fix:** "Won't fix - [reason]"
- **Deferred:** "Good catch, tracking in #issue"
- **Acknowledged:** "Acknowledged - [explanation]"

## Prerequisites

- `gh` CLI authenticated
- `pre-commit` installed (`pip install pre-commit`)
- Pre-commit hooks in repo (`.pre-commit-config.yaml`)

## Permission Setup

Add to `.claude/settings.local.json`:

```
Bash(~/.claude/skills/pr-review-loop/scripts/commit-and-push.sh:*)
Bash(~/.claude/skills/pr-review-loop/scripts/reply-to-comment.sh:*)
Bash(~/.claude/skills/pr-review-loop/scripts/trigger-review.sh:*)
```

## References

- `references/scripts-reference.md` - Complete script documentation
- `references/workflow-examples.md` - End-to-end examples
