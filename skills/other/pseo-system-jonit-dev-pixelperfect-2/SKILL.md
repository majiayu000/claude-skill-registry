---
name: pseo-system
description: Create and manage programmatic SEO pages. Use when creating new pSEO pages, adding content to existing categories, or validating SEO quality.
---

# pSEO System

## Quick Reference

### Directory Structure

```
app/(pseo)/                    # Route group (not in URL)
├── {category}/[slug]/page.tsx # Dynamic routes
├── _components/pseo/          # Templates and sections
│   ├── templates/             # Page templates
│   └── sections/              # Reusable sections
└── _components/seo/           # Schema markup

app/seo/data/                  # JSON data files
├── tools.json
├── formats.json
├── scale.json
├── use-cases.json
├── comparisons.json
├── alternatives.json
├── guides.json
└── free.json

lib/seo/                       # Core SEO utilities
├── pseo-types.ts              # TypeScript interfaces
├── data-loader.ts             # Data loading with cache
├── url-utils.ts               # URL validation/generation
├── schema-generator.ts        # JSON-LD schemas
├── metadata-factory.ts        # Metadata generation
└── keyword-mappings.ts        # Keyword-to-page mapping
```

## Adding a New Page

### 1. Choose the Category

| Category     | Use Case                   | Template                |
| ------------ | -------------------------- | ----------------------- |
| tools        | AI tools and features      | ToolPageTemplate        |
| formats      | File format pages          | FormatPageTemplate      |
| scale        | Resolution/dimension pages | ScalePageTemplate       |
| use-cases    | Industry applications      | UseCasePageTemplate     |
| compare      | Competitor comparisons     | ComparePageTemplate     |
| alternatives | "X alternatives" pages     | AlternativePageTemplate |
| guides       | How-to tutorials           | GuidePageTemplate       |
| free         | Free tool landing pages    | FreePageTemplate        |

### 2. Create Page Data

Add to the appropriate JSON file in `/app/seo/data/`:

```json
{
  "slug": "your-page-slug",
  "title": "Page Title",
  "metaTitle": "SEO Title - Benefit | MyImageUpscaler",
  "metaDescription": "150-160 chars with keyword and CTA.",
  "h1": "Main Heading",
  "intro": "Intro paragraph for the page.",
  "primaryKeyword": "main keyword",
  "secondaryKeywords": ["kw1", "kw2", "kw3"],
  "lastUpdated": "2025-12-26T00:00:00Z",
  "category": "tools"
  // ... category-specific fields
}
```

### 3. Update Meta Count

```json
{
  "meta": {
    "totalPages": 9, // Increment this
    "lastUpdated": "2025-12-26T00:00:00Z"
  }
}
```

## Type Interfaces

### Base Fields (all pages)

```typescript
interface IBasePSEOPage {
  slug: string; // URL path segment
  title: string; // Display title
  metaTitle: string; // SEO title (50-60 chars)
  metaDescription: string; // Meta description (150-160 chars)
  h1: string; // Page heading
  intro: string; // Introduction text
  primaryKeyword: string; // Main target keyword
  secondaryKeywords: string[]; // Related keywords
  ogImage?: string; // Open Graph image
  lastUpdated: string; // ISO 8601 date
}
```

### Category-Specific

```typescript
// Tools: features, useCases, benefits, howItWorks, faq
IToolPage extends IBasePSEOPage

// Formats: formatName, extension, characteristics, bestPractices
IFormatPage extends IBasePSEOPage

// Scale: resolution, dimensions, useCases, benefits
IScalePage extends IBasePSEOPage

// Use Cases: industry, challenges, solutions, results
IUseCasePage extends IBasePSEOPage

// Compare: comparisonType, products, criteria, verdict
IComparisonPage extends IBasePSEOPage

// Alternatives: originalTool, alternatives, comparisonCriteria
IAlternativePage extends IBasePSEOPage

// Guides: guideType, difficulty, steps, tips
IGuidePage extends IBasePSEOPage

// Free: toolName, features, limitations, upgradePoints
IFreePage extends IBasePSEOPage
```

## SEO Guidelines

### Title Optimization

```
✅ "AI Image Upscaler - Enlarge to 4K Free | MyImageUpscaler" (58 chars)
❌ "Best AI Image Upscaler Tool Online Free No Watermark" (too stuffed)
```

### Meta Description

```
✅ "Upscale images up to 8x with AI. Free tool preserves text and logos. No watermarks. Try now." (95 chars + CTA)
❌ "Our image upscaler is the best tool for upscaling images online." (no value prop)
```

### URL Slugs

```
✅ ai-image-upscaler
✅ png-to-jpg-converter
❌ AIImageUpscaler (no uppercase)
❌ ai_image_upscaler (no underscores)
```

## Data Loading Pattern

```typescript
// lib/seo/data-loader.ts pattern
import { cache } from 'react';
import toolsData from '@/app/seo/data/tools.json';

export const getToolData = cache(async (slug: string) => {
  return toolsData.pages.find(p => p.slug === slug) || null;
});

export const getAllToolSlugs = cache(async () => {
  return toolsData.pages.map(p => p.slug);
});
```

## Route Pattern

```typescript
// app/(pseo)/{category}/[slug]/page.tsx
import { getToolData, getAllToolSlugs, generateMetadata } from '@/lib/seo';
import { ToolPageTemplate } from '../_components/pseo/templates/ToolPageTemplate';
import { SchemaMarkup } from '../_components/seo/SchemaMarkup';
import { generateToolSchema } from '@/lib/seo';

export async function generateStaticParams() {
  const slugs = await getAllToolSlugs();
  return slugs.map(slug => ({ slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const data = await getToolData(slug);
  if (!data) return {};
  return generateMetadata(data, 'tools');
}

export default async function Page({ params }) {
  const { slug } = await params;
  const data = await getToolData(slug);
  if (!data) notFound();

  const schema = generateToolSchema(data);
  return (
    <>
      <SchemaMarkup schema={schema} />
      <ToolPageTemplate data={data} />
    </>
  );
}
```

## Sitemap Generation

Each category has a sitemap at `/app/sitemap-{category}.xml/route.ts`:

```typescript
export async function GET() {
  const pages = await getAllToolSlugs();
  const urls = pages.map(slug => ({
    loc: `${BASE_URL}/tools/${slug}`,
    lastmod: new Date().toISOString(),
    changefreq: 'weekly',
    priority: 0.8,
  }));
  return new Response(generateSitemapXML(urls), {
    headers: { 'Content-Type': 'application/xml' },
  });
}
```

## Schema Markup

JSON-LD schemas are generated per category:

- **Tools**: `SoftwareApplication` + `FAQPage` + `BreadcrumbList`
- **Guides**: `HowTo` + `Article` + `FAQPage`
- **Compare**: `Article` + `Review` + `FAQPage`
- **Use Cases**: `Article` + `FAQPage`

## Validation Checklist

Before deploying new pSEO pages:

- [ ] Slug is lowercase, hyphenated, max 60 chars
- [ ] metaTitle is 50-60 chars with primary keyword
- [ ] metaDescription is 150-160 chars with CTA
- [ ] primaryKeyword is unique across all pages
- [ ] All required interface fields are populated
- [ ] FAQ has 3+ meaningful questions
- [ ] relatedTools/relatedGuides use valid slugs
- [ ] JSON is valid, meta.totalPages updated
- [ ] `yarn verify` passes
- [ ] Build completes without errors

## Keyword Research

Reference files:

- `/app/seo/keywords.csv` - Full keyword list (1,340+ keywords)
- `/app/seo/top_keywords.csv` - Priority keywords (103)
- `/lib/seo/keyword-mappings.ts` - Page-to-keyword assignments

## Common Patterns

### Adding Features Array

```json
"features": [
  {
    "title": "Feature Name",
    "description": "What it does and why users care",
    "icon": "optional-icon-name"
  }
]
```

### Adding FAQ

```json
"faq": [
  {
    "question": "Is this tool free?",
    "answer": "Yes, 10 free uses per month with no watermarks."
  }
]
```

### Adding Use Cases

```json
"useCases": [
  {
    "title": "E-commerce Products",
    "description": "Meet marketplace requirements for image size",
    "example": "Upscale a 400px image to 1600px for Amazon"
  }
]
```
