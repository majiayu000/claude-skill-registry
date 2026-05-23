---
name: company-name-generator
description: Generates business/company names across 10 categories (Descriptive, Metaphoric, Invented, Founder-based, Acronym, Compound, Foreign, Playful, Geographic, Legacy) with USPTO trademark screening, domain availability checking, and 0-100 scoring. Use when users need company/product/brand naming for new business launches, rebranding, trademark strategy, IP protection naming, evaluating current name strength, or any naming/branding tasks requiring systematic analysis with legal clearance.
---

# Company Name Generator

Systematic business naming with trademark screening and domain availability validation.

## Core Workflow

1. Extract business context (domain, audience, competitive positioning, IP requirements)
2. Generate 5-15 names per category (10 categories)
3. Score each name 0-100 across 5 weighted criteria
4. Check USPTO TESS for trademark conflicts
5. Verify .com/.ai/.io domain availability
6. Present top 25 ranked names with availability data

## 10 Naming Categories

**Descriptive** - Direct function description. Clear but may lack trademark strength.  
**Metaphoric** - Evoke imagery/emotions. Strong storytelling (e.g., "Everest", "Summit").  
**Invented** - Unique coined words. Highest trademark strength (e.g., "Auctioniq").  
**Founder-Based** - Personal brand authority. Clear IP ownership (e.g., "Shapira Formula").  
**Acronym** - Memorable initialisms (e.g., "APEX").  
**Compound** - Two-word combinations (e.g., "BidDeed", "LienLogic").  
**Foreign Language** - Sophistication/authority (e.g., "Veritas").  
**Playful** - Approachable, memorable (e.g., "BidWise").  
**Geographic** - Place-based authority (e.g., "Brevard BidTech").  
**Legacy** - Institutional authority (e.g., "The Shapira Group").

## Scoring Formula (0-100)

```
Score = (Trademark×0.30) + (Domain_Signal×0.25) + (Tech_Signal×0.25) + (Metaphor×0.10) + (Memo×0.10)
```

**Trademark Strength (30%)**: USPTO conflict risk  
**Domain Signal (25%)**: Industry/function clarity  
**Tech Signal (25%)**: AI/ML/automation implication  
**Metaphor Power (10%)**: Storytelling/pitch strength  
**Memorability (10%)**: Ease of recall/pronunciation

## USPTO & Domain Checking

Use `scripts/check_availability.py` to verify both:

```bash
python scripts/check_availability.py "Company Name" --classes 9,42 --tlds com,ai,io
```

**Trademark Classes:**
- Class 9: Software
- Class 42: SaaS
- Class 41: Education (if methodology/certification)

**Risk Levels:**  
LOW (0-1 conflicts) | MEDIUM (2-4 conflicts) | HIGH (5+ conflicts)

## Output Format

Present top 25 as markdown table:

| Rank | Name | Category | Score | TM Risk | Domain | Notes |
|------|------|----------|-------|---------|--------|-------|
| 1 | BidDeed.AI | Compound | 90 | LOW | ✅ .ai | Function + AI clear |
| 2 | Shapira Formula™ | Founder | 92 | LOW | ✅ .ai | Personal IP ownership |

## Special Cases

**Metric/Framework Names**: Emphasize Founder-based + Formula categories. High metaphor power for investor pitches.

**IP Protection Focus**: Favor Founder-based (personal ownership clear) and Invented (high TM strength).

**Dual-Brand Strategy**: Generate both umbrella + product names. Verify brand hierarchy logic.

See `references/naming_best_practices.md` for trademark templates and brand architecture patterns.
