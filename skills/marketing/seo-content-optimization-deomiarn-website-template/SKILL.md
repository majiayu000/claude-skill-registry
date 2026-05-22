---
name: seo-content-optimization
description: Optimize page content for target keywords. Use per page after building to integrate keywords naturally into headings, text, and i18n files. Reads docs/seo-analysis.md for keyword targets. Triggers on "optimize content for SEO", "keyword optimization", "SEO text", "integrate keywords".
---

# SEO Content Optimization

Optimize page content for target keywords to rank on Google.

## Prerequisites

- **docs/seo-analysis.md** must exist with keyword targets (run `/00_seo-research` first)
- Page must be built (sections installed, i18n added)

## Workflow

1. **Read SEO Analysis** - Get target keywords for this page from docs/seo-analysis.md
2. **Analyze Current Content** - Review existing page, text in components and i18n files
3. **Optimize H1** - Ensure primary keyword is in H1 (naturally)
4. **Optimize Headings** - Include keywords in H2/H3 where relevant
5. **Optimize Body Text** - Integrate keywords naturally (max. 0.8% density)
6. **Optimize Meta** - Title tag and meta description with keywords
7. **Update i18n** - Apply changes to de.json and en.json

## Reading docs/seo-analysis.md

The SEO analysis file contains per-page optimization guides. For each page, find:

### Location in File

```markdown
## Per-Page Optimization Guide

### [Page Name] `/[route]`

**Primary Keyword:** [keyword]
**Search Intent:** [intent]

| Element | Recommendation |
|---------|----------------|
| Title (50-60 chars) | [recommendation] |
| Meta Description (150-160 chars) | [recommendation] |
| H1 | [recommendation] |
| H2 Topics | [list of H2s] |
| Keyword Density | [target] |
| Internal Links | [pages to link] |

**Secondary Keywords to Include:**
- [keyword 1] - use in [section]
- [keyword 2] - use in [section]
```

### What to Extract

For the page you're optimizing, note:
1. **Primary Keyword** - Must be in H1 and title
2. **Title Recommendation** - Use for meta title (50-60 chars)
3. **Meta Description Recommendation** - Use for meta description (150-160 chars)
4. **H1 Recommendation** - The actual H1 text to use
5. **H2 Topics** - What H2 headings should cover
6. **Secondary Keywords** - Where to use them in content
7. **Semantic Keywords** - From the "Semantic Keywords (LSI)" section

## Keyword Integration Rules

**DO:**
- Place primary keyword in H1 (required)
- Include keyword in first 100 words
- Use keyword variations and synonyms
- Write naturally for humans first
- Use keywords in image alt text
- Follow the specific recommendations from seo-analysis.md

**DON'T:**
- Keyword stuff (max. 0.8% density)
- Force unnatural phrasing
- Repeat exact keyword excessively
- Sacrifice readability for SEO

## Content Optimization Checklist

### H1 (Most Important)
- [ ] Contains primary keyword from seo-analysis.md
- [ ] Matches or adapts the H1 recommendation
- [ ] Compelling and clear
- [ ] Only ONE H1 per page
- [ ] Different from meta title (can be similar)

### H2 Headings
- [ ] Cover the H2 Topics listed in seo-analysis.md
- [ ] Include secondary keywords where natural
- [ ] Describe section content accurately
- [ ] Use question format for FAQ keywords

### Body Text
- [ ] Keyword in first paragraph
- [ ] Natural keyword variations throughout
- [ ] Semantic keywords (LSI) from seo-analysis.md included
- [ ] Minimum 300 words per major section

### Meta Title (50-60 chars)
Use the Title recommendation from seo-analysis.md, or follow this format:
```
[Primary Keyword] | [Brand] - [Benefit]
```
Example: `Webdesign Zürich | Local Studios - Professionelle Websites`

### Meta Description (150-160 chars)
Use the Meta Description recommendation from seo-analysis.md, or follow this format:
```
[What you offer] + [Unique value] + [CTA]
```
Example: `Professionelles Webdesign in Zürich für KMUs. Handcodierte Websites ab CHF 100/Monat. Jetzt kostenloses Erstgespräch vereinbaren.`

### Image Alt Text
- [ ] Descriptive and keyword-relevant
- [ ] Not keyword-stuffed
- [ ] Describes actual image content

## Example Optimization

### Step 1: Read seo-analysis.md for Homepage

```markdown
### Homepage `/`

**Primary Keyword:** Webdesign Zürich
**Search Intent:** Transactional/Navigational

| Element | Recommendation |
|---------|----------------|
| Title (50-60 chars) | Webdesign Zürich - Local Studios - Professionelle Websites |
| Meta Description (150-160 chars) | Professionelles Webdesign in Zürich für KMUs. Handcodierte Websites ab CHF 100/Monat. Jetzt kostenloses Erstgespräch vereinbaren. |
| H1 | Webdesign Zürich für KMUs |
| H2 Topics | Unsere Leistungen, Warum wir, Preise, Kundenstimmen |

**Secondary Keywords to Include:**
- "Website erstellen lassen" - use in services section
- "Webdesign Agentur" - use in about section
```

### Step 2: Update i18n

**Before (generic):**
```json
{
  "hero": {
    "title": "Willkommen bei uns",
    "subtitle": "Wir erstellen Websites"
  }
}
```

**After (SEO-optimized using seo-analysis.md):**
```json
{
  "hero": {
    "title": "Webdesign Zürich für KMUs",
    "subtitle": "Professionelle Websites, die Kunden bringen. Handcodiert, schnell, SEO-optimiert."
  }
}
```

## Keyword Density Check

Target: max. 0.8% keyword density

Formula: `(keyword count / total words) × 100`

For a 500-word page targeting "Webdesign Zürich":
- Max occurrences = 0.008 × 500 = 4 times
- Use variations and synonyms to avoid stuffing:
- Include variations: "Webdesign in Zürich", "Zürcher Webdesign", "Website Zürich"

## Output

- Updated messages/de.json with SEO-optimized text
- Updated messages/en.json with SEO-optimized text
- Meta title and description for the page
- All headings optimized for keywords per seo-analysis.md recommendations
