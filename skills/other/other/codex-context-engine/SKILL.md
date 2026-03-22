---
name: codex-context-engine
description: Generate and load multi-layer project context documentation to reduce AI hallucination. Use before any task on a project with 50+ files, or on explicit $codex-genome command.
load_priority: always
---

## TL;DR

Generate `.codex/context/genome.md` for macro project understanding. Load `genome.md` automatically if it exists. For large projects, also generate per-module maps. This reduces hallucination by giving AI compressed project knowledge instead of raw file scanning.

# Context Engine (Project Genome)

## Activation

1. **Auto-load:** If `.codex/context/genome.md` exists in the project, load it at session start.
2. **Auto-suggest:** If project has 50+ files and no `genome.md` exists, suggest generating one.
3. **Explicit:** On `$codex-genome`, `$generate-genome`, or `$genome` command.

## Quick Commands

- `$codex-genome` / `$genome` - Generate or refresh project genome
- `$codex-genome --force` / `$genome --force` - Force regeneration

## When to Generate

| Project Size | Action |
| --- | --- |
| < 50 files | Optional. Suggest only if user asks |
| 50-500 files | Suggest on first encounter. Shallow depth (`genome.md` only) |
| 500+ files | Strongly recommend. Full depth (`genome.md` + module maps) |

## When to Load

- **genome.md:** Load at session start if it exists. This is your project briefing - read it before any code edit.
- **Module maps:** Load only the module(s) relevant to the current task. Never load all module maps at once.

## How to Use Context

After loading `genome.md`:

1. You now know the tech stack, directory structure, entry points, data models, API surface, and coding conventions.
2. When working on a specific module, check if `.codex/context/modules/{module-name}.md` exists and load it.
3. Use this knowledge to avoid:
   - Guessing import paths (genome tells you the structure)
   - Wrong naming conventions (genome tells you the patterns)
   - Missing dependencies (genome tells you module boundaries)
   - Hallucinating APIs (genome tells you the real routes)

## Script Invocation

- Use `generate_genome.py` from `codex-project-memory`.
- Xem `skills/.system/REGISTRY.md` để biết đường dẫn đầy đủ.

## Script Invocation Discipline

1. Always run `--help` before invoking.
2. Treat script as a black-box tool and execute by contract first.
3. Read script source only when customization or bug fixing is required.

## Freshness Check

- `genome.md` includes a "Generated:" timestamp and file counts.
- If current file count differs significantly (>20%) from `genome.md` counts, suggest re-generation.
- When user restructures the project (adds/removes modules), remind to regenerate.

## Output Files

| File | Purpose | Size Target |
| --- | --- | --- |
| `.codex/context/genome.md` | Macro project context | 500-800 words |
| `.codex/context/modules/{name}.md` | Per-module detail | 200-400 words each |

## Context Loading Budget

- `genome.md`: always (~2000-2400 tokens)
- Module maps: max 3 at a time (~600-1200 tokens each)
- Total context overhead: <5000 tokens (<4% of context window)
