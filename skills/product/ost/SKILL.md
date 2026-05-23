---
name: ost
description: Build Opportunity-Solution Trees to connect customer needs to solutions. Use when deciding what to build, structuring discovery work, translating stakeholder requests into opportunities, or testing assumptions before committing to solutions. Based on Teresa Torres's Continuous Discovery Habits framework.
---

# Opportunity-Solution Tree Skill

Help product teams structure discovery and connect solutions to real customer opportunities.

## The Framework

```
Business Outcome
    │   What the company needs (revenue, retention, market share)
    ▼
Product Outcome
    │   Customer behavior change that drives the business outcome
    ▼
Opportunities
    │   Customer needs, pains, desires (from research, not assumptions)
    ▼
Solutions
    │   Possible ways to address each opportunity
    ▼
Assumptions
    │   What must be true for the solution to work
    ▼
Experiments
        Tests to validate or invalidate assumptions
```

## Core Principles

1. **Start with outcomes, not outputs.** Features are outputs. Behavior changes are outcomes.
2. **Opportunities come from customers.** Not your ideas—their needs, pains, desires.
3. **Multiple solutions per opportunity.** Never fall in love with your first idea.
4. **Surface assumptions before building.** What must be true? What's riskiest?
5. **Small experiments, fast learning.** Test assumptions before committing resources.

## Workflows

### 1. Build a Tree

**Use when:** "Help me structure what we should build" or "I need to organize our discovery"

**Approach:** Work top-down through each layer, asking questions to populate the tree.

**Step 1: Business Outcome**
> "What business metric are you trying to move?"

Examples: Increase retention, reduce churn, grow revenue, expand to new segment.

**Step 2: Product Outcome**
> "What customer behavior change would drive that business outcome?"

Ask: "If customers did [X] more/less/differently, would that move the business metric?"

> For guidance on distinguishing outcomes, read `references/outcome-levels.md`

**Step 3: Opportunities**
> "What customer needs, pains, or desires have you discovered that relate to this outcome?"

Sources: Interview transcripts, support tickets, usage data, survey responses.

If they don't have research:
> "What do you *believe* are the opportunities? Flag these as assumptions to validate."

**Step 4: Solutions**
> "For each opportunity, what are 3+ different ways you could address it?"

Push for variety:
- "What's the simplest version?"
- "What would a competitor do?"
- "What if you had unlimited resources?"
- "What if you had to ship in a week?"

**Step 5: Assumptions**
> "For your top solution, what must be true for this to work?"

Categories:
- **Desirability:** Will customers want this?
- **Usability:** Can they figure out how to use it?
- **Feasibility:** Can we build it?
- **Viability:** Does the business model work?

> For detailed assumption mapping, read `references/assumption-mapping.md`

**Step 6: Experiments**
> "Which assumption is riskiest? How could you test it with minimal effort?"

Experiment types:
- Interviews / usability tests (desirability, usability)
- Prototypes / fake doors (desirability)
- Spikes / proof of concepts (feasibility)
- Pricing tests / landing pages (viability)

**Output:** Complete OST diagram with all layers populated.

See `assets/templates/ost-canvas.md` for the template.

---

### 2. Extract Opportunities from Research

**Use when:** "I have interview notes but don't know what opportunities exist"

**Approach:** Analyze research to surface opportunities in customer language.

**Questions to ask:**
1. "Share your research (interview quotes, survey responses, support tickets)"
2. "What patterns do you see in customer struggles?"
3. "What are they trying to do? What's getting in the way?"

**How to identify opportunities:**
- Look for pain points: "I hate when..." / "It's frustrating that..."
- Look for workarounds: "I have to..." / "The way I deal with it is..."
- Look for desires: "I wish..." / "It would be great if..."
- Look for unmet needs: "I can't..." / "There's no way to..."

**Output:** List of opportunities framed as customer needs, in their language.

**Format:**
```
Opportunity: [Customer need/pain/desire]
Evidence: [Quote or data point]
Frequency: [How often did this come up?]
```

---

### 3. Generate Multiple Solutions

**Use when:** "We're stuck on one solution" or "I need more options"

**Approach:** Force divergent thinking before converging.

**Questions to ask:**
1. "What's the opportunity you're trying to address?"
2. "What's your current solution idea?"
3. "Let's generate 5+ alternatives..."

**Prompts for alternatives:**
- "What if you had to solve this without writing code?"
- "What if you had to ship something in 24 hours?"
- "What would [competitor] do?"
- "What would make this 10x better, ignoring constraints?"
- "What's the opposite of your current idea?"
- "How did people solve this before software existed?"

**Output:** List of 5+ solution options for the opportunity, ranging from quick wins to ambitious bets.

---

### 4. Map Assumptions

**Use when:** "How do I know if this solution will work?" or "What should we test?"

**Approach:** Surface and prioritize the assumptions underlying a solution.

**Questions to ask:**
1. "What solution are you considering?"
2. "Let's identify what must be true for this to work..."

**Assumption categories:**

| Type | Question | Example |
|------|----------|---------|
| **Desirability** | Will customers want this? | "Users will prefer automated over manual" |
| **Usability** | Can they use it? | "Users will understand the new workflow" |
| **Feasibility** | Can we build it? | "We can integrate with their existing tools" |
| **Viability** | Does it work for the business? | "Users will pay $X for this feature" |

**For each assumption, assess:**
- **Confidence:** How sure are we? (Low/Medium/High)
- **Risk:** If wrong, how bad? (Low/Medium/High)

**Prioritize:** Low confidence + High risk = Test first

**Output:** Assumption map with prioritized list of what to test.

> For detailed framework, read `references/assumption-mapping.md`

---

### 5. Design Experiments

**Use when:** "How do I test this assumption?"

**Approach:** Match assumption type to appropriate experiment method.

**Questions to ask:**
1. "What assumption are you testing?"
2. "What type of assumption is it?" (Desirability/Usability/Feasibility/Viability)
3. "What's the cheapest way to get signal?"

**Experiment options by type:**

| Assumption Type | Light Experiments | Heavier Experiments |
|-----------------|-------------------|---------------------|
| **Desirability** | Customer interviews, surveys, fake door tests | Concierge MVP, landing page signups |
| **Usability** | Paper prototype tests, 5-second tests | Clickable prototype, wizard of oz |
| **Feasibility** | Spike, architecture review, vendor research | Proof of concept, technical prototype |
| **Viability** | Pricing surveys, competitive analysis | Pricing page test, pilot program |

**Experiment brief format:**
```
Assumption: [What we're testing]
Method: [How we'll test it]
Success criteria: [What would validate/invalidate]
Timeline: [How long]
Resources: [What we need]
```

**Output:** Experiment brief ready to execute.

---

### 6. Translate Feature Requests

**Use when:** "My stakeholder wants feature X" or "Leadership asked for this"

**Approach:** Reframe feature requests as opportunities to understand the underlying need.

**The problem:** Stakeholders often request solutions (features) not opportunities (needs). Building exactly what they ask for might not solve the real problem.

**Questions to ask:**
1. "What feature was requested?"
2. "Who requested it and why?"
3. "Let's find the opportunity beneath the request..."

**Reframing questions:**
- "What problem are they trying to solve with this feature?"
- "Who is experiencing this problem?"
- "What evidence do we have that this is a real problem?"
- "What would success look like for them?"
- "Are there other ways to address this need?"

**Example:**
- **Request:** "Add a dashboard with charts"
- **Opportunity beneath:** "Managers need to quickly understand team performance to intervene early"
- **Alternative solutions:** Daily email digest, alerts for anomalies, weekly automated report

**Output:**
1. The opportunity behind the request
2. The original request as one solution option
3. Alternative solutions to consider
4. Questions to validate the opportunity

---

## Quick Reference

### The Layers

| Layer | Question | Source |
|-------|----------|--------|
| Business Outcome | What does the company need? | Business strategy |
| Product Outcome | What behavior change drives that? | Product strategy |
| Opportunity | What customer need relates to this? | Customer research |
| Solution | How might we address this need? | Ideation |
| Assumption | What must be true? | Critical thinking |
| Experiment | How do we test it? | Discovery methods |

### Good vs. Bad Outcomes

| Bad (Output) | Better (Outcome) |
|--------------|------------------|
| Launch feature X | Increase weekly active users |
| Redesign onboarding | Reduce time-to-first-value |
| Build mobile app | Increase usage frequency |
| Add integrations | Reduce data entry time |

### Assumption Risk Matrix

```
                    High Risk
                        │
         ┌──────────────┼──────────────┐
         │   TEST       │    TEST      │
         │   SECOND     │    FIRST     │
         │              │              │
Low ─────┼──────────────┼──────────────┼───── High
Confidence              │              Confidence
         │   MONITOR    │    PROCEED   │
         │              │              │
         │              │              │
         └──────────────┼──────────────┘
                        │
                    Low Risk
```

## Reference Files

- `references/outcome-levels.md` - Business vs Product outcomes with examples
- `references/assumption-mapping.md` - Assumption types and prioritization

## Templates

- `assets/templates/ost-canvas.md` - Full OST template

## Attribution

This framework is based on Teresa Torres's work in "Continuous Discovery Habits" (2021).
