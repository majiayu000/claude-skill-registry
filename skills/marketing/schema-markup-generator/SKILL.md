---
name: schema-markup-generator
description: Generates structured data markup (Schema.org JSON-LD) to enable rich results in search engines including FAQ snippets, How-To cards, Product listings, Reviews, and more.
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

## Instructions

When a user requests schema markup:

1. **Identify Content Type and Rich Result Opportunity**

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
       // Article properties...
     },
     {
       "@context": "https://schema.org",
       "@type": "FAQPage",
       // FAQ properties...
     },
     {
       "@context": "https://schema.org",
       "@type": "BreadcrumbList",
       // Breadcrumb properties...
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
    
    1. **Google Rich Results Test**
       - URL: https://search.google.com/test/rich-results
       - Test your live URL or paste code
       - Check for errors and warnings
    
    2. **Schema.org Validator**
       - URL: https://validator.schema.org/
       - Validates against Schema.org spec
    
    3. **Google Search Console**
       - Monitor rich results in Search Console
       - Check Enhancements reports for issues
    
    ### Validation Checklist
    
    - [ ] JSON syntax is valid (no trailing commas)
    - [ ] All required properties present
    - [ ] URLs are absolute, not relative
    - [ ] Dates are in ISO 8601 format
    - [ ] Content matches visible page content
    - [ ] No Google policy violations
    ```

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

Test at: https://search.google.com/test/rich-results

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

## Related Skills

- [seo-content-writer](../seo-content-writer/) - Create content worth marking up
- [geo-content-optimizer](../geo-content-optimizer/) - Optimize FAQ content
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) - Audit existing schema
- [technical-seo-checker](../../optimize/technical-seo-checker/) - Technical validation

