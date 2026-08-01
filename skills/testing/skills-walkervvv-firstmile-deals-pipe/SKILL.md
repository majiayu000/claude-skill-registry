---
name: skills-walkervvv-firstmile-deals-pipe
description: 'Purpose: Autonomous overnight research to identify new shipping leads
  from target industries.'
---

# Brand Scout Agent Skill

**Purpose**: Autonomous overnight research to identify new shipping leads from target industries.

## Core Reference
→ **See [rules.md](../../rules.md) → Agent-Specific Rules → Brand Scout Agent**

## Execution Workflow

### Phase 1: Research Planning (10 PM - 11 PM)
1. Load target industry lists from `.claude/brand_scout/targets/`
2. Identify companies not already in HubSpot (search first)
3. Queue research jobs for overnight processing

### Phase 2: Data Collection (11 PM - 5 AM)
1. Extract company info: industry, size, location, website
2. Identify key decision makers (VP Supply Chain, Director Logistics, COO)
3. Estimate shipping volume from:
   - Company size + industry averages
   - Public shipping data (if available)
   - Job postings mentioning fulfillment/logistics
4. Flag pain points: shipping costs, slow delivery, multi-carrier complexity

### Phase 3: Report Generation (5 AM - 6 AM)
1. Generate markdown summaries in `.claude/brand_scout/output/YYYY-MM-DD/`
2. Calculate confidence scores (High/Medium/Low)
3. Prioritize leads by estimated annual shipping spend
4. **STOP** → Human reviews during 9AM sync

## Output Template

```markdown
# Brand Scout Report: {Company Name}
**Date**: {YYYY-MM-DD}
**Confidence**: {High/Medium/Low}
**Estimated Annual Shipping Spend**: ${amount}
**Industry**: {industry}
**Employee Count**: {count}

## Company Profile
- **Website**: {URL}
- **Headquarters**: {City, State}
- **Business Model**: {B2B/B2C/Hybrid}
- **eCommerce Platforms**: {Shopify/WooCommerce/Custom/etc.}

## Key Contacts
| Name | Title | LinkedIn | Email (if found) |
|------|-------|----------|------------------|
| [Name] | [Title] | [URL] | [Email] |

## Shipping Profile
**Estimated Volume**: {parcels/month}
**Service Needs**: {Ground/Expedited/Priority mix}
**Current Carriers**: {inferred from data}
**Pain Points Identified**:
- [Pain point 1]
- [Pain point 2]

## Geographic Distribution
**Top Destination States**: {states based on customer base}
**Warehouse/Fulfillment Locations**: {if found}

## Recommendation
**Action**: {Pursue/Hold/Archive}
**Reasoning**: {why this lead is/isn't a good fit}
**Next Steps**: {if pursuing, what's the approach?}

## Sources
- [Source 1 URL]
- [Source 2 URL]
```

## Strict Compliance Rules

### ✅ MUST DO
- Generate research summaries with confidence scores
- Include source URLs and data freshness timestamps
- Flag high-priority leads (>$500K annual shipping spend)
- Preserve raw research data in `.claude/brand_scout/data/`
- Log all research queries and results

### ❌ NEVER DO
- Auto-create HubSpot records without human approval
- Run brand scout during business hours (overnight only)
- Overwrite existing lead folders
- Skip confidence scoring or source attribution
- Research companies already in HubSpot pipeline

## Quality Gates

Before marking research complete:
- [ ] All target companies researched (or flagged as "insufficient data")
- [ ] Confidence scores calculated for each lead
- [ ] Output files generated in `.claude/brand_scout/output/YYYY-MM-DD/`
- [ ] High-priority leads (>$500K) flagged in summary report
- [ ] Source URLs documented for verification

## Human Approval Workflow

**During 9AM Sync**:
1. Prioritization Agent loads brand scout output
2. Human reviews each lead's recommendation
3. Approved leads → Create HubSpot contact + company
4. Held leads → Move to `.claude/brand_scout/hold/` for later review
5. Archived leads → Move to `.claude/brand_scout/archive/` (not a fit)

**HubSpot Creation** (only after approval):
```python
from hubspot_sync_core import HubSpotSyncManager

# After human says "approve Brand X"
sync_manager.create_contact(
    first_name="John",
    last_name="Smith",
    email="john@brandx.com",
    company="Brand X",
    lifecycle_stage="lead"
)

# Move approved lead to [00-LEAD]_Brand_X/ folder
```

## Research Source Priorities

**Primary Sources** (most reliable):
1. Company website (about, team, contact pages)
2. LinkedIn company page (employee count, locations)
3. Public shipping/logistics data (if available)
4. Job postings (mentions of "fulfillment", "shipping volume")

**Secondary Sources** (use with caution):
1. Industry reports (estimates, not specific to company)
2. News articles (recent shipping partnerships)
3. Glassdoor reviews (employee mentions of shipping operations)

**Avoid**:
- Speculative data without sources
- Outdated information (>1 year old)
- Competitor websites (not reliable for volume estimates)

## Error Handling

**Insufficient Data**:
- Flag lead as "Low Confidence - Insufficient Data"
- Document what data is missing
- Suggest manual research approach for human

**Rate Limiting**:
- Respect research source rate limits (LinkedIn, Google, etc.)
- Implement exponential backoff for blocked requests
- Log all rate limit encounters for future optimization

**Duplicate Detection**:
- Search HubSpot before researching (avoid duplicate work)
- Check `.claude/brand_scout/archive/` for previously rejected leads
- Flag potential duplicates for human review

## Performance Metrics

**Target Benchmarks**:
- Research 10-20 companies per night
- >70% leads rated Medium or High confidence
- <10% duplicate/already-researched companies
- 100% source attribution

**Monthly Review**:
- Conversion rate: Brand Scout leads → Closed-Won deals
- Data quality: Accuracy of shipping spend estimates
- Time savings: Hours saved vs. manual research

## Related Documentation

- [rules.md](../../rules.md) - Complete agent rules and prohibitions
- [.claude/docs/systems/BRAND_SCOUT_SYSTEM.md](../docs/systems/BRAND_SCOUT_SYSTEM.md) - System architecture
- [.claude/brand_scout/README.md](../brand_scout/README.md) - Research templates and targets
