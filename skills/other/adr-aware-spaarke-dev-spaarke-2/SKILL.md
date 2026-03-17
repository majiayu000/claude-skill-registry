# adr-aware

---
description: Automatically load and apply relevant ADRs when creating or modifying resources
tags: [adr, architecture, design, conventions]
techStack: [all]
appliesTo: ["**/*.cs", "**/*.ts", "**/*.tsx"]
alwaysApply: true
---

## Purpose

Ensures Architecture Decision Records (ADRs) are automatically considered when AI agents create or modify code. This skill provides **proactive ADR awareness** versus reactive checking (which is handled by `adr-check`).

**Philosophy:**
- `adr-aware` (this skill) = **BEFORE** - Load relevant ADRs when starting work
- `adr-check` = **AFTER** - Validate completed work against all ADRs

---

## Always-Apply Rules

### Rule 1: Resource-Type to ADR Mapping

**When creating or modifying these resource types, automatically load the specified ADRs:**

| Resource Type | Detection Pattern | Required ADRs |
|---------------|-------------------|---------------|
| **API Endpoint** | `*Endpoints.cs`, `*Handler.cs`, `Program.cs` routes | ADR-001, ADR-008, ADR-010 |
| **AI Endpoint/Service** | `Api/Ai/*`, `*DocumentIntelligence*`, `*Analysis*`, `*Ai*` | ADR-013, ADR-015, ADR-016, ADR-018, ADR-019, ADR-020 |
| **Authorization** | `*Authorization*.cs`, `*Filter.cs`, `*Policy*.cs` | ADR-003, ADR-008 |
| **Caching** | `*Cache*.cs`, `IDistributedCache`, `IMemoryCache` | ADR-009 |
| **Dataverse Plugin** | `*Plugin.cs` in plugins folder | ADR-002 |
| **Graph/SPE Integration** | `*Spe*.cs`, `*Graph*.cs`, `*Drive*.cs` | ADR-007 |
| **PCF Control** | `*.tsx` in pcf/, `ControlManifest.Input.xml` | ADR-006, ADR-011, ADR-012, ADR-021 |
| **Webresource** | `*.js` in webresources/ | ADR-006 |
| **DI Registration** | `Program.cs` DI section, `Add*` extension methods | ADR-010 |
| **Background Worker** | `*Worker.cs`, `*Service.cs` implementing `BackgroundService` | ADR-001, ADR-004 |
| **Job Status/Persistence** | `*JobStatus*`, `JobOutcome`, `JobContract` | ADR-004, ADR-017, ADR-020 |
| **Feature Flags / Kill Switches** | `*Feature*`, `FeatureFlag`, `IOptions*` gates | ADR-018 |
| **API Errors / ProblemDetails** | `ProblemDetails`, `Results.Problem`, `IResult` error helpers | ADR-019 |
| **Versioning** | `v1/`, `ApiVersion`, contracts/DTO versioning | ADR-020 |
| **Storage/Documents** | `*Store*.cs`, `*Document*.cs`, `*File*.cs` | ADR-005, ADR-007 |

### Rule 2: Automatic Context Loading (Two-Tier Strategy)

When a task or prompt involves creating/modifying files matching the patterns above:

```
BEFORE writing any code:
  1. IDENTIFY resource types from task/file patterns
  2. LOOKUP applicable ADRs from mapping table (Rule 1)

  3. LOAD Tier 1 context (concise, AI-optimized):
     a. LOAD .claude/constraints/{domain}.md for MUST/MUST NOT rules
        - API work → .claude/constraints/api.md
        - PCF work → .claude/constraints/pcf.md
        - Plugin work → .claude/constraints/plugins.md
        - Auth work → .claude/constraints/auth.md
        - Caching work → .claude/constraints/data.md
        - AI work → .claude/constraints/ai.md
        - Testing → .claude/constraints/testing.md

     b. LOAD .claude/adr/ADR-XXX.md for each applicable ADR
        - These are 100-150 line concise versions
        - Focus on constraints, not full rationale

     c. LOAD .claude/patterns/{domain}/*.md for code examples
        - API patterns → .claude/patterns/api/
        - Auth patterns → .claude/patterns/auth/
        - PCF patterns → .claude/patterns/pcf/
        - Dataverse patterns → .claude/patterns/dataverse/

  4. IF more context needed (rare):
     → READ docs/adr/ADR-XXX-*.md for full rationale and history

  5. APPLY constraints during implementation
```

### Resource Type to Context Files Mapping

| Resource Type | Constraints File | Pattern Directory | ADRs |
|---------------|------------------|-------------------|------|
| API Endpoint | `.claude/constraints/api.md` | `.claude/patterns/api/` | ADR-001, 008, 010 |
| PCF Control | `.claude/constraints/pcf.md` | `.claude/patterns/pcf/` | ADR-006, 011, 012, 021 |
| Plugin | `.claude/constraints/plugins.md` | `.claude/patterns/dataverse/` | ADR-002 |
| Auth/OAuth | `.claude/constraints/auth.md` | `.claude/patterns/auth/` | ADR-003, 008 |
| Caching | `.claude/constraints/data.md` | `.claude/patterns/caching/` | ADR-009 |
| AI Features | `.claude/constraints/ai.md` | `.claude/patterns/ai/` | ADR-013, 014, 015, 016 |
| Background Jobs | `.claude/constraints/jobs.md` | — | ADR-001, 004, 017 |
| Testing | `.claude/constraints/testing.md` | `.claude/patterns/testing/` | ADR-022 |

### Rule 3: ADR Constraint Comments

When writing code affected by ADRs, include a brief ADR reference comment:

```csharp
// ✅ DO: Reference ADRs in significant architectural code
public static class NavMapEndpoints
{
    /// <summary>
    /// ADR Compliance:
    /// - ADR-001: Minimal API (no controllers)
    /// - ADR-008: Endpoint-level authorization
    /// - ADR-009: Redis-first caching (L1 exception for metadata)
    /// </summary>
    public static void MapNavMapEndpoints(this WebApplication app) { }
}

// ❌ DON'T: Clutter every method - only significant decisions
public string FormatDate(DateTime dt) => dt.ToString("yyyy-MM-dd"); // No ADR ref needed
```

### Rule 4: ADR Violation Prevention

If about to write code that violates an ADR:

```
IF detected violation pattern:
  1. STOP before writing
  2. NOTIFY user with:
     🔔 **ADR Conflict Detected**
     
     **ADR**: {ADR-XXX} - {Title}
     **Constraint**: {Specific rule being violated}
     **Intended Code**: {What you were about to write}
     **Compliant Alternative**: {What to write instead}
     
     Proceed with compliant alternative? (y/n)
  3. AWAIT confirmation before continuing
```

---

## ADR Quick Reference

Reference this table for common constraints. The source of truth is:
- **Concise ADRs**: `.claude/adr/` (AI-optimized, 100-150 lines each)
- **Full ADRs**: `docs/adr/INDEX.md` (complete with history and rationale)

| ADR | Title | Key Constraint | Violation Pattern |
|-----|-------|----------------|-------------------|
| ADR-001 | Minimal API + Workers | No Azure Functions | `[FunctionName]`, `Microsoft.Azure.Functions` |
| ADR-002 | Thin Plugins | No HTTP in plugins; <50ms | `HttpClient` in Plugin class |
| ADR-003 | Authorization Seams | Two seams only: UAC + Storage | Multiple `IAuthorizationXxx` interfaces |
| ADR-004 | Async Job Contract | Uniform job processing | Ad-hoc `Task.Run` for async work |
| ADR-005 | Flat Storage | No folder hierarchies in SPE | `CreateFolder`, nested paths |
| ADR-006 | PCF over Webresources | No new JS webresources | New `.js` in webresources/ |
| ADR-007 | SpeFileStore Facade | No Graph types above facade | `Microsoft.Graph` in API controllers |
| ADR-008 | Endpoint Filters | No global auth middleware | `app.UseAuthorization()` for resources |
| ADR-009 | Redis-First | No hybrid L1+L2 without proof | `IMemoryCache` cross-request |
| ADR-010 | DI Minimalism | ≤15 DI registrations | Interface for single implementation |
| ADR-011 | Dataset PCF | PCF for data grids | Native subgrid with custom actions |
| ADR-012 | Shared Components | Reuse @spaarke/ui-components | Duplicate component implementations |
| ADR-013 | AI Architecture | No hidden/orphaned AI elements | Undocumented AI endpoints/jobs |
| ADR-014 | AI Caching | Define cache reuse policy | Ad-hoc caching per endpoint |
| ADR-015 | AI Data Governance | Minimize/secure AI data flows | Logging prompts/PII, unclear retention |
| ADR-016 | AI Backpressure | Rate limits + bounded concurrency | Unbounded fanout / no throttling |
| ADR-017 | Job Status | Persist job status contract | Fire-and-forget without status |
| ADR-018 | Feature Flags | Kill switches for risky features | No gating for AI/expensive features |
| ADR-019 | API Errors | ProblemDetails standards | Ad-hoc error payloads/status codes |
| ADR-020 | Versioning | Version APIs/jobs/contracts | Breaking changes without version bump |
| ADR-021 | Fluent UI v9 Design | Use Fluent v9; dark mode; tokens | Hard-coded colors, Fluent v8 imports |

---

## Integration with Other Skills

### design-to-project
- Phase 2 (Context) should invoke ADR lookup using the mapping table
- Generated CLAUDE.md should list applicable ADRs

### task-create  
- Task `<constraints>` should include ADR references
- Task `<files>` should include ADRs to read

### code-review
- Should reference this skill for ADR-specific checks
- Violations should cite specific ADR numbers

### adr-check
- This skill prevents violations; adr-check validates afterward
- Both should use the same ADR quick reference

---

## Examples

### Example 1: Creating a new API endpoint

**Task**: "Create a new endpoint to get document metadata"

**adr-aware activates**:
```
Detected: API Endpoint creation
Loading ADRs: ADR-001, ADR-008, ADR-010

Key constraints:
- ADR-001: Use Minimal API pattern (MapGet/MapPost), not controllers
- ADR-008: Add endpoint filter for authorization, not global middleware
- ADR-010: Inject concrete SpeFileStore, not interface
```

**Generated code includes**:
```csharp
// ADR-001: Minimal API pattern
app.MapGet("/api/documents/{id}/metadata", GetDocumentMetadataAsync)
   .AddEndpointFilter<DocumentAuthorizationFilter>()  // ADR-008
   .WithName("GetDocumentMetadata");
```

### Example 2: Creating a PCF control

**Task**: "Create a document viewer PCF control"

**adr-aware activates**:
```
Detected: PCF Control creation
Loading ADRs: ADR-006, ADR-011, ADR-012, ADR-021

Key constraints:
- ADR-006: Use PCF, not webresource (already doing this ✅)
- ADR-011: Use Dataset PCF for list views
- ADR-012: Import from @spaarke/ui-components for shared components
- ADR-021: Use Fluent v9, semantic tokens, dark mode support
```

**Generated code includes**:
```typescript
// ADR-012: Use shared component library
import { DocumentCard, StatusBadge } from "@spaarke/ui-components";
// ADR-021: Fluent v9 components and tokens
import { Button, tokens, makeStyles } from "@fluentui/react-components";
import { DocumentAdd20Regular } from "@fluentui/react-icons";

const useStyles = makeStyles({
  container: {
    backgroundColor: tokens.colorNeutralBackground1, // ADR-021: semantic tokens
    color: tokens.colorNeutralForeground1,
  },
});
```

### Example 3: Prevented violation

**Task**: "Add caching to the document service"

**adr-aware detects**:
```
About to use IMemoryCache for cross-request caching...

🔔 **ADR Conflict Detected**

**ADR**: ADR-009 - Redis-first caching
**Constraint**: No hybrid L1+L2 cache; use IDistributedCache for cross-request
**Intended Code**: `_memoryCache.Set(key, value, TimeSpan.FromMinutes(5))`
**Compliant Alternative**: `await _distributedCache.SetStringAsync(key, json, options)`

Proceed with compliant alternative? (y/n)
```

---

## Validation

Run `/adr-check` after completing tasks to verify no violations were introduced.

---

*Last updated: December 25, 2025*
