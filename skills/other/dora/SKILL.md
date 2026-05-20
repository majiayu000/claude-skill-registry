---
name: dora
description: Query codebase using `dora` CLI for code intelligence, symbol definitions, dependencies, and architectural analysis
---

## Philosophy

**IMPORTANT: Use dora FIRST for ALL code exploration tasks.**

dora understands code structure, dependencies, symbols, and architectural relationships through its indexed database. It provides instant answers about:

- Where symbols are defined and used
- What depends on what (and why)
- Architectural patterns and code health
- Impact analysis for changes

**When to use dora vs other tools:**

- **dora**: Code exploration, symbol search, dependency analysis, architecture understanding
- **Read**: Reading actual source code after finding it with dora
- **Grep**: Only for non-code files, comments, or when dora doesn't have what you need
- **Edit/Write**: Making changes after understanding with dora
- **Bash**: Running tests, builds, git commands

**Workflow pattern:**

1. Use dora to understand structure and find relevant code
2. Use Read to examine the actual source
3. Use Edit/Write to make changes
4. Use Bash to test/verify

## Commands

### Overview

- `dora status` - Check index health, file/symbol counts, last indexed time
- `dora map` - Show packages, file count, symbol count

### Files & Symbols

- `dora ls [directory] [--limit N] [--sort field]` - List files in directory with metadata (symbols, deps, rdeps). Default limit: 100
- `dora file <path>` - Show file's symbols, dependencies, and dependents. Note: includes local symbols (parameters).
- `dora symbol <query> [--kind type] [--limit N]` - Find symbols by name across codebase
- `dora refs <symbol> [--kind type] [--limit N]` - Find all references to a symbol
- `dora exports <path>` - List exported symbols from a file. Note: includes function parameters.
- `dora imports <path>` - Show what a file imports

### Dependencies

- `dora deps <path> [--depth N]` - Show file dependencies (what this imports). Default depth: 1
- `dora rdeps <path> [--depth N]` - Show reverse dependencies (what imports this). Default depth: 1
- `dora adventure <from> <to>` - Find shortest dependency path between two files

### Code Health

- `dora leaves [--max-dependents N]` - Find files with few/no dependents. Default: 0
- `dora lost [--limit N]` - Find unused exported symbols. Default limit: 50
- `dora treasure [--limit N]` - Find most referenced files and files with most dependencies. Default: 10

### Architecture Analysis

- `dora cycles [--limit N]` - Detect circular dependencies. Empty = good. Default: 50
- `dora coupling [--threshold N]` - Find bidirectionally dependent file pairs. Default threshold: 5
- `dora complexity [--sort metric]` - Show file complexity (symbol_count, outgoing_deps, incoming_deps, stability_ratio, complexity_score). Sort by: complexity, symbols, stability. Default: complexity

### Change Impact

- `dora changes <ref>` - Show files changed since git ref and their impact
- `dora graph <path> [--depth N] [--direction type]` - Generate dependency graph. Direction: deps, rdeps, both. Default: both, depth 1

### Documentation

- `dora docs [--type TYPE]` - List all documentation files. Use --type to filter by md or txt
- `dora docs search <query> [--limit N]` - Search through documentation content. Default limit: 20
- `dora docs show <path> [--content]` - Show document metadata and references. Use --content to include full text

**Note:** To find where a symbol is documented, use `dora symbol` which includes a `documented_in` field. To find documentation about a file, use `dora file` which also includes `documented_in`.

### Database

- `dora schema` - Show database schema (tables, columns, indexes)
- `dora cookbook show [recipe]` - Query patterns with real examples (quickstart, methods, references, exports)
- `dora query "<sql>"` - Execute read-only SQL query against the database

## When to Use What

- Finding symbols → `dora symbol`
- Understanding a file → `dora file`
- Impact of changes → `dora rdeps`, `dora refs`
- Finding entry points → `dora treasure`, `dora leaves`
- Architecture issues → `dora cycles`, `dora coupling`, `dora complexity`
- Navigation → `dora deps`, `dora adventure`
- Dead code → `dora lost`
- Finding documentation → `dora symbol` (shows documented_in), `dora docs search`
- Listing documentation → `dora docs`
- Custom queries → `dora cookbook` for examples, `dora schema` for structure, `dora query` to execute

## Typical Workflow

1. `dora status` - Check index health
2. `dora treasure` - Find core files
3. `dora file <path>` - Understand specific files
4. `dora deps`/`dora rdeps` - Navigate relationships
5. `dora refs` - Check usage before changes

## Common Patterns: DON'T vs DO

Finding where a symbol is defined:

```bash
# DON'T: grep -r "class AuthService" .
# DON'T: grep -r "function validateToken" .
# DON'T: Glob("**/*.ts") then search each file
# DO:
dora symbol AuthService
dora symbol validateToken
```

Finding all usages of a function/class:

```bash
# DON'T: grep -r "AuthService" . --include="*.ts"
# DON'T: Grep("AuthService", glob="**/*.ts")
# DO:
dora refs AuthService
```

Finding files that import a module:

```bash
# DON'T: grep -r "from.*auth/service" .
# DON'T: grep -r "import.*AuthService" .
# DO:
dora rdeps src/auth/service.ts
```

Finding what a file imports:

```bash
# DON'T: grep "^import" src/app.ts
# DON'T: cat src/app.ts | grep import
# DO:
dora deps src/app.ts
dora imports src/app.ts
```

Finding files in a directory:

```bash
# DON'T: find src/components -name "*.tsx"
# DON'T: Glob("src/components/**/*.tsx")
# DO:
dora ls src/components
dora ls src/components --sort symbols  # With metadata
```

Finding entry points or core files:

```bash
# DON'T: grep -r "export.*main" .
# DON'T: find . -name "index.ts" -o -name "main.ts"
# DO:
dora treasure           # Most referenced files
dora file src/index.ts  # Understand the entry point
```

Understanding a file's purpose:

```bash
# DON'T: Read file, manually trace imports
# DON'T: grep for all imports, then read each
# DO:
dora file src/auth/service.ts   # See symbols, deps, rdeps at once
```

Finding unused code:

```bash
# DON'T: grep each export manually across codebase
# DON'T: Complex script to track exports vs imports
# DO:
dora lost     # Unused exported symbols
dora leaves   # Files with no dependents
```

Checking for circular dependencies:

```bash
# DON'T: Manually trace imports in multiple files
# DON'T: Write custom script to detect cycles
# DO:
dora cycles
```

Impact analysis for refactoring:

```bash
# DON'T: Manually grep for imports and usages
# DON'T: Read multiple files to understand impact
# DO:
dora rdeps src/types.ts --depth 2     # See full impact
dora refs UserContext                 # All usages
dora complexity --sort complexity     # Find risky files
```

Finding documentation for code:

```bash
# DON'T: grep -r "AuthService" docs/
# DON'T: Manually search through README files
# DO:
dora symbol AuthService                 # Shows documented_in field
dora file src/auth/service.ts           # Shows documented_in field
dora docs search "authentication"       # Search doc content
dora docs                               # List all docs
```

Understanding what a document covers:

```bash
# DON'T: Read entire doc, manually trace references
# DON'T: grep for symbol names in the doc
# DO:
dora docs show README.md                # See all symbols/files/docs referenced
dora docs show docs/api.md --content    # Include full content
```

## Practical Examples

Understanding a feature:

```bash
dora symbol AuthService              # Find the service
dora file src/auth/service.ts        # See what it depends on
dora rdeps src/auth/service.ts       # See what uses it
dora refs validateToken              # Find all token validation usage
```

Impact analysis before refactoring:

```bash
dora file src/types.ts               # See current dependencies
dora rdeps src/types.ts --depth 2    # See full impact tree
dora refs UserContext                # Find all usages of the type
dora complexity --sort stability     # Find stable vs volatile files
```

Finding dead code:

```bash
dora lost --limit 100                # Unused exported symbols
dora leaves                          # Files nothing depends on
dora file src/old-feature.ts         # Verify it's truly unused
```

Architecture investigation:

```bash
dora cycles                          # Check for circular deps (should be empty)
dora coupling --threshold 10         # Find tightly coupled modules
dora complexity --sort complexity    # Find complex/risky files
dora treasure                        # Find architectural hubs
```

Navigating unfamiliar code:

```bash
dora map                             # Overview of packages and structure
dora treasure                        # Find entry points and core files
dora file src/index.ts               # Start from main entry
dora deps src/index.ts --depth 2     # See what it depends on
dora adventure src/a.ts src/b.ts     # Find connection between modules
```

Working with changes:

```bash
dora changes main                    # See what changed vs main branch
dora rdeps src/modified.ts           # Check impact of your changes
dora graph src/modified.ts --depth 2 # Visualize dependency tree
```

Custom analysis:

```bash
dora cookbook show methods                # See query pattern examples
dora schema                          # See database structure
dora query "SELECT f.path, COUNT(s.id) as symbols FROM files f JOIN symbols s ON s.file_id = f.id WHERE s.is_local = 0 GROUP BY f.path ORDER BY symbols DESC LIMIT 20"
```

Working with documentation:

```bash
dora symbol AuthService              # Shows documented_in field
dora docs show README.md             # What does README reference?
dora docs search "setup"             # Find all docs about setup
dora docs                            # List all documentation files
dora docs --type md                  # List only markdown docs
```

## Advanced Tips

Performance:

- dora uses denormalized data for instant queries (symbol_count, reference_count, dependent_count)
- Incremental indexing only reindexes changed files
- Use `--limit` to cap results for large codebases

Symbol filtering:

- Local symbols (parameters, closure vars) are filtered by default with `is_local = 0`
- Use `--kind` to filter by symbol type (function, class, interface, type, etc.)
- Symbol search is substring-based, not fuzzy

Dependencies:

- `deps` shows outgoing dependencies (what this imports)
- `rdeps` shows incoming dependencies (what imports this)
- Use `--depth` to explore transitive dependencies
- High rdeps count = high-impact file (changes affect many files)

Architecture metrics:

- `complexity_score = symbol_count × incoming_deps` (higher = riskier to change)
- `stability_ratio = incoming_deps / outgoing_deps` (higher = more stable)
- Empty `cycles` output = healthy architecture
- High `coupling` (> 20 symbols) = consider refactoring

Documentation:

- Automatically indexes `.md` and `.txt` files
- Tracks symbol references (e.g., mentions of `AuthService`)
- Tracks file references (e.g., mentions of `src/auth/service.ts`)
- Tracks document-to-document references (e.g., README linking to docs/api.md)
- Use `dora symbol` or `dora file` to see where code is documented (via `documented_in` field)
- Use `dora docs` to list all documentation files
- Use `dora docs show` to see what a document covers with line numbers

## Limitations

- Includes local symbols (parameters) in `dora file` and `dora exports`
- Symbol search is substring-based, not fuzzy
- Index is a snapshot, updates at checkpoints
- Documentation indexing processes text files (.md, .txt, etc.) at index time
