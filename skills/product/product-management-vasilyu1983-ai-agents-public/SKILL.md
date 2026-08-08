---
name: product-management
description: "Founder-PM toolkit for discovery, roadmaps, prioritization, and PMF measurement. Use when planning product strategy, metrics, or roadmaps."
---

# Product Management (Jan 2026)

This skill turns the assistant into an operator, not a lecturer.

Everything here is:
- **Executable**: templates, checklists, decision flows
- **Decision-first**: measurable outcomes, explicit trade-offs, clear ownership
- **Organized**: resources for depth; templates for immediate copy-paste

---

**Modern Best Practices (Jan 2026)**:
- Evidence quality beats confidence: label signals strong/medium/weak; write what would change your mind.
- Outcomes > output: roadmaps are bets with measurable impact and guardrails, not feature inventories.
- Metrics must be defined (formula + timeframe + data source) to be actionable.
- Privacy, security, and accessibility are requirements, not afterthoughts.
- Hybrid decision loops: AI surfaces anomalies, patterns, and forecasts; humans apply context, ethics, and long-term strategy.
- Accountability: product is often held responsible for business outcomes; confirm the operating model in your org and validate benchmarks with current sources.
- Portfolio diversification: a common heuristic is 70% core, 20% adjacent, 10% transformational; adapt to strategy and constraints.

## When to Use This Skill

Use this skill when the user asks to do real product work, such as:

- “Create / refine a PRD / spec / business case / 1-pager”
- “Turn this idea into a roadmap” / “Outcome roadmap for X”
- “Design a discovery plan / interview script / experiment plan”
- “Define success metrics / OKRs / metric tree”
- “Position this product against competitors”
- “Run a difficult conversation / feedback / 1:1 / negotiation”
- “Plan a product strategy / vision / opportunity assessment”

Do not use this skill for:
- Book summaries, philosophy, or general education
- Long case studies or storytelling

---

## Quick Reference

| Task | Template | Domain | Output |
|------|----------|---------|---------|
| Discovery interview | `customer-interview-template.md` | Discovery | Interview script with Mom Test patterns |
| Opportunity mapping | `opportunity-solution-tree.md` | Discovery | OST with outcomes, problems, solutions |
| PMF survey | `pmf-survey-template.md` | Discovery | Sean Ellis + NPS + usage survey |
| Outcome roadmap | `outcome-roadmap.md` | Roadmap | Now/Next/Later with outcomes and themes |
| OKR definition | `okr-template.md` | Metrics | 1-3 objectives with 2-4 key results each |
| Product positioning | `positioning-template.md` | Strategy | Competitive alternatives -> value -> segment |
| Product vision | `product-vision-template.md` | Strategy | From→To narrative with 3-5 year horizon |
| Quarterly review | `quarterly-product-review.md` | Strategy | Keep / cut / double-down product audit |
| Prioritization | `prioritization-scorecard.md` | Prioritization | RICE/ICE scoring with kill criteria |
| Kill criteria | `kill-criteria-template.md` | Prioritization | Pre-defined stop conditions per initiative |
| 1:1 meeting | `1-1-template.md` | Leadership | Check-in, progress, blockers, growth |
| Post-incident debrief | `a3-debrief.md` | Leadership | Intent vs actual, root cause, action items |

---

## Decision Tree: Choosing the Right Workflow

```text
User needs: [Product Work Type]
    ├─ Discovery / Validation?
    │   ├─ Customer insights? → Customer interview template
    │   ├─ Hypothesis testing? → Assumption test template
    │   └─ Opportunity mapping? → Opportunity Solution Tree
    │
    ├─ Strategy / Vision?
    │   ├─ Long-term direction? → Product vision template
    │   ├─ Market positioning? → Positioning template (Dunford)
    │   ├─ Big opportunity? → Opportunity assessment
    │   └─ Amazon-style spec? → PR/FAQ template
    │
    ├─ Planning / Roadmap?
    │   ├─ Outcome-driven? → Outcome roadmap (Now/Next/Later)
    │   ├─ Theme-based? → Theme roadmap
    │   └─ Metrics / OKRs? → Metric tree + OKR template
    │
    ├─ Prioritization / Focus?
    │   ├─ What to build next? → Prioritization scorecard (RICE/ICE)
    │   ├─ What to stop? → Kill criteria template + quarterly review
    │   ├─ Scope too large? → Scope negotiation patterns
    │   └─ PMF check? → PMF survey + retention curve analysis
    │
    └─ Leadership / Team Ops?
        ├─ 1:1 meeting? → 1-1 template
        ├─ Giving feedback? → Feedback template (SBI model)
        ├─ Post-incident? → A3 debrief
        ├─ Stakeholder pushback? → Stakeholder management patterns
        └─ Negotiation? → Negotiation one-sheet (Voss)
```

---

## Do / Avoid (Jan 2026)

### Do

- Start from the decision: what are we deciding, by when, and with what evidence.
- Define metrics precisely (formula + timeframe + data source) and add guardrails.
- Use discovery to de-risk value before building; prioritize by evidence, not opinions.
- Write “match vs ignore” competitive decisions, not feature grids.

### Avoid

- Roadmap theater (shipping lists) without outcomes and learning loops.
- Vanity KPIs (raw signups, impressions) without activation/retention definitions.
- "Build-first validation" (shipping MVPs without falsifiable hypotheses).
- Collecting customer data without purpose limitation, retention, and access controls.
- Building for engineering elegance instead of user value (technical founder trap).
- Feature creep without kill criteria (every feature should have a pre-defined stop condition).
- Saying "yes" to stakeholder requests without trade-off analysis.
- Measuring PMF once instead of continuously across segments.

## Prioritization & Saying No

The most common founder-PM failure: building everything, killing nothing, and running out of time before impact.

### Prioritization Frameworks

| Framework | Formula / Method | Best For | Watch For |
|-----------|-----------------|----------|-----------|
| **RICE** | (Reach x Impact x Confidence) / Effort | Comparing features with data | Gaming confidence scores |
| **ICE** | Impact x Confidence x Ease | Quick gut-check prioritization | Over-simplification |
| **Opportunity Scoring** | Importance x (Importance - Satisfaction) | Discovery-driven, JTBD-aligned | Requires user research data |
| **Cost of Delay** | Value per unit time / Duration | Time-sensitive decisions | Harder to estimate accurately |
| **Weighted Shortest Job First (WSJF)** | Cost of Delay / Job Size | SAFe/Lean, flow optimization | Requires calibrated estimates |

Pick one. Use it consistently. The framework matters less than the discipline of scoring everything the same way.

### Kill Criteria

Every initiative should have pre-defined conditions for stopping:

- **Usage threshold**: If <X% of target users adopt within Y weeks, stop.
- **Cost ceiling**: If development exceeds X hours/dollars, pause and re-evaluate.
- **Time limit**: If not shipped within X weeks, kill or radically descope.
- **Metric guardrail**: If [guardrail metric] degrades by >X%, roll back.

Use `assets/prioritization/kill-criteria-template.md` to define these before starting.

### Feature Bridge Migration

When replacing an existing feature with a new one, don't hard-kill the old feature. Use a **bridge migration** pattern to prevent user loss.

**Bridge mode**: Run both old and new features simultaneously. Route users to the new experience by default but keep the old path accessible (via link, fallback, or settings toggle).

**Substitution-based kill rule**:
1. Define the absorption metric: % of old-feature users who now use the new feature for the same job.
2. Set the kill threshold: new feature absorbs ≥80% of old-feature users.
3. Set the duration: threshold must hold for 14 consecutive days with no retention regression.
4. Only kill the old feature when all three conditions are met.

```text
BRIDGE MIGRATION SEQUENCE:

1. Ship new feature alongside old feature
2. Default new users to new experience
3. Migrate existing users gradually (progressive rollout)
4. Monitor: absorption rate, retention by cohort, support tickets
5. Old feature absorbs ≥80% for 14 days + no retention drop?
   ├─ Yes → Kill old feature, remove code
   └─ No → Investigate gaps, iterate new feature, extend bridge
```

**When NOT to bridge**: Security vulnerabilities, compliance requirements, or features with near-zero usage (<1% MAU). These can be killed directly with notice.

### Scope Negotiation

When stakeholders push for more scope:
- Reframe as trade-offs: "We can add X if we cut Y — which matters more?"
- Anchor on outcomes: "The goal is [metric]. Does this addition move it?"
- Offer phased delivery: "V1 without this; measure; add in V2 if data supports it."
- Document non-goals explicitly in every spec.

### "What to Stop Doing" Quarterly Review

Every quarter, review the product with `assets/strategy/quarterly-product-review.md`:
- Which features have <5% usage? → Candidate for removal
- Which initiatives produced no measurable outcome? → Stop or pivot
- Which ongoing costs (maintenance, support) exceed their value? → Sunset
- What are you doing "because we always have" but nobody asked for? → Question

For detailed prioritization patterns and worked examples: see `references/prioritization-frameworks.md`.

---

## Product-Market Fit Measurement

PMF is not a binary event. It's a signal you measure across multiple dimensions.

### Sean Ellis Test

Survey users: "How would you feel if you could no longer use [product]?"
- **Very disappointed**: Target >40% for PMF signal
- **Somewhat disappointed**: Useful but not dependent
- **Not disappointed**: Not finding value

Use `assets/discovery/pmf-survey-template.md` for the full survey (combines Sean Ellis + NPS + usage questions).

### Retention Curve Analysis

- Plot cohort retention over time (weekly or monthly depending on product cadence)
- **Flattening curve** = PMF signal (users who stay, stay)
- **Declining curve** = No PMF (even retained users eventually leave)
- Segment by ICP: you may have PMF in one segment but not another

### Engagement Scoring

Define activation precisely (formula + timeframe + data source):
- What actions constitute "activated"? (not just signed up)
- What's the activation window? (first 7 days, first 14 days?)
- What engagement depth separates power users from casual?

### Feature Audit

Periodically audit feature usage to identify what to keep, improve, or remove:
- Top 20% features by usage → invest, polish
- Middle 60% → maintain, don't expand
- Bottom 20% → candidate for removal or redesign
- Features with high support cost relative to usage → redesign or sunset

### Segmented PMF

PMF varies by segment. Measure separately for:
- ICP vs non-ICP customers
- Free vs paid users
- Self-serve vs sales-assisted
- By company size, industry, or geography

For detailed PMF measurement methodology: see `references/pmf-measurement.md`.

---

## Stakeholder Management

Founders manage board members, investors, early customers, co-founders, and (eventually) team leads — often without formal PM training.

Key patterns:
- **Board / investors**: Update monthly with metrics + decisions + asks. Use narrative format, not slide decks. Lead with "what we learned" not "what we shipped."
- **Early customers**: They are partners, not just users. Share roadmap intent (not commitments). Ask for input on priorities, not feature requests.
- **Co-founder alignment**: Weekly sync on priorities. Disagree and commit. Document decisions.
- **Saying no to stakeholders**: "We're not doing X because [reason tied to strategy]. Here's what we're doing instead and why."

For detailed stakeholder management patterns: see `references/stakeholder-management.md`.

---

## What Good Looks Like

- Evidence: 5–10 real user touchpoints or equivalent primary data for material bets.
- Scope: clear non-goals and acceptance criteria that can be tested.
- Learning: post-launch review with metric deltas, guardrail impact, and next decision.

## PRDs and Specs

For PRDs/specs and writing-quality requirements, use the templates in `../docs-ai-prd/`:

- PRD templates: [../docs-ai-prd/assets/prd/prd-template.md](../docs-ai-prd/assets/prd/prd-template.md) and [../docs-ai-prd/assets/prd/ai-prd-template.md](../docs-ai-prd/assets/prd/ai-prd-template.md)

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- AI system lifecycle: [assets/ai/ai-lifecycle-template.md](assets/ai/ai-lifecycle-template.md)
- Agentic workflow docs: [assets/ai/agentic-ai-orchestration.md](assets/ai/agentic-ai-orchestration.md)
- AI product patterns: [references/ai-product-patterns.md](references/ai-product-patterns.md)

## Navigation

**Resources**
- [references/discovery-best-practices.md](references/discovery-best-practices.md)
- [references/roadmap-patterns.md](references/roadmap-patterns.md)
- [references/delivery-best-practices.md](references/delivery-best-practices.md)
- [references/strategy-patterns.md](references/strategy-patterns.md)
- [references/positioning-patterns.md](references/positioning-patterns.md)
- [references/data-product-best-practices.md](references/data-product-best-practices.md)
- [references/interviewing-patterns.md](references/interviewing-patterns.md)
- [references/metrics-best-practices.md](references/metrics-best-practices.md)
- [references/leadership-decision-frameworks.md](references/leadership-decision-frameworks.md)
- [references/operational-guide.md](references/operational-guide.md)
- [references/prioritization-frameworks.md](references/prioritization-frameworks.md)
- [references/pmf-measurement.md](references/pmf-measurement.md)
- [references/stakeholder-management.md](references/stakeholder-management.md)
- [data/sources.json](data/sources.json)

**Templates**
- Discovery: [assets/discovery/customer-interview-template.md](assets/discovery/customer-interview-template.md), [assets/discovery/assumption-test-template.md](assets/discovery/assumption-test-template.md), [assets/discovery/opportunity-solution-tree.md](assets/discovery/opportunity-solution-tree.md), [assets/discovery/pmf-survey-template.md](assets/discovery/pmf-survey-template.md)
- Prioritization: [assets/prioritization/prioritization-scorecard.md](assets/prioritization/prioritization-scorecard.md), [assets/prioritization/kill-criteria-template.md](assets/prioritization/kill-criteria-template.md)
- Strategy/Vision: [assets/strategy/product-vision-template.md](assets/strategy/product-vision-template.md), [assets/strategy/opportunity-assessment.md](assets/strategy/opportunity-assessment.md), [assets/strategy/positioning-template.md](assets/strategy/positioning-template.md), [assets/strategy/PRFAQ-template.md](assets/strategy/PRFAQ-template.md), [assets/strategy/quarterly-product-review.md](assets/strategy/quarterly-product-review.md)
- Data: [assets/data/data-product-canvas.md](assets/data/data-product-canvas.md)
- Roadmaps: [assets/roadmap/outcome-roadmap.md](assets/roadmap/outcome-roadmap.md), [assets/roadmap/theme-roadmap.md](assets/roadmap/theme-roadmap.md)
- Metrics: [assets/metrics/metric-tree.md](assets/metrics/metric-tree.md), [assets/metrics/okr-template.md](assets/metrics/okr-template.md)
- Ops/Leadership: [assets/ops/1-1-template.md](assets/ops/1-1-template.md), [assets/ops/feedback-template.md](assets/ops/feedback-template.md), [assets/ops/a3-debrief.md](assets/ops/a3-debrief.md), [assets/ops/negotiation-one-sheet.md](assets/ops/negotiation-one-sheet.md)

**Related Skills**
- [../docs-ai-prd/SKILL.md](../docs-ai-prd/SKILL.md) — PRD, stories, and prompt/playbook templates
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System design guidance for specs and PRDs
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — UI implementation considerations for product specs
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — Backend/API implications of product decisions
- [../startup-growth-playbooks/SKILL.md](../startup-growth-playbooks/SKILL.md) — PLG case studies for activation design

---

## Operational Guide

See [references/operational-guide.md](references/operational-guide.md) for detailed patterns, template walkthroughs, example flows, and execution checklists. Keep SKILL.md as the navigation hub; use assets/ when producing artifacts.

---

## External Resources

See [data/sources.json](data/sources.json) for official frameworks (Lean Startup, OST, PR/FAQ, OKRs) and AI/LLM safety references.

---

Use the quick reference and decision tree above to choose a template, then follow the operational guide for depth.

---

## Trend Awareness Protocol

**IMPORTANT**: When users ask recommendation questions about product management tools, frameworks, or practices, use a web search tool to check current trends before answering. If web search is unavailable, use `data/sources.json` and state clearly what you verified vs assumed.

### Trigger Conditions

- "What's the best tool for [roadmapping/product analytics/discovery]?"
- "What should I use for [OKRs/metrics/customer feedback]?"
- "What's the latest in product management?"
- "Current best practices for [discovery/roadmaps/prioritization]?"
- "Is [framework/tool] still relevant in 2026?"
- "[Linear] vs [Jira] vs [other]?" or "[Amplitude] vs [Mixpanel]?"
- "Best approach for [AI product management/agentic products]?"

### Required Searches

1. Search: `"product management best practices 2026"`
2. Search: `"[specific tool] vs alternatives 2026"`
3. Search: `"product management trends January 2026"`
4. Search: `"[discovery/roadmap/OKR] frameworks 2026"`

### What to Report

After searching, provide:

- **Current landscape**: What PM tools/frameworks are popular NOW
- **Emerging trends**: New tools, methods, or patterns gaining traction
- **Deprecated/declining**: Frameworks/tools losing relevance
- **Recommendation**: Based on fresh data, not just static knowledge

### Example Topics (verify with fresh search)

- Product management tools (Linear, Productboard, Notion, Coda)
- Analytics platforms (Amplitude, Mixpanel, PostHog)
- Discovery and research tools (Maze, UserTesting, Dovetail)
- Roadmapping approaches (outcome-based, theme-based, now/next/later)
- AI product management patterns
- Prioritization frameworks (RICE, ICE, opportunity scoring)
- OKR and metrics tools

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
