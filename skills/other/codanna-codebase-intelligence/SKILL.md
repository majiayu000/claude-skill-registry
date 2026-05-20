---
name: codanna-codebase-intelligence
description: Use codanna MCP tools for semantic code search, call graphs, and impact analysis before grep/find.
---

# Codanna Codebase Intelligence

Codanna indexes your codebase and provides semantic search, call graphs, and dependency analysis via MCP tools. **Use codanna before grep/find** - it understands code structure, not just text patterns.

## When to Use

- **Finding code**: "Where do we handle authentication?" → `semantic_search_docs`
- **Understanding dependencies**: "What calls this function?" → `find_callers`
- **Impact analysis**: "What breaks if I change this?" → `analyze_impact`
- **Exploring symbols**: "Show me the Parser struct" → `find_symbol`

## Core Tools

### Discovery

```
# Natural language search - finds code by intent, not keywords
semantic_search_docs query:"error handling patterns" limit:5

# Search symbols by name/pattern
search_symbols query:"parse" kind:"function"

# Get full details on a specific symbol
find_symbol name:"process_file"
```

### Relationships

```
# Who calls this function? (upstream)
find_callers symbol:"validate_input"

# What does this function call? (downstream)
get_calls symbol:"process_request"

# Full dependency graph - what breaks if I change this?
analyze_impact symbol:"DatabaseConnection" depth:3
```

### Documentation (RAG)

```
# Search indexed markdown/docs
search_documents query:"API authentication" collection:"docs"
```

## Tool Selection Guide

| Task | Tool | Example |
|------|------|---------|
| Find code by concept | `semantic_search_docs` | "database migrations" |
| Find symbol by name | `search_symbols` | Pattern: "auth*" |
| Get symbol details | `find_symbol` | Exact: "UserService" |
| Trace callers | `find_callers` | "Who uses this?" |
| Trace dependencies | `get_calls` | "What does this call?" |
| Assess refactor risk | `analyze_impact` | "What breaks?" |

## Workflow Patterns

### Before Refactoring

1. `find_symbol` - understand current implementation
2. `find_callers` - identify all usage sites
3. `analyze_impact` - assess blast radius
4. Then proceed with changes

### Understanding Unfamiliar Code

1. `semantic_search_docs` - "how does X work"
2. `find_symbol` - get entry point details
3. `get_calls` - trace execution flow

### Finding Where to Add Code

1. `semantic_search_docs` - "similar patterns"
2. `find_callers` - how existing code integrates
3. Follow established patterns

## Why Codanna Over Grep

| Grep/Find | Codanna |
|-----------|---------|
| Text matching | Semantic understanding |
| String "parse" matches comments | `find_symbol` finds the actual function |
| Manual call tracing | `find_callers` shows full graph |
| Guessing impact | `analyze_impact` shows dependencies |

## Integration with Agent-Loops

Codanna complements the agent-loops review workflow by providing structural code
intelligence that diff-based review alone cannot offer.

### Pre-review impact analysis

Before invoking `specialist-review.sh`, run codanna to understand the blast radius
of your changes. This feeds grounded structural data into the review, helping
reviewers focus on real downstream effects rather than guessing from the diff.

```bash
# Gather impact data for changed symbols
codanna mcp find_callers process_request --watch
codanna mcp analyze_impact DatabaseConnection --watch --json
```

### Multi-specialist review support

In the multi-specialist review architecture (see `docs/development/plans/multi-specialist-review.md`),
specialists can use codanna tools alongside Read/Grep/Glob for grounded analysis.
Impact data can also inform specialist triage — determining which review perspectives
to activate based on which parts of the codebase are structurally affected.

### Automatic index freshness

The `--watch` flag on CLI commands checks for file changes and re-indexes before
running, so impact data stays current throughout a review session without manual
reindexing. The MCP server equivalent (`codanna serve --watch`) provides the same
freshness guarantee for interactive sessions.

## Tips

- Start broad with `semantic_search_docs`, then drill down with `find_symbol`
- Use `analyze_impact` before any refactor touching shared code
- `find_callers` with depth > 1 shows transitive callers
- Results include file paths and line numbers - use for navigation
