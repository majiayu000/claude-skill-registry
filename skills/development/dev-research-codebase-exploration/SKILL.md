---
name: dev-research-codebase-exploration
description: Efficient codebase search using Glob and Grep
category: research
---

# Codebase Exploration

Efficiently explore the codebase using Glob and Grep tools.

## Glob Tool

Find files by pattern:

```bash
# Find all TypeScript files
Glob("**/*.ts")

# Find all TSX files
Glob("**/*.tsx")

# Find specific folders
Glob("src/components/**/*.tsx")
Glob("src/hooks/**/*.ts")

# Find files with keyword
Glob("**/*player*")
Glob("**/*physics*")
```

## Grep Tool

Search file contents:

```bash
# Search for specific text
Grep("useFrame", "src/")
Grep("useState", "src/")

# Case-insensitive search
Grep("COLYSEUS", "src/", { ignoreCase: true })

# Search with context
Grep("function.*movement", "src/", { context: 2 })
```

## Search Patterns

### Find Component Definitions
```bash
Grep("function.*Component|const.*=.*=>", "src/components/")
```

### Find State Stores
```bash
Glob("src/stores/**/*.ts")
Grep("create.*Store|zustand", "src/stores/")
```

### Find Type Definitions
```bash
Glob("src/types/**/*.ts")
Grep("interface.*|type.*=", "src/types/")
```

### Find Exports
```bash
Grep("export.*function|export.*const", "src/")
```

## Tips

1. **Start broad, then narrow** - Use Glob first, then Grep
2. **Use specific patterns** - More specific = faster results
3. **Check multiple locations** - Code may be in unexpected places
4. **Read related files** - Found patterns often have related code nearby

## Anti-Patterns

❌ **DON'T:**

- Use overly broad globs - `Glob("**/*")` is useless
- Search from root every time - Narrow to relevant directories
- Ignore file extensions - Searching `.md` files for code patterns wastes time
- Skip context - Reading just the matched line misses important context
- Search for common words - `Grep("const")` returns everything

✅ **DO:**

- Combine Glob + Grep - `Glob("src/**/*.ts")` then `Grep("pattern", "src/")`
- Use specific globs - `Glob("src/components/**/*.tsx")` instead of `Glob("**/*.tsx")`
- Search with context - `Grep("pattern", "src/", { context: 3 })`
- Filter by file type - Search `.ts` files for code, `.md` for docs
- Start from known locations - Check similar features first
