---
name: standards
description: 'Language-specific coding standards and validation rules. Provides Python, Go, Rust, TypeScript, Shell, YAML, JSON, and Markdown standards. Auto-loaded by /vibe, /implement, /doc, /bug-hunt, /complexity based on file types.'
metadata:
  tier: library
  dependencies: []
  internal: true
---

# Standards Skill

Language-specific coding standards loaded on-demand by other skills.

## Purpose

This is a **library skill** - it doesn't run standalone but provides standards
references that other skills load based on file types being processed.

## Standards Available

| Standard | Reference | Loaded By |
|----------|-----------|-----------|
| Skill Structure | `references/skill-structure.md` | vibe (skill audits), doc (skill creation) |
| Python | `references/python.md` | vibe, implement, complexity |
| Go | `references/go.md` | vibe, implement, complexity |
| Rust | `references/rust.md` | vibe, implement, complexity |
| TypeScript | `references/typescript.md` | vibe, implement |
| Shell | `references/shell.md` | vibe, implement |
| YAML | `references/yaml.md` | vibe |
| JSON | `references/json.md` | vibe |
| Markdown | `references/markdown.md` | vibe, doc |

## How It Works

Skills declare `standards` as a dependency:

```yaml
skills:
  - standards
```

Then load the appropriate reference based on file type:

```python
# Pseudo-code for standard loading
if file.endswith('.py'):
    load('standards/references/python.md')
elif file.endswith('.go'):
    load('standards/references/go.md')
elif file.endswith('.rs'):
    load('standards/references/rust.md')
# etc.
```

## Deep Standards

For comprehensive audits, skills can load extended standards from
`vibe/references/*-standards.md` which contain full compliance catalogs.

| Standard | Size | Use Case |
|----------|------|----------|
| Tier 1 (this skill) | ~5KB each | Normal validation |
| Tier 2 (vibe/references) | ~15-20KB each | Deep audits, `--deep` flag |

## Integration

Skills that use standards:
- `/vibe` - Loads based on changed file types
- `/implement` - Loads for files being modified
- `/doc` - Loads markdown standards
- `/bug-hunt` - Loads for root cause analysis
- `/complexity` - Loads for refactoring recommendations

## Examples

### Vibe Loads Python Standards

**User says:** `/vibe` (detects changed Python files)

**What happens:**
1. Vibe skill checks git diff for file types
2. Vibe finds `auth.py` in changeset
3. Vibe loads `standards/references/python.md` automatically
4. Vibe validates against Python standards (type hints, docstrings, error handling)
5. Vibe reports findings with standard references

**Result:** Python code validated against language-specific standards without manual reference loading.

### Implement Loads Go Standards

**User says:** `/implement ag-xyz-123` (issue modifies Go files)

**What happens:**
1. Implement skill reads issue metadata to identify file targets
2. Implement finds `server.go` in implementation scope
3. Implement loads `standards/references/go.md` for context
4. Implement writes code following Go standards (error handling, naming, package structure)
5. Implement validates output against loaded standards before committing

**Result:** Go code generated conforming to standards, reducing post-implementation vibe findings.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Standards not loaded | File type not detected or standards skill missing | Check file extension matches reference; verify standards in dependencies |
| Wrong standard loaded | File type misidentified (e.g., .sh as .bash) | Manually specify standard; update file type detection logic |
| Deep standards missing | Vibe needs extended catalog, not found | Check `vibe/references/*-standards.md` exists; use `--deep` flag |
| Standard conflicts | Multiple languages in same changeset | Load all relevant standards; prioritize by primary language |
