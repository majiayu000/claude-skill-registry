---
name: ln-700-project-bootstrap
description: "Universal project bootstrapper: CREATE new or TRANSFORM existing project to production-ready structure"
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-700-project-bootstrap

**Type:** L1 Top Orchestrator
**Category:** 7XX Project Bootstrap

Universal project bootstrapper with two modes: CREATE (generate production-ready project from scratch) or TRANSFORM (migrate existing prototype from any platform to production structure). Output: Clean Architecture, Docker, CI/CD, quality tooling.

---

## Mode Selection

| Aspect | CREATE | TRANSFORM |
|--------|--------|-----------|
| **Input** | Empty directory or target stack config | Existing project (Replit, StackBlitz, CodeSandbox, Glitch, custom) |
| **Detection** | No source files found | Source files + optional platform config detected |
| **ln-710** | SKIP (no deps to upgrade) | RUN (upgrade existing deps) |
| **ln-720** | SCAFFOLD + GENERATE | RESTRUCTURE + MIGRATE |
| **ln-724** | SKIP (no artifacts) | CONDITIONAL (if platform detected) |
| **ln-730–780** | RUN (same for both modes) | RUN (same for both modes) |

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Empty directory (CREATE) or source project (TRANSFORM) |
| **Output** | Production-ready project with all infrastructure |
| **Delegations** | ln-710 (conditional) -> ln-720 -> ln-730 -> ln-740 -> ln-750 -> ln-760 -> ln-770 -> ln-780 |

---

## Workflow

```
Phase 0: Analyze (Tech Detection)
    |
    v
Phase 1: Plan (Generate Transformation Plan)
    |
    v
Phase 2: Confirm (User Approval)
    |
    v
Phase 3: Execute (Delegate to L2 Coordinators)
    |
    +---> ln-710: Dependency Upgrader
    +---> ln-720: Structure Migrator
    +---> ln-730: DevOps Setup
    +---> ln-740: Quality Setup
    +---> ln-750: Commands Generator
    +---> ln-760: Security Setup
    +---> ln-770: Crosscutting Setup
    +---> ln-780: Bootstrap Verifier
    |
    v
Phase 4: Report (Summary of Changes)
```

---

## Phase 0: Technology Detection

### Step 0.0: Mode Detection

| Condition | Mode | Action |
|-----------|------|--------|
| Empty directory (no source files) | CREATE | Ask user for target stack, project name, entities |
| Source files found | TRANSFORM | Auto-detect stack, scan for platform artifacts |
| Ambiguous (few files, unclear) | ASK | Present both options, let user choose |

### Step 0.1: CREATE Mode — User Input

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| Project name | Yes | — | MyApp |
| Target backend | Yes | — | .NET / Node.js / Python |
| Target frontend | Yes | — | React / Vue / Angular / Svelte |
| Database | Yes | — | PostgreSQL / MongoDB / MySQL |
| Main entities | No | User, Role (starter) | User, Product, Order |

### Step 0.2: Idempotency Pre-flight

If target directory contains existing files:
1. Detect existing structure (package.json, .csproj, etc.)
2. **Warn user:** "Target directory is not empty. Existing files may be overwritten."
3. Ask: **Overwrite** (replace all) / **Merge** (keep existing, add missing) / **Abort**

### Step 0.3: Technology Detection (TRANSFORM mode) / Stack Config (CREATE mode)

Analyze project to detect tech stack before delegations.

### Detection Rules

```yaml
Frontend:
  React:
    - package.json contains "react"
    - Files: *.tsx, *.jsx with React imports
  Vue:
    - package.json contains "vue"
    - Files: *.vue
  Angular:
    - package.json contains "@angular/core"
    - Files: *.component.ts
  Svelte:
    - package.json contains "svelte"
    - Files: *.svelte

Backend:
  .NET:
    - *.csproj files exist
    - *.sln files exist
  Node.js:
    - package.json + (express|fastify|nest|koa)
    - tsconfig.json or jsconfig.json
  Python:
    - requirements.txt OR pyproject.toml OR setup.py
    - (fastapi|flask|django) in dependencies
  Go:
    - go.mod exists

Database:
  PostgreSQL:
    - DATABASE_URL contains "postgres"
    - docker-compose.yml contains "postgres"
  MongoDB:
    - MONGODB_URI in env
    - docker-compose.yml contains "mongo"
  MySQL:
    - DATABASE_URL contains "mysql"

ORM:
  Drizzle: drizzle.config.ts exists
  Prisma: prisma/schema.prisma exists
  EF Core: *.csproj references Microsoft.EntityFrameworkCore
  SQLAlchemy: "sqlalchemy" in requirements
```

### Detection Output

```yaml
Detected Stack:
  Frontend:
    Framework: React
    Version: 19.x
    Build Tool: Vite
    UI Library: shadcn/ui
    State: React Query

  Backend:
    Current: Node.js + Express
    Target: .NET 10 (user preference)
    ORM: Drizzle -> EF Core

  Database:
    Type: PostgreSQL
    Version: 17

  Structure:
    Type: Monolith (Prototype)
    Origin: replit | stackblitz | codesandbox | glitch | custom
    Target: Clean Architecture
```

---

## Phase 1: Generate Transformation Plan

Based on detected stack, create detailed plan:

```markdown
# Bootstrap Transformation Plan

## Source Analysis
- Frontend: React 19 + Vite + TypeScript
- Backend: Express + Drizzle (to be replaced with .NET)
- Database: PostgreSQL 17

## Transformations

### 1. Dependencies (ln-710)
- Upgrade React 18 -> 19
- Upgrade Vite 5 -> 6
- Add missing peer dependencies

### 2. Structure (ln-720)
- Move frontend to src/frontend/
- Create .NET backend: MyApp.Api, MyApp.Domain, etc.
- Migrate mock data from Drizzle to MockData classes

### 3. DevOps (ln-730)
- Create Dockerfile.frontend (multi-stage)
- Create Dockerfile.backend (.NET SDK)
- Create docker-compose.yml
- Create .github/workflows/ci.yml

### 4. Quality (ln-740)
- Configure ESLint (flat config)
- Add Prettier
- Setup Husky + lint-staged
- Create test infrastructure (Vitest, xUnit)

### 5. Commands (ln-750)
- Generate refresh_context.md
- Generate refresh_infrastructure.md
- Generate build-and-test.md

### 6. Security (ln-760)
- Scan for hardcoded secrets
- Run npm audit
- Create SECURITY.md

### 7. Crosscutting (ln-770)
- Configure Serilog logging
- Add GlobalExceptionMiddleware
- Configure CORS policy
- Add /health endpoints
- Enable Swagger

### 8. Verification (ln-780)
- Build all projects
- Run tests
- Start Docker containers
- Verify health checks

## Estimated Changes
- Files created: ~45
- Files modified: ~12
- Files deleted: ~8 (replaced backend)
```

---

## Phase 2: User Confirmation

Present plan and ask for approval:

```
Bootstrap Plan Ready!

Summary:
- Frontend: React 19 (upgrade from 18)
- Backend: .NET 10 (replacing Node.js)
- Docker: Multi-container setup
- CI/CD: GitHub Actions
- Quality: ESLint, Prettier, Husky

Proceed with bootstrap? [Y/n]
```

If user declines, ask for modifications.

---

## Phase 3: Execute Delegations

Sequential delegation to L2 coordinators:

| Order | Skill | Purpose | CREATE mode | TRANSFORM mode | Depends On |
|-------|-------|---------|-------------|----------------|------------|
| 1 | ln-710 | Upgrade dependencies | **SKIP** | RUN | — |
| 2 | ln-720 | Structure (SCAFFOLD/RESTRUCTURE) | RUN (SCAFFOLD) | RUN (RESTRUCTURE) | ln-710 |
| 3 | ln-730 | Setup Docker/CI | RUN | RUN | ln-720 |
| 4 | ln-740 | Configure quality tools | RUN | RUN | ln-720 |
| 5 | ln-750 | Generate .claude/commands | RUN | RUN | ln-720 |
| 6 | ln-760 | Security scanning | RUN | RUN | ln-710 |
| 7 | ln-770 | Crosscutting concerns | RUN | RUN | ln-720 |
| 8 | ln-780 | Build and verify | RUN | RUN | All above |

### Delegation Protocol

For each L2 coordinator:

1. **Prepare context:**
   ```yaml
   Stack:
     frontend: { framework, version, buildTool }
     backend: { framework, version }
     database: { type, version }

   Paths:
     root: /project
     frontend: /project/src/frontend
     backend: /project/src/MyApp.Api

   Options:
     skipTests: false
     allowFailures: false
   ```

2. **Invoke skill:** Pass context as input

3. **Collect result:**
   ```yaml
   Status: success | partial | failed
   FilesCreated: [...]
   FilesModified: [...]
   Warnings: [...]
   Errors: [...]
   ```

4. **Handle errors:**
   - Log error details
   - Ask user: continue or abort?
   - If abort, rollback if possible

---

## Phase 4: Generate Report

### Bootstrap Completeness Assessment

**Context:** Final verification that bootstrap produced a working project, not just files.

| # | Category | Check | Source |
|---|----------|-------|--------|
| 1 | **Structure** | Clean Architecture layers present | ln-720 result |
| 2 | **Dependencies** | All packages installed, no version conflicts | ln-710 result |
| 3 | **DevOps** | Docker builds, CI pipeline valid | ln-730 result |
| 4 | **Quality** | Linters/formatters configured and pass | ln-740 result |
| 5 | **Security** | No hardcoded secrets, scanning configured | ln-760 result |
| 6 | **Build** | Project compiles/builds without errors | ln-780 result |

**Completeness Score = count of PASS / 6**
- 6/6: Bootstrap complete
- 4-5/6: Bootstrap complete with warnings (list failing categories)
- <4/6: Bootstrap incomplete — list blocking issues for user action

### Summary Report

Final summary after all delegations:

```yaml
Bootstrap Complete!

Duration: 24 minutes 32 seconds

Changes Summary:
  Files Created: 47
  Files Modified: 15
  Files Deleted: 9

By Category:
  Dependencies:
    - Upgraded 23 packages
    - No breaking changes detected

  Structure:
    - Created 5 .NET projects
    - Restructured frontend (12 components extracted)
    - Migrated 8 mock data files

  DevOps:
    - Created Dockerfile.frontend
    - Created Dockerfile.backend
    - Created docker-compose.yml
    - Created .github/workflows/ci.yml

  Quality:
    - Configured ESLint + Prettier
    - Installed Husky hooks
    - Created 3 test files

  Commands:
    - Generated 3 .claude/commands

  Security:
    - Scanned 156 files
    - Found 0 secrets
    - 2 vulnerability warnings (low severity)

  Crosscutting:
    - Configured Serilog
    - Added error handling
    - CORS enabled for localhost
    - Health checks at /health
    - Swagger at /swagger

Verification:
  Build: SUCCESS
  Tests: 42 passed, 0 failed
  Docker: 3 containers running
  Health: All endpoints responding

Next Steps:
  1. Open http://localhost:3000 (frontend)
  2. Open http://localhost:5000/swagger (API docs)
  3. Review generated .claude/commands
  4. Run 'git add . && git commit -m "Bootstrap complete"'
```

---

## Error Handling

### Recoverable Errors

| Error | Action |
|-------|--------|
| Dependency conflict | Try with --legacy-peer-deps |
| Build failure | Log error, suggest fix, continue |
| Test failure | Log warning, continue with --allow-failures |
| Docker build fail | Suggest Dockerfile fixes |

### Fatal Errors

| Error | Action | Mode |
|-------|--------|------|
| No package.json (TRANSFORM) | Abort: "Not a Node.js project" | TRANSFORM |
| Unsupported stack | Abort: "Stack not supported: {stack}" | Both |
| Permission denied | Abort: "Cannot write to {path}" | Both |
| No stack selected | Abort: "Target stack required for CREATE mode" | CREATE |
| Conflicting files | Abort if user chose "Abort" in pre-flight | CREATE |

---

## Configuration

### Skill Options

```yaml
Options:
  # Backend replacement
  targetBackend: ".NET" | "Node" | "Python" | "keep"

  # Frontend refactoring depth
  frontendRefactoring: "minimal" | "moderate" | "full"

  # Docker setup
  dockerEnabled: true
  dockerRegistry: null  # Optional: ghcr.io/user

  # CI/CD
  cicdProvider: "github" | "azure" | "gitlab" | "none"

  # Quality tools
  linterConfig: "recommended" | "strict"
  precommitHooks: true

  # Commands to generate
  commands: ["refresh_context", "refresh_infrastructure", "build-and-test"]

  # Verification
  runTests: true
  startContainers: true
  keepContainersRunning: true
```

### Environment Variables

```bash
# Optional: Override detection
BOOTSTRAP_FRONTEND=react
BOOTSTRAP_BACKEND=dotnet
BOOTSTRAP_DB=postgres

# Optional: Skip steps
SKIP_DEPENDENCIES=false
SKIP_DOCKER=false
SKIP_TESTS=false
```

---

## Integration with Existing Skills

| Skill | Integration |
|-------|-------------|
| ln-001-standards-researcher | Query for best practices during ln-720 |
| ln-002-best-practices-researcher | Generate guides during ln-720 |
| ln-100-documents-pipeline | Call after bootstrap for docs |
| ln-310-story-validator | Validate generated tasks |

---

## References

- [stack_detection.md](references/stack_detection.md) - Detection rules and patterns
- [transformation_plan_template.md](references/transformation_plan_template.md) - Plan template
- [verification_checklist.md](references/verification_checklist.md) - Verification steps

---

**Version:** 2.0.0
**Last Updated:** 2026-02-07
