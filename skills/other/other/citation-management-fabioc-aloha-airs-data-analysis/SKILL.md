---
name: "Citation Management"
description: "APA 7th formatting, citation integration, reference validation, and bibliography generation"
---

# Skill: Citation Management

> APA 7th formatting, citation integration, reference validation, and bibliography generation.

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | citation-management |
| **Version** | 1.0.0 |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Prerequisites** | None |
| **Related Skills** | literature-review, academic-paper-drafting |

---

## Overview

Proper citation is the invisible infrastructure of scholarly work. This skill ensures accurate attribution, consistent formatting, and valid references across academic writing.

### Supported Styles

| Style | Primary Use | Key Resource |
|-------|-------------|--------------|
| **APA 7th** | Psychology, social sciences, business | Publication Manual (2019) |
| **Chicago** | History, humanities | Chicago Manual of Style |
| **IEEE** | Engineering, CS | IEEE Reference Guide |
| **Harvard** | UK/Australia academia | Varies by institution |

**Default**: APA 7th (DBA dissertation standard)

---

## Module 1: APA 7th Quick Reference

### In-Text Citations

| Situation | Format | Example |
|-----------|--------|---------|
| One author | (Author, Year) | (Newport, 2016) |
| Two authors | (Author & Author, Year) | (Lee & See, 2004) |
| Three+ authors | (First Author et al., Year) | (Venkatesh et al., 2012) |
| Direct quote | (Author, Year, p. X) | (Newport, 2016, p. 42) |
| Multiple sources | (Author, Year; Author, Year) | (Lee, 2020; Smith, 2021) |
| Same author, same year | (Author, Year-a, Year-b) | (Brown, 2023a, 2023b) |

### Narrative vs. Parenthetical

**Parenthetical** (author in parentheses):
> Trust calibration is essential for human-automation interaction (Lee & See, 2004).

**Narrative** (author in sentence):
> Lee and See (2004) demonstrated that trust calibration is essential for human-automation interaction.

### Page Numbers

Required for:
- Direct quotes
- Paraphrases of specific passages
- Referring to specific figures/tables

Not required for:
- General reference to entire work
- Summarizing main argument

---

## Module 2: Reference List Formatting

### Basic Structure

```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), Page–Page. https://doi.org/xxxxx
```

### Journal Article

```
Venkatesh, V., Thong, J. Y., & Xu, X. (2012). Consumer acceptance and use of information technology: Extending the unified theory of acceptance and use of technology. MIS Quarterly, 36(1), 157-178. https://doi.org/10.2307/41410412
```

**Key rules:**
- Italicize journal name and volume
- Include DOI as hyperlink when available
- Use sentence case for article title
- Use title case for journal name

### Book

```
Newport, C. (2016). Deep work: Rules for focused success in a distracted world. Grand Central Publishing.
```

**Key rules:**
- Italicize book title
- Include publisher (no location since APA 7th)
- Sentence case for title

### Book Chapter

```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book (pp. xx–xx). Publisher.
```

### Conference Paper

```
Schemmer, M., Kuehl, N., Benz, C., Bartos, A., Satzger, G., & Fromm, J. (2023). Appropriate reliance on AI advice: Conceptualization and the effect of explanations. Proceedings of the 28th International Conference on Intelligent User Interfaces, 410-422. https://doi.org/10.1145/3581641.3584066
```

### Website/Online Source

```
Author, A. A. (Year, Month Day). Title of page. Site Name. https://www.url.com
```

### Dissertation/Thesis

```
Correa, F. (2025). AI readiness scale: Extending UTAUT2 to predict enterprise AI adoption [Doctoral dissertation, University Name]. ProQuest Dissertations.
```

---

## Module 3: Common Errors and Fixes

### Formatting Errors

| Error | Incorrect | Correct |
|-------|-----------|---------|
| Ampersand in narrative | Smith & Jones (2020) found... | Smith and Jones (2020) found... |
| Missing comma | (Smith 2020) | (Smith, 2020) |
| Et al. too early | (Smith et al., 2020) for 2 authors | (Smith & Jones, 2020) |
| Italics wrong | *Article Title* | Article title (not italicized) |
| DOI format | doi: 10.xxx | https://doi.org/10.xxx |

### Reference List Errors

| Error | Fix |
|-------|-----|
| Missing DOI | Add if available; most recent articles have DOIs |
| URL instead of DOI | Prefer DOI over URL when both exist |
| Retrieval date included | Only for content that may change (e.g., wiki) |
| Publisher location | Omit in APA 7th (changed from 6th) |
| "Retrieved from" | Omit unless content changes (use DOI directly) |

### Consistency Errors

| Error | Fix |
|-------|-----|
| Inconsistent author names | Use same format throughout |
| Mixed capitalization | Sentence case for titles, title case for journals |
| Orphaned citations | Every in-text citation needs reference list entry |
| Orphaned references | Remove unused references |

---

## Module 4: Citation Verification

### Verification Checklist

**For each in-text citation:**
- [ ] Author name spelled correctly?
- [ ] Year matches reference list?
- [ ] Page number included for quotes?
- [ ] Corresponding entry in reference list?

**For each reference:**
- [ ] All authors listed (up to 20)?
- [ ] Year accurate?
- [ ] Title accurate and correctly capitalized?
- [ ] Journal/publisher accurate?
- [ ] DOI functional (if included)?
- [ ] Formatting matches APA 7th template?

### DOI Validation

```
https://doi.org/10.XXXX/XXXXXXX
```

**Test**: Paste DOI in browser—should resolve to article.

**Finding DOIs:**
- CrossRef: https://www.crossref.org/guestquery
- DOI lookup: https://doi.org

---

## Module 5: Reference Management Tools

### Tool Comparison

| Tool | Pros | Cons | Best For |
|------|------|------|----------|
| **Zotero** | Free, browser integration, groups | Sync limits on free | Individuals, small teams |
| **Mendeley** | Free, PDF annotation | Owned by Elsevier | PDF-heavy workflows |
| **EndNote** | Powerful, institutional | Expensive, complex | Large institutional projects |
| **Paperpile** | Google Docs integration | Subscription | Google ecosystem users |

### Integration Workflow

1. **Capture**: Browser extension captures metadata
2. **Store**: Central library with PDFs
3. **Cite**: Word/Google Docs plugin inserts citations
4. **Generate**: Auto-generate bibliography
5. **Verify**: Manual check against APA 7th

### Manual Backup Strategy

Always keep:
- Exported BibTeX file (portable format)
- Annotated PDF copies
- Citation spreadsheet for complex works

---

## Module 6: Special Cases

### Secondary Sources

When citing a source you read about in another source:

> (Original Author, Year, as cited in Secondary Author, Year)

**Reference list**: Only include the secondary source you actually read.

### Personal Communications

- In-text only: (J. Smith, personal communication, January 15, 2025)
- NOT in reference list (not recoverable)

### Works in Press

```
Author, A. A. (in press). Title. Journal Name.
```

### Retracted Articles

```
Author, A. A. (Year). Title (Retracted). Journal, Volume, Pages. https://doi.org/xxx
```

### AI-Generated Content

APA guidance (as of 2023):
- Cite the AI tool as author
- Include prompt in quotes
- Note that output is not retrievable

```
OpenAI. (2025). ChatGPT (May 2025 version) [Large language model]. https://chat.openai.com
```

---

## Quick Reference Card

### In-Text Patterns

```
One author:    (Smith, 2020)
Two authors:   (Smith & Jones, 2020)
Three+:        (Smith et al., 2020)
Quote:         (Smith, 2020, p. 42)
Narrative:     Smith (2020) argued...
Multiple:      (Jones, 2019; Smith, 2020)
```

### Reference Patterns

```
Journal:  Author. (Year). Title. Journal, Vol(Iss), pp. DOI
Book:     Author. (Year). Title. Publisher.
Chapter:  Author. (Year). Title. In Editor (Ed.), Book (pp.). Publisher.
Web:      Author. (Year, Month Day). Title. Site. URL
```

### Numbers to Remember

| Rule | Value |
|------|-------|
| Et al. threshold | 3+ authors |
| Max authors in reference | 20 (then use ... before last) |
| Hanging indent | 0.5 inch |
| Double spacing | Yes, throughout |
| Alphabetize by | First author's last name |

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "citation", "APA", "reference" | Full skill activation |
| "format this reference", "cite this" | Direct formatting help |
| "check citations", "verify references" | Module 4 verification |
| "in-text citation" | Module 1 quick reference |
| "reference list" | Module 2 formatting |

---

*Skill created: 2026-02-10 | Category: Research | Status: Active*

---

## Synapses

- [.github/skills/literature-review/SKILL.md] (High, Enables, Bidirectional) - "Lit review requires proper citations"
- [.github/skills/academic-paper-drafting/SKILL.md] (High, Enables, Forward) - "Papers need correct citations"
- [.github/skills/dissertation-defense/SKILL.md] (Medium, Supports, Forward) - "Defense references must be accurate"
