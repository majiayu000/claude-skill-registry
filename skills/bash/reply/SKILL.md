---
name: reply
description: Review p11 document comments and replies, then post useful replies to visible threads that ask questions, are unclear, are indecisive, or need input. Use when Claude Code should answer reviewers on a p11 document.
---

# p11:reply

Use this skill to inspect p11 comments/replies and post replies where a response is useful.

## Target Resolution

Resolve the p11 document target in this order:

1. Use the p11 read URL, edit URL, read ID, or edit ID provided by the user.
2. If none is provided, use the most recent p11 document mentioned or created in the current chat conversation.
3. Only if the current chat has no usable p11 target, run `p11 history` and use the most recent relevant entry.

Do not use `p11 history` when the current chat already contains a usable p11 target.

## CLI Resolution

Prefer the global `p11` CLI. If missing, install `@p11-core/cli` globally. Use `npx -y @p11-core/cli@latest` only when global install is not possible. Never install p11 into the project.

Check availability with `command -v p11` and `p11 --help`.

Install or upgrade with `npm install -g @p11-core/cli@latest` when the command is missing or any `p11` command prints an update warning.

Use `--json` when structured comment fields are useful.

## Review Comments

Fetch all comments/replies:

```bash
p11 comments <target>
```

Use `--version <number>` only when the user asks for comments on a historical version.

Only consider comments/replies that are visible to reviewers. Do not reply to resolved or hidden comments; reviewers will not see those replies in the UI.

Review every visible thread before replying. Decide from the comment/reply content, not from an unresolved status field alone. Reply when a visible thread:

- asks a question
- requests clarification
- needs input or a decision
- is indecisive
- has conflicting replies
- is unclear to Claude Code
- needs a lightweight acknowledgement before the document can be revised

Do not equate an unresolved or visible status with needing a reply. If the thread already gives a clear action, such as "change this to...", "remove this...", "use this wording", or another settled decision, do not reply; those should be handled by `p11:revise`.

If no threads need replies, say that clearly and summarize any clear decisions that should be handled by `p11:revise`.

When discussing comments with the user, refer to quoted text or thread content instead of line numbers unless the user asks for line numbers.

## Posting Replies

Post replies with:

```bash
p11 reply <readUrl|readId> <commentId> --name "Claude Code" --body <text>
```

If the user provided only an edit URL or edit ID, use the current chat context, `p11 comments`, or `p11 history` to recover the matching read URL or read ID before replying.

Use `--body-file <file>` or `--body-file -` for multi-line replies. Use the reply name `Claude Code` for replies from Claude Code.

Keep replies concise and specific. If the comment is unclear, ask one direct clarifying question and name the decision needed to proceed.

After posting replies, ask the user to refresh the p11 page to see them.
