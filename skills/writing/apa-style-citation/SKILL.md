---
name: apa-style-citation
description: |
  Generate, format, and validate academic citations following APA 7th Edition (2019) guidelines.
  Use when user requests: citations, reference lists, bibliographies, in-text citations, or mentions
  "APA style", "APA format", "APA 7", "cite this", "reference list", academic references, or
  scholarly sources. Handles all source types: books, journals, websites, AI tools, social media,
  videos, podcasts, government documents, and edge cases. Can check/correct existing citations
  and generate complete reference lists from research materials.
---

# APA Style Citation

Generate and validate citations following APA Publication Manual, 7th Edition (2019).

## Capabilities

- Generate in-text citations (parenthetical and narrative)
- Create formatted reference list entries for any source type
- Check existing citations for errors and correct them
- Build complete reference lists from research materials
- Handle modern sources: AI tools, social media, streaming content
- Apply edge case rules: missing info, secondary sources, translations

## In-Text Citation Rules

### Author-Date Format

| Authors | Parenthetical | Narrative |
|---------|---------------|-----------|
| 1 | (Smith, 2023) | Smith (2023) |
| 2 | (Smith & Jones, 2023) | Smith and Jones (2023) |
| 3+ | (Smith et al., 2023) | Smith et al. (2023) |
| Group (first) | (American Psychological Association [APA], 2019) | American Psychological Association (APA, 2019) |
| Group (subsequent) | (APA, 2019) | APA (2019) |
| No author | ("Article Title," 2023) | "Article Title" (2023) |

**Key rules:**
- Use `&` in parenthetical, spell out "and" in narrative
- Use `et al.` from FIRST citation for 3+ authors (changed from 6th ed.)
- Period goes AFTER parenthetical citation: `...end of sentence (Smith, 2023).`

### Direct Quotations

Always include locator for direct quotes:
- Page: `(Smith, 2023, p. 45)` or `(Smith, 2023, pp. 45-47)`
- Paragraph: `(Smith, 2023, para. 4)`
- Section: `(Smith, 2023, Methods section)`
- Timestamp: `(Smith, 2023, 2:15)`
- Classical: `(Shakespeare, 1623/2003, 1.5.45-60)`

### Block Quotations (40+ words)

- Indent entire block 0.5 inches
- No quotation marks
- Period BEFORE citation: `...end of quote. (Smith, 2023, p. 45)`

### Multiple Sources

Alphabetize, separate with semicolons:
```
(Adams, 2020; Chen, 2019; Williams, 2021)
```

Same author, multiple years:
```
(Smith, 2019, 2021, 2023)
```

Same author, same year (alphabetize by title in reference list):
```
(Smith, 2023a, 2023b)
```

## Reference List Format

### Core Structure

Every reference has four elements:
1. **Author** - Who created it
2. **Date** - When published (Year) or (Year, Month Day)
3. **Title** - What it's called
4. **Source** - Where to find it (publisher, URL, DOI)

### Formatting Rules

- Heading: **References** (bold, centered)
- Double-spaced throughout
- Hanging indent: 0.5 inches
- Alphabetize by first author's surname
- No period after DOI or URL

### DOI Format

Use hyperlink format: `https://doi.org/10.xxxx/xxxxx`

**NOT:** `doi:10.xxxx` or `DOI: 10.xxxx`

### Common Source Types

#### Journal Article
```
Author, A. A., & Author, B. B. (Year). Title of article in sentence case.
    *Journal Name in Title Case, Volume*(Issue), Page-Page.
    https://doi.org/10.xxxx/xxxxx
```

#### Book
```
Author, A. A. (Year). *Title of book in sentence case*. Publisher.
```

#### Book Chapter
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), *Title of book*
    (pp. xx-xx). Publisher. https://doi.org/10.xxxx/xxxxx
```

#### Website
```
Author, A. A. (Year, Month Day). Title of page. Site Name. https://url
```
Omit site name if same as author.

#### AI Tools (ChatGPT, Claude, etc.)
```
OpenAI. (2024). ChatGPT (Mar 14 version) [Large language model].
    https://chat.openai.com/chat

Anthropic. (2024). Claude (3.5 Sonnet version) [Large language model].
    https://claude.ai
```
Include prompt and response in appendix. Note: AI output not replicable.

#### Social Media

**X/Twitter:**
```
Author, A. A. [@username]. (Year, Month Day). Content up to 20 words
    [Tweet]. X. https://twitter.com/username/status/xxxxx
```

**YouTube:**
```
Uploader Name. (Year, Month Day). *Title of video* [Video]. YouTube.
    https://www.youtube.com/watch?v=xxxxx
```

**Podcast Episode:**
```
Host, A. A. (Host). (Year, Month Day). Episode title (No. xx) [Audio
    podcast episode]. In *Podcast Title*. Producer. https://url
```

For all source type formats, see [references/source-types.md](references/source-types.md).

## Handling Missing Information

| Missing | Solution |
|---------|----------|
| No date | Use `(n.d.)` |
| No author | Move title to author position |
| No title | Use `[Description of work]` in brackets |
| No page numbers | Use para., section, timestamp |
| No DOI, from database | Omit URL entirely |
| No DOI, from web | Include direct URL |

## Edge Cases Quick Reference

**Secondary sources** (citing a source you found in another source):
- In-text: `(Rabbitt, 1982, as cited in Lyon et al., 2014)`
- Reference list: Only include Lyon (the source you read)

**Personal communications** (emails, interviews, conversations):
- In-text only: `(J. Smith, personal communication, January 15, 2023)`
- NOT in reference list (not recoverable)

**Translated works:**
```
Freud, S. (1961). *The ego and the id* (J. Strachey, Trans.). W. W. Norton.
    (Original work published 1923)
```
In-text: `(Freud, 1923/1961)`

**Retracted articles:**
```
Author, A. A. (Year). Title. *Journal, Volume*(Issue), Pages.
    https://doi.org/xxxxx (Retraction published Year, *Journal, Volume*, Page)
```

For comprehensive edge case guidance, see [references/edge-cases.md](references/edge-cases.md).

## Common Errors to Avoid

1. **"&" vs. "and"** - Use & only in parenthetical citations
2. **Period placement** - Period after citation, not before
3. **DOI format** - Must be `https://doi.org/` not `doi:`
4. **Title capitalization** - Sentence case for articles/books, Title Case for journals
5. **et al. usage** - Use from first citation for 3+ authors
6. **Issue number italics** - Only volume is italic: *12*(3)
7. **Missing page numbers** - Required for all direct quotes
8. **Retrieved from** - Omit unless retrieval date included
9. **Publisher location** - Not required in APA 7th
10. **Database URLs** - Omit for common databases (JSTOR, ProQuest)

For complete error checklist, see [references/common-errors.md](references/common-errors.md).

## Workflow: Checking Citations

When asked to check/correct citations:

1. **Identify format issues** - DOI format, capitalization, punctuation
2. **Verify completeness** - All four elements present
3. **Check in-text/reference correspondence** - Every citation has reference entry
4. **Apply source-specific rules** - Correct format for source type
5. **Flag uncertainties** - Note if information appears incomplete

## Workflow: Creating Reference List

When asked to create a reference list from sources:

1. **Identify source type** for each item
2. **Extract four elements** - Author, Date, Title, Source
3. **Apply correct format** per source type
4. **Alphabetize** by first author surname
5. **Format with hanging indent** (note in output)
6. **Generate matching in-text citations** if requested

## Examples

### Example 1: Format a journal article

**Input:** "Cite this: Article by Sarah Chen and Michael Park in Journal of Psychology, volume 45, issue 3, pages 112-128, published 2023, DOI 10.1037/psych.2023.045"

**Output:**
Reference:
```
Chen, S., & Park, M. (2023). [Article title needed]. *Journal of Psychology,
    45*(3), 112-128. https://doi.org/10.1037/psych.2023.045
```
In-text: (Chen & Park, 2023)

Note: Article title needed to complete reference.

### Example 2: Correct a citation

**Input:** "Fix this: (Smith, John, 2020, p.15)"

**Output:**
Corrected: (Smith, 2020, p. 15)

Issues fixed:
- Removed first name (use last name only)
- Added space after "p."

### Example 3: Cite AI-generated content

**Input:** "How do I cite something Claude told me?"

**Output:**
Reference:
```
Anthropic. (2024). Claude (3.5 Sonnet version) [Large language model].
    https://claude.ai
```
In-text: (Anthropic, 2024)

Requirements:
- Include full prompt and response in appendix
- Note in text that AI output cannot be replicated exactly
- Verify any factual claims independently
