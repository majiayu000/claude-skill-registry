---
name: code-structure
description: Extract file structure (functions, classes, exports) efficiently without reading entire files, using ast-grep, go doc, ctags, or other language-specific tools to get outlines and signatures
---

# Code Structure Exploration Tools

## Recognizing Structure Questions

**These keywords mean use structure tools, NOT grep/search:**
- "all the methods/functions/classes in..."
- "list of function signatures"
- "what functions/exports/API..."
- "package API" or "module exports"
- "method signatures with receivers" (Go)
- "what's available in..."

**These keywords mean use search (Grep tool or ast-grep):**
- "where is X defined"
- "find calls to X"
- "search for pattern Y"

## Before You Choose a Tool

Ask yourself:
1. Am I listing/exploring what exists? → Structure tools
2. Am I finding WHERE something is? → Search tools (Grep or ast-grep)
3. Am I understanding HOW something works? → Read

## When to Get File Outline vs Read

**Get outline/index when:**
- File is large (>500 lines)
- Need to see what's available (functions, classes, exports)
- Exploring unfamiliar code
- Want to decide what to read in detail
- **Saves 90%+ context** vs reading entire file

**Just use Read when:**
- File is small (<500 lines)
- Already know what you're looking for
- Need to understand implementation details
- ast-grep pattern already targets what you need

## Anti-Patterns

**DON'T use grep/rg/Grep tool for:**
- Extracting function/method lists
- Getting API overviews
- Finding all exports/public members
- Getting signatures/interfaces

These are STRUCTURE queries, not SEARCH queries.

## Exploration Strategy

**Tiered approach (try in order):**

1. **ast-grep with known patterns** - Fast, targeted
   - Extract exports, functions, classes with specific patterns
   - See [code structure guide](./reference/code-structure-guide.md) for patterns

2. **Toolchain-specific approaches** - When available
   - **Go:** `go doc -all <package>` for all methods/functions with signatures
     - Example: "list all methods" → `go doc -all ./internal/pkg`
     - Example: "method signatures" → `go doc -all ./internal/pkg`
   - **Python:** Language-specific indexers
   - **ctags/universal-ctags:** Symbol index across languages
   - See [code structure guide](./reference/code-structure-guide.md) for examples

3. **Read file** - Last resort for exploration
   - Sometimes necessary to understand structure

## Key Principle

**Use structure tools to decide what to read, then read selectively.**

Don't read 1000-line files blind. Get an outline first, then read the 50 lines you actually need.

## Detailed Patterns

For language-specific extraction patterns, ast-grep examples, ctags usage, and integration strategies, load [code structure guide](./reference/code-structure-guide.md).
