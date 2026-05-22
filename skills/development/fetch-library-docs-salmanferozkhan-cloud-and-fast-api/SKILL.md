---
name: fetch-library-docs
description: Fetches official documentation for external libraries and frameworks (React, Next.js, Prisma, FastAPI, Express, Tailwind, MongoDB, etc.) with 60-90% token savings via content-type filtering. Use this skill when implementing features using library APIs, debugging library-specific errors, troubleshooting configuration issues, installing or setting up frameworks, integrating third-party packages, upgrading between library versions, or looking up correct API patterns and best practices. Triggers automatically during coding work - fetch docs before writing library code to get correct patterns, not after guessing wrong.
---

# Library Documentation Skill

Fetches official library documentation with 60-90% token savings.

---

## WHEN TO INVOKE (Auto-Detection)

**INVOKE AUTOMATICALLY when:**

| Context | Detection Signal | Content Type |
|---------|------------------|--------------|
| **Implementing** | About to write code using library API | `examples,api-ref` |
| **Debugging** | Error contains library name (e.g., `PrismaClientError`) | `troubleshooting` |
| **Installing** | Adding new package, `npm install`, setup task | `setup` |
| **Integrating** | Connecting libraries ("use X with Y") | `examples,setup` |
| **Upgrading** | Version migration, breaking changes | `migration` |
| **Uncertain** | First use of library feature, unsure of pattern | `examples` |

**DO NOT INVOKE when:**
- Already have sufficient knowledge from training
- User pasted docs or has them open
- Task is about local/private code (use codebase search)
- Comparing libraries (use web search)

---

## DECISION LOGIC

### 1. Identify Library

```
Priority: User mention → Error message → File imports → package.json → Ask user
```

Examples:
- `PrismaClientKnownRequestError` → library = "prisma"
- `import { useState } from 'react'` → library = "react"
- `from fastapi import FastAPI` → library = "fastapi"

### 2. Identify Topic

```
Priority: User specifies → Error message → Feature being implemented → "getting started"
```

### 3. Select Content Type

| Task | Content Type |
|------|--------------|
| Implementing code | `examples,api-ref` |
| Debugging error | `troubleshooting,examples` |
| Installing/setup | `setup` |
| Integrating libs | `examples,setup` |
| Upgrading version | `migration` |
| Understanding why | `concepts` |
| Best practices | `patterns` |

---

## EXECUTION

```bash
# With known library ID (faster - saves 1 API call)
bash scripts/fetch-docs.sh --library-id <id> --topic "<topic>" --content-type <types>

# With library name (auto-resolves)
bash scripts/fetch-docs.sh --library <name> --topic "<topic>" --content-type <types>
```

### Quick Library IDs

| Library | ID |
|---------|----|
| React | `/reactjs/react.dev` |
| Next.js | `/vercel/next.js` |
| Prisma | `/prisma/docs` |
| Tailwind | `/tailwindlabs/tailwindcss.com` |
| FastAPI | `/tiangolo/fastapi` |

See [references/library-ids.md](references/library-ids.md) for complete list.

---

## ERROR HANDLING (Quick Reference)

| Error | Action |
|-------|--------|
| `[LIBRARY_NOT_FOUND]` | Try spelling variations |
| `[LIBRARY_MISMATCH]` | Use --library-id directly |
| `[EMPTY_RESULTS]` | Broaden topic or use `--content-type all` |
| `[RATE_LIMIT_ERROR]` | Check API key setup |

**Call Budget**: Context7 allows 3 calls/question. Use `--library-id` to save 1 call.

See [references/context7-tools.md](references/context7-tools.md) for full error handling.

---

## REFERENCES

- [Library IDs](references/library-ids.md) - Complete library ID list
- [Usage Patterns](references/patterns.md) - Real-world examples
- [Context7 Tools](references/context7-tools.md) - API details, error codes, setup
