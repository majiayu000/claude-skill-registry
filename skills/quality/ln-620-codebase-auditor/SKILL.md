---
name: ln-620-codebase-auditor
description: Coordinates 9 specialized audit workers (security, build, architecture, code quality, dependencies, dead code, observability, concurrency, lifecycle). Researches best practices, delegates parallel audits, aggregates results into single Linear task in Epic 0.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, mcp__linear-server, Skill
---

# Codebase Auditor (L2 Coordinator)

Coordinates 9 specialized audit workers to perform comprehensive codebase quality analysis.

## Purpose & Scope

- **Coordinates 9 audit workers** (ln-621 through ln-629) running in parallel
- Research current best practices for detected tech stack via MCP tools ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Create single refactoring task in Linear under Epic 0 with all findings
- Manual invocation by user; not part of Story pipeline

## Workflow

1) **Discovery:** Load tech_stack.md, principles.md, package manifests, auto-discover Team ID
2) **Research:** Query MCP tools for current best practices per major dependency ONCE
3) **Build Context:** Create contextStore with best practices + tech stack metadata
4) **Domain Discovery:** Detect project domains from folder structure (NEW)
5) **Delegate:** Two-stage delegation - global workers + domain-aware workers (UPDATED)
6) **Aggregate:** Collect worker results, group by domain, calculate scores
7) **Generate Report:** Build consolidated report with Domain Health Summary, Findings by Domain
8) **Create Task:** Create Linear task in Epic 0 titled "Codebase Refactoring: [YYYY-MM-DD]"

## Phase 1: Discovery

**Load project metadata:**
- `docs/project/tech_stack.md` - detect tech stack for research
- `docs/principles.md` - project-specific quality principles
- Package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Auto-discover Team ID from `docs/tasks/kanban_board.md`

**Extract metadata only** (not full codebase scan):
- Programming language(s)
- Major frameworks/libraries
- Database system(s)
- Build tools
- Test framework(s)

## Phase 2: Research Best Practices (ONCE)

**For each major dependency identified in Phase 1:**

1. Use `mcp__Ref__ref_search_documentation` for current best practices
2. Use `mcp__context7__get-library-docs` for up-to-date library documentation
3. Focus areas by technology type:

| Type | Research Focus |
|------|----------------|
| Web Framework | Async patterns, middleware, error handling, request lifecycle |
| ML/AI Libraries | Inference optimization, memory management, batching |
| Database | Connection pooling, transactions, query optimization |
| Containerization | Multi-stage builds, security, layer caching |
| Language Runtime | Idioms, performance patterns, memory management |

**Build contextStore:**
```json
{
  "tech_stack": {...},
  "best_practices": {...},
  "principles": {...},
  "codebase_root": "..."
}
```

## Phase 3: Domain Discovery

**Purpose:** Detect project domains from folder structure for domain-aware auditing.

**Algorithm:**

1. **Priority 1: Explicit domain folders**
   - Check for: `src/domains/*/`, `src/features/*/`, `src/modules/*/`
   - Monorepo patterns: `packages/*/`, `libs/*/`, `apps/*/`
   - If found (>1 match) → use these as domains

2. **Priority 2: Top-level src/* folders**
   - List folders: `src/users/`, `src/orders/`, `src/payments/`
   - Exclude infrastructure: `utils`, `shared`, `common`, `lib`, `helpers`, `config`, `types`, `interfaces`, `constants`, `middleware`, `infrastructure`, `core`
   - If remaining >1 → use as domains

3. **Priority 3: Fallback to global mode**
   - If <2 domains detected → `domain_mode = "global"`
   - All workers scan entire codebase (backward-compatible behavior)

**Heuristics for domain detection:**

| Heuristic | Indicator | Example |
|-----------|-----------|---------|
| File count | >5 files in folder | `src/users/` with 12 files |
| Structure | controllers/, services/, models/ present | MVC/Clean Architecture |
| Barrel export | index.ts/index.js exists | Module pattern |
| README | README.md describes domain | Domain documentation |

**Output:**
```json
{
  "domain_mode": "domain-aware",
  "all_domains": [
    {"name": "users", "path": "src/users", "file_count": 45, "is_shared": false},
    {"name": "orders", "path": "src/orders", "file_count": 32, "is_shared": false},
    {"name": "shared", "path": "src/shared", "file_count": 15, "is_shared": true}
  ]
}
```

**Shared folder handling:**
- Folders named `shared`, `common`, `utils`, `lib`, `core` → mark `is_shared: true`
- Shared code audited but grouped separately in report
- Does not affect domain-specific scores

## Phase 4: Delegate to Workers

### Phase 4a: Global Workers (PARALLEL)

**Global workers** scan entire codebase (not domain-aware):

| # | Worker | Priority | What It Audits |
|---|--------|----------|----------------|
| 1 | ln-621-security-auditor | CRITICAL | Hardcoded secrets, SQL injection, XSS, insecure deps |
| 2 | ln-622-build-auditor | CRITICAL | Compiler/linter errors, deprecations, type errors |
| 5 | ln-625-dependencies-auditor | MEDIUM | Outdated packages, unused deps, custom implementations |
| 6 | ln-626-dead-code-auditor | LOW | Dead code, unused imports/variables, commented-out code |
| 7 | ln-627-observability-auditor | MEDIUM | Structured logging, health checks, metrics, tracing |
| 8 | ln-628-concurrency-auditor | HIGH | Race conditions, async/await, resource contention |
| 9 | ln-629-lifecycle-auditor | MEDIUM | Bootstrap, graceful shutdown, resource cleanup |

**Invocation (7 workers in PARALLEL):**
```javascript
FOR EACH worker IN [ln-621, ln-622, ln-625, ln-626, ln-627, ln-628, ln-629]:
  Skill(skill=worker, args=JSON.stringify(contextStore))
```

### Phase 4b: Domain-Aware Workers (PARALLEL per domain)

**Domain-aware workers** run once per domain:

| # | Worker | Priority | What It Audits |
|---|--------|----------|----------------|
| 3 | ln-623-code-principles-auditor | HIGH | DRY/KISS/YAGNI violations, TODO/FIXME, error handling, DI |
| 4 | ln-624-code-quality-auditor | MEDIUM | Cyclomatic complexity, O(n²), N+1 queries, magic numbers |

**Invocation (2 workers × N domains):**
```javascript
IF domain_mode == "domain-aware":
  FOR EACH domain IN all_domains:
    domain_context = {
      ...contextStore,
      domain_mode: "domain-aware",
      current_domain: { name: domain.name, path: domain.path }
    }
    // Invoke both workers for this domain
    Skill(skill="ln-623-code-principles-auditor", args=JSON.stringify(domain_context))
    Skill(skill="ln-624-code-quality-auditor", args=JSON.stringify(domain_context))
ELSE:
  // Fallback: invoke once for entire codebase (global mode)
  Skill(skill="ln-623-code-principles-auditor", args=JSON.stringify(contextStore))
  Skill(skill="ln-624-code-quality-auditor", args=JSON.stringify(contextStore))
```

**Parallelism strategy:**
- Phase 4a: All 7 global workers run in PARALLEL
- Phase 4b: All (2 × N) domain-aware invocations run in PARALLEL
- Example: 3 domains → 6 invocations (ln-363×3 + ln-364×3) in single message

## Phase 5: Aggregate Results

**Collect results from workers:**

**Global worker output (unchanged):**
```json
{
  "category": "Security",
  "score": 7,
  "total_issues": 5,
  "critical": 1,
  "high": 2,
  "medium": 2,
  "low": 0,
  "findings": [...]
}
```

**Domain-aware worker output (NEW):**
```json
{
  "category": "Architecture & Design",
  "score": 6,
  "domain": "users",
  "scan_path": "src/users",
  "total_issues": 4,
  "critical": 1,
  "high": 2,
  "medium": 1,
  "low": 0,
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "src/users/controllers/UserController.ts:45",
      "issue": "Controller directly uses Repository",
      "principle": "Layer Separation (Clean Architecture)",
      "recommendation": "Create UserService",
      "effort": "L",
      "domain": "users"
    }
  ]
}
```

**Aggregation steps:**

1. **Global workers** → merge findings (as before)
2. **Domain-aware workers** → group by domain.name:
   - Calculate domain-level scores (Architecture + Quality per domain)
   - Build Domain Health Summary table
3. **Overall score** → average of all category scores (Architecture/Quality averaged across domains)
4. **Severity summary** → sum critical/high/medium/low across ALL workers
5. **Findings grouping:**
   - Global categories (Security, Build, etc.) → single table
   - Domain-aware categories → subtables per domain

## Output Format

```markdown
## Codebase Audit Report - [DATE]

### Executive Summary
[2-3 sentences on overall codebase health, major risks, and key strengths]

### Compliance Score

| Category | Score | Notes |
|----------|-------|-------|
| Security | X/10 | ... |
| Build Health | X/10 | ... |
| Architecture & Design | X/10 | ... |
| Code Quality | X/10 | ... |
| Dependencies & Reuse | X/10 | ... |
| Dead Code | X/10 | ... |
| Observability | X/10 | ... |
| Concurrency | X/10 | ... |
| Lifecycle | X/10 | ... |
| **Overall** | **X/10** | |

### Severity Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

### Domain Health Summary (NEW - if domain_mode="domain-aware")

| Domain | Files | Arch Score | Quality Score | Issues |
|--------|-------|------------|---------------|--------|
| users | 45 | 7/10 | 8/10 | 5 |
| orders | 32 | 5/10 | 6/10 | 8 |
| payments | 28 | 8/10 | 7/10 | 3 |
| shared | 15 | 6/10 | 9/10 | 2 |
| **Total** | **120** | **6.5/10** | **7.5/10** | **18** |

### Strengths
- [What's done well in this codebase]
- [Good patterns and practices identified]

### Findings by Category

#### 1. Security (Global)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| CRITICAL | src/api/auth.ts:45 | Hardcoded API key | Secrets Management | Move to .env | S |

#### 2. Build Health (Global)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| CRITICAL | Multiple files | TypeScript strict errors | Type Safety | Fix types | S |

#### 3. Architecture & Design (Domain-Grouped)

##### Domain: users (src/users/)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| CRITICAL | UserController.ts:12 | Controller→Repository bypass | Layer Separation | Add Service layer | L |

##### Domain: orders (src/orders/)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| HIGH | OrderService.ts:45 | DRY violation (duplicate validation) | DRY Principle | Extract to validators/ | M |

##### Domain: shared (src/shared/)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| MEDIUM | utils.ts:78 | TODO older than 6 months | Code Hygiene | Complete or remove | S |

#### 4. Code Quality (Domain-Grouped)

##### Domain: users (src/users/)

| Severity | Location | Issue | Principle Violated | Recommendation | Effort |
|----------|----------|-------|-------------------|----------------|--------|
| HIGH | UserService.ts:120 | Complexity 25 | Maintainability | Split function | M |

... (continue for remaining global categories: 5-9)

### Recommended Actions (Priority-Sorted)

| Priority | Category | Domain | Location | Issue | Recommendation | Effort |
|----------|----------|--------|----------|-------|----------------|--------|
| CRITICAL | Security | - | src/api/auth.ts:45 | Hardcoded API key | Move to .env | S |
| CRITICAL | Architecture | users | UserController.ts:12 | Controller→Repository bypass | Add Service layer | L |
| CRITICAL | Build | - | Multiple files | TypeScript strict errors | Fix types | S |
| HIGH | Architecture | orders | OrderService.ts:45 | DRY violation | Extract to validators/ | M |
| HIGH | Code Quality | users | UserService.ts:120 | Complexity 25 | Split function | M |

### Priority Actions
1. Fix all Critical issues before next release
2. Address High issues within current sprint
3. Plan Medium issues for technical debt sprint
4. Track Low issues in backlog

### Sources Consulted
- [Framework] best practices: [URL from MCP Ref]
- [Library] documentation: [URL from Context7]
```

## Phase 6: Create Linear Task

Create task in Epic 0:
- Title: `Codebase Refactoring: [YYYY-MM-DD]`
- Description: Full report from Phase 5 (markdown format)
- Team: Auto-discovered from kanban_board.md
- Epic: 0 (technical debt / refactoring epic)
- Labels: `refactoring`, `technical-debt`, `audit`
- Priority: Based on highest severity findings (Critical → Urgent, High → High, etc.)

## Critical Rules

- **Two-stage delegation:** Global workers (7) + Domain-aware workers (2 × N domains)
- **Domain discovery:** Auto-detect domains from folder structure; fallback to global mode
- **Parallel execution:** All workers (global + domain-aware) run in PARALLEL
- **Single context gathering:** Research best practices ONCE, pass contextStore to all workers
- **Metadata-only loading:** Coordinator loads metadata only; workers load full file contents
- **Domain-grouped output:** Architecture & Code Quality findings grouped by domain
- **Language preservation:** Task description in project's language (EN/RU from kanban_board.md)
- **Single task:** Create ONE task with all findings; do not create multiple tasks
- **Do not audit:** Coordinator orchestrates only; audit logic lives in workers

## Definition of Done

- Best practices researched via MCP tools for major dependencies
- Domain discovery completed (domain_mode determined)
- contextStore built with tech stack + best practices + domain info
- Global workers (7) invoked in PARALLEL
- Domain-aware workers (2 × N domains) invoked in PARALLEL
- All workers completed successfully (or reported errors)
- Results aggregated with domain grouping
- Domain Health Summary built (if domain_mode="domain-aware")
- Compliance score (X/10) calculated per category + overall
- Executive Summary and Strengths sections included
- Linear task created in Epic 0 with full report
- Sources consulted listed with URLs

## Workers

See individual worker SKILL.md files for detailed audit rules:
- [ln-621-security-auditor](../ln-621-security-auditor/SKILL.md)
- [ln-622-build-auditor](../ln-622-build-auditor/SKILL.md)
- [ln-623-code-principles-auditor](../ln-623-code-principles-auditor/SKILL.md)
- [ln-624-code-quality-auditor](../ln-624-code-quality-auditor/SKILL.md)
- [ln-625-dependencies-auditor](../ln-625-dependencies-auditor/SKILL.md)
- [ln-626-dead-code-auditor](../ln-626-dead-code-auditor/SKILL.md)
- [ln-627-observability-auditor](../ln-627-observability-auditor/SKILL.md)
- [ln-628-concurrency-auditor](../ln-628-concurrency-auditor/SKILL.md)
- [ln-629-lifecycle-auditor](../ln-629-lifecycle-auditor/SKILL.md)

## Reference Files

- Principles: `docs/principles.md`
- Tech stack: `docs/project/tech_stack.md`
- Kanban board: `docs/tasks/kanban_board.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-12-23
