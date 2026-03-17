---
name: cache-docs
description: When fetching library documentation, API references, or technical docs for project dependencies via WebFetch, automatically save a copy to the docs/ folder. Also triggers when user pastes documentation or discusses library APIs that should be cached for reference. Every non-stdlib import in the project should have corresponding reference docs cached.
---

# Documentation Caching Skill

When you fetch or receive documentation for a library dependency, cache it locally.

## When to Activate

- After any WebFetch of documentation sites (readthedocs, official docs, GitHub READMEs)
- When user pastes library documentation into the conversation
- When discussing a library's API and realizing docs should be cached
- When importing a new dependency that lacks cached documentation

## Caching Process

1. **Determine the library name** from the URL or content context
2. **Create the directory** if it doesn't exist: `docs/<library-name>/`
3. **Generate a slugified filename** from the page title or topic
4. **Write the file** with YAML frontmatter:

```markdown
---
source: <original URL>
fetched: <ISO 8601 date>
library: <library name>
summary: <one-line summary of what this doc covers>
---

# <Page Title>

<Content here>
```

5. **Update the index** at `docs/_index.md` with the new entry

## File Organization

```text
docs/
├── _index.md           # Auto-maintained index of all cached docs
├── pycrdt/
│   ├── quickstart.md
│   └── api-reference.md
├── stytch/
│   ├── magic-links.md
│   └── rbac.md
├── nicegui/
│   └── getting-started.md
└── sqlmodel/
    └── tutorial.md
```

## Index Format

The `_index.md` should list all cached documentation:

```markdown
# Cached Documentation Index

## pycrdt
- [Quickstart](pycrdt/quickstart.md) - Getting started with pycrdt CRDT library
- [API Reference](pycrdt/api-reference.md) - Full API documentation

## stytch
- [Magic Links](stytch/magic-links.md) - Email magic link authentication
- [RBAC](stytch/rbac.md) - Role-based access control

...
```

## Important Notes

- Always preserve code examples from documentation
- Include version information when available
- If documentation is very long, summarize and link to source
- Cache critical information even if full doc doesn't fit
