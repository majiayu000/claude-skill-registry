---
name: lsp-refactoring
description: Intelligent code refactoring using IDE-level tools (rename, find-references, go-to-definition), AST-aware pattern matching, and TDD verification. Use for safe, large-scale refactoring with precision.
---

# LSP Refactoring

Refactoring workflow that combines language server capabilities with code search and test-driven verification for safe, precise code transformations.

## When to Use This Skill

- Renaming symbols across an entire workspace
- Extracting functions, classes, or modules
- Moving code between files with automatic reference updates
- Large-scale pattern-based code transformations
- Any refactoring where manual find-replace is error-prone

## What This Skill Does

### Phase 1: Analysis — Understand Before Changing

1. **Scope assessment**: Find all usages of the target symbol using grep or IDE references
2. **Dependency graph**: Trace where the symbol is defined and what depends on it
3. **Impact analysis**: Identify all files that will be affected
4. **Pattern discovery**: Search for similar patterns that should be refactored consistently

```bash
# Find all usages of a function
grep -rn "getUserData" src/ --include="*.ts"

# Find pattern across codebase with AST-aware tools (if available)
# e.g., ast-grep, semgrep, or comby
ast-grep --pattern 'console.log($MSG)' --lang typescript
```

### Phase 2: Plan — Design the Transformation

1. **Pre-flight check**: Run the type checker / linter to capture baseline errors
2. **Rename validation**: Verify the symbol can be safely renamed (no conflicts)
3. **Transformation plan**: List each change with file, line, before/after
4. **Test identification**: Find tests covering the code being refactored

### Phase 3: Execute — Apply Changes Safely

**For renames (use IDE/editor capabilities when available):**
```bash
# Using sed for simple renames
find src/ -name "*.ts" -exec sed -i '' 's/getUserData/fetchUserProfile/g' {} +

# Or use language-specific tools
# TypeScript: ts-morph, jscodeshift
# Python: rope, bowler
# Go: gorename
```

**For pattern-based transformations:**
```bash
# Using ast-grep (if installed)
ast-grep --pattern 'console.log($MSG)' --rewrite 'logger.info($MSG)' --lang typescript

# Using comby
comby 'console.log(:[msg])' 'logger.info(:[msg])' .ts
```

**For structural changes (extract/move):**
1. Create the new target (file, function, class)
2. Move the code
3. Update all references using LSP rename
4. Remove the old code
5. Verify no dangling references

### Phase 4: Verify — TDD Confirmation

1. **Type check**: Run the project type checker — must be clean
   ```bash
   npx tsc --noEmit          # TypeScript
   mypy src/                  # Python
   go vet ./...               # Go
   ```
2. **Build check**: Run project build — must pass
3. **Test check**: Run test suite — all previously passing tests must still pass
4. **Diff review**: `git diff` to review the complete changes for unintended modifications

If any check fails:
- Revert changes: `git checkout -- .`
- Analyze the failure
- Adjust approach and retry

## Approach by Language

| Language | Rename Tool | Pattern Search | Type Check |
|----------|-------------|----------------|------------|
| TypeScript | `ts-morph`, `jscodeshift` | `ast-grep`, `semgrep` | `tsc --noEmit` |
| Python | `rope`, `bowler` | `ast-grep`, `semgrep` | `mypy`, `pyright` |
| Go | `gorename`, `gopls` | `ast-grep`, `semgrep` | `go vet` |
| Java | IntelliJ refactor, `openrewrite` | `semgrep` | `javac` |
| Rust | `rust-analyzer` | `ast-grep` | `cargo check` |

## Anti-Patterns

- Manual find-replace without verifying all references — misses dynamic usages
- Skipping type check after rename — may introduce type errors
- Not running tests after refactoring — behavior may have changed
- Refactoring while fixing bugs — do one or the other, never both

## Example

**User**: "Rename getUserData to fetchUserProfile across the project"

**Output**:
1. `grep -rn` finds 23 usages across 8 files
2. Applies rename using sed/jscodeshift across all locations
3. `tsc --noEmit` passes with no errors
4. `npm test` — 47 tests pass
5. `git diff` shows clean, focused changes

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) /refactor command
