---
name: spec-decomposer
description: Decompose large unified specifications into agent skills with progressive disclosure. Use when converting documentation, frameworks, or knowledge bases exceeding 50KB into properly structured skills that an AI agent can navigate efficiently.
---

# Specification Decomposer

Transform large unified specifications into agent skills with multi-level progressive disclosure.

## When to Use

- Source specification exceeds 50KB (too large for single context load)
- Content has natural semantic groupings (domains, topics, categories)
- Granular access needed (load only relevant parts per query)
- Source has atomic units (patterns, sections, articles) that can stand alone

## Core Workflow

1. **Analyze** source spec structure and size
2. **Identify** semantic domains (not structural divisions)
3. **Map** atomic units to domains
4. **Design navigation architecture**:
   - SKILL.md as AI decision hub
   - Domain indexes with manual navigation + auto-generated tables
   - Pattern preservation strategy for updates
5. **Generate** 4-level hierarchy:
   - Level 1: SKILL.md frontmatter (always loaded)
   - Level 2: SKILL.md body (on skill trigger)
   - Level 3: Domain index files (on domain access)
   - Level 4: Individual unit files (on specific need)
6. **Implement generation script** with navigation preservation
7. **Validate** file sizes (<50KB each)

## Key Principles

### Semantic over Structural

Group by meaning/use-case, NOT by source document structure.

**Bad**: Part A, Part B, Part C (mirrors source structure)
**Good**: foundations, workflows, trust-assessment (mirrors usage)

### Individual over Clustered

Keep atomic units separate with TOC navigation.

**Bad**: Cluster related items into single files
**Good**: Individual files + domain index with "Load when..." guidance

Why: Clustering forces loading unnecessary context. Individual files + TOC = load exactly what's needed.

### Levels Encoded by Convention

```
domain/
├── index.md          # Level 3 (always named index.md)
├── unit_1.md         # Level 4
└── unit_2.md         # Level 4
```

No separate level folders - the level is implicit in the file role.

## File Size Limits

| Level | Max Size | Content |
|-------|----------|---------|
| L2 SKILL.md body | 50KB / ~500 lines | Core workflow + domain navigation |
| L3 domain/index.md | 20KB / ~200 lines | Domain overview + unit TOC |
| L4 individual files | 50KB | Single atomic unit |

If a unit exceeds 50KB, split into sub-units with their own index.

## Optional Directories

According to the Agent Skills specification, three optional directories can enhance your skill:

### references/prompts/

For complex skills, add operational prompts in `references/prompts/`:

| File | Purpose |
|------|---------|
| `workflow.md` | Step-by-step process for using the skill |
| `principles.md` | Quick reference for key concepts |
| `keywords.md` | Navigation hints, search terms |

Prompts help the agent know HOW to use the decomposed content effectively.
See [references/operational-prompts.md](references/operational-prompts.md) for details.

### assets/

Store static resources that support the skill:
- Templates (document templates, configuration templates)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

### scripts/

Automation scripts for maintaining the skill structure (generation, validation, etc.)

## Frontmatter Extensions

The official Agent Skills specification defines a minimal set of required fields (`name`, `description`) and optional fields (`license`, `compatibility`, `metadata`, `allowed-tools`).

Specific clients (e.g., Cursor) may extend frontmatter with additional fields:
- `priority: high` - skill loading priority
- `auto_load: true` - automatic activation

Such extensions maintain backward compatibility with the base specification.

## References

- **4-level architecture details**: See [references/4-level-architecture.md](references/4-level-architecture.md)
- **Navigation architecture**: See [references/navigation-architecture.md](references/navigation-architecture.md) - SKILL.md and index.md structure patterns
- **Domain identification**: See [references/domain-grouping.md](references/domain-grouping.md)
- **Size enforcement**: See [references/size-constraints.md](references/size-constraints.md)
- **Operational prompts**: See [references/operational-prompts.md](references/operational-prompts.md)
