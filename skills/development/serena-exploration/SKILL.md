---
name: serena-exploration
description: "코드 탐색, 코드 분석, 탐색, 코드 구조, 심볼 분석 - Use when exploring or analyzing code. Systematic code exploration workflow using Serena MCP tools for symbol navigation and reference tracking."
---

# Serena MCP Code Exploration Workflow

## Core Principle

Follow the order: **Structure Overview → Symbol Search → Analysis → Modification**

## Tool Priority

1. **`get_symbols_overview`** - First understand file structure
2. **`find_symbol`** - Find specific classes, functions, variables
3. **`find_referencing_symbols`** - Check where symbols are used
4. **`search_for_pattern`** - Regex-based code search
5. **`read_file`** - Use only when above tools are insufficient

## Work Process

```
1. Check file structure with get_symbols_overview
   ↓
2. Search for needed symbols with find_symbol
   ↓
3. Analyze and understand code
   ↓
4. Perform modification/creation
```

## Checklist

**Before Starting Exploration:**
- [ ] Identify target files/directories
- [ ] Run get_symbols_overview first

**During Exploration:**
- [ ] Navigate by symbols (functions, classes, variables)
- [ ] Use find_referencing_symbols when checking references

**After Exploration:**
- [ ] Confirm sufficient context has been gathered
- [ ] Document analysis results in docs directory (if needed)

## What to Avoid

- Using `read_file` directly without understanding structure
- Skipping Serena MCP tools and reading files directly
- Reading entire files indiscriminately
