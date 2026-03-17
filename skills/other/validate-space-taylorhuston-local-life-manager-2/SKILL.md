---
name: validate-space
description: "Validate project space structure, boilerplate docs, and consistency with ideas/"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Grep, Bash
argument-hint: <project-name>
---

# /validate-space

Validate that a project space has all required structure, boilerplate docs, and stays consistent with its planning docs in ideas/.

## Usage

```bash
/validate-space leaf-nextjs-convex    # Validate specific space
/validate-space coordinatr            # Another project
/validate-space                       # Prompt for project name
```

## Validation Checklist

### Required Files (Every Space)

| File | Purpose | Check |
|------|---------|-------|
| **CLAUDE.md** | AI instructions for codebase | Must exist |
| **README.md** | Entry point for developers | Must exist |
| **package.json** (JS/TS) | Project config | Stack-dependent |

### Required Directory Structure

| Directory | Purpose | Check |
|-----------|---------|-------|
| **docs/** | Documentation root | Must exist |
| **docs/specs/** | Protocol/feature specs | Must exist |
| **docs/adrs/** | Architecture Decision Records | Must exist |

### Required Overview Docs (in docs/)

| File | Purpose |
|------|---------|
| **architecture-overview.md** | System architecture |
| **api-overview.md** | API documentation |
| **data-model.md** | Data structures |
| **deployment.md** | Deployment guide |
| **security.md** | Security considerations |
| **testing-overview.md** | Testing strategy |
| **ui-guide.md** | UI patterns and components |

Templates available at `shared/templates/docs/`

### CLAUDE.md Requirements

- Overview section with stack description
- Project structure section
- Commands section (dev, build, deploy)
- Environment variables section (if applicable)
- Link to ideas/ planning docs

### Consistency Checks

| Check | Description |
|-------|-------------|
| **Version sync** | package.json versions match docs (e.g., "Next.js 16" in CLAUDE.md matches `"next": "16.x"`) |
| **Stack accuracy** | Listed technologies actually exist in dependencies |
| **Structure accuracy** | Documented directories actually exist |
| **Ideas link** | Referenced ideas/[project]/ exists and has matching info |

### Cross-Reference with ideas/

| Check | Description |
|-------|-------------|
| **README.md** | Stack listed in ideas/ matches spaces/ |
| **project-brief.md** | Technical decisions match actual implementation |
| **Issues** | Current phase/status is accurate |

## Execution Flow

### 1. Locate Project

```bash
ls spaces/[project-name]/
```

Error if not found.

### 2. Check Required Files

```
Read: spaces/[project]/CLAUDE.md
Read: spaces/[project]/README.md
Read: spaces/[project]/package.json (if JS/TS)
```

### 3. Validate CLAUDE.md Sections

Check for required sections:
- Overview / Stack
- Project Structure
- Commands
- Environment Variables (if .env.example exists)

### 4. Check Version Consistency

Extract versions from:
- CLAUDE.md stack description
- ideas/[project]/README.md
- ideas/[project]/project-brief.md
- package.json dependencies

Flag any mismatches.

### 5. Verify Directory Structure

Check required directories exist:
```bash
ls -la spaces/[project]/docs/
ls -la spaces/[project]/docs/specs/
ls -la spaces/[project]/docs/adrs/
```

Check overview docs present:
```bash
ls spaces/[project]/docs/*.md
# Should have: architecture-overview.md, api-overview.md, data-model.md,
#              deployment.md, security.md, testing-overview.md, ui-guide.md
```

Compare documented structure in CLAUDE.md against actual:
```bash
ls -la spaces/[project]/
ls -la spaces/[project]/src/ (if documented)
```

### 6. Cross-Reference ideas/

```bash
Read: ideas/[project]/README.md
Read: ideas/[project]/project-brief.md
```

Check stack/version consistency.

## Validation Report

```markdown
# Space Validation: [Project Name]

## Status
- Space location: spaces/[project]/
- Ideas location: ideas/[project]/ (exists/missing)

## Required Files
✅ CLAUDE.md - Present
✅ README.md - Present
✅ package.json - Present

## Required Directories
✅ docs/ - Present
✅ docs/specs/ - Present
✅ docs/adrs/ - Present

## Overview Docs (in docs/)
✅ architecture-overview.md - Present
✅ api-overview.md - Present
✅ data-model.md - Present
✅ deployment.md - Present
✅ security.md - Present
✅ testing-overview.md - Present
✅ ui-guide.md - Present

## CLAUDE.md Sections
✅ Overview/Stack - Complete
✅ Project Structure - Complete
⚠️  Commands - Missing deploy command
✅ Environment Variables - Complete

## Version Consistency
✅ Next.js: 16.1.3 (package.json) matches "Next.js 16" (docs)
❌ React: 19.0.0 (package.json) but docs say "React 18"

## Ideas Cross-Reference
✅ ideas/leaf-nextjs-convex/ exists
✅ Stack matches between spaces/ and ideas/
⚠️  project-brief.md says "Next.js 15" - outdated

## Issues Found
1. React version mismatch in documentation
2. project-brief.md has outdated version

## Recommendations
1. Update React version in CLAUDE.md
2. Update project-brief.md to say Next.js 16
3. Fill in overview doc templates with project-specific content
```

## Fixing Missing Structure

If docs/ structure is missing, create it:
```bash
mkdir -p spaces/[project]/docs/specs
mkdir -p spaces/[project]/docs/adrs
cp shared/templates/docs/*.md spaces/[project]/docs/
```

## When to Use

- After initial project scaffolding
- Before starting implementation work
- After upgrading dependencies
- Monthly maintenance checks
- When onboarding to existing project

## Integration

```
/validate-space → Fix issues → /validate-space again → /implement
```

## Stack-Specific Checks

### Next.js Projects
- Check for `next.config.js` or `next.config.ts`
- Verify `src/app/` structure for App Router
- Check for `public/` directory

### Convex Projects
- Check for `convex/` directory
- Verify `convex/schema.ts` exists
- Check for `convex/_generated/`

### General JS/TS
- Verify `tsconfig.json` if TypeScript
- Check for `.env.example` if env vars documented
- Verify `.gitignore` exists
