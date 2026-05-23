---
name: google-structured-data
description: Google Search structured data implementation - Schema.org markup for rich results, JSON-LD templates, JavaScript generation, and SEO best practices
version: "1.1"
---

# Google Structured Data Skill

Implement Schema.org structured data markup for Google Search rich results. This skill provides JSON-LD templates, required/recommended properties, and best practices for all major structured data types.

## When to Use This Skill

Trigger this skill when:
- Adding structured data to web pages for SEO
- Implementing JSON-LD markup for rich results
- Creating Schema.org markup for articles, products, events, FAQs, recipes, videos, or local businesses
- Generating structured data dynamically with JavaScript or Google Tag Manager
- Debugging structured data issues
- Optimizing search appearance in Google Search, News, or Discover

## Quick Reference

### Supported Formats
- **JSON-LD** (Recommended) - Embedded in `<script type="application/ld+json">`
- **Microdata** - Inline HTML attributes
- **RDFa** - Semantic HTML attributes

### Core Principles
1. **Mark up visible content only** - Don't mark up hidden content
2. **Be accurate** - Markup must represent actual page content
3. **Be specific** - Use the most specific Schema.org type
4. **Include all required properties** - Each type has mandatory fields
5. **Test before deploying** - Use Rich Results Test tool

## Common Structured Data Types

### 1. Article (NewsArticle, BlogPosting)

**Use for:** News articles, blog posts, sports articles

**Required:** None (all recommended)

**Recommended Properties:**
- `headline` - Article title (keep concise)
- `image` - Representative images (16x9, 4x3, 1x1 ratios; min 50K pixels)
- `datePublished` - ISO 8601 with timezone
- `dateModified` - Last modification date
- `author` - Person or Organization with name and URL

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Article Title Here",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2024-01-05T08:00:00+08:00",
  "dateModified": "2024-02-05T09:20:00+08:00",
  "author": [{
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://example.com/profile/janedoe123"
  }]
}
```

---

### 2. Product

**Use for:** E-commerce product pages, product reviews

**Required Properties:**
- `name` - Product name

**Recommended Properties:**
- `image` - Product images
- `description` - Product description
- `brand` - Brand name
- `offers` - Price, availability, currency
- `aggregateRating` - Average rating
- `review` - Individual reviews

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Executive Anvil",
  "image": "https://example.com/anvil.jpg",
  "description": "Sleek and deadly executive anvil.",
  "brand": {
    "@type": "Brand",
    "name": "ACME"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/anvil",
    "priceCurrency": "USD",
    "price": 119.99,
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2025-12-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.4,
    "reviewCount": 89
  }
}
```

---

### 3. LocalBusiness

**Use for:** Physical business locations, restaurants, stores

**Required Properties:**
- `name` - Business name
- `address` - Full postal address

**Recommended Properties:**
- `telephone` - With country code
- `openingHoursSpecification` - Business hours
- `geo` - Latitude/longitude (min 5 decimal places)
- `url` - Location-specific URL
- `priceRange` - "$" to "$$$$" or price range
- `servesCuisine` - For restaurants
- `menu` - Menu URL for food establishments

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Dave's Steak House",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "148 W 51st St",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10019",
    "addressCountry": "US"
  },
  "telephone": "+12122459600",
  "url": "https://www.example.com/restaurant-locations/manhattan",
  "servesCuisine": "American",
  "priceRange": "$$$",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.761293,
    "longitude": -73.982294
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "11:30",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday"],
      "opens": "16:00",
      "closes": "23:00"
    }
  ],
  "menu": "https://www.example.com/menu"
}
```

---

### 4. FAQPage

**Use for:** FAQ pages on authoritative sites (government, health)

**Required Properties:**
- `mainEntity` - Array of Question objects

**Question Required Properties:**
- `name` - Full question text
- `acceptedAnswer` - Answer object with `text` property

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>You can return items within 30 days of purchase.</p>"
      }
    },
    {
      "@type": "Question",
      "name": "How do I track my order?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Use the tracking link in your confirmation email.</p>"
      }
    }
  ]
}
```

**Allowed HTML in answers:** `<h1>-<h6>`, `<br>`, `<ol>`, `<ul>`, `<li>`, `<a>`, `<p>`, `<div>`, `<b>`, `<strong>`, `<i>`, `<em>`

---

### 5. Event

**Use for:** Concerts, conferences, festivals, sports events

**Required Properties:**
- `name` - Event title (no venue names or promotions)
- `startDate` - ISO 8601 with timezone offset
- `location` - Place with name and full address

**Recommended Properties:**
- `description` - Event details
- `endDate` - When event concludes
- `eventStatus` - EventScheduled, EventCancelled, EventPostponed, EventRescheduled
- `image` - High-res images (1920px width, 16x9/4x3/1x1)
- `offers` - Ticket info with price, currency, availability, URL
- `organizer` - Hosting organization
- `performer` - Artists or participants

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "The Adventures of Kira and Morrison",
  "startDate": "2025-07-21T19:00-05:00",
  "endDate": "2025-07-21T23:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "Snickerpark Stadium",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "100 West Snickerpark Dr",
      "addressLocality": "Snickertown",
      "postalCode": "19019",
      "addressRegion": "PA",
      "addressCountry": "US"
    }
  },
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "description": "The Adventures of Kira and Morrison is coming to Snickertown.",
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/event_offer/12345",
    "price": 30,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2024-05-21T12:00"
  },
  "performer": {
    "@type": "PerformingGroup",
    "name": "Kira and Morrison"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Kira and Morrison Music",
    "url": "https://kiraandmorrisonmusic.com"
  }
}
```

---

### 6. BreadcrumbList

**Use for:** Site navigation hierarchy

**Required Properties:**
- `itemListElement` - Array of ListItem objects

**ListItem Required Properties:**
- `position` - Sequential number starting at 1
- `name` - Breadcrumb title
- `item` - URL (optional for final item)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Books",
      "item": "https://example.com/books"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Science Fiction",
      "item": "https://example.com/books/sciencefiction"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Award Winners"
    }
  ]
}
```

---

### 7. VideoObject

**Use for:** Video content, livestreams, tutorials

**Required Properties:**
- `name` - Unique video title
- `thumbnailUrl` - Multiple thumbnail URLs
- `uploadDate` - ISO 8601 with timezone

**Recommended Properties:**
- `contentUrl` - Direct video file URL
- `description` - Unique description
- `duration` - ISO 8601 (e.g., PT1M54S)
- `embedUrl` - Video player URL
- `hasPart` - Clip objects for key moments
- `publication` - BroadcastEvent for LIVE badge

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to Make Banana Bread",
  "description": "Learn to bake delicious banana bread in 30 minutes.",
  "thumbnailUrl": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg"
  ],
  "uploadDate": "2024-03-31T08:00:00+08:00",
  "duration": "PT15M30S",
  "contentUrl": "https://example.com/video/banana-bread.mp4",
  "embedUrl": "https://example.com/embed/banana-bread",
  "hasPart": [
    {
      "@type": "Clip",
      "name": "Mixing Ingredients",
      "startOffset": 30,
      "endOffset": 120,
      "url": "https://example.com/video?t=30"
    },
    {
      "@type": "Clip",
      "name": "Baking Process",
      "startOffset": 120,
      "endOffset": 600,
      "url": "https://example.com/video?t=120"
    }
  ]
}
```

---

### 8. Recipe

**Use for:** Cooking recipes, food preparation guides

**Required Properties:**
- `name` - Dish name
- `image` - Multiple images (16x9, 4x3, 1x1; min 50K pixels)

**Recommended Properties:**
- `author` - Recipe creator
- `aggregateRating` - Average rating
- `prepTime`, `cookTime`, `totalTime` - ISO 8601 durations
- `recipeYield` - Servings (required if nutrition specified)
- `recipeCategory` - Meal type (dinner, dessert)
- `recipeCuisine` - Regional origin
- `recipeIngredient` - Array of ingredients
- `recipeInstructions` - HowToStep array
- `nutrition.calories` - Calorie count

```json
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Non-Alcoholic Pina Colada",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "author": {
    "@type": "Person",
    "name": "Mary Stone"
  },
  "datePublished": "2024-03-10",
  "description": "This non-alcoholic pina colada is everyone's favorite!",
  "recipeCuisine": "American",
  "prepTime": "PT1M",
  "cookTime": "PT2M",
  "totalTime": "PT3M",
  "keywords": "non-alcoholic, tropical, summer",
  "recipeYield": "4 servings",
  "recipeCategory": "Drink",
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "120 calories"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 5,
    "ratingCount": 18
  },
  "recipeIngredient": [
    "400ml of pineapple juice",
    "100ml cream of coconut",
    "ice"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "name": "Blend",
      "text": "Blend 400ml of pineapple juice and 100ml cream of coconut until smooth.",
      "url": "https://example.com/recipe#step1",
      "image": "https://example.com/photos/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Fill",
      "text": "Fill a glass with ice.",
      "url": "https://example.com/recipe#step2"
    },
    {
      "@type": "HowToStep",
      "name": "Pour",
      "text": "Pour the pineapple juice and coconut mixture over ice.",
      "url": "https://example.com/recipe#step3"
    }
  ],
  "video": {
    "@type": "VideoObject",
    "name": "How to Make Pina Colada",
    "description": "Watch how to make this refreshing drink.",
    "thumbnailUrl": "https://example.com/video-thumb.jpg",
    "contentUrl": "https://example.com/video.mp4",
    "uploadDate": "2024-03-10T08:00:00+00:00",
    "duration": "PT3M"
  }
}
```

---

## Multiple Items on a Page

### Nesting Approach
```json
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Banana Bread",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.7,
    "ratingCount": 123
  },
  "video": {
    "@type": "VideoObject",
    "name": "How To Make Banana Bread"
  }
}
```

### Array Approach
```json
[
  {
    "@context": "https://schema.org/",
    "@type": "Recipe",
    "name": "Banana Bread"
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [...]
  }
]
```

---

## Dynamic Generation with JavaScript

For SPAs, dynamic content, or CMS integrations, structured data can be generated client-side using JavaScript.

### Method 1: Google Tag Manager (GTM)

**Best for:** Sites already using GTM, marketing teams managing structured data

**Setup:**
1. Install GTM on your site
2. Add a Custom HTML tag to your container
3. Insert structured data block with GTM variables
4. Publish the container
5. Test with Rich Results Test (URL mode)

**GTM Example with Variables:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "{{recipe_name}}",
  "image": ["{{recipe_image}}"],
  "author": {
    "@type": "Person",
    "name": "{{recipe_author}}"
  },
  "datePublished": "{{recipe_date}}",
  "description": "{{recipe_description}}"
}
</script>
```

**GTM Variable Setup:**
- Create Data Layer variables or Custom JavaScript variables
- Extract values from page elements or data layer
- Reduces duplication between page content and markup

### Method 2: Custom JavaScript

**Best for:** SPAs, API-driven content, custom implementations

**Basic DOM Injection:**
```javascript
// Create and inject structured data
function injectStructuredData(data) {
  const script = document.createElement('script');
  script.setAttribute('type', 'application/ld+json');
  script.textContent = JSON.stringify(data);
  document.head.appendChild(script);
}

// Example: Article structured data
const articleData = {
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": document.querySelector('h1').textContent,
  "image": document.querySelector('article img')?.src,
  "datePublished": document.querySelector('time')?.getAttribute('datetime'),
  "author": {
    "@type": "Person",
    "name": document.querySelector('.author-name')?.textContent
  }
};

injectStructuredData(articleData);
```

**API-Driven Generation:**
```javascript
// Fetch data from API and inject structured data
fetch('https://api.example.com/recipes/123')
  .then(response => response.json())
  .then(recipe => {
    const structuredData = {
      "@context": "https://schema.org/",
      "@type": "Recipe",
      "name": recipe.title,
      "image": recipe.images,
      "author": {
        "@type": "Person",
        "name": recipe.author.name
      },
      "datePublished": recipe.publishedAt,
      "description": recipe.summary,
      "recipeIngredient": recipe.ingredients,
      "recipeInstructions": recipe.steps.map((step, i) => ({
        "@type": "HowToStep",
        "position": i + 1,
        "text": step.instruction
      }))
    };

    const script = document.createElement('script');
    script.setAttribute('type', 'application/ld+json');
    script.textContent = JSON.stringify(structuredData);
    document.head.appendChild(script);
  });
```

**React/Next.js Example:**
```jsx
import Head from 'next/head';

function ProductPage({ product }) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": product.name,
    "image": product.images,
    "description": product.description,
    "brand": {
      "@type": "Brand",
      "name": product.brand
    },
    "offers": {
      "@type": "Offer",
      "url": `https://example.com/products/${product.slug}`,
      "priceCurrency": "USD",
      "price": product.price,
      "availability": product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock"
    }
  };

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </Head>
      {/* Page content */}
    </>
  );
}
```

### Method 3: Server-Side Rendering (Recommended)

For frameworks supporting SSR (Next.js, Nuxt, etc.), include structured data in the rendered HTML output for best reliability.

```javascript
// Next.js getServerSideProps example
export async function getServerSideProps({ params }) {
  const product = await fetchProduct(params.id);

  return {
    props: {
      product,
      structuredData: {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        // ... complete structured data
      }
    }
  };
}
```

### JavaScript Generation: Important Considerations

**Testing Requirements:**
- Always use **URL input** in Rich Results Test (not code input)
- Code input has JavaScript limitations
- Test the actual rendered page, not source code

**Product Markup Warning:**
Dynamically-generated Product markup can:
- Reduce shopping crawl frequency
- Affect reliability for fast-changing content (price, availability)
- Require sufficient server resources for increased Google traffic

**Best Practices:**
1. Use GTM variables to extract data from page (avoid duplication)
2. Ensure JavaScript executes before Google renders
3. Test with Mobile-Friendly Test to verify rendering
4. Consider SSR for critical structured data
5. Monitor Search Console for rendering issues

---

## Implementation Checklist

### Before Deployment
- [ ] Use JSON-LD format (recommended)
- [ ] Include all required properties for type
- [ ] Add recommended properties for quality
- [ ] Use most specific Schema.org type
- [ ] Markup matches visible page content
- [ ] Images are crawlable and indexable
- [ ] Dates use ISO 8601 with timezone
- [ ] URLs are fully qualified

### Testing
- [ ] Validate with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Check [Schema.org validator](https://validator.schema.org/)
- [ ] Test with URL Inspection tool in Search Console
- [ ] Verify no manual actions in Search Console

### After Deployment
- [ ] Submit sitemap for recrawling
- [ ] Monitor Rich Results report in Search Console
- [ ] Allow several days for indexing
- [ ] Track performance changes

---

## Common Mistakes to Avoid

1. **Marking up invisible content** - Only mark up content users can see
2. **Misleading markup** - Content must match what's marked up
3. **Missing required properties** - Each type has mandatory fields
4. **Wrong timezone format** - Always include UTC offset
5. **Using midnight (00:00:00)** - Only if event actually starts at midnight
6. **Low-quality images** - Use high-res images meeting size requirements
7. **Blocking Googlebot** - Don't use robots.txt or noindex on structured data pages
8. **Duplicate markup inconsistency** - All versions of a page need identical markup
9. **Using deprecated formats** - Don't use data-vocabulary.org

---

## Validation Tools

1. **Rich Results Test**: https://search.google.com/test/rich-results
2. **Schema.org Validator**: https://validator.schema.org/
3. **Search Console URL Inspection**: Test live URLs
4. **Search Console Rich Results Report**: Monitor status

---

## Resources

- [Google Search Central - Structured Data](https://developers.google.com/search/docs/appearance/structured-data)
- [Generate Structured Data with JavaScript](https://developers.google.com/search/docs/appearance/structured-data/generate-structured-data-with-javascript)
- [Schema.org Full Hierarchy](https://schema.org/docs/full.html)
- [Google Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Rich Results Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)

---

## Notes

- Rich results are not guaranteed even with correct markup
- Google's algorithms determine when to show rich results
- Violations can result in manual actions (loss of rich result eligibility)
- Keep markup updated when page content changes
- Test after any significant changes

---

**Source**: Google Search Central Documentation
**Last Updated**: January 2026
**Version**: 1.1

### Changelog
- **1.1**: Added JavaScript generation section (GTM, custom JS, React/Next.js, SSR)
- **1.0**: Initial release with 8 structured data types
