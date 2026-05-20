---
name: dotnet-writing-plans
description: Use when you have a spec or requirements for a multi-step .NET backend task, before touching code. Creates concise implementation plans that reference architecture contracts.
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# .NET Writing Plans

## Overview

Plans are **architectural blueprints**, not copy-paste code. Each task references contracts defined in the architecture doc. Implementers use TDD skills to fill in the actual code.

**Announce at start:** "I'm using the dotnet-writing-plans skill to create the implementation plan."

**Save plans to:** `_docs/plans/YYYY-MM-DD-<feature-name>.md`

## When NOT to Use
- Single-file bug fix with obvious cause and fix
- Config/environment changes (appsettings, launchSettings, .csproj tweaks)
- Renaming or moving files without logic changes
- Adding a NuGet package with no code changes beyond the import

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** **REQUIRED SUB-SKILL:** Use `saurun:dotnet-tdd` to implement this plan task-by-task with TDD.

**Goal:** [One sentence describing what this builds]

**Architecture:** `_docs/specs/{DATE}-{feature}-architecture.md`

**Tech Stack:** .NET 9, ASP.NET Core, EF Core 9, SQLite, xUnit, NSubstitute

---
```

## Task Structure

```markdown
### Task N: [Name]

**Implements:** [Contract reference from Architecture doc, e.g., "POST /lists/{id}/items (Architecture §API Contract)"]

**Files:**
- Create: `exact/path/to/File.cs`
- Test: `tests/exact/path/to/FileTests.cs`

**Behaviors:**
- [Happy path behavior]
- [Error case 1]
- [Error case 2]

**Dependencies:** Task X (if applicable)
```

## Backend Task Examples

### Domain Entity Task

```markdown
### Task 2: ShoppingList aggregate

**Implements:** ShoppingList entity (Architecture §Entity Model)

**Files:**
- Create: `Domain/Aggregates/ShoppingList.cs`
- Test: `Tests/Domain/ShoppingListTests.cs`

**Behaviors:**
- Creating with valid name initializes empty items collection
- Adding item with valid name increases item count
- Adding item when at max capacity throws DomainException
- Removing non-existent item throws DomainException
```

### API Endpoint Task

```markdown
### Task 5: AddItem endpoint

**Implements:** POST /lists/{id}/items (Architecture §API Contract)

**Files:**
- Create: `Api/Endpoints/ShoppingListEndpoints.cs`
- Test: `Tests/Api/ShoppingListEndpointsTests.cs`

**Behaviors:**
- Valid input → 201 with ShoppingItemDto
- Validates per Architecture §API Contract

**Dependencies:** Task 2 (ShoppingList entity), Task 4 (DbContext)
```

> **Note:** 401/404 for auth/invalid-id are omitted — standard patterns assumed. Validation rules reference architecture, not repeated.

### Infrastructure Task

```markdown
### Task 4: EF Core DbContext and migrations

**Implements:** Data persistence (Architecture §Infrastructure Decisions)

**Files:**
- Create: `Infrastructure/AppDbContext.cs`
- Create: `Infrastructure/Configurations/ShoppingListConfiguration.cs`
- Modify: `Program.cs` (add DbContext registration)

**Behaviors:**
- DbContext configured with SQLite provider
- ShoppingList entity mapped with owned Items collection
- Migration creates tables matching entity model

**Dependencies:** Task 2 (ShoppingList entity)
```

## What Plans Include

| Element | Required |
|---------|----------|
| Exact file paths (Create/Modify/Test) | ✓ |
| Contract reference (`Implements:`) | ✓ |
| Behaviors (one line each) | ✓ |
| Task dependencies | When applicable |

## What Plans Do NOT Include

| Element | Reason |
|---------|--------|
| Full test code | TDD skill generates tests from behaviors |
| Full implementation code | Implementer writes from contract + behaviors |
| Step-by-step TDD instructions | TDD skill handles workflow |
| Expected failure messages | TDD skill handles verification |
| "What bugs does this catch?" table | Behaviors implicitly define bug coverage |
| Validation rules | Architecture §API Contract defines these — just reference it |
| DTO field lists | Architecture §API Contract defines these — just reference it |
| Standard auth behaviors (`401 for unauthed`) | Universal pattern — assumed for all `[Authorize]` endpoints |
| Standard `404 for invalid ID` | Universal pattern — assumed for all `{id}` routes |
| Mapper descriptions like "maps X to Y" | Obvious from naming convention |

**Token budget:** Plans for autonomous agents, not humans. Every repeated pattern wastes tokens. If architecture defines it, reference it — don't repeat it.

## Test Infrastructure Task

**Task 1 of every plan MUST set up test infrastructure:**

```markdown
### Task 1: Test infrastructure setup

**Implements:** Shared test helpers (N/A - infrastructure)

**Files:**
- Create: `Tests/CustomWebApplicationFactory.cs`
- Create: `Tests/TestHelpers.cs`

**Behaviors:**
- CustomWebApplicationFactory configured with SQLite in-memory
- TestHelpers provides authenticated HttpClient creation
- IClassFixture pattern ready for integration tests
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing full test/implementation code | Just list behaviors — TDD skill writes code |
| Forgetting `Implements:` reference | Every task MUST reference architecture contract |
| Vague behaviors like "handles errors" | Be specific: "Empty name → returns 400" |
| Missing file paths | Every task MUST list exact Create/Modify/Test paths |
| Tasks too large (>3 files) | Split into smaller tasks |
| No test infrastructure in Task 1 | `CustomWebApplicationFactory` + helpers MUST be Task 1 |
| Repeating validation rules from architecture | Just write `Validates per Architecture §API Contract` |
| Listing DTO fields | Reference architecture — `AuthResponse per Architecture §DTOs` |
| Writing "when not authenticated → 401" for every endpoint | Omit — assumed for `[Authorize]` endpoints |
| Writing "invalid id → 404" for every endpoint | Omit — assumed for `{id}` routes |
| Describing what mappers do | `CategoryMapper` obviously maps Category → omit |

## Completion

After saving the plan, report:

**"Plan saved to `_docs/plans/<filename>.md`. Ready for execution."**
