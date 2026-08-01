---
name: genres
description: '> Style/formatting: Follow ~/.claude/skills/word-doc-generator/SKILL.md'
---

# INTEGRITY CHECK - Genre Template

> **Style/formatting:** Follow `~/.claude/skills/word-doc-generator/SKILL.md`

## Purpose

Quick integrity screening covering sanctions, watchlists, adverse media, and basic court records. Suitable for lower-risk assessments.

---

## REPORT STRUCTURE

### Required Sections (In Order)


1. **Subject Identification**


2. **Sanctions and Watchlists** → `sections/universal/SANCTIONS_WATCHLISTS.skill.md`


3. **Adverse Media** → `sections/universal/ADVERSE_MEDIA.skill.md`


4. **Court Records**


5. **Assessment Summary**



---

## ALLOWED_ACTIONS

These actions define the research scope for this genre:


- `SEARCH_SANCTIONS`

- `SEARCH_PEP`

- `SEARCH_COURT`

- `SEARCH_NEWS`

- `SEARCH_REGISTRY`


---

## STANDARD INTRODUCTION

```markdown
## Introduction

This report has been prepared at the request of [CLIENT] and sets out the results of integrity check research on **[SUBJECT NAME]** (the "Subject").

### Scope of Engagement

Quick integrity screening covering sanctions, watchlists, adverse media, and basic court records. Suitable for lower-risk assessments.

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


- Sanctions databases

- PEP lists

- News archives

- Court databases

- Corporate registries


---

## VOICE AND STYLE

| Attribute | Value |
|-----------|-------|
| **Voice** | Third Person |
| **Formality** | Professional |
| **Stance** | Neutral Observer |

---

## DISCLAIMERS

**See `library/DISCLAIMERS.skill.md`** for standard disclaimers.

---

## FOOTNOTE FORMAT

**See `word-doc-generator/SKILL.md`** - URL-only footnotes.

---

## TYPICAL DURATION

1-2 business days

---

## JURISDICTION COVERAGE

For jurisdiction-specific guidance (registry URLs, legal forms, filings), refer to:
`jurisdictions/[COUNTRY].skill.md`

---

## MINED DATA

This genre template was generated from 8 mined reports.