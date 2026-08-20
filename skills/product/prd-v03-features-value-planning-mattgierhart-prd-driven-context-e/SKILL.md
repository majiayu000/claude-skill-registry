---
name: prd-v03-features-value-planning
description: Define and prioritize features with strategic traceability during PRD v0.3 Commercial Model. Triggers on requests to define features, prioritize capabilities, scope MVP, map features to pricing tiers, identify parity vs. delta features, or when user asks "what features do we build?", "what's in MVP?", "which features matter?", "feature priority", "parity features", "what's our delta?". Consumes KPI- (Outcome Definition), BR- (Pricing Model, Moat), and CFD- (Market Moat Analysis) from v0.3. Outputs FEA- entries with strategic traceability and BR-FEA- governance rules. Feeds v0.4 User Journeys.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# Feature Value Planning

Position in workflow: v0.3 Commercial Model → **v0.3 Feature Value Planning** → v0.4 User Journeys

Features are the unit of scope. Every feature must trace back to why it exists: outcome, moat, competitive position, or pricing tier.

## Consumes

This skill requires prior work from v0.1-v0.3:

- **CFD-\* entries** (customer feedback, from v0.1-v0.2) — Evidence for what users need/want
- **KPI-\* entries** (outcome definitions, from v0.3 Outcome Definition) — What metrics does each feature support
- **BR-\* moat entries** (from v0.3 Moat Definition) — What features defend our competitive position
- **BR-\* pricing entries** (from v0.3 Pricing Model) — What features differentiate tiers
- **Market landscape analysis** (from v0.2) — Competitive feature comparison

This skill assumes v0.1-v0.2 research is complete and risk/tech decisions (v0.5) are not yet made.

## Produces

This skill creates/updates:

- **FEA-\* entries** (feature definitions, with confidence scoring) — Every feature in scope with traceability
- **BR-FEA-\* entries** (governance rules for feature decisions) — Scope protection rules
- **MVP-SCOPE artifact** — Explicit list: "These X features (FEA-001, FEA-005, FEA-008) define our MVP"
  - Example: `MVP-SCOPE: 5 P0 features + 3 P1 features = 8 total. Rationale: Delivers value on [KPI-001, KPI-002]. Competitive parity [FEA-001-003], Delta [FEA-004], Pricing [FEA-005]`
  - This becomes the definition for v0.4 user journeys and v0.7 build scope

All FEA- entries include confidence:
- `confidence: 2-3/5` (based on CFD- evidence strength)
- Evidence: "CFD-001, CFD-005, competitive-analysis"
- Forward target: "Would move to 4/5 if beta cohort uses it"

## Feature Classification Framework

| Type | Definition | Strategic Purpose | Evidence Required |
|------|------------|-------------------|-------------------|
| **Moat** | Builds/defends competitive advantage | Supports BR- moat rule | High (CFD- proving differentiation) |
| **Outcome** | Directly drives success metric | Tied to KPI- entry | High (KPI- link mandatory) |
| **Parity** | Matches competitor baseline | From Competitive Landscape | Medium (CFD- competitor evidence) |
| **Delta** | Differentiation from competitors | Our advantage over market | High (CFD- gap evidence) |
| **Tier** | Differentiates pricing packages | From Pricing BR- | Medium (BR- tier assignment) |
| **Table Stakes** | Expected but not differentiating | Industry standard | Low (common knowledge) |

**Rule**: P0 features require Moat, Outcome, or Delta classification. Table Stakes alone cannot justify P0.

## Product Type × Feature Strategy

Feature focus varies by product type (from v0.2 classification):

| Product Type | Primary Focus | Parity Approach | Delta Approach |
|--------------|---------------|-----------------|----------------|
| **Fast Follow** | Parity + focused delta | 1:1 critical feature match | Single compelling improvement |
| **Innovation** | Moat-building features | Minimal (new category) | Core differentiation IS the product |
| **Slice** | Segment-specific features | Partial (niche needs differ) | Deep fit for underserved segment |

### Fast Follow Constraint
**BR-FEA-PARITY-FIRST**: No delta features until parity features complete. Users compare to incumbent first.

### Innovation Pattern
Moat features = 60%+ of scope. Table stakes minimized. Delta is the entire value proposition.

### Slice Pattern
80/20 rule: Match 20% of incumbent features that serve 80% of niche use cases. Delta = niche-specific depth.

## Priority Tier Criteria

| Tier | Criteria | Evidence Threshold |
|------|----------|-------------------|
| **P0 — Must Have** | Blocks launch without it; tied to primary KPI- or moat BR- | CFD- proof + KPI-/BR- link |
| **P1 — Should Have** | Meaningfully improves outcome; supports tier differentiation | CFD- user signal |
| **P2 — Nice to Have** | Enhances experience; no direct KPI impact | Reasonable assumption OK |
| **P3 — Defer/Cut** | Scope creep signal; can add post-launch | None (remove from scope) |

**Kill criterion**: If >40% of features are P2/P3, scope is bloated. Re-evaluate.

## FEA- Output Template

Create FEA- entries in this format:

```
FEA-XXX: [Feature Name]
Type: [Moat | Outcome | Parity | Delta | Tier | Table Stakes]
Priority: [P0 | P1 | P2 | P3]
Description: [What the feature does — user-facing capability]
Outcome Link: [KPI-XXX this supports, or "N/A"]
Moat Link: [BR-XXX moat rule this supports, or "N/A"]
Pricing Link: [BR-XXX tier this belongs to, or "All tiers"]
Competitor Comparison: [Parity with X | Delta vs X | Unique | Table stakes]
Validation: [CFD-XXX evidence, or validation method]
Acceptance Criteria: [Testable condition for "done"]
```

**Example entries:**
```
FEA-001: One-Click Scheduling
Type: Parity
Priority: P0
Description: Schedule meetings with single click from availability view
Outcome Link: KPI-002 (activation rate)
Moat Link: N/A
Pricing Link: All tiers
Competitor Comparison: Parity with Calendly
Validation: CFD-012 (competitor feature audit)
Acceptance Criteria: User completes scheduling in ≤3 clicks

FEA-002: Offline Mode
Type: Delta
Priority: P0
Description: Full functionality without internet connection
Outcome Link: KPI-001 (TTFV for field users)
Moat Link: BR-012 (moat: works anywhere)
Pricing Link: BR-045 (Pro tier differentiator)
Competitor Comparison: Delta vs Notion (requires connection)
Validation: CFD-018 (user interviews: connectivity complaints)
Acceptance Criteria: All core features function with 0 connectivity for 24h
```

## BR-FEA- Governance Rules

Create governance rules for feature decisions:

```
BR-FEA-XXX: [Rule Name]
Type: [Scope Protection | Prioritization Rule | Validation Gate]
Rule: [Constraint statement]
Rationale: [Why this rule exists]
Enforcement: [When/how applied]
```

**Standard rules to establish:**
- `BR-FEA-001: Outcome Link Required` — P0/P1 features must link to KPI- entry
- `BR-FEA-002: Validation Before Build` — P0 features require CFD- evidence before development
- `BR-FEA-003: Scope Freeze Gate` — Feature list locked after v0.4; changes require EPIC

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Feature creep** | P2/P3 > 40% of scope | Cut ruthlessly; defer to backlog |
| **Implementation masquerading as feature** | "Use Redis caching" | Reframe as user outcome |
| **Orphaned features** | No KPI-, BR-, or CFD- link | Add traceability or cut |
| **Assumption-based priority** | "Users will love this" | Require CFD- evidence |
| **Parity inflation** | Everything is "parity" | Challenge: is competitor feature actually used? |
| **Delta without moat** | Delta feature easy to copy | Tie to defensible BR- moat |

## Downstream Connections

This skill's outputs feed into multiple downstream skills:

| Consumer | Consumes | Purpose |
|----------|----------|---------|
| **v0.4 User Journeys** | FEA-* entries + MVP-SCOPE artifact | Design journey paths through MVP features |
| **v0.5 Red Team Review** | FEA-* entries | Assess technical/risk feasibility of features |
| **v0.6 Architecture** | FEA-* entries + MVP-SCOPE | Design system that supports MVP features |
| **v0.7 Build Execution** | FEA-* entries + MVP-SCOPE | Define EPIC scope (which features = which EPICs) |
| **v0.9 GTM** | FEA-* entries (especially Delta) | Build launch messaging around delta features |

**Critical handoff**: The MVP-SCOPE artifact is the boundary. Everything in the list goes to v0.4+. Everything outside gets deferred to post-launch backlog.

## Detailed References

- **Good/bad examples**: See `references/examples.md`
- **FEA- entry template**: See `assets/fea.md`
- **Competitive feature matrix**: See `assets/competitive-feature-matrix.md`
