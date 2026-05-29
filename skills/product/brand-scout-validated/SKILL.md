---
name: brand-scout-validated
description: "Self-validating Brand Scout with Ralph Loop - iterates until 5-point shipping checklist complete. Triggers: 'validated brand scout', 'complete brand scout', 'full brand scout'"
version: 1.0.0
author: Brett Walker
---

# Brand Scout: Validated

**Purpose**: Create Brand Scout reports that iterate until ALL shipping data is documented. Uses Ralph Loop methodology to guarantee completeness.

## Trigger Phrases

- "validated brand scout for [company]"
- "complete brand scout for [company]"
- "full brand scout [company]"
- "brand scout validated [company]"
- `/brand-scout:validated [company]`

## The Problem This Solves

Audit revealed **50% of Brand Scout reports are missing shipping data**:
- 41 reports missing shipping page URL
- 38 missing free shipping threshold
- 27 missing delivery window
- 19 missing expedited options

## The Solution

A self-correcting loop that:
1. Researches the company
2. Validates against 5-point checklist
3. Re-researches gaps
4. Iterates until complete OR explicitly marks data as "Not found"

---

## Validation Checklist (5 Points)

| # | Criterion | Must Have |
|---|-----------|-----------|
| 1 | Shipping Page URL | Exact URL or "Not found" |
| 2 | Free Shipping Threshold | Dollar amount or "No free shipping" |
| 3 | Standard Delivery Window | X-Y days or "Not specified" |
| 4 | Carrier/Fulfillment Info | Names or "Not disclosed" |
| 5 | Expedited Options | Service names or "Not offered" |

**Confidence Markers**:
- `Confirmed` - Found with source URL
- `Inferred` - Estimated from context
- `Not found` - Researched 3x, unavailable

---

## Execution Flow

```
START
  |
  v
[Initial Research] -----> Research company, scrape shipping pages
  |
  v
[Generate Draft] -------> Create report with available data
  |
  v
[Validate Checklist] ---> Check 5 criteria against report
  |                         |
  | (gaps found)            | (all complete)
  v                         v
[Research Gaps] -------> [Mark Complete]
  |                         |
  | (max 3 attempts         |
  |  per criterion)         |
  v                         v
[Update Report] --------> [Save to Brand Scout Reports/]
  |                         |
  | (still gaps?)           |
  v                         v
[Loop or Mark            [Output Success]
 "Not found"]               |
  |                         v
  +----------------------> END
```

---

## Ralph Loop Integration

When invoked, this skill automatically sets up Ralph Loop:

```yaml
ralph_loop_config:
  max_iterations: 5
  completion_promise: "BRAND SCOUT VALIDATED"
  validation_gate: 5-point shipping checklist
  failure_mode: mark_incomplete_and_flag
```

**Iteration Behavior**:
- **Iteration 1**: Full research, draft report
- **Iteration 2**: Validate, identify gaps, targeted research
- **Iteration 3**: Deep dive on stubborn gaps (try alternate URLs)
- **Iteration 4**: Last research attempt, prepare to mark "Not found"
- **Iteration 5**: Final validation, save report (complete or flagged)

---

## Research Sequence

### Shipping Page Discovery (Try in Order)

1. `[domain]/shipping`
2. `[domain]/pages/shipping`
3. `[domain]/policies/shipping-policy` (Shopify)
4. `[domain]/shipping-returns`
5. `[domain]/delivery`
6. `[domain]/faq` (search for shipping section)
7. `[domain]/help/shipping`
8. Footer links labeled "Shipping" or "Delivery"

### Data Extraction Patterns

**Free Shipping Threshold**:
- Look for: "Free shipping on orders over $X"
- Banner/header promotions
- Cart page messaging
- FAQ answers

**Delivery Windows**:
- "Standard: 3-5 business days"
- "Ground shipping: 5-7 days"
- Processing time + transit time

**Carrier Info**:
- Tracking page (carrier logos)
- FAQ mentions of UPS/FedEx/USPS
- AfterShip/Route/Narvar branding
- 3PL partner mentions

**Expedited Options**:
- "Express", "Priority", "2-Day", "Overnight"
- Checkout shipping options (if accessible)
- FAQ shipping tiers

---

## Report Template

See `.claude/commands/brand-scout-validated.md` for full template.

Key sections that MUST be complete:

```markdown
## SHIPPING & LOGISTICS PROFILE

### Shipping Page
- **URL**: [REQUIRED] | Confidence: [REQUIRED]

### Shipping Options
| Service | Delivery Window | Cost | Confidence |
|---------|-----------------|------|------------|
| Standard | [REQUIRED] | [REQUIRED] | [REQUIRED] |
| Expedited | [VALUE or "Not offered"] | ... | ... |

### Free Shipping
- **Threshold**: [REQUIRED] | Confidence: [REQUIRED]

### Carrier & Fulfillment
- **Carriers Used**: [REQUIRED - even if "Not disclosed"]

---

## VALIDATION STATUS

| Criteria | Status | Value |
|----------|--------|-------|
| Shipping URL | [PASS/FAIL] | [value] |
| Free Threshold | [PASS/FAIL] | [value] |
| Delivery Window | [PASS/FAIL] | [value] |
| Carrier Info | [PASS/FAIL] | [value] |
| Expedited Options | [PASS/FAIL] | [value] |

**Overall**: [X/5 COMPLETE]
```

---

## Output Location

Reports saved to: `Brand Scout Reports/[Company_Name]_Brand_Scout.md`

If incomplete after max iterations:
- Saved as: `Brand Scout Reports/[INCOMPLETE]_[Company_Name]_Brand_Scout.md`
- Added to: `Brand Scout Reports/_AUDIT_REPORT.md` priority list

---

## Usage Examples

### Basic
```
/brand-scout:validated Huel
```

### With Domain
```
/brand-scout:validated "Bare Performance Nutrition" --domain bpnsupps.com
```

### More Iterations for Complex Companies
```
/brand-scout:validated "Hims & Hers" --max-iterations 7
```

### Fix Existing Report
```
/brand-scout:validated "Phys Choice" --update-existing
```

---

## Success Criteria

Report is VALIDATED when:

1. All 5 shipping criteria have values
2. Each value has a confidence marker
3. No placeholder text ("TBD", "[RESEARCH]")
4. Validation table shows 5/5 PASS or explicit "Not found"
5. Report saved to correct location

**Completion Promise**: `<promise>BRAND SCOUT VALIDATED</promise>`

---

## Integration with Existing Skills

This skill enhances but does not replace:

| Skill | Use Case |
|-------|----------|
| `/brand-scout:quick` | Fast 15-min research (no validation) |
| `/brand-scout:scout` | Standard 25-35min (basic validation) |
| `/brand-scout:validated` | Full validation loop (guaranteed complete) |
| `/brand-scout:full` | Validated + HubSpot creation |

**Recommended Flow**:
1. Use `/brand-scout:validated` for all new leads
2. Use audit to check existing reports
3. Run validated on flagged reports to fix gaps

---

## Metrics

Track these to measure improvement:

| Metric | Before | Target |
|--------|--------|--------|
| Reports 5/5 complete | 50% | 90% |
| Reports needing fixes | 46 | <10 |
| Avg shipping criteria per report | 3.2 | 4.8 |

---

*Built on Ralph Loop methodology: iterate until genuinely complete.*
