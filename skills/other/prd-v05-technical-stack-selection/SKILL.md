---
name: prd-v05-technical-stack-selection
description: >
  Make technology decisions for every product capability by discovering existing assets,
  evaluating vendor-aligned options, and categorizing as Reuse/Extend/Build/Buy/Integrate/Research
  during PRD v0.5 Red Team Review. Handles both greenfield and brownfield contexts.
  Triggers on "tech stack", "build or buy?", "what technologies?", "technical decisions",
  "what do we reuse?", "existing stack", "vendor constraint", "IBM-first",
  "what tools do we need?", "evaluate solutions", "select tech stack".
  Consumes FEA- (features), SCR- (screens), RISK- (constraints).
  Outputs TECH- entries with decisions, rationale, and cross-references.
  Feeds v0.6 Architecture Design.
---

# Technical Stack Selection

Make technology decisions for every capability your product needs — starting with what you already have, then evaluating what fits, then deciding what to build.

Position in workflow: v0.5 Risk Discovery Interview → **v0.5 Technical Stack Selection** → v0.6 Architecture Design

## Workflow Overview

1. **Discover Existing Assets** → Read SOT or interview user for current tech stack
2. **Categorize Layers** → Reuse / Extend / New / Replace for each capability
3. **Evaluate Vendor Fit** → Check preferred vendor catalog for New/Replace layers
4. **Evaluate Alternatives** → Research non-vendor options where vendor has gaps
5. **Check Product Family** → Shared infrastructure, component reuse, cross-product UX
6. **Create TECH- Entries** → Write entries using standard or reuse template
7. **Map to Risks** → Cross-reference every TECH- entry with RISK- constraints

## Decision Categories

| Category | Definition | When to Choose |
|----------|------------|----------------|
| **Reuse** | Existing asset covers this need as-is | Sibling product or prior work already solves this |
| **Extend** | Existing asset needs augmentation | Asset exists but needs new capabilities for this product |
| **Replace** | Existing asset doesn't fit, needs new solution | Current tool/service is wrong for this product's requirements |
| **Build** | Create custom solution | Core differentiator, no good alternatives, full control needed |
| **Buy** | Use paid service or managed product | Commodity capability, proven solutions exist, not a differentiator |
| **Integrate** | Connect to external platform or API | Ecosystem play, user expects it, data lives elsewhere |
| **Research** | Need POC before deciding | High uncertainty, multiple viable options, significant commitment |

**Evaluation order:** Reuse → Vendor-fit → Non-vendor alternatives → Build custom. Default to Buy for everything that isn't a core differentiator.

## Decision Framework

| Factor | Favors Reuse/Extend | Favors Buy (Vendor) | Favors Buy (Non-Vendor) | Favors Build |
|--------|---------------------|---------------------|-------------------------|--------------|
| **Existing asset** | Already deployed and working | Vendor has a product | Non-vendor product fits better | Nothing fits |
| **Differentiation** | Not relevant | Commodity capability | Commodity capability | Core to value prop |
| **Vendor alignment** | Already committed | Vendor product fits | Vendor has gap or poor fit | No vendor option |
| **Compliance** | Already compliant | Vendor product is compliant | Non-vendor has compliance cert | Must control compliance |
| **Team expertise** | Team already operates it | Managed service, less expertise needed | Team knows this tool | Team has deep knowledge |
| **Cost** | Sunk cost, incremental only | Reasonable vendor pricing | Better price/fit ratio | Long-term cost lower |

**Strong Reuse signals:**
- "We already run this for [sibling product]"
- "The team already operates and understands this"
- "Switching would cost more than keeping"

**Strong Build signals:**
- "This is why users choose us over competitors"
- "No existing solution fits our specific need"
- "We need to change this weekly based on learning"

**Strong Buy signals:**
- "Every product needs this"
- "Multiple proven solutions exist"
- "We'd just be recreating what vendors already built"

### Example Vendor Catalog (IBM Default)

Load `references/ibm-products.md` for the full catalog. Brief overview:

| Layer | Vendor Product | Fit Notes |
|-------|---------------|-----------|
| AI/ML | watsonx.ai | Foundation models, RAG, fine-tuning |
| AI Governance | watsonx.governance | Model monitoring, audit trails |
| Kubernetes | IBM Cloud Kubernetes (IKS) | HIPAA-ready, HITRUST certified |
| Database | IBM Cloud Databases (PostgreSQL, MongoDB, Redis, Elasticsearch) | HIPAA-ready, managed |
| Secrets | IBM Cloud Secrets Manager | Single-tenant Vault, HIPAA-ready |
| Messaging | IBM MQ, IBM Event Streams (Kafka) | Enterprise-grade, HIPAA-ready |
| Rules | IBM ODM | Decision management, rule execution |

When evaluating vendor products, check compliance certifications (HIPAA, SOC2, FedRAMP) against RISK- constraints before proceeding.

---

## Step 1: Discover Existing Assets

**Adaptive approach:** Check SOT first, then fill gaps with user interview.

**If TECH- entries exist in `SoT.TECHNICAL_DECISIONS.md`:**
Read existing entries. Present a summary to the user: "I found these existing technology decisions: [list]. Are these still current? Any changes since these were documented?"

**If SOT is empty (first time running this skill):**
Interview the user with these discovery questions:

1. "Does an existing product family exist with established technology choices?"
   - If YES → Load `references/brownfield.md` for asset discovery workflow
   - If NO → Proceed to Step 2 with all layers marked as "New"

2. "What is the current tech stack?" (ask per area)
   - Frontend framework and hosting
   - Backend language/framework
   - Authentication system
   - Database(s)
   - Cloud provider and infrastructure
   - CI/CD pipeline
   - Observability/monitoring tools

3. "Are there vendor constraints (e.g., IBM-first, AWS-only, Azure-only)?"
   - If YES → Load the relevant vendor reference (e.g., `references/ibm-products.md`)
   - If NO → Proceed with open evaluation

4. "Is this a regulated industry (healthcare, finance, government)?"
   - If YES → Note compliance requirements as constraints on all technology choices

### Discovery Output

Create a summary table:

| Capability Area | Existing Asset | Status |
|----------------|---------------|--------|
| [derived from FEA-/RISK-] | [what exists or "None"] | [Reuse / Extend / New / Replace] |

---

## Step 2: Categorize Layers

For each capability required by FEA- and RISK- entries, categorize:

| Category | Criteria | Action |
|----------|----------|--------|
| **Reuse** | Existing asset covers the need as-is | Create lightweight TECH- entry (use `assets/tech-reuse.md`) |
| **Extend** | Existing asset needs augmentation | Create TECH- entry documenting what changes are needed |
| **New** | No existing asset, greenfield decision | Proceed to Steps 3-4 for full evaluation |
| **Replace** | Existing asset is wrong for this product | Proceed to Steps 3-4; document what's being replaced and why |

**Derive capability areas from upstream IDs, not a fixed list.** Read FEA- entries and ask: "What technical capability does this feature require?" Read RISK- entries and ask: "Does this risk constrain or require a specific technology?"

Do not walk a generic layer checklist. Every capability area should trace to at least one FEA- or RISK- entry.

---

## Step 3: Evaluate Vendor Fit

For each "New" or "Replace" layer from Step 2:

1. Check if the preferred vendor has a product for this capability
2. Evaluate fit, compliance status, and cost
3. If vendor product fits → create TECH- entry with Category: Buy
4. If vendor product has poor fit or gaps → proceed to Step 4

**Evaluation criteria for vendor products:**

| Criterion | Questions |
|-----------|-----------|
| **Fit** | Does the vendor product solve our specific need? Feature gaps? |
| **Compliance** | Does it meet our regulatory requirements (from RISK- entries)? |
| **Cost** | What's the pricing? Cost at current scale AND 10x scale? |
| **Maturity** | Production-ready? Documentation quality? Active development? |
| **Integration** | How hard to integrate? Does it work with our existing stack? |

Use `assets/evaluation-scorecard.md` for structured comparison when multiple options exist.

---

## Step 4: Evaluate Alternatives

For layers where the vendor has gaps or poor fit:

1. Research 2-3 non-vendor alternatives
2. Score against the same criteria from Step 3
3. If a clear winner exists → create TECH- entry with decision
4. If high uncertainty → create TECH- entry with Category: Research, including evaluation criteria and deadline

**For Research items, define:**
- What must be learned before deciding
- How to evaluate (specific metrics, benchmarks, POC scope)
- Decision deadline (tied to a WAVE or milestone)

---

## Step 5: Check Product Family

**Only if sibling products were discovered in Step 1.** Skip for solo/greenfield products.

Lightweight checklist:

- [ ] **Shared infrastructure?** Will this product share clusters, databases, or services with siblings?
- [ ] **Component reuse?** Can UI components, API patterns, or operational tooling be shared?
- [ ] **Cross-product UX?** Should customers using multiple products have SSO or unified experience?
- [ ] **Shared vs. separate instances?** For each reused service, should it be the same deployment (separate namespace/realm) or a dedicated instance?

Document answers in relevant TECH- entries under "Product Family Notes."

---

## Step 6: Create TECH- Entries

For each technology decision, create a TECH- entry using the appropriate template:

- **Reuse/Extend:** Use `assets/tech-reuse.md` (lighter template)
- **Replace/Build/Buy/Integrate/Research:** Use `assets/tech.md` (standard template)

**Mandatory fields for every TECH- entry:**
- Features Served (FEA-XXX references)
- Risk Constraints (RISK-XXX references)
- Rationale (why this choice, not just what)
- Cost (at current AND 10x scale for Buy decisions)

**All TECH- entries are written to `SoT.TECHNICAL_DECISIONS.md`.** The skill produces entries; the SoT stores them.

See `references/examples.md` for 3 filled examples (Reuse, Buy, Research).

---

## Step 7: Map to Risks

Cross-reference every TECH- entry with RISK- constraints:

1. For each RISK- entry, verify at least one TECH- entry addresses it
2. For each TECH- entry, verify it doesn't introduce new unmitigated risks
3. Document the mapping in a summary table:

| Risk | Score | Technology Response |
|------|-------|-------------------|
| RISK-XXX | [score] | TECH-XXX addresses this by [how] |

If a RISK- entry has no corresponding TECH- response, flag it as an unmitigated risk requiring attention before proceeding to v0.6.

---

## Quality Gates

Before proceeding to v0.6 Architecture Design:

- [ ] All capability areas addressed (or explicitly N/A with rationale)
- [ ] Every TECH- entry cross-references FEA- and RISK- IDs it serves
- [ ] Build decisions justified as core differentiators
- [ ] Buy decisions have cost estimates at current AND 10x scale
- [ ] Research items have clear evaluation criteria and deadlines
- [ ] RISK- constraints from v0.5 Risk Discovery reflected in choices
- [ ] No vendor lock-in without explicit acknowledgment
- [ ] All TECH- entries written to SoT.TECHNICAL_DECISIONS.md
- [ ] Existing assets cataloged before new evaluations (brownfield check)

---

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| Resume-driven dev | "Let's use [hot new tech]" | Choose boring technology for non-differentiators |
| Evaluate everything | Scoring auth when Keycloak already works | Categorize Reuse/Extend/New/Replace first |
| Greenfield assumption | "Pick a frontend framework" when React exists | Discover existing assets before evaluating |
| Build everything | No Buy/Integrate decisions | Challenge: is this really a differentiator? |
| Buy everything | No Build decisions | Some things must be custom for your moat |
| Analysis paralysis | Research everything | Time-box research; decide with 70% confidence |
| Ignoring constraints | Tech choice conflicts with RISK- | Review RISK- entries before finalizing |
| Cost blindness | No cost estimates on Buy decisions | Every TECH- needs cost at current + 10x scale |
| Premature optimization | "We need Kubernetes for scale" | Design for 10x current needs, not 1000x |
| Orphan TECH- entry | TECH-003 references no FEA- or RISK- | Mandatory cross-reference in template |
| SoT contamination | Decision rationale essays in SoT template | Methodology in skill; structure in SoT |

---

## Bundled Resources

- **`references/ibm-products.md`** — IBM product catalog mapped to technology capabilities.
  Load when evaluating Buy options for teams with IBM-first or vendor constraints.

- **`references/brownfield.md`** — Existing product family discovery workflow.
  Load when user confirms existing products share infrastructure.

- **`references/examples.md`** — Completed TECH- entry examples (Reuse, Buy, Research).
  Load when producing TECH- entries to match format and depth.

- **`assets/tech.md`** — Standard TECH- entry template for Replace/Build/Buy/Integrate/Research.

- **`assets/tech-reuse.md`** — Lighter TECH- entry template for Reuse/Extend decisions.

- **`assets/evaluation-scorecard.md`** — Weighted scorecard for comparing Buy/Integrate options.

---

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.6 Architecture Design** | TECH- selections define the system | TECH-001 → ARC-001 frontend architecture |
| **v0.6 Technical Specification** | TECH- informs API design | TECH-003 → API-XXX data model constraints |
| **v0.7 Build Execution** | TECH- Research items become spikes | TECH-005 (Research) → EPIC task |
| **Hiring/Resourcing** | TECH- Build items define skills needed | TECH-010 (custom ML) → need ML engineer |

## Handoff

TECH- entries are complete when all quality gates pass.
Next stage: **v0.6 Architecture Design** (APOLLO ownership).
APOLLO should be able to start architecture work using only TECH- entries + upstream SoT files — no re-research needed.
