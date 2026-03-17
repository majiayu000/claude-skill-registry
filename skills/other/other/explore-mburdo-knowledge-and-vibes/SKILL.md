---
name: explore
description: Parallel codebase search with Warp-Grep MCP. Use for codebase discovery, understanding how things work, data flow analysis, or when the user asks "how does X work" about the codebase.
---

# Explore — Codebase Discovery

Parallel codebase search. Runs 8 searches per turn for efficient discovery. Direct execution.

> **Design rationale:** This skill executes directly as a simple MCP call, not substantial analytical work. The Warp-Grep MCP handles the complexity internally.

## When This Applies

| Signal | Action |
|--------|--------|
| "How does X work?" | Use /explore |
| Data flow across files | Use /explore |
| Cross-cutting concerns | Use /explore |
| Understanding architecture | Use /explore |
| User says "/explore" | Run discovery |

---

## How It Works

Warp-Grep is an MCP tool that activates automatically for natural language code questions. It:

1. Interprets your question
2. Runs up to 8 parallel searches
3. Returns relevant code snippets with context

---

## Tool Reference

The Warp-Grep MCP provides these capabilities:

| Capability | Description |
|------------|-------------|
| Parallel search | Up to 8 searches per turn |
| Context-aware | Returns surrounding code |
| Natural language | Understands questions |
| Cross-file | Follows data flow |

---

## Query Patterns

### Good Queries

```
"How does the payment processing flow work?"
"Where are user sessions managed?"
"How is error handling done in the API layer?"
"What happens when a request comes in?"
"How do modules communicate?"
"What's the data flow for authentication?"
```

### Less Effective Queries

| Query | Problem | Better Tool |
|-------|---------|-------------|
| "Find function X" | Too specific | `Grep` or `rg` |
| "Open file Y" | Not a search | `Read` tool |
| "Does X exist?" | Simple check | `Glob` |

---

## When to Use /explore

| Use Case | Use /explore? |
|----------|---------------|
| "How does authentication work?" | **YES** |
| Data flow analysis | **YES** |
| Understanding module interactions | **YES** |
| Finding all usages of a pattern | **YES** |
| Cross-cutting concern analysis | **YES** |
| Architecture understanding | **YES** |

---

## When NOT to Use /explore

| Use Case | Use Instead |
|----------|-------------|
| Known function name | `Grep` tool |
| Known exact file | `Read` tool |
| Simple existence check | `Glob` tool |
| Single specific search | `Grep` tool |
| External API docs | `/ground` |
| Past session content | `/recall` |

---

## Integration with Workflow

### During /prime
```
Use /explore to understand project structure
```

### During /advance
```
Use /explore to understand code you'll modify
```

### When stuck
```
Use /explore to find related implementations
```

---

## Decision Tree

```
What are you looking for?

UNDERSTANDING ──► /explore (this skill)
                 "How does X work?"
                 "What's the flow for Y?"

SPECIFIC CODE ──► Grep tool
                 "Find usages of functionX"

FILE PATHS ─────► Glob tool
                 "Find all *.ts files"

READ FILE ──────► Read tool
                 "Show me src/auth.ts"

EXTERNAL ───────► /ground
                 "Current API for library X"

HISTORY ────────► /recall
                 "How did we do this before?"
```

---

## Requirements

Requires Morph API key configured:

```bash
claude mcp add morph-fast-tools -s user \
  -e MORPH_API_KEY=your-key \
  -e ALL_TOOLS=true \
  -- npx -y @morphllm/morphmcp
```

---

## Quick Reference

**Use for:**
- Architecture understanding
- Data flow analysis
- Cross-cutting concerns
- Module interactions
- "How does X work?"

**Don't use for:**
- Specific function lookup → Grep
- Known file path → Read
- External APIs → /ground
- Past sessions → /recall

---

## See Also

- `/ground` — External documentation search
- `/recall` — Past session patterns
- `Grep` tool — Specific pattern search
- `Glob` tool — File pattern matching
