---
name: create-doc
description: Create a new doc file in .chalk/docs/ when the user asks to create, write, or add documentation
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write
argument-hint: "[doc description]"
read-only: false
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: docs, documentation, writing
capabilities: docs.create, chalk.docs.create
activation-intents: create doc, add documentation, write documentation
activation-events: user-prompt
activation-artifacts: .chalk/docs/**
risk-level: low
---

Create a new documentation file in `.chalk/docs/`.

## Workflow

1. **Parse the request** — Identify the target vertical and topic from `$ARGUMENTS`.
2. **Check existing docs** — Read filenames in the target directory to find the highest numbered file. The next doc number is `highest + 1`.
3. **Draft the doc** — Write substantive content, not stubs. Use the structure and tone guidelines below.
4. **Write the file** — Save to `.chalk/docs/<vertical>/<number>_<slug>.md`.
5. **Confirm** — Tell the user the doc was created with its path and a brief summary.

## Verticals

| Vertical | Directory | Use For |
|----------|-----------|---------|
| Product | `product/` | Vision, strategy, user research, pricing, competitive analysis |
| AI | `ai/` | Agent context, codebase orientation, prompt patterns, gotchas |
| Engineering | `engineering/` | Architecture, conventions, APIs, runbooks, data flows |
| Root | `.chalk/docs/` | Docs that don't fit a vertical |

If the user specifies a vertical ("engineering doc about..."), use it. If ambiguous, infer from content: technical architecture -> engineering, product strategy -> product, agent context -> ai.

## Filename Convention

```
<number>_<snake_case_slug>.md
```

- Number is sequential within the vertical directory (profile docs are always `0_`)
- Slug is a short snake_case summary

## Doc File Structure

```markdown
# <Doc Title>

Last updated: <YYYY-MM-DD> (<brief change note>)

## <First Section>

Content...

## <Next Section>

Content...
```

- No YAML frontmatter (docs are plain markdown)
- First `# Heading` is the title
- "Last updated" line immediately after the title
- Use `## Heading` for sections
- All GFM features supported: tables, checkboxes, strikethrough, code blocks, Mermaid diagrams

## Content Guidelines

| Vertical | Tone | Focus |
|----------|------|-------|
| `product/` | Business-facing, concise | What and why: user problems, strategy, metrics |
| `ai/` | Agent-facing, reference-style | Where things are, how they work, gotchas |
| `engineering/` | Technical, comprehensive | Architecture, conventions, APIs, data flows |
