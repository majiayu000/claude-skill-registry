---
name: jd-docs
description: >
  Scaffold, validate, and maintain Johnny.Decimal documentation structure
  for software projects. Use when user mentions "Johnny Decimal", "J.D docs",
  "docs structure", "organize docs", "documentation layout", "scaffold docs",
  "docs migration", "generate index", "docs index", "add area", "classify docs",
  "move doc", editing files in numbered directories (00-*, 10-*, 20-*),
  or discussing documentation organization.
---

# Johnny.Decimal Documentation

Scaffold, validate, and maintain [Johnny.Decimal](https://johnnydecimal.com/) documentation structure with sensible defaults and per-project customization.

## Quick Start

```bash
# Scaffold a new structure
uv run scripts/jd_init.py --dry-run   # Preview first
uv run scripts/jd_init.py             # Create docs/ with defaults
uv run scripts/jd_init.py --diataxis  # Include Diataxis areas (41-44)

# Validate existing structure
uv run scripts/jd_validate.py --dir docs

# Regenerate README index
uv run scripts/jd_index.py --dir docs

# Day-2: Add a new area
uv run scripts/jd_add_area.py --prefix 40 --name operations --dry-run

# Day-2: Classify unorganized files
uv run scripts/jd_classify.py docs/*.md
uv run scripts/jd_classify.py docs/*.md --diataxis  # With quadrant info

# Day-2: Move a file to an area
uv run scripts/jd_add.py docs/roadmap.md 00 --dry-run
```

See [WORKFLOW.md](WORKFLOW.md) for the full methodology.

## Capabilities

- **Scaffolding** (`jd_init.py`) — Create J.D directory tree with README templates; supports `--product` for monorepo sub-trees, `--init-config` to generate `.jd-config.json`, and `--diataxis` to include Diataxis quadrant areas (41-44)
- **Validation** (`jd_validate.py`) — Check `NN-kebab-case` naming, detect orphan files, verify README presence per area; `--strict` for CI enforcement
- **Index generation** (`jd_index.py`) — Generate/update root README with table or tree index; preserves custom content via `<!-- JD:INDEX:START/END -->` markers
- **Migration** (Claude-driven) — Classify flat docs into J.D areas using naming heuristics, present a move plan, execute interactively

## Day-2 Operations

- **Add area** (`jd_add_area.py`) — Create a new J.D area with prefix, name, README stub, config update, and auto re-index
- **Classify** (`jd_classify.py`) — Classify files into areas using keyword heuristics with confidence scoring (high/medium/low); `--diataxis` adds Diataxis quadrant column, `--diataxis-move` routes files to quadrant areas (41-44)
- **Add/move file** (`jd_add.py`) — Move a file to an area with auto-normalized kebab-case naming and cross-reference detection

## Default Area Scheme

| Prefix | Name | Purpose |
|--------|------|---------|
| `00-` | getting-started | Onboarding, setup, quick start, MVP |
| `10-` | product | Specs, features, roadmap, design, branding |
| `20-` | architecture | Tech decisions, system design, integration |
| `30-` | research | Spikes, investigations, reference material |
| `90-` | archive | Historical/deprecated docs |

Gap at 40-80 reserved for per-project customization (e.g., `40-operations`).

**With `--diataxis`**, areas 41-44 are added for Diataxis quadrants:

| `41-` | tutorials | Tutorials — step-by-step lessons (Diataxis) |
| `42-` | how-to | How-to guides — practical tasks (Diataxis) |
| `43-` | reference | Reference — technical descriptions (Diataxis) |
| `44-` | explanation | Explanation — conceptual discussions (Diataxis) |

## Config File (.jd-config.json)

Optional per-project override at project root:

```json
{
  "version": 1,
  "root": "docs",
  "areas": { "00": "getting-started", "10": "product", "20": "architecture", "30": "research", "90": "archive" },
  "products": [],
  "ignore": ["adr", "*.pdf"],
  "readme_format": "table"
}
```

Create with `uv run scripts/jd_init.py --init-config`. All fields have sensible defaults.

## Common Issues

| Issue | Fix |
|-------|-----|
| `uv` not found | `curl -LsSf https://astral.sh/uv/install.sh \| sh` or run with `python3 scripts/jd_init.py` |
| Orphan files in validation | Move to area dir, or add to `"ignore"` in `.jd-config.json` |
| Index appended at wrong position | Move `<!-- JD:INDEX:START/END -->` markers to desired location after first run |
| Low confidence on all files | Expand keywords in config or use Claude-driven classification |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for all error scenarios.

## References

- [WORKFLOW.md](WORKFLOW.md) — Full methodology (discovery, config, scaffold, validate, index, migrate, day-2)
- [EXAMPLES.md](EXAMPLES.md) — Real-world examples for all operations
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error handling and debugging tips
