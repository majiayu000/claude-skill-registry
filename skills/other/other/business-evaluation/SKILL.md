---
name: business-evaluation
version: 1.0.0
description: '[Content] Evaluate business idea viability: Business Model Canvas, financial projections, risk matrix, go-to-market, execution plan.'
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Evaluate business idea viability with BMC, financials, risk matrix, GTM, and execution plan.

**Workflow:**

1. **Capture idea** — Problem, solution, target customer
2. **Load market analysis** — Market data from market-analysis
3. **Business Model Canvas** — All 9 blocks with evidence
4. **Financial projections** — 3-year revenue, costs, break-even
5. **Risk assessment** — 5+ risks with mitigation
6. **Execution plan** — 3 phases with milestones
7. **Verdict** — Viability score, confidence, recommendation

**Key Rules:**

- All 9 BMC blocks required, each with evidence
- Financial projections: explicit assumptions table
- Minimum 5 risks with mitigation AND residual risk
- Verdict must be evidence-backed with confidence declaration

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Business Evaluation

## Step 1: Capture the Idea

From user input, extract:

- **One-liner** — Elevator pitch in 1 sentence
- **Problem** — What pain point does it solve?
- **Solution** — How does it solve it?
- **Target customer** — Who specifically benefits?

## Step 2: Business Model Canvas

All 9 blocks required:

| Block                      | Key Question                      | Evidence Required    |
| -------------------------- | --------------------------------- | -------------------- |
| **Customer Segments**      | Who are we serving?               | Market research      |
| **Value Propositions**     | What value do we deliver?         | Customer pain points |
| **Channels**               | How do we reach customers?        | Channel analysis     |
| **Customer Relationships** | How do we maintain relationships? | Retention strategy   |
| **Revenue Streams**        | How do we make money?             | Pricing research     |
| **Key Resources**          | What do we need?                  | Resource assessment  |
| **Key Activities**         | What must we do?                  | Operational analysis |
| **Key Partnerships**       | Who helps us?                     | Partner landscape    |
| **Cost Structure**         | What does it cost?                | Cost analysis        |

## Step 3: Financial Projections (3 Years)

### Revenue Model

| Year | Users/Customers | ARPU | Revenue | Growth |
| ---- | --------------- | ---- | ------- | ------ |

### Cost Structure

| Category | Y1  | Y2  | Y3  |
| -------- | --- | --- | --- |

### Break-Even

- **Monthly burn:** ${X}
- **Break-even point:** Month/Year
- **Funding needed:** ${X}

### Assumptions Table

Every number must list its assumption and source.

## Step 4: Risk Assessment

Minimum 5 risks:

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
| ---- | ---------- | ------ | ---------- | ------------- |

Categories to consider: market, execution, financial, competitive, regulatory, technical.

## Step 5: Execution Plan

| Phase          | Timeline    | Focus                     | Key Milestones             |
| -------------- | ----------- | ------------------------- | -------------------------- |
| **Validation** | 0-3 months  | Customer discovery, MVP   | N interviews, prototype    |
| **Build**      | 3-6 months  | Core product, early users | Beta launch, first revenue |
| **Growth**     | 6-12 months | Scale, optimize           | Revenue target, team size  |

## Step 6: Go-to-Market

- **Launch strategy** — How to enter the market
- **Initial channels** — Top 3 acquisition channels
- **Pricing strategy** — Model + rationale + competitive comparison

## Step 7: Verdict

- **Viability score:** 1-10 with rationale
- **Confidence:** 95%/80%/60%/<60% with evidence basis
- **Recommendation:** Pursue | Pivot | Pause | Pass
- **Key condition:** What must be true for this to succeed?

## Output

Write to `docs/knowledge/strategy/business/{descriptive-slug}.md` using enforced template from `docs/templates/business-evaluation-template.md`.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/domain-analysis (Recommended)"** — Analyze domain model from business evaluation
- **"/plan"** — If ready to plan implementation
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
