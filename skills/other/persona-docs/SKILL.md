---
name: persona-docs
model: reasoning
version: 1.0.0
description: >
  Create persona documentation for a product or codebase. Use when asked to create persona docs,
  document target users, define user journeys, document onboarding flows, or when starting a new
  product and needing to define its audience. Persona docs should be the first documentation
  created for any product.
tags: [personas, user-research, product, documentation, onboarding, user-journey]
---

# Persona Docs

Create user-centered documentation that defines who a product is for and how they interact with it. Persona docs establish the foundation for product-driven development — every feature decision, design choice, and prioritization call flows from understanding your users.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install persona-docs
```


## When to Create

Persona docs should be the first thing fleshed out for any product. Even minimal documentation about who uses the product helps direct development and design decisions.

- **Project inception** — before writing code, define who you're building for
- **Pivoting to a new audience** — document the shift so the team aligns
- **Team lacks clarity on target users** — when people disagree on "who is this for?"
- **Before major feature planning** — validate that planned features serve actual users
- **New team member onboarding** — give them context on who they're building for

## Process

1. **Analyze the codebase** — look for existing documentation, README, landing pages, or marketing copy that hints at the target audience
2. **Ask clarifying questions** if the target user isn't clear:
   - "Who is the primary user of this product?"
   - "What problem does this solve for them?"
   - "How would they discover this product?"
   - "What's the first thing they'd do after finding it?"
3. **Start minimal** — a few sentences per section is better than nothing
4. **Read the template** — see `references/template.md` for the full structure
5. **Iterate** — revisit and expand as you learn more about actual users

## Core Components

### 1. Target User Profile

Who they are, their background, their context. Be specific enough to be useful.

**Good:** "Backend engineers at mid-size SaaS companies who debug production issues under time pressure, typically 3-8 years of experience, comfortable with command-line tools."

**Too vague:** "Developers."

Include:
- Role, job title, or archetype
- Technical level and relevant skills
- Industry or domain context
- When and where they'd use this product
- Team size and organizational context

### 2. User Needs and Pain Points

The problems this product solves. What frustrations or gaps exist in their current workflow?

Structure as:
- **Primary pain point** — the single biggest problem you solve
- **Secondary pain points** — additional problems you address
- **Current workarounds** — what they do today without your product
- **Why existing solutions fail** — what alternatives exist and why they're insufficient

### 3. Discovery Path

How they find the product. This informs marketing, positioning, and first-impression design.

- **Search** — what queries lead them here?
- **Referral** — word of mouth, colleague recommendation?
- **Content** — blog posts, tutorials, conference talks?
- **Marketplace** — app store, plugin directory, package registry?
- **The hook** — what makes them click "sign up" or "download"?

### 4. Onboarding Flow

The simplest possible path from "I found this" to "I'm getting value."

Define:
- **First encounter** — landing page, app store listing, GitHub README
- **Registration/Login** — minimum viable auth (email-only? OAuth? no account?)
- **Time to value** — how quickly can they experience the core benefit?
- **First success moment** — the specific action that makes them think "this is useful"
- **Friction points** — where do users drop off, and how do you minimize that?

Example flow:
> User lands on homepage → clicks "Try it" → pastes their data → sees result in <30 seconds → decides to create account

### 5. User Journey Map

Key touchpoints and interactions across the user lifecycle.

**New User (Day 1):**
- Discovers product via [channel]
- Takes [first action]
- Achieves [first success]

**Returning User (Week 1):**
- Key repeated action they perform
- Features they explore
- Integrations or customizations they set up

**Power User (Month 1+):**
- Advanced features they rely on
- Workflows they've established
- How they'd describe the product to others

### 6. Feature Touchpoints

Map where users encounter key features in their journey:

| Feature | When Encountered | User Need at That Moment |
|---------|------------------|--------------------------|
| [Feature 1] | [Journey stage] | [What they're trying to do] |
| [Feature 2] | [Journey stage] | [What they're trying to do] |

## Multi-Persona Products

If your product serves multiple distinct user types:

1. **Identify the primary persona first** — who must you serve to survive?
2. **Document secondary personas separately** — one file per persona
3. **Note conflicts** — where persona needs clash, document the tradeoff
4. **Prioritize ruthlessly** — you can't optimize for everyone simultaneously

## Output Location

Place persona docs at:
- `docs/PERSONA.md` — single file for simple products
- `docs/personas/` — directory for multiple personas

Keep it in the repo so it evolves with the product.

## Quality Criteria

A good persona doc should:

- Be **specific** enough that two team members would build the same feature from it
- Include **evidence** — data, quotes, or observations, not just assumptions
- Be **actionable** — reading it should change how you build
- Be **maintained** — outdated personas are worse than none
- Be **honest** — don't describe aspirational users; describe actual users

## NEVER Do

1. **NEVER skip personas for a new product** — building without knowing your user is guessing, and guessing is expensive
2. **NEVER describe users as demographics alone** — "25-34 male" tells you nothing about what they need; describe behaviors and goals
3. **NEVER create personas in isolation** — involve the team; one person's assumptions become the whole product's blind spots
4. **NEVER treat personas as permanent** — users change, markets shift; review personas quarterly
5. **NEVER create more than 3 personas initially** — if you try to serve everyone, you serve no one; start with your primary user
6. **NEVER write aspirational personas** — document who actually uses your product, not who you wish did
