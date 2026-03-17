---
name: writing-plans
description: Use when you have a spec, PRD, requirements, or feature request that needs an implementation plan before coding.
model: haiku
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# Writing Plans (Router)

## Overview

This skill routes to the appropriate stack-specific planning skill. It does NOT contain planning logic itself.

**Announce at start:** "I'm using the writing-plans skill to route to the appropriate planner."

## When to Use
- Spec, PRD, or requirements document exists
- Work involves multiple implementation steps
- Need a structured plan before coding begins

## When NOT to Use
- Simple single-file change (just do it)
- Exploratory spike work (use investigation skills)
- Plan already exists in `_docs/plans/`

## Route Table

| Work Unit Type | Route To | Context to Load First |
|----------------|----------|----------------------|
| **Backend** | **REQUIRED:** `saurun:dotnet-writing-plans` | **REQUIRED:** `saurun:dotnet-tactical-ddd` |
| **Frontend** | **REQUIRED:** `saurun:react-writing-plans` | **REQUIRED:** `saurun:react-tailwind-v4-components` |
| **Scaffold** | Both skills, backend first | Both context skills |
| **Integration** | Both skills, backend first | Both context skills |

## Detection Heuristics

**Backend signals:**
- Spec mentions: API endpoints, database, entities, domain logic, authentication, authorization
- Files involved: `*.cs`, `Controllers/`, `Services/`, `Domain/`, `Infrastructure/`

**Frontend signals:**
- Spec mentions: components, pages, forms, UI, user interactions, state management
- Files involved: `*.tsx`, `*.ts`, `components/`, `stores/`, `pages/`

**Scaffold signals:**
- No `CLAUDE.md` in working directory
- Spec describes a new application from scratch

**Integration signals:**
- Spec describes end-to-end feature spanning API and UI
- Both backend and frontend files will be created/modified

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling generic planning without routing | Always detect work unit type first |
| Writing one plan for full-stack feature | Create separate backend and frontend plans |
| Skipping context skill before planning | Context skills inform the planner about patterns |
| Frontend plan before backend | Backend first — frontend depends on API contracts |
