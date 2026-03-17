---
name: using-serena-symbols
description: Guidance for using Serena's LSP-powered symbol analysis. Use when exploring codebases, finding symbol definitions, tracing references, or when grep/text search would be imprecise.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Using Serena Symbol Analysis

Serena provides LSP-powered code intelligence for accurate symbol extraction, relationship discovery, and cross-file analysis.

## When to Use Serena vs Text Search

| Use Serena | Use Grep/Text Search |
|------------|---------------------|
| Finding class/function definitions | Searching for string literals |
| Tracing method references | Finding patterns in comments |
| Understanding call hierarchies | Searching config files |
| Analyzing imports/dependencies | Finding TODO/FIXME markers |
| Cross-file architecture analysis | Simple keyword search |

**Key advantage**: Serena understands code structure. `find_symbol("UserService")` finds the actual class definition, not every mention of "UserService" in comments or strings.

## Core Tools

### 1. get_symbols_overview

Get high-level view of symbols in a file. **Start here** when exploring a new file.

```python
mcp__plugin_serena_serena__get_symbols_overview({
  "relative_path": "src/services/auth.py",
  "depth": 1  # 0=top-level only, 1=include methods
})
```

**Returns**: Classes, functions, variables with their kind and location.

### 2. find_symbol

Find symbols by name pattern. Supports flexible matching.

**Name path patterns**:

- `UserService` - Find any symbol named "UserService"
- `UserService/authenticate` - Find method in class
- `/UserService` - Exact match (absolute path)
- `Service` with `substring_matching: true` - Matches "UserService", "AuthService", etc.

```python
mcp__plugin_serena_serena__find_symbol({
  "name_path_pattern": "UserService/authenticate",
  "include_body": true,  # Get source code
  "depth": 0  # 0=just this symbol, 1=include children
})
```

**Key parameters**:

- `include_body` (bool): Include source code (use judiciously for context)
- `depth` (int): How many levels of children to retrieve
- `relative_path` (str): Restrict search to file/directory
- `substring_matching` (bool): Partial name matching

### 3. find_referencing_symbols

Find all references to a symbol. Essential for understanding impact.

```python
mcp__plugin_serena_serena__find_referencing_symbols({
  "name_path": "UserService/authenticate",
  "relative_path": "src/services/auth.py"
})
```

**Returns**: Code snippets showing each reference with context.

### 4. search_for_pattern

Regex search when you need flexibility (like grep, but smarter file filtering).

```python
mcp__plugin_serena_serena__search_for_pattern({
  "substring_pattern": "def.*async.*:",
  "restrict_search_to_code_files": true,
  "context_lines_before": 2,
  "context_lines_after": 2
})
```

## Process

### Exploring a New Codebase

1. **Directory structure** - Understand layout

   ```python
   mcp__plugin_serena_serena__list_dir({
     "relative_path": ".",
     "recursive": false
   })
   ```

2. **Entry points** - Find main files

   ```python
   mcp__plugin_serena_serena__get_symbols_overview({
     "relative_path": "src/main.py",
     "depth": 1
   })
   ```

3. **Trace key classes** - Understand structure

   ```python
   mcp__plugin_serena_serena__find_symbol({
     "name_path_pattern": "App",
     "include_body": false,
     "depth": 1
   })
   ```

### Understanding a Specific Class

1. **Find the class** with children

   ```python
   mcp__plugin_serena_serena__find_symbol({
     "name_path_pattern": "AuthService",
     "depth": 1,
     "include_body": false
   })
   ```

2. **Read specific methods** you need

   ```python
   mcp__plugin_serena_serena__find_symbol({
     "name_path_pattern": "AuthService/validate_token",
     "include_body": true
   })
   ```

3. **Find who calls it**

   ```python
   mcp__plugin_serena_serena__find_referencing_symbols({
     "name_path": "AuthService/validate_token",
     "relative_path": "src/services/auth.py"
   })
   ```

### Tracing Dependencies

1. **Find all imports of a module**

   ```python
   mcp__plugin_serena_serena__search_for_pattern({
     "substring_pattern": "from.*auth.*import|import.*auth",
     "restrict_search_to_code_files": true
   })
   ```

2. **Find references to trace usage**

   ```python
   mcp__plugin_serena_serena__find_referencing_symbols({
     "name_path": "AuthService",
     "relative_path": "src/services/auth.py"
   })
   ```

## Symbol Kinds Reference

LSP symbol kinds (for `include_kinds`/`exclude_kinds` filtering):

| Kind | Int | Description |
|------|-----|-------------|
| File | 1 | |
| Module | 2 | |
| Namespace | 3 | |
| Package | 4 | |
| Class | 5 | |
| Method | 6 | |
| Property | 7 | |
| Field | 8 | |
| Constructor | 9 | |
| Enum | 10 | |
| Interface | 11 | |
| Function | 12 | |
| Variable | 13 | |
| Constant | 14 | |

Example - find only classes:

```python
mcp__plugin_serena_serena__find_symbol({
  "name_path_pattern": "Service",
  "substring_matching": true,
  "include_kinds": [5]  # Class only
})
```

## Efficiency Tips

1. **Use `relative_path`** to scope searches - much faster than searching entire codebase
2. **Start with `include_body: false`** - get structure first, read code only when needed
3. **Use `depth: 0`** initially - expand to children only when exploring specific classes
4. **Combine with Forgetful** - create memories for important architectural findings

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `how do I find a symbol` | find_symbol with name_path_pattern |
| `how do I explore a file's structure` | get_symbols_overview with depth |
| `how do I trace references` | find_referencing_symbols |
| `how do I search code patterns` | search_for_pattern with regex |
| `what methods does this class have` | find_symbol with depth=1 |

---

## When to Use

Use this skill when:

- Exploring class/function definitions with structural accuracy
- Tracing method call hierarchies across files
- Analyzing imports and dependencies
- Need code intelligence beyond text matching

Use Grep/text search instead when:

- Searching for string literals or comments
- Finding patterns in config files or YAML
- Looking for TODO/FIXME markers
- Simple keyword search across non-code files

Use [serena-code-architecture](../serena-code-architecture/SKILL.md) instead when:

- Performing full architectural analysis with memory persistence
- Building entity graphs from code structure

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Searching entire codebase without relative_path | Slow, noisy results | Scope with relative_path parameter |
| Starting with include_body=true | Wastes tokens on code you may not need | Start with include_body=false, read selectively |
| Using depth > 1 on large modules | Returns excessive nested symbols | Use depth=0 or depth=1, expand as needed |
| Using text grep for symbol definitions | Matches comments, strings, false positives | Use find_symbol for structural accuracy |
| Skipping get_symbols_overview | Jumping to find_symbol without context | Start with overview to understand file structure |

---

## Verification

After symbol analysis:

- [ ] Correct symbol found (not a similarly named one)
- [ ] References traced to all call sites
- [ ] Scope was narrowed with relative_path where possible
- [ ] Results were token-efficient (include_body only when needed)

---

## Language Support

Serena works with any language that has an LSP server configured:

- Python (pyright/pylsp)
- TypeScript/JavaScript (tsserver)
- Rust (rust-analyzer)
- Go (gopls)
- Java (jdtls)
- And more...

The specific features available depend on the language server's capabilities.
