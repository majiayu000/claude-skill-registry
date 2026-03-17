---
name: llm-doc-writer
description: Write token-efficient documentation for LLM context. Use when creating CLAUDE.md, README, technical docs, agent instructions, or any documentation consumed by AI assistants.
---

# LLM-Optimized Documentation

## Core Principles

| Principle | Rule |
|-----------|------|
| **Density** | Max info, min tokens |
| **Format** | Tables > prose, bullets > paragraphs |
| **No fluff** | Ban filler words (see list below) |
| **Show don't tell** | Code examples > explanations |
| **Progressive disclosure** | TOC + separate files for details |

## Banned Patterns

```
# Filler words - NEVER use
simplement, il suffit de, en fait, basically, just, simply,
it's important to note, as mentioned, obviously, of course,
please note that, keep in mind, remember that

# Redundant structures - NEVER use
"This file contains..." (obvious from filename)
"In this section we will..." (just do it)
"The following example shows..." (just show it)
```

## Format Rules

### Tables over Prose

```markdown
# BAD - 45 tokens
The system supports three modes: development mode which
enables hot reload, production mode which optimizes for
performance, and test mode which mocks external services.

# GOOD - 20 tokens
| Mode | Behavior |
|------|----------|
| dev | Hot reload |
| prod | Optimized |
| test | Mocked services |
```

### Bullets over Paragraphs

```markdown
# BAD - Narrative
To run the project, first ensure Node.js is installed,
then install dependencies with npm install, and finally
start the dev server with npm run dev.

# GOOD - Scannable
## Run
1. Requires: Node.js 18+
2. `npm install`
3. `npm run dev`
```

### Code over Explanation

```markdown
# BAD - Explaining
To create a new user, call the createUser function
with an object containing name and email properties.

# GOOD - Showing
```ts
createUser({ name: "Jo", email: "jo@x.com" })
```
```

## Structure Template

For CLAUDE.md / agent docs:

```markdown
# Project Name

## Stack
- Frontend: React/Vite
- Backend: FastAPI
- DB: PostgreSQL

## Commands
| Action | Command |
|--------|---------|
| Dev | `npm run dev` |
| Test | `npm test` |
| Build | `npm run build` |

## Architecture
[Brief description, link to detailed docs if needed]

## Conventions
- [Rule 1]
- [Rule 2]
```

## Progressive Disclosure

For long docs (>200 lines):

```markdown
# Main Doc

## Quick Reference
[Essential info here]

## Details
See [ARCHITECTURE.md](ARCHITECTURE.md)
See [API.md](API.md)
```

## Self-Check

Before finalizing, verify:

- [ ] No filler words?
- [ ] Tables used where possible?
- [ ] Bullet points, not paragraphs?
- [ ] Examples over explanations?
- [ ] < 500 lines (or split)?
- [ ] No redundant info?

## Examples

See [patterns.md](patterns.md) for before/after examples.
