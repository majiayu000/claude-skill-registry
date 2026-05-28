---
name: standards
description: 'Language-specific coding standards and validation rules. Provides Python, Go, TypeScript, Shell, YAML, JSON, and Markdown standards. Auto-loaded by /vibe, /implement, /doc, /bug-hunt, /complexity based on file types.'
---

# Standards Skill

Language-specific coding standards loaded on-demand by other skills.

## Purpose

This is a **library skill** - it doesn't run standalone but provides standards
references that other skills load based on file types being processed.

## Standards Available

| Language | Reference | Loaded By |
|----------|-----------|-----------|
| Python | `references/python.md` | vibe, implement, complexity |
| Go | `references/go.md` | vibe, implement, complexity |
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
