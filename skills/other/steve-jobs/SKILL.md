---
name: steve-jobs
description: >-
  Experience-first product planning with ruthless focus. Start from the customer
  experience, say no to good ideas, enforce a Top-10 list, assign DRIs, ship real
  increments. Use when: (1) planning a product or feature roadmap, (2) prioritizing
  with scope discipline, (3) grounding UX decisions in user outcomes, (4) cutting
  scope to ship, (5) assigning ownership and accountability.
category: principles
---

# Steve Jobs

Start with the customer experience. Work backward to the technology. Focus equals saying no.

## Operating Principles

1. Start with the customer experience and work backward to the technology.
2. Focus equals saying no to many good ideas. Keep a visible "Not Doing" list.
3. If the portfolio is not legible, cut until it is.
4. Constrain priorities so the A-team can cover what matters.
5. Design is how it works (behavior, states, recovery), not surface decoration.
6. Own the complete user experience. If it is bad, it is your fault.
7. One DRI per committed item. Several owners means no owner.
8. Keep teams scrappy. Fight bureaucracy with clarity and accountability.
9. Ship real increments. Defer polish by cutting scope, not by shipping sloppy.
10. Integrate key layers when the UX depends on it. Own the seams.

## Planning Workflow

### Step A: Experience-First Brief

One page maximum:

| Field | Content |
|-------|---------|
| Primary user | Who benefits |
| Primary task | One sentence |
| Incredible benefit | User language, not features |
| First-success moment | What the user sees or gets |
| Failure and recovery | Top 3 failure modes |
| Not doing | Explicit exclusions |
| Demo definition | What you can show in 2 minutes |

### Step B: Candidate List

List initiatives in plain language. No solutioning yet. For each: expected benefit, who benefits, what it replaces.

### Step C: Ruthless Cuts

For each item, answer:

- Does it materially improve the core experience from Step A?
- Does it fit the cohesive product vision?
- Can we ship a coherent increment in 1-2 cycles if we cut scope?

If any answer is no: move to NOT DOING or LATER with a rationale.

### Step D: Top-10 Enforcement

- Produce a Top-10 list maximum.
- If you have more than 10, you are not prioritizing.
- Everything not in the Top-10 is explicitly deprioritized.

### Step E: Assign Ownership

- Exactly one DRI for each Top-10 item.
- DRIs define the demo, acceptance checks, and success metrics.

### Step F: Ship Plan

For each top item:

| Field | Content |
|-------|---------|
| Shippable increment | Smallest coherent release |
| Acceptance criteria | Including recovery |
| Metrics | Leading and lagging |
| Trade-offs | What was cut to make it shippable |

### Step G: Post-Ship Review

- Did the experience improve? Measure.
- If not: iterate or kill quickly. Do not linger in zombie mode.

## Agent Operating Mode

When invoked, produce in order:

1. Experience-First Brief (filled)
2. Top-10 list and Not Doing list (with reasons)
3. DRI assignment list
4. Ship plan for top items (increment, acceptance, metrics)
5. Trade-off ledger (what got cut and why)

## Anti-Patterns

| Pattern | Problem |
|---------|---------|
| Tech-first roadmap | Starts with capabilities, ends with hand-wavy users |
| 18 directions | Lots of projects, no integrated outcome |
| Consensus ownership | Multiple owners, no DRI |
| Feature hoarding | Refusing to cut creates an incoherent product |
| Shipping theatre | "Almost done" work that never reaches users |

Flag these immediately when detected.

## Metrics (Pick Only a Few)

**Experience:** Time-to-first-success, task completion rate, recovery success rate.

**Focus:** Number of concurrent top priorities, percent capacity on top priorities.

**Shipping:** Release cadence, rollback rate, severe defect rate post-ship.

**Accountability:** Percent committed items with a DRI, cycle time variance.

## Checklist

- [ ] Can we state the customer benefit without listing features?
- [ ] What are we explicitly not doing, and why?
- [ ] Is the portfolio legible to customers and frontline teams?
- [ ] Is the Top-10 list enforced with a real cut line?
- [ ] Does every top item have one DRI?
- [ ] Is there a demo definition and a ship definition?
- [ ] Do we own the end-to-end experience, including recovery?

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "We can do all of them" | You cannot. Spreading thin kills quality. | Cut to Top-10 |
| "We need more research first" | Start from the experience, not the technology | Write the brief |
| "Nobody owns this, it's a team effort" | No DRI means no accountability | Assign one person |
| "We'll polish it later" | Later means zombie mode | Cut scope to ship clean |
| "The technology drives the roadmap" | Experience drives the roadmap | Work backward from the user |
| "We can't cut that, stakeholders want it" | Focus equals saying no | Move to Not Doing with rationale |

## Chaining

- **linus-torvalds**: Complementary. Steve-jobs focuses on product-level prioritization and UX. Linus-torvalds focuses on engineering-level regression discipline and compatibility.
- **bryan-cantrill**: Steve-jobs produces the experience brief. Bryan-cantrill produces the written engineering design that implements it.
- **rick-rubin**: Scope discipline at the diff level. Steve-jobs enforces scope at the product level (Top-10 gate).
- **elon-musk**: Both delete aggressively. Steve-jobs cuts features for focus. Elon-musk cuts code for simplicity.
