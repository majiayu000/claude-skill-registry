---
name: synthesizing-voc
description: Use when you have customer feedback files (transcripts, tickets, surveys) and need to identify themes and opportunities without hallucinating.
---

# Synthesizing VOC

## Overview

Converts raw Voice of Customer data into decision-grade themes and opportunities. Strict protocol prevents hallucination by requiring verbatim quotes, source attribution, and minimum source thresholds.

## When to Use

- Have 3+ interview transcripts, support tickets, or survey responses
- Need to understand "what are customers actually saying?"
- Preparing for roadmap planning or prioritization
- Want to validate assumptions with real customer evidence

## Core Pattern

**Step 1: Validate Sources**

1. List all files in `inputs/voc/`
2. Count total sources
3. **If fewer than 3 sources:**
   - State: "Insufficient sources (found N, need 3+)"
   - List what you found
   - STOP and ask user for more data
4. Read each file completely

**Step 2: Tag Verbatims (Internal)**

Create a mental index:
- Verbatim Quote → Source File → User/Segment (if known)

**DO NOT** summarize or paraphrase at this stage.

**Step 3: Identify Themes**

Find patterns appearing in **3+ separate sources**. For each theme:

| Required | Rule |
|----------|------|
| Core pain point | One sentence, factual |
| Frequency | Exact count of sources |
| Quotes | Up to 3 verbatim (if fewer, say so) |
| Segment | Only if explicitly stated |
| Impact | Only if user explicitly stated |

**Step 4: Generate Output**

Write to `outputs/insights/voc-synthesis-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: synthesizing-voc
sources:
  - inputs/voc/interview-1.md (modified: YYYY-MM-DD)
  - inputs/voc/interview-2.md (modified: YYYY-MM-DD)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# VOC Synthesis: [Date]

## Summary
[2-3 sentences: what did we learn?]

## Themes

| Theme | Frequency | Segment | Impact | Confidence |
|-------|-----------|---------|--------|------------|
| [Theme 1] | N sources | Explicit/Unknown | Explicit/Unknown | High/Med/Low |
| ... | ... | ... | ... | ... |

## Voice of the Customer

### Theme 1: [Name]
**Pain point:** [One sentence]

> "[Verbatim quote 1]"
> — Source: [filename], [user/segment if known]

> "[Verbatim quote 2]"
> — Source: [filename]

### Theme 2: [Name]
...

## Top 5 Opportunities
1. **[Opportunity]** — Evidence: [N sources mention this]
2. ...

## Top 5 Terminology Gaps / Misconceptions
1. **[Term/Concept]** — What users say vs. what we mean
2. ...

## What to Validate Next Week
- [ ] [Specific hypothesis to test]
- [ ] [Question to ask in next interview]

## Recommended Actions
[Only if supported by 3+ sources. Otherwise: "No recommendations; need more data."]

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| ... | Evidence | [file:line] |
```

**Step 5: Copy to History & Update Tracker**

- Copy to `history/synthesizing-voc/voc-synthesis-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Item | Value |
|------|-------|
| Minimum sources | 3 |
| Quote format | Verbatim with source attribution |
| PII handling | Redact as `[REDACTED]` |
| Unknown segments | Label "Unknown", never infer |

## Common Mistakes

- **Paraphrasing:** "User was frustrated" → Use exact words: "This is so annoying"
- **Inferring sentiment:** "They seemed happy" → Only state what's written
- **Assuming segments:** "Probably enterprise" → Only use explicit segment data
- **Recommending without evidence:** "We should build X" → Need 3+ sources
- **Counting wrong:** "Many users said" → Exact count: "4 of 7 sources"

## Verification Checklist

- [ ] Counted sources (minimum 3)
- [ ] All quotes are verbatim (no paraphrasing)
- [ ] Every quote has source file attribution
- [ ] Segment/Impact marked "Unknown" if not explicit
- [ ] PII redacted as [REDACTED]
- [ ] Frequency is exact count, not "many" or "some"
- [ ] Recommendations backed by 3+ sources
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Theme exists] | Evidence | [3+ files cited] |
| [User segment] | Evidence/Unknown | [explicit in source or "Unknown"] |
| [Recommendation] | Evidence | [3+ sources supporting] |
