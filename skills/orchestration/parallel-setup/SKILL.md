---
name: parallel-setup
description: One-time setup of parallel/ directory for multi-agent development
argument-hint: "[--tech django|typescript|go]"
---

# parallel-setup

**Category**: Parallel Development

## Usage

```bash
/parallel-setup [--tech django|typescript|go]
```

## Arguments

- `--tech`: Optional - Technology stack hint for future decompositions (default: auto-detect)

## Purpose

**One-time** initialization of the `parallel/` directory at project root for parallel multi-agent development. This creates the infrastructure for organizing decomposed tasks by Tech Spec.

> Run this once per project. Then use `/parallel-decompose` for each Tech Spec.

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Create Directory Structure

```bash
mkdir -p parallel
```

Creates:
```
parallel/
├── README.md           # Explains parallel development workflow
└── .gitignore          # What to track vs ignore
```

### 2. Create README.md

Create `parallel/README.md`:
```markdown
# Parallel Development Artifacts

This directory contains artifacts for parallel multi-agent development.

## Structure

Each Tech Spec decomposition creates a subdirectory:

```
parallel/
├── TS-0042-inventory-system/      # Keyed by Tech Spec ID
│   ├── manifest.json              # Regeneration metadata
│   ├── context.md                 # Shared project context
│   ├── tasks/                     # Task specifications
│   ├── contracts/                 # Shared types & API schema
│   ├── prompts/                   # Agent launch prompts
│   ├── scripts/                   # Launch & monitor scripts
│   ├── architecture.md            # System design
│   └── task-graph.md              # Dependency visualization
└── ...
```

## Commands

- `/parallel-decompose <prd> --tech-spec <ts-file>` - Decompose PRD into tasks
- `/parallel-integrate --parallel-dir <dir>` - Verify integration

## Regeneration

Each subdirectory contains a `manifest.json` with metadata to regenerate artifacts:
```bash
# Re-run decomposition with same args
/parallel-decompose docs/prd.md --tech-spec tech-specs/approved/TS-XXXX.md
```
```

### 3. Create .gitignore

Create `parallel/.gitignore`:
```gitignore
# Generated prompts and scripts (regenerate with /parallel-decompose)
*/prompts/
*/scripts/

# Integration reports
*/integration-report.md

# Keep tracked:
# - manifest.json (regeneration metadata)
# - context.md (shared context)
# - tasks/ (task specifications)
# - contracts/ (shared types & API)
# - architecture.md (system design)
# - task-graph.md (dependencies)
```

### 4. Update CLAUDE.md (if exists)

If `CLAUDE.md` exists at project root, add a section:

```markdown
## Parallel Development

This project uses parallel multi-agent development. Artifacts are in `parallel/`.

- Each Tech Spec decomposition creates `parallel/TS-XXXX-{slug}/`
- Task files use compact YAML format for token efficiency
- Contracts are shared via `contracts/` subdirectory
- Run `/parallel-decompose --help` for usage
```

### 5. Report Results

Output summary:
```
Created parallel/ directory structure

parallel/
├── README.md           # Workflow documentation
└── .gitignore          # Track config

Next steps:
1. Create a Tech Spec: /create-tech-spec <title>
2. Decompose PRD: /parallel-decompose <prd> --tech-spec <ts-file>
```

## Example

```bash
# Initialize parallel development
/parallel-setup

# With technology hint
/parallel-setup --tech django
```

## Notes

- This command is idempotent - safe to run multiple times
- Existing files are NOT overwritten
- Creates foundation for `/parallel-decompose` command
- Each decomposition creates its own subdirectory (e.g., `parallel/TS-0042-slug/`)
