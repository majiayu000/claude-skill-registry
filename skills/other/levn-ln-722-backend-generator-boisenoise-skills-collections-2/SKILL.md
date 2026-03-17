---
name: ln-722-backend-generator
description: Generates .NET Clean Architecture backend structure from entity definitions
---

# ln-722-backend-generator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Generates complete .NET backend structure following Clean Architecture principles.

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | Project name, entity list, configuration options |
| **Output** | Complete .NET solution with layered architecture |
| **Target** | .NET 10+, ASP.NET Core |

**Scope boundaries:**
- Generates project structure and boilerplate code
- Creates MockData for initial development
- Does not implement business logic or database connections

---

## Workflow

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| 1 | Receive Context | Get project name, entities, options from coordinator | Configuration |
| 2 | Create Solution | Create .sln and .csproj files | Empty solution structure |
| 3 | Generate Domain | Create entities, enums, base classes | Domain project files |
| 4 | Generate API | Create controllers, DTOs, middleware | API project files |
| 5 | Verify | Build solution, check references | Build success |

---

## Phase 1: Receive Context

Accept delegation from ln-720-structure-migrator.

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `projectName` | string | Yes | Solution and project name prefix |
| `targetPath` | string | Yes | Directory for generated solution |
| `targetFramework` | string | Yes | .NET version (e.g., net10.0) |
| `entities` | list | Yes | Entity names to generate |
| `features` | list | Yes | Feature groupings for MockData |

**Options:**

| Option | Default | Effect |
|--------|---------|--------|
| `useSwagger` | true | Add Swashbuckle for API docs |
| `useSerilog` | true | Add structured logging |
| `useHealthChecks` | true | Add health endpoints |
| `createMockData` | true | Generate mock data classes |

---

## Phase 2: Create Solution

Generate solution file and project structure.

| Step | Action | Reference |
|------|--------|-----------|
| 2.1 | Create solution directory | — |
| 2.2 | Generate .sln file | — |
| 2.3 | Create project directories | `layer_structure.md` |
| 2.4 | Generate .csproj files per layer | `layer_structure.md` |
| 2.5 | Add project references | `layer_structure.md` |

**Generated projects:**

| Project | Purpose |
|---------|---------|
| `{Project}.Api` | HTTP endpoints, middleware |
| `{Project}.Domain` | Entities, enums |
| `{Project}.Services` | Business logic interfaces |
| `{Project}.Repositories` | Data access interfaces |
| `{Project}.Shared` | Cross-cutting utilities |

---

## Phase 3: Generate Domain

Create domain layer files.

| Step | Action | Reference |
|------|--------|-----------|
| 3.1 | Create `BaseEntity` class | `entity_patterns.md` |
| 3.2 | Generate entity classes per input | `entity_patterns.md` |
| 3.3 | Generate status enums | `entity_patterns.md` |
| 3.4 | Create folder structure | `layer_structure.md` |

**Entity generation rules:**

| Entity Property | Generated As |
|-----------------|--------------|
| Primary key | `public Guid Id { get; set; }` |
| String field | `public string Name { get; set; } = string.Empty;` |
| Status field | `public {Entity}Status Status { get; set; }` |
| Timestamps | `CreatedAt`, `UpdatedAt` from BaseEntity |

---

## Phase 4: Generate API

Create API layer files.

| Step | Action | Reference |
|------|--------|-----------|
| 4.1 | Generate Program.cs | `program_sections.md` |
| 4.2 | Generate controllers per entity | `controller_patterns.md` |
| 4.3 | Generate DTOs per entity | `controller_patterns.md` |
| 4.4 | Generate middleware classes | `layer_structure.md` |
| 4.5 | Generate extension methods | `program_sections.md` |
| 4.6 | Generate MockData classes (if enabled) | `layer_structure.md` |
| 4.7 | Add NuGet packages | `nuget_packages.md` |

**Controller endpoints per entity:**

| Endpoint | Method | Route |
|----------|--------|-------|
| GetAll | GET | `/api/{entities}` |
| GetById | GET | `/api/{entities}/{id}` |
| Create | POST | `/api/{entities}` |
| Update | PUT | `/api/{entities}/{id}` |
| Delete | DELETE | `/api/{entities}/{id}` |

---

## Phase 5: Verify

Validate generated solution.

| Check | Command | Expected |
|-------|---------|----------|
| Solution builds | `dotnet build` | Success, no errors |
| Project references | Check .csproj | All references valid |
| Files created | Directory listing | All expected files present |

---

## Generated Structure Summary

| Layer | Folders | Files per Entity |
|-------|---------|------------------|
| Api | Controllers/, DTOs/, Middleware/, MockData/, Extensions/ | Controller, DTO |
| Domain | Entities/, Enums/, Common/ | Entity, Status enum |
| Services | Interfaces/ | Interface (stub) |
| Repositories | Interfaces/ | Interface (stub) |
| Shared | — | Utility classes |

---

## Critical Rules

- **Single Responsibility:** Generate only backend structure, no frontend
- **Idempotent:** Can re-run to regenerate (will overwrite)
- **Build Verification:** Must verify `dotnet build` passes
- **Clean Architecture:** Respect layer dependencies (inner layers independent)
- **No Business Logic:** Generate structure only, not implementation
- **MockData First:** Enable immediate API testing without database

---

## Definition of Done

- [ ] Solution file created with all projects
- [ ] All project references configured correctly
- [ ] Domain entities generated for all input entities
- [ ] Controllers generated with CRUD endpoints
- [ ] DTOs generated for request/response
- [ ] MockData classes generated (if enabled)
- [ ] Program.cs configured with all services
- [ ] `dotnet build` passes successfully
- [ ] Swagger UI accessible (if enabled)

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| Build failure | `dotnet build` fails | Check .csproj references, verify SDK version |
| Missing references | CS0246 errors | Add missing project references |
| Invalid entity names | Build or runtime errors | Validate entity names before generation |
| Path conflicts | File exists errors | Check target path, prompt before overwrite |
| Package restore failure | NuGet errors | Verify network, check package names |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/layer_structure.md` | Project organization, folder structure, dependencies |
| `references/entity_patterns.md` | Entity generation rules, property patterns |
| `references/controller_patterns.md` | Controller and DTO generation rules |
| `references/program_sections.md` | Program.cs structure and service registration |
| `references/nuget_packages.md` | Required and optional NuGet packages |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
