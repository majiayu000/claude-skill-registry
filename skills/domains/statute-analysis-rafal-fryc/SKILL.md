---
name: statute-analysis-rafal-fryc
description: Guide for reading, interpreting, and applying statutes, regulations, and rules in legal and compliance contexts. Use when the user asks about (1) how to read and interpret statutes, regulations, or rules, (2) statutory interpretation methods and canons of construction, (3) understanding legislative intent, (4) applying statutes to specific legal situations, (5) extracting requirements from legal text, (6) distinguishing between different types of legal requirements, or (7) cross-jurisdictional compliance analysis.
metadata:
  author: Rafał Stanisław Fryc
  license: AGPL-3.0
  version: 2026.01.14
---

# Statutory Interpretation Guide

## When to Use This Skill

Use this skill when the user asks about:
- How to read and interpret statutes, regulations, or rules
- Statutory interpretation methods and canons of construction
- Understanding legislative intent
- Applying statutes to specific legal situations
- Extracting requirements from legal text
- Distinguishing between different types of legal requirements
- Cross-jurisdictional compliance analysis

---

## Understanding the Legal Hierarchy

### Statutes vs. Regulations vs. Rules

| Type | Created By | Characteristics |
|------|------------|-----------------|
| **Statute** | Legislature (Congress, state legislature) | Formal written enactment; commands, prohibits, or declares policy; provides framework |
| **Regulation** | Government agency | Implements statutes; more detailed than statutes; has force of law |
| **Rule** | Government agency or court | Another term for regulation (administrative rules) or procedural requirements |

**Key Insight:** Statutes give agencies authority to create regulations. Always read BOTH the statute AND implementing regulations for complete understanding. The regulation often contains the operational details that the statute leaves to agency discretion.

---

## Before Reading: Preliminary Steps

### 1. Verify Currency and Status

Before analyzing any statute:
- [ ] Check the effective date (may be future)
- [ ] Determine if amendments are pending
- [ ] Find the consolidated/codified version
- [ ] Identify implementing regulations
- [ ] Check for court decisions interpreting the statute
- [ ] Note multiple effective dates for different provisions

**Lesson:** The statute as passed may not be the statute as implemented. A statute with a future effective date may be amended before taking effect.

### 2. Understand the Regulatory Ecosystem

- [ ] Identify the enforcement agency
- [ ] Research the agency's enforcement history
- [ ] Check for guidance documents, FAQs, or informal interpretations
- [ ] Determine if the agency is known for aggressive or permissive enforcement

**Lesson:** The same statutory language can mean different things depending on who enforces it.

### 3. Browse the Structure First

State statutes are organized by topic and subtopic. Before diving into specific sections:
- Browse the index or table of contents
- Understand how your issue fits in the larger whole
- Note the overall organizational pattern

---

## Reading the Statute: Core Techniques

### Start with Definitions

**Every word has meaning.** Find the definitions section first and reference it constantly.

- Terms may have specific statutory meanings that differ from common usage
- Definitions may incorporate external standards by reference
- Some definitions depend on other definitions (creating interconnected webs)
- Watch for whether definitions are exhaustive ("means") or illustrative ("includes")

**Practical Tip:** Create a reference sheet of key definitions before analyzing substantive provisions.

### Read Slowly and Carefully

Statutes are dense. Every word AND punctuation mark has meaning.
- Read each sentence multiple times
- Parse complex sentences into their component parts
- Don't skim—statutory language rewards close attention

### The Operator Words

These words have consistent legal functions across all statutes:

| Term | Meaning |
|------|---------|
| **Shall** | Mandatory—you are REQUIRED to do this |
| **May** | Permissive—you are ALLOWED to do this |
| **And** | Conjunctive—ALL elements must be satisfied |
| **Or** | Disjunctive—ANY ONE element is sufficient |
| **Unless / Except** | Signals an exception to the general rule |
| **Subject to** | This provision is limited by another section |
| **Notwithstanding** | This provision applies DESPITE what other sections say |
| **If...then / Upon / Provided that** | A precondition must be satisfied |
| **Means** | Exhaustive definition follows |
| **Includes** | Examples follow (may not be exhaustive) |

**Critical Warning:** Misreading "and" as "or" or "shall" as "may" fundamentally changes a provision's meaning.

### Track Cross-References

When you encounter references to other statutes or sections:
- Stop and read those referenced provisions
- They may expand, limit, or modify the provision you're analyzing
- Build a map of how sections relate to each other

---

## Tools of Statutory Interpretation

When language is ambiguous, use these established methods:

### A. The Text Itself

**Plain Meaning Rule:** Courts assume words mean what an ordinary person would understand. If clear and unambiguous, no further inquiry is needed.

**Dictionary Definitions:** Compare multiple dictionaries for consensus. Use legal dictionaries for technical terms, general dictionaries for common terms.

### B. Canons of Construction

**Textual Canons:**

| Canon | Meaning |
|-------|---------|
| **General-Terms Canon** | General terms get their full scope without arbitrary limitation |
| **Negative-Implication Canon** (Expressio Unius) | Expressing one thing implies exclusion of others |
| **Whole-Act Rule** | Construe the text as a coherent whole |
| **Consistent Usage Presumption** | Same word used repeatedly has the same meaning |
| **Meaningful Variation** | Different terms presumably have different meanings |
| **Surplusage Canon** | Every word should have meaning; avoid rendering words superfluous |
| **Associated Words Canon** (Noscitur a Sociis) | Words grouped together inform each other's meaning |
| **Ejusdem Generis** | General terms following specific ones are limited to the same class |

**Purpose Canons:**

| Canon | Application |
|-------|-------------|
| **Presumption Against Ineffectiveness** | Favor interpretations that further the statute's purpose |
| **Avoiding Absurdity** | Reject interpretations producing absurd results |
| **Remedial Statutes** | Liberally construe to achieve remedial purpose |
| **Rule of Lenity** | Penal statutes strictly construed in favor of defendant |

### C. Legal Interpretations

- **Case Law:** Court decisions interpreting the statute
- **Agency Regulations:** Implementing rules (courts grant deference)
- **Agency Guidance:** FAQs, guidance documents, enforcement actions
- **Legislative History:** Committee reports, floor debates, sponsor statements

### D. Purpose and Context

- **Preamble/Purpose Clauses:** Often state legislative intent explicitly
- **Findings Sections:** Explain the problem the statute addresses
- **Structural Context:** How the provision fits in the overall scheme

---

## Distinguishing Requirement Types

When extracting requirements, categorize by type:

| Type | Examples | Implementation |
|------|----------|----------------|
| **Disclosure** | Privacy notices, warning labels, terms | Legal/policy team; document publication |
| **Operational** | Response deadlines, internal processes | Compliance team; process design |
| **Technical** | System requirements, security standards | Engineering team |
| **UI/Design** | Link placement, font size, button design | Product/design team |

**Key Insight:** A "privacy policy requirements" checklist should not include operational deadlines that never appear in the policy itself. Separate WHAT must be disclosed from HOW the business must operate.

---

## Handling Exemptions

### Entity vs. Data Exemptions

- **Entity exemptions:** The entire organization is exempt
- **Data exemptions:** Only certain data types are exempt; comply for non-exempt data

### Federal Preemption

Most state statutes defer to federal sector-specific laws:
- HIPAA (health), GLBA (financial), FCRA (credit), FERPA (education), etc.

### Delayed Application vs. Exemption

Some entities have delayed compliance deadlines rather than permanent exemptions. Track WHEN the grace period ends.

---

## Applicability Analysis

Before extracting requirements, determine WHO must comply:

### Common Threshold Types

| Type | Examples |
|------|----------|
| **Revenue** | Annual gross revenue > $X million |
| **Volume** | Process data of > X consumers/transactions |
| **Revenue from Activity** | Derive X% of revenue from [regulated activity] |
| **Entity Type** | Applies to [developers/controllers/operators] |

### Conjunctive vs. Disjunctive Thresholds

- **OR (Disjunctive):** Meet ANY threshold = covered
- **AND (Conjunctive):** Must meet ALL thresholds = covered

**Lesson:** A statute requiring "$25M revenue AND 100K consumers" is far more limited than one requiring either condition.

---

## Cross-Jurisdictional Analysis

When analyzing multiple related statutes:

### Look for Patterns

- "Consumer-protective" vs. "business-friendly" orientations
- Common provisions vs. unique outliers
- Standard vs. unusual thresholds
- Model laws that others follow

### Watch for Variations

- Rights may differ (some jurisdictions omit "standard" rights)
- Definitions vary (especially "sale," "sensitive data," thresholds)
- Age-based protections use different cutoffs
- Enforcement mechanisms differ significantly

**Practical Approach:** Identify the most protective standard as a baseline; note where others are more permissive.

---

## Enforcement Analysis

### Factors Affecting Practical Priority

| Factor | Questions to Ask |
|--------|------------------|
| **Enforcement Authority** | Who can enforce? AG only? Private parties? Agency? |
| **Penalties** | Civil, criminal, or administrative? Amount? |
| **Cure Period** | Opportunity to fix before penalties? |
| **Private Right of Action** | Can individuals sue? |
| **Enforcement History** | Is the agency actively enforcing? |

**Lesson:** Two requirements with identical language may have vastly different practical importance depending on enforcement dynamics.

---

## What the Statute Doesn't Say

Compare against typical provisions to identify notable absences:

- [ ] Is there a private right of action? (If not, note explicitly)
- [ ] Are there safe harbors?
- [ ] Are definitions exhaustive or illustrative?
- [ ] What is left to regulatory discretion?
- [ ] What common provisions are notably absent?

**Lesson:** The absence of a remedy or protection is often as significant as what is included.

---

## Consistency and Common Sense

Keep these principles in mind:

1. **Internal Consistency:** Statutes are written to be consistent, not contradictory. If your interpretation creates a conflict, reconsider.

2. **Avoiding Absurdity:** Statutes are written to make sense. If your interpretation leads to an absurd result, it's probably wrong.

3. **Purposive Reading:** Consider what problem the legislature was trying to solve. Interpretations that further that purpose are preferred.

---

## Quick Reference Checklist

### Before Reading
- [ ] Current version verified?
- [ ] Effective date noted?
- [ ] Amendments checked?
- [ ] Implementing regulations identified?
- [ ] Enforcement agency identified?

### During Reading
- [ ] Definitions section located and referenced?
- [ ] Applicability thresholds identified?
- [ ] Cross-references tracked?
- [ ] Operator words (shall/may, and/or) parsed carefully?
- [ ] Exemptions identified and categorized?

### After Reading
- [ ] Requirements categorized by type?
- [ ] Ambiguous terms flagged?
- [ ] Enforcement mechanisms analyzed?
- [ ] Time-based requirements extracted?
- [ ] Notable absences documented?

---

## Navigation

See `references/index.md` for detailed documentation including:
- Comprehensive canons of construction with examples
- Practical lessons from multi-statute analysis
- Detailed checklists and reference tables
