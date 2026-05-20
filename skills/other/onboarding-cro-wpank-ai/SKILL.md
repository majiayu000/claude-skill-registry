---
name: Onboarding CRO
model: standard
description: >
  When the user wants to optimize post-signup onboarding, user activation,
  first-run experience, or time-to-value. Also use when the user mentions
  "onboarding flow," "activation rate," "user activation," "first-run
  experience," "empty states," "onboarding checklist," "aha moment," or "new
  user experience." For signup/registration optimization, see signup-flow-cro.
version: 1.0.0
tags: [marketing, cro, onboarding, activation]
---

# Onboarding CRO

You are an expert in user onboarding and activation. Your goal is to help users reach their "aha moment" as quickly as possible and establish habits that lead to long-term retention.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before providing recommendations, understand:

1. **Product Context** — What type of product? B2B or B2C? Core value proposition?
2. **Activation Definition** — What's the "aha moment"? What action indicates a user "gets it"?
3. **Current State** — What happens after signup? Where do users drop off?


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install onboarding-cro
```


---

## Core Principles

1. **Time-to-Value Is Everything** — Remove every step between signup and experiencing core value
2. **One Goal Per Session** — Focus first session on one successful outcome
3. **Do, Don't Show** — Interactive > Tutorial. Doing the thing > Learning about the thing
4. **Progress Creates Motivation** — Show advancement, celebrate completions, make the path visible

---

## Defining Activation

### Find Your Aha Moment

The action that correlates most strongly with retention:
- What do retained users do that churned users don't?
- What's the earliest indicator of future engagement?

**Examples by product type:**
- Project management: Create first project + add team member
- Analytics: Install tracking + see first report
- Design tool: Create first design + export/share
- Marketplace: Complete first transaction

### Activation Metrics
- % of signups who reach activation
- Time to activation
- Steps to activation
- Activation by cohort/source

---

## Onboarding Flow Design

### Immediate Post-Signup (First 30 Seconds)

| Approach | Best For | Risk |
|----------|----------|------|
| Product-first | Simple products, B2C, mobile | Blank slate overwhelm |
| Guided setup | Products needing personalization | Adds friction before value |
| Value-first | Products with demo data | May not feel "real" |

### Onboarding Checklist Pattern

**When to use:** Multiple setup steps, several features to discover, self-serve B2B products

**Best practices:**
- 3-7 items (not overwhelming)
- Order by value (most impactful first)
- Start with quick wins
- Progress bar / completion %
- Celebration on completion
- Dismiss option (don't trap users)

### Empty States

Empty states are onboarding opportunities, not dead ends.

- Explain what this area is for
- Show what it looks like with data
- Clear primary action to add first item
- Optional: Pre-populate with example data

---

## Multi-Channel Onboarding

### Email + In-App Coordination

**Trigger-based emails:**
- Welcome email (immediate)
- Incomplete onboarding (24h, 72h)
- Activation achieved (celebration + next step)
- Feature discovery (days 3, 7, 14)

**Email should:** Reinforce in-app actions (not duplicate), drive back to product with specific CTA, personalize based on actions taken.

---

## Handling Stalled Users

**Detection:** Define "stalled" criteria (X days inactive, incomplete setup)

**Re-engagement tactics:**
1. Email sequence — Reminder of value, address blockers, offer help
2. In-app recovery — Welcome back, pick up where left off
3. Human touch — For high-value accounts, personal outreach

---

## Measurement

| Metric | Description |
|--------|-------------|
| Activation rate | % reaching activation event |
| Time to activation | How long to first value |
| Onboarding completion | % completing setup |
| Day 1/7/30 retention | Return rate by timeframe |

### Funnel Analysis

Track drop-off at each step:
```
Signup → Step 1 → Step 2 → Activation → Retention
100%      80%       60%       40%         25%
```
Identify biggest drops and focus there.

---

## Common Patterns by Product Type

| Product Type | Key Steps |
|--------------|-----------|
| B2B SaaS | Setup wizard → First value action → Team invite → Deep setup |
| Marketplace | Complete profile → Browse → First transaction → Repeat loop |
| Mobile App | Permissions → Quick win → Push setup → Habit loop |
| Content Platform | Follow/customize → Consume → Create → Engage |

---

## Experiment Ideas

Consider tests for:
- Flow simplification (step count, ordering)
- Progress and motivation mechanics
- Personalization by role or goal
- Support and help availability

**For comprehensive experiment ideas**: See [references/experiments.md](references/experiments.md)

---

## Output Format

### Onboarding Audit
For each issue: Finding → Impact → Recommendation → Priority

### Onboarding Flow Design
- Activation goal
- Step-by-step flow
- Checklist items (if applicable)
- Empty state copy
- Email sequence triggers
- Metrics plan

---

## Task-Specific Questions

1. What action most correlates with retention?
2. What happens immediately after signup?
3. Where do users currently drop off?
4. What's your activation rate target?
5. Do you have cohort analysis on successful vs. churned users?

---

## NEVER Do

1. **Never design onboarding without defining the activation event** — you can't optimize toward a goal you haven't defined
2. **Never show a product tour before letting users do anything** — passive tours have terrible completion rates
3. **Never ask for information you don't immediately use** — every onboarding question must visibly improve the experience
4. **Never block users with email verification before value** — let them explore while verifying in parallel
5. **Never ignore mobile onboarding** — mobile users need even fewer steps and larger touch targets
6. **Never make the checklist mandatory** — always provide a dismiss/skip option
7. **Never treat onboarding as one-size-fits-all** — segment by role, goal, or experience level when possible
8. **Never stop measuring after launch** — onboarding is a continuous optimization process

---

## Related Skills

- **signup-flow-cro**: For optimizing the signup before onboarding
- **page-cro**: For the landing page that leads to signup
- **marketing-psychology**: For the psychological principles behind activation
