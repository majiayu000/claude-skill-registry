---
name: ln-700-project-bootstrap
description: Orchestrates full project bootstrap from Replit export to production-ready structure
---

# ln-700-project-bootstrap

**Type:** L1 Top Orchestrator
**Category:** 7XX Project Bootstrap

Transforms a prototype project (Replit export or early-stage repo) into a production-ready codebase with Clean Architecture, Docker, CI/CD, and development tooling.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Source project directory |
| **Output** | Production-ready project with all infrastructure |
| **Delegations** | ln-710 -> ln-720 -> ln-730 -> ln-740 -> ln-750 -> ln-760 -> ln-770 -> ln-780 |
| **Duration** | ~30 minutes (vs 4+ hours manual) |

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
    Type: Monolith (Replit default)
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
- Create .NET backend: Kehai.Api, Kehai.Domain, etc.
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

| Order | Skill | Purpose | Depends On |
|-------|-------|---------|------------|
| 1 | ln-710 | Upgrade dependencies | - |
| 2 | ln-720 | Restructure project | ln-710 |
| 3 | ln-730 | Setup Docker/CI | ln-720 |
| 4 | ln-740 | Configure quality tools | ln-720 |
| 5 | ln-750 | Generate .claude/commands | ln-720 |
| 6 | ln-760 | Security scanning | ln-710 |
| 7 | ln-770 | Crosscutting concerns | ln-720 |
| 8 | ln-780 | Build and verify | All above |

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
     backend: /project/src/Kehai.Api

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

| Error | Action |
|-------|--------|
| No package.json | Abort: "Not a Node.js project" |
| Unsupported stack | Abort: "Stack not supported: {stack}" |
| Permission denied | Abort: "Cannot write to {path}" |

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

**Version:** 1.0.0
**Last Updated:** 2026-01-10
