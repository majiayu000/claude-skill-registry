---
name: gh-search
description: Search GitHub for code examples and patterns. Use when user asks to "search GitHub", "find examples on GitHub", "how do people implement X", or needs real-world code patterns.
allowed-tools: Bash(aaa gh-search:*), Bash(bin/aaa gh-search:*), Read, Write
argument-hint: <query>
---

# GitHub Code Search

Search GitHub for real-world code examples and implementation patterns.

@context/blocks/construct/gh-search.md

## When to Use

- Need real-world examples ("how do people implement X?")
- Exploring unfamiliar libraries/frameworks
- Comparing implementation approaches

## Workflow

1. **Generate Queries:** Create 3-5 targeted queries
   - Language filters: `language:typescript`, `language:go`
   - Code patterns: `function use`, `const use =`
   - Config files: `filename:tsconfig.json`

2. **Execute:** Run `aaa gh-search "query"` for each query

3. **Aggregate:** Combine results, deduplicate, ensure diversity

4. **Analyze:** Extract imports, patterns, architectural styles

5. **Report:** Synthesize findings with GitHub URLs

6. **Save:** Write report to `docs/research/github/[timestamp]-topic.md`

## Input: $ARGUMENTS

The search query. Can include GitHub search qualifiers:
- `language:typescript`
- `path:src/`
- `extension:json`

## Output

```markdown
# GitHub Code Search: [Topic]

## Summary
[Overview of patterns found]

## Patterns
- **[Pattern Name]**: [Description] (Refs: [repo/file](url))

## Examples
### [Approach Name]
- **Pros/Cons**: [Trade-offs]
- **Code**: [Link to file](url)

## All Files
[List of all analyzed files with GitHub URLs]
```
