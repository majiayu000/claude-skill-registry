---
name: tldr
description: |
  TLDR code analysis for token-efficient codebase understanding.

  AUTO-INVOKE when:
  - User asks "who calls X", "what affects X", "find implementation"
  - Need to trace dependencies, call graphs, or data flow
  - Semantic search for code by meaning (not exact string)
  - Understanding large codebases efficiently
  - Before reading any large file (use context first)
  - Debugging "why is X null/undefined here"
  - Before refactoring (impact analysis)

  PREFER TLDR over raw file reads - 95% token savings.
context: fork
allowed-tools: [mcp__tldr__semantic, mcp__tldr__context, mcp__tldr__impact, mcp__tldr__arch, mcp__tldr__slice, mcp__tldr__structure, mcp__tldr__calls, mcp__tldr__cfg, mcp__tldr__dfg, mcp__tldr__change_impact, mcp__tldr__dead, mcp__tldr__imports, mcp__tldr__importers, mcp__tldr__diagnostics]
---

# TLDR Code Analysis

Token-efficient codebase analysis using llm-tldr. **95% fewer tokens than reading raw files.**

## Quick Reference

| Task | Command |
|------|---------|
| "How does X work?" | `semantic` → `context` |
| "Who calls X?" | `impact` |
| "What would break?" | `impact` + `change_impact` |
| "Why is X null here?" | `slice` (backward) |
| "What does X affect?" | `slice` (forward) |
| "Project structure?" | `arch` + `structure` |
| "Find auth code" | `semantic "authentication"` |
| "Data flow in function" | `dfg` |
| "Control flow" | `cfg` |
| "Find dead code" | `dead` |
| "Type errors?" | `diagnostics` |

## Commands

### Semantic Search (Natural Language)
Find code by meaning, not exact text:
```
mcp__tldr__semantic { "project": ".", "query": "user authentication flow" }
mcp__tldr__semantic { "project": ".", "query": "error handling" }
```

### Function Context (95% Token Savings)
Get LLM-ready summary instead of reading entire file:
```
mcp__tldr__context { "project": ".", "entry": "handleLogin", "depth": 2 }
```

### Impact Analysis (Before Refactoring)
Find all callers - critical before changing any function:
```
mcp__tldr__impact { "project": ".", "function": "useAuth" }
```

### Architecture Overview
Understand project layers and dependencies:
```
mcp__tldr__arch { "project": "." }
```

### Program Slice (Debugging)
What affects a specific line (backward) or what it affects (forward):
```
mcp__tldr__slice {
  "file": "src/auth.ts",
  "function": "login",
  "line": 42,
  "direction": "backward",
  "variable": "user"
}
```

### Call Graph
Cross-file function call relationships:
```
mcp__tldr__calls { "project": ".", "language": "typescript" }
```

### Data Flow Graph
Variable references and def-use chains:
```
mcp__tldr__dfg { "file": "src/auth.ts", "function": "validateToken" }
```

### Control Flow Graph
Basic blocks and branching:
```
mcp__tldr__cfg { "file": "src/auth.ts", "function": "handleRequest" }
```

### Change Impact (Affected Tests)
Find tests affected by changed files:
```
mcp__tldr__change_impact { "project": "." }
```

### Dead Code Detection
Find unreachable code:
```
mcp__tldr__dead { "project": ".", "entry_points": ["main", "test_"] }
```

### Import Analysis
Parse imports or find importers:
```
mcp__tldr__imports { "file": "src/utils.ts" }
mcp__tldr__importers { "project": ".", "module": "auth" }
```

### Diagnostics (Type/Lint)
Type checking and linting:
```
mcp__tldr__diagnostics { "path": "src/", "language": "typescript" }
```

### Structure Overview
Functions, classes, methods per file:
```
mcp__tldr__structure { "project": ".", "language": "typescript", "max_results": 50 }
```

## Workflow Patterns

### Understanding Code
```
1. tldr arch .                    # Get project overview
2. tldr semantic "feature name"   # Find relevant code
3. tldr context functionName      # Get LLM-ready summary
4. Read (only if more detail needed)
```

### Before Refactoring
```
1. tldr impact functionName       # Who calls this?
2. tldr change_impact             # What tests affected?
3. tldr context functionName      # Understand the function
4. Make changes
5. tldr diagnostics src/          # Check for errors
```

### Debugging
```
1. tldr slice file func line      # What affects this line?
2. tldr dfg file func             # Data flow analysis
3. tldr context func              # Understand function
```

## Prerequisites

```bash
pipx install llm-tldr
tldr daemon start     # Background service (300x faster)
tldr warm .           # Build indexes including embeddings
```

## CRITICAL RULES

1. **ALWAYS use `tldr context` BEFORE reading large files**
2. **ALWAYS use `tldr impact` BEFORE refactoring**
3. **ALWAYS use `tldr semantic` for "how does X work" questions**
4. **Use `grep` ONLY for exact string matching**

## Output

Return findings with:
- **Relevant code**: Key functions/files found
- **Call chain**: How things connect
- **Recommendations**: Next steps based on analysis
- **Store as learning** if discovering non-obvious patterns
