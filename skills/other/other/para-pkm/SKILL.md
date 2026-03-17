---
name: para-pkm
description: Manage PARA-based personal knowledge management (PKM) systems using Projects, Areas, Resources, and Archives organization method. Use when users need to (1) Create a new PARA knowledge base, (2) Organize or reorganize existing knowledge bases into PARA structure, (3) Decide where content belongs in PARA (Projects vs Areas vs Resources vs Archives), (4) Create AI-friendly navigation files for knowledge bases, (5) Archive completed projects, (6) Validate PARA structure, or (7) Learn PARA organizational patterns for specific use cases (developers, consultants, researchers, etc.)
---

# PARA PKM

Organize by actionability, not topic. Projects/Areas/Resources/Archives for optimal AI navigation. Monthly review cadence.

## Core Concepts

- **Projects** = Time-bound goals with deadlines (completes → Archives); includes `projects/stories/` for job applications
- **Areas** = Ongoing responsibilities (use `_overview.md` per area for context)
- **Resources** = Reference material; when unsure, put here temporarily
- **Archives** = Inactive items from any category

## Decision Tree

```
Has deadline/end state? → Projects
Ongoing responsibility? → Areas
Reference material? → Resources (default for uncertain items)
Completed/inactive? → Archives
```

## Quick Start

1. `python scripts/init_para_kb.py <name>` - Creates PARA + `projects/stories/` + navigation
2. Identify projects (deadlines) → areas (ongoing) → resources (reference)
3. `python scripts/generate_nav.py` - Generate AI navigation

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `init_para_kb.py` | Scaffold new KB | `<name> [--path <dir>]` |
| `validate_para.py` | Check structure, detect anti-patterns | `[path]` |
| `archive_project.py` | Archive with metadata (date, origin) | `<project-file> [--kb-path]` |
| `generate_nav.py` | Create AI nav (<100 lines) | `[--kb-path] [--output]` |

## Templates

| Template | Purpose |
|----------|---------|
| `assets/AGENTS.md.template` | AI navigation index |
| `assets/project.md.template` | Project file structure |
| `assets/area-overview.md.template` | Area `_overview.md` format |
| `assets/README.md.template` | Knowledge base README |

## Patterns by Role

- **Developers**: `projects/active/` features/bugs, `areas/professional-development/`, `resources/coding-standards/`
- **Consultants**: `projects/active/` deliverables + `projects/stories/`, `areas/consulting/clients/`, `resources/templates/`
- **Researchers**: `projects/active/` papers/grants, `areas/research-program/`, `resources/literature-review/`
- **Product Builders**: `projects/active/` launches, `areas/product-development/{active,research,graduated,legacy}/`

## Complex Scenarios

**Client = project + relationship**: `projects/active/client-x.md` (deliverables) + `areas/consulting/clients/client-x.md` (relationship, billing)

**Research lifecycle**: `areas/product-development/{research → graduated → active → legacy}` with cross-references

## Anti-Patterns

- inbox/ folder (capture directly into PARA; use Resources when uncertain)
- Deep nesting (max 2-3 levels; flat > nested)
- Topic-based organization ("work/personal" → use actionability)
- Todo folders (tasks belong with their projects/areas)
- Perfectionism (move freely as understanding evolves; monthly review catches misplacements)

## Content Lifecycle

```
Resources → Projects → Archives (research → active work → completed)
Areas → Archives (no longer responsible)
Projects ⟺ Areas (goal becomes ongoing or vice versa)
```

## AI Navigation & Success Tips

- Keep nav under 100 lines; point to paths not files; minimize tokens
- Start simple ("What am I working on now?"); one home per item (use links)
- Monthly review: archive completed, reassess areas; let patterns emerge

## References

- [para-principles.md](references/para-principles.md) - Complete PARA method, "actionability not topic" principle
- [decision-guide.md](references/decision-guide.md) - Detailed decision tree with edge cases
- [common-patterns.md](references/common-patterns.md) - Proven patterns for different roles
- [ai-navigation.md](references/ai-navigation.md) - AI-friendly navigation best practices
