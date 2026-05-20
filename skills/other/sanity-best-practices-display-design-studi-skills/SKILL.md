---
name: sanity-best-practices
description: Comprehensive Sanity development best practices covering GROQ performance, schema design, Visual Editing, images, Portable Text, page builders, Studio configuration, TypeGen, localization, and migrations. Use this skill when building, reviewing, or optimizing Sanity applications.
license: MIT
metadata:
  author: sanity
  version: "1.0.0"
---

# Sanity Best Practices

Comprehensive best practices guide for Sanity development, maintained by Sanity. Contains rules across 10 categories, prioritized by impact to guide schema design, query optimization, and frontend integration.

## When to Apply

Reference these guidelines when:
- Writing GROQ queries or optimizing performance
- Designing content schemas
- Implementing Visual Editing and live preview
- Working with images, Portable Text, or page builders
- Configuring Sanity Studio structure
- Setting up TypeGen for type safety
- Implementing localization
- Migrating content from other systems

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | GROQ Performance | CRITICAL | `groq-` |
| 2 | Schema Design | HIGH | `schema-` |
| 3 | Visual Editing | HIGH | `visual-` |
| 4 | Images | HIGH | `image-` |
| 5 | Portable Text | HIGH | `pte-` |
| 6 | Page Builder | MEDIUM | `pagebuilder-` |
| 7 | Studio Configuration | MEDIUM | `studio-` |
| 8 | TypeGen | MEDIUM | `typegen-` |
| 9 | Localization | MEDIUM | `i18n-` |
| 10 | Migration | LOW-MEDIUM | `migration-` |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/groq-optimizable-filters.md
rules/schema-data-over-presentation.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
- Framework-specific notes (when applicable)

## Framework Integration

Framework-specific guidance (Next.js, Astro, Remix, etc.) is available via the Sanity MCP server using `list_sanity_rules` and `get_sanity_rules` tool calls when available. If the MCP server is not configured, run `npx sanity@latest mcp configure` to set it up.
