---
name: bootstrap
description: "(ePost) Scaffold new projects or modules — auto-detects scope"
user-invokable: true
context: fork
agent: epost-implementer
metadata:
  argument-hint: "[project or module description]"
  connections:
    enhances: [bootstrap-fast, bootstrap-parallel]
---

# Bootstrap — Unified Scaffolding Command

Scaffold new projects or modules with automatic scope detection.

## Scope Auto-Detection

### New Module (within existing project)
**Detection:** CWD is inside an existing project (has `package.json`, `build.gradle`, etc.) AND request describes a module/feature
**Action:** Scaffold module structure:
- For web B2B: Create knowledge file from `domain-b2b/references/module-template.md`, scout existing files, populate knowledge, update module index
- For other platforms: Create appropriate directory structure and boilerplate

### New Project (greenfield)
**Detection:** No existing project structure detected OR request says "new project/app"
**Action:** Full project bootstrap:
1. Git init (main branch)
2. Research tech stack (epost-researcher, max 5 sources)
3. Create implementation plan (epost-architect)
4. Design guidelines if UI project (epost-muji)
5. Implement step by step (linear, sequential)
6. Run tests (epost-tester), fix failures (epost-debugger)
7. Code review (epost-reviewer), iterate until clean
8. Create docs (README.md, project-overview-pdr.md)
9. Git commit (DO NOT push)

## Complexity → Variant

- Single-module project → `:fast` (linear)
- Multi-module project → `:parallel` (concurrent)

<request>$ARGUMENTS</request>

**IMPORTANT:** Analyze the skills catalog and activate needed skills.
