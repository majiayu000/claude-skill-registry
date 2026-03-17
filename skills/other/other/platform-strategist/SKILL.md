---
name: platform-strategist
type: domain
family: executive
rigor: standard
description: "Use when analyzing platform business models, network effects, or aggregation dynamics."
keywords: "platform, business-model, network-effects, aggregation, strategy, architecture"
compatibility: "Claude Code and compatible agent products"
requires: []
enhances: ["strategy-clarity", "market-context", "operational-excellence"]
sources_pdf: ["Zero to One (Thiel)", "High Growth Handbook (Gil)", "Working Backwards (Bryar)", "Working in Public (Eghbal)"]
sources_web: ["Stratechery: The Bill Gates Line", "Stratechery: Shopify & Platforms", "Stratechery: The Amazon Tax"]
---

## Overview

Platform strategy is the art of building foundational systems that facilitate value creation by third parties. This skill distinguishes between "Aggregators" (who own the user relationship) and "Platforms" (who empower an ecosystem), focusing on network effects, economies of scale, and the externalization of internal "primitives" as a growth engine.

## Guiding Principles

### Principle 1: The Bill Gates Line (Source: Stratechery, "The Bill Gates Line")
A true platform's value is defined by the economic value created by third parties *exceeding* the value of the platform itself. If you capture all the value, you aren't a platform; you're a vertical silo.

### Principle 2: Empower, Don't Intermediate (Source: Stratechery, "Shopify & Platforms")
A platform wins by enabling its suppliers to differentiate themselves and acquire their own customers. Aggregators commoditize supply; Platforms empower supply. (Example: Shopify vs. Amazon Marketplace).

### Principle 3: Externalize the Primitives (Source: Stratechery, "The Amazon Tax")
Identify the fundamental "building blocks" of your business (storage, compute, logistics, payments). Design them as modular APIs (primitives) so they can be used internally and then externalized to the market. (Source: Bryar, *Working Backwards*).

### Principle 4: Network Effects & The Niche (Source: Thiel, *Zero to One*)
Platform value scales with network density. To avoid the "chicken and egg" problem, start by monopolizing a small, high-intensity niche (e.g., Harvard for Facebook) before expanding to the broader market.

### Principle 5: The Marketplace Subsidy (Source: Gil, *High Growth Handbook*)
In a two-sided platform, one side is usually harder to acquire. Identify which side (supply or demand) is the "limiting step" and subsidize them to create the initial liquidity required for network effects to take hold.

## When to Use This Skill

- When evaluating whether a business model is structurally a "Platform" or an "Aggregator."
- When designing APIs or developer ecosystems.
- When planning the expansion from a product-centric business to a platform-centric one.
- When identifying potential "Network Effects" in a new category.

## When NOT to Use This Skill

- For pure B2B service businesses that don't scale through third-party value creation.
- For niche products where network effects are non-existent or irrelevant to the value prop.

## Core Process

### Step 1: Identify the Ecosystem Role
Determine if the strategic goal is to be a Platform or an Aggregator. (Source: Stratechery, "The Bill Gates Line")
1. **The Aggregator Path:** Own the user experience, commoditize supply, capture high rent.
2. **The Platform Path:** Provide the stage for third-party apps, empower suppliers, capture a "tax" on ecosystem growth.

### Step 2: Map the Flywheel
Identify the reinforcing loops that drive platform growth. (Source: Bryar, Ch. 1)
1. **Direct Network Effects:** Does more users → more value for users?
2. **Indirect Network Effects:** Does more supply → more value for users (and vice versa)?
3. **Data Network Effects:** Does more usage → better product → more users?

### Step 3: Define the Primitives (Service-Oriented Architecture)
Audit internal infrastructure for platform potential. (Source: Stratechery, "The Amazon Tax")
1. **Modularize:** Can this internal function be separated into a stand-alone service?
2. **API-First:** Is it accessible via a clean interface?
3. **Self-Service:** Can someone use it without human intervention from your team?

### Step 4: Solve the Liquidity Problem (The Cold Start)
Design the entry strategy to overcome the "chicken and egg" problem. (Source: Gil, Ch. 8)
1. **Niche Monopoly:** Monopolize a small sub-market where the platform is useful with only a few participants. (Source: Thiel, Ch. 5)
2. **Side-Switching:** Can users also be suppliers (e.g., Airbnb, Uber)?
3. **The Subsidy:** Which side should we pay or provide for free to attract the other?

### Step 5: Establish Platform Governance
Set the rules for participation to prevent ecosystem decay. (Source: Gil, Ch. 8)
1. **Quality Standards:** How do we filter "bad" supply?
2. **Taxation:** What is our "cut"? Is it low enough to encourage growth but high enough to sustain the platform?
3. **Interoperability:** How easily can third parties build on and leave the platform?

## Frameworks & Models

### Platform vs. Aggregator Matrix (Source: Stratechery)
- **Aggregator:** Owns User → Controls Supply → Modularizes Suppliers. (Focus: UX)
- **Platform:** Owns Foundation → Empowers Supply → Facilitates User-Supplier Relationship. (Focus: Infrastructure)

### The 10x Technology Audit (Source: Thiel, *Zero to One*)
A platform must be 10x better in at least one dimension to trigger a platform shift:
1. **Efficiency:** Is it 10x cheaper/faster? (AWS)
2. **UX:** Is it 10x easier to use? (iPhone)
3. **Availability:** Does it provide 10x more selection? (Amazon Retail)

## Cross-Skill Invocations

- **REQUIRED SUB-SKILL:** `strategy-clarity` — To ensure the platform model aligns with the "Winning Aspiration."
- **RECOMMENDED SUB-SKILL:** `market-context` — To identify structural shifts (Aggregation/Unbundling).
- **RECOMMENDED SUB-SKILL:** `operational-excellence` — To build the "Mechanisms" for platform governance.

## Common Mistakes

1. **The Rent-Seeking Trap:** Raising platform taxes too early, killing the ecosystem before it reaches critical mass. (Source: Stratechery, "The Bill Gates Line")
2. **Ignoring the Cold Start:** Trying to launch a platform to everyone at once instead of a small niche. (Source: Thiel, Ch. 5)
3. **Confusing Product for Platform:** Thinking that "having an API" makes you a platform. If nobody builds on it, it's just a product feature.
4. **Weak Governance:** Allowing low-quality supply to overwhelm the platform, destroying user trust. (Source: Gil, Ch. 8)

## Diagnostic Checklist

- [ ] Does the economic value created by third parties exceed the value of our company?
- [ ] Have we identified the "Primitives" that can be externalized?
- [ ] Is there a clear "Flywheel" of direct or indirect network effects?
- [ ] Are we monopolizing a small niche to solve the "Cold Start" problem?
- [ ] Is our governance (rules/taxes) designed to encourage long-term ecosystem growth?

## Sources

- Thiel, *Zero to One*, Ch. 5 — Network Effects, Economies of Scale, 10x Tech.
- Gil, *High Growth Handbook*, Ch. 8 — Marketplaces, Governance, Liquidity.
- Bryar & Carr, *Working Backwards*, Ch. 1 — AWS origin, Flywheels, APIs.
- Stratechery, "The Bill Gates Line" & "Shopify & Platforms" — Defining the platform role.
- Stratechery, "The Amazon Tax" — Externalizing internal primitives.
