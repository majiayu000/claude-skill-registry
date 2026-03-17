---
name: ln-720-structure-migrator
description: "Coordinates project structure: SCAFFOLD new or RESTRUCTURE existing to Clean Architecture"
---

# ln-720-structure-migrator

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates project restructuring to Clean Architecture. Mode-aware: delegates to workers with appropriate mode parameters based on CREATE/TRANSFORM pipeline.

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | Current project structure + mode (CREATE/TRANSFORM) from ln-700 |
| **Output** | Restructured project with Clean Architecture |
| **Workers** | See Workers table below |

### Workers

| Worker | Role | CREATE mode | TRANSFORM mode |
|--------|------|-------------|----------------|
| ln-721 | Frontend structure | SCAFFOLD (generate starter) | RESTRUCTURE (migrate monolith) |
| ln-722 | Backend generator | RUN (generate backend) | RUN (generate backend) |
| ln-723 | Seed data | GENERATE (from entities) | MIGRATE (from ORM schemas) |
| ln-724 | Artifact cleaner | **SKIP** (no artifacts) | **CONDITIONAL** (only if platform detected) |

**Scope boundaries:**
- Analyzes current project structure (TRANSFORM) or accepts target config (CREATE)
- Generates migration plan or scaffold plan
- Delegates to specialized workers via Task tool
- Verifies final result

---

## Workflow

| Phase | Name | CREATE mode | TRANSFORM mode |
|-------|------|-------------|----------------|
| 1 | Analyze | Receive target stack config | Scan structure, detect framework, map files |
| 2 | Plan | Calculate scaffold actions | Calculate moves, identify conflicts |
| 3 | Execute | Delegate: ln-721 SCAFFOLD → ln-722 → ln-723 GENERATE | Delegate: ln-724 (conditional) → ln-721 RESTRUCTURE → ln-722 → ln-723 MIGRATE |
| 4 | Verify | Check file structure, validate configs | Run builds, check imports, validate structure |

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

### To ln-724 (Artifact Cleaner)

**When to invoke:** TRANSFORM mode AND platform artifacts detected (`.replit`, `.stackblitzrc`, `sandbox.config.json`, `glitch.json`).
**Skip conditions:** CREATE mode OR no platform config files found.

```yaml
Context:
  projectPath: /project
  skipPreview: false
Options:
  # ln-724 auto-detects platform, no need to specify
  cleanConfigFiles: true
  cleanDirectories: true
  cleanPackages: true
  cleanBuildConfig: true
  cleanCodeComments: true
  cleanGitignore: true
```

### To ln-721 (Frontend)

```yaml
Context:
  mode: SCAFFOLD | RESTRUCTURE          # From pipeline mode
  # SCAFFOLD mode:
  targetPath: /project/src/frontend
  projectName: MyApp
  # RESTRUCTURE mode:
  sourcePath: /project/client
  targetPath: /project/src/frontend
  framework: react
  features:
    - Dashboard
    - Settings
    - Profile
Options:
  # RESTRUCTURE only:
  splitMonolithicFiles: true
  extractConstants: true
  extractTypes: true
  createComponentLibrary: true
```

### To ln-722 (Backend)

```yaml
Context:
  projectName: MyApp
  targetPath: /project/src
  targetFramework: net10.0
  features:
    - Dashboard
    - Users
Options:
  createMockData: true
  addSwagger: true
  addHealthChecks: true
```

### To ln-723 (Seed Data)

```yaml
Context:
  mode: MIGRATE | GENERATE              # From pipeline mode
  targetFormat: csharp | typescript | python | json | sql
  # MIGRATE mode:
  sourceORM: auto                        # Auto-detect (drizzle/prisma/typeorm/efcore/sqlalchemy/django)
  sourcePath: /project/shared/schema.ts
  # GENERATE mode:
  entities:                              # Optional — if empty, starter template used
    - name: User
      fields: [id, name, email, role, createdAt]
    - name: Role
      fields: [id, name, description]
  targetPath: /project/src/MyApp.Api/MockData
```

---

## Critical Rules

- **Orchestrator Pattern:** Analyze and delegate via Task tool, do not execute transformations directly
- **Mode Awareness:** Pass correct mode to all workers — CREATE vs TRANSFORM determines worker behavior
- **Conditional Workers:** ln-724 runs ONLY in TRANSFORM mode when platform artifacts detected; SKIP otherwise
- **Sequential Workers:** Execute in order (ln-724 conditional → ln-721 → ln-722 → ln-723)
- **Pre-flight Checks:** Verify git status clean, target paths available
- **No Data Loss:** Copy before delete, verify before removing source (TRANSFORM mode)
- **Build Verification:** All builds must pass (`npm run build`, `dotnet build`)
- **Rollback Ready:** Keep backup branch until verification complete (TRANSFORM mode)

---

## Definition of Done

**CREATE mode:**
- [ ] Target stack config received from ln-700
- [ ] ln-721 completed: Frontend scaffolded (SCAFFOLD mode)
- [ ] ln-722 completed: Backend generated
- [ ] ln-723 completed: Seed data generated (GENERATE mode)
- [ ] File structure matches target templates
- [ ] All configs valid (package.json, tsconfig.json, .csproj)

**TRANSFORM mode:**
- [ ] Current structure analyzed and documented
- [ ] Migration plan generated
- [ ] ln-724 completed: Platform artifacts removed (if applicable)
- [ ] ln-721 completed: Frontend restructured (RESTRUCTURE mode)
- [ ] ln-722 completed: Backend generated
- [ ] ln-723 completed: Seed data migrated (MIGRATE mode)
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
| Wrong worker mode | Mode mismatch | Validate mode parameter before delegation |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/clean_architecture_dotnet.md` | .NET project structure template |
| `references/frontend_structure.md` | React project structure template |

---

**Version:** 3.0.0
**Last Updated:** 2026-02-07
