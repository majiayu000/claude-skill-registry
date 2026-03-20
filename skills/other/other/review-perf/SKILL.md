---
name: review-perf
description: Performance review. Detects project type and dispatches compute and/or web performance reviewers. Advisory only — no changes made.
model: opus
---

# Performance Review

Advisory-only performance review. Detects whether the project contains web content, non-web source code, or both, and dispatches the appropriate performance reviewer(s). No changes are made.

## Philosophy

**Measure, don't guess.** Performance intuitions are unreliable. The reviewers identify structural issues and recommend what to measure, not just what to optimize.

**Two domains, one workflow.** Compute performance (algorithms, memory, CPU) and web performance (network latency, caching, asset delivery) are fundamentally different disciplines. This skill dispatches the right specialist(s) for the project rather than applying one lens to everything.

**Diagnostic, not therapeutic.** This skill identifies performance problems and recommends fixes. It does not implement them. Ask for changes directly after reviewing the findings, or use `/implement` with the review as context.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                 PERFORMANCE REVIEW                   │
├──────────────────────────────────────────────────────┤
│  1. Detect project type (web, non-web, or both)      │
│  2. Determine scope                                  │
│  3. Dispatch performance reviewer(s)                 │
│  4. Present consolidated report                      │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Detect Project Type

Scan the project for source files to determine what performance domains apply.

**Web indicators** (any of these → dispatch web reviewer):

| Indicator                                                               | Signal   |
|-------------------------------------------------------------------------|----------|
| `.html`, `.htm`, `.jsx`, `.tsx`, `.vue`, `.svelte`                      | Strong   |
| `package.json` with web framework (react, vue, next, nuxt, astro, etc.) | Strong   |
| `webpack.config.*`, `vite.config.*`, `next.config.*`                    | Strong   |
| `.css`, `.scss`, `.less` files (more than a few)                        | Moderate |
| `_headers`, `_redirects`, `vercel.json`, `netlify.toml`                 | Moderate |
| Service worker files (`sw.js`, `service-worker.js`)                     | Strong   |

**Non-web indicators** (any of these → dispatch compute reviewer):

| Indicator                                                                | Signal   |
|--------------------------------------------------------------------------|----------|
| `.go`, `.rs`, `.c`, `.cpp`, `.java`, `.py`, `.rb`, `.zig` source files   | Strong   |
| Existing benchmarks (`*_bench*`, `Benchmark` in test files, `criterion`) | Strong   |
| Database query code (SQL files, ORM usage)                               | Moderate |
| Data processing pipelines (ETL, batch processing)                        | Moderate |
| CLI tool entry points                                                    | Moderate |

**Full-stack projects** will have both indicators — dispatch both reviewers.

**If neither is detected:** Report "No performance-relevant source code detected in this project." and abort.

### 2. Determine Scope

Present detected project type and ask the user:

```
Detected project characteristics:
  - Web content: [Yes — N files / No]
  - Source code: [Yes — N files in Go, Python, etc. / No]

Performance domains to review:
  - [x] Web performance (caching, assets, loading strategy)
  - [x] Compute performance (algorithms, memory, benchmarks)

What should I review?
  - Both domains (default)
  - Web performance only
  - Compute performance only
  - Specific directory/scope
```

Accept the user's selection. Default: all applicable domains, entire project.

### 3. Dispatch Performance Reviewers

Spawn the applicable reviewer(s) **in parallel**.

**Web performance reviewer** (if web content detected and not excluded):

Spawn a `SWE - Web Performance Reviewer` agent:

```
Review this project for web performance issues.
Scope: [scope]

Read all relevant files (HTML, CSS, JS, build configs, server configs)
and perform your full audit:
1. Detect tooling and environment (build tools, monitoring, server config)
2. Audit across all categories: caching, asset delivery, critical path,
   resource loading, images, JavaScript cost, CSS efficiency, network
   overhead, Core Web Vitals risk factors
3. Classify every issue by severity (CRITICAL / HIGH / LOW)

Produce your standard output format with summary, issues by severity,
caching assessment, asset delivery assessment, and tooling recommendations.
```

**Compute performance reviewer** (if non-web source detected and not excluded):

Spawn a `SWE - Performance Reviewer` agent:

```
Review this project for computational performance issues.
Scope: [scope]

Read all source files within scope and perform your full review:
1. Scan for performance-critical code, existing benchmarks, and profiling
   infrastructure
2. Assess benchmark coverage and quality
3. Identify optimization opportunities (algorithmic, memory, I/O,
   concurrency)
4. Check for performance regressions and missing regression detection

Produce your standard output format with findings organized by priority.
```

### 4. Present Consolidated Report

Collect all agent responses. Present a consolidated report:

```
## Performance Review

Scope: [what was reviewed]
Domains reviewed: [Web / Compute / Both]

### Web Performance
[web reviewer findings — or "Not applicable" if no web content]

Issues: N (X critical, Y high, Z low)

[merged findings by severity]

---

### Compute Performance
[compute reviewer findings — or "Not applicable" if no non-web source]

Issues: N (X critical, Y high, Z low)

[merged findings by severity]

---

### Cross-Cutting Concerns
[Your synthesis — issues that span both domains. For example:
- Server-side rendering that is both a compute bottleneck and a web loading issue
- API response times that are both an algorithmic problem and a network latency problem
- Database queries that affect both backend throughput and frontend time-to-interactive
If no cross-cutting concerns, omit this section.]

### Suggested Next Steps
[Based on findings:
- If critical/high issues found: recommend fixing them, noting which
  domain each belongs to
- If no significant issues: "No significant performance issues found"
- If missing tooling: recommend specific tools (Lighthouse, benchmarking
  frameworks, profiling tools)]
```

**The cross-cutting section is your synthesis.** Don't just concatenate the two reviewer outputs — look for issues that span both domains.

## Agent Coordination

- Both reviewer agents run **in parallel** (they are read-only and independent)
- Wait for all agents to complete before presenting the consolidated report
- If an agent fails or times out, note the failure in the report and continue with other results

## Abort Conditions

**Abort:**
- Not a git repository
- No source files detected in scope

**Do NOT abort:**
- Only one domain applies (run the applicable reviewer)
- Missing performance tooling (reviewers will note this in their findings)
- A single agent fails in a dual-agent dispatch (report failure, continue)
- Few issues found (report "no significant issues" — that's a valid outcome)
