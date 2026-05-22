---
name: aio-geo-optimizer
description: |
  Optimize blog articles for AI Overview (AIO) and Generative Engine Optimization (GEO).
  MANDATORY TRIGGERS: AIO, GEO, AI Overview, generative engine, AI search optimization, LLM citation, AI-ready content, snippet optimization
  Use when preparing content for AI-powered search engines and LLM citation, restructuring articles for AI extraction, adding schema markup recommendations, or improving E-E-A-T signals.
---

# AIO/GEO Blog Article Optimizer

Transform blog articles into AI-ready content optimized for AI Overviews and generative engine citations.

## Workflow

1. **Analyze** the source article
2. **Restructure** content for AI extraction
3. **Add** schema markup recommendations
4. **Enhance** E-E-A-T signals
5. **Generate** optimized output with implementation notes

## Step 1: Analyze Source Article

Evaluate the input article for:

- Current heading structure (H1-H3 hierarchy)
- Question-answer patterns (explicit or implicit)
- Authority signals (author info, citations, credentials)
- Content length and paragraph structure
- Existing schema markup (if HTML provided)

## Step 2: Restructure for AI Extraction

Apply these transformations:

### Heading Hierarchy
- One clear H1 (article title, include primary keyword)
- Logical H2 sections for major topics
- H3 subsections for specific details
- Keep headings descriptive and question-oriented where natural

### Paragraph Structure
- Max 2-3 sentences per paragraph
- Lead with the key point (inverted pyramid)
- One idea per paragraph

### Q&A Blocks
Insert explicit Q&A sections for common questions:

```markdown
## Frequently Asked Questions

### [Question matching user intent]
[Direct answer in 1-2 sentences. Expand with supporting detail if needed.]
```

### Snippet-Friendly Answers
For key facts, create concise answers (<300 characters) that can be extracted standalone:

```markdown
**What is [topic]?** [Topic] is [concise definition that works as a standalone snippet].
```

## Step 3: Schema Markup Recommendations

Generate JSON-LD schema recommendations based on content type:

### Article Schema (Always Include)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Article Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "[Author Profile URL]",
    "jobTitle": "[Credentials/Title]"
  },
  "datePublished": "[ISO Date]",
  "dateModified": "[ISO Date]",
  "publisher": {
    "@type": "Organization",
    "name": "[Company Name]",
    "logo": { "@type": "ImageObject", "url": "[Logo URL]" }
  }
}
```

### FAQ Schema (When Q&A Present)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text]"
      }
    }
  ]
}
```

### HowTo Schema (For Instructional Content)
Include when article contains step-by-step instructions.

### Product Schema (For Product Content)
Include when discussing specific products with features/pricing.

## Step 4: Enhance E-E-A-T Signals

Add or strengthen these elements:

### Experience
- First-person insights where appropriate
- Specific examples from real usage
- Original data or observations

### Expertise
- Author bio with relevant credentials
- Technical depth appropriate to topic
- Accurate, current information

### Authority
- Citations to authoritative sources (link format: `[Source Name](URL)`)
- References to recognized experts
- Mention of relevant affiliations

### Trust
- Clear "Last Updated" date
- Transparent methodology
- Balanced presentation of information

## Step 5: Output Format

Deliver two outputs:

### 1. Optimized Article (Markdown)
The restructured article with all transformations applied.

### 2. Implementation Checklist
```markdown
## AIO/GEO Implementation Checklist

### Content Structure
- [ ] Single H1 with primary keyword
- [ ] Logical H2/H3 hierarchy
- [ ] Short paragraphs (2-3 sentences)
- [ ] FAQ section added
- [ ] Snippet-friendly definitions included

### Schema Markup
- [ ] Article schema (required)
- [ ] FAQ schema (if applicable)
- [ ] HowTo schema (if applicable)
- [ ] Author/Organization schema

### E-E-A-T Signals
- [ ] Author bio with credentials
- [ ] Last updated date visible
- [ ] Citations to authoritative sources
- [ ] Original insights/data included

### Technical (For Dev Team)
- [ ] Implement JSON-LD in page head
- [ ] Verify schema with Google Rich Results Test
- [ ] Ensure AI crawler access (check robots.txt)
- [ ] Consider llms.txt file for AI bot guidance
- [ ] Page load time < 3 seconds
```

## Quick Reference: AIO vs GEO Focus

| Element | AIO Priority | GEO Priority |
|---------|-------------|--------------|
| Heading hierarchy | High | Medium |
| Q&A blocks | High | High |
| Schema markup | High | High |
| Snippet answers | Medium | High (<300 char) |
| Author authority | High | Medium |
| External citations | Medium | High |
| Brand signals | Medium | High |
| Update frequency | Quarterly | Quarterly |

## Notes

- Preserve the article's voice and style while restructuring
- Don't over-optimize—content should read naturally
- Schema recommendations are suggestions; actual implementation depends on CMS/tech stack
- For monitoring AI citations, suggest tools like Profound, Otterly, or manual tracking
