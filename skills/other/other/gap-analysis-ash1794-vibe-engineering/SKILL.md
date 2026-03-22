---
name: vibe-gap-analysis
description: Assesses production readiness or audits a codebase against its specs. Supports quick static mode, deep 17-dimension audit, or single-dimension focus.
user-invocable: true
---

# vibe-gap-analysis

Cynical gap analysis comparing specs/architecture to actual implementation. Three modes from fast to exhaustive. Works with any project that has architecture docs and implementation code.

## When to Use This Skill
- Before launching to production
- After a major refactor to verify nothing was lost
- When inheriting a codebase and need to assess completeness
- Periodic production readiness audits
- When stakeholders ask "how done are we?"

## When NOT to Use This Skill
- Greenfield projects with no specs yet (write specs first)
- Simple bug fixes or feature additions
- Frontend-only or design-only reviews

## Usage

```
/vibe-gap-analysis              # Quick static (5 structural dimensions)
/vibe-gap-analysis --deep       # Full 17-dimension audit with parallel agents
/vibe-gap-analysis --dim N      # Single dimension deep-dive (1-17)
/vibe-gap-analysis --dim 1,4,9  # Multiple specific dimensions
```

## Modes

### Quick Static (default)

Fast, single-agent structural audit. No subagents dispatched.

1. Read architecture/design docs in `docs/` or similar
2. Read implementation code in `src/`, `internal/`, `lib/` etc.
3. Compare implementation against architecture doc section by section
4. Cover dimensions 1-5 (structural):
   - **Dim 1**: Spec Compliance — check specs against implementation
   - **Dim 2**: Backend Code Quality — test coverage, error handling, lint issues
   - **Dim 3**: Frontend Completeness — UI components, routes, test coverage
   - **Dim 4**: Deployment & Ops — deploy scripts, CI/CD, Docker, TLS
   - **Dim 5**: Architecture Integrity — design pattern compliance, component boundaries
5. Produce structured gap report: component, expected status, actual status, % complete, action items
6. Save to `docs/plans/gap-analysis-$(date +%Y%m%d).md`
7. Commit with `docs: gap analysis $(date +%Y%m%d)`

### Deep (`--deep`)

Full 17-dimension audit using parallel subagents. Exhaustive production readiness assessment.

**Dispatch parallel agents** (model: sonnet) in 3 rounds:

**Round 1 — Structural (5 agents):**
- Dim 1: Spec Compliance
- Dim 2: Backend Code Quality
- Dim 3: Frontend Completeness
- Dim 4: Deployment & Ops
- Dim 5: Architecture Integrity

**Round 2 — Runtime Execution (7 agents):**
- Dim 6: Database Concurrency & Integrity
- Dim 7: Failure Cascades & Recovery
- Dim 8: E2E Data Flow
- Dim 9: Security & Input Validation
- Dim 10: Observability & Alerting
- Dim 11: Data Durability & Backup
- Dim 12: Cost/Resource Explosion Safeguards

**Round 3 — Business & Product Maturity (5 agents):**
- Dim 13: Performance & Load Testing
- Dim 14: Multi-Tenancy / User Isolation
- Dim 15: Privacy & Compliance (GDPR/CCPA)
- Dim 16: Supply Chain Security
- Dim 17: Operational Readiness

Each agent gets this prompt template:
```
You are auditing [project] for production readiness.

**Your dimension:** [Dimension N — Name]
**Scope:** [Description]
**Previous gap analysis:** [path, if exists]

Instructions:
1. Read all relevant source files for your dimension
2. For each finding: severity (CRITICAL/HIGH/MEDIUM/LOW), location (file:line), issue, fix, effort
3. Score your dimension 0-100
4. Return findings as structured markdown

Be extremely pedantic. Question everything. Assume this is a $100M ARR product.
```

After all rounds:
1. Merge findings, deduplicate across dimensions
2. Build production readiness scorecard (17 dimensions)
3. Build findings-by-system-area cross-reference
4. Build recommended action plan (phased)
5. Save and commit

### Single Dimension (`--dim N`)

Deep-dive into specific dimensions. One agent per requested dimension.

After completion, update only the audited dimensions in the existing gap analysis doc.

## Dimension Reference

| # | Dimension | Type | What to Audit |
|---|-----------|------|---------------|
| 1 | Spec Compliance | Structural | Specs vs implementation |
| 2 | Backend Code Quality | Structural | Tests, errors, lint, races |
| 3 | Frontend Completeness | Structural | UI, routes, stores, tests |
| 4 | Deployment & Ops | Structural | Deploy, CI/CD, Docker, TLS |
| 5 | Architecture Integrity | Structural | Design patterns, boundaries |
| 6 | Database Concurrency | Runtime | Transactions, locks, backups |
| 7 | Failure Cascades | Runtime | Recovery, circuit breakers |
| 8 | E2E Data Flow | Runtime | API contracts, idempotency |
| 9 | Security | Runtime | Input validation, injection, secrets |
| 10 | Observability | Runtime | Logging, alerting, metrics |
| 11 | Data Durability | Runtime | RPO/RTO, backups, replication |
| 12 | Cost/Resource Control | Runtime | Budgets, limits, rate limiting |
| 13 | Performance & Load | Business | Timeouts, benchmarks, limits |
| 14 | Multi-Tenancy | Business | User isolation, data scoping |
| 15 | Privacy & Compliance | Business | GDPR, PII, consent, encryption |
| 16 | Supply Chain | Business | Dep pinning, vuln scanning, builds |
| 17 | Operational Readiness | Business | Runbooks, SLOs, incident response |

## Output Format

All modes produce:
- Executive summary with total findings count
- Audit dimensions table with scores
- CRITICAL findings (full detail)
- HIGH findings (full detail)
- MEDIUM findings (one-line each)
- LOW findings (one-line each)
- Findings by system area (cross-reference)
- Recommended action plan (phased)
- Production readiness scorecard
