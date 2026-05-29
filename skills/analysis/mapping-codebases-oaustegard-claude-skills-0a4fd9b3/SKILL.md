---
name: mapping-codebases
description: Generate navigable code maps for unfamiliar codebases. Use when exploring a new codebase, needing to understand project structure, or before diving into code modifications. Extracts exports/imports via AST (tree-sitter) to create _MAP.md files per directory. Triggers on "map this codebase", "understand this project structure", "generate code map", or when starting work on an unfamiliar repository.
metadata:
  version: 0.5.0
---

# Mapping Codebases

Generate `_MAP.md` files that provide a hierarchical view of code structure without reading every file.

## Installation

**CRITICAL - Use uv for dependency installation in Claude Code:**

```bash
# In Claude Code environments, ALWAYS use uv with --system flag:
uv pip install --system tree-sitter-language-pack

# Only fall back to pip if uv is not available
```

**Why uv?** Claude Code environments have uv pre-installed for efficient package management. Using uv is faster and preferred.

## Quick Start

```bash
# Generate maps for a codebase
python scripts/codemap.py /path/to/repo
```

## What It Produces

Per-directory `_MAP.md` files listing:
- Directory statistics (file count, subdirectory count)
- Subdirectories (with links to their maps)
- **Symbol hierarchy** with kind markers: (C) class, (m) method, (f) function
- **Function signatures** extracted from AST (Python, partial TypeScript)
- **Line number references** (`:42` format) for direct navigation
- Import previews
- **Markdown ToC** for `.md` files (h1/h2 headings only for brevity)
- **Other Files** section listing non-code files (JSON, YAML, shell scripts, etc.)

Example output:
```markdown
# auth/
*Files: 5 | Subdirectories: 1*

## Subdirectories
- [middleware/](./middleware/_MAP.md)

## Files

### handlers.py
> Imports: `flask, functools, jwt, .models`...
- **login** (f) `(username: str, password: str)` :15
- **logout** (f) `()` :42
- **AuthHandler** (C) :58
  - **__init__** (m) `(self, config: dict)` :59
  - **validate_token** (m) `(self, token: str)` :72
  - **refresh_session** (m) `(self, user_id: int)` :95

### README.md
- Authentication Module `h1` :1
- Installation `h2` :5
- Configuration `h2` :12

## Other Files
- config.yaml
- setup.sh
```

## Supported Languages

Python, JavaScript, TypeScript, TSX, Go, Rust, Ruby, Java, HTML, Markdown.

## Commands

```bash
python scripts/codemap.py /path/to/repo                    # Generate maps
python scripts/codemap.py /path/to/repo --skip locale,tests # Skip specific directories
python scripts/codemap.py /path/to/repo --clean             # Remove all _MAP.md
python scripts/codemap.py /path/to/repo -n                  # Dry run (preview)
```

### Skip Patterns

Use `--skip` to exclude directories that add noise without value:

```bash
# Common patterns
--skip locale,migrations,tests              # Django projects
--skip locales,__snapshots__,coverage       # JavaScript projects
--skip target,docs                          # Rust projects
```

Default skip patterns: `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`, `.next`

## Workflow Integration

1. Run `codemap.py` on the target repo first
2. Read `_MAP.md` at repo root for overview (high-level structure)
3. Navigate to relevant subdirectory maps as needed (drill down)
4. Read actual source files only when necessary

Maps use hierarchical disclosure - you only load what you need. Even massive codebases (1000+ files) stay navigable because each map remains focused on its directory.

## Post-Generation: Making Maps Persistent

**CRITICAL - After generating maps, integrate them into the development workflow:**

### In Claude Code Environments (Persistent Repos)

After generating `_MAP.md` files, **ALWAYS** update or create the repository's `CLAUDE.md` file to document the maps:

```bash
# Check if CLAUDE.md exists in the repo root
if [ -f CLAUDE.md ]; then
    # Add a section about the code maps (if not already present)
    echo "Found existing CLAUDE.md - will add _MAP.md documentation"
else
    # Create CLAUDE.md with map documentation
    echo "No CLAUDE.md found - will create one with map documentation"
fi
```

**Add this section to CLAUDE.md:**

```markdown
## Code Maps

This repository has navigable code maps generated via the mapping-codebases skill.

### Using the Maps

- Start with `_MAP.md` at the repository root for a high-level overview
- Each directory has its own `_MAP.md` showing:
  - Subdirectory links for hierarchical navigation
  - File-level symbol exports (classes, functions, methods)
  - Import previews
  - Function signatures (Python, partial TypeScript)

### Keeping Maps Fresh

Maps are generated from AST analysis and can drift from source code. To refresh:

```bash
python /path/to/mapping-codebases/scripts/codemap.py .
```

Consider adding a git pre-commit hook to auto-update maps (see mapping-codebases skill documentation).
```

**Why this matters:** Claude Code sessions are persistent. Documenting the maps in CLAUDE.md ensures future Claude instances (and developers) know the maps exist and how to use/maintain them.

### In Claude.ai Chat Environments (Ephemeral)

If working in a Claude.ai chat session (web/mobile):

1. **Use the maps immediately** - the session is ephemeral, so use them while they exist
2. **Tell the user** to add instructions to their Project Instructions if they want to use maps in future conversations:

```
I've generated _MAP.md files for this codebase. Since this is an ephemeral session,
these maps won't persist to the next conversation. If you want to use code maps in
future conversations, add this to your Project Instructions:

"When exploring this codebase, first invoke the mapping-codebases skill to generate
_MAP.md files, then navigate using those hierarchical maps rather than reading all
source files directly."
```

### Environment Detection

To determine which environment you're in:

- **Claude Code**: Working directory is a git repository with persistent filesystem access
- **Claude.ai Chat**: Files are uploaded/temporary, no git context, ephemeral session

Use this to decide whether to update CLAUDE.md (Claude Code) or recommend Project Instructions (Claude.ai).

## Features

**Symbol Hierarchy**: Shows classes with nested methods, not just flat lists. See the structure at a glance with kind markers (C/m/f).

**Function Signatures**: Extracts parameter lists from Python and partial TypeScript, showing what functions expect without reading the source.

**Line Number References**: Every symbol includes its line number (`:42` format), enabling direct navigation to definitions using `file:line` patterns.

**Markdown ToC**: Extracts h1 and h2 headings from `.md` files with line numbers, creating navigable documentation maps without the noise of deeper heading levels.

**Other Files Section**: Lists non-code files (JSON, YAML, shell scripts, config files) that exist in the directory but aren't parsed for symbols.

**Directory Statistics**: Each map header shows file and subdirectory counts, helping you quickly assess scope.

**Hierarchical Navigation**: Links between maps let you traverse the codebase structure naturally without overwhelming context windows.

**Skip Patterns**: Exclude noise directories (locales with 100+ language subdirs, test snapshots, generated code) to focus maps on actual source code.

## Git Hook (Optional)

For repos where maps should stay fresh:

```bash
# .git/hooks/pre-commit
#!/bin/sh
python /path/to/codemap.py . >/dev/null
git add '*/_MAP.md'
```

## Limitations

- Extracts structural info only (symbols/imports), not semantic descriptions
- Method extraction: Full support for Python/TypeScript, partial for other languages
- Signatures: Python (full), TypeScript (partial), others (not extracted)
- Markdown: Extracts h1/h2 headings only (deeper levels excluded for brevity)
- Skips: `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `build` (plus user-specified patterns)
- Private symbols (Python `_prefix`) excluded from top-level exports (methods not filtered yet)
