---
name: ndepend
description: >
  USE FOR: Static analysis of .NET assemblies including code metrics, dependency graphs,
  architecture validation rules, technical debt estimation, and CQLinq queries for code quality gates.
  DO NOT USE FOR: Runtime profiling (use dotTrace or PerfView), Roslyn-based live code analysis
  (use Roslyn analyzers), or security vulnerability scanning (use Semgrep or Snyk).
license: MIT
metadata:
  displayName: NDepend
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "NDepend Official Website"
    url: "https://www.ndepend.com/"
  - title: "NDepend Documentation"
    url: "https://www.ndepend.com/docs/getting-started-with-ndepend"
  - title: "NDepend Product Features"
    url: "https://www.ndepend.com/features/"
---

# NDepend

## Overview

NDepend is a static analysis tool for .NET that operates on compiled assemblies to compute code metrics, visualize dependencies, enforce architecture rules, and track technical debt. Unlike Roslyn analyzers that run during compilation, NDepend analyzes the final IL and provides a query language called CQLinq (Code Query LINQ) for writing custom rules against the code model. NDepend integrates with Visual Studio, Azure DevOps, GitHub Actions, and other CI systems.

NDepend's analysis covers cyclomatic complexity, coupling, cohesion, code coverage correlation, dependency cycles, and layered architecture validation. Reports can be generated as HTML dashboards or consumed programmatically through the NDepend.API.

## CQLinq Queries

CQLinq uses LINQ syntax to query the NDepend code model. Queries run against types, methods, fields, assemblies, and namespaces.

### Finding Complex Methods

```csharp
// CQLinq: Methods with high cyclomatic complexity
from m in Methods
where m.CyclomaticComplexity > 15
   && !m.IsGeneratedByCompiler
orderby m.CyclomaticComplexity descending
select new {
    m,
    m.CyclomaticComplexity,
    m.NbLinesOfCode,
    m.PercentageCoverage
}
```

### Finding Large Classes

```csharp
// CQLinq: Types with too many methods (God classes)
from t in Types
where t.NbMethods > 30
   && !t.IsGeneratedByCompiler
   && !t.IsEnumeration
orderby t.NbMethods descending
select new {
    t,
    t.NbMethods,
    t.NbFields,
    t.NbLinesOfCode,
    t.TypeRank  // PageRank-style importance metric
}
```

### Detecting Dependency Cycles

```csharp
// CQLinq: Find namespaces involved in dependency cycles
from n in Namespaces
where n.DepthOfIsUsingAny > 0
select new {
    n,
    DependsOn = n.NamespacesUsed,
    UsedBy = n.NamespacesUsingMe,
    CycleDepth = n.DepthOfIsUsingAny
}
```

### Finding Methods That Should Be Static

```csharp
// CQLinq: Instance methods that do not use instance state
from m in Methods
where !m.IsStatic
   && !m.IsVirtual
   && !m.IsConstructor
   && !m.IsAbstract
   && m.NbMethods > 0
   && !m.IsUsing("this")
   && !m.IsGeneratedByCompiler
select new {
    m,
    m.NbLinesOfCode,
    m.ParentType
}
```

## Architecture Rules

NDepend enforces layered architecture constraints through CQLinq rules.

```csharp
// CQLinq Rule: Ensure UI layer does not reference Data layer directly
warnif count > 0
from t in Types
where t.IsUsing("MyApp.Data")
   && t.ParentNamespace.Name.Contains("MyApp.UI")
select new {
    t,
    Violation = "UI types must not reference Data layer directly. Use Service layer."
}
```

```csharp
// CQLinq Rule: Ensure abstractions do not depend on implementations
warnif count > 0
from t in Types
where t.ParentNamespace.Name.Contains("Abstractions")
   && t.DepthOfDeriveFrom("System.Object") >= 0
let dependencies = t.TypesUsed.Where(
    dep => !dep.ParentNamespace.Name.Contains("Abstractions")
        && !dep.ParentNamespace.Name.StartsWith("System"))
where dependencies.Any()
select new {
    t,
    BadDependencies = dependencies,
    Message = "Abstraction types should not depend on concrete implementations"
}
```

## Code Metrics Reference

| Metric                        | Good Range    | Warning       | Critical     | Description                              |
|-------------------------------|---------------|---------------|--------------|------------------------------------------|
| Cyclomatic Complexity         | 1-10          | 11-20         | >20          | Number of independent execution paths    |
| Lines of Code (method)        | 1-20          | 21-40         | >40          | Executable lines in a method             |
| Lines of Code (type)          | 1-200         | 201-500       | >500         | Executable lines in a type               |
| Number of Methods (type)      | 1-20          | 21-40         | >40          | Methods declared in a type               |
| Afferent Coupling (Ca)        | --            | >20           | >50          | Types that depend on this type           |
| Efferent Coupling (Ce)        | --            | >20           | >50          | Types this type depends on               |
| Instability (Ce/(Ca+Ce))      | 0.0-1.0       | Near 0.5      | --           | Resistance to change (0=stable, 1=unstable) |
| Abstractness                  | 0.0-1.0       | --            | --           | Ratio of abstract types to total types   |
| TypeRank                      | --            | --            | --           | PageRank-style importance score          |

## Quality Gates for CI

Define quality gate rules that fail the build when thresholds are exceeded.

```csharp
// CQLinq Quality Gate: No method should exceed complexity 30
failif count > 0
from m in Methods
where m.CyclomaticComplexity > 30
   && !m.IsGeneratedByCompiler
select new {
    m,
    m.CyclomaticComplexity,
    Message = "Method exceeds maximum allowed complexity of 30"
}
```

```csharp
// CQLinq Quality Gate: Code coverage must not drop below 70%
failif value > 30
let coveragePercent = codeBase.PercentageCoverage
where coveragePercent < 70
select 100 - coveragePercent
// Fails if more than 30% of code is uncovered
```

```csharp
// CQLinq Quality Gate: No new technical debt added
failif count > 0
from i in Issues
where i.Severity == Severity.Critical
   && i.WasAdded()
select new {
    i,
    i.Severity,
    i.DebtInMinutes,
    Message = "New critical issues introduced in this build"
}
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ndepend.yml
name: NDepend Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.0.x'
      - name: Build
        run: dotnet build -c Release
      - name: Run NDepend
        run: |
          NDepend.Console.exe MyApp.ndproj /OutDir ./ndepend-report
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: ndepend-report
          path: ./ndepend-report
```

## NDepend Project Configuration

```xml
<!-- MyApp.ndproj -->
<NDepend AppName="MyApp" Platform="DotNet">
  <OutputDir KeepHistoric="True">NDependOut</OutputDir>
  <Assemblies>
    <Name>MyApp.Core</Name>
    <Name>MyApp.Api</Name>
    <Name>MyApp.Services</Name>
  </Assemblies>
  <FrameworkAssemblies />
  <Queries>
    <Group Name="Quality Gates" Active="True">
      <!-- CQLinq rules loaded from .ndproj or external files -->
    </Group>
  </Queries>
</NDepend>
```

## Trending and Baseline

NDepend supports historical analysis by comparing the current build against a baseline.

```csharp
// CQLinq: Methods that became more complex since baseline
from m in Methods
where m.CyclomaticComplexity > m.OlderVersion().CyclomaticComplexity
   && m.CyclomaticComplexity > 10
select new {
    m,
    Current = m.CyclomaticComplexity,
    Previous = m.OlderVersion().CyclomaticComplexity,
    Increase = m.CyclomaticComplexity - m.OlderVersion().CyclomaticComplexity
}
```

```csharp
// CQLinq: New types added since baseline without sufficient test coverage
from t in Types
where t.WasAdded()
   && t.PercentageCoverage < 60
   && t.NbLinesOfCode > 10
   && !t.IsGeneratedByCompiler
select new {
    t,
    t.PercentageCoverage,
    t.NbLinesOfCode,
    Message = "New types should have at least 60% code coverage"
}
```

## Best Practices

1. **Set a baseline snapshot after stabilizing the codebase and use `WasAdded()`, `WasChanged()`, and `OlderVersion()` in CQLinq rules** to enforce that new or modified code meets quality standards without forcing fixes to all legacy code at once.

2. **Define `failif` quality gates for cyclomatic complexity, code coverage, and critical issues** and run them in CI so that builds fail when new code introduces measurable quality regressions.

3. **Create architecture rules using CQLinq `warnif` queries that enforce layer boundaries** (e.g., UI must not reference Data directly) to prevent architecture erosion over time through automated CI enforcement.

4. **Exclude compiler-generated code with `!m.IsGeneratedByCompiler` in all CQLinq queries** to prevent false positives from async state machines, LINQ expression trees, record types, and source-generated code.

5. **Track the Instability metric (Ce/(Ca+Ce)) and Abstractness ratio for each namespace** to identify namespaces in the "zone of pain" (too stable and concrete) or "zone of uselessness" (too abstract and unstable).

6. **Use TypeRank to identify the most important types in the codebase** and prioritize test coverage and code review efforts on high-TypeRank types, as bugs in these types have the widest impact.

7. **Configure NDepend to consume code coverage data from your test runner** (Coverlet, dotnet-coverage, or VS Enterprise) so that coverage metrics are correlated with complexity metrics in quality gate queries.

8. **Review the NDepend dependency graph before refactoring to identify the actual dependency fan-out** rather than guessing which types will be affected; the visual graph reveals transitive dependencies that text-based analysis misses.

9. **Run NDepend analysis on every pull request and publish the HTML report as a CI artifact** so that reviewers can inspect metric changes, new technical debt, and architecture violations before merging.

10. **Keep the NDepend project file (`.ndproj`) in version control alongside the solution** so that rule definitions, quality gates, and analysis configuration are shared and versioned with the codebase.
