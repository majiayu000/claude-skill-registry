---
name: seo-lookup
description: Looks up SEO best practices for meta tags, Open Graph, Twitter Cards, and structured data (JSON-LD), returning Google/official documentation URLs with concise summaries. Use when user asks about SEO requirements (e.g., "title tag length", "og:image size"), meta tags (e.g., "canonical", "robots"), social media tags (e.g., "Open Graph", "Twitter Card"), or structured data schemas (e.g., "Article schema", "Product JSON-LD", "FAQ markup").
---

# SEO Lookup

Quick lookup for SEO meta tags, Open Graph, Twitter Cards, and structured data with official documentation references.

## Lookup Workflow

1. **Identify the query type**:
   - Meta tag (e.g., "title", "description", "canonical", "robots")
   - Open Graph tag (e.g., "og:image", "og:title")
   - Twitter Card (e.g., "twitter:card", "twitter:image")
   - Structured data schema (e.g., "Article", "Product", "FAQPage")

2. **Search the appropriate index**:
   - For meta/OG/Twitter: Read [seo-index.json](seo-index.json)
   - For structured data: Read [structured-data-index.json](structured-data-index.json)

3. **Return results**:
   - Summary (1-2 sentences)
   - Key requirements or best practices
   - Official documentation URL

4. **For detailed implementation**:
   - Suggest fetching the official URL
   - Or reference Google Search Central documentation

## Response Format

When returning lookup results, use this format:

```
### [Tag/Schema Name]

**Summary**: [1-2 sentence explanation]

**Requirements**:
- [Requirement 1]
- [Requirement 2]

**Validation**: [Length limits, format requirements if applicable]

**Official Reference**: [URL]
```

## Quick Reference

### Meta Tags - Critical

| Tag | Recommended Length | Key Point |
|-----|-------------------|-----------|
| `<title>` | 50-60 characters | Unique, descriptive, keywords first |
| `<meta name="description">` | 150-160 characters | Compelling, includes call-to-action |
| `<link rel="canonical">` | Full URL | Prevents duplicate content issues |
| `<meta name="robots">` | Directives | Controls indexing behavior |

### Open Graph - Essential Tags

| Tag | Purpose | Best Practice |
|-----|---------|---------------|
| `og:title` | Social share title | Same or similar to page title |
| `og:description` | Social share description | 2-4 sentences |
| `og:image` | Social share image | 1200x630px, under 8MB |
| `og:url` | Canonical URL | Full absolute URL |
| `og:type` | Content type | `website`, `article`, `product` |

### Twitter Cards - Types

| Type | Use Case | Required Tags |
|------|----------|---------------|
| `summary` | Default card | title, description |
| `summary_large_image` | Large image card | title, description, image |
| `player` | Video/audio | All above + player URL |

### Structured Data - Priority Schemas

| Schema | Use Case | Rich Result |
|--------|----------|-------------|
| Article | Blog/news content | Enhanced listing |
| Product | E-commerce | Price, availability |
| FAQPage | FAQ sections | Expandable Q&A |
| BreadcrumbList | Site navigation | Breadcrumb path |
| LocalBusiness | Physical locations | Knowledge panel |

## Common Patterns

### Complete Head Template

```html
<head>
  <!-- Essential Meta -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Brand Name</title>
  <meta name="description" content="Page description here.">
  <link rel="canonical" href="https://example.com/page">

  <!-- Open Graph -->
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Page description here.">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Page Title">
  <meta name="twitter:description" content="Page description here.">
  <meta name="twitter:image" content="https://example.com/image.jpg">
</head>
```

### JSON-LD Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-01T00:00:00Z",
  "image": "https://example.com/image.jpg"
}
</script>
```

## External Resources

- [Google Search Central](https://developers.google.com/search)
- [Open Graph Protocol](https://ogp.me/)
- [Twitter Card Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [Schema.org](https://schema.org/)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
