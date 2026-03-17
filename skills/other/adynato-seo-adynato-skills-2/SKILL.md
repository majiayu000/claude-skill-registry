---
name: adynato-seo
description: Handles SEO requirements for all web content including blogs, landing pages, and documentation. Covers LD+JSON schema.org structured data, internal backlinks strategy, further reading sections, meta tags, and Open Graph. Use when creating or editing any public-facing web content, blog posts, or pages that need search visibility.
---

# SEO Skill

Use this skill when creating or modifying any public-facing web content for Adynato projects.

## Requirements Checklist

Every public page MUST include:

1. **LD+JSON Structured Data** - schema.org markup in `<script type="application/ld+json">`
2. **Internal Backlinks** - Links to related Adynato projects/pages
3. **Further Reading Section** - At the end of content, link to related resources
4. **Meta Tags** - title, description, keywords
5. **Open Graph Tags** - og:title, og:description, og:image, og:url

## LD+JSON Schema.org

Always include structured data. See [references/SCHEMAS.md](references/SCHEMAS.md) for templates.

### Required Schemas by Content Type

| Content Type | Required Schemas |
|--------------|------------------|
| Blog Post | Article, BreadcrumbList, Organization |
| Landing Page | WebPage, Organization, optional Product/Service |
| Documentation | TechArticle, BreadcrumbList |
| Product Page | Product, BreadcrumbList, Organization |

### Implementation

Place LD+JSON in the `<head>` or before closing `</body>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  ...
}
</script>
```

For multiple schemas, use `@graph`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Article", ... },
    { "@type": "BreadcrumbList", ... },
    { "@type": "Organization", ... }
  ]
}
</script>
```

## Internal Backlinks

Every piece of content must link to related Adynato projects and pages.

### Rules

1. **Minimum 2-3 internal links** per page/post
2. **Link naturally** within content, not just in footer sections
3. **Use descriptive anchor text** - not "click here" or "read more"
4. **Cross-link related projects** - if mentioning image optimization, link to img4web

### Example

```markdown
When optimizing images for your project, use [img4web](https://github.com/adynato/img4web)
to automatically compress and convert assets to modern formats like WebP and AVIF.
```

## Further Reading Section

Every blog post and documentation page must end with a "Further Reading" section.

### Format

```markdown
## Further Reading

- [Related Post Title](/blog/related-post) - Brief description of what reader will learn
- [Another Project](https://github.com/adynato/project) - How it relates to current topic
- [External Resource](https://example.com) - Why this external link is valuable
```

### Rules

1. **Minimum 3 links** in Further Reading
2. **At least 1 internal link** to Adynato content
3. **Include brief descriptions** explaining relevance
4. **Mix of internal and external** resources when appropriate

## Meta Tags

### Required Meta Tags

```html
<meta name="title" content="Page Title - Adynato">
<meta name="description" content="Concise description under 160 characters">
<meta name="keywords" content="relevant, keywords, comma, separated">
<meta name="author" content="Adynato">
```

### Open Graph (Required)

```html
<meta property="og:type" content="article">
<meta property="og:url" content="https://adynato.com/blog/post-slug">
<meta property="og:title" content="Post Title">
<meta property="og:description" content="Description for social sharing">
<meta property="og:image" content="https://adynato.com/images/og/post-slug.png">
<meta property="og:site_name" content="Adynato">
```

### Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Post Title">
<meta name="twitter:description" content="Description for Twitter">
<meta name="twitter:image" content="https://adynato.com/images/og/post-slug.png">
```

## Blog Post Frontmatter

For MDX/Markdown blogs, include this frontmatter:

```yaml
---
title: "Post Title"
description: "Meta description under 160 characters"
date: "2026-01-17"
author: "Author Name"
tags: ["tag1", "tag2"]
image: "/images/blog/post-slug/cover.png"
ogImage: "/images/og/post-slug.png"
schema:
  type: "Article"
  datePublished: "2026-01-17"
  dateModified: "2026-01-17"
---
```

## Validation

Before publishing, verify:

- [ ] LD+JSON validates at https://validator.schema.org/
- [ ] Meta description is under 160 characters
- [ ] OG image exists and is correct dimensions (1200x630)
- [ ] At least 2 internal backlinks present
- [ ] Further Reading section has 3+ links
- [ ] All links are working (no 404s)
