---
name: crm-hygiene
description: Audit and improve CRM data quality by identifying missing fields, inconsistent values, duplicate records, and stale data
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# CRM Hygiene

> Systematically identify and resolve data quality issues in your CRM to improve forecast accuracy, reporting, and automation reliability.

## When to Use This Skill

- Quarterly CRM audits
- Before major reporting periods
- When automation workflows fail
- After team changes or migrations
- Preparing for CRM integrations

## Methodology Foundation

Based on **Salesforce Data Quality Best Practices** and **RevOps Co-op Data Governance frameworks**, focusing on:
- Completeness (required fields populated)
- Consistency (standardized values)
- Accuracy (correct and current data)
- Timeliness (recent updates)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Defines audit criteria | Which fields are required |
| Identifies data issues | Priority of fixes |
| Categorizes problems by type | Who owns cleanup tasks |
| Suggests remediation steps | Automation vs manual fix |
| Creates cleanup reports | Enforcement policies |

## What This Skill Does

1. **Audit design** - Define required fields and validation rules
2. **Issue identification** - Find missing, inconsistent, duplicate data
3. **Prioritization** - Rank issues by business impact
4. **Remediation planning** - Action steps to fix issues
5. **Governance recommendations** - Prevent future issues

## How to Use

### For Audit Design:
```
Help me create a CRM hygiene audit for [CRM System].

Key objects to audit:
- [Leads, Contacts, Accounts, Opportunities]

Critical fields for each:
- Leads: [list required fields]
- Opportunities: [list required fields]

Our main issues:
- [Describe known problems]
```

### For Data Audit:
```
Audit this opportunity data for hygiene issues:

[Paste export or describe data]

Required fields:
- [List fields that must be populated]

Validation rules:
- [List rules like "Stage must match Amount > $0"]
```

## Instructions

### Step 1: Define Audit Scope

**Object Priority (typical):**
1. Opportunities - Revenue impact
2. Accounts - Relationship foundation
3. Contacts - Communication accuracy
4. Leads - Pipeline source

**Field Categories:**
- **Critical** - Blocks processes if missing
- **Important** - Affects reporting/segmentation
- **Nice-to-Have** - Enriches but not required

### Step 2: Completeness Audit

Check required fields by object:

**Opportunities:**
| Field | Criticality | Why Required |
|-------|-------------|--------------|
| Amount | Critical | Forecast, pipeline value |
| Close Date | Critical | Forecast timing |
| Stage | Critical | Pipeline reporting |
| Owner | Critical | Accountability |
| Account | Critical | Company linkage |
| Primary Contact | Important | Communication |
| Next Step | Important | Deal momentum |
| Competitor | Important | Win/loss analysis |
| Loss Reason | Critical (if lost) | Improvement insights |

**Accounts:**
| Field | Criticality | Why Required |
|-------|-------------|--------------|
| Industry | Important | Segmentation |
| Employee Count | Important | ICP fit |
| Website | Important | Research, enrichment |
| Billing Address | Critical | Invoicing |
| Account Owner | Critical | Accountability |

### Step 3: Consistency Audit

Check for standardization issues:

| Issue Type | Example | Impact |
|------------|---------|--------|
| Picklist variations | "US" vs "USA" vs "United States" | Reporting breaks |
| Case inconsistency | "ACME" vs "Acme" vs "acme" | Duplicates |
| Format variations | "(555) 123-4567" vs "5551234567" | Automation fails |
| Null vs blank | NULL vs "" vs "N/A" | Filters don't work |

### Step 4: Accuracy Audit

Identify likely incorrect data:

| Check | Criteria | Action |
|-------|----------|--------|
| Stale close dates | Past date, still open | Update or close |
| Amount mismatches | $0 in late stage | Verify pricing |
| Stage regression | Stage 4 → Stage 2 | Investigate |
| Impossible values | 200% probability | Fix validation |
| Bounced emails | Marked invalid | Remove or update |

### Step 5: Duplicate Detection

Find potential duplicates:

| Match Type | Criteria | Confidence |
|------------|----------|------------|
| Exact email | Same email address | 99% duplicate |
| Domain match | Same company domain | 80% duplicate |
| Fuzzy name | Similar company name | Investigate |
| Phone match | Same phone number | 90% duplicate |

### Step 6: Timeliness Audit

Flag stale records:

| Object | Staleness Threshold | Action |
|--------|---------------------|--------|
| Open Opportunity | No activity 30 days | Review with rep |
| Lead | No touch 14 days | Reassign or nurture |
| Account | No contact 90 days | Re-engagement |
| Contact | Bounced + 30 days | Archive |

## Examples

### Example 1: Opportunity Audit

**Input:**
```
Audit these opportunities:

1. Acme Corp - Stage: Proposal, Amount: $0, Close: Jan 15 (past), Owner: Empty
2. Beta Inc - Stage: Closed Won, Amount: $50K, Close: Feb 1, Loss Reason: "Price"
3. Gamma LLC - Stage: Discovery, Amount: $100K, Close: Mar 30, No activity 45 days
4. Delta Co - Stage: Negotiation, Amount: $75K, Close: Feb 28, Next Step: Empty
5. Echo Systems - Stage: Closed Lost, Amount: $200K, Loss Reason: Empty
```

**Output:**
```
## CRM Hygiene Audit: Opportunities

### Summary
- **Total Records**: 5
- **Critical Issues**: 4
- **Warnings**: 2
- **Clean Records**: 0

### Critical Issues (Fix Immediately)

#### 1. Acme Corp - 3 Critical Issues
| Issue | Field | Current | Required |
|-------|-------|---------|----------|
| 🔴 Missing | Owner | Empty | Assigned rep |
| 🔴 Missing | Amount | $0 | Deal value |
| 🔴 Stale | Close Date | Jan 15 (past) | Future date |

**Action**: Assign owner, verify if deal is active, update amount and close date.

#### 2. Beta Inc - Logic Error
| Issue | Field | Current | Problem |
|-------|-------|---------|---------|
| 🔴 Inconsistent | Loss Reason | "Price" | Stage is "Closed Won" |

**Action**: Either change stage to Closed Lost, or clear Loss Reason.

#### 3. Echo Systems - Missing Required
| Issue | Field | Current | Required |
|-------|-------|---------|----------|
| 🔴 Missing | Loss Reason | Empty | Required for Closed Lost |

**Action**: Rep must document why deal was lost.

#### 4. Delta Co - Missing Next Step
| Issue | Field | Current | Impact |
|-------|-------|---------|--------|
| 🟠 Missing | Next Step | Empty | No clear action |

**Action**: Rep should define next step for Negotiation stage.

### Warnings (Review This Week)

#### 5. Gamma LLC - Stale Deal
| Issue | Indicator | Value |
|-------|-----------|-------|
| 🟡 Stale | Last Activity | 45 days ago |

**Action**: Review with rep - is this deal still active? If yes, update. If no, close lost.

### Hygiene Score: 20/100 (Poor)

### Recommended Actions by Priority

1. **Today**: Fix Acme Corp (no owner = orphaned deal)
2. **Today**: Fix Beta Inc logic error (affects win rate)
3. **This Week**: Get Echo Systems loss reason
4. **This Week**: Update Gamma LLC status
5. **This Week**: Add Delta Co next step

### Process Recommendations
- Add validation rule: Amount required when Stage > Discovery
- Add validation rule: Owner required on all opportunities
- Add validation rule: Loss Reason required when Closed Lost
- Create stale deal report (no activity 30+ days)
```

### Example 2: Duplicate Detection

**Input:**
```
Check these accounts for duplicates:

1. Acme Corporation, acme.com, San Francisco
2. ACME Corp, acme.com, SF
3. Acme Inc, acme-inc.com, San Francisco
4. Beta Technologies, beta.io, New York
5. Beta Tech, betatech.com, NYC
6. Beta Technologies Inc, beta.io, New York
```

**Output:**
```
## Duplicate Detection Report

### High Confidence Duplicates (Merge)

#### Duplicate Set 1: Acme Corporation
| Record | Name | Domain | Location | Confidence |
|--------|------|--------|----------|------------|
| #1 | Acme Corporation | acme.com | San Francisco | Master |
| #2 | ACME Corp | acme.com | SF | 99% - Same domain |

**Recommendation**: Merge #2 into #1
- Same domain (acme.com)
- Same location (SF = San Francisco)
- Name variation only (Corp vs Corporation)

#### Duplicate Set 2: Beta Technologies
| Record | Name | Domain | Location | Confidence |
|--------|------|--------|----------|------------|
| #4 | Beta Technologies | beta.io | New York | Master |
| #6 | Beta Technologies Inc | beta.io | New York | 99% - Same domain |

**Recommendation**: Merge #6 into #4
- Same domain (beta.io)
- Same location (New York)
- Name variation only (Inc suffix)

### Investigate (Possible Duplicates)

#### Possible Set 1: Acme variations
| Record | Name | Domain | Location | Confidence |
|--------|------|--------|----------|------------|
| #1 | Acme Corporation | acme.com | San Francisco | - |
| #3 | Acme Inc | acme-inc.com | San Francisco | 40% |

**Recommendation**: Investigate manually
- Same location, similar name
- BUT different domains (acme.com vs acme-inc.com)
- Could be: subsidiary, different company, or typo

#### Possible Set 2: Beta variations
| Record | Name | Domain | Location | Confidence |
|--------|------|--------|----------|------------|
| #4 | Beta Technologies | beta.io | New York | - |
| #5 | Beta Tech | betatech.com | NYC | 50% |

**Recommendation**: Investigate manually
- Same location (NYC = New York)
- Similar names (Beta Tech vs Beta Technologies)
- Different domains - likely different companies

### Summary
- **Definite Duplicates**: 2 sets (4 records → 2)
- **Possible Duplicates**: 2 sets (need research)
- **Unique Records**: Pending investigation

### Merge Checklist
Before merging, verify:
- [ ] All opportunities moved to master record
- [ ] All contacts linked to master
- [ ] Activity history preserved
- [ ] Custom fields compared
- [ ] Integration IDs noted (for external systems)
```

## Skill Boundaries

### What This Skill Does Well
- Defining audit criteria systematically
- Identifying common data quality issues
- Prioritizing fixes by business impact
- Creating actionable remediation plans

### What This Skill Cannot Do
- Access your actual CRM data
- Execute cleanup automatically
- Know your specific business rules
- Detect all semantic errors

### When to Escalate to Human
- Merge decisions (data loss risk)
- Business rule definitions
- Enforcement policy decisions
- Cross-object relationship issues

## Iteration Guide

### Follow-up Prompts
- "Create a monthly hygiene report template."
- "What validation rules would prevent these issues?"
- "Prioritize the top 10 issues by revenue impact."
- "Design a data entry form that enforces these rules."

### Continuous Improvement Cycle
1. Audit → Identify issues
2. Fix → Clean data
3. Prevent → Add validation rules
4. Monitor → Track hygiene score weekly
5. Iterate → Refine rules quarterly

## Checklists & Templates

### Weekly Hygiene Report Template
```markdown
## CRM Hygiene Report - Week of [Date]

### Hygiene Score: X/100

### Critical Issues (Fix Today)
| Object | Record | Issue | Owner |
|--------|--------|-------|-------|

### Warnings (Fix This Week)
| Object | Count | Issue Type |
|--------|-------|------------|

### Trends
- Issues closed this week: X
- New issues this week: X
- Net change: +/- X

### Action Items
1.
2.
3.
```

### Data Governance Checklist
- [ ] Required fields defined per object
- [ ] Validation rules implemented
- [ ] Duplicate rules active
- [ ] Stale record reports scheduled
- [ ] Ownership assignments current
- [ ] Integration mappings documented

## References

- Salesforce Data Quality Best Practices
- RevOps Co-op Data Governance Framework
- Marketo Database Health Guide
- Gartner Data Quality Market Guide

## Related Skills

- `pipeline-forecasting` - Clean data improves forecasts
- `lead-scoring` - Requires complete lead data
- `deal-risk-scoring` - Depends on activity data

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 30-60 min for audit, varies for cleanup
- **Prerequisites**: CRM data export, field requirements list
