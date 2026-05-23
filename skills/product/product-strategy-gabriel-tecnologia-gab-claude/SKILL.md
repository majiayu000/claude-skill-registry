---
name: product-strategy
description: Create Product Strategies. Use when users ask for "product strategy", "product strategy document", or need to define the strategic vision and direction of a product.
---

# Product Strategy Generator

## Overview

Guide users in creating comprehensive Product Strategies:

```
Product Strategy = Vision + Insights + Challenges + Approaches + Accountability

```

This skill helps product managers create strategic documents that align stakeholders, define clear direction, and establish accountability metrics.

## Main Workflow

When a user requests to create a Product Strategy (e.g., "create a product strategy for App Gabriel"), follow this 5-phase workflow.

### Phase 1: Product Vision (ESSENCE)

**Objective:** Define the essence of the product—the what, for whom, and why now.

**Discovery Questions:**

```
1. What problem are you solving? (WHAT)
2. Who are you solving it for? (WHO)
3. Why is now the right time? (WHY)

```

**Generate Vision Statement using the format:**

| Field           | Description                                          |
| --------------- | ---------------------------------------------------- |
| **For**         | (Target customer)                                    |
| **Who**         | (Need or opportunity) - What problem are we solving? |
| **The**         | (Product name) is a (product category)               |
| **That**        | (Key benefit, reason to buy)                         |
| **Unlike**      | (Primary competitive alternative)                    |
| **Our Product** | (Primary differentiation statement)                  |

**Vision Characteristics:**

- Connects with the company vision.
- Aspirational, long-term goal.
- Relatively stable; pivots less than the strategy.

---

### Phase 2: Product Insights (LOGIC)

**Objective:** Gather data and logic that underpin the strategy.

**Components:**

**1. Competitors (Competitive Analysis)**

- Use WebSearch to research competitors.
- Document differentiators and similarities.
- Include quantitative data when available.

**2. Market Insight (TAM, audience, opportunity)**

- Define audience and target market.
- Identify market opportunities.
- Estimate market size if possible.

**3. Market Trends**

- Identify relevant trends.
- Use WebSearch for updated data.
- Connect trends with product timing.

**4. Customer Insights (Personas)**

- Define 2-3 main personas.
- Include behaviors, needs, and pain points.
- Search Slack for discussions about user feedback.

**Research Strategy:**

1. Search Slack for discussions about the product/problem.
2. Use WebSearch for competitive analysis.
3. Check Linear for related projects/issues.
4. Consolidate insights from all sources.

---

### Phase 3: Challenges (ROADBLOCKS)

**Objective:** Identify anticipated obstacles and risks.

**Challenge Categories:**

| Category                 | Guiding Question                                                                 |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Technical**            | What technical hurdles do we anticipate?                                         |
| **Customer Pain Points** | What customer problems will we face? Include emotional/psychological challenges. |
| **GTM Risks**            | What go-to-market risks exist? Why now?                                          |
| **Legal/Regulatory**     | What regulatory requirements do we need to mitigate?                             |

**Tips:**

- Be realistic but not pessimistic.
- Connect challenges with mitigations in the next phase.
- Consider internal challenges (team, resources) and external challenges (market, regulation).

---

### Phase 4: Approaches (PATHS)

**Objective:** Define the strategic path to achieve the vision.

**Components:**

**1. Approach (Chosen Strategy)**

- Single approach or multi-prong approach.
- Can vary for different customer segments.
- Justify the choice of approach.

**2. Overcoming Challenges**

- High-level plan to overcome each challenge from Phase 3.
- Be specific but not excessively detailed.
- Prioritize critical challenges.

**3. Do's & Don'ts (Guardrails)**

- What we WILL do along the way.
- What we WILL NOT do along the way.
- Maintain focus and avoid scope creep.

**Example Structure:**

```markdown
**Approach:** Multi-prong approach focused on:

1. [Approach 1]
2. [Approach 2]

**Overcome Challenges:**

- Technical: [mitigation plan]
- GTM: [mitigation plan]

**Do's:**

- [Allowed action 1]

**Don'ts:**

- [Prohibited action 1]
```

---

### Phase 5: Accountability (MEASURE)

**Objective:** Define how to measure success and maintain accountability.

**Components:**

**1. North Star Metric**

- Unique strategic and visionary metric.
- Represents the core value delivered to the customer.
- Aligned with the vision.

**2. Supporting Metrics**

- Perceptual metrics: engagement, satisfaction, happiness.
- Value metrics: sales, leads, ROI.
- Mix of leading and lagging indicators.

**3. Targets (Specific Goals)**

- Current baseline.
- Short-term goal (3-6 months).
- Long-term goal (12+ months).

**4. Progress Tracking**

- How and when to review progress.
- Who is responsible for tracking.
- Review rituals.

---

## Supported Modes

### Full Mode (~5 pages)

**When to use:** New products, significant pivots, annual strategies.
**Output:** Full markdown document with all 5 detailed phases.

### Quick Mode / One-Pager (~1 page)

**When to use:** Initial iteration, quick alignment, specific features.
**Output:** Summarized one-pager with essential points from each phase.

---

## Output and Saving

**File Location:** Save at `products/{product}/strategy.md`

---

## Best Practices

**DO:**

- Think deeply before writing.
- Collaborate with stakeholders 1:1 during creation.
- Share drafts early and often.
- Update as learning emerges.

**DON'T:**

- Wait to have all the answers to start.
- Work in isolation.
- Treat it as a static document.

---

**Product Strategy skill is active. Would you like to start a discovery session for a new product strategy or update an existing one?**
