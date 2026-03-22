---
name: docs-seeker
description: (ePost) Use when you need API docs, library references, or framework documentation for an unfamiliar package

metadata:
  agent-affinity: [epost-researcher, epost-fullstack-developer, epost-mcp-manager]
  keywords: [docs, documentation, search, context7, api-reference, library, research, best-practices]
  platforms: [all]
  triggers: ["documentation", "docs", "api reference", "how to use"]
  connections:
    enhances: [research]
---

# Documentation Seeker Skill

## Purpose
Finding and reading documentation for packages, libraries, and frameworks.

## When Active
User needs documentation, you're unfamiliar with a library, need API reference.

## Expertise

### Search Strategy

#### 1. Context7 MCP (preferred)
Use `resolve-library-id` then `query-docs` for up-to-date library documentation.

#### 2. WebSearch
Search for "[library name] documentation [version] [topic]"

#### 3. Official Docs
Use WebFetch to read official documentation websites.

#### 4. GitHub Repository
Use `gh` CLI or repomix to read source code documentation.

### Source Priority
1. Official docs (most authoritative)
2. Context7 library docs
3. GitHub repository README/docs
4. Community resources (Stack Overflow, blog posts)

## Search Patterns

### Effective Queries
- "[library] [version] [topic]" - precise searches
- "how to [task] in [library]" - task-oriented
- "[error message]" - for debugging docs
- "[library] examples" - for code samples

### Error Handling
- If Context7 fails, fall back to WebSearch
- If no docs found, check package README on npm/PyPI/CocoaPods
- Always note when documentation may be outdated
- Verify version-specific info matches your target

## Best Practices
- Always specify version when searching
- Check documentation date (prefer recent)
- Look for official examples first
- Read Getting Started before API reference
- Cross-reference with source code if unclear
- Note breaking changes between versions

### Related Skills
- `knowledge-retrieval` — Internal-first search (check before going external)
- `research` — Multi-source investigation methodology
- `repomix` — Codebase summarization for context
