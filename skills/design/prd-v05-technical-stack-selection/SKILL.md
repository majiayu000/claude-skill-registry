---
name: prd-v05-technical-stack-selection
description: Determine technologies needed to build the product, making build/buy/integrate decisions during PRD v0.5 Red Team Review. Handles both greenfield and brownfield contexts. Triggers on requests to select tech stack, evaluate technologies, make build vs. buy decisions, discover existing assets, or when user asks "what technologies?", "select tech stack", "build or buy?", "what do we reuse?", "existing stack", "technical decisions", "what tools do we need?", "evaluate solutions". Consumes FEA- (features), SCR- (screens), RISK- (constraints). Outputs TECH- entries with decisions, rationale, and trade-offs. Feeds v0.6 Architecture Design.
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

# Technical Stack Selection

Make technology decisions for every capability your product needs — starting with what you already have, then evaluating what fits, then deciding what to build.

Position in workflow: v0.5 Risk Discovery Interview → **v0.5 Technical Stack Selection** → v0.6 Architecture Design

## Consumes

This skill requires prior work from v0.3-v0.5:

- **FEA-\* feature entries** (from v0.3 Features Value Planning) — Every feature translates to technical capability requirements; derives which capability areas need technology decisions
- **SCR-\* screen entries** (from v0.4 Screen Flow Definition) — Screen count and component complexity informs frontend technology needs; DES- components reveal design system constraints
- **RISK-\* risk entries** (from v0.5 Risk Discovery Interview) — RISK- constraints directly affect technology choices (RISK-003: latency → choose edge hosting; RISK-004: compliance → choose HIPAA-ready provider)
- **Existing TECH-\* entries** (from prior products if brownfield) — If product family exists, inherited technology decisions constrain new choices
- **Product family information** (from user discovery if brownfield) — Shared infrastructure, existing databases, established frameworks narrow the evaluation space

This skill assumes v0.5 Risk Discovery Interview is complete and FEA-/SCR-/RISK- entries provide the constraint foundation.

## Produces

This skill creates/updates:

- **TECH-\* entries** (technology decisions, decision type + rationale) — Decisions for each capability area with categories (Reuse/Extend/New/Replace), options considered, choice made, and rationale tied to FEA-/RISK- constraints
- **Risk-to-Technology mapping table** — Validation showing every RISK- entry has corresponding TECH- response or explicit acceptance
- **Technical feasibility artifact** — Confidence assessment on whether technology choices support feature MVP-SCOPE and risk mitigations

All TECH- entries should include:
- **Decision Category**: Reuse/Extend/New/Replace/Build/Buy/Integrate/Research
- **Features Served**: FEA-XXX references (every TECH- must serve at least one feature)
- **Risk Constraints**: RISK-XXX references (if any risks constrain this decision)
- **Rationale**: Why this choice; trade-offs considered
- **Cost Assessment**: Current stage cost AND 10x scale cost for Buy decisions (MVP stage: prioritize speed and quality, not optimization)

Example TECH- entry (Buy decision with RISK constraint):
```markdown
TECH-003: Authentication & Authorization
Decision Category: Buy (managed service)
Features Served: FEA-010 (user auth), FEA-020 (role-based access control) — both in MVP-SCOPE
Risk Constraints: RISK-005 (security: we have no in-house security expertise), RISK-008 (compliance: need SOC2 certification path)

Choice: Clerk (platform auth)
Rationale:
  - Reduces security surface (RISK-005 mitigation: no password storage, no token handling)
  - Provides SOC2 compliance path (RISK-008 mitigation)
  - Includes MFA, passwordless, social login; UI handles all FEA-010 requirements without build
  - 30 day free tier; $25–$500/mo at growth stage (acceptable for MVP runway)

Trade-offs:
  - Plus: Zero auth code to maintain; future-proofs as compliance requirements evolve
  - Minus: Vendor lock-in; customer data in Clerk's tables (acceptable for SMB stage)

Cost:
  - MVP stage (0–10k users): ~$50–200/mo (free tier covers launch)
  - 10x scale (100k users): ~$500–2000/mo (still cheaper than building in-house team)

Product Family Notes: If sibling products exist, Clerk can SSO across them using shared realm config (document in shared infrastructure EPIC)

Alternatives Considered:
  - Firebase Auth: Similar, but tighter Google lock-in and slightly higher cost at scale
  - Auth0: Too expensive for MVP stage; better for enterprise products
  - Build custom: Rejected — RISK-005 says we lack in-house security expertise; not a differentiator

Next Step: If TECH-005 (Research: custom data encryption) decides to build, reconsider Auth0 for compliance sync
```

Example TECH- entry (Reuse decision from brownfield):
```markdown
TECH-001: Frontend Framework
Decision Category: Reuse
Features Served: FEA-006 (dashboard), FEA-007 (reports), all screen components — every UI in MVP-SCOPE
Risk Constraints: None (no frontend risk identified)

Existing Asset: React + Next.js (running in sibling product since 2023)
Rationale:
  - Already deployed, proven stable at 50k users
  - Team expertise established; no learning curve
  - Incremental cost: just new feature builds, no framework evaluation/migration risk
  - Shared component library available (DES-001–005 can import existing primitives)

Cost: $0 incremental (infrastructure already paid)

Product Family Notes: Share component library and auth context across products using monorepo structure (document in shared infrastructure EPIC)
```


## Workflow Overview

1. **Discover Existing Assets** → Read SOT or interview user for current tech stack
2. **Categorize Layers** → Reuse / Extend / New / Replace for each capability
3. **Evaluate Vendor Fit** → Check vendor options for New/Replace layers (if constraints exist)
4. **Evaluate Alternatives** → Research non-vendor options where gaps exist
5. **Check Product Family** → Shared infrastructure, component reuse, cross-product UX
6. **Create TECH- Entries** → Write entries using standard or reuse template
7. **Map to Risks** → Cross-reference every TECH- entry with RISK- constraints

## Decision Categories

| Category | Definition | When to Choose |
| --- | --- | --- |
| **Reuse** | Existing asset covers this need as-is | Sibling product or prior work already solves this |
| **Extend** | Existing asset needs augmentation | Asset exists but needs new capabilities for this product |
| **New** | No existing asset, greenfield decision | No prior work; need full evaluation |
| **Replace** | Existing asset doesn't fit, needs new solution | Current tool/service is wrong for this product's requirements |
| **Build** | Create custom solution | Core differentiator, no good alternatives, full control needed |
| **Buy** | Use paid service or managed product | Commodity capability, proven solutions exist, not a differentiator |
| **Integrate** | Connect to external platform or API | Ecosystem play, user expects it, data lives elsewhere |
| **Research** | Need POC before deciding | High uncertainty, multiple viable options, significant commitment |

**Evaluation order:** Reuse → Vendor-fit → Non-vendor alternatives → Build custom. Default to Buy for everything that isn't a core differentiator.

## Decision Framework

| Factor | Favors Reuse/Extend | Favors Buy (Vendor) | Favors Buy (Non-Vendor) | Favors Build |
| --- | --- | --- | --- | --- |
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

3. "Are there vendor constraints (e.g., must use AWS, Azure, or another preferred platform)?"
   - If YES → Load the relevant vendor reference if available
   - If NO → Proceed with open evaluation

4. "Is this a regulated industry (healthcare, finance, government)?"
   - If YES → Note compliance requirements as constraints on all technology choices

### Discovery Output

Create a summary table:

| Capability Area | Existing Asset | Status |
| --- | --- | --- |
| [derived from FEA-/RISK-] | [what exists or "None"] | [Reuse / Extend / New / Replace] |

---

## Step 2: Categorize Layers

For each capability required by FEA- and RISK- entries, categorize:

| Category | Criteria | Action |
| --- | --- | --- |
| **Reuse** | Existing asset covers the need as-is | Create lightweight TECH- entry (use `assets/tech-reuse.md`) |
| **Extend** | Existing asset needs augmentation | Create TECH- entry documenting what changes are needed |
| **New** | No existing asset, greenfield decision | Proceed to Steps 3-4 for full evaluation |
| **Replace** | Existing asset is wrong for this product | Proceed to Steps 3-4; document what's being replaced and why |

**Derive capability areas from upstream IDs, not a fixed list.** Read FEA- entries and ask: "What technical capability does this feature require?" Read RISK- entries and ask: "Does this risk constrain or require a specific technology?"

Do not walk a generic layer checklist. Every capability area should trace to at least one FEA- or RISK- entry.

### Reference Technology Layers

For context, here are common technology layers in modern products:

| Layer | Questions to Answer | Common Options |
| --- | --- | --- |
| **Frontend** | Framework? Hosting? Mobile/Web? | React, Vue, Next.js, Vercel |
| **Backend** | Language? Framework? Serverless? | Node, Python, Go, AWS Lambda |
| **Database** | SQL/NoSQL? Managed? | PostgreSQL, MongoDB, Supabase |
| **Auth** | Build or buy? SSO? | Auth0, Clerk, Firebase Auth |
| **Payments** | If monetized, processor? | Stripe, Paddle, LemonSqueezy |
| **Infrastructure** | Cloud? Edge? CDN? | AWS, GCP, Vercel, Cloudflare |
| **Integrations** | External services? APIs? | Depends on product |
| **AI/ML** | Models? Services? | OpenAI, Anthropic, local models |
| **Analytics** | Product analytics? Error tracking? | Mixpanel, PostHog, Sentry |
| **DevOps** | CI/CD? Monitoring? | GitHub Actions, Datadog |

---

## Step 3: Evaluate Vendor Fit

For each "New" or "Replace" layer from Step 2:

1. If your team has vendor constraints (AWS-only, Azure-first, etc.), check if the preferred vendor has a product for this capability
2. Evaluate fit, compliance status, and cost
3. If vendor product fits → create TECH- entry with Category: Buy
4. If vendor product has poor fit or gaps → proceed to Step 4

**Evaluation criteria for vendor products (or any Buy option):**

| Criterion | Questions |
| --- | --- |
| **Fit** | Does the vendor product solve our specific need? Feature gaps? |
| **Compliance** | Does it meet our regulatory requirements (from RISK- entries)? |
| **Cost** | What's the pricing at your current stage? Can you afford it until you reach product-market fit? (Cost optimization comes later, not MVP.) |
| **Maturity** | Production-ready? Documentation quality? Active development? |
| **Integration** | How hard to integrate? Does it work with our existing stack? |

**If your team has vendor constraints:** Create or load a vendor catalog reference that maps capability areas to vendor products and notes compliance certifications (e.g., HIPAA, SOC2, FedRAMP). Use `assets/evaluation-scorecard.md` for structured comparison when multiple options exist.

---

## Step 4: Evaluate Alternatives

For layers where vendor options don't exist or have poor fit:

1. Research 2-3 non-vendor alternatives
2. Score against the same criteria from Step 3
3. If a clear winner exists → create TECH- entry with decision
4. If high uncertainty → create TECH- entry with Category: Research, including evaluation criteria and deadline

**For Research items, define:**
- What must be learned before deciding
- How to evaluate (specific metrics, benchmarks, POC scope)
- Decision deadline (tied to a WAVE or milestone)

Use `assets/evaluation-scorecard.md` for structured scoring when comparing options.

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
| --- | --- | --- |
| RISK-XXX | [score] | TECH-XXX addresses this by [how] |

If a RISK- entry has no corresponding TECH- response, flag it as an unmitigated risk requiring attention before proceeding to v0.6.

---

## Quality Gates

Before proceeding to v0.6 Architecture Design:

- [ ] All capability areas addressed (or explicitly N/A with rationale)
- [ ] Every TECH- entry cross-references FEA- and RISK- IDs it serves
- [ ] Build decisions justified as core differentiators
- [ ] Buy decisions have realistic cost estimates for your current stage (MVP vs. scaling phase)
- [ ] Cost decisions prioritize speed-to-market and quality experience for MVP (not premature optimization)
- [ ] Research items have clear evaluation criteria and deadlines
- [ ] RISK- constraints from v0.5 Risk Discovery reflected in choices
- [ ] No vendor lock-in without explicit acknowledgment
- [ ] All TECH- entries written to SoT.TECHNICAL_DECISIONS.md
- [ ] Existing assets cataloged before new evaluations (brownfield check)

---

## Anti-Patterns to Avoid

| Pattern | Signal | Fix |
| --- | --- | --- |
| Resume-driven development | "Let's use [hot new tech]" | Choose boring technology for non-differentiators |
| Evaluate everything | Scoring auth when Keycloak already works | Categorize Reuse/Extend/New/Replace first |
| Greenfield assumption | "Pick a frontend framework" when React exists | Discover existing assets before evaluating |
| Build everything | No Buy/Integrate decisions | Challenge: is this really a differentiator? |
| Buy everything | No Build decisions | Some things must be custom for your moat |
| Analysis paralysis | Research everything | Time-box research; decide with 70% confidence |
| Ignoring constraints | Tech choice conflicts with RISK- | Review RISK- entries before finalizing |
| **Premature cost optimization** | "We must use the cheapest database" for MVP | Optimize for speed-to-market and quality first. Reduce costs after product-market fit. |
| Cost blindness | No cost estimates on Buy decisions | Every TECH- needs realistic cost for your stage |
| Over-engineering for scale | "We need Kubernetes for scale" | Design for 10x current needs, not 1000x unknown scale |
| Orphan TECH- entry | TECH-003 references no FEA- or RISK- | Mandatory cross-reference in template |
| SoT contamination | Decision rationale essays in SoT template | Methodology in skill; structure in SoT |

---

## Bundled Resources

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
| --- | --- | --- |
| **v0.6 Architecture Design** | TECH- selections define the system | TECH-001 → ARC-001 frontend architecture |
| **v0.6 Technical Specification** | TECH- informs API design | TECH-003 → API-XXX data model constraints |
| **v0.7 Build Execution** | TECH- Research items become spikes | TECH-005 (Research) → EPIC task |
| **Hiring/Resourcing** | TECH- Build items define skills needed | TECH-010 (custom ML) → need ML engineer |

## Handoff

TECH- entries are complete when all quality gates pass.
Next stage: **v0.6 Architecture Design** (downstream ownership).
The downstream consumer should be able to start architecture work using only TECH- entries + upstream SoT files — no re-research needed.
