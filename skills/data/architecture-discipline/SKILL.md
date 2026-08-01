---
name: architecture-discipline
description: 'Use when designing/modifying system architecture or evaluating technology
  choices. Enforces 7-section TodoWrite with 22+ items. Triggers: "design architecture",
  "system design", "architectural decisio'
---

---
name: architecture-discipline
description: Use when designing/modifying system architecture or evaluating technology choices. Enforces 7-section TodoWrite with 22+ items. Triggers: "design architecture", "system design", "architectural decision", "should we use [tech]", "compare [A] vs [B]", "add new service", "microservices", "database choice", "API design", "scale to [X] users", "infrastructure decision". If thinking ANY of these, USE THIS SKILL: "quick recommendation is fine", "obvious choice", "we already know the answer", "just need to pick one", "simple architecture question".
---

# Architecture Discipline

## When to Use

**Use when decisions affect:**
- Data models or schema changes
- Service boundaries or new services
- Deployment topology or infrastructure
- Scale characteristics (10x growth implications)
- Technology stack choices
- API contracts or external integrations

**Skip for:**
- Parameter tweaks or configuration changes
- UI/styling changes
- Localization or copy changes
- Bug fixes within existing architecture
- Adding fields to existing models (unless schema migration)

**Threshold:** If the decision could cause a 3+ month re-architecture project if wrong, use this skill.

## CRITICAL: This Is Reasoning Discipline, Not a Checklist

The 7 sections are a **reasoning sequence**, not boxes to check:
- Alternatives BEFORE choosing
- Scale requirements BEFORE design
- Failure modes built in, not bolted on

🚨 **If you wrote architecture without starting with all 7 sections:** DELETE and restart. Retrofitting analysis is rationalization, not evaluation.

---

## MANDATORY FIRST STEP

**CREATE TodoWrite** with these 7 sections (22+ items total):

| Section | Minimum Items |
|---------|---------------|
| Scale Analysis | 4+ |
| Architectural Options | 3+ |
| Ripple Effect Analysis | 5+ |
| Failure Modes | 3+ |
| Observability | 3+ |
| Documentation | 2+ |
| Migration/Compatibility | 2+ |

**Do not design, propose solutions, or implement until TodoWrite is verified.**

---

## Verification Checkpoint

After creating TodoWrite, verify 3 random items pass this test:

**Each item must have ALL THREE:**
- ✓ Concrete numbers/thresholds ("100K users", "$500/mo", "P95 < 500ms")
- ✓ Specific tools/technologies ("PostgreSQL", "Redis", "CloudWatch")
- ✓ Measurable outcome ("handles 1M req/sec", "costs $X at 10x")

| ❌ FAILS | ✅ PASSES |
|----------|-----------|
| "Add monitoring" | "CloudWatch: `websocket.connections.active`, alert if >5% error rate via PagerDuty" |
| "Evaluate caching" | "Compare: Redis (1ms, $300/mo) vs In-memory LRU (0.1ms, $0) vs No cache (100ms)" |
| "Analyze scale" | "Current: 100K DAU, 50 req/sec. 10x: 1M users, 500 req/sec. Bottleneck: PostgreSQL connection pool" |

**DO NOT PROCEED until 22+ items AND quality check passes.**

---

## Section Requirements

### 1. Scale Analysis (4+ items)

**NEVER design for current scale only.** Before proposing any solution:
- Current scale: Users (DAU/MAU), requests/sec, data volume, read/write ratio
- 10x scale: What numbers at 10x? When expected?
- Bottlenecks: What breaks at 10x? (DB connections, API limits, memory)
- Mitigation: Specific solution for each bottleneck

### 2. Architectural Options (3+ items)

**NEVER present single solution.** Minimum 3 distinct options, each with:
- Performance: Latency (P50/P95/P99), throughput, scale limit
- Complexity: LOC estimate, services involved, operational burden
- Cost: Infrastructure ($X/mo current, $Y/mo at 10x), development (engineer-weeks)
- Trade-offs: Specific advantages (✅) and disadvantages (❌)

**If stakeholder suggests solution:** Add as Option A, evaluate with SAME rigor as alternatives.

### 3. Ripple Effect Analysis (5+ items)

Changes propagate across layers. Analyze ALL:
- Data layer: Schema changes, migrations, indexes, query performance
- Services: Which need updates? API contracts changed?
- API: Breaking changes? Version bump? Backward compatibility?
- Clients: Mobile updates? Web UI changes?
- Operations: Deployment changes? New monitoring? Cost changes?

### 4. Failure Modes (3+ items)

For each mode:
- Scenario: [Component] fails because [reason]
- Detection: How we know (metrics drop, error rate spike)
- Impact: What breaks (user features, data integrity)
- Mitigation: Circuit breaker, fallback, redundancy

### 5. Observability (3+ items)

- Metrics: Specific (latency P95, error rate %, throughput)
- Alerts: Conditions (error rate > 5%, latency P95 > 500ms)
- Dashboards: Key visualizations

### 6. Documentation (2+ items)

- ADR: Chosen option, rejected alternatives, trade-offs, constraints
- Diagram: New components, data flows, failure paths

### 7. Migration/Compatibility (2+ items)

- Backward compatibility: Old clients work? API versioning?
- Migration path: Phased rollout, feature flags, rollback procedure

---

## Red Flags - STOP When You Think:

| Thought | Reality |
|---------|---------|
| "Analysis paralysis" | This IS the analysis that prevents expensive mistakes |
| "We'll add scale/alternatives/failure modes later" | Retrofitting costs 5-10x more |
| "CTO already decided" | Still needs independent evaluation |
| "Being pragmatic not dogmatic" | These requirements ARE pragmatic |
| "Just a simple feature" | Simple becomes complex at scale |
| "We already know the solution" | Compare 3 alternatives first |
| "Keep it simple" | Simple for current scale = complex re-architecture at 10x |
| "I can add missing sections to existing work" | DELETE and restart |

---

## Override Requirements

To skip ANY requirement, you MUST provide ALL 4:
1. Specific retrofit date (not "later")
2. Budget allocated (engineer-weeks)
3. Risk acceptance signed by decision maker
4. Interim mitigation plan

| Skipped | Risk | Cost |
|---------|------|------|
| Scale Analysis | Re-architecture in 6-12 months | 3-6 month project, 5-10x cost |
| Alternatives | Optimize wrong dimension | 2-4 month migration |
| Failure Modes | Production incidents | $5-50K per incident |
| Ripple Effects | Broken clients, data issues | Deployment failures |

---

## Verification Before Complete

| Category | Requirements |
|----------|-------------|
| Scale | ✓ Current + 10x projected ✓ Bottlenecks ✓ Mitigations |
| Trade-offs | ✓ 3+ options ✓ Performance/complexity/cost ✓ Rationale |
| Impact | ✓ All layers analyzed ✓ Breaking changes identified |
| Failure | ✓ Specific modes ✓ Detection ✓ Mitigation ✓ Rollback |
| Documentation | ✓ ADR ✓ Diagram updated |

**If any item missing, do not proceed to implementation.**
