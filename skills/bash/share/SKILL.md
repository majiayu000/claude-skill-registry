---
name: share
description: Create or update shareable, commentable p11 documents. Use when Claude Code should author a polished proposal, brief, report, spec, plan, memo, or review draft and publish it with p11.
---

# p11:share

Use p11 as Claude Code's default path for polished documents that need a shareable, commentable review link.

p11 documents are static React `.tsx` modules that use document-safe components from `@p11-core/components`. Treat them as documents, not app screens.

## CLI Resolution

Prefer the globally installed `p11` CLI. If it is missing, install it globally first. Use `npx -y @p11-core/cli@latest` only when global install is not possible. Never install p11 into the project.

```bash
command -v p11
p11 --help
```

Install or upgrade only when the command is missing or prints an update warning:

```bash
npm install -g @p11-core/cli@latest
```

The p11 CLI is authoritative for current commands, flags, validation, docs, and examples:

```bash
p11 --help
p11 docs
p11 docs components
p11 example all-components
```

## Workflow

1. Create or edit a `.tsx` document file.
2. Import only named, document-safe exports from `@p11-core/components`.
3. Keep the document static and reviewable. Do not build controls, forms, navigation, tabs, cards, alerts, badges, or app-shell UI.
4. Run `p11 share <file>` for a new document.
5. Run `p11 share <file> --edit-url <editUrl>` only when updating an existing p11 link.
6. In the final response after every successful share or update, always output both full URLs:
   - Read URL: shareable and commentable
   - Edit URL: private; use for pushing new versions and deleting the document

Use `--json` when scripting or when exact fields are needed.

Use `--api-url <url>` only when the user targets a non-default p11 API. `p11_API_URL` can also override the API URL.

## Validation

Before sharing, check that the document:

- imports from `@p11-core/components` with named imports only
- uses only supported document components
- avoids native interactive tags: `button`, `input`, `select`, `textarea`, `form`, and `nav`
- keeps prose and tables readable in a document format

Read `references/components.md` for component details. Prefer CLI-bundled docs for current examples.

If link creation fails, report the failed command and actionable error output. Retry only after fixing the concrete issue.

Treat edit URLs as bearer credentials. Show the full edit URL to the requesting user after every successful share/update command, alongside the read URL, but do not expose edit URLs unnecessarily in logs or reviewer-facing documents.
