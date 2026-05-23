---
name: Codebase Organizer
description: Monitor and refactor large files into smaller, AI-friendly modules. Use when user asks to check file sizes, split large files, or organize the codebase. Ensures tests pass before and after refactoring.
---

# Codebase Organizer

Maintain optimal file sizes for AI-assisted development by splitting large files into focused modules.

## Quick Start

**Most common usage:**
```bash
# Check file sizes
make report-file-sizes

# If files >800 lines found:
# 1. Analyze structure
# 2. Plan split
# 3. Execute with test validation
```

## When to Use This Skill

Invoke when user says:
- "Check file sizes" / "report file sizes"
- "Split this file" / "refactor large file"
- "Organize the codebase"
- "Make files AI-friendly"

## File Size Targets

| Size | Status | Action |
|------|--------|--------|
| 200-500 lines | Sweet spot | None needed |
| 500-800 lines | Acceptable | Consider splitting |
| >800 lines | **CRITICAL** | Must split |

## Workflow

### Step 1: Status Check

```bash
# Find all large files
make report-file-sizes

# Or manually:
find internal -name "*.go" -exec wc -l {} \; | awk '$1 > 500 {print}' | sort -rn
```

**Output format:**
```
=== File Size Report ===

CRITICAL (>800 lines):
  internal/types/typechecker_core.go: 2736 lines
  internal/parser/parser.go: 2518 lines

WARNING (500-800 lines):
  internal/eval/eval_core.go: 765 lines
```

### Step 2: Plan the Split

Before ANY refactoring:

1. **Run baseline tests**: `make test`
2. **Identify natural boundaries**:
   - Expression parsing vs statement parsing
   - Type inference vs type checking
   - Different AST node types
   - Public API vs internal helpers

3. **Plan file names** (match to primary functions):
   - `expressions.go` → `parseExpression()`, `parseCall()`
   - `statements.go` → `parseStatement()`, `parseLetDecl()`
   - `helpers.go` → utility functions

4. **Check for circular dependency risks**

### Step 3: Execute Split

```bash
# 1. Create new files with clear names
# 2. Move related functions together (maintain cohesion)
# 3. Update imports in all affected files
# 4. Keep main struct in pkg.go
```

**Keep together:**
- Tightly coupled functions
- Helper functions used by one main function
- Functions that share complex state

### Step 4: Validate

```bash
# MUST run after every split
make test              # All tests must pass
make lint              # No linting errors
make check-file-sizes  # Verify all <800 lines
```

**If tests fail:**
1. DO NOT COMMIT
2. Analyze failure (missing import? broken reference?)
3. Fix issue
4. Re-run tests
5. Only commit when tests pass

### Step 5: Document & Commit

Update package documentation:
```go
// Package parser implements AILANG source code parsing.
//
// # Architecture
//
// The parser is split into several files:
//   - parser.go: Main struct and entry points
//   - expressions.go: Expression parsing
//   - statements.go: Statement parsing
```

Commit with descriptive message:
```bash
git add internal/path/*.go
git commit -m "Split path/file.go into N files (AI-friendly)

- parser.go: Main struct (200 lines)
- expressions.go: Expression parsing (450 lines)
..."
```

## Error Handling

### Circular Dependency

If split creates circular dependency:

1. **Identify cycle**: File A imports B, File B imports A
2. **Solutions**:
   - Extract shared code to new file (e.g., `types.go`)
   - Use interfaces to break dependency
   - Restructure to have one-way dependency
   - Merge files if truly inseparable (<800 lines combined)

### Test Failures

Common issues after split:
- Missing import in new file
- Function moved but still referenced in old location
- Test file not updated to match new structure

## Example Session

**User**: "Check codebase organization"

**Response**:
```
Running make report-file-sizes...

=== File Size Report ===

CRITICAL (>800 lines):
  internal/parser/parser.go: 2518 lines

WARNING (500-800 lines):
  internal/eval/eval_core.go: 765 lines

Recommendation: Split internal/parser/parser.go into ~6 focused files.
Would you like me to analyze and propose a split plan?
```

**User**: "Yes, split parser.go"

**Response**:
```
Analyzing internal/parser/parser.go (2518 lines)...

Proposed split:
  parser.go (200 lines) - Main struct, entry points
  expressions.go (450 lines) - Expression parsing
  statements.go (400 lines) - Declaration parsing
  types.go (300 lines) - Type annotation parsing
  patterns.go (350 lines) - Pattern parsing
  modules.go (300 lines) - Module system
  helpers.go (200 lines) - Utilities

Proceed? Tests will run before and after.
```

## Success Metrics

After refactoring:
- 0 files over 800 lines
- <5 files between 500-800 lines
- Average file size: 300-400 lines
- 100% test pass rate maintained

## Important Reminders

- **ALWAYS run tests before and after refactoring**
- **NEVER commit if tests fail**
- **One refactoring at a time** (easier to debug)
- **Show plan before executing** (get user approval)
- **Keep related functions together** (maintain cohesion)
