---
name: omg
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when writing or editing .omg.md files - the human-first DSL for API specification that compiles to OpenAPI 3.1
---

# OMG (OpenAPI Markdown Grammar)

## Quick Start

```markdown
---
method: GET
path: /accounts/{accountId}
operationId: get-account
tags: [Accounts]
---
# Get Account
Returns details of a specific account.
```omg.path
{ accountId: uuid }
```
```omg.response
{ id: uuid, name: string, balance: decimal }
```
```

## Core Concepts

- **`.omg.md` files** - Markdown with YAML frontmatter, one endpoint per file
- **Code blocks**: `omg.path`, `omg.query`, `omg.body`, `omg.response`, `omg.response.{code}`, `omg.returns`, `omg.type`
- **Types**: `string`, `integer`, `decimal`, `boolean`, `date`, `datetime`, `uuid`, `any`
- **Syntax**: `field?: type` (optional), `type[]` (array), `"a"|"b"` (enum), `@min(0)` (constraints)
- **Partials**: `@path/to/partial` or `{{> path/to/partial }}` for reuse

## CLI

```bash
node packages/omg-cli/dist/cli.js build api.omg.md -o output.yaml
node packages/omg-cli/dist/cli.js parse endpoint.omg.md
```

## Notes

- Compiles to OpenAPI 3.1, ~6x reduction in lines
- Run `npm run build` before using CLI
