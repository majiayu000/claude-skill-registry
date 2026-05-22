---
name: large-file-refactor
description: Use when Claude Code hits "File content exceeds maximum allowed tokens" error, or when files are too large to read. Helps analyze and break apart large files into smaller, focused modules.
user-invocable: true
allowed-tools: Read, Glob, Grep, LSP, Edit, Write, Bash(wc:*)
---

# Large File Refactoring

Guide for analyzing and breaking apart files that exceed Claude Code's read limits.

## When This Applies

- **Token limit error**: "File content (X tokens) exceeds maximum allowed tokens (25000)"
- **Files > 2000 lines**: Likely to cause issues or be hard to maintain
- **User request**: "break apart", "split", "refactor large file"

## Quick Start Algorithm

### 1. Assess the File

```bash
# Get line count
wc -l <file>

# Get structure overview (Rust example)
grep -n "^pub fn\|^fn\|^impl\|^struct\|^enum\|^mod" <file>
```

Use `LSP documentSymbol` for accurate symbol outline.

### 2. Identify Natural Breakpoints

Look for cohesive groups:

- Related functions (CRUD operations, handlers, validators)
- Type + its impl blocks
- Feature-specific code
- Test modules

### 3. Plan the Breakout

**Target**: Each new file should be 200-500 lines (readable in one read).

| Pattern | When to Use |
|---------|-------------|
| Extract to submodule | Related impl blocks, feature code |
| Extract to sibling file | Independent utilities, types |
| Create package/directory | Multiple related modules |

### 4. Execute Refactor

1. Create new file(s)
2. Move code with `Read` (offset/limit) + `Write`
3. Update imports/exports
4. Update the original file's module declarations

### 5. Validate

- [ ] All imports resolve (LSP hover, no red squiggles)
- [ ] Tests pass
- [ ] No circular dependencies
- [ ] Original functionality preserved

## Analysis Without Full Read

When you can't read the whole file:

| Tool | Use For |
|------|---------|
| `Grep` | Find definitions: `^fn`, `^class`, `^def`, `impl` |
| `LSP documentSymbol` | Get complete symbol outline |
| `Read` with offset/limit | Read specific sections |
| `wc -l` | Total line count |

**Example workflow**:

```text
1. wc -l file.rs                    # 3500 lines
2. grep -n "^impl" file.rs          # Find impl blocks at lines 100, 800, 2000
3. LSP documentSymbol file.rs       # Get full structure
4. Read file.rs offset=100 limit=200  # Read first impl block
```

## Breakout Decision Matrix

| File Size | Recommendation |
|-----------|----------------|
| < 500 lines | Usually fine as-is |
| 500-1000 lines | Consider splitting if multiple concerns |
| 1000-2000 lines | Should split unless highly cohesive |
| > 2000 lines | Must split for maintainability |

## Language-Specific Patterns

See `@large-file-refactor/references/breakout-patterns.md` for detailed examples.

| Language | Primary Pattern |
|----------|-----------------|
| Rust | Submodules in directory, re-export from mod.rs |
| TypeScript | Separate files, barrel export from index.ts |
| Python | Package with **init**.py |
| Go | Multiple files in same package |

## Common Pitfalls

1. **Breaking public API**: Ensure exports remain accessible
2. **Circular imports**: Plan dependency direction before splitting
3. **Lost context**: Keep related code together (don't over-split)
4. **Forgetting tests**: Move/update test imports too

## References

- `@large-file-refactor/references/analysis-strategies.md` - Detailed analysis techniques
- `@large-file-refactor/references/breakout-patterns.md` - Language-specific examples
- `@large-file-refactor/references/validation-checklist.md` - Pre/post refactor checks
