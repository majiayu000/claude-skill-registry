---
name: code-cleanup
description: |
  Detect and clean redundant code in Python and TypeScript projects.
  Finds unused imports, dead functions, stale comments, debug statements,
  and unused dependencies. Use when asked to "clean code", "find dead code",
  "remove unused imports", "check redundant code", or "清理代码".
---

# Code Cleanup Skill

Scan projects for redundant code and generate cleanup reports.

## Quick Start

```bash
# Scan for dead code (unused imports, functions, variables)
python scripts/scan_dead_code.py backend/

# Scan for stale code (old TODOs, debug statements, commented code)
python scripts/scan_stale_code.py src/

# Check unused dependencies
python scripts/scan_unused_deps.py .
```

## Scripts

| Script | Detects | Confidence |
|--------|---------|------------|
| scan_dead_code.py | Unused imports, functions, classes, variables | High |
| scan_stale_code.py | Commented code, old TODOs, debug statements | Medium |
| scan_unused_deps.py | Unused packages in requirements.txt/package.json | Low |

## Usage

### scan_dead_code.py

```bash
python scripts/scan_dead_code.py <dir> [--format json|text] [--ignore "test_*"]
```

Detects:
- Unused imports (high confidence, safe to remove)
- Unused functions/classes not starting with `_` (medium confidence)
- Unused top-level variables (medium confidence)

### scan_stale_code.py

```bash
python scripts/scan_stale_code.py <dir> [--todo-days 90] [--no-debug]
```

Detects:
- Commented-out code blocks
- TODOs/FIXMEs older than N days (default: 90)
- Debug statements: `print(`, `console.log(`, `debugger`, `pdb`

### scan_unused_deps.py

```bash
python scripts/scan_unused_deps.py <dir> [--type python|node|all]
```

Checks:
- requirements.txt vs actual imports
- package.json dependencies vs actual imports

## Output Format

All scripts output JSON by default:

```json
{
  "target": "backend/",
  "issues": [
    {
      "type": "unused_import",
      "file": "services/user.py",
      "line": 3,
      "code": "import os",
      "confidence": "high",
      "suggestion": "Remove unused import: os"
    }
  ],
  "summary": {
    "total": 15,
    "high": 10,
    "medium": 5,
    "low": 0
  }
}
```

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| high | Definitely unused | Safe to remove |
| medium | Likely unused | Review before removing |
| low | Possibly unused | Manual inspection needed |

## Cleanup Workflow

1. Run scan scripts on target directory
2. Review JSON output, filter by confidence
3. For each issue: remove, keep, or defer
4. Apply changes (Claude can help edit files)
5. Run tests to verify nothing broke

## Safety Notes

- Scripts are **read-only** (scan only, no modifications)
- Always backup before bulk cleanup
- Run tests after cleanup
- Some "unused" code may be used dynamically (reflection, `__getattr__`, lazy imports)
- Ignore `__init__.py` re-exports

## References

- Detection patterns: `references/detection-patterns.md`
- Cleanup examples: `references/cleanup-examples.md`
