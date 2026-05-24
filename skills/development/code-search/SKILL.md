---
name: code-search
description: Token-efficient codebase exploration using MCP-first approach. Locates functions, classes, patterns, and traces dependencies with 80-90% token savings. Use when searching code, finding implementations, or tracing call chains.
---

# Code Search

Explores codebases efficiently using MCP tools before falling back to file reads.

## When to Use

- Finding functions, classes, or patterns
- Understanding feature implementation
- Tracing dependencies and call chains
- Architecture boundary verification
- Gathering context for documentation

## MCP Workflow

```
# 1. Check past context
claude-mem.search(query="<keyword>", project="<project>")

# 2. Get file overview
serena.get_symbols_overview(relative_path="target/directory")

# 3. Find symbol (signature only first)
serena.find_symbol(name_path="ClassName", depth=1, include_body=False)

# 4. Get body only when needed
serena.find_symbol(name_path="ClassName/method", include_body=True)

# 5. Trace dependencies
serena.find_referencing_symbols(name_path="ClassName/method")

# 6. Framework patterns
context7.get-library-docs("<framework>", topic="<topic>")
```

## Search Patterns

### By Name
```
serena.find_symbol("*Service", include_kinds=[5])      # Classes
serena.find_symbol("UserService/create", include_body=True)  # Method
```

### By Pattern (TOKEN CRITICAL - Always Scope!)

```python
# WRONG - Will return 20k+ tokens:
serena.search_for_pattern("@Cacheable|@cached")

# CORRECT - Scoped and limited:
serena.search_for_pattern(
    substring_pattern="@Cacheable",
    relative_path="module-core-domain/",
    context_lines_after=1,
    max_answer_chars=3000
)
```

### Dependencies
```
serena.find_referencing_symbols("UserService/create")  # Who calls this?
```

### Architecture
```
serena.search_for_pattern("import.*infra", relative_path="src/domain/")
```

### For Documentation
```
# Public APIs (classes, methods)
serena.get_symbols_overview(depth=1)                    # Module structure
serena.find_symbol("*Service", depth=1, include_body=False)  # Signatures

# Find existing docs
serena.find_file(file_mask="*.md", relative_path=".")
serena.find_file(file_mask="README*", relative_path=".")
```

## Output Format

```markdown
## Search: [Target]

| File | Symbol | Line | Type |
|------|--------|------|------|
| path/file | Class.method | 45 | function |

### Key Code
[Relevant snippet - max 20 lines]

### Dependencies
- Calls: [list]
- Called By: [list]
```

## Symbol Kinds

| Kind | Number | Description |
|------|--------|-------------|
| Class | 5 | Class definition |
| Method | 6 | Class method |
| Function | 12 | Standalone function |
| Interface | 11 | Interface |

## Efficiency Rules

**Do:**
- Start with `get_symbols_overview` before reading files
- Use `include_body=False` first
- Limit searches with `relative_path`

**Avoid:**
- Reading entire files before symbol search
- Fetching bodies for signature checks
- Broad searches without scope restriction
