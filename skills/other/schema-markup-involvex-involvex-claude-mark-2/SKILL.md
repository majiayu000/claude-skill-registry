---
name: schema-markup
description: Schema.org markup implementation patterns for rich results. Use when adding structured data to content for enhanced SERP appearances.
---

# Schema Markup

## When to Use

- Adding structured data to content
- Implementing rich results
- Validating existing schema
- Planning schema strategy

## Common Schema Types

### Article/BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title (max 110 chars)",
  "image": ["https://example.com/image.jpg"],
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.jpg"
    }
  },
  "datePublished": "2025-01-01",
  "dateModified": "2025-01-15"
}
```

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text."
      }
    }
  ]
}
```

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to do something",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 title",
      "text": "Step 1 description"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2 title",
      "text": "Step 2 description"
    }
  ]
}
```

## Implementation Checklist

- [ ] Use JSON-LD format (preferred by Google)
- [ ] Place in `<head>` or end of `<body>`
- [ ] Include all required properties
- [ ] Validate with Google Rich Results Test
- [ ] Test with Schema.org validator
- [ ] Check Search Console for errors

## Best Practices

1. **Be specific**: Use most specific type (BlogPosting over Article)
2. **Be accurate**: Only mark up visible content
3. **Be complete**: Include all required properties
4. **Test thoroughly**: Use validation tools
5. **Monitor**: Check Search Console regularly
