---
name: unified-search-discover
description: Progressive search and discovery with structured refinement workflows for file finding, content searching, and safe refactoring operations using fd/find, rg/grep, and ast-grep tools. Use when searching, discovering, or refactoring code with progressive refinement patterns.
allowed-tools:
  - Bash(fd *)
  - Bash(find *)
  - Bash(rg *)
  - Bash(grep *)
  - Bash(ast-grep *)
  - Read
  - Write
  - Edit
---

## Purpose

Provide progressive search and discovery workflows with structured refinement patterns that assess scope before execution. Enable safe, efficient file discovery, content searching, and code refactoring through COUNT → PREVIEW → EXECUTE methodology.

## Quick Decision Guide

### File Discovery: fd vs find

**Use `fd` when:**
- Need gitignore-aware file discovery (default preference)
- Performance is critical (5-10x faster than find)
- Working with modern development environments

**Use `find` when:**
- Need to discover hidden/ignored files
- System lacks `fd` installation
- Require POSIX compatibility

### Text Search: ast-grep vs rg vs grep

**Use `ast-grep` when:**
- Structural code analysis required
- Refactoring with language awareness
- Need AST pattern matching

**Use `rg` when:**
- Fast text search across many files
- Regex pattern matching needed
- Performance-critical searches

**Use `grep` when:**
- Maximum compatibility required
- Minimal system environments
- Simple text patterns

## Progressive Refinement Pattern

ALWAYS follow this 3-step pattern for search operations:

### Step 1: COUNT - Assess Scope

Count results before displaying to prevent overwhelming output:
```bash
# File discovery scope
fd --type ts | wc -l
find . -name "*.ts" | wc -l

# Text search scope
rg "function" --count --type ts
grep -r "function" --include="*.ts" | wc -l

# Structural analysis scope
ast-grep --pattern 'function $NAME()' --dry-run --json | jq '.matches | length'
```

### Step 2: PREVIEW - Validate with Limited Results

Show representative samples to confirm pattern accuracy:
```bash
# File discovery preview
fd --type ts | head -10
find . -name "*.ts" | head -10

# Text search preview with context
rg "function" --type ts -A 2 -B 2 | head -20

# Structural analysis preview
ast-grep --pattern 'function $NAME()' --dry-run -A 1 -B 1
```

### Step 3: EXECUTE - Apply with Full Awareness

Execute full search only after scope validation:
```bash
# Full file discovery
fd --type ts -x rg "pattern"

# Full text search
rg "function" --type ts -A 2 -B 2

# Full structural analysis
ast-grep --pattern 'function $NAME()' -A 2 -B 2
```

## Tool-Specific Guidelines

### File Discovery with fd/find

**Preferred: fd (gitignore-aware, fast)**
```bash
# COUNT: Assess TypeScript file scope
fd --type ts | wc -l

# PREVIEW: Show sample files
fd --type ts | head -10

# EXECUTE: Full discovery with execution
fd --type ts -x rg "import.*React"

# Advanced patterns
fd --type ts --exclude "node_modules"  # Additional exclusions
fd --type ts --hidden                  # Include hidden files
```

**Fallback: find (maximum compatibility)**
```bash
# COUNT: Assess file scope
find . -name "*.ts" -not -path "*/node_modules/*" | wc -l

# PREVIEW: Sample files
find . -name "*.ts" -not -path "*/node_modules/*" | head -10

# EXECUTE: Full discovery
find . -name "*.ts" -not -path "*/node_modules/*" -exec grep "pattern" {} +
```

### Text Search with rg/grep

**Preferred: rg (fast, modern)**
```bash
# COUNT: Scope assessment
rg "console\.log" --count --type ts

# PREVIEW: Context samples
rg "console\.log" --type ts -A 1 -B 1 | head -20

# EXECUTE: Full search with context
rg "console\.log" --type ts -A 2 -B 2 --line-number

# Advanced patterns
rg "function" --type ts --word-boundary    # Whole words only
rg "import.*React" --type ts --context 3  # 3 lines context
```

**Fallback: grep (maximum compatibility)**
```bash
# COUNT: Scope assessment
grep -r "console\.log" --include="*.ts" | wc -l

# PREVIEW: Context samples
grep -r -n -A 1 -B 1 "console\.log" --include="*.ts" | head -20

# EXECUTE: Full search
grep -r -n -A 2 -B 2 "console\.log" --include="*.ts"
```

### Structural Analysis with ast-grep

**Language-aware pattern matching for refactoring:**
```bash
# COUNT: Assess refactoring impact
ast-grep --pattern 'import $NAME from "./old-path"' --dry-run --json | jq '.matches | length'

# PREVIEW: Show sample changes
ast-grep --pattern 'import $NAME from "./old-path"' --dry-run -A 1 -B 1

# EXECUTE: Safe refactoring with backup
cp -r src/ src-backup-$(date +%s)/
ast-grep --pattern 'import $NAME from "./old-path"' --rewrite 'import $NAME from "./new-path"'

# Common refactoring patterns
ast-grep --pattern 'console.log($MSG)' --rewrite ''  # Remove console logs
ast-grep --pattern 'var $NAME = $VALUE' --rewrite 'let $NAME = $VALUE'  # var to let
```

## Refactoring Workflows

### Discovery → Search → Analyze → Refactor Pipeline

**Phase 1: Discovery**
```bash
# Find all relevant files
fd --type ts src/ | wc -l  # COUNT
fd --type ts src/ | head -10  # PREVIEW
```

**Phase 2: Search**
```bash
# Locate patterns in discovered files
fd --type ts src/ -x rg "console\.log" --count-matches  # COUNT
fd --type ts src/ -x rg "console\.log" -A 1 -B 1 | head -20  # PREVIEW
```

**Phase 3: Analysis**
```bash
# Structural verification
ast-grep --pattern 'console.log($MSG)' --dry-run --json | jq '.matches | length'  # COUNT
ast-grep --pattern 'console.log($MSG)' --dry-run -A 1 -B 1  # PREVIEW
```

**Phase 4: Refactor**
```bash
# Safe execution with backup
cp -r src/ src-backup-$(date +%s)/  # Backup
ast-grep --pattern 'console.log($MSG)' --rewrite ''  # EXECUTE
```

### Safety Protocols for Refactoring

**Before any refactoring:**
1. COUNT - Always assess impact scope first
2. PREVIEW - Review sample changes before execution
3. BACKUP - Create timestamped backups
4. DRY-RUN - Use `--dry-run` with ast-grep for verification
5. TEST - Apply changes to small subset first

**After refactoring:**
1. VERIFY - Confirm changes applied correctly
2. TEST - Run tests to ensure functionality preserved
3. CLEANUP - Remove backups after verification

## Performance Optimization

### Large Codebase Strategies

```bash
# Parallel execution with xargs
fd --type ts | xargs -P 4 -I {} rg "pattern" {}

# Memory-efficient searches
rg --max-filesize 1M "pattern"  # Skip large files
find . -name "*.log" -prune -o -name "*.ts" -print  # Exclude logs

# Incremental searches
rg --type ts "pattern" | head -100  # Limit initial results
```

### Platform Considerations

- macOS: Use `gnu-sed`, `gnu-find` for consistency
- Linux: Standard GNU tools typically available
- Windows: Use WSL or Git Bash for Unix tooling

## Integration Points

### Environment Validation

Always couple with `skill:environment-validation` to check tool availability:
```bash
# Tool availability check
fd --version && rg --version && ast-grep --version
```

### Language-Specific Integration

- TypeScript: `--type ts`, `.ts/.tsx` patterns
- Python: `--type py`, `.py` patterns
- JavaScript: `--type js`, `.js/.jsx` patterns
- Go: `--type go`, `.go` patterns

### Agent Workflow Integration

- **Discovery Phase**: File enumeration with fd/find
- **Analysis Phase**: Content searching with rg/grep
- **Refactoring Phase**: Structural changes with ast-grep
- **Verification Phase**: Pattern validation across all tools