---
name: project-docs
description: "Project documentation structure — standard proj-[name]/ layout with ADRs, stories, and operations guides. Use when: initializing docs for a new project, recording architecture decisions, or maintaining project knowledge bases."
---

# Project Documentation

## Core Principles

- **Docs are for future you** — Good docs let you resume context in 5 minutes after 3 months away
- **Record decisions, not just results** — "We use X" is not enough. Record "why X, not Y"

## Project Docs Structure

Each project gets a `proj-[name]/` directory:

```
proj-[name]/
├── SKILL.md                    # Project entry point (concise summary)
└── references/
    ├── _index.md               # Navigation guide
    ├── product/
    │   ├── vision.md           # What problem this project solves
    │   └── principles.md       # Core development principles
    ├── system/
    │   └── overview.md         # System architecture overview
    ├── decisions/
    │   ├── _index.md           # Decision index
    │   ├── adr/                # Architecture Decision Records
    │   └── stories/            # Feature stories
    └── operations/
        ├── quick-nav.md        # Quick navigation
        └── troubleshooting.md  # Common issues & solutions
```

## Initializing a New Project

1. Create the directory structure above
2. Fill `product/vision.md` — What problem does this project solve?
3. Define `product/principles.md` — What are the core development principles?
4. Document `system/overview.md` — What does the system look like now?
5. Backfill `decisions/adr/` — Record important technical choices already made

> See [doc-standards.md](references/doc-standards.md) for ADR format, story format, and naming conventions.

## References

| File | Content |
|------|---------|
| [doc-standards.md](references/doc-standards.md) | Document formats and templates |
