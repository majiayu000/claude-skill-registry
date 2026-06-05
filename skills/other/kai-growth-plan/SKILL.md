---
name: kai-growth-plan
description: Generate a stage-appropriate marketing plan based on your company's MRR/stage. Uses the marketing-by-stage playbook to tell you exactly what to do (and what NOT to do) at pre-launch, early ($0-10K MRR), growth ($10-100K MRR), or scale ($100K+ MRR). Use when "what should I do for marketing", "growth plan", "marketing plan", "I just raised a round", "marketing strategy", "what's the right marketing for my stage", "GTM strategy", or any request for a stage-appropriate marketing roadmap.
---

Generate a marketing plan matched to your company stage. The wrong strategy at the wrong stage wastes money.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Stage Assessment

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Product** — what do you do? (1 sentence)
2. **Revenue** — current MRR/ARR? (determines stage)
3. **Team** — how many people? Any marketing hire?
4. **Channels active** — what are you already doing?
5. **Budget** — monthly marketing budget?
6. **PMF status** — do you have product-market fit? (retention cohorts, NPS, or gut feel)
7. **Top constraint** — time, money, or knowledge?

## Phase 2: Stage Diagnosis

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\marketing-by-stage.md`
Also load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\growth-loops-applied.md`
Also load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\demand-generation.md`
Also load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\saas-metrics-guide.md`

### Stage Map

| Stage | Revenue | Goal | Marketing Mode |
|-------|---------|------|---------------|
| **Pre-Launch** | $0 | Validate demand | Talk to humans, build waitlist |
| **Early** | $0-$10K MRR | Find PMF + first channel | Manual, unscalable, learn what works |
| **Growth** | $10K-$100K MRR | Optimize + expand channels | Systematize what works, test new channels |
| **Scale** | $100K+ MRR | Systematize + build team | Hire, automate, diversify |

## Phase 3: Marketing Plan

For each stage, produce:

### What to DO (prioritized)

| Priority | Activity | Why | /kai Skill to Use | Timeline |
|----------|----------|-----|-------------------|----------|
| P0 | [activity] | [reason] | `/kai-[skill]` | Week 1-2 |
| P1 | [activity] | [reason] | `/kai-[skill]` | Week 3-4 |
| P2 | [activity] | [reason] | `/kai-[skill]` | Month 2 |

### What NOT to do (critical)

| Don't Do This | Why It's Tempting | Why It's Wrong at This Stage |
|--------------|-------------------|------------------------------|
| [activity] | [reason] | [reason] |

### Growth Loop Recommendation

Based on the product, recommend 1-2 growth loops to design:
- **Viral loop** — does usage create shareable artifacts?
- **Content loop** — does user-generated content attract new users?
- **Paid loop** — can you profitably acquire and monetize?
- **Sales loop** — does each customer intro the next?

Point to `/kai-growth-plan` isn't the place to design the loop — it identifies which loop to build, then points to the right resources.

### Metrics Dashboard

What to measure at this stage (from SaaS metrics guide):

| Metric | Target | Why It Matters |
|--------|--------|---------------|
| [metric] | [target] | [reason] |

### 90-Day Roadmap

| Month | Focus | Key Activities | Expected Outcome |
|-------|-------|---------------|-----------------|
| Month 1 | [focus] | [activities] | [outcome] |
| Month 2 | [focus] | [activities] | [outcome] |
| Month 3 | [focus] | [activities] | [outcome] |

### Budget Allocation

| Channel | % of Budget | Monthly $ | Why |
|---------|------------|-----------|-----|
| [channel] | [%] | [$] | [reason] |

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\marketing-budget-forecasting.md` for budget frameworks.

## Phase 4: Skill Routing

Map the plan to specific /kai skills the user should run next:

```
Your 90-day plan maps to these skills:

Week 1: /kai-landing-page → produce your core conversion page
Week 2: /kai-email-system → set up lifecycle emails
Week 3: /kai-content-calendar → plan first month of content
Week 4: /kai-ad-campaign → launch first paid campaign
Month 2: /kai-cold-outreach → start outbound
Month 3: /kai-surround-sound → build AI presence
```

## Phase 5: Output

Save to `workspace/growth-plan/`:

```
workspace/growth-plan/
├── _stage-assessment.md         # Your stage + diagnosis
├── _90-day-plan.md              # The full plan
├── _budget-allocation.md        # Where to spend
├── _metrics-dashboard.md        # What to measure
├── _skill-routing.md            # Which /kai skills to run next
└── _anti-patterns.md            # What NOT to do
```
