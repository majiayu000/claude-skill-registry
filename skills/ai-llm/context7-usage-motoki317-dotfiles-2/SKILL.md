---
name: Context7 Usage
description: This skill should be used when the user asks to "check documentation", "latest API", "library docs", "context7", or needs up-to-date library documentation. Provides Context7 MCP usage patterns.
---

# Context7 MCP Documentation Retrieval

## Tools

### resolve-library-id
Resolve package name to Context7-compatible library ID. **Must call before query-docs** unless ID is known.

### query-docs
Fetch documentation with parameters:
- `libraryId` - From resolve-library-id (e.g., `/facebook/react`)
- `query` - Specific question or topic

## Common Library IDs
- React: `/facebook/react`
- Next.js: `/vercel/next.js`
- TypeScript: `/microsoft/typescript`
- NixOS: `/nixos/nixpkgs`
- Home Manager: `/nix-community/home-manager`

## Usage Patterns

### Specific Feature Lookup
```
query-docs libraryId="/facebook/react" query="useState hook usage"
```

### General Overview
```
query-docs libraryId="/vercel/next.js" query="getting started app router"
```

### Verify Codebase Usage
1. Use Serena to find current library usage
2. Query Context7 for latest documentation
3. Compare usage with documented best practices

## Critical Rules
- Always resolve library ID before fetching documentation
- Prefer libraries with trust score 7+ (quality indicator)
- Use specific queries to get relevant results
- Combine with Serena for codebase verification workflows

## Anti-Patterns to Avoid
- Skipping ID resolution (causes lookup failures)
- Using incorrect/outdated library names
- Ignoring trust scores (low scores = unreliable docs)
