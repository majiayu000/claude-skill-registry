---
name: terms-analyzer
description: Analyze terms of service and privacy policies to identify concerning clauses, hidden permissions, and user rights implications
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Terms of Service Analyzer

> Decode complex terms of service and privacy policies to identify concerning clauses, hidden permissions, and implications for users.

## When to Use This Skill

- Evaluating new SaaS tools
- Assessing platform policies
- Comparing competitor terms
- Due diligence on acquisitions
- Consumer protection analysis

## Methodology Foundation

Based on **consumer protection frameworks** and **EFF/ToS;DR guidelines**, analyzing:
- Data usage and ownership
- Liability limitations
- Arbitration clauses
- Change provisions
- Termination rights

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Identifies key clauses | Risk tolerance |
| Flags concerning terms | Whether to accept |
| Compares to standards | Alternative tools |
| Summarizes rights | Business necessity |
| Rates overall fairness | Action to take |

## Instructions

### Step 1: Document Overview

**Initial Assessment:**
| Element | What to Capture |
|---------|-----------------|
| Service | What the product does |
| Provider | Company and jurisdiction |
| Last Updated | Currency of terms |
| Length | Complexity indicator |
| Readability | Plain language or legalese |

### Step 2: Key Clause Categories

**Critical Clauses to Analyze:**

| Category | What to Find | Risk Signal |
|----------|--------------|-------------|
| **Data Ownership** | Who owns your content | "Perpetual, irrevocable license" |
| **Data Usage** | How they use your data | "Any purpose", "train AI" |
| **Data Sharing** | Third-party access | "Partners", "affiliates" |
| **Termination** | Can they cancel you | "At sole discretion" |
| **Changes** | Can they modify terms | "Without notice" |
| **Liability** | What they're liable for | "In no event" disclaimers |
| **Disputes** | How conflicts resolve | Mandatory arbitration |
| **Account Data** | What happens on deletion | No deletion guarantee |

### Step 3: Rights Assessment

**User Rights Checklist:**

| Right | Status | Clause |
|-------|--------|--------|
| Data portability | Yes/No/Limited | § reference |
| Account deletion | Yes/No/Limited | § reference |
| Content ownership | Yes/No/Limited | § reference |
| Privacy controls | Yes/No/Limited | § reference |
| Opt-out options | Yes/No/Limited | § reference |
| Refund rights | Yes/No/Limited | § reference |

### Step 4: Red Flag Analysis

**Common Problematic Clauses:**

| Red Flag | What It Means | Severity |
|----------|---------------|----------|
| "Perpetual license" | They keep your data forever | High |
| "Sole discretion" | They decide everything | High |
| "Without notice" | No warning of changes | Medium |
| "Mandatory arbitration" | Can't sue in court | Medium |
| "Class action waiver" | Can't join lawsuits | Medium |
| "Unilateral modification" | Can change anytime | Medium |
| "Indemnification" | You pay their legal fees | High |
| "No refunds" | No money back ever | Low-Medium |

### Step 5: Generate Summary

**Output Format:**
1. Service overview
2. Overall grade (A-F or Good/Caution/Avoid)
3. Key findings summary
4. Detailed clause analysis
5. Rights checklist
6. Red flags
7. Comparison to alternatives
8. Recommendations

## Examples

### Example 1: Full ToS Analysis

**Input:**
```
Analyze these ToS excerpts:

"By using our Service, you grant us a worldwide, non-exclusive,
royalty-free, sublicensable, transferable license to use, reproduce,
modify, distribute, and display your Content in connection with
operating and improving the Service and developing new products."

"We may modify these Terms at any time. Continued use constitutes
acceptance of modified Terms."

"All disputes will be resolved through binding arbitration in
accordance with AAA rules. You waive any right to participate
in class actions."

"We may terminate your account at our sole discretion with or
without cause and with or without notice."
```

**Output:**
```
## Terms of Service Analysis

### Service Overview
Provider: [Service Name]
Type: [SaaS/Platform/etc.]
Analysis Date: 2026-01-31

---

### Overall Grade: C- (CAUTION)

This ToS contains several concerning clauses that significantly
favor the provider. Users should be aware of limited rights
before signing up.

---

### Key Findings Summary

| Area | Status | Concern Level |
|------|--------|---------------|
| Data Rights | Problematic | HIGH |
| Terms Changes | Problematic | MEDIUM |
| Dispute Resolution | Restrictive | MEDIUM |
| Termination | One-Sided | HIGH |

---

### Detailed Clause Analysis

#### 1. Content License (HIGH CONCERN)

**Clause:**
> "...worldwide, non-exclusive, royalty-free, sublicensable,
> transferable license to use, reproduce, modify, distribute,
> and display your Content in connection with operating and
> improving the Service and developing new products."

**Analysis:**

| Term | Meaning | Concern |
|------|---------|---------|
| Worldwide | Any country | Standard |
| Non-exclusive | You keep rights too | Good |
| Royalty-free | No payment to you | Expected |
| **Sublicensable** | They can give to others | CONCERNING |
| **Transferable** | Survives if they're sold | CONCERNING |
| **Developing new products** | Beyond operating service | PROBLEMATIC |

**What This Means:**
- Your content can be used to train AI or build new features
- They can sell/transfer your content in an acquisition
- "Improving the Service" is standard; "developing new products" is not

**Industry Standard:** Most services limit to "operating and providing
the Service" without the "new products" language.

**Recommendation:** If uploading sensitive content, consider if
you're comfortable with it being used beyond the core service.

---

#### 2. Terms Modification (MEDIUM CONCERN)

**Clause:**
> "We may modify these Terms at any time. Continued use constitutes
> acceptance of modified Terms."

**Analysis:**
- No notice requirement
- No opt-out period
- Acceptance by inaction

**What This Means:**
Terms could change tomorrow and using the service = agreeing.

**Better Standard:** "30 days notice with right to terminate"

**Recommendation:** Periodically review terms, especially before
renewal dates.

---

#### 3. Arbitration Clause (MEDIUM CONCERN)

**Clause:**
> "All disputes will be resolved through binding arbitration...
> You waive any right to participate in class actions."

**Analysis:**

| Element | Impact |
|---------|--------|
| Binding arbitration | Can't go to court |
| AAA rules | Expensive, but structured |
| Class action waiver | Can't join mass lawsuits |

**What This Means:**
- Individual disputes only
- Arbitration can cost thousands
- Small claims may not be worth pursuing

**Context:** Common in US tech companies, may not be enforceable
in some jurisdictions (EU).

**Recommendation:** Acceptable for business use; concerning for
consumer services where individual damage may be small.

---

#### 4. Termination (HIGH CONCERN)

**Clause:**
> "We may terminate your account at our sole discretion with or
> without cause and with or without notice."

**Analysis:**
- No reason needed
- No warning required
- Complete discretion

**What This Means:**
You could lose access tomorrow with no explanation or recourse.

**Better Standard:** "Termination for violation of Terms with
14 days to cure, or immediately for material breach"

**Recommendation:** Do not rely on this service for critical
business functions without data backup strategy. Consider what
happens to your data on termination.

---

### Rights Checklist

| Right | Status | Notes |
|-------|--------|-------|
| Own your content | Partial | Broad license granted |
| Export data | Unknown | Not addressed |
| Delete account | Unknown | Not addressed |
| Dispute in court | No | Arbitration only |
| Notice of changes | No | No requirement |
| Reason for termination | No | "Sole discretion" |

---

### Red Flags Summary

| Flag | Severity | Clause |
|------|----------|--------|
| "Developing new products" license | HIGH | §3 |
| Termination without notice | HIGH | §12 |
| Class action waiver | MEDIUM | §15 |
| Modification without notice | MEDIUM | §2 |

---

### Comparison to Alternatives

| Feature | This Service | Industry Better Practice |
|---------|--------------|--------------------------|
| Content license | New products | Operating service only |
| Terms changes | No notice | 30-day notice |
| Termination | No cause/notice | Cause + cure period |
| Disputes | Arbitration only | Court option preserved |

---

### Recommendations

1. **For Personal Use:** Consider alternatives with fairer terms
2. **For Business Use:**
   - Negotiate enterprise agreement if possible
   - Ensure data backup procedures
   - Document all content uploaded
   - Set calendar reminders to review terms changes
3. **Data Strategy:** Don't upload anything you wouldn't want
   used for "new products"
```

### Example 2: Quick Privacy Policy Check

**Input:**
```
Quick check - is this privacy policy concerning?
"We may share your information with our affiliates and business
partners for marketing purposes."
```

**Output:**
```
## Quick Privacy Analysis

### Verdict: CONCERNING

---

### Clause Breakdown

> "We may share your information with our affiliates and business
> partners for marketing purposes."

| Term | Meaning | Concern |
|------|---------|---------|
| "affiliates" | Related companies | Medium - often broad |
| "business partners" | Anyone they work with | HIGH - undefined |
| "marketing purposes" | Advertising to you | HIGH - not service-related |

---

### What This Means

- Your data can go to undefined third parties
- You'll likely receive marketing from companies you never chose
- "Business partners" could be hundreds of companies

---

### Questions to Ask

1. Can you opt out of partner sharing?
2. Who are these "business partners"?
3. Is consent required or is it opt-out?

---

### Better Language

"We may share your information with affiliates solely to provide
the Service. We will not share your information with third parties
for marketing purposes without your explicit consent."

---

### Recommendation

Check for:
- [ ] Opt-out mechanism in privacy settings
- [ ] List of specific partners
- [ ] GDPR/CCPA rights section
- [ ] Data selling disclosure

If no opt-out exists, this service will share your data widely.
```

## Skill Boundaries

### What This Skill Does Well
- Identifying concerning clauses
- Explaining legal language
- Comparing to standards
- Flagging risks

### What This Skill Cannot Do
- Provide legal advice
- Know all jurisdictional variations
- Predict enforcement
- Guarantee interpretation

### When to Escalate to Human
- Enterprise agreement negotiation
- Regulated industry implications
- Cross-border data concerns
- Contract disputes

## Iteration Guide

**Follow-up Prompts:**
- "What should I negotiate for an enterprise agreement?"
- "Compare this to [competitor]'s terms"
- "What questions should I ask their sales team?"
- "Draft a request for term modifications"

## References

- ToS;DR (Terms of Service; Didn't Read)
- EFF Privacy Analysis Frameworks
- EDPB Guidelines on Transparency
- FTC Unfair Business Practices

## Related Skills

- `contract-review` - Full contract analysis
- `gdpr-compliance` - Privacy specifics
- `competitive-analysis` - Compare services

## Skill Metadata

- **Domain**: Legal / Consumer
- **Complexity**: Beginner-Intermediate
- **Mode**: cyborg
- **Time to Value**: 15-30 min
- **Prerequisites**: ToS document access
