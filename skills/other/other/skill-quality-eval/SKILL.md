---
name: skill-quality-eval
description: "Validate and audit quality of AI agent slash commands (.claude/commands/*.md) — checks YAML frontmatter, description length, jargon detection, directive language, and duplicate detection. Use when creating, editing, or auditing project commands and skills. Run proactively after adding new commands."
---

# Skill Quality Evaluator

Validates `.claude/commands/*.md` files for quality, triggering accuracy, and best practices from Phil Schmid's (Google DeepMind) eval harness methodology.

## What it checks

1. **YAML frontmatter** — every command must start with `---` block containing `description:`
2. **Description length** — minimum 40 characters (short descriptions don't trigger well)
3. **Jargon detection** — flags internal terms that confuse users (dogfood, --dangerously, etc.)
4. **Directive language** — descriptions must contain action verbs (Run, Fix, Scan, Extract, etc.) because passive descriptions don't trigger Claude's skill routing
5. **Duplicate detection** — similar commands must have distinct descriptions (first 30 chars normalized)

## How to run

Execute the bundled script — it requires **zero dependencies** (pure Node.js):

```bash
node .claude/skills/skill-quality-eval/scripts/run-eval.js [commands-dir]
```

- Default `commands-dir`: `.claude/commands` (relative to cwd)
- Pass an absolute path to scan a different directory

The script outputs a structured report with PASS/FAIL per file, summary stats, and specific fix suggestions.

## When a check fails

| Check | How to fix |
|-------|-----------|
| Missing frontmatter | Add `---\ndescription: "..."\n---` at top of file |
| Description too short | Expand to 40+ chars — explain WHEN to use and WHAT it does |
| Jargon detected | Replace internal terms with user-facing language |
| No directive verb | Add action verbs: "Run...", "Fix...", "Scan...", "Use when..." |
| Duplicate description | Make the first 30 chars unique between similar commands |

## Customization

Edit `scripts/run-eval.js` to add:
- Custom jargon patterns (line ~15, `JARGON_PATTERNS` array)
- Additional directive verbs (line ~30, `DIRECTIVE_PATTERNS` array)
- Differentiation pairs (line ~50, `DIFF_PAIRS` array)

## Integration with CI

The script exits with code 1 if any check fails, making it suitable for pre-commit hooks or CI pipelines:

```bash
node .claude/skills/skill-quality-eval/scripts/run-eval.js || echo "Fix command quality issues!"
```

## Background

Based on Phil Schmid's (Google DeepMind) eval harness methodology. See `references/phil-schmid-eval-harness.md` for the full framework and best practices.
