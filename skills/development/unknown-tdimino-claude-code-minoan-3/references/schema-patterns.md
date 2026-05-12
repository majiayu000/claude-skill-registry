# Schema JSON-LD Patterns

Structured data patterns for AI search visibility, organized by site type.

---

## Schema Citation Stack (7 Layers)

Per Digital Strategy Force, argbe.tech, and Floyi:

| Layer | Purpose | Schema Types |
|-------|---------|-------------|
| 1. Identity | Who you are | Organization, LocalBusiness, Person |
| 2. Content | What you publish | Article, BlogPosting, HowTo, FAQPage, TechArticle |
| 3. Relationship | What you sell/offer | Product, Service, Offer, Review |
| 4. Provenance | When and by whom | author, datePublished, dateModified, publisher |
| 5. Temporal | Time-bound info | Event, Schedule, validThrough |
| 6. Authority | External validation | sameAs (Wikipedia, Wikidata, social), knowsAbout |
| 7. Linkage | Content relationships | mentions, about, subjectOf, isPartOf |

---

## Critical Research Findings

- **73% of AI-cited pages have schema** vs 30% average (Rankeo, 50K AI responses)
- **FAQPage schema: 2.7x citation lift** (Relixir 2025)
- **Minimal schema (41.6%) WORSE than none (59.8%)** — completeness > presence (Rankeo)
- **JSON-LD + entity pages: +29.6% RAG accuracy** (arXiv, March 2026)

**The completeness rule:** Every primary @type must have 8+ attributes. Fewer than 5 actively hurts citation rates compared to having no schema at all.

---

## Patterns by Site Type

### E-commerce

**Required:** Product, Organization, BreadcrumbList
**Bonus:** AggregateRating, Review, Offer

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "{BASE_URL}/#organization",
      "name": "{ORG_NAME}",
      "url": "{BASE_URL}",
      "logo": "{BASE_URL}/logo.png",
      "description": "{ORG_DESCRIPTION}",
      "sameAs": [
        "https://twitter.com/{HANDLE}",
        "https://www.facebook.com/{PAGE}",
        "https://www.instagram.com/{HANDLE}",
        "https://www.youtube.com/@{CHANNEL}"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "email": "{EMAIL}"
      }
    },
    {
      "@type": "Product",
      "@id": "{BASE_URL}/product/{SLUG}#product",
      "name": "{PRODUCT_NAME}",
      "description": "{PRODUCT_DESCRIPTION}",
      "image": "{PRODUCT_IMAGE_URL}",
      "brand": { "@id": "{BASE_URL}/#organization" },
      "sku": "{SKU}",
      "gtin13": "{GTIN}",
      "offers": {
        "@type": "Offer",
        "price": "{PRICE}",
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock",
        "url": "{BASE_URL}/product/{SLUG}"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "{RATING}",
        "reviewCount": "{REVIEW_COUNT}"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}" },
        { "@type": "ListItem", "position": 2, "name": "{CATEGORY}", "item": "{BASE_URL}/category/{CAT_SLUG}" },
        { "@type": "ListItem", "position": 3, "name": "{PRODUCT_NAME}" }
      ]
    }
  ]
}
```

### SaaS / B2B

**Required:** Organization, SoftwareApplication, FAQPage
**Bonus:** HowTo, Article

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "{BASE_URL}/#organization",
      "name": "{ORG_NAME}",
      "url": "{BASE_URL}",
      "logo": "{BASE_URL}/logo.png",
      "description": "{ORG_DESCRIPTION}",
      "foundingDate": "{FOUNDING_YEAR}",
      "sameAs": [
        "https://twitter.com/{HANDLE}",
        "https://github.com/{ORG}",
        "https://www.linkedin.com/company/{SLUG}",
        "https://www.youtube.com/@{CHANNEL}"
      ]
    },
    {
      "@type": "SoftwareApplication",
      "name": "{APP_NAME}",
      "applicationCategory": "{CATEGORY}",
      "operatingSystem": "Web",
      "description": "{APP_DESCRIPTION}",
      "url": "{BASE_URL}",
      "publisher": { "@id": "{BASE_URL}/#organization" },
      "offers": {
        "@type": "Offer",
        "price": "{PRICE}",
        "priceCurrency": "USD"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "{RATING}",
        "reviewCount": "{REVIEW_COUNT}"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "{QUESTION_1}",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "{ANSWER_1}"
          }
        }
      ]
    }
  ]
}
```

### Content / Media

**Required:** Article, Organization, Person
**Bonus:** NewsArticle, BlogPosting, LiveBlogPosting

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "{BASE_URL}/#organization",
      "name": "{ORG_NAME}",
      "url": "{BASE_URL}",
      "logo": "{BASE_URL}/logo.png",
      "sameAs": [
        "https://twitter.com/{HANDLE}",
        "https://github.com/{ORG}",
        "https://www.youtube.com/@{CHANNEL}"
      ]
    },
    {
      "@type": "Person",
      "@id": "{BASE_URL}/#author",
      "name": "{AUTHOR_NAME}",
      "url": "{AUTHOR_URL}",
      "jobTitle": "{JOB_TITLE}",
      "sameAs": [
        "https://twitter.com/{AUTHOR_HANDLE}",
        "https://www.linkedin.com/in/{AUTHOR_SLUG}"
      ],
      "knowsAbout": ["{TOPIC_1}", "{TOPIC_2}"]
    },
    {
      "@type": "Article",
      "headline": "{HEADLINE}",
      "description": "{DESCRIPTION}",
      "image": "{OG_IMAGE_URL}",
      "datePublished": "{DATE_PUBLISHED}",
      "dateModified": "{DATE_MODIFIED}",
      "author": { "@id": "{BASE_URL}/#author" },
      "publisher": { "@id": "{BASE_URL}/#organization" },
      "mainEntityOfPage": "{ARTICLE_URL}",
      "wordCount": "{WORD_COUNT}",
      "keywords": ["{KW_1}", "{KW_2}"]
    }
  ]
}
```

### Local Business

**Required:** LocalBusiness, Organization
**Bonus:** Review, GeoCoordinates, OpeningHoursSpecification

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "{BASE_URL}/#business",
      "name": "{BUSINESS_NAME}",
      "url": "{BASE_URL}",
      "image": "{IMAGE_URL}",
      "description": "{DESCRIPTION}",
      "telephone": "{PHONE}",
      "email": "{EMAIL}",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "{STREET}",
        "addressLocality": "{CITY}",
        "addressRegion": "{STATE}",
        "postalCode": "{ZIP}",
        "addressCountry": "US"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "{LAT}",
        "longitude": "{LNG}"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "09:00",
          "closes": "17:00"
        }
      ],
      "sameAs": [
        "https://www.google.com/maps/place/{PLACE_ID}",
        "https://www.yelp.com/biz/{YELP_SLUG}",
        "https://www.facebook.com/{PAGE}"
      ],
      "priceRange": "{PRICE_RANGE}"
    }
  ]
}
```

### Documentation

**Required:** TechArticle, Organization
**Bonus:** HowTo, SoftwareSourceCode

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "{BASE_URL}/#organization",
      "name": "{ORG_NAME}",
      "url": "{BASE_URL}",
      "logo": "{BASE_URL}/logo.png",
      "sameAs": [
        "https://github.com/{ORG}",
        "https://twitter.com/{HANDLE}"
      ]
    },
    {
      "@type": "TechArticle",
      "headline": "{TITLE}",
      "description": "{DESCRIPTION}",
      "datePublished": "{DATE_PUBLISHED}",
      "dateModified": "{DATE_MODIFIED}",
      "author": { "@id": "{BASE_URL}/#organization" },
      "publisher": { "@id": "{BASE_URL}/#organization" },
      "mainEntityOfPage": "{DOC_URL}",
      "proficiencyLevel": "{LEVEL}",
      "dependencies": "{FRAMEWORK} {VERSION}",
      "programmingLanguage": "{LANGUAGE}"
    }
  ]
}
```

### Personal / Portfolio

**Required:** Person, Organization (if applicable)
**Bonus:** CreativeWork, Article

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "{BASE_URL}/#person",
      "name": "{FULL_NAME}",
      "url": "{BASE_URL}",
      "image": "{HEADSHOT_URL}",
      "jobTitle": "{JOB_TITLE}",
      "description": "{BIO}",
      "email": "{EMAIL}",
      "sameAs": [
        "https://github.com/{HANDLE}",
        "https://twitter.com/{HANDLE}",
        "https://www.linkedin.com/in/{SLUG}",
        "https://en.wikipedia.org/wiki/{PAGE}"
      ],
      "knowsAbout": ["{SKILL_1}", "{SKILL_2}", "{SKILL_3}"],
      "alumniOf": {
        "@type": "EducationalOrganization",
        "name": "{UNIVERSITY}"
      },
      "worksFor": {
        "@type": "Organization",
        "name": "{EMPLOYER}"
      }
    }
  ]
}
```

---

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|-------------|-------------|-----|
| Duplicate singleton @types on same page | Google silently drops duplicates | One FAQPage per page, one Organization per site |
| Generic Organization (name + url only) | Fewer than 5 attributes: 41.6% citation rate vs 59.8% for no schema | Add logo, description, sameAs, contactPoint, foundingDate |
| Missing dateModified | Perplexity freshness gate treats undated content as stale | Add dateModified to all content types |
| No sameAs links | Missed entity disambiguation — AI can't verify who you are | Link to Wikipedia, Wikidata, social profiles |
| Microdata/RDFa instead of JSON-LD | Harder for AI crawlers to parse; JSON-LD is the standard | Convert to JSON-LD |
| Schema on every page with same data | Bloats pages without adding signal | Use @id references; define entities once |
| FAQ bloat (50+ questions) | Damages traditional SEO (Lily Ray) which undermines GEO | 5–10 genuinely useful questions per page |

---

## Validation Checklist

1. **Google Rich Results Test** — validate syntax and eligible rich results
2. **Schema.org validator** — check type and property validity
3. **Attribute count** — verify 8+ attributes on each primary @type
4. **sameAs audit** — all links resolve, no dead profiles
5. **Duplicate check** — no singleton @types repeated on same page
6. **dateModified** — present on all content types, matches actual update date
7. **@id consistency** — same entity uses same @id across pages
