---
name: value-stack
description: Build a value stack table — list every deliverable with its individual value, calculate total value, show the price, show the savings. Includes 3-5 bonus items with names, descriptions, and assigned values. Use when user needs a "value stack", "pricing table", "offer stack", or wants to visualize their product's value vs. price.
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Value Stack Builder

**Purpose:** Create a compelling value stack that shows the total value of everything included in an offer vs. the actual price. The goal: make the price feel like a steal relative to the perceived value.

## When to Activate

Use this skill when:
- User wants to build a value stack or pricing table
- User mentions "offer stack", "value comparison", or "pricing visualization"
- User is creating a sales page and needs the pricing section
- User wants to design bonuses for their offer

## Core Principle

**Price on value, not cost.** The customer doesn't care what it costs you to deliver. They care what the outcome is worth to them. A $2,000 offer that solves a $20,000 problem is cheap. The value stack makes this math visible.

**Target ratio:** Total perceived value should be 5-10x the actual price. At $1,497, aim for $10,000-$15,000 in total stacked value.

## Required Information

- **Core product/offer name**
- **What's included** (features, modules, deliverables)
- **Price**
- **Existing bonuses** (if any)
- **Top 3 objections** (bonuses should address these)

## Process

### Step 1: List Core Deliverables

Break the core offer into individual components. Each should be something that could theoretically be sold separately.

**For each deliverable:**
- Name it compellingly (not "Module 3" but "The Content Engine Framework")
- Describe what it includes (1-2 sentences)
- Assign individual value based on what a comparable standalone product costs

**Value assignment rules:**
- Research comparable products/services for realistic pricing
- Use "if you hired someone" or "comparable product costs" framing
- Don't make values absurdly inflated — credibility matters
- Round to clean numbers ($497, $997, $1,997)

### Step 2: Design Strategic Bonuses (3-5)

**Each bonus should address a specific objection:**

| Objection | Bonus Solution |
|-----------|---------------|
| "I don't have time" | Quick-start guide, done-for-you templates |
| "I'm not sure it'll work for me" | Personalized assessment, 1-on-1 call |
| "I don't have the tech skills" | Tech setup walkthrough, support access |
| "What if I get stuck?" | Community access, office hours, Q&A |
| "I've tried similar things before" | Case studies, guarantee, proven process doc |

**For each bonus:**
- Compelling name (not "Bonus 1")
- What it is and what problem it solves (2-3 sentences)
- Individual value
- Why it's valuable (connect to objection)

### Step 3: Build the Stack

## Output Format

```markdown
# Value Stack: [Offer Name]

**Offer Price:** $[Price]
**Total Stacked Value:** $[Total]
**You Save:** $[Savings] ([X]%)

---

## Core Offer

| # | What You Get | Description | Value |
|---|-------------|-------------|-------|
| 1 | [Deliverable Name] | [1-2 sentence description] | $[X] |
| 2 | [Deliverable Name] | [1-2 sentence description] | $[X] |
| 3 | [Deliverable Name] | [1-2 sentence description] | $[X] |
| 4 | [Deliverable Name] | [1-2 sentence description] | $[X] |
| | **Core Offer Subtotal** | | **$[X]** |

---

## Bonuses (Included Free)

| # | Bonus | What It Solves | Value |
|---|-------|---------------|-------|
| 🎁 | **[Bonus Name]** | [Objection it addresses — 1-2 sentences] | $[X] |
| 🎁 | **[Bonus Name]** | [Objection it addresses] | $[X] |
| 🎁 | **[Bonus Name]** | [Objection it addresses] | $[X] |
| | **Bonus Subtotal** | | **$[X]** |

---

## The Math

| | |
|---|---|
| Core Offer Value | $[X] |
| Bonus Value | $[X] |
| **Total Value** | **$[Total]** |
| **Your Price** | **$[Price]** |
| **You Save** | **$[Savings]** |

---

## Sales Page Copy (Ready to Use)

### Everything You Get:

**[Deliverable 1]** (Value: $[X])
[What it is and why it matters — 2-3 sentences]

**[Deliverable 2]** (Value: $[X])
[Description]

[Continue for all deliverables...]

**PLUS these bonuses when you join today:**

🎁 **[Bonus 1]** (Value: $[X])
[Description and what objection it removes]

🎁 **[Bonus 2]** (Value: $[X])
[Description]

🎁 **[Bonus 3]** (Value: $[X])
[Description]

**Total value: $[Total]**
**Your investment: $[Price]**

[CTA Button]
```

## Quality Checklist

- [ ] Every deliverable has a compelling name (not "Module 1")
- [ ] Individual values are credible (not absurdly inflated)
- [ ] 3-5 bonuses that address specific objections
- [ ] Total value is 5-10x the price
- [ ] Each bonus solves a real barrier to purchase
- [ ] Sales page copy section is ready to use
- [ ] Math adds up correctly
- [ ] Voice matches context profiles
- [ ] No fabricated testimonials or results in descriptions
- [ ] Value assignments are defensible (comparable products/services exist)
