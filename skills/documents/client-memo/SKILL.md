---
name: client-memo
description: >-
  Drafts structured client memoranda translating legal analysis and strategic
  recommendations into plain language for non-lawyer audiences. Covers corporate
  governance, fiduciary duties, compliance, and transactional advice. Enforces
  standard memo architecture: heading block, executive summary, background,
  analysis, options, and recommendations. Use when preparing client-facing memos,
  opinion letters, or governance briefings.
---

# Client Memo

Produces client-facing memoranda that translate corporate governance legal issues into clear analysis and actionable recommendations for non-lawyer decision-makers.

## Prerequisites

1. **Matter description** — client name, entity type, jurisdiction, subject matter
2. **Supporting documents** — contracts, board minutes, correspondence, filings, prior opinions
3. **Legal questions** — specific issues or decisions the client faces
4. **Deadlines** — filing dates, board meetings, regulatory timelines

## Quick Start

1. Gather matter details and supporting documents from the user
2. Identify the legal questions to address
3. Draft memo following the Output Structure below
4. Mark any uncertain citations `[VERIFY]` and flag factual gaps as Open Items
5. Label the draft Attorney-Client Privileged / Work Product

## Output Structure

### Heading Block

| Field | Content |
|---|---|
| TO | [Client name / contact] |
| FROM | [Firm / attorney name] |
| DATE | [Date] |
| RE | [Matter — specific subject] |
| CONFIDENTIAL | Attorney-Client Privileged |

### 1. Executive Summary

- 2–4 sentences: issue, bottom-line conclusion, immediate next steps
- Plain language; no citations; written for a CEO or board chair

### 2. Background

- Chronological narrative from uploaded documents
- Key parties, dates, agreements, events
- Flag factual gaps needing client clarification

### 3. Legal Analysis

- Labeled subsection per issue
- Structure: **Rule → Application → Conclusion**
- Translate citations into business-impact terms
- Note controlling authority and any majority/minority splits

### 4. Strategic Options (if applicable)

| Option | Description | Risks | Benefits |
|---|---|---|---|
| A | | | |
| B | | | |
| C | | | |

### 5. Recommendations

- Numbered actionable steps
- Assign responsibility (client vs. counsel) and deadline per item
- Identify decisions required before counsel can proceed

### 6. Open Items

- Facts, documents, or clarifications needed to complete the analysis

## Pitfalls and Checks

- **Privilege**: Always label drafts Attorney-Client Privileged / Work Product
- **Citations**: Include statute/regulation/case with one-sentence plain-English gloss; mark uncertain citations `[VERIFY]`
- **Scope**: US-focused by default; flag foreign law, state-specific rules, or non-US entities explicitly
- **No guarantees**: Frame conclusions as analysis, not outcome predictions; qualify where law is unsettled or facts incomplete
- **Tone**: Professional and direct; avoid legalese but keep precision on operative legal terms
