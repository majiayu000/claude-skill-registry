---
name: genres
description: '> Style/formatting: Follow ~/.claude/skills/word-doc-generator/SKILL.md'
---

# POLICY ASSESSMENT REPORT - Genre Template

> **Style/formatting:** Follow `~/.claude/skills/word-doc-generator/SKILL.md`

## Purpose

Assessment of regulatory and policy environment for business decisions. Analyzes legislative landscape, regulatory trends, and compliance requirements.

---

## REPORT STRUCTURE

### Required Sections (In Order)


1. **Executive Summary** → `sections/universal/EXECUTIVE_SUMMARY.skill.md`


2. **Regulatory Landscape**


3. **Key Stakeholders**


4. **Policy Trends**


5. **Compliance Requirements**


6. **Risk Assessment**



---

## ALLOWED_ACTIONS

These actions define the research scope for this genre:


- `SEARCH_REGULATORY`

- `SEARCH_NEWS`

- `SEARCH_WEBSITE`

- `SEARCH_SANCTIONS`

- `SEARCH_PEP`


---

## STANDARD INTRODUCTION

```markdown
## Introduction

This report has been prepared at the request of [CLIENT] and sets out the results of policy assessment report research on **[SUBJECT NAME]** (the "Subject").

### Scope of Engagement

Assessment of regulatory and policy environment for business decisions. Analyzes legislative landscape, regulatory trends, and compliance requirements.

### Methodology

Research was conducted using open-source intelligence methods including official registries, financial databases, regulatory registers, court records, and media archives.

### Subject Identification

| Field | Details |
|-------|---------|
| **Subject Name** | [NAME] |
| **Subject Type** | [Company/Person] |
| **Jurisdiction** | [COUNTRY] |
| **Report Date** | [DATE] |
```

---

## STANDARD CONCLUSION

```markdown
## Conclusion

Based on the research conducted, **[SUBJECT]** [SUMMARY ASSESSMENT - 1-2 sentences].

### Key Findings

[POSITIVE:]
- [FINDING 1]
- [FINDING 2]

[CONCERNS (if any):]
- [CONCERN 1]
- [CONCERN 2]

### Limitations

This report is based on publicly available information as of [DATE]. See Research Methodology section for details.
```

---

## TYPICAL SOURCES


- Government websites

- Regulatory announcements

- Policy papers

- Trade associations

- News and analysis


---

## VOICE AND STYLE

| Attribute | Value |
|-----------|-------|
| **Voice** | First Plural |
| **Formality** | Analytical |
| **Stance** | Neutral Observer |

---

## DISCLAIMERS

**See `library/DISCLAIMERS.skill.md`** for standard disclaimers.

---

## FOOTNOTE FORMAT

**See `word-doc-generator/SKILL.md`** - URL-only footnotes.

---

## TYPICAL DURATION

5-7 business days

---

## JURISDICTION COVERAGE

For jurisdiction-specific guidance (registry URLs, legal forms, filings), refer to:
`jurisdictions/[COUNTRY].skill.md`

---

## MINED DATA

This genre template was generated from 20 mined reports.