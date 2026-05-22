---
name: tech-debt
description: This skill should be used when the user asks to "find dead code", "remove unused code", "clean up tech debt", "find duplicates", "identify unused functions", "kill dead code", or mentions tech debt cleanup, code cruft, or unused exports. Provides automated detection and removal of dead code, duplicates, and code quality issues with archive-based safety.
---

# Tech Debt Hunter

## Overview

Automatically detect and remove technical debt from codebases: dead code, unused exports, duplicate functions, accumulated TODOs, and complexity hotspots. All removals are archived for safety—aggressive action with a recovery net.

**Core principle:** Detect the stack, use appropriate tools, archive before removing, report what was killed.

## When to Use

- Starting a refactor or cleanup sprint
- Codebase feels bloated with unused code
- Before major feature work to reduce noise
- User mentions "tech debt", "dead code", "cleanup", "unused"

## Stack Detection

Detect project type by checking for marker files:

| Marker | Stack | Tools |
|--------|-------|-------|
| `package.json` + `tsconfig.json` | TypeScript | ts-prune, eslint, knip |
| `package.json` (no tsconfig) | JavaScript | eslint, knip |
| `requirements.txt` or `pyproject.toml` | Python | vulture, flake8, pylint |
| `Cargo.toml` | Rust | cargo-udeps, clippy |
| `go.mod` | Go | staticcheck, deadcode |

For mixed repos, run appropriate tools for each detected stack.

## Detection Categories

### Tier 1: Auto-Kill (100% safe)

Remove immediately, archive for safety:

- **Unused imports** - Detected by linters, never referenced
- **Unreachable code** - After return/throw, dead branches
- **Commented-out code blocks** - `// old implementation` cruft
- **Empty files** - Source files with no exports/definitions
- **Unused private functions** - Private/unexported, zero internal refs

### Tier 2: Archive (High confidence)

Remove with archive, report in summary:

- **Unused exports** - Exported but never imported elsewhere
- **Dead functions** - Defined but never called
- **Duplicate code blocks** - >20 lines with >90% similarity
- **Unused variables** - Declared but never read
- **Deprecated API usage** - Using removed/deprecated APIs

### Tier 3: Report Only (Needs review)

Flag for manual review, do not auto-remove:

- **High complexity functions** - Cyclomatic complexity >15
- **TODO/FIXME accumulation** - Files with >5 outstanding items
- **Missing type coverage** - Functions without type annotations
- **Large files** - Source files >500 lines
- **Deeply nested code** - Nesting depth >5 levels

## Archive Structure

```
/Users/braydon/projects/archive/tech-debt/
├── 2026-02-03-143022-projectname/
│   ├── metadata.json
│   └── [preserved file structure]
```

### Metadata Format

```json
{
  "timestamp": "2026-02-03T14:30:22Z",
  "project": "/Users/braydon/projects/experiments/foo",
  "stack": ["typescript", "python"],
  "summary": {
    "tier1_removed": 23,
    "tier2_removed": 12,
    "tier3_flagged": 8,
    "lines_removed": 847
  },
  "files": [
    {
      "path": "src/utils/old-helper.ts",
      "action": "deleted",
      "tier": 1,
      "reason": "unused_export",
      "details": "Exported but never imported"
    }
  ]
}
```

## Execution Workflow

### 1. Detect Stack

```bash
# Check for project markers
[[ -f "tsconfig.json" ]] && STACK+=("typescript")
[[ -f "package.json" ]] && [[ ! -f "tsconfig.json" ]] && STACK+=("javascript")
[[ -f "requirements.txt" ]] || [[ -f "pyproject.toml" ]] && STACK+=("python")
[[ -f "Cargo.toml" ]] && STACK+=("rust")
[[ -f "go.mod" ]] && STACK+=("go")
```

### 2. Run Detection Tools

For each detected stack, run appropriate analysis. See `references/tool-commands.md` for specific commands.

**TypeScript/JavaScript:**
- `npx knip` - Comprehensive unused detection
- `npx ts-prune` - Unused exports (TS only)
- `npx eslint --rule 'no-unused-vars: error'`

**Python:**
- `vulture . --min-confidence 80`
- `flake8 --select=F401,F841` (unused imports/vars)
- `pylint --disable=all --enable=W0611,W0612`

**Rust:**
- `cargo +nightly udeps`
- `cargo clippy -- -W dead_code`

**Go:**
- `staticcheck ./...`
- `deadcode ./...`

### 3. Analyze Results

Parse tool output and categorize by tier:
- Tier 1: Pattern match known safe removals
- Tier 2: Cross-reference to confirm unused
- Tier 3: Complexity/quality metrics

### 4. Create Archive

```bash
ARCHIVE_DIR="/Users/braydon/projects/archive/tech-debt/$(date +%Y-%m-%d-%H%M%S)-$(basename $PWD)"
mkdir -p "$ARCHIVE_DIR"
```

### 5. Execute Removals

For Tier 1 and Tier 2 items:
1. Copy file to archive preserving structure
2. Apply removal (delete file, remove function, etc.)
3. Log to metadata.json

### 6. Generate Report

```
🔪 Tech Debt Hunter - /Users/braydon/projects/foo
Stack: TypeScript, Python | Scanning...

📊 Results:

TIER 1 - Auto-killed (100% safe):
  ✓ 8 unused imports removed
  ✓ 3 unreachable code blocks removed
  ✓ 2 empty files deleted
  ✓ 4 commented code blocks removed

TIER 2 - Archived & removed:
  ✓ 5 unused exports removed
  ✓ 3 dead functions removed
  ✓ 2 duplicate code blocks consolidated

TIER 3 - Flagged for review:
  ⚠ src/services/auth.ts - complexity 23 (threshold: 15)
  ⚠ src/utils/helpers.py - 7 TODO items
  ⚠ src/legacy/old-api.ts - 612 lines (threshold: 500)

📦 Archive: /Users/braydon/projects/archive/tech-debt/2026-02-03-143022-foo/
   847 lines removed | 17 files modified | 2 files deleted

💡 Run '/tech-debt --report' for detailed breakdown
```

## Usage

```bash
/tech-debt                    # Full scan + removal
/tech-debt --report           # Report only, no changes
/tech-debt --tier1-only       # Only auto-kill safe items
/tech-debt src/               # Scope to directory
/tech-debt --restore <id>     # Restore from archive
```

## Protected Patterns

Never touch:
- `.git/`, `node_modules/`, `.venv/`, `dist/`, `build/`
- `package.json`, `requirements.txt`, `*.lock`
- `CLAUDE.md`, `README.md`, `.env*`
- Files with uncommitted changes
- Test files (unless explicitly included)

## Tool Installation

Before first run, ensure tools are available. See `scripts/install-tools.sh` for installation commands.

## Common Mistakes

**Running without reading output first**
- Always use `--report` first on unfamiliar codebases
- Review Tier 3 items manually

**Ignoring test coverage**
- Dead code detection may miss dynamically-called code
- Ensure tests pass after cleanup

**Not checking git status**
- Only run on clean working directory
- Commit or stash changes first

## Additional Resources

### Reference Files

- **`references/tool-commands.md`** - Detailed tool commands per language
- **`references/detection-patterns.md`** - Regex patterns for code detection

### Scripts

- **`scripts/install-tools.sh`** - Install all detection tools
- **`scripts/detect-stack.sh`** - Stack detection utility
