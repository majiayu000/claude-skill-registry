---
name: firecrawl-scraper
description: Extract property data from real estate listing URLs using Firecrawl AI. Use when scraping Zillow, Redfin, Realtor.com, or any property listing site. Returns structured data ready for video generation.
allowed-tools: Read, Grep, Glob, Bash
---

# Firecrawl Property Extraction

## Overview
Firecrawl transforms any real estate listing URL into structured JSON data for video generation. It handles JavaScript rendering, anti-bot measures, and image extraction automatically.

## Quick Start

```typescript
import Firecrawl from '@mendable/firecrawl-js';
import { z } from 'zod';

const firecrawl = new Firecrawl({
  apiKey: process.env.FIRECRAWL_API_KEY
});

const result = await firecrawl.extract({
  urls: [listingUrl],
  prompt: 'Extract property details for video generation',
  schema: PropertySchema
});
```

## Supported Sites

| Site | URL Pattern | Data Quality |
|------|-------------|--------------|
| Zillow | zillow.com/homedetails/* | Excellent |
| Redfin | redfin.com/*/home/* | Excellent |
| Realtor.com | realtor.com/realestateandhomes-detail/* | Excellent |
| Trulia | trulia.com/home/* | Good |
| Homes.com | homes.com/property/* | Good |
| MLS Sites | Varies by region | Good |
| Broker Sites | Any | Variable |

## Property Schema

See [rules/property-extraction.md](rules/property-extraction.md) for complete schema.

```typescript
const PropertySchema = z.object({
  address: z.string(),
  city: z.string(),
  state: z.string(),
  zipCode: z.string(),
  price: z.number(),
  bedrooms: z.number(),
  bathrooms: z.number(),
  sqft: z.number(),
  lotSize: z.string().optional(),
  yearBuilt: z.number().optional(),
  propertyType: z.string(),
  description: z.string(),
  features: z.array(z.string()),
  images: z.array(z.string()),
  agent: z.object({
    name: z.string(),
    phone: z.string().optional(),
    brokerage: z.string().optional(),
  }).optional(),
});
```

## Advanced Extraction

### Competitor Analysis
```typescript
const CompetitorSchema = z.object({
  listings: z.array(z.object({
    address: z.string(),
    price: z.number(),
    daysOnMarket: z.number(),
    pricePerSqft: z.number(),
  })),
  marketTrends: z.object({
    medianPrice: z.number(),
    averageDaysOnMarket: z.number(),
    inventoryCount: z.number(),
  }),
});
```

### Market Data
See [rules/market-data.md](rules/market-data.md)

## Best Practices

1. **Rate Limiting**: Max 10 requests/minute on standard plan
2. **Error Handling**: Always wrap in try/catch
3. **Image Quality**: Request high-res images when available
4. **Caching**: Cache results for 24 hours to save credits
5. **Validation**: Always validate extracted data with Zod

## API Integration

### Next.js Route Handler
```typescript
// /app/api/scrape/route.ts
export async function POST(request: Request) {
  const { url } = await request.json();

  const firecrawl = new Firecrawl({
    apiKey: process.env.FIRECRAWL_API_KEY!
  });

  const result = await firecrawl.extract({
    urls: [url],
    prompt: 'Extract property listing data',
    schema: PropertySchema,
  });

  return Response.json({
    success: true,
    data: result.data
  });
}
```

## Credit Usage

| Operation | Credits |
|-----------|---------|
| /scrape (single page) | 1 |
| /crawl (per page) | 1 |
| /extract (AI) | Tokens-based |
| /map (URL discovery) | 1 per 100 URLs |

## Error Handling

```typescript
try {
  const result = await firecrawl.extract({ ... });
} catch (error) {
  if (error.statusCode === 429) {
    // Rate limited - wait and retry
  } else if (error.statusCode === 403) {
    // Site blocked - try alternative approach
  } else {
    // Log and return fallback
  }
}
```
