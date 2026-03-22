---
name: strategy-sprint
description: Create product strategy in 1 day, 1 week, or 1 month timeframes. Progressive strategy development framework.
disable-model-invocation: false
user-invocable: true
---

# Strategy Sprint: Write Strategy in 1 Day / 1 Week / 1 Month

**When to use:** When you need to create or update product strategy quickly, align stakeholders, or prepare for planning cycles

**Framework source:** Aakash Gupta's "How to Write a Product Strategy in 1 Day/Week/Month"

## Quick Start

1. Tell me: "I need a [1-day / 1-week / 1-month] strategy for [topic]"
2. I will check `context-library/strategy/` and `context-library/business-info-template.md` for existing context
3. I will ask 3-5 clarifying questions about scope, stakeholders, and constraints
4. We build progressively -- even a 1-month sprint starts with the 1-day foundation first
5. Output goes to `outputs/strategy-[topic]-[date].md`

**Which tier should you pick?**
- **1-Day:** You need a quick strategic POV for a specific question. An exec asked for direction, a new opportunity appeared, or you need to align the team before deeper work. Output: 1-page doc.
- **1-Week:** You are building a full strategic plan for a new initiative, quarterly planning, or cross-functional buy-in. Includes research, validation, and rollout planning. Output: 3-5 page doc with research backing.
- **1-Month:** You are defining annual/quarterly strategy for the entire product, planning a major pivot, launching a new business line, or preparing for board-level decisions. Includes financial modeling, competitive analysis, and full stakeholder socialization. Output: 10-15 page comprehensive strategy doc.

### Tier Escalation Triggers

Sometimes you start at one tier and realize you need a bigger sprint. Here's when to escalate:

**1-Day → 1-Week Escalation:**
Escalate when any of these appear during your 1-day sprint:
- You discover the problem is not well-defined (you're debating WHAT to solve, not HOW)
- Competitive landscape has shifted significantly and you need fresh research
- Key stakeholders disagree on the strategic direction (not just the tactic)
- The "snap strategy" keeps changing scope as you work -- sign of insufficient framing

**1-Week → 1-Month Escalation:**
Escalate when any of these appear during your 1-week sprint:
- The strategy requires cross-functional alignment that can't happen in a week (e.g., pricing changes, platform shifts)
- You need primary research (user interviews, market data) that takes time to collect
- The strategy touches 3+ product areas and each needs its own analysis
- Leadership wants a Board-level strategy document, not an internal working doc

**How to escalate gracefully:**
1. Don't restart -- use what you've already produced as input to the higher tier
2. Frame it: "The 1-day sprint surfaced that this is bigger than a tactical fix. Here's what I found so far. I recommend a 1-week sprint starting with [specific question we need to answer]."
3. The 1-day output becomes Day 1 of the 1-week sprint

---

## Overview

Strategy doesn't always need to be a month-long exercise. Depending on your timeline and context, you can create effective strategy in three different timeframes:

- **1 Day:** Snap strategy for quick alignment
- **1 Week:** Iteration with design sprints and validation
- **1 Month:** Full socialization with all stakeholders

---

## The Framework

### 1-Day Strategy (Snap Strategy)

**Use when:**
- New opportunity emerges suddenly
- Executive asks for quick direction
- Need to align team before deeper work

**What to include:**
1. **Problem/Opportunity** (2-3 sentences)
   - What's the core issue or opportunity?
   - Why does it matter now?

2. **Target Customer** (1 paragraph)
   - Who are we solving this for?
   - What's their current pain?

3. **Hypothesis** (1 sentence)
   - If we build X, then Y will happen because Z

4. **Success Metric** (1 metric + target)
   - What number moves if this works?
   - Example: "Increase activation from 45% to 60%"

5. **Key Risks** (3 bullets)
   - What could prevent success?
   - What assumptions are we making?

6. **Next Steps** (3 action items with owners)

**Time investment:** 4-6 hours
**Output:** 1-page doc that gets everyone pointed in the same direction

---

### 1-Week Strategy (Iteration Strategy)

**Use when:**
- Quarterly planning cycle
- New product area exploration
- Need cross-functional buy-in

**Build on 1-day foundation with:**

1. **Jobs-to-Be-Done Analysis**
   - What job is the customer hiring our product to do?
   - What progress are they trying to make?
   - Reference: `@context-library/strategy/jtbd-canvas.md`

2. **Competitive Positioning**
   - How do we differentiate?
   - What's our unfair advantage?
   - Reference: `@context-library/strategy/7-powers-framework.md`

3. **User Research Validation**
   - 5-10 customer interviews
   - Survey existing users
   - Review support tickets and feedback

4. **Technical Feasibility Check**
   - Sync with engineering leads
   - Identify major technical risks
   - Get rough effort estimates

5. **Success Criteria (expanded)**
   - Primary metric + 3-5 guardrail metrics
   - Leading indicators to track early
   - Definition of "good enough" to ship

6. **Rollout Plan**
   - Phased approach or big bang?
   - Beta testing strategy
   - Kill criteria (when to stop)

**Daily Breakdown (1-Week Sprint):**

| Day | Focus | Deliverable | Hours |
|-----|-------|-------------|-------|
| **Monday** | Foundation + Research Setup | 1-day snap strategy draft; schedule 5-8 interviews; pull support tickets and NPS data | 5-6 hrs |
| **Tuesday** | Customer Research | Conduct 3-5 interviews; review survey data and support themes; draft JTBD canvas | 5-6 hrs |
| **Wednesday** | Competitive + Technical | Competitive positioning analysis; engineering feasibility sync; identify top 3 technical risks | 4-5 hrs |
| **Thursday** | Synthesis + Strategy Draft | Combine research into strategy doc; define success criteria and guardrails; draft rollout plan | 5-6 hrs |
| **Friday** | Review + Finalize | Get feedback from 2-3 key stakeholders; incorporate feedback; finalize 3-5 page doc with clear next steps | 3-4 hrs |

**End-of-week deliverable:** 3-5 page strategy doc with JTBD analysis, competitive positioning, success metrics, and rollout plan.

**Time investment:** 20-30 hours across 5 days
**Output:** 3-5 page doc with research backing

---

### 1-Month Strategy (Full Socialization)

**Use when:**
- Annual planning
- Major product pivot
- New business line
- Board-level strategic decisions

**Build on 1-week foundation with:**

1. **Market Analysis**
   - TAM/SAM/SOM sizing
   - Market trends and forces
   - Competitor deep dives (3-5 players)
   - Reference: `/competitor-analysis`

2. **Strategic Fit**
   - How does this ladder up to company vision?
   - Resource allocation tradeoffs
   - What are we NOT doing as a result?

3. **7 Powers Analysis**
   - Which power(s) does this unlock?
   - Network effects, brand, scale, switching costs?
   - Reference: `@context-library/strategy/7-powers-framework.md`

4. **Financial Model**
   - Revenue projections
   - Cost to build and maintain
   - Payback period and ROI

5. **Org & Resourcing Plan**
   - Team structure needed
   - Hiring requirements
   - Dependencies on other teams

6. **Risk Mitigation**
   - For each major risk, what's the mitigation plan?
   - What experiments can de-risk early?

7. **Roadmap (6-12 months)**
   - Phased milestones
   - Key decision points
   - Go/no-go criteria at each phase

8. **Stakeholder Alignment Sessions**
   - Engineering review
   - Design review
   - Executive review
   - Sales/CS input (if relevant)
   - Legal/compliance check

**Weekly Breakdown (1-Month Sprint):**

| Week | Theme | Key Activities | Deliverables |
|------|-------|----------------|-------------|
| **Week 1: Foundation** | Discovery + Snap Strategy | Complete 1-day snap strategy; kick off market research; schedule all stakeholder reviews for weeks 2-3; begin competitive analysis; pull baseline metrics | Snap strategy doc (1-page); research plan; stakeholder review calendar |
| **Week 2: Deep Research** | User Research + Market Analysis | Conduct 8-10 user interviews; complete competitive deep dives (3-5 players); TAM/SAM/SOM sizing; engineering feasibility assessment; 7 Powers analysis | Research synthesis; competitive landscape doc; market sizing; technical feasibility report |
| **Week 3: Synthesis + Socialization** | Strategy Draft + Stakeholder Reviews | Write full strategy doc; run stakeholder alignment sessions (engineering, design, exec, sales/CS, legal); build financial model; draft roadmap | Strategy doc v1 (10-15 pages); financial model; stakeholder feedback log |
| **Week 4: Finalization** | Incorporate Feedback + Finalize | Incorporate all stakeholder feedback; finalize roadmap with go/no-go criteria; create executive summary; build FAQ doc from all questions received; present final strategy | Final strategy doc; executive summary; FAQ; presentation deck; risk mitigation plan |

**Key milestones within each week:**
- **Week 1, Day 3:** Snap strategy shared with leadership for early alignment
- **Week 2, Day 5:** Research synthesis complete, major insights shared
- **Week 3, Day 2-4:** Stakeholder reviews (do NOT push these to Week 4)
- **Week 4, Day 3:** Final draft circulated for async comments
- **Week 4, Day 5:** Strategy approved and shared broadly

**Time investment:** 60-80 hours across 4 weeks
**Output:** 10-15 page comprehensive strategy doc

---

## How to Use This Skill

### Step 1: Determine Your Timeline

Ask yourself:
- How much time do I actually have?
- What's the decision we're trying to make?
- Who needs to be aligned?

**Don't default to 1-month if 1-week will do.**

---

### Step 2: Use This Prompt Pattern

```
Use /strategy-sprint and reference context-library/business-info-template.md

I need to create a [1-day / 1-week / 1-month] strategy for: [describe the opportunity/problem]

Timeline: [your actual deadline]
Key stakeholders: [who needs to approve this]
Main decision: [what decision does this strategy inform]

Help me work through the appropriate framework step by step.
```

---

### Step 3: Build Progressively

- Start with 1-day version FIRST (even if you have a month)
- Get early feedback on the snap strategy
- Then layer in additional depth based on timeline
- **Don't skip the foundation**

---

## Pro Tips

**For 1-Day Strategy:**
- Write the hypothesis FIRST - everything else supports it
- If you can't articulate it in one sentence, you're not clear yet
- Get feedback from 2-3 key people before sharing broadly

**For 1-Week Strategy:**
- Do customer interviews EARLY in the week (Mon-Tue)
- Leave Fri for synthesis and doc writing
- Use `/user-research-synthesis` to process interviews quickly

**For 1-Month Strategy:**
- Schedule stakeholder reviews in weeks 2-3, not week 4
- Build in time to incorporate feedback
- Create a FAQ doc as you go (capture all questions you get)
- Use sub-agents for multiple perspectives: `@sub-agents/engineer-reviewer.md`, `@sub-agents/executive-reviewer.md`

**Universal tip:**
- Always include "What we're NOT doing" - strategy is about tradeoffs
- Make your assumptions explicit - call them out directly
- End with clear next steps and owners

---

## Common Mistakes

❌ **Spending a month when a week would work**
- Strategy should be "just enough" to make a decision
- You can always add depth later

❌ **Skipping the 1-day foundation**
- Jumping straight to detailed analysis without clarity
- Results in unfocused strategy documents

❌ **Writing strategy in isolation**
- Strategy needs conversation and debate
- Get input early and often

❌ **Treating this as final**
- Strategy evolves as you learn
- Plan to revisit quarterly

---

## Example Workflow

**Scenario:** You need a growth strategy for Q2

**Week 1:** Create 1-day snap strategy
- Define problem, hypothesis, success metric
- Share with team leads for initial feedback
- Time: 4 hours

**Week 2:** Expand to 1-week strategy
- Run 8 customer interviews
- Get technical feasibility input
- Draft rollout plan
- Time: 20 hours

**Week 3-4:** (Optional) Expand to 1-month if needed
- Build financial model
- Run competitive analysis
- Socialize with all stakeholders
- Time: 40 additional hours

**Result:** You have a clear strategy in 2 weeks instead of rushing a half-baked doc in 1 month

---

## Related Skills

- `/prd-draft` - Turn strategy into PRDs
- `/competitor-analysis` - Research competitors
- `/user-research-synthesis` - Process customer insights
- `context-library/strategy/jtbd-canvas.md` - Understand customer jobs
- `context-library/strategy/7-powers-framework.md` - Identify unfair advantages

---

## Output Quality Self-Check

Before delivering the strategy document, verify:

- [ ] **Hypothesis is one sentence:** Can you state the core hypothesis in a single, clear sentence? If not, sharpen it.
- [ ] **Tradeoffs are explicit:** Does the doc include a "What we are NOT doing" section with real tradeoffs, not just obvious non-starters?
- [ ] **Success metric is measurable:** Is there at least one concrete metric with a baseline and target (not "improve engagement")?
- [ ] **Risks are specific:** Are risks named with probability/impact, not vague ("market risk")? Each risk should have a mitigation action.
- [ ] **Next steps have owners and dates:** Every action item has a name attached and a deadline, not just "follow up."
- [ ] **Appropriate depth for tier:** 1-day = 1 page max. 1-week = 3-5 pages. 1-month = 10-15 pages. If you are significantly over or under, adjust.
- [ ] **Stakeholder input reflected:** If stakeholders were consulted, their feedback is visibly incorporated (not just "we talked to engineering").
- [ ] **Progressive build verified:** If doing a 1-week or 1-month sprint, confirm the 1-day foundation was completed first and is consistent with the expanded doc.
- [ ] **Tier escalation triggers noted:** If scope expanded beyond the chosen tier during the sprint, flag the escalation triggers that were hit and recommend the appropriate higher tier.

---

**Framework credit:** Adapted from Aakash Gupta's strategy framework. Read the full article: https://www.news.aakashg.com/p/strategy-in-1-day-week-month
