---
name: abaqus-docs
description: Download and manage abqpy API documentation. Use when user asks about API documentation, API reference, or downloading Abaqus docs.
allowed-tools:
  - Read
  - Write
  - Bash(uv:*)
  - Bash(python:*)
---

# Abaqus Documentation Skill

Navigate and access Abaqus Python API documentation for parameter lookups and method reference.

## When to Use This Skill

**Route here when user asks:**
- "Where is the API documentation?"
- "What parameters does X take?"
- "What methods are available for Material/Part/Mesh?"
- "Show me the API reference for..."
- "Download/refresh the docs"

**Route elsewhere:**
- Learning concepts or workflows -> specific analysis skills
- Running analyses -> `/abaqus-static-analysis`, `/abaqus-dynamic-analysis`, etc.
- Quick code examples -> module-specific skills like `/abaqus-material`

## Documentation Location

All API documentation is pre-downloaded at:

`.claude/docs/abaqus-api/modules/`

## Module Index

| Task | Documentation File |
|------|-------------------|
| Model database | `modules/mdb.md` |
| Model internals | `modules/mdb_model.md` |
| Part creation | `modules/part.md` |
| 2D sketching | `modules/sketcher.md` |
| Assembly/instances | `modules/assembly.md` |
| Material properties | `modules/material.md` |
| Section properties | `modules/property.md` |
| Meshing | `modules/mesh.md` |
| Analysis steps | `modules/step.md` |
| Loads | `modules/load.md` |
| Boundary conditions | `modules/bc.md` |
| Contact/ties | `modules/interaction.md` |
| Time-varying definitions | `modules/amplitude.md` |
| Initial/predefined fields | `modules/field.md` |
| Output requests | `modules/output.md` |
| Topology optimization | `modules/optimization.md` |
| Job management | `modules/job.md` |
| Results access | `modules/odb.md` |

## How to Use

### Answering API Questions

1. Identify which module the user needs from the index above
2. Read the relevant documentation file
3. Extract specific method signatures, parameters, or examples

### Common Lookups

| User Asks About | Read This Module |
|-----------------|------------------|
| Creating geometry | `part.md`, `sketcher.md` |
| Positioning parts | `assembly.md` |
| Defining materials | `material.md` |
| Creating sections | `property.md` |
| Generating mesh | `mesh.md` |
| Setting up analysis | `step.md` |
| Applying forces | `load.md` |
| Fixing supports | `bc.md` |
| Defining contact | `interaction.md` |
| Running analysis | `job.md` |
| Extracting results | `odb.md` |

## Refreshing Documentation

If documentation is missing or outdated:
1. Run the download script at `.claude/skills/abaqus-docs/scripts/download_abqpy_docs.py`
2. Use `--force` flag to overwrite existing files

## Documentation Sources

- **Primary**: https://hailin.wang/abqpy/en/2025/reference/
- **GitHub**: https://github.com/haiiliin/abqpy

## Code Patterns

For actual API syntax and code examples, see:
- `references/api-quick-ref.md`
- `references/common-patterns.md`
