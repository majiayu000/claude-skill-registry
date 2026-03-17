---
name: prd-v02-product-type-classification
description: Classify product approach into one of six types (Clone, Unbundle, Undercut, Slice, Wrapper, Innovation) based on competitive landscape. Triggers on PRD v0.2 work after competitive analysis, or when user asks "what type of product should we build?", "should we clone or innovate?", "is this a fast-follow opportunity?", "how should we position against competitors?", "clone vs undercut", "unbundle vs slice", or requests help choosing product strategy. Outputs BR- entries for product type classification and inherited GTM constraints.
---

# Product Type Classification

Position in HORIZON workflow: v0.2 Competitive Landscape → **v0.2 Product Type Classification** → v0.3 Outcome Definition

## Six Product Types

| Type | Definition | When Evidence Shows |
|------|------------|---------------------|
| **Clone** | Copy proven product, execute better | Leader validated market; weak moat; execution gap |
| **Unbundle** | Extract one category from horizontal platform | Multi-category platform does your thing poorly |
| **Undercut** | Same product, simpler + cheaper for niche | Tool overserves broad market; 60%+ price gap possible |
| **Slice** | Plugin/extension in existing ecosystem | Platform has marketplace; users already there |
| **Wrapper** | AI/API layer on existing data/tools | Middleware gap between tools; data accessible |
| **Innovation** | New solution to known problem | Existing approaches fundamentally broken; high pain |

## Classification Decision Flow

```
START: What does v0.2 Competitive Landscape show?

Q1: Is there a dominant horizontal platform doing many things?
    YES → Does it do YOUR thing poorly? 
          YES → UNBUNDLE (extract the vertical)
          NO → Continue to Q2
    NO → Continue to Q2

Q2: Is there a single-purpose leader with validated market?
    YES → Can you price 60%+ lower for a niche?
          YES → UNDERCUT
          NO → Can you execute better (speed/UX)?
                YES → CLONE
                NO → Continue to Q3
    NO → Continue to Q3

Q3: Does target customer live in a platform ecosystem?
    YES → Does platform have marketplace/app store?
          YES → SLICE (build extension)
          NO → Continue to Q4
    NO → Continue to Q4

Q4: Is there a data/API integration gap between tools?
    YES → Is the data accessible (API/scraping)?
          YES → WRAPPER
          NO → Continue to Q5
    NO → Continue to Q5

Q5: Are existing solutions fundamentally broken?
    YES → Is pain severe enough for education investment?
          YES → INNOVATION
          NO → Reconsider market
    NO → Reconsider market or revisit Q1-Q4
```

## Evidence Requirements Per Type

| Type | Required Evidence (from v0.2 Landscape) | Confidence Threshold |
|------|----------------------------------------|---------------------|
| Clone | Revenue proof + feature gap + weak moat | Medium (50%+) |
| Unbundle | Platform size + category neglect + user complaints | Medium (50%+) |
| Undercut | Price benchmarks + niche pain + simplification path | High (70%+) |
| Slice | Platform MAU + marketplace presence + integration docs | High (70%+) |
| Wrapper | API availability + use case validation + cost model | High (70%+) |
| Innovation | Failed alternatives + severe pain + budget evidence | Very High (85%+) |

## Output Template

After classification, create these entries:

**BR-XXX: Product Type Classification**
```
Type: [Clone | Unbundle | Undercut | Slice | Wrapper | Innovation]
Confidence: [X]%
Primary Evidence: [CFD-XXX reference]
Classification Rationale: [2-3 sentences]
```

**BR-XXX: GTM Constraints (inherited from type)**
```
Pricing Constraint: [See references/gtm-constraints.md]
Channel Constraint: [See references/gtm-constraints.md]
Scope Constraint: [See references/gtm-constraints.md]
Timeline Implication: [See references/gtm-constraints.md]
```

## Anti-Patterns to Avoid

1. **Claiming Innovation when it's really Clone**: If competitor exists with revenue, you're not innovating
2. **Undercut without price evidence**: Must show 60%+ reduction is possible AND sustainable
3. **Slice without ecosystem validation**: Platform must actually want third-party apps
4. **Wrapper without API access confirmed**: Technical feasibility must precede classification
5. **Unbundle from small platform**: Only works against large horizontal players

## Reference Files

- **Decision Framework**: See `references/decision-framework.md` for expanded decision trees
- **Examples**: See `references/examples.md` for good/bad classification cases
- **GTM Constraints**: See `references/gtm-constraints.md` for type → constraint mapping
- **Classification Template**: See `assets/classification.md` for structured worksheet

## Downstream Impact

Classification constrains v0.3 decisions:
- **Outcome metrics** must match type (Clone = feature parity; Undercut = price advantage)
- **Pricing model** anchored to type (Undercut must show savings; Slice follows platform norms)
- **MVP scope** bounded by type (Clone = match leader; Undercut = ruthlessly cut features)
- **GTM channel** determined by type (Slice = marketplace; Undercut = direct to niche)
