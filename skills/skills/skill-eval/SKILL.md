---
name: skill-eval
description: Evaluate all workspace-hub skills for structural validity, content quality, cross-reference integrity, and registry consistency. Runs 18 checks across critical, warning, and info severity levels with actionable fix suggestions.
version: 1.0.0
category: development
last_updated: 2026-01-29
capabilities:
  - structural_validation
  - content_quality_analysis
  - cross_reference_integrity
  - report_generation
tools:
  - Bash
  - Read
  - Glob
  - Grep
related_skills:
  - skill-creator
  - compliance-check
  - repository-health-analyzer
  - verification-loop
---

# Skill Eval

## Quick Start

```bash
# Full evaluation of all skills
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py

# JSON output
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py --format json

# Single skill
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py --skill testing-tdd-london

# Only critical issues
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py --severity critical
```

## When to Use

- Auditing skill quality after bulk creation or migration
- Pre-release validation of the skills library
- CI/CD quality gate for skill changes
- Identifying broken cross-references after renaming skills
- Checking compliance with v2 SKILL.md template format

## Core Concepts

### Evaluation Dimensions

The evaluator runs 18 checks organized into three severity levels:

**Critical** (blocks skill usage):
- YAML frontmatter exists and parses
- Required fields present: `name`, `description`

**Warning** (degrades quality):
- Version follows semver, category matches directory
- Required content sections present (Quick Start, When to Use, etc.)
- Code blocks in key sections, no TODO/FIXME markers
- Cross-references in `related_skills` resolve to real skills

**Info** (improvement opportunities):
- Uses v2 template format, has optional sections (Metrics, etc.)
- No duplicate skill names across the library

### Report Output

Reports include:
- Summary with pass/fail counts and percentages
- Issues grouped by severity with counts
- Per-category breakdown
- Top 10 most common issues
- Per-skill details with actionable fix suggestions

## Usage Examples

### Full Evaluation

```bash
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py
```

Output:
```
================================================================
  SKILL EVALUATION REPORT
  Generated: 2026-01-29T14:30:00+00:00
================================================================

SUMMARY
----------------------------------------
  Total skills evaluated:  230
  Passed (no critical):    187  (81.3%)
  Warnings only:           102  (44.3%)
  Critical failures:        43  (18.7%)
```

### JSON for CI/CD

```bash
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py \
  --format json --severity critical \
  --output reports/skill-eval.json
```

### Filter by Category

```bash
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py --category development
```

### Summary Only

```bash
uv run .claude/skills/development/skill-eval/scripts/eval-skills.py --summary-only
```

## Best Practices

- Run after creating new skills with `/skill-creator` to validate structure
- Use `--format json` in CI pipelines for machine-readable output
- Address critical issues first (missing frontmatter, invalid YAML)
- Use `--severity warning` to focus on actionable improvements
- Run `--category` filters for focused audits of specific skill areas

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | All skills pass (no critical issues) |
| 1 | Critical failures found |
| 2 | Script error (missing directory, invalid arguments) |

| Common Issue | Cause | Fix |
|-------------|-------|-----|
| `frontmatter_missing` | Skill uses legacy heading format | Add `---` delimited YAML frontmatter |
| `yaml_invalid` | Syntax error in frontmatter | Fix YAML syntax (check colons, indentation) |
| `related_skill_unresolved` | Referenced skill name doesn't exist | Correct the name or remove the reference |
| `section_missing` | Missing required H2 section | Add the section heading and content |

## Metrics & Success Criteria

| Metric | Target |
|--------|--------|
| Skills passing all critical checks | 100% |
| Skills with complete v2 sections | >80% |
| Resolved cross-references | 100% |
| No TODO/FIXME in skills | 100% |

## Version History

- **1.0.0** (2026-01-29): Initial release with 18 checks, human + JSON output, category/skill filtering
