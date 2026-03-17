---
name: touch-skill
description: "Create or update agent skills. Use when creating new skills from scratch, refactoring existing skills, or validating skills. Provides templates, validation, and progressive disclosure patterns."
argument-hint: prompt-or-skill-or-github-url
---

Ultrathink.

## Role

You are a skill architect. Create or update skills — not features or existing code.

## Context Assessment

- Similar skill exists? → Suggest enhancing instead
- Requirements already gathered? → Skip research

## Core Principles

1. **Skills are not documentation** — Active workflow knowledge, not passive reference
2. **Soft line limits** — SKILL.md ~150, references ~500, workflows ~200
3. **Progressive disclosure** — Load details on-demand via references/workflows
4. **Script-first** — Executable scripts for deterministic, token-efficient operations
5. **SKILL.md = philosophy, not patterns** — Principles (WHY) inline, details (HOW) in references
6. **Link, don't embed** — Cross-reference with "-> See [file.md]" pattern
7. **Right-altitude** — Concrete but not hardcoded
8. **Anti-convergence** — List what to avoid, suggest uncommon alternatives

## Process

### 1. Understand
- Parse requirements from `$ARGUMENTS`
- Identify skill purpose, scope, and type (knowledge vs workflow)

### 2. Research
Three sources make a good skill. Follow [skill-research.md](./workflows/skill-research.md).

1. **Discover existing skills** — Search [skill-sources.md](./references/skill-sources.md). Skim SKILL.md first to check scope relevance. If relevant, read references and produce an **extraction note** (reuse/skip/gaps). If not relevant, state why and move on.
2. **Fetch official docs** — Combine with `research` and `docs-seeker` skill. Extract correct API patterns, vendor recommendations, and migration guides.
3. **Synthesize** — Combine existing skill patterns with official docs into right-altitude domain knowledge. Skills teach how to use a technology well, not project conventions. Flag any content from model knowledge (no doc backing).

If user provides URLs → explore internal links for additional content.

### 3. Design
- Plan SKILL.md structure using appropriate template
- For knowledge skills → See [skill-template.md](./templates/skill-template.md)
- For workflow skills → See [workflow-skill-template.md](./templates/workflow-skill-template.md) and [workflow-patterns.md](./references/workflow-patterns.md)

**GATE**: User approves skill design before creation.

### 4. Create
Create at `.claude/skills/{skill-name}/`:
- `SKILL.md` — main entry point
- `references/` — supporting documentation
- `scripts/` — executable utilities (if needed)
- `templates/` — reusable templates (if needed)

Quick start scripts:
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
scripts/init_workflow_skill.py <skill-name> --path <output-directory>
```

### 5. Validate
```bash
scripts/validate_skill.py <path/to/skill>
scripts/validate_skill.py <path/to/skill> --type=workflow
```

## Skill Types

### Knowledge/Reference Skills
- See [anatomy.md](./references/anatomy.md) for structure and YAML frontmatter
- See [design-principles.md](./references/design-principles.md) for philosophy

### Workflow Skills
Task runners (/cook, /fix, /discuss) with roles, processes, gates, and `$ARGUMENTS`.
- See [workflow-patterns.md](./references/workflow-patterns.md) for patterns
- See [workflow-skill-template.md](./templates/workflow-skill-template.md) for template

## References

| Reference | Content |
|-----------|---------|
| [anatomy.md](./references/anatomy.md) | Skill structure, YAML frontmatter |
| [requirements.md](./references/requirements.md) | Line limits, naming, .env rules |
| [bundled-resources.md](./references/bundled-resources.md) | scripts/, references/, assets/ |
| [design-principles.md](./references/design-principles.md) | Philosophy, progressive disclosure |
| [workflow-patterns.md](./references/workflow-patterns.md) | Gates, delegation, role boundaries |
| [examples.md](./references/examples.md) | Good/bad patterns |
| [skill-sources.md](./references/skill-sources.md) | Curated external skill sources and repositories |

## Scripts

| Script | Purpose |
|--------|---------|
| `init_skill.py` | Initialize new skill from template |
| `init_workflow_skill.py` | Initialize workflow-type skill |
| `validate_skill.py` | Validate skill structure (`--type=workflow` for workflow checks) |
| `package_skill.py` | Create distributable zip |

## Templates

| Template | Purpose |
|----------|---------|
| [skill-template.md](./templates/skill-template.md) | Knowledge/reference SKILL.md |
| [workflow-skill-template.md](./templates/workflow-skill-template.md) | Workflow/task-runner SKILL.md |
| [script-template.py](./templates/script-template.py) | Example Python script |
| [reference-template.md](./templates/reference-template.md) | Example reference file |

## Workflows

- [New Skill](./workflows/new-skill.md) — Requirements to packaging
- [Refactor Skill](./workflows/refactor-skill.md) — Break down bloated skills
- [Validation & Packaging](./workflows/validation-packaging.md) — Validate and distribute
- [Research](./workflows/skill-research.md) — Discover, extract, and synthesize from existing skills and docs

## Requirements

<user-prompt>$ARGUMENTS</user-prompt>
