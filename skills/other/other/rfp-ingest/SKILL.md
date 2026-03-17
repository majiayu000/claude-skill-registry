---
name: rfp-ingest
description: Ingest RFP opportunities from multiple data sources (SAM.gov, eMMA, RFPMart). Use when adding new data sources, modifying ingestion logic, or debugging data fetching issues.
allowed-tools: Read, Grep, Glob, Bash(npm:*), Bash(npx:*)
---

# RFP Ingestion Skill

## Overview

This skill helps implement multi-source RFP data ingestion with canonical schema normalization and deduplication.

## Supported Data Sources

| Source | Priority | API Type | Rate Limits |
|--------|----------|----------|-------------|
| SAM.gov | P1 | REST API | 10 req/sec, 10k/day |
| Maryland eMMA | P1 | Web scraping | Respectful crawling |
| RFPMart | Current | REST API | As documented |
| GovTribe | P2 | REST API (paid) | Per subscription |

## Canonical Schema

All sources must normalize to this schema:

```typescript
interface Opportunity {
  externalId: string;         // Source-specific ID
  source: "sam.gov" | "emma" | "rfpmart" | "govtribe";
  title: string;
  description: string;
  summary?: string;
  location: string;
  category: string;
  naicsCode?: string;
  setAside?: string;          // "Small Business", "8(a)", etc.
  postedDate: number;         // Unix timestamp
  expiryDate: number;         // Unix timestamp
  url: string;
  attachments?: Attachment[];
  eligibilityFlags?: string[];
  rawData: Record<string, unknown>;
  ingestedAt: number;
}
```

## SAM.gov Integration

### API Endpoint
```
https://api.sam.gov/opportunities/v2/search
```

### Required Headers
```typescript
{
  "Accept": "application/json",
  "X-Api-Key": process.env.SAM_GOV_API_KEY
}
```

### Example Query
```typescript
const params = new URLSearchParams({
  postedFrom: "2024-01-01",
  postedTo: "2024-12-31",
  limit: "100",
  offset: "0",
  ptype: "o",  // Opportunities only
});
```

### Field Mapping

| SAM.gov Field | Canonical Field |
|---------------|-----------------|
| `noticeId` | `externalId` |
| `title` | `title` |
| `description` | `description` |
| `postedDate` | `postedDate` (parse to timestamp) |
| `responseDeadLine` | `expiryDate` (parse to timestamp) |
| `placeOfPerformance.state` | `location` |
| `naicsCode` | `naicsCode` |
| `setAsideDescription` | `setAside` |

## Convex Implementation

### Ingestion Action

```typescript
// convex/ingestion.ts
import { action, internalMutation } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const ingestFromSam = action({
  args: { daysBack: v.optional(v.number()) },
  handler: async (ctx, args) => {
    const apiKey = process.env.SAM_GOV_API_KEY;
    if (!apiKey) throw new Error("SAM_GOV_API_KEY not configured");

    const fromDate = new Date();
    fromDate.setDate(fromDate.getDate() - (args.daysBack ?? 7));

    const response = await fetch(
      `https://api.sam.gov/opportunities/v2/search?` +
      `api_key=${apiKey}&postedFrom=${fromDate.toISOString().split("T")[0]}&limit=100`,
      { headers: { Accept: "application/json" } }
    );

    if (!response.ok) {
      throw new Error(`SAM.gov API error: ${response.status}`);
    }

    const data = await response.json();
    let ingested = 0;
    let updated = 0;

    for (const opp of data.opportunitiesData ?? []) {
      const result = await ctx.runMutation(internal.rfps.upsert, {
        externalId: opp.noticeId,
        source: "sam.gov",
        title: opp.title ?? "Untitled",
        description: opp.description ?? "",
        location: opp.placeOfPerformance?.state ?? "USA",
        category: opp.naicsCode ?? "Unknown",
        postedDate: new Date(opp.postedDate).getTime(),
        expiryDate: new Date(opp.responseDeadLine).getTime(),
        url: `https://sam.gov/opp/${opp.noticeId}/view`,
        rawData: opp,
      });

      if (result.action === "inserted") ingested++;
      else updated++;
    }

    // Log ingestion
    await ctx.runMutation(internal.ingestion.logIngestion, {
      source: "sam.gov",
      status: "completed",
      recordsProcessed: data.opportunitiesData?.length ?? 0,
      recordsInserted: ingested,
      recordsUpdated: updated,
    });

    return { ingested, updated, source: "sam.gov" };
  },
});
```

### Upsert Mutation

```typescript
// convex/rfps.ts (internal mutation)
export const upsert = internalMutation({
  args: {
    externalId: v.string(),
    source: v.string(),
    title: v.string(),
    description: v.string(),
    location: v.string(),
    category: v.string(),
    postedDate: v.number(),
    expiryDate: v.number(),
    url: v.string(),
    rawData: v.optional(v.any()),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("rfps")
      .withIndex("by_external_id", (q) =>
        q.eq("externalId", args.externalId).eq("source", args.source)
      )
      .first();

    const now = Date.now();

    if (existing) {
      await ctx.db.patch(existing._id, { ...args, updatedAt: now });
      return { id: existing._id, action: "updated" as const };
    }

    const id = await ctx.db.insert("rfps", {
      ...args,
      ingestedAt: now,
      updatedAt: now,
    });
    return { id, action: "inserted" as const };
  },
});
```

## Deduplication Strategy

1. **Exact match**: `externalId` + `source` combination
2. **Title similarity**: Fuzzy match titles within same deadline window
3. **URL canonicalization**: Normalize URLs before comparison

## Eligibility Pre-Filtering

Detect disqualifiers during ingestion:

```typescript
const DISQUALIFIER_PATTERNS = [
  { pattern: /u\.?s\.?\s*(citizen|company|organization)\s*only/i, flag: "us-org-only" },
  { pattern: /onshore\s*(only|required)/i, flag: "onshore-required" },
  { pattern: /on-?site\s*(required|mandatory)/i, flag: "onsite-required" },
  { pattern: /security\s*clearance\s*required/i, flag: "clearance-required" },
  { pattern: /small\s*business\s*set[- ]aside/i, flag: "small-business-set-aside" },
];

function detectEligibilityFlags(text: string): string[] {
  return DISQUALIFIER_PATTERNS
    .filter(({ pattern }) => pattern.test(text))
    .map(({ flag }) => flag);
}
```

## Scheduled Ingestion

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

crons.interval(
  "ingest-sam-gov",
  { hours: 6 },
  internal.ingestion.ingestFromSam,
  { daysBack: 3 }
);

export default crons;
```

## Error Handling

| Error Type | Action |
|------------|--------|
| Rate limit (429) | Exponential backoff, retry after delay |
| Auth error (401/403) | Log error, alert admin |
| Server error (5xx) | Retry up to 3 times |
| Parse error | Log raw data, skip record |

## Testing Approach

1. Mock API responses for unit tests
2. Use sandbox/test endpoints when available
3. Validate schema transformation
4. Test deduplication logic
5. Verify eligibility flag detection
