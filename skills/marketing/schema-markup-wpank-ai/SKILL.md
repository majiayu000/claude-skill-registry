---
name: schema-markup
model: fast
version: 1.0.0
description: >
  Add, fix, or optimize schema markup and structured data. Use when the user mentions
  schema markup, structured data, JSON-LD, rich snippets, schema.org, FAQ schema,
  product schema, review schema, or breadcrumb schema.
tags: [seo, schema, structured-data, json-ld, rich-snippets, search]
---

# Schema Markup

Implement schema.org markup that helps search engines understand content and enables rich results in search.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install schema-markup
```


## When to Use

- Adding structured data to new or existing pages
- Fixing schema validation errors
- Optimizing for specific rich results (FAQ, product, article)
- Implementing JSON-LD in React/Next.js applications
- Auditing existing schema markup

## Initial Assessment

Before implementing schema, understand:

1. **Page Type** — What kind of page? What's the primary content? What rich results are possible?
2. **Current State** — Any existing schema? Errors? Which rich results already appearing?
3. **Goals** — Which rich results are you targeting? What's the business value?

## Core Principles

### 1. Accuracy First
- Schema must accurately represent page content
- Don't markup content that doesn't exist on the page
- Keep updated when content changes

### 2. Use JSON-LD
- Google recommends JSON-LD format
- Easier to implement and maintain than microdata or RDFa
- Place in `<head>` or before `</body>`

### 3. Follow Google's Guidelines
- Only use markup Google supports for rich results
- Avoid spam tactics
- Review eligibility requirements for each type

### 4. Validate Everything
- Test before deploying
- Monitor Search Console enhancement reports
- Fix errors promptly

## Common Schema Types

| Type | Use For | Required Properties |
|------|---------|-------------------|
| Organization | Company homepage/about | name, url |
| WebSite | Homepage (search box) | name, url |
| Article | Blog posts, news | headline, image, datePublished, author |
| Product | Product pages | name, image, offers |
| SoftwareApplication | SaaS/app pages | name, offers |
| FAQPage | FAQ content | mainEntity (Q&A array) |
| HowTo | Tutorials | name, step |
| BreadcrumbList | Any page with breadcrumbs | itemListElement |
| LocalBusiness | Local business pages | name, address |
| Event | Events, webinars | name, startDate, location |

**For complete JSON-LD examples with required/recommended field annotations**: See `references/schema-examples.md`

## Quick Reference

### Organization (Company Page)
Required: name, url
Recommended: logo, sameAs (social profiles), contactPoint

### Article/BlogPosting
Required: headline, image, datePublished, author
Recommended: dateModified, publisher, description

### Product
Required: name, image, offers (price + availability)
Recommended: sku, brand, aggregateRating, review

### FAQPage
Required: mainEntity (array of Question/Answer pairs)

### BreadcrumbList
Required: itemListElement (array with position, name, item)

## Multiple Schema Types

Combine multiple schema types on one page using `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "..." : "..." },
    { "@type": "WebSite", "..." : "..." },
    { "@type": "BreadcrumbList", "..." : "..." }
  ]
}
```

Use `@id` to create referenceable entities — define once, reference elsewhere with `{ "@id": "..." }`.

## Validation and Testing

### Tools
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: Enhancements reports

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing required field | Required property not included | Add the missing property |
| Invalid URL | Relative URL or malformed | Use fully qualified URLs (`https://...`) |
| Invalid date format | Not ISO 8601 | Use `YYYY-MM-DDTHH:MM:SS+00:00` |
| Invalid enum value | Wrong enumeration value | Use exact schema.org URLs (e.g., `https://schema.org/InStock`) |
| Content mismatch | Schema doesn't match visible content | Ensure schema reflects actual page content |
| Invalid price | Currency symbol or commas included | Use numeric value only (`"149.99"`) |

## Implementation

### Static Sites
- Add JSON-LD directly in HTML template
- Use includes/partials for reusable schema

### Dynamic Sites (React, Next.js)

```tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
```

### CMS / WordPress
- Plugins: Yoast, Rank Math, Schema Pro
- Theme modifications for custom types
- Custom fields mapped to structured data

## Testing Checklist

- [ ] Validates in Rich Results Test with no errors
- [ ] No warnings for recommended properties
- [ ] Schema content matches visible page content
- [ ] All required properties included for each type
- [ ] URLs are fully qualified
- [ ] Dates are ISO 8601 format
- [ ] Prices are numeric without currency symbols

## Task-Specific Questions

Before implementing, gather answers to:

1. What type of page is this? (product, article, FAQ, local business)
2. What rich results are you targeting? (FAQ dropdown, product stars, breadcrumbs)
3. What data is available to populate the schema? (prices, ratings, dates)
4. Is there existing schema on the page? (check with Rich Results Test first)
5. What's your tech stack? (static HTML, React/Next.js, CMS/WordPress)

## Implementation Workflow

1. **Identify page types** — map your site's pages to schema types
2. **Start with homepage** — Organization + WebSite schema
3. **Add per-page schema** — Article for blog, Product for shop, etc.
4. **Add BreadcrumbList** — every page with navigation breadcrumbs
5. **Validate each page** — Rich Results Test before and after
6. **Monitor Search Console** — check enhancement reports weekly after launch

## NEVER Do

1. **NEVER add schema for content that doesn't exist on the page** — this violates Google's guidelines and risks penalties
2. **NEVER use microdata or RDFa when JSON-LD is an option** — JSON-LD is easier to maintain and Google's recommended format
3. **NEVER hardcode schema that should be dynamic** — product prices, availability, and ratings must reflect current data
4. **NEVER skip validation before deploying** — invalid schema is worse than no schema; it wastes crawl budget
5. **NEVER mark up every page identically** — each page type needs its own appropriate schema types
6. **NEVER ignore Search Console errors** — schema errors can cause rich results to disappear entirely
