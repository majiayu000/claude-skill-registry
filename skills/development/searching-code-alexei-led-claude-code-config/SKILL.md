---
name: searching-code
description: Intelligent codebase search via WarpGrep. Use when user asks "how does X work", "trace flow", "find all implementations", "understand codebase", or needs cross-file exploration in large repos (1000+ files).
user-invocable: false
allowed-tools:
  - mcp__morphllm__warpgrep_codebase_search
  - mcp__morphllm__codebase_search
  - Read
  - Grep
  - Glob
---

# Intelligent Code Search with WarpGrep

WarpGrep is an RL-trained search agent that reasons about code, not just pattern matches.

## How It Works

- **8 parallel searches** per turn (explores multiple hypotheses)
- **4 reasoning turns** (follows causal chains across files)
- **F1=0.73** in ~3.8 steps (vs 12.4 for standard search)

## When to Use WarpGrep

| Use WarpGrep                | Use Built-in Grep        |
| --------------------------- | ------------------------ |
| "How does auth flow work?"  | "Find class UserService" |
| "Trace data from API to DB" | Simple regex patterns    |
| "Find all error handling"   | "Where is X defined?"    |
| Large repos (1000+ files)   | Known file patterns      |
| Before major refactoring    | Quick needle lookups     |

## Query Formulation

**Good queries** (reasoning required):

```
"How does authentication flow from the login handler to the database?"
"Find all places where user permissions are checked"
"Trace the request lifecycle from router to response"
```

**Bad queries** (use Grep instead):

```
"Find UserService" → use Grep
"Search for 'import React'" → use Grep
```

## Workflow

1. **Formulate query**: Describe WHAT you want to understand, not just WHAT to find
2. **Run WarpGrep**: `mcp__morphllm__warpgrep_codebase_search`
3. **Interpret results**: Ranked snippets with file paths and line numbers
4. **Follow up**: Read specific files for deeper understanding

## Parameters

```
search_string: "natural language description of what to find"
repo_path: "/absolute/path/to/repo"
```

## Tips

- Be specific about the behavior or flow you're investigating
- Include context: "in the API layer" or "during startup"
- WarpGrep handles ambiguity better than exact pattern matching
- Results include surrounding context for understanding
