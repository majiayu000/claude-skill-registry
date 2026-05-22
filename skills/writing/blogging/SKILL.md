---
name: blogging
description: Technical blogging strategies, SEO, and content creation for developer audiences
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 03-content-creator
bond_type: PRIMARY_BOND
---

# Technical Blogging

Create **compelling technical blog content** that educates and engages developers.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - topic: string
    - target_audience: enum[beginner, intermediate, advanced]
  optional:
    - word_count: integer
    - seo_keywords: array[string]
    - include_code: boolean
```

### Output
```yaml
output:
  blog_post:
    title: string
    body: markdown
    meta_description: string
    estimated_reading_time: duration
```

## Content Strategy

### Topic Sources
```
1. Questions from community
2. Problems you solved
3. New feature announcements
4. Industry trends
5. Tutorial requests
6. Comparison guides
7. Best practices
```

### Content Calendar
| Week | Type | Example |
|------|------|---------|
| 1 | Tutorial | "Getting Started with..." |
| 2 | Deep dive | "Understanding X internals" |
| 3 | Comparison | "X vs Y: Which to choose" |
| 4 | Case study | "How Company X achieved..." |

## Blog Post Structure

```markdown
# Compelling Title (SEO keyword + benefit)

**TL;DR**: One paragraph summary for skimmers

## Introduction (Hook + Promise)
Why should they care? What will they learn?

## Prerequisites
What they need to know/have before starting.

## Main Content
### Section 1: The What
### Section 2: The Why
### Section 3: The How (with code)

## Summary
- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

## Next Steps / Resources
- Link to docs
- Related posts
- Call to action
```

## SEO Basics

| Element | Best Practice |
|---------|---------------|
| Title | Keyword + benefit, <60 chars |
| URL | Short, keyword-rich slug |
| Meta | 150-160 chars description |
| H1 | One per page, matches title |
| Images | Alt text, compressed |

## Writing Tips

1. **Start with outline** - Structure before prose
2. **Write for skimmers** - Headers, bullets, bold
3. **Show, don't tell** - Code over explanation
4. **Be concise** - Cut ruthlessly
5. **End with action** - What should reader do next

## Retry Logic

```yaml
retry_patterns:
  low_engagement:
    strategy: "Rewrite hook, add visuals"

  seo_not_ranking:
    strategy: "Audit keywords, update title"

  code_errors_reported:
    strategy: "Test in fresh environment, fix"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Code doesn't work | Reader feedback | Hotfix immediately |
| Low engagement | <2 min avg time | Rewrite hook |
| Not ranking | Not in top 20 | SEO audit |

## Debug Checklist

```
□ Code examples tested?
□ Links verified?
□ Images optimized?
□ Spell/grammar checked?
□ Mobile preview OK?
□ Meta description set?
□ Keywords in title?
```

## Test Template

```yaml
test_blogging:
  unit_tests:
    - test_code_works:
        assert: "All code samples run"
    - test_seo_elements:
        assert: "Title, meta, keywords present"

  integration_tests:
    - test_reader_journey:
        assert: "Can follow to completion"
```

## Observability

```yaml
metrics:
  - word_count: integer
  - reading_time: duration
  - code_blocks: integer
  - publish_date: date
```

See `assets/` for blog templates.
