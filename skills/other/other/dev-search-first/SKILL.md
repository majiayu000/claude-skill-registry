---
version: 1.0.0
name: dev-search-first
description: >
  Research-before-coding workflow. Search for existing tools, packages, and
  patterns before writing custom code. Checks NuGet, npm, MCP servers, GitHub,
  and the existing codebase. Use when starting a new feature, adding a dependency,
  or before creating a new utility.
disable-model-invocation: true
user-invocable: true
argument-hint: "[what you need]"
---

# Search First — Research Before You Code

Search for existing solutions before implementing custom code.

> **Stack:** C#/.NET + Angular/TypeScript

## When to Use

- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- Before creating a new utility, helper, or abstraction
- The user asks "add X functionality" and you're about to write code

## Workflow

```
1. NEED ANALYSIS
   Define what functionality is needed
   Identify framework constraints (.NET / Angular)

2. PARALLEL SEARCH
   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
   │  NuGet / │ │  MCP /   │ │ Existing │ │ GitHub / │
   │  npm     │ │  Skills  │ │ Codebase │ │  Web     │
   └──────────┘ └──────────┘ └──────────┘ └──────────┘

3. EVALUATE
   Score candidates (functionality, maintenance,
   community, docs, license, dependencies)

4. DECIDE
   ┌─────────┐  ┌──────────┐  ┌─────────┐
   │  Adopt  │  │  Extend  │  │  Build  │
   │ as-is   │  │  /Wrap   │  │ Custom  │
   └─────────┘  └──────────┘  └─────────┘

5. IMPLEMENT
   Install package / Configure / Write minimal custom code
```

## Decision Matrix

| Signal | Action |
|--------|--------|
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + write thin wrapper |
| Multiple weak matches | **Compose** — combine small packages |
| Nothing suitable found | **Build** — write custom, informed by research |

## Search Checklist

Before writing anything, mentally run through:

0. **Does this already exist in the repo?** → `rg` through relevant code first
1. **Is this a common problem?** → Search NuGet (C#) or npm (Angular)
2. **Is there an MCP for this?** → Check configured MCP servers
3. **Is there a skill for this?** → Check `.claude/skills/`
4. **Is there an llms.txt?** → Check the library/framework docs site for `/llms.txt`
5. **Is there a GitHub implementation?** → Search for maintained OSS

## Search Shortcuts by Stack

### C#/.NET

| Need | Look for |
|------|----------|
| Validation / Result types | Results (ValidationBuilder, Result\<T\>) |
| Mapping | Mapster with Mapster.Tool (compile-time code generation). Manual mapping preferred for simple cases |
| HTTP client | `IHttpClientFactory` (built-in), Refit, Flurl |
| Serialization | System.Text.Json (built-in) |
| Logging | Serilog, NLog (over raw `ILogger`) |
| Testing | xUnit, NSubstitute, Testcontainers |
| Background jobs | Hangfire, Quartz.NET |
| Caching | HybridCache (`Microsoft.Extensions.Caching.Hybrid`), `IMemoryCache` (built-in), `IDistributedCache` |
| Auth | ASP.NET Core Identity, Duende IdentityServer |
| Rate limiting | `Microsoft.AspNetCore.RateLimiting` (built-in .NET 7+) |
| Feature flags | Microsoft.FeatureManagement |
| Health checks | `Microsoft.Extensions.Diagnostics.HealthChecks` (built-in) |
| OpenAPI | Swashbuckle, NSwag |
| Resilience | Polly, Microsoft.Extensions.Http.Resilience |
| Domain building blocks | ErikLieben.* NuGet packages (event sourcing, strongly typed IDs, specifications, etc.) |
| ID generation | `Guid.CreateVersion7()` (.NET 9+) |

### Angular/TypeScript

| Need | Look for |
|------|----------|
| State management | Signals (built-in, preferred), NgRx only for complex event-driven scenarios |
| Forms | Template-driven forms with FormsModule (preferred), Reactive Forms for complex cases |
| HTTP | HttpClient (built-in), interceptors for auth/retry |
| UI components | Angular Material, PrimeNG |
| Tables | ag-Grid, ngx-datatable |
| Charts | ngx-charts, Chart.js wrappers |
| i18n | @ngx-translate/core, Angular i18n (built-in) |
| Validation | class-validator, zod |
| Date handling | date-fns, Luxon (over Moment.js) |
| Feature flags | @internal/ng-feature-flags (custom internal library) |
| Permissions | @internal/ng-permissions (custom internal library) |
| Testing | Vitest, @testing-library/angular, Playwright |
| Linting | eslint + @angular-eslint |

### Shared / Infrastructure

| Need | Look for |
|------|----------|
| CI/CD | GitHub Actions, Azure DevOps pipelines |
| Containers | Docker multi-stage builds |
| Database | EF Core migrations, Flyway |
| Monitoring | OpenTelemetry, Application Insights |
| Docs site | VitePress (you have `/tool-vitepress`) |

## Examples

### Example 1: "Add retry logic to HTTP calls"
```
Need: Resilient HTTP calls with retry and circuit breaker
Search: NuGet "resilience http"
Found: Microsoft.Extensions.Http.Resilience (built-in .NET 8+)
Action: ADOPT — already in the framework, zero extra deps
Result: AddStandardResilienceHandler() on HttpClient registration
```

### Example 2: "Add a data table with sorting and filtering"
```
Need: Feature-rich data table for Angular
Search: npm "angular data table"
Found: ag-Grid Community (score: 9/10), PrimeNG Table (score: 8/10)
Action: ADOPT — ag-Grid for complex needs, PrimeNG if already using PrimeNG
Result: One package, battle-tested, accessible
```

### Example 3: "Add input validation to API"
```
Need: Request validation in ASP.NET Core
Search: NuGet "validation", check built-in options
Found: Results (in-house), DataAnnotations (built-in)
Action: ADOPT Results for Result-based validation with Railway-Oriented flow
Result: Explicit success/failure flow, TypedResults integration, error accumulation
```

### Example 4: "Persist domain state with full audit trail"
```
Need: Persist domain state with full audit trail
Search: NuGet "event sourcing", check built-in options
Found: EventSourcing (in-house, Azure Storage backend)
Action: ADOPT — already in-house, battle-tested, includes analyzers + testing helpers
Result: Aggregate + event pattern with blob storage, projections for read models
```

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **Ignoring built-ins**: .NET and Angular have rich built-in capabilities — check the framework first
- **Dependency bloat**: Installing a massive package for one small feature
- **Over-wrapping**: Wrapping a library so heavily it loses its benefits
- **Outdated packages**: Preferring a familiar but unmaintained package over the modern equivalent
