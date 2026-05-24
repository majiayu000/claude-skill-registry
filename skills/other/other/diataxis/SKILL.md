---
name: diataxis
description: >-
  Audit, classify, validate, and scaffold documentation using the Diataxis
  framework (Tutorials, How-to guides, Reference, Explanation). Use when user
  mentions "diataxis", "documentation framework", "quadrant", "doc audit",
  "doc coverage", "collapsed document", "tutorial vs how-to", "quadrant purity",
  "documentation types", or wants to classify docs by type.
---

# Diataxis Documentation Framework

Audit, classify, validate, and scaffold documentation using the [Diataxis](https://diataxis.fr/) framework.

## Quick Start

```bash
# Classify individual files
uv run scripts/diataxis_classify.py docs/*.md

# Audit a docs directory for coverage
uv run scripts/diataxis_audit.py --dir docs

# Validate quadrant purity
uv run scripts/diataxis_validate.py --dir docs

# Scaffold a new Diataxis structure
uv run scripts/diataxis_scaffold.py --dry-run
uv run scripts/diataxis_scaffold.py
```

## Capabilities

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `diataxis_classify.py` | Classify files into quadrants | `--json`, `--verbose`, `--no-content` |
| `diataxis_audit.py` | Coverage report with quality score | `--dir`, `--json`, `--min-coverage` |
| `diataxis_validate.py` | Lint for quadrant purity (DX001-DX010) | `--dir`, `--file`, `--strict`, `--json` |
| `diataxis_scaffold.py` | Generate folder structure | `--layout folders\|flat`, `--init-config`, `--dry-run` |

## The Four Quadrants

| Quadrant | Orientation | User State | Folder |
|----------|-------------|------------|--------|
| **Tutorial** | Learning | Study + Action | `tutorials/` |
| **How-to** | Task | Work + Action | `how-to/` |
| **Reference** | Information | Work + Cognition | `reference/` |
| **Explanation** | Understanding | Study + Cognition | `explanation/` |

## Classification Algorithm

Multi-signal weighted scoring (title 30%, headings 25%, content 25%, structure 20%). Documents scoring highly for 2+ quadrants are flagged as "collapsed" with split suggestions.

## Validation Rules

| ID | Rule | Severity |
|----|------|----------|
| DX001 | Tutorial contains reference tables | warning |
| DX002 | How-to has long conceptual preamble | warning |
| DX003 | Reference contains step-by-step instructions | warning |
| DX004 | Explanation contains execution commands | warning |
| DX005 | No clear quadrant signal | info |
| DX006 | Collapsed document (mixed quadrants) | warning |
| DX007 | Tutorial missing prerequisites | info |
| DX008 | Tutorial missing learning objectives | info |
| DX009 | How-to missing problem statement | info |
| DX010 | Reference missing tables | info |

## Config File (.diataxis-config.json)

Optional per-project override:

```json
{
  "version": 1,
  "root": "docs",
  "layout": "folders",
  "ignore": ["node_modules", ".git", "adr", "rfcs", "*.pdf"],
  "custom_signals": {}
}
```

Create with `uv run scripts/diataxis_scaffold.py --init-config`.

## Common Issues

| Issue | Fix |
|-------|-----|
| `uv` not found | `curl -LsSf https://astral.sh/uv/install.sh \| sh` or run with `python3 scripts/diataxis_classify.py` |
| Low confidence on all files | Files may lack quadrant-specific keywords; use `--verbose` to inspect scores |
| Too many collapsed warnings | Some docs legitimately mix quadrants; consider splitting or accepting |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for all error scenarios.

## References

- [WORKFLOW.md](WORKFLOW.md) — Full methodology (discover, classify, audit, validate, scaffold)
- [EXAMPLES.md](EXAMPLES.md) — Real-world examples for all operations
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error handling and debugging tips
- [Diataxis framework](https://diataxis.fr/) — Official documentation
