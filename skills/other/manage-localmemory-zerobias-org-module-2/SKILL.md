---
name: manage-localmemory
description: Local memory storage patterns, file coordination, and cleanup
---

# Memory Management Rules

## Local Memory Storage

- **Location**: `${PROJECT_ROOT}/.claude/.localmemory/`
- **Purpose**: Task progress and intermediate results
- **Scope**: Local only - NEVER commit to git
- **Path Type**: **ALWAYS use absolute paths** (never relative paths)

## Folder Structure

Pattern: `${PROJECT_ROOT}/.claude/.localmemory/{action}-{module-identifier}/`

**CRITICAL:** Always construct absolute paths using:
```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
MEMORY_PATH="${PROJECT_ROOT}/.claude/.localmemory/${action}-${moduleId}"
```

Where module-identifier is:
- `{vendor}-{module}` for simple modules
- `{vendor}-{suite}-{module}` when suite exists

Examples (where PROJECT_ROOT is your project's absolute path):
- `${PROJECT_ROOT}/.claude/.localmemory/create-github-github/`
- `${PROJECT_ROOT}/.claude/.localmemory/update-amazon-aws-s3/`
- `${PROJECT_ROOT}/.claude/.localmemory/fix-gitlab-gitlab/`

## Phase Output Files

Standard naming in memory folders:
```
phase-01-discovery.json
phase-02-scaffolding.json
phase-03-api-spec.json
phase-04-type-generation.json
phase-05-implementation.json
phase-06-testing.json
phase-07-documentation.json
phase-08-build.json
phase-09-validation.json
_work/                    # Working files
```

## Context Passing

1. Each phase reads previous phase output
2. Each phase writes standardized output
3. Use JSON format for structured data
4. Include status and metadata

## Important Notes

- Memory folders created by first running task
- No folder = work not started yet
- Clean up after workflow completion
- Never reference in production code
