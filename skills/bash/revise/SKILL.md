---
name: revise
description: Revise the most recent or provided p11 shareable document based on comments/replies and publish a new version. Use when Claude Code should apply clear reviewer decisions to a p11 document.
---

# p11:revise

Use this skill to revise an existing p11 document from reviewer comments and share a new version.

## Target Resolution

Resolve the p11 document target in this order:

1. Use the p11 read URL, edit URL, read ID, edit ID, or source `.tsx` file provided by the user.
2. If none is provided, use the most recent p11 document mentioned or created in the current chat conversation.
3. Only if the current chat has no usable p11 target, run `p11 history` and use the most recent relevant entry.

Do not use `p11 history` when the current chat already contains a usable p11 target.

To publish a new version, locate both:

- the source `.tsx` document file
- the existing p11 edit URL

If either cannot be determined from the chat, local files, or p11 history, ask the user for the missing target.

## CLI Resolution

Prefer the global `p11` CLI. If missing, install `@p11-core/cli` globally. Use `npx -y @p11-core/cli@latest` only when global install is not possible. Never install p11 into the project.

Check availability with `command -v p11` and `p11 --help`.

Install or upgrade with `npm install -g @p11-core/cli@latest` when the command is missing or any `p11` command prints an update warning.

## Comment Review

Fetch all comments/replies before editing:

```bash
p11 comments <target>
```

Use `--json` when structured fields are useful. Use `--version <number>` only when the user asks to revise from a historical version.

Only consider comments/replies that are visible to reviewers. Ignore resolved or hidden comments; reviewers will not see replies to them in the UI.

Classify every visible thread by its content, not by an unresolved status field alone:

- Clear decision: a settled, actionable instruction such as "change this to...", "remove this...", "use this wording", or an accepted alternative.
- Needs clarification: a question, request for clarification, disagreement, undecided thread, conflicting replies, or anything Claude Code cannot confidently apply.

If any visible threads need clarification, ask the user before editing or publishing whether to:

- use `p11:reply` first to ask clarifying questions on those threads, or
- ignore those threads for this revision and publish only the clear changes.

If the user chooses `p11:reply`, post clarifying replies and do not publish a revision until reviewers answer or the user asks to proceed anyway. If the user chooses to ignore those threads, apply only clear decisions.

If all threads are clear, apply clear decisions directly to the source `.tsx` document.

Do not silently ignore visible threads that need clarification.

## Revising The Document

Keep the document static and reviewable. Do not add controls, forms, navigation, tabs, cards, alerts, badges, or app-shell UI.

Read `references/components.md` when editing component structure. Prefer CLI-bundled docs for current examples:

```bash
p11 docs
p11 docs components
p11 example all-components
```

Before sharing, verify the document still:

- imports from `@p11-core/components` with named imports only
- uses only supported document components
- avoids native interactive tags: `button`, `input`, `select`, `textarea`, `form`, and `nav`
- keeps prose and tables readable in a document format

## Share The New Version

Publish the revision to the existing p11 document:

```bash
p11 share <page.tsx> --edit-url <editUrl>
```

Return the updated Read URL and Edit URL when available. Treat edit URLs as bearer credentials and avoid exposing them unnecessarily.
