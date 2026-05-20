---
name: deal-review
description: Review active deals and surface risks
role_groups: [sales, leadership]
jtbd: |
  You have multiple deals in flight and it's hard to keep track of which need 
  attention. This scans your deal pages, identifies stale deals (no recent activity), 
  flags missing next steps, and checks for upcoming deadlines so nothing slips 
  through the cracks.
time_investment: "5-10 minutes per review"
---

## Purpose

Get a comprehensive view of your deal pipeline health - identify at-risk deals, surface blockers, and ensure every deal has clear next steps.

## Usage

- `/deal-review` - Review all active deals
- `/deal-review [stage]` - Filter by deal stage (e.g., "discovery", "proposal", "negotiation")
- `/deal-review [timeframe]` - Focus on deals closing in timeframe (e.g., "this month", "Q1")

---

## Step 1: Identify Deal Files

Search for deal-related files:

1. **Primary location:** 04-Projects/
2. **Search patterns:**
   - Files containing "deal", "opportunity", "proposal"
   - Company names from People/External/
   - Tags like `#deal` or `#pipeline`

3. **Extract from each deal file:**
   - Company/account name
   - Deal size/value (if mentioned)
   - Stage (discovery, demo, proposal, negotiation, contract)
   - Last modified date
   - Next steps
   - Close date (if mentioned)
   - Stakeholders involved

---

## Step 2: Analyze Deal Health

For each deal, assess health:

### Staleness Check
- **Fresh:** Updated within last 5 days - ✅
- **Aging:** 6-10 days without update - ⚠️
- **Stale:** 11+ days without update - 🚨

### Next Steps Check
- **Clear:** Next step defined with owner and date - ✅
- **Vague:** Next step exists but unclear - ⚠️
- **Missing:** No next step documented - 🚨

### Risk Indicators
- Keywords: "ghosting", "went dark", "waiting", "blocked", "concern", "competitor"
- Missing stakeholders (no champion, no economic buyer)
- Extended timeline (deal age > typical sales cycle)

### Deadline Check
- Deals with close dates in next 7 days
- Deals with next steps overdue
- Deals with proposal expirations

---

## Step 3: Cross-Reference Context

Enhance deal intelligence:

1. **Check person pages** for stakeholders
   - When did we last talk to them?
   - Any concerns noted?
   - Relationship strength?

2. **Search meeting notes** (last 30 days)
   - Recent conversations about this deal
   - Concerns raised
   - Commitments made

3. **Check for patterns**
   - Multiple deals stuck at same stage?
   - Common blockers across deals?

---

## Step 4: Generate Deal Review

Present findings in this format:

```markdown
# 💼 Deal Review

**Date:** [Today's date]
**Active deals:** [Count]
**Total pipeline value:** [Sum if values available]
**Deals reviewed:** [Count]

---

## 🚨 Needs Immediate Attention

### [Company Name] - [Deal Size if known]
**Status:** Stale (15 days since update)
**Stage:** Proposal
**Risk:** High
**Last activity:** [Date] - [What happened]
**Issue:** No activity since sending proposal. Possible ghosting.
**Next step:** Follow up with champion [Name] ASAP

---

## ⚠️ Watch List

[Deals that need attention soon but not urgent]

### [Company Name]
**Status:** Aging (8 days since update)
**Stage:** Discovery
**Risk:** Medium
**Last activity:** Demo on [Date]
**Issue:** No follow-up scheduled
**Next step:** Schedule discovery call this week

---

## ✅ On Track

[Deals with recent activity and clear next steps]

### [Company Name] - $XX,XXX
**Stage:** Contract Review
**Last activity:** 2 days ago - Sent contract
**Next step:** Review call with Legal on [Date]
**Close date:** [Date]
**Confidence:** High

---

## 📅 Closing Soon (Next 7 Days)

### [Company Name] - $XX,XXX
**Close date:** [Date] (4 days)
**Stage:** Contract Review
**Status:** On track
**Final steps:**
- [ ] Legal review complete
- [ ] Signatures collected
- [ ] Payment terms confirmed

---

## 🎯 Key Insights

**Stage distribution:**
- Discovery: [X deals]
- Demo: [X deals]
- Proposal: [X deals]
- Negotiation: [X deals]
- Contract: [X deals]

**Common blockers:**
1. [Blocker 1] - affecting [X] deals
2. [Blocker 2] - affecting [X] deals

**Recommended actions:**
1. [Top priority action]
2. [Second priority action]
3. [Third priority action]

---

## 📊 Pipeline Health Score

**Overall health:** [Good / Needs Attention / At Risk]

- ✅ Healthy deals: [X]
- ⚠️ Watch list: [X]
- 🚨 At risk: [X]
- Stale (10+ days): [X]
- Missing next steps: [X]
```

---

## Step 5: Offer Follow-Up Actions

After presenting the review, ask:

> "Want me to:
> 1. Draft follow-up email for [stale deal]?
> 2. Prep for upcoming call with [company]?
> 3. Update a specific deal with current status?
> 4. Deep dive on deals stuck in [stage]?"

---

## Stage Filtering

When user specifies a stage, focus on:

1. All deals in that stage
2. How long they've been in that stage
3. What typically moves deals out of this stage
4. Specific risks for this stage

**Common stages:**
- **Discovery:** New opportunities, qualification
- **Demo:** Product demonstration scheduled/completed
- **Proposal:** Pricing/proposal sent
- **Negotiation:** Terms discussion, stakeholder alignment
- **Contract:** Legal review, signatures

---

## Timeframe Filtering

When user specifies timeframe:

1. Filter to deals with close dates in that window
2. Add urgency indicators
3. Check if timeline is realistic given stage
4. Identify what needs to happen to close on time

---

## Integration with Other Skills

- **After running:** Suggest `/call-prep [company]` for at-risk deals
- **If staleness detected:** Suggest `/account-plan` to re-engage
- **For pattern issues:** Suggest reviewing process with `/process-audit`

---

## Example Output

```markdown
# 💼 Deal Review

**Date:** 2026-01-28
**Active deals:** 12
**Total pipeline value:** $847K
**Deals reviewed:** 12

---

## 🚨 Needs Immediate Attention

### TechStart Inc - $75K
**Status:** Stale (18 days since update)
**Stage:** Proposal
**Risk:** High - Possible Lost
**Last activity:** Jan 10 - Sent proposal after successful demo
**Issue:** No response to proposal or 3 follow-up emails. Champion Mike not responding.
**Next step:** Last-ditch call to Mike today. Escalate to VP if no response.

### DataFlow Corp - $120K
**Status:** Competitor risk
**Stage:** Negotiation
**Risk:** High
**Last activity:** 3 days ago - They mentioned evaluating ProductX
**Issue:** Product team showed them ProductX demo. Concerned about our dashboard capabilities.
**Next step:** Executive alignment call scheduled Friday. Prep competitive positioning.

---

## ⚠️ Watch List

### GlobalCo - $95K
**Status:** Aging (9 days since update)
**Stage:** Discovery
**Risk:** Medium
**Last activity:** Jan 19 - Discovery call with Sarah (CTO)
**Issue:** No follow-up call scheduled. She mentioned needing to discuss with team.
**Next step:** Follow up this week to schedule demo

### InnovateCo - $45K
**Status:** Vague next steps
**Stage:** Demo
**Risk:** Medium
**Last activity:** 5 days ago - Demo with product team
**Issue:** Next step says "follow up" but no date or specific action
**Next step:** Schedule proposal review call with timeline

---

## ✅ On Track

### Acme Corp - $180K
**Stage:** Contract Review
**Last activity:** Yesterday - Contract sent to Legal
**Next step:** Legal review call on Thursday
**Close date:** Feb 5
**Confidence:** High - Champion Sarah is actively driving this

### FastGrow - $60K
**Stage:** Proposal
**Last activity:** 2 days ago - Proposal presentation
**Next step:** Decision call scheduled for Friday
**Close date:** Feb 15
**Confidence:** Medium-High - Positive response, waiting on budget approval

### StartupX - $40K
**Stage:** Contract
**Last activity:** Today - Signatures received
**Next step:** Process payment
**Close date:** This week
**Confidence:** Very High - Deal done, just processing

---

## 📅 Closing Soon (Next 7 Days)

### StartupX - $40K
**Close date:** Jan 30 (2 days)
**Stage:** Contract - Signatures received
**Status:** Processing

### NewCorp - $55K
**Close date:** Feb 2 (5 days)
**Stage:** Negotiation
**Status:** On track - final terms discussion tomorrow

---

## 🎯 Key Insights

**Stage distribution:**
- Discovery: 3 deals ($220K)
- Demo: 2 deals ($105K)
- Proposal: 4 deals ($295K)
- Negotiation: 2 deals ($175K)
- Contract: 1 deal ($52K)

**Common blockers:**
1. **Dashboard capabilities** - 2 deals expressing concern (DataFlow, NewCorp)
2. **Budget approval timing** - 3 deals waiting on Q1 budget (FastGrow, GlobalCo, StartupX)

**Recommended actions:**
1. **Re-engage TechStart today** - 18 days stale, high value, likely lost if no action
2. **Prep competitive positioning for DataFlow** - Friday call critical, ProductX threat
3. **Follow up with GlobalCo and InnovateCo** - Both aging, need clear next steps

---

## 📊 Pipeline Health Score

**Overall health:** Needs Attention

- ✅ Healthy deals: 6 ($387K)
- ⚠️ Watch list: 4 ($260K)
- 🚨 At risk: 2 ($195K)
- Stale (10+ days): 1 ($75K)
- Missing next steps: 2 ($140K)

**Critical:** TechStart and DataFlow need immediate action this week.
```
