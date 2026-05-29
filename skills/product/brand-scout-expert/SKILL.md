# Brand Scout Expert

Self-improving lead research expert for autonomous eCommerce brand intelligence gathering.

---
name: brand-scout-expert
description: |
  Autonomous lead research system with Chrome DevTools MCP, web search, and HubSpot integration.
  Use when: researching prospects, generating brand profiles, creating email sequences, HubSpot lead creation
  Triggers on: "brand scout", "scout [brand]", "research [company]", "lead intelligence",
               "generate brand profile", "prospect research", "email sequence", "shipping intelligence"
---

## Quick Reference

| Item | Value |
|------|-------|
| Version | Brand Scout v3.8 |
| Time/Report | 25-35 minutes (standard), 15 min (quick) |
| Report Sections | 9 comprehensive sections |
| Confidence Target | 80%+ (HIGH) |
| **Shipping Validation** | **5/5 REQUIRED** |
| Contacts Required | 2+ verified per report |
| Weekly Capacity | 15-20 reports |
| Output Location | `Brand Scout Reports/` |
| Owner ID | `699257003` |

## Execution Modes

| Mode | Command | Time | Output |
|------|---------|------|--------|
| Quick Scout | `/brand-scout:quick [BRAND]` | 15 min | Core sections, contacts focus |
| Standard | `/brand-scout:scout [BRAND]` | 25-35 min | Full 9-section report |
| Full Automation | `/brand-scout:full [BRAND]` | 30-40 min | Report + HubSpot + folder + email sequence |

## Decision Rules Summary

### BEFORE Research
- IF company already in HubSpot → UPDATE existing record, don't create duplicate
- IF target is B2B/wholesale only → SKIP (not DTC fit)
- IF no website found → SKIP (insufficient data)

### DURING Research
- IF shipping page not found → CHECK checkout flow AND FAQ AND search "[BRAND] shipping policy"
- IF no contacts on website → TRY LinkedIn "See all employees" AND press releases
- IF Chrome DevTools timeout → FALLBACK to WebSearch AND Wayback Machine
- IF revenue unknown → ESTIMATE from (funding ÷ 10) OR (employees × $200K)

### AFTER Research
- IF confidence < 60% → DO NOT SUBMIT (LOW quality)
- IF confidence 60-79% → FLAG for manual review (MEDIUM)
- IF confidence 80%+ → READY for HubSpot creation (HIGH)
- IF contacts < 2 verified → CONTINUE research until 2+ found

### HubSpot Integration
- ALWAYS search by email AND domain BEFORE creating records
- ALWAYS use exact industry values (CONSUMER_GOODS not "consumer goods")
- ALWAYS set hubspot_owner_id = "699257003"
- ALWAYS create Company THEN Contact(s) THEN Associate

## Shipping Validation Quality Gate (v3.8)

**MANDATORY**: Every Brand Scout report MUST validate 5 shipping criteria before completion.

### 5-Point Checklist

| # | Criterion | Required Value | Confidence Marker |
|---|-----------|----------------|-------------------|
| 1 | Shipping Page URL | Exact URL or "Not found" | Confirmed/Not found |
| 2 | Free Shipping Threshold | $X+ or "No free shipping" | Confirmed/Inferred/Not found |
| 3 | Standard Delivery Window | X-Y business days | Confirmed/Inferred/Not found |
| 4 | Carrier/Fulfillment Info | Names or "Not disclosed" | Confirmed/Inferred/Not found |
| 5 | Expedited Options | Service names or "Not offered" | Confirmed/Inferred/Not found |

### Research Sequence (try in order)

1. `/shipping` or `/pages/shipping`
2. `/policies/shipping-policy` (Shopify standard)
3. `/shipping-returns` or `/delivery`
4. `/faq` (search for shipping section)
5. `/help` or help center subdomain
6. **Return Policy Page** - Often reveals 3PL/warehouse address
7. **FALLBACK**: Coupon sites (Knoji, SimplyCodes) for free threshold

### Validation Rules

- Report is **INCOMPLETE** until all 5 criteria have explicit values
- "Not found" is a valid value (means data is unavailable, not missing research)
- Every report MUST include `## SHIPPING VALIDATION STATUS` table
- Score of 5/5 required for report completion

## Report Structure (9 Sections)

1. **Snapshot** - Revenue, AOV, annual volume, growth rate
2. **Shipping Intelligence** - Carriers, service levels, SLA, complaints, 3PL
3. **Company Overview** - Legal name, HQ, founding, DTC/wholesale split
4. **Stakeholders & Contacts** - Decision makers with verified emails/LinkedIn
5. **Observations & Competitors** - Strengths, complaints %, benchmarks, risks
6. **HubSpot Lead Record** - Copy/paste fields ready for import
7. **CRM Contact Summary** - One-line format for quick reference
8. **Technical Integration** - Platform, APIs, monitoring capabilities
9. **Methodology & Versioning** - Sources, tools, confidence score

## Confidence Levels

| Level | Score | Criteria | Action |
|-------|-------|----------|--------|
| HIGH | 80%+ | 2+ sources, verified contacts, shipping confirmed | Ready for HubSpot |
| MEDIUM | 60-79% | Single source, some estimates | Manual review needed |
| LOW | <60% | Multiple blanks, no verified contacts | DO NOT SUBMIT |

## Reference Files

| File | Load When | Purpose |
|------|-----------|---------|
| `00-decision-rules.md` | Always | IF-THEN rules for all scenarios |
| `01-research-protocol.md` | Starting research | 4-phase methodology with time budgets |
| `02-chrome-devtools-patterns.md` | Using Chrome MCP | Browser automation tactics |
| `03-hubspot-integration.md` | Creating records | 6-step HubSpot process |
| `04-email-sequence-templates.md` | After report complete | 5-email outreach structure |
| `05-known-failures.md` | Before any operation | Documented issues with prevention |

## Integration Points

### With Discovery/Sales Expert
- Brand Scout reports feed 38 Questions discovery prep
- Shipping intelligence informs service level recommendations
- Contact research enables personalized outreach

### With HubSpot CRM Expert
- Uses association IDs for lead creation (578, 580)
- Follows timestamp and rate limiting patterns
- Integrates with deal folder naming conventions

### With Goal Tracking Expert
- new_leads metric counts Contacts created (not Companies)
- Stage 1 micro-actions reference Brand Scout workflow
- Weekly goals include 15-20 reports target

## Common Commands

```bash
# Quick research (15 min)
/brand-scout:quick [BRAND] --focus contacts

# Standard research (25-35 min)
/brand-scout:scout [BRAND]

# Full automation with HubSpot
/brand-scout:full [BRAND] --hubspot --folder --email-sequence

# Check if lead exists
/check-lead [BRAND]

# Add to HubSpot after research
/add-lead [BRAND]

# Generate email sequence only
/brand-scout:email-sequence [BRAND]
```

## Learning Mechanism

After each Brand Scout execution:
1. Log outcome (success/failure/partial)
2. Record any new patterns discovered
3. Update expertise.yaml if learning occurred
4. Note Chrome DevTools workarounds that worked

## Version History

- **v3.8** (Current): 5-Point Shipping Validation Quality Gate - mandatory checklist, research sequence, confidence markers
- **v3.7**: Full Chrome DevTools integration, 9-section template
- **v3.5**: Added email sequence generation
- **v3.0**: HubSpot Lead object support
