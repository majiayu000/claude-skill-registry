---
name: cleanup-project
description: |
  Project cleanup and pruning workflow. Use when removing unused guides,
  cleaning up stale components, or streamlining an Samuel installation
  to match actual project needs.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Project Cleanup Workflow

## When to Use

| Trigger | Description |
|---------|-------------|
| **Post-Initialization** | After `initialize-project.md` completes |
| **Quarterly Maintenance** | Every 3 months as part of project hygiene |
| **Pre-Release** | Before major releases to reduce deployment footprint |
| **Size Threshold** | When `.claude/` exceeds 1MB |
| **Stack Change** | After removing a language/framework from the project |

---

## Prerequisites

Before starting cleanup:

- [ ] Project has been initialized (`CLAUDE.md` exists or stack is clear)
- [ ] No active development in progress that might need guides being pruned
- [ ] Git working directory is clean (commit or stash changes first)

---

## Process Overview

```
Step 1: Analyze Project Stack
    ↓
Step 2: Prune Unused Guides
    ↓
Step 3: Archive Stale Tasks
    ↓
Step 4: Consolidate Memory
    ↓
Step 5: Clean Patterns
    ↓
Step 6: Update Documentation
    ↓
Output: Leaner .claude/ directory
```

---

## Step 1: Analyze Project Stack

### 1.1 Detect Active Languages

Scan project files to identify which languages are actually used:

| File | Language |
|------|----------|
| `package.json` | TypeScript/JavaScript |
| `tsconfig.json` | TypeScript |
| `requirements.txt`, `pyproject.toml`, `setup.py` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `build.gradle.kts`, `*.kt` | Kotlin |
| `pom.xml`, `build.gradle`, `*.java` | Java |
| `*.csproj`, `*.sln` | C# |
| `composer.json` | PHP |
| `Package.swift`, `*.swift` | Swift |
| `CMakeLists.txt`, `Makefile`, `*.cpp`, `*.c` | C/C++ |
| `Gemfile`, `*.rb` | Ruby |
| `pubspec.yaml` | Dart |

**AI Action**: List all detected languages based on project files.

### 1.2 Detect Active Frameworks

Check dependency files for framework usage:

**Node.js/TypeScript** (`package.json` dependencies):
- `react`, `react-dom` → React
- `next` → Next.js
- `express` → Express

**Python** (`requirements.txt`, `pyproject.toml`):
- `django` → Django
- `fastapi` → FastAPI
- `flask` → Flask

**Go** (`go.mod`):
- `github.com/gin-gonic/gin` → Gin
- `github.com/labstack/echo` → Echo
- `github.com/gofiber/fiber` → Fiber

**Rust** (`Cargo.toml`):
- `axum` → Axum
- `actix-web` → Actix-web
- `rocket` → Rocket

*(Continue for all language families)*

**AI Action**: List all detected frameworks based on dependencies.

### 1.3 Generate Active Guides Manifest

Create `.claude/active-guides.json`:

```json
{
  "generated": "2025-01-15T10:00:00Z",
  "languages": [
    "typescript"
  ],
  "frameworks": [
    "react",
    "nextjs"
  ],
  "guides_kept": [
    "skills/typescript-guide/SKILL.md",
    "skills/react/SKILL.md",
    "skills/nextjs/SKILL.md"
  ],
  "guides_archived": [
    "skills/python-guide/SKILL.md",
    "skills/go-guide/SKILL.md",
    "..."
  ]
}
```

**AI Action**: Create `active-guides.json` with detected stack.

---

## Step 2: Prune Unused Guides

### 2.1 Identify Unused Guides

Compare existing guides against `active-guides.json`:

```
All Language Guides: 21
Active Languages: 1 (TypeScript)
Unused Guides: 20 (95% reduction possible)

All Framework Skills: 33
Active Frameworks: 2 (React, Next.js)
Unused Skills: 31 (94% reduction possible)
```

### 2.2 Archive Strategy (Recommended)

Move unused guides to `.claude/.archive/` for potential future use:

```bash
# Create archive directories
mkdir -p .claude/.archive/skills

# Move unused language guide skills
mv .claude/skills/python-guide/ .claude/.archive/skills/
mv .claude/skills/go-guide/ .claude/.archive/skills/
# ... (all unused)

# Move unused framework skills
mv .claude/skills/django/ .claude/.archive/skills/
mv .claude/skills/fastapi/ .claude/.archive/skills/
# ... (all unused)
```

### 2.3 Delete Strategy (Minimal Footprint)

For maximum reduction, delete unused guides entirely:

```bash
# Delete unused language guide skills
rm -rf .claude/skills/python-guide/
rm -rf .claude/skills/go-guide/
# ... (all unused)

# Delete unused framework skills
rm -rf .claude/skills/django/
rm -rf .claude/skills/fastapi/
# ... (all unused)
```

**Note**: Deleted guides can be restored from the template repository if needed later.

### 2.4 Always Keep

Never remove these files regardless of stack:

- `.claude/README.md` - Directory documentation
- `.claude/skills/README.md` - Skills index (language guides, framework skills, custom skills)
- `.claude/skills/*` - All skills (stack-agnostic utilities and workflows)

**AI Action**: Execute chosen strategy (archive or delete). Report space saved.

---

## Step 3: Archive Stale Tasks

### 3.1 Identify Stale PRDs

Find PRDs and task files older than 6 months:

```bash
# Find PRDs older than 180 days
find .claude/tasks -name "*" -mtime +180 -type f
```

### 3.2 Check Status

For each old PRD, determine status:

| Status | Action |
|--------|--------|
| **Completed** | Archive to `.claude/tasks/ARCHIVE/` |
| **Abandoned** | Archive with `ABANDONED-` prefix |
| **Active** | Keep in place (update modified date) |

### 3.3 Archive Process

```bash
# Create archive directory
mkdir -p .claude/tasks/ARCHIVE

# Move completed/abandoned PRDs
mv .claude/tasks/0001-prd-old-feature.md .claude/tasks/ARCHIVE/
mv .claude/tasks/tasks-0001-prd-old-feature.md .claude/tasks/ARCHIVE/

# For abandoned, rename with prefix
mv .claude/tasks/0002-prd-never-built.md .claude/tasks/ARCHIVE/ABANDONED-0002-prd-never-built.md
```

**AI Action**: Identify stale tasks, confirm status with user, archive appropriately.

---

## Step 4: Consolidate Memory

### 4.1 Identify Old Memory Files

Find memory files older than 3 months:

```bash
# Find memory files older than 90 days
find .claude/memory -name "*" -mtime +90 -type f
```

### 4.2 Create Quarterly Summary

Consolidate old memory files into quarterly summaries:

```markdown
# Q4 2024 Decision Summary

## Overview
This file consolidates decisions from October-December 2024.

## Key Decisions

### Authentication Strategy (2024-10-15)
- Chose JWT over sessions for stateless API
- See: archived/2024-10-15-auth-strategy.md

### Database Selection (2024-11-02)
- Selected PostgreSQL over MySQL
- See: archived/2024-11-02-database-choice.md

### Caching Approach (2024-12-10)
- Implemented Redis for distributed caching
- See: archived/2024-12-10-caching-approach.md

## Archived Files
- 2024-10-15-auth-strategy.md
- 2024-11-02-database-choice.md
- 2024-12-10-caching-approach.md
```

### 4.3 Archive Individual Files

```bash
# Create archive directory
mkdir -p .claude/memory/archived

# Move old files
mv .claude/memory/2024-10-* .claude/memory/archived/
mv .claude/memory/2024-11-* .claude/memory/archived/
mv .claude/memory/2024-12-* .claude/memory/archived/
```

**AI Action**: Create quarterly summary, archive old memory files.

---

## Step 5: Clean Patterns

### 5.1 Review patterns.md

If `CLAUDE.md` exists, review for:

- Patterns referencing pruned languages/frameworks
- Duplicate or similar patterns
- Outdated patterns (superseded by newer approaches)

### 5.2 Remove Irrelevant Patterns

Example: If Python was pruned, remove Python-specific patterns:

```markdown
## Removed Patterns

<!-- Remove this section if Python pruned -->
## Python Patterns
...
```

### 5.3 Consolidate Similar Patterns

Merge similar patterns across languages into generic versions where applicable.

**AI Action**: Review and clean `patterns.md` if it exists.

---

## Step 6: Update Documentation

### 6.1 Update .claude/README.md

Add project-specific information:

```markdown
# .claude/ Directory

> **Project**: MyApp
> **Stack**: TypeScript, React, Next.js
> **Last Cleaned**: 2025-01-15

## Active Guides
- Language: TypeScript
- Frameworks: React, Next.js

## Archived Content
See `.archive/` for pruned guides (can be restored if stack changes).
```

### 6.2 Update active-guides.json

Ensure manifest reflects final state after cleanup.

### 6.3 Add to .gitignore (Optional)

If not tracking generated content:

```gitignore
# Optional: Don't track cleanup artifacts
.claude/active-guides.json
.claude/.archive/
.claude/memory/archived/
.claude/tasks/ARCHIVE/
```

**AI Action**: Update documentation to reflect cleaned state.

---

## Output Summary

After cleanup, report:

```
## Cleanup Summary

### Space Reduction
- Before: 2.4 MB
- After: 156 KB
- Saved: 2.24 MB (93% reduction)

### Guides
- Language guide skills: 21 → 1 (20 archived)
- Framework skills: 33 → 2 (31 archived)

### Tasks
- Active PRDs: 3
- Archived PRDs: 5

### Memory
- Active decisions: 4
- Archived to quarterly: 12

### Files Updated
- .claude/README.md ✓
- .claude/active-guides.json ✓
```

---

## Restoration

If you need a pruned guide later:

### From Archive

```bash
# Restore from archive
mv .claude/.archive/skills/python-guide/ .claude/skills/
mv .claude/.archive/skills/django/ .claude/skills/
```

### From Template Repository

```bash
# Re-download language guide skill from template
curl -o .claude/skills/python-guide/SKILL.md --create-dirs \
  https://raw.githubusercontent.com/ar4mirez/samuel/main/.claude/skills/python-guide/SKILL.md

# Re-download framework skill from template
curl -o .claude/skills/django/SKILL.md --create-dirs \
  https://raw.githubusercontent.com/ar4mirez/samuel/main/.claude/skills/django/SKILL.md
```

### Update Manifest

After restoration, regenerate `active-guides.json` by re-running Step 1.

---

## Automation (Future)

This workflow can be automated with a script:

```bash
#!/bin/bash
# .claude/scripts/cleanup.sh

# Run cleanup workflow
# TODO: Implement automated detection and cleanup
```

---

## Checklist

Before completing cleanup:

- [ ] Active languages correctly identified
- [ ] Active frameworks correctly identified
- [ ] `active-guides.json` created
- [ ] Unused guides archived/deleted
- [ ] Stale tasks archived
- [ ] Memory files consolidated
- [ ] patterns.md cleaned (if exists)
- [ ] README.md updated with project info
- [ ] Space reduction reported
- [ ] Git commit created (if desired)

---

## Related Workflows

- [initialize-project.md](../workflows/initialize-project.md) - Run cleanup after initialization
- [troubleshooting.md](../workflows/troubleshooting.md) - If cleanup causes issues
- [generate-agents-md.md](../workflows/generate-agents-md.md) - Regenerate AGENTS.md after cleanup
