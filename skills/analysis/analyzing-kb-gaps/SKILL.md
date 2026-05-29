---
name: analyzing-kb-gaps
description: Use when you have Knowledge Base exports and want to identify user pain points, missing articles, and AI assistance opportunities.
---

# Analyzing KB Gaps

## Overview

Uses the Knowledge Base as a proxy for where users struggle. Identifies high-volume topics, missing guidance, and opportunities for better self-service or AI-assisted resolution.

## When to Use

- Have KB article exports to analyze
- Want to understand what users struggle with most
- Exploring AI assistant opportunities
- Planning documentation improvements

## Core Pattern

**Step 1: Gather Sources**

Read files in:
- `inputs/knowledge_base/` - KB article exports
- `outputs/insights/voc-synthesis-*.md` - VOC insights (if available, for correlation)

**Step 2: Analyze Article Coverage**

For each KB article (or category), note:
- Topic / Category
- Article count
- Last updated date
- Estimated complexity (simple how-to vs. complex troubleshooting)

**Step 3: Identify Gaps**

Look for:
1. **High-volume topics** - Many articles = users struggle here
2. **Outdated articles** - Not updated in 6+ months
3. **Missing topics** - VOC mentions issues with no KB coverage
4. **Complex troubleshooting** - Multi-step processes that could be simplified

**Step 4: Assess AI Opportunities**

For each gap, evaluate:

| Opportunity Type | Criteria | Risk Level |
|------------------|----------|------------|
| Better search/IA | Hard to find articles | Low |
| Guided resolution | Multi-step process | Low-Medium |
| AI-assisted | Can be automated with citations | Medium |
| **DO NOT automate** | Compliance, billing, trust-sensitive | High |

**Step 5: Generate Output**

Write to `outputs/insights/kb-gaps-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: analyzing-kb-gaps
sources:
  - inputs/knowledge_base/*.md
  - outputs/insights/voc-synthesis-*.md (if used)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# KB Gap Analysis: [Date]

## Executive Summary
[2-3 sentences: What's the state of KB? Where are the biggest gaps?]

## Coverage Overview

| Category | Article Count | Last Updated | Complexity | Gap Score |
|----------|---------------|--------------|------------|-----------|
| [Category 1] | N | YYYY-MM-DD | Simple/Complex | High/Med/Low |
| ... | ... | ... | ... | ... |

## High-Volume Topics
*Categories with most articles (signal: users struggle here)*

| Topic | Article Count | Sample Titles | VOC Correlation |
|-------|---------------|---------------|-----------------|
| [Topic] | N | [title1, title2] | [Yes/No/Unknown] |

## Missing / Outdated Articles

| Gap | Type | Evidence | Priority |
|-----|------|----------|----------|
| [Topic with no article] | Missing | VOC mentions in [file] | High |
| [Article X] | Outdated | Last updated [date] | Medium |

## AI Opportunity Assessment

### Safe to Automate (Low Risk)
| Opportunity | Type | Rationale |
|-------------|------|-----------|
| [Better search for X] | Search/IA | Articles exist but hard to find |
| [Guided wizard for Y] | Guided resolution | Clear steps, no judgment needed |

### Automate with Caution (Medium Risk)
| Opportunity | Type | Guardrails Needed |
|-------------|------|-------------------|
| [AI assist for Z] | AI-assisted | Must cite source article, human review |

### DO NOT Automate (High Risk)
| Topic | Reason |
|-------|--------|
| [Billing disputes] | Financial, requires human judgment |
| [Data deletion] | Compliance, irreversible |
| [Access control] | Trust/security sensitive |

## Recommendations
1. **[Recommendation]** — Evidence: [source]
2. ...

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [High volume in X] | Evidence | [article count] |
| [Users struggle with Y] | Evidence | [VOC file] |
```

**Step 6: Copy to History & Update Tracker**

- Copy to `history/analyzing-kb-gaps/kb-gaps-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Risk Level | Examples | Action |
|------------|----------|--------|
| Low | Search improvements, FAQ bots | Safe to build |
| Medium | Troubleshooting assistants | Build with guardrails |
| High | Billing, compliance, security | Human only |

## Common Mistakes

- **Counting wrong:** "Many articles" → Exact count: "47 articles"
- **Missing VOC correlation:** KB analysis in isolation → Cross-reference with VOC
- **Underestimating risk:** "AI can handle billing" → Compliance topics need humans
- **No priorities:** "Everything is a gap" → Rank by impact
- **Stale analysis:** Using old VOC → Check VOC synthesis date

## Verification Checklist

- [ ] All KB files read
- [ ] Article counts accurate
- [ ] Outdated articles identified (6+ months)
- [ ] VOC correlation checked (if available)
- [ ] AI opportunities categorized by risk
- [ ] DO NOT automate list includes compliance/billing/trust topics
- [ ] Recommendations backed by evidence
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [47 articles on X] | Evidence | [KB export count] |
| [Users complain about Y] | Evidence | [VOC file:line] |
| [Safe to automate Z] | Assumption | [no compliance concern identified] |
