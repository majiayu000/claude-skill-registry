---
name: schema-markup-generator
description: Generates structured data markup (Schema.org JSON-LD) to enable rich results in search engines including FAQ snippets, How-To cards, Product listings, Reviews, and more.
geo-relevance: "medium"
---

# Schema Markup Generator

This skill creates Schema.org structured data markup in JSON-LD format to help search engines understand your content and enable rich results in SERPs.

## When to Use This Skill

- Adding FAQ schema for expanded SERP presence
- Creating How-To schema for step-by-step content
- Adding Product schema for e-commerce pages
- Implementing Article schema for blog posts
- Adding Local Business schema for location pages
- Creating Review/Rating schema
- Implementing Organization schema for brand presence
- Any page where rich results would improve visibility

## What This Skill Does

1. **Schema Type Selection**: Recommends appropriate schema types
2. **JSON-LD Generation**: Creates valid structured data markup
3. **Property Mapping**: Maps your content to schema properties
4. **Validation Guidance**: Ensures schema meets requirements
5. **Nested Schema**: Handles complex, multi-type schemas
6. **Rich Result Eligibility**: Identifies which rich results you can target

## How to Use

### Generate Schema for Content

```
Generate schema markup for this [content type]: [content/URL]
```

```
Create FAQ schema for these questions and answers: [Q&A list]
```

### Specific Schema Types

```
Create Product schema for [product name] with [details]
```

```
Generate LocalBusiness schema for [business name and details]
```

### Audit Existing Schema

```
Review and improve this schema markup: [existing schema]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~web crawler connected:**
Automatically crawl and extract page content (visible text, headings, lists, tables), existing schema markup, page metadata, and structured content elements that map to schema properties.

**With manual data only:**
Ask the user to provide:
1. Page URL or full HTML content
2. Page type (article, product, FAQ, how-to, local business, etc.)
3. Specific data needed for schema (prices, dates, author info, Q&A pairs, etc.)
4. Current schema markup (if optimizing existing)

Proceed with the full workflow using provided data. Note in the output which data is from automated extraction vs. user-provided data.

## Instructions

When a user requests schema markup:

1. **Identify Content Type and Rich Result Opportunity**

   Reference the [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md) item **O05 (Schema Markup)** for content-type to schema mapping:

   ```markdown
   ### CORE-EEAT Schema Mapping (O05)

   | Content Type | Required Schema | Conditional Schema |
   |-------------|----------------|--------------------|
   | Blog (guides) | Article, Breadcrumb | FAQ, HowTo |
   | Blog (tools) | Article, Breadcrumb | FAQ, Review |
   | Blog (insights) | Article, Breadcrumb | FAQ |
   | Alternative | Comparison*, Breadcrumb, FAQ | AggregateRating |
   | Best-of | ItemList, Breadcrumb, FAQ | AggregateRating per tool |
   | Use-case | WebPage, Breadcrumb, FAQ | — |
   | FAQ | FAQPage, Breadcrumb | — |
   | Landing | SoftwareApplication, Breadcrumb, FAQ | WebPage |
   | Testimonial | Review, Breadcrumb | FAQ, Person |

   *Use the mapping above to ensure schema type matches content type (CORE-EEAT O05: Pass criteria).*
   ```

   ```markdown
   ### Schema Analysis

   **Content Type**: [blog/product/FAQ/how-to/local business/etc.]
   **Page URL**: [URL]

   **Eligible Rich Results**:
   
   | Rich Result Type | Eligibility | Impact |
   |------------------|-------------|--------|
   | FAQ | ✅/❌ | High - Expands SERP presence |
   | How-To | ✅/❌ | Medium - Shows steps in SERP |
   | Product | ✅/❌ | High - Shows price, availability |
   | Review | ✅/❌ | High - Shows star ratings |
   | Article | ✅/❌ | Medium - Shows publish date, author |
   | Breadcrumb | ✅/❌ | Medium - Shows navigation path |
   | Video | ✅/❌ | High - Shows video thumbnail |
   
   **Recommended Schema Types**:
   1. [Primary schema type] - [reason]
   2. [Secondary schema type] - [reason]
   ```

2. **Generate FAQ Schema**

   ```markdown
   ### FAQ Schema (FAQPage)
   
   **Requirements**:
   - Minimum 2 Q&A pairs
   - Questions must be complete questions
   - Answers should be comprehensive
   - Must match visible page content
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "[Question 1 - exactly as shown on page]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[Complete answer text]"
         }
       },
       {
         "@type": "Question",
         "name": "[Question 2]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[Complete answer text]"
         }
       }
     ]
   }
   ```
   
   **Rich Result Preview**:
   ```
   [Page Title]
   [URL]
   [Meta Description]
   
   ▼ Question 1?
     [Answer preview...]
   ▼ Question 2?
     [Answer preview...]
   ```
   ```

3. **Generate How-To Schema**

   ```markdown
   ### How-To Schema (HowTo)
   
   **Requirements**:
   - Clear step-by-step instructions
   - Each step must have text
   - Optional: images, videos, time, supplies
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "HowTo",
     "name": "[How-to title]",
     "description": "[Brief description of what this teaches]",
     "totalTime": "PT[X]M",
     "estimatedCost": {
       "@type": "MonetaryAmount",
       "currency": "USD",
       "value": "[cost]"
     },
     "supply": [
       {
         "@type": "HowToSupply",
         "name": "[Supply item 1]"
       }
     ],
     "tool": [
       {
         "@type": "HowToTool",
         "name": "[Tool 1]"
       }
     ],
     "step": [
       {
         "@type": "HowToStep",
         "name": "[Step 1 title]",
         "text": "[Step 1 detailed instructions]",
         "url": "[URL]#step1",
         "image": "[Step 1 image URL]"
       },
       {
         "@type": "HowToStep",
         "name": "[Step 2 title]",
         "text": "[Step 2 detailed instructions]",
         "url": "[URL]#step2",
         "image": "[Step 2 image URL]"
       }
     ]
   }
   ```
   ```

4. **Generate Article Schema**

   ```markdown
   ### Article Schema
   
   **Schema Type Options**:
   - `Article` - General articles
   - `BlogPosting` - Blog posts
   - `NewsArticle` - News content
   - `TechArticle` - Technical documentation
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Article",
     "headline": "[Article title - max 110 chars]",
     "description": "[Article summary]",
     "image": [
       "[Image URL 1 - 1200px wide]",
       "[Image URL 2 - 4:3 ratio]",
       "[Image URL 3 - 16:9 ratio]"
     ],
     "datePublished": "[ISO 8601 date: 2024-01-15T08:00:00+00:00]",
     "dateModified": "[ISO 8601 date]",
     "author": {
       "@type": "Person",
       "name": "[Author Name]",
       "url": "[Author profile URL]"
     },
     "publisher": {
       "@type": "Organization",
       "name": "[Publisher Name]",
       "logo": {
         "@type": "ImageObject",
         "url": "[Logo URL - 60px high max]"
       }
     },
     "mainEntityOfPage": {
       "@type": "WebPage",
       "@id": "[Canonical URL]"
     }
   }
   ```
   ```

5. **Generate Product Schema**

   ```markdown
   ### Product Schema
   
   **Requirements for Rich Results**:
   - Name (required)
   - Image (required)
   - Offers with price (for price rich results)
   - AggregateRating (for star ratings)
   - Review (for review snippets)
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Product",
     "name": "[Product Name]",
     "image": [
       "[Product image URL 1]",
       "[Product image URL 2]"
     ],
     "description": "[Product description]",
     "sku": "[SKU]",
     "mpn": "[Manufacturer Part Number]",
     "brand": {
       "@type": "Brand",
       "name": "[Brand Name]"
     },
     "offers": {
       "@type": "Offer",
       "url": "[Product URL]",
       "priceCurrency": "USD",
       "price": "[Price]",
       "priceValidUntil": "[Date]",
       "availability": "https://schema.org/InStock",
       "seller": {
         "@type": "Organization",
         "name": "[Seller Name]"
       }
     },
     "aggregateRating": {
       "@type": "AggregateRating",
       "ratingValue": "[4.5]",
       "reviewCount": "[89]"
     },
     "review": {
       "@type": "Review",
       "reviewRating": {
         "@type": "Rating",
         "ratingValue": "[5]"
       },
       "author": {
         "@type": "Person",
         "name": "[Reviewer Name]"
       },
       "reviewBody": "[Review text]"
     }
   }
   ```
   ```

6. **Generate Local Business Schema**

   ```markdown
   ### LocalBusiness Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "[LocalBusiness/Restaurant/Store/etc.]",
     "name": "[Business Name]",
     "image": "[Business image URL]",
     "@id": "[Business URL]",
     "url": "[Website URL]",
     "telephone": "[Phone number]",
     "priceRange": "[$$]",
     "address": {
       "@type": "PostalAddress",
       "streetAddress": "[Street Address]",
       "addressLocality": "[City]",
       "addressRegion": "[State]",
       "postalCode": "[ZIP]",
       "addressCountry": "US"
     },
     "geo": {
       "@type": "GeoCoordinates",
       "latitude": [latitude],
       "longitude": [longitude]
     },
     "openingHoursSpecification": [
       {
         "@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "09:00",
         "closes": "17:00"
       }
     ],
     "aggregateRating": {
       "@type": "AggregateRating",
       "ratingValue": "[4.5]",
       "reviewCount": "[123]"
     }
   }
   ```
   ```

7. **Generate Organization Schema**

   ```markdown
   ### Organization Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "name": "[Organization Name]",
     "url": "[Website URL]",
     "logo": "[Logo URL]",
     "sameAs": [
       "[Facebook URL]",
       "[Twitter URL]",
       "[LinkedIn URL]",
       "[Instagram URL]"
     ],
     "contactPoint": {
       "@type": "ContactPoint",
       "telephone": "[Phone]",
       "contactType": "customer service",
       "availableLanguage": ["English"]
     }
   }
   ```
   ```

8. **Generate Breadcrumb Schema**

   ```markdown
   ### BreadcrumbList Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "BreadcrumbList",
     "itemListElement": [
       {
         "@type": "ListItem",
         "position": 1,
         "name": "Home",
         "item": "[Homepage URL]"
       },
       {
         "@type": "ListItem",
         "position": 2,
         "name": "[Category Name]",
         "item": "[Category URL]"
       },
       {
         "@type": "ListItem",
         "position": 3,
         "name": "[Page Name]",
         "item": "[Page URL]"
       }
     ]
   }
   ```
   ```

9. **Combine Multiple Schema Types**

   ```markdown
   ### Combined Schema Implementation
   
   For pages needing multiple schema types:
   
   ```json
   <script type="application/ld+json">
   [
     {
       "@context": "https://schema.org",
       "@type": "Article",
       "headline": "[Article title]",
       "author": { "@type": "Person", "name": "[Author name]" }
     },
     {
       "@context": "https://schema.org",
       "@type": "FAQPage",
       "mainEntity": [{ "@type": "Question", "name": "[Question]", "acceptedAnswer": { "@type": "Answer", "text": "[Answer]" } }]
     },
     {
       "@context": "https://schema.org",
       "@type": "BreadcrumbList",
       "itemListElement": [{ "@type": "ListItem", "position": 1, "name": "Home", "item": "[URL]" }]
     }
   ]
   </script>
   ```
   ```

10. **Provide Implementation and Validation**

    ```markdown
    ## Implementation Guide

    ### Adding Schema to Your Page

    **Option 1: In HTML <head>**
    ```html
    <head>
      <script type="application/ld+json">
        [Your JSON-LD schema here]
      </script>
    </head>
    ```

    **Option 2: Before closing </body>**
    ```html
      <script type="application/ld+json">
        [Your JSON-LD schema here]
      </script>
    </body>
    ```

    ### Validation Steps

    1. **~~schema validator**
       - Test your live URL or paste code
       - Check for errors and warnings

    2. **Schema.org Validator**
       - URL: https://validator.schema.org/
       - Validates against Schema.org spec

    3. **~~search console**
       - Monitor rich results in ~~search console
       - Check Enhancements reports for issues

    ### Validation Checklist

    - [ ] JSON syntax is valid (no trailing commas)
    - [ ] All required properties present
    - [ ] URLs are absolute, not relative
    - [ ] Dates are in ISO 8601 format
    - [ ] Content matches visible page content
    - [ ] No policy violations
    ```

## Validation Checkpoints

### Input Validation
- [ ] Page URL or content provided
- [ ] Schema type appropriate for content (Article for blog, Product for e-commerce, etc.)
- [ ] All required data available (author, dates, prices, etc. depending on schema type)
- [ ] Content eligibility for rich results confirmed

### Output Validation
- [ ] JSON syntax validates (no trailing commas, proper quotes)
- [ ] All required properties present for chosen schema type
- [ ] URLs are absolute, not relative
- [ ] Dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SS+00:00)
- [ ] Schema content matches visible page content exactly
- [ ] Passes ~~schema validator with no errors
- [ ] Source of each data point clearly stated (~~web crawler extraction, user-provided, or manual entry)

## Example

**User**: "Generate FAQ schema for a page about SEO with 3 questions"

**Output**:

```markdown
## FAQ Schema for SEO Page

### Schema Markup

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO (Search Engine Optimization) is the practice of optimizing websites and content to rank higher in search engine results pages (SERPs). It involves technical optimizations, content creation, and link building to increase organic visibility and drive qualified traffic to your website."
      }
    },
    {
      "@type": "Question",
      "name": "How long does SEO take to work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO typically takes 3-6 months to show significant results, though this varies based on competition, domain authority, and effort invested. New websites may take 6-12 months, while established sites with existing authority can see improvements in 1-3 months for less competitive keywords."
      }
    },
    {
      "@type": "Question",
      "name": "Is SEO better than paid advertising?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO and paid advertising serve different purposes. SEO provides sustainable, long-term traffic without per-click costs but takes time to build. Paid advertising delivers immediate results but stops when you stop paying. Most successful businesses use both: paid ads for immediate leads and SEO for long-term growth."
      }
    }
  ]
}
```

### Implementation

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO (Search Engine Optimization) is the practice of optimizing websites and content to rank higher in search engine results pages (SERPs). It involves technical optimizations, content creation, and link building to increase organic visibility and drive qualified traffic to your website."
      }
    },
    {
      "@type": "Question",
      "name": "How long does SEO take to work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO typically takes 3-6 months to show significant results, though this varies based on competition, domain authority, and effort invested. New websites may take 6-12 months, while established sites with existing authority can see improvements in 1-3 months for less competitive keywords."
      }
    },
    {
      "@type": "Question",
      "name": "Is SEO better than paid advertising?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO and paid advertising serve different purposes. SEO provides sustainable, long-term traffic without per-click costs but takes time to build. Paid advertising delivers immediate results but stops when you stop paying. Most successful businesses use both: paid ads for immediate leads and SEO for long-term growth."
      }
    }
  ]
}
</script>
```

### Validation

Test with ~~schema validator

### SERP Preview

```
SEO Guide: Complete Beginner's Tutorial
yoursite.com/seo-guide/
Learn SEO from scratch with our comprehensive guide...

▼ What is SEO?
  SEO (Search Engine Optimization) is the practice of optimizing...
▼ How long does SEO take to work?
  SEO typically takes 3-6 months to show significant results...
▼ Is SEO better than paid advertising?
  SEO and paid advertising serve different purposes...
```
```

## Schema Type Quick Reference

| Content Type | Schema Type | Key Properties |
|--------------|-------------|----------------|
| Blog Post | BlogPosting/Article | headline, datePublished, author |
| Product | Product | name, price, availability |
| FAQ | FAQPage | Question, Answer |
| How-To | HowTo | step, totalTime |
| Local Business | LocalBusiness | address, geo, openingHours |
| Recipe | Recipe | ingredients, cookTime |
| Event | Event | startDate, location |
| Video | VideoObject | uploadDate, duration |
| Course | Course | provider, name |
| Review | Review | itemReviewed, ratingValue |

## Tips for Success

1. **Match visible content** - Schema must reflect what users see
2. **Don't spam** - Only add schema for relevant content
3. **Keep updated** - Update dates and prices when they change
4. **Test thoroughly** - Validate before deploying
5. **Monitor Search Console** - Watch for errors and warnings

## Schema Type Decision Tree

### When to Use Which Schema

| Your Content | Primary Schema | Add If Applicable | Rich Result Eligibility |
|-------------|---------------|-------------------|----------------------|
| Blog post / article | Article | FAQ, HowTo, Speakable | Article carousel, FAQ rich result |
| Product page | Product | Review, Offer, AggregateRating | Product snippet with price/rating |
| Service page | Service | FAQ, LocalBusiness | Service snippet |
| How-to guide | HowTo | Article, FAQ | How-to rich result with steps |
| FAQ page | FAQPage | Article | FAQ accordion in SERP |
| Recipe | Recipe | Video, AggregateRating | Recipe carousel |
| Event | Event | Offer, Organization | Event snippet with date/location |
| Video | VideoObject | Article | Video carousel, key moments |
| Local business | LocalBusiness | Review, OpeningHoursSpecification | Local pack, knowledge panel |
| Person/author | Person | Organization | Knowledge panel |
| Organization | Organization | ContactPoint, Logo | Knowledge panel |
| Course | Course | Organization | Course rich result |
| Job posting | JobPosting | Organization | Google for Jobs listing |
| Breadcrumb | BreadcrumbList | (Always add alongside other schema) | Breadcrumb trail in SERP |
| Software/App | SoftwareApplication | Review, Offer | App snippet |

### Industry-Specific Schema Recommendations

| Industry | Essential Schema | High-Value Additions |
|----------|-----------------|---------------------|
| E-commerce | Product, BreadcrumbList, Organization | AggregateRating, FAQ, Review |
| SaaS | SoftwareApplication, FAQPage, Organization | HowTo, VideoObject, Review |
| Local Services | LocalBusiness, Service | FAQ, Review, Event |
| Publishing/Media | Article, Person, Organization | FAQ, Speakable, VideoObject |
| Education | Course, Organization | FAQ, HowTo, Event |
| Healthcare | MedicalWebPage, Organization | FAQ, Physician, MedicalClinic |
| Real Estate | RealEstateListing, Organization | LocalBusiness, FAQ |
| Restaurants | Restaurant, Menu | Review, Event, FAQ |

### Schema Implementation Priority

| Priority | Schema Types | Why |
|----------|-------------|-----|
| P0 -- Always | Organization, BreadcrumbList, WebSite (SearchAction) | Foundation for all sites |
| P1 -- Content | Article, FAQPage, HowTo | Direct rich result eligibility |
| P2 -- Commercial | Product, Review, AggregateRating, Offer | Revenue-impacting rich results |
| P3 -- Authority | Person, SameAs, Speakable | E-E-A-T signals, AI citation |
| P4 -- Specialized | Industry-specific types | Niche rich results |

### Schema Validation Quick Reference

| Issue | Impact | Fix |
|-------|--------|-----|
| Missing required property | Schema ignored by Google | Add all required fields (check schema.org) |
| Invalid date format | Warning, may lose rich result | Use ISO 8601: "2026-02-11" |
| Incorrect @type | Schema misinterpreted | Match @type exactly to schema.org |
| Self-referencing sameAs | Warning | sameAs should link to EXTERNAL profiles |
| Missing image for Article | Loses article rich result | Add image property with valid URL |
| Review without itemReviewed | Review not connected | Nest review inside Product/Service/etc. |

## Reference Materials

- [Schema Templates](./references/schema-templates.md) - Copy-ready JSON-LD templates for all schema types
- [Validation Guide](./references/validation-guide.md) - Common errors, required properties, testing workflow

## Related Skills

- [seo-content-writer](../seo-content-writer/) — Create content worth marking up
- [geo-content-optimizer](../geo-content-optimizer/) — Optimize FAQ content
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — Audit existing schema
- [technical-seo-checker](../../optimize/technical-seo-checker/) — Technical validation
- [entity-optimizer](../../cross-cutting/entity-optimizer/) — Entity audit informs Organization, Person, Product schema
- [meta-tags-optimizer](../meta-tags-optimizer/) — Optimize meta tags alongside structured data

