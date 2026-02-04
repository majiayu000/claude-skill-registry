---
name: ln-720-structure-migrator
description: Coordinates project structure migration to Clean Architecture
---

# ln-720-structure-migrator

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates project restructuring from prototype layout to Clean Architecture.

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | Current project structure, target architecture |
| **Output** | Restructured project with Clean Architecture |
| **Workers** | ln-721 (frontend), ln-722 (backend), ln-723 (mockdata), ln-724 (replit-cleaner) |

**Scope boundaries:**
- Analyzes current project structure
- Generates migration plan
- Delegates to specialized workers
- Verifies final result

---

## Workflow

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| 1 | Analyze | Scan current structure, detect framework, map files | File inventory |
| 2 | Plan | Calculate moves, identify conflicts | Migration plan |
| 3 | Execute | Delegate to workers (ln-724, ln-721, ln-722, ln-723) via Task tool | Restructured project |
| 4 | Verify | Run builds, check imports, validate structure | Success report |

---

## Target Structures

### Frontend (React)

```
src/frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── layout/      # AppLayout, Header, Sidebar
│   │   └── ui/          # Reusable UI components
│   ├── contexts/        # React contexts
│   ├── hooks/           # Custom hooks
│   ├── lib/             # Utilities, API clients
│   ├── pages/           # Page components
│   │   └── {Feature}/   # Feature-specific files
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── vite.config.ts
└── tsconfig.json
```

### Backend (.NET Clean Architecture)

```
src/
├── {Project}.Api/
│   ├── Controllers/
│   ├── DTOs/
│   ├── Middleware/
│   ├── MockData/
│   ├── Extensions/
│   ├── Program.cs
│   └── appsettings.json
├── {Project}.Domain/
│   ├── Entities/
│   ├── Enums/
│   └── Common/
├── {Project}.Services/
│   └── Interfaces/
├── {Project}.Repositories/
│   └── Interfaces/
└── {Project}.Shared/
```

---

## Delegation Protocol

### To ln-724 (Replit Cleanup)

```yaml
Context:
  projectPath: /project
  skipPreview: false  # Set true for automated pipelines
Options:
  cleanConfigFiles: true      # .replit, replit.nix
  cleanDirectories: true      # .local/, .cache/, .upm/
  cleanPackages: true         # @replit/* from package.json
  cleanViteConfig: true       # Replit imports/plugins
  cleanCodeComments: true     # // @replit annotations
  cleanGitignore: true        # .replit entry
```

### To ln-721 (Frontend)

```yaml
Context:
  sourcePath: /project/client
  targetPath: /project/src/frontend
  framework: react
  features:
    - ProductPlanning
    - Settings
    - Profile
Options:
  splitMonolithicFiles: true
  extractConstants: true
  extractTypes: true
  createComponentLibrary: true
```

### To ln-722 (Backend)

```yaml
Context:
  projectName: Kehai
  targetPath: /project/src
  targetFramework: net10.0
  features:
    - ProductPlanning
    - Users
Options:
  createMockData: true
  addSwagger: true
  addHealthChecks: true
```

### To ln-723 (MockData)

```yaml
Context:
  sourceORM: drizzle
  sourcePath: /project/shared/schema.ts
  targetPath: /project/src/Kehai.Api/MockData
  entities:
    - Epic
    - Story
    - Bet
```

---

## Critical Rules

- **Orchestrator Pattern:** Analyze and delegate, do not execute transformations directly
- **Sequential Workers:** Execute workers in order (replit-cleanup → frontend → backend → mockdata)
- **Pre-flight Checks:** Verify git status clean, target paths available
- **No Data Loss:** Copy before delete, verify before removing source
- **Build Verification:** Both `npm run build` and `dotnet build` must pass
- **Rollback Ready:** Keep backup branch until verification complete

---

## Definition of Done

- [ ] Current structure analyzed and documented
- [ ] Migration plan generated
- [ ] ln-724 completed: Replit artifacts removed
- [ ] ln-721 completed: Frontend restructured
- [ ] ln-722 completed: Backend generated
- [ ] ln-723 completed: MockData migrated
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Backend builds successfully (`dotnet build`)
- [ ] No orphan files in old locations
- [ ] All imports resolve correctly
- [ ] Migration report generated

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| Uncommitted changes | `git status` not clean | Require clean working directory |
| Build failure (frontend) | `npm run build` fails | Rollback, delegate to ln-721 for fix |
| Build failure (backend) | `dotnet build` fails | Rollback, delegate to ln-722 for fix |
| Lost files | Files missing after migration | Restore from backup branch |
| Import errors | Module not found | Re-run import update phase |
| Partial migration | Worker fails mid-execution | Atomic: complete all or rollback all |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/clean_architecture_dotnet.md` | .NET project structure template |
| `references/frontend_structure.md` | React project structure template |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
