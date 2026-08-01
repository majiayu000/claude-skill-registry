---
name: ontoly-software-graph
description: Use Ontoly's deterministic Software Graph and MCP capabilities for repository architecture, request tracing, dependency analysis, configuration lookup, and impact analysis before falling back to source search.
---

# Ontoly Software Graph

Use this skill when a coding agent needs graph-backed understanding of a TypeScript repository. Ontoly is the source of truth; the skill only teaches the workflow.

## When to Use

- Explain repository architecture or package/module topology
- Trace a route, controller, service, function, or dependency path
- Find services, controllers, providers, modules, routes, configuration, or environment variables
- Estimate impact before refactoring or deleting code
- Audit unresolved imports, circular dependencies, dead code, semantic coverage, or graph quality
- Produce onboarding, documentation, or architecture-review notes with deterministic evidence

## Workflow

1. Check whether an Ontoly graph already exists: `.ontoly/`, `SoftwareGraph.json`, `diagnostics.json`, validation reports, graph hash, or MCP setup.
2. If the graph is missing and local analysis is allowed, run:

   ```bash
   ontoly build .
   ```

3. Inspect graph health before answering: diagnostics, graph hash, semantic coverage, trust or quality score, framework detection, and build timestamp.
4. Prefer Ontoly CLI or MCP capabilities over repository search for graph-answerable questions.
5. Search source files only when Ontoly cannot answer, the graph is stale or incomplete, or the user explicitly asks for file-level verification.
6. Always cite graph evidence: node IDs, edge types, file paths, source locations, diagnostics, framework analyzer output, and confidence.

## Capability Map

- Architecture review: `ExplainArchitecture`
- Dependency analysis: `FindDependencies`
- Impact analysis: `ImpactAnalysis`
- Request tracing: `TraceExecution`
- Configuration analysis: `FindConfigurationUsage`
- Framework analysis: `FrameworkReport`
- Dead-code review: `FindDeadCode`

## Response Pattern

Return the direct answer first, then evidence:

```text
AuthController handles authentication.

Evidence:
- node: class:src/auth/auth.controller.ts:AuthController
- route edges: HANDLES POST /login and POST /logout
- dependency edges: USES AuthService and JwtService

Confidence: high, because the graph has controller, route, and dependency edges with source locations.
```

## Fallbacks

- If the graph is missing, build it first when allowed.
- If validation fails, report the graph issue and verify only the affected area with source search.
- If several nodes match, show candidates with package/module context.
- If nothing matches, return `NOT_FOUND` with the closest graph evidence instead of inventing an answer.

