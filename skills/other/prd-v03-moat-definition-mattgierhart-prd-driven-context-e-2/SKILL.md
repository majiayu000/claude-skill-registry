---
name: prd-v03-moat-definition
description: Assess competitor defensibility and define our own moat strategy during PRD v0.3 Commercial Model. Triggers on requests to analyze competitor moats, define our defensibility, assess switching costs, identify vulnerabilities, find wedge opportunities, or when user asks "what's our moat?", "how defensible are they?", "where can we compete?", "switching costs?", "defensibility", "who to target". Consumes Competitive Landscape (v0.2) CFD- entries. Outputs CFD- entries for competitor moats and BR- entries for targeting rules and our defensibility strategy.
---

# Moat Definition

Position in HORIZON workflow: v0.2 Competitive Landscape → **v0.3 Moat Definition** → v0.3 Pricing Model Selection

## Moat Type Taxonomy

Every moat falls into one of six types. Identify primary + secondary moats per competitor:

| Moat Type | Definition | Strong When | Weak When |
|-----------|------------|-------------|-----------|
| **Switching Costs** | Friction to leave (data, workflow, contracts) | Multi-year data, deep integrations | Easy export, monthly contracts |
| **Network Effects** | Value increases with users | Two-sided marketplace, content platform | Single-player tool, linear value |
| **Data/IP** | Proprietary data or algorithms | Unique training data, patents | Commodity ML, public datasets |
| **Brand/Trust** | Recognition, credibility | Regulated industry, high-risk decisions | Low-stakes, undifferentiated |
| **Scale/Cost** | Volume economics | Infrastructure-heavy, marginal cost near zero | Labor-intensive, linear cost |
| **Regulatory** | Compliance barriers | Certifications required, government contracts | No compliance requirements |

**For micro-SaaS**: Switching costs and brand/trust matter most. Network effects and scale rarely apply.

## Moat Strength Tiers

Rate each competitor's defensibility:

| Tier | Criteria | Evidence Signals | Targeting Implication |
|------|----------|------------------|----------------------|
| **Impenetrable** | Multi-layered moat, 10+ years data lock-in | "Would take years to switch" | Avoid direct competition |
| **Strong** | Significant switching friction, 1-2 year contracts | High NPS + low churn despite complaints | Target underserved segments only |
| **Moderate** | Some friction, workarounds exist | Churn 5-10%, export options | Wedge opportunity exists |
| **Weak** | Easy to replace, commodity offering | Monthly plans, high churn, price shopping | Direct competition viable |
| **Eroding** | Former strength declining | New alternatives gaining share | Aggressive targeting |

**Gate rule**: Don't compete where incumbent has Impenetrable or Strong moat unless targeting segment they explicitly ignore.

## Switching Cost Inventory

Quantify ALL switching costs — the sum determines moat strength:

| Cost Type | High Impact | Low Impact | How to Assess |
|-----------|-------------|------------|---------------|
| **Financial** | >6mo contract, early termination fees | Monthly billing, no penalty | Check pricing page terms |
| **Time/Effort** | 40+ hr migration, retraining | <4 hr setup, familiar UX | Trial the competitor |
| **Data Migration** | Proprietary format, no export | Standard export (CSV, API) | Test export function |
| **Workflow Retraining** | Unique methodology, team habits | Standard patterns | Read onboarding docs |
| **Integration Rework** | Deep API dependencies | Standalone tool | Map their integrations |

**Calculation**: Sum hours + dollars. >$5K or >40hr = material switching cost.

## Targeting Decision Framework

Use moat analysis to determine where to compete:

```
Moat Impenetrable/Strong → DON'T COMPETE HERE
                          ↓ unless
                          Target ignored segment (SMB, specific vertical)
                          
Moat Moderate → WEDGE STRATEGY
                ↓ identify
                Entry point that bypasses switching friction
                
Moat Weak/Eroding → DIRECT COMPETITION
                    ↓ execute
                    Feature + price attack on their core
```

### Wedge Opportunity Signals

A wedge exists when:
- Competitor moat doesn't apply to specific segment
- One feature has LOW switching cost (can start there)
- Integration allows coexistence (not replacement)
- Price sensitivity > switching friction

## Analysis Workflow

### Step 1: Pull Competitor Data
Retrieve CFD- entries from v0.2 Competitive Landscape. For each competitor, you need: pricing, complaints, feature set.

### Step 2: Identify Moat Type
For each competitor, determine primary moat type. Use evidence from reviews, pricing structure, integration depth.

### Step 3: Rate Moat Strength
Apply tier criteria. Flag if insufficient evidence (Tier 4-5 confidence).

### Step 4: Inventory Switching Costs
Complete the 5-category switching cost assessment. Quantify hours + dollars.

### Step 5: Identify Vulnerabilities
Where is their moat weakest? Which segments do they ignore? What's eroding?

### Step 6: Generate IDs

**CFD entries** (customer_feedback.md):
Template: [assets/cfd-moat-analysis.md](assets/cfd-moat-analysis.md)
```
CFD-MOT-###: [Competitor] Moat Analysis — [Moat Type], [Strength Tier]
```

**BR entries** (BUSINESS_RULES.md):
Template: [assets/br-targeting.md](assets/br-targeting.md)
```
BR-TGT-###: [Targeting Rule] — based on [Competitor] moat weakness
```

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| "They're big" | Specify which moat type + evidence |
| Assume low switching cost | Quantify: hours + dollars |
| Only analyze direct competitors | Include Type 4-5 (workarounds, inertia) |
| Underestimate integration moat | Map actual dependency depth |
| Ignore eroding moats | Track signals: new entrants, complaints |
| Target where moat is strong | Find the segment where moat doesn't apply |

## Output Requirements

Before advancing to Our Moat Articulation:
- [ ] ≥3 competitors with moat type identified
- [ ] ≥2 competitors with switching costs quantified
- [ ] Moat strength tier assigned (with evidence)
- [ ] Targeting decision per competitor (compete/avoid/wedge)
- [ ] CFD-MOT entries created (≥3)
- [ ] BR-TGT entries created (≥2)

## Downstream Connections

| Consumer | What It Needs | Format |
|----------|---------------|--------|
| **v0.3 Our Moat Articulation** | Where competitors are weak, what moats work | CFD-MOT entries |
| **v0.3 Pricing Model** | What price points bypass switching friction | BR-TGT entries |
| **v0.5 Red Team** | Risks of competitor response | Moat strength tiers |
| **v0.9 GTM** | Positioning against competitor moats | Targeting rules |

## Detailed References

- **Good/bad examples**: See `references/examples.md`
- **CFD-MOT template**: See `assets/cfd-moat-analysis.md`
- **BR-TGT template**: See `assets/br-targeting.md`
