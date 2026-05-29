---
name: ln-630-test-auditor
description: Test suite audit coordinator (L2). Delegates to 5 workers (Business Logic, E2E, Value, Coverage, Isolation). Aggregates results, creates Linear task in Epic 0.
allowed-tools: Read, Grep, Glob, Bash, mcp__Ref, mcp__context7, mcp__linear-server, Skill
---

# Test Suite Auditor (L2 Coordinator)

Coordinates comprehensive test suite audit across 6 quality categories using 5 specialized workers.

## Purpose & Scope

- **L2 Coordinator** that delegates to L3 specialized audit workers
- Audits all tests against 6 quality categories (via 5 workers)
- Calculates **Usefulness Score** for each test (Keep/Remove/Refactor)
- Identifies missing tests for critical business logic
- Detects anti-patterns and isolation issues
- Aggregates results into unified report
- Creates single Linear task in Epic 0
- Manual invocation by user; not part of Story pipeline

## Core Philosophy

> "Write tests. Not too many. Mostly integration." — Kent Beck
> "Test based on risk, not coverage." — ISO 29119

**Key Principles:**
1. **Test business logic, not frameworks** — bcrypt/Prisma/Express already tested
2. **No performance/load/stress tests** — Tests infrastructure, not code correctness (use k6/JMeter separately)
3. **Risk-based prioritization** — Priority ≥15 or remove
4. **E2E for critical paths only** — Money/Security/Data (Priority ≥20)
5. **Usefulness over quantity** — One useful test > 10 useless tests
6. **Every test must justify existence** — Impact × Probability ≥15

## Workflow

### Phase 1: Discovery (Automated)

**Inputs:** Codebase root directory

**Actions:**
1. Find all test files using Glob:
   - `**/*.test.*` (Jest, Vitest)
   - `**/*.spec.*` (Mocha, Jasmine)
   - `**/__tests__/**/*` (Jest convention)
2. Parse test file structure (test names, assertions count)
3. Auto-discover Team ID from [docs/tasks/kanban_board.md](../docs/tasks/kanban_board.md)

**Output:** `testFilesMetadata` — list of test files with basic stats

### Phase 2: Research Best Practices (ONCE)

**Goal:** Gather testing best practices context ONCE, share with all workers

**Actions:**
1. Use MCP Ref/Context7 to research testing best practices for detected tech stack
2. Load [../shared/references/risk_based_testing_guide.md](../shared/references/risk_based_testing_guide.md)
3. Build `contextStore` with:
   - Testing philosophy (E2E primary, Unit supplementary)
   - Usefulness Score formulas (Impact × Probability)
   - Anti-patterns catalog
   - Framework detection patterns

**Output:** `contextStore` — shared context for all workers

**Key Benefit:** Context gathered ONCE → passed to all workers → token-efficient

### Phase 3: Domain Discovery (NEW)

**Purpose:** Detect project domains from production code folder structure for domain-aware coverage analysis.

**Algorithm:** (same as ln-360-codebase-auditor)

1. **Priority 1: Explicit domain folders**
   - Check for: `src/domains/*/`, `src/features/*/`, `src/modules/*/`
   - Monorepo patterns: `packages/*/`, `libs/*/`, `apps/*/`
   - If found (>1 match) → use as domains

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
    {"name": "users", "path": "src/users", "file_count": 45},
    {"name": "orders", "path": "src/orders", "file_count": 32},
    {"name": "shared", "path": "src/shared", "file_count": 15, "is_shared": true}
  ]
}
```

**Shared folder handling:**
- Folders named `shared`, `common`, `utils`, `lib`, `core` → mark `is_shared: true`
- Shared code audited but grouped separately in report

### Phase 4: Delegate to Workers

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

**Prompt template:**
```
Task(description: "Test audit via ln-63X",
     prompt: "Execute ln-63X-{worker}. Read skill from ln-63X-{worker}/SKILL.md. Context: {contextStore}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

#### Phase 4a: Global Workers (PARALLEL)

**Global workers** scan entire test suite (not domain-aware):

| # | Worker | Category | What It Audits |
|---|--------|----------|----------------|
| 1 | [ln-631-test-business-logic-auditor](../ln-631-test-business-logic-auditor/) | Business Logic Focus | Framework/Library tests (Prisma, Express, bcrypt, JWT, axios, React hooks) → REMOVE |
| 2 | [ln-632-test-e2e-priority-auditor](../ln-632-test-e2e-priority-auditor/) | E2E Priority | E2E baseline (2/endpoint), Pyramid validation, Missing E2E tests |
| 3 | [ln-633-test-value-auditor](../ln-633-test-value-auditor/) | Risk-Based Value | Usefulness Score = Impact × Probability<br>Decisions: ≥15 KEEP, 10-14 REVIEW, <10 REMOVE |
| 5 | [ln-635-test-isolation-auditor](../ln-635-test-isolation-auditor/) | Isolation + Anti-Patterns | Isolation (6 categories), Determinism, Anti-Patterns (6 types) |

**Invocation (4 workers in PARALLEL):**
```javascript
FOR EACH worker IN [ln-631, ln-632, ln-633, ln-635]:
  Task(description: "Test audit via " + worker,
       prompt: "Execute " + worker + ". Read skill. Context: " + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

#### Phase 4b: Domain-Aware Worker (PARALLEL per domain)

**Domain-aware worker** runs once per domain:

| # | Worker | Category | What It Audits |
|---|--------|----------|----------------|
| 4 | [ln-634-test-coverage-auditor](../ln-634-test-coverage-auditor/) | Coverage Gaps | Missing tests for critical paths per domain (Money 20+, Security 20+, Data 15+, Core Flows 15+) |

**Invocation:**
```javascript
IF domain_mode == "domain-aware":
  FOR EACH domain IN all_domains:
    domain_context = {
      ...contextStore,
      domain_mode: "domain-aware",
      current_domain: { name: domain.name, path: domain.path }
    }
    Skill(skill="ln-634-test-coverage-auditor", args=JSON.stringify(domain_context))
ELSE:
  // Fallback: invoke once for entire codebase (global mode)
  Skill(skill="ln-634-test-coverage-auditor", args=JSON.stringify(contextStore))
```

**Parallelism strategy:**
- Phase 4a: All 4 global workers run in PARALLEL
- Phase 4b: All N domain-aware invocations run in PARALLEL
- Example: 3 domains → 3 ln-374 invocations in single message

**Worker Output Contract (Unified):**

All workers MUST return JSON with this structure:
```json
{
  "category": "Category Name",
  "score": 7,
  "total_issues": 12,
  "critical": 0,
  "high": 3,
  "medium": 7,
  "low": 2,
  "findings": [
    {
      "severity": "HIGH",
      "location": "path/file.ts:123",
      "issue": "Description of the issue",
      "principle": "Category / Sub-principle",
      "recommendation": "How to fix",
      "effort": "S"
    }
  ]
}
```

**Unified Scoring Formula (all workers):**
```
penalty = (critical × 2.0) + (high × 1.0) + (medium × 0.5) + (low × 0.2)
score = max(0, 10 - penalty)
```

**Domain-aware workers** add optional fields: `domain`, `scan_path`

### Phase 5: Aggregate Results

**Goal:** Merge all worker results into unified Test Suite Audit Report

**Aggregation Algorithm:**
```
1. Collect JSON from all 5 workers
2. Merge findings from all workers into single array
3. Sum severity counts:
   total_critical = sum(worker.critical for all workers)
   total_high = sum(worker.high for all workers)
   total_medium = sum(worker.medium for all workers)
   total_low = sum(worker.low for all workers)
4. Calculate Overall Score:
   overall_score = average(worker.score for all workers)
5. Sort findings by severity: CRITICAL → HIGH → MEDIUM → LOW
6. Group findings by category for report sections
```

**Actions:**
1. **Collect results** from all workers (global + domain-aware)
2. **Merge findings** into single flat array (all workers use unified format)
3. **Sum severity counts** across all workers
4. **Calculate overall score** = average of 5 worker scores
5. **Domain-aware worker (ln-634)** → group by domain.name if domain_mode="domain-aware"
6. **Generate Executive Summary** (2-3 sentences)
7. **Create Linear task** in Epic 0 with full report (see Output Format below)
8. **Return summary** to user

**Findings grouping:**
- Categories 1-3, 5-6 (Business Logic, E2E, Value, Isolation, Anti-Patterns) → single tables (global)
- Category 4 (Coverage Gaps) → subtables per domain (if domain_mode="domain-aware")

## Output Format

```markdown
## Test Suite Audit Report - [DATE]

### Executive Summary
[2-3 sentences: test suite health, major issues, key recommendations]

### Severity Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| **Total** | **X** |

### Compliance Score

| Category | Score | Notes |
|----------|-------|-------|
| Business Logic Focus | X/10 | X framework tests found |
| E2E Critical Coverage | X/10 | X critical paths missing E2E |
| Risk-Based Value | X/10 | X low-value tests |
| Coverage Gaps | X/10 | X critical paths untested |
| Isolation & Anti-Patterns | X/10 | X isolation + anti-pattern issues |
| **Overall** | **X/10** | Average of 5 categories |

### Domain Coverage Summary (NEW - if domain_mode="domain-aware")

| Domain | Critical Paths | Tested | Coverage % | Gaps |
|--------|---------------|--------|------------|------|
| users | 8 | 6 | 75% | 2 |
| orders | 12 | 8 | 67% | 4 |
| payments | 6 | 5 | 83% | 1 |
| **Total** | **26** | **19** | **73%** | **7** |

### Audit Findings

| Severity | Location | Issue | Principle | Recommendation | Effort |
|----------|----------|-------|-----------|----------------|--------|
| **CRITICAL** | routes/payment.ts:45 | Missing E2E for payment processing (Priority 25) | E2E Critical Coverage / Money Flow | Add E2E: successful payment + discount edge cases | M |
| **HIGH** | auth.test.ts:45-52 | Test 'bcrypt hashes password' validates library behavior | Business Logic Focus / Crypto Testing | Delete — bcrypt already tested by maintainers | S |
| **HIGH** | db.test.ts:78-85 | Test 'Prisma findMany returns array' validates ORM | Business Logic Focus / ORM Testing | Delete — Prisma already tested | S |
| **HIGH** | user.test.ts:45 | Anti-pattern 'The Liar' — no assertions | Anti-Patterns / The Liar | Add specific assertions or delete test | S |
| **MEDIUM** | utils.test.ts:23-27 | Test 'validateEmail' has Usefulness Score 4 | Risk-Based Value / Low Priority | Delete — likely covered by E2E registration | S |
| **MEDIUM** | order.test.ts:200-350 | Anti-pattern 'The Giant' — 150 lines | Anti-Patterns / The Giant | Split into focused tests | M |
| **LOW** | payment.test.ts | Anti-pattern 'Happy Path Only' — no error tests | Anti-Patterns / Happy Path | Add negative tests | M |

### Coverage Gaps by Domain (if domain_mode="domain-aware")

#### Domain: users (src/users/)

| Severity | Category | Missing Test | Location | Priority | Effort |
|----------|----------|--------------|----------|----------|--------|
| CRITICAL | Money | E2E: processRefund() | services/user.ts:120 | 20 | M |
| HIGH | Security | Unit: validatePermissions() | middleware/auth.ts:45 | 18 | S |

#### Domain: orders (src/orders/)

| Severity | Category | Missing Test | Location | Priority | Effort |
|----------|----------|--------------|----------|----------|--------|
| CRITICAL | Money | E2E: applyDiscount() | services/order.ts:45 | 25 | M |
| HIGH | Data | Integration: orderTransaction() | repositories/order.ts:78 | 16 | M |
```

## Worker Architecture

Each worker:
- Receives `contextStore` with testing best practices
- Receives `testFilesMetadata` with test file list
- Loads full test file contents when analyzing
- Returns structured JSON with category findings
- Operates independently (failure in one doesn't block others)

**Token Efficiency:**
- Coordinator: metadata only (~1000 tokens)
- Workers: full test file contents when needed (~5000-10000 tokens each)
- Context gathered ONCE, shared with all workers

## Critical Rules

- **Two-stage delegation:** Global workers (4) + Domain-aware worker (ln-374 × N domains)
- **Domain discovery:** Auto-detect domains from folder structure; fallback to global mode if <2 domains
- **Parallel execution:** All workers (global + domain-aware) run in PARALLEL
- **Domain-grouped output:** Coverage Gaps findings grouped by domain (if domain_mode="domain-aware")
- **Delete > Archive:** Remove useless tests, don't comment out
- **E2E baseline:** Every endpoint needs 2 E2E (positive + negative)
- **Justify each test:** If can't explain Priority ≥15, remove it
- **Trust frameworks:** Don't test Express/Prisma/bcrypt behavior
- **No performance/load tests:** Flag and REMOVE tests measuring throughput/latency/memory (DevOps Epic territory)
- **Code is truth:** If test contradicts code behavior, update test
- **Language preservation:** Report in project's language (EN/RU)

## Definition of Done

- All test files discovered via Glob
- Context gathered from testing best practices (MCP Ref/Context7)
- Domain discovery completed (domain_mode determined)
- contextStore built with test metadata + domain info
- Global workers (4) invoked in PARALLEL
- Domain-aware worker (ln-374) invoked per domain in PARALLEL
- All workers completed successfully (or reported errors)
- Results aggregated with domain grouping (if domain_mode="domain-aware")
- Domain Coverage Summary built (if domain_mode="domain-aware")
- Compliance scores calculated (6 categories)
- Keep/Remove/Refactor decisions for each test
- Missing tests identified with Priority (grouped by domain if applicable)
- Anti-patterns catalogued
- Linear task created in Epic 0 with full report
- Summary returned to user

## Reference Files

- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Risk-based testing methodology:** `shared/references/risk_based_testing_guide.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Related Skills

- **Workers:**
  - [ln-631-test-business-logic-auditor](../ln-631-test-business-logic-auditor/) — Framework tests detection
  - [ln-632-test-e2e-priority-auditor](../ln-632-test-e2e-priority-auditor/) — E2E baseline validation
  - [ln-633-test-value-auditor](../ln-633-test-value-auditor/) — Usefulness Score calculation
  - [ln-634-test-coverage-auditor](../ln-634-test-coverage-auditor/) — Coverage gaps identification
  - [ln-635-test-isolation-auditor](../ln-635-test-isolation-auditor/) — Isolation + Anti-Patterns

- **Reference:**
  - [../shared/references/risk_based_testing_guide.md](../shared/references/risk_based_testing_guide.md) — Risk-Based Testing Guide
  - [../ln-620-codebase-auditor](../ln-620-codebase-auditor/) — Codebase audit coordinator (similar pattern)

---
**Version:** 4.0.0
**Last Updated:** 2025-12-23
