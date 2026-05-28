---
description: Analyze a company to identify their Ideal Customer Profiles (ICPs) - buyer personas, verticals, and tiers
---

# ICP Analysis

Use this skill when: user asks to "analyze ICPs", "identify target customers", "who should [company] sell to", or any request to understand buyer profiles for a business.

---

## Input Gathering

Before analyzing, collect:

1. **Company name** (required)
2. **Website** (required - primary research source)
3. **Product/service description** (optional - will research if not provided)
4. **Existing customers** (optional - helpful for pattern recognition)

If the user doesn't provide website or description, use web search to find the company first.

---

## Research Phase

### Step 1: Website Analysis

Fetch the company website and extract:

- **Products/Services**: What exactly do they sell?
- **Value proposition**: What problem do they solve?
- **Pricing signals**: Enterprise, SMB, consumer?
- **Case studies/testimonials**: Who are their current customers?
- **Industries mentioned**: What verticals do they serve?
- **Company sizes**: Startup, mid-market, enterprise?
- **Job titles**: Who do they market to?

### Step 2: Market Context

Search for:

- Competitors and their customers
- Industry reports or analyses
- Reviews and customer mentions
- LinkedIn company page (employee count, industry)

### Step 3: Pattern Recognition

Look for signals:

- **Direct fit**: Companies that obviously need this product
- **Adjacent fit**: Companies with similar needs but different context
- **Expansion opportunities**: New markets or use cases
- **Anti-patterns**: Who would NOT be a good fit

---

## ICP Framework

### Determining Number of Tiers

The number of tiers should match the business reality. DO NOT default to 4 tiers—analyze the situation first.

| Business Type | Typical Tiers | Why |
|--------------|---------------|-----|
| Niche B2B tool | 2-3 | Narrow focus, clear fit/no-fit |
| Horizontal SaaS | 3-4 | Multiple segments, similar needs |
| Enterprise platform | 4-5 | Complex buying, many personas |
| Marketplace/platform | 3-5 | Supply + demand sides |
| Consumer product | 2-3 | Demographics-based, simpler |
| Professional services | 2-4 | Relationship-driven |

**Questions to determine tier count:**

1. **How many distinct buying personas exist?** (Each major persona type = potential tier)
2. **How different are sales cycles?** (If cycles vary 3x+, likely need separate tiers)
3. **Are there natural market segments?** (Industry, size, geography, use case)
4. **What's the product complexity?** (Simple = fewer tiers, complex = more)
5. **How wide is the TAM?** (Narrow = 2-3 tiers, broad = 4+)

### Tier Template

For EACH tier you create, define:

**Tier [N]: [Descriptive Name] ([Priority Level])**

- **Profile**: Who are they? (size, industry, stage, characteristics)
- **Need intensity**: Immediate/strong/moderate/emerging
- **Buying behavior**: Self-serve, sales-assisted, enterprise sale
- **Sales cycle**: Days/weeks/months
- **Success indicators**: What signals a good fit?
- **Decision makers**: Titles to target

### Example Tier Structures

**2-Tier Example (Developer Tool):**
- **Tier 1: Individual Developers** — Self-serve, immediate need, low friction
- **Tier 2: Engineering Teams** — Sales-assisted, team licenses, longer cycle

**3-Tier Example (Marketing SaaS):**
- **Tier 1: Growth-Stage Startups** — Immediate need, fast decision, price-sensitive
- **Tier 2: Mid-Market Companies** — Strong need, committee buying, budget available
- **Tier 3: Enterprise** — Strategic deals, long cycle, high value

**5-Tier Example (Enterprise Platform):**
- **Tier 1: Innovation Leaders** — Early adopters, direct fit, fast cycle
- **Tier 2: Fast Followers** — Proven ROI needed, strong fit
- **Tier 3: Industry Specialists** — Vertical-specific needs, customization required
- **Tier 4: Cost Optimizers** — Replace existing solution, price-driven
- **Tier 5: Strategic Partnerships** — Platform/integration deals, complex

### Priority Mapping

| Priority | Score Range | Characteristics |
|----------|-------------|-----------------|
| Highest | 4-5 | Immediate need, direct fit, accessible |
| High | 3-4 | Strong fit, some friction |
| Medium | 2-3 | Good fit, requires nurturing |
| Lower | 1-2 | Future potential, long-term |
| Experimental | 0-1 | Unproven, exploration only |

*Note: Not all tiers need to exist for every business. Use only what makes sense.*

---

## Exclusion Criteria

Define who NOT to target:

### Automatic Exclusions

| Category | Why Exclude |
|----------|-------------|
| Wrong industry | No product fit |
| Wrong size | Below/above ideal customer size |
| Wrong geography | Can't serve their market |
| Wrong stage | Too early/late for their needs |
| Competitors | Conflict of interest |
| DIY solutions | Build vs buy preference |

### Exclusion Keywords

List specific keywords/patterns that indicate non-fit:
- Industry terms that suggest wrong vertical
- Company name patterns (e.g., "consulting" if selling to product companies)
- Product categories that don't overlap

---

## Scoring System (0-5)

| Score | Definition | Criteria |
|-------|------------|----------|
| **5** | Hot Lead | Direct fit + buying signals + contact available |
| **4** | High Priority | Strong fit + clear need + reachable |
| **3** | Standard | Good fit + some indicators |
| **2** | Low Priority | Uncertain fit OR missing info |
| **1** | Minimal | Weak connection, keep for reference |
| **0** | Exclude | No fit OR can't reach |

### Scoring Modifiers

| Modifier | Score Impact |
|----------|--------------|
| Recent funding | +1 |
| Hiring for relevant roles | +1 |
| Competitor customer (churn opportunity) | +1 |
| Direct contact available | +1 |
| No website or contact info | -1 |
| Generic email only (info@) | -0.5 |

---

## Decision-Maker Titles

For each tier, identify relevant titles to target:

### Executive (strategic deals)
- CEO, Founder, President, Owner
- CTO, CIO, COO, CFO
- VP of [relevant function]

### Manager (operational deals)
- Director of [function]
- Head of [function]
- [Function] Manager

### Practitioner (bottoms-up adoption)
- Senior [role]
- Lead [role]
- [Function] Specialist

---

## Output Formats

### Option 1: Methodology Document

Generate a markdown document like:

```markdown
# ICP Methodology for [Company]

## Overview
[Brief description of the company and their product]

## Why [N] Tiers
[Explain the reasoning for the chosen number of tiers based on business model, sales motion, and market structure]

## Tier Definitions

### Tier 1: [Name] ([Priority Level])
**Score Range: [X-Y]**

[Description of who belongs here]

| Criteria | Examples |
|----------|----------|
| [Signal 1] | [Company types] |
| [Signal 2] | [Company types] |

**Why This Tier:** [Business rationale]
**Sales Motion:** [Self-serve / Sales-assisted / Enterprise]
**Decision Makers:** [Titles to target]

### Tier 2: [Name] ([Priority Level])
...

[Continue for each tier - may be 2, 3, 4, 5, or more]

## Exclusion Criteria
[Categories and keywords to skip]

## Scoring System
[Customized scoring with modifiers]

## Enrichment Priority
[Which tiers to enrich first and what to look for]
```

### Option 2: Structured Data

Output as structured data for CSV import:

```csv
tier,tier_name,description,criteria,examples,decision_makers,priority_score_range
1,Direct_Buyers,Companies with immediate need,[criteria],[examples],[titles],4-5
2,Strong_Fit,Adjacent use cases,[criteria],[examples],[titles],3-4
...
```

### Option 3: Both

Generate methodology doc AND structured data.

---

## Quality Checklist

Before delivering:

- [ ] Tier count justified (explained why 2, 3, 4, or more)
- [ ] Each tier has clear, distinct criteria (no overlap)
- [ ] Exclusion criteria are specific (not generic)
- [ ] Scoring modifiers are relevant to this business
- [ ] Decision-maker titles match the buying process
- [ ] Examples are concrete, not theoretical
- [ ] Output format matches what user requested

---

## Example Analyses

### Example 1: Developer CLI Tool (2 Tiers)

Why 2 tiers: Simple product, binary fit (devs use it or don't), self-serve model.

**Tier 1: Power Users** — Individual developers already using similar tools, active on GitHub, blog about tooling
**Tier 2: Team Adoption** — Engineering teams at companies >20 devs, standardizing toolchain

**Exclusions**: Non-technical roles, companies without engineering teams

---

### Example 2: B2B SaaS Project Management (3 Tiers)

Why 3 tiers: Clear market segments by company size, different sales motions.

**Tier 1: Growth Startups** — VC-backed (50-200 employees), scaling fast, modern stack, hiring PMs
**Tier 2: Mid-Market** — Established companies (200-1000), consolidating tools, budget approved
**Tier 3: Enterprise** — Large orgs (1000+), complex procurement, long cycle, high ACV

**Exclusions**: Solo consultants, <20 employees, specialized industries (construction, film)

---

### Example 3: Enterprise Data Platform (5 Tiers)

Why 5 tiers: Complex product, multiple buyer types, varying use cases, long sales cycles.

**Tier 1: Data-First Companies** — Tech companies with dedicated data teams, immediate need
**Tier 2: Digital Transformers** — Traditional companies modernizing, strong executive buy-in
**Tier 3: Regulated Industries** — Finance/healthcare with compliance needs, specific requirements
**Tier 4: Cost Consolidators** — Companies replacing legacy tools, price-sensitive
**Tier 5: Platform Partners** — ISVs/consultancies building on the platform

**Exclusions**: Companies <$10M revenue, no data team, industries we can't serve (defense)

---

*This skill adapts to any business model. Let the customer's reality dictate the tier structure.*
