---
name: parties
description: Reference for parallel agent deployment protocols (search-party, qa-party, plan-party)
---

# Party Protocols

> **Purpose:** Display the PAI party protocol structures
> **Trigger:** `/parties`
> **Updated:** 2026-01-03

---

## Party Overview

| Party | Staff | Probes/Agents | Purpose | Invocation |
|-------|-------|---------------|---------|------------|
| **SEARCH_PARTY** | G-2 (Intel) | 120 probes | Reconnaissance | `/search-party` |
| **QA_PARTY** | IG (Inspector General) | 120 agents | Validation | `/qa-party` |
| **PLAN_PARTY** | G-5 (Strategic) | 10 probes | Planning | `/plan-party` |

---

## SEARCH_PARTY (G-2 Reconnaissance)

```
G2_RECON (Commander)
    │
    ├─ G2-BACKEND-CORE ────┬─ PERCEPTION ─── Surface state, logs, errors
    │  (backend/app/api/)  ├─ INVESTIGATION  Dependencies, call chains
    │                      ├─ ARCANA ─────── ACGME rules, security
    │                      ├─ HISTORY ────── Git log, recent changes
    │                      ├─ INSIGHT ────── Design decisions, intent
    │                      ├─ RELIGION ───── CLAUDE.md compliance
    │                      ├─ NATURE ─────── Over-engineering detection
    │                      ├─ MEDICINE ───── System diagnostics, leaks
    │                      ├─ SURVIVAL ───── Edge cases, failure modes
    │                      └─ STEALTH ────── Hidden coupling, blind spots
    │
    ├─ G2-BACKEND-MODELS ──┬─ (10 probes)
    │  (backend/app/models/)
    │
    ├─ G2-SCHEDULING ──────┬─ (10 probes)
    │  (backend/app/scheduling/)
    │
    ├─ G2-RESILIENCE ──────┬─ (10 probes)
    │  (backend/app/resilience/)
    │
    ├─ G2-FRONTEND-CORE ───┬─ (10 probes)
    │  (frontend/src/components/)
    │
    ├─ G2-FRONTEND-HOOKS ──┬─ (10 probes)
    │  (frontend/src/hooks/)
    │
    ├─ G2-TESTS-BACKEND ───┬─ (10 probes)
    │  (backend/tests/)
    │
    ├─ G2-TESTS-FRONTEND ──┬─ (10 probes)
    │  (frontend/__tests__/)
    │
    ├─ G2-MCP ─────────────┬─ (10 probes)
    │  (mcp-server/)
    │
    ├─ G2-DOCS ────────────┬─ (10 probes)
    │  (docs/, .claude/)
    │
    ├─ G2-INFRASTRUCTURE ──┬─ (10 probes)
    │  (docker, .github/, scripts/)
    │
    └─ G2-SECURITY ────────┬─ (10 probes)
       (backend/app/core/)
```

**Total: 12 G-2 teams × 10 probes = 120 probes**

### D&D Probe Lenses

| Probe | Lens | What It Finds |
|-------|------|---------------|
| **PERCEPTION** | Surface state | Logs, errors, health checks |
| **INVESTIGATION** | Connections | Dependencies, imports, call chains |
| **ARCANA** | Domain knowledge | ACGME rules, resilience patterns |
| **HISTORY** | What changed | Git log, recent PRs, migrations |
| **INSIGHT** | Intent/design | Why built this way, tech debt |
| **RELIGION** | Sacred law | CLAUDE.md compliance, heresies |
| **NATURE** | Organic growth | Over-engineering, forced patterns |
| **MEDICINE** | Diagnostics | Unhealthy components, leaks |
| **SURVIVAL** | Edge resilience | Brittleness, failure modes |
| **STEALTH** | Hidden elements | Hidden coupling, blind spots |

---

## QA_PARTY (IG Validation)

```
COORD_QUALITY (Commander)
    │
    ├─ QA-UNIT-TESTS ──────┬─ pytest backend/tests/unit/
    │                      ├─ Coverage analysis
    │                      ├─ Mock validation
    │                      └─ Edge case detection
    │
    ├─ QA-INTEGRATION ─────┬─ pytest backend/tests/integration/
    │                      ├─ API endpoint validation
    │                      ├─ Database transaction tests
    │                      └─ Service interaction tests
    │
    ├─ QA-FRONTEND ────────┬─ npm test (Jest)
    │                      ├─ Component rendering
    │                      ├─ Hook behavior
    │                      └─ State management
    │
    ├─ QA-E2E ─────────────┬─ Playwright tests
    │                      ├─ Critical user journeys
    │                      ├─ Cross-browser validation
    │                      └─ Accessibility checks
    │
    ├─ QA-LINT-BACKEND ────┬─ ruff check
    │                      ├─ ruff format --check
    │                      └─ mypy type checking
    │
    ├─ QA-LINT-FRONTEND ───┬─ npm run lint
    │                      ├─ npm run type-check
    │                      └─ Prettier validation
    │
    ├─ QA-BUILD ───────────┬─ npm run build
    │                      ├─ Docker build validation
    │                      └─ Asset optimization
    │
    ├─ QA-SECURITY ────────┬─ Dependency audit
    │                      ├─ Secret scanning
    │                      ├─ SAST analysis
    │                      └─ OWASP checks
    │
    ├─ QA-ACGME ───────────┬─ Compliance validation
    │                      ├─ 80-hour rule tests
    │                      ├─ 1-in-7 rule tests
    │                      └─ Supervision ratio tests
    │
    ├─ QA-MIGRATIONS ──────┬─ alembic upgrade/downgrade
    │                      ├─ Schema validation
    │                      └─ Data integrity checks
    │
    ├─ QA-API-CONTRACT ────┬─ OpenAPI validation
    │                      ├─ Schema drift detection
    │                      └─ Breaking change detection
    │
    └─ QA-PERFORMANCE ─────┬─ Load test baselines
                           ├─ Memory profiling
                           └─ Query optimization
```

**Total: 12 QA teams × 10 validators = 120 agents**

---

## PLAN_PARTY (G-5 Strategic)

```
G5_PLANNING (Commander)
    │
    ├─ PROBE-ARCHITECTURE ─── System design implications
    │
    ├─ PROBE-DEPENDENCIES ─── Library/service dependencies
    │
    ├─ PROBE-MIGRATION ────── Database schema changes
    │
    ├─ PROBE-TESTING ──────── Test strategy requirements
    │
    ├─ PROBE-SECURITY ─────── Security considerations
    │
    ├─ PROBE-PERFORMANCE ──── Performance implications
    │
    ├─ PROBE-ACGME ────────── Compliance impact
    │
    ├─ PROBE-FRONTEND ─────── UI/UX requirements
    │
    ├─ PROBE-RESILIENCE ───── Failure mode analysis
    │
    └─ PROBE-ROLLBACK ─────── Reversion strategy
```

**Total: 10 planning probes**

### Plan Output Structure

Each probe contributes to:
1. **Implementation Steps** - Ordered task breakdown
2. **Critical Files** - Files requiring modification
3. **Risk Assessment** - Potential issues and mitigations
4. **Dependencies** - Prerequisites and blockers
5. **Validation Criteria** - How to verify success

---

## Economics: Zero Marginal Wall-Clock Cost

```
Sequential (BAD):        Parallel (GOOD):
120 probes × 30s each    120 probes × 30s in parallel
Total: 3600s (1 hour)    Total: 30s (120x faster)
```

**All probes run in parallel. No cost savings from running fewer.**

---

## IDE Crash Prevention

**CRITICAL: Never spawn 8+ agents directly from ORCHESTRATOR**

```
CORRECT:                           WRONG:
ORCHESTRATOR → 1 Commander         ORCHESTRATOR → 12 G-2s directly
                ↓                                  ↓
         Commander manages N               IDE CRASH
```

Always route through the party Commander (G2_RECON, COORD_QUALITY, G5_PLANNING).

---

## Quick Reference

| Command | Staff | Scale | Use For |
|---------|-------|-------|---------|
| `/search-party` | G-2 | 120 probes | Codebase exploration |
| `/qa-party` | IG | 120 agents | Comprehensive validation |
| `/plan-party` | G-5 | 10 probes | Implementation planning |

---

*Run `/parties` anytime for this reference.*
