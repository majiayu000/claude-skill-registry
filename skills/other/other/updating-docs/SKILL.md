---
name: updating-docs
description: Use when creating or updating documentation in peek-stash-browser. Covers MkDocs conventions, doc structure, API reference generation, and plan document formatting.
---

# Updating Documentation

## Documentation Stack

- **Engine**: MkDocs with Material theme
- **Deployment**: GitHub Pages via GitHub Actions (auto on push to main)
- **API Reference**: Auto-generated from TypeScript source via `server/scripts/generate-api-docs.ts`

## Directory Structure

```
docs/
  index.md                      # Landing page
  getting-started/              # Installation, config, troubleshooting (6 files)
  user-guide/                   # Feature documentation (14 files)
  development/                  # Developer docs (4 files)
  reference/                    # API reference, entity relationships, Docker basics
  plans/                        # Design docs and implementation plans (~120 files)
  audits/                       # Documentation audits
  assets/                       # Images, logos
  stylesheets/                  # Custom CSS
  javascripts/                  # Custom JS
```

## Writing User-Facing Docs

### Page Structure

```markdown
# Feature Name

Brief description of what this feature does and why it's useful.

## Section Name

Step-by-step instructions or explanation.

### Subsection

More detail as needed.

!!! tip
    Helpful hint for the user.

!!! warning
    Important caution about potential issues.

!!! info
    Additional context or background information.
```

### Conventions

- **H1**: Page title only (one per page)
- **H2**: Major sections
- **H3**: Subsections within a section
- **Admonitions**: Use `!!! tip`, `!!! warning`, `!!! info`, `!!! note` for callouts
- **Numbered lists**: For step-by-step procedures
- **Tables**: For keyboard shortcuts, comparisons, reference data
- **Cross-links**: Use relative paths: `[Link Text](../user-guide/playlists.md)`
- **Code blocks**: Always specify language (```bash, ```json, etc.)
- **Feature location**: Include where to find the feature ("Location: Home page > Settings")
- **Troubleshooting**: Add a section at the end for common issues

### What Goes Where

| Content | Directory |
|---------|-----------|
| How to install/configure | `getting-started/` |
| How to use a feature | `user-guide/` |
| How the code works | `development/` |
| API endpoints, entity models | `reference/` |
| Feature design before implementation | `plans/` |

## Plan Documents

### Naming Convention

```
docs/plans/YYYY-MM-DD-feature-name-type.md
```

Types:
- `-design.md` — Problem statement, proposed solution, architecture decisions
- `-plan.md` — Task-by-task implementation steps
- `-impl.md` or `-implementation.md` — Detailed implementation notes

### Design Document Template

```markdown
# Feature Name

## Objective
Brief statement of what we're building and why.

## Current State
What exists today, what's missing or broken.

## Solution

### Approach
High-level description of the solution.

### Changes
#### File: `path/to/file.ts`
- Description of changes with code context

## Files Affected
- `path/to/file.ts` — description
```

### Implementation Plan Template

```markdown
# Feature Name — Implementation Plan

## Goal
One-line goal.

## Architecture
Brief architecture summary.

---

### Task 1: Task Title

**Files:**
- Modify: `path/to/file.ts`
- Create: `path/to/new-file.ts`

**Steps:**
1. Step description
2. Step description

**Verification:** `npm test` or manual check description.

---

### Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Task title | file.ts |
```

## API Reference

The API reference at `docs/reference/api-reference.md` is **auto-generated**. Do not edit it manually.

### Regenerating

```bash
cd server && npm run generate-api-docs
```

This parses route files, controller implementations, and TypeScript type definitions to generate the reference. It runs automatically in CI when relevant source files change.

### Triggers for Auto-Rebuild

The docs GitHub Action rebuilds when these paths change:
- `docs/**`
- `mkdocs.yml`
- `server/routes/**`
- `server/types/api/**`
- `server/controllers/**`
- `server/scripts/**`

## Redirects

When moving a doc to a new path, add a redirect in `mkdocs.yml`:

```yaml
plugins:
  - redirects:
      redirect_maps:
        'old/path.md': 'new/path.md'
```

## Local Preview

```bash
pip install mkdocs-material mkdocs-minify-plugin mkdocs-redirects
mkdocs serve
```

Site available at `http://localhost:8000`.
