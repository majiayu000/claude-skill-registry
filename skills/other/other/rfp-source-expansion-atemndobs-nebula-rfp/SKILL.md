---
name: RFP Source Expansion
description: Guidelines for integrating additional RFP data sources beyond RFPMart
---

# RFP Source Expansion Skill

This skill provides guidance for expanding RFP data sources to include SAM.gov, eMMA, and other platforms.

## Data Source Priority

Based on strategic analysis, integrate sources in this order:

1. **SAM.gov** - Federal opportunities (highest quality, API available)
2. **Maryland eMMA** - State/local opportunities (target geography)
3. **GovTribe** - Market intelligence (paid, API available)
4. **BidNet Direct** - Broad SLED coverage
5. **DemandStar** - State/local agencies

## Unified Data Model

All sources should normalize to a common `RFP` interface:

```typescript
interface NormalizedRfp {
  // Identity
  id: string;                    // Convex-generated
  externalId: string;            // Source platform ID
  source: RfpSource;             // Enum of sources
  
  // Core fields
  title: string;
  summary: string;
  fullDescription?: string;
  url: string;
  
  // Dates
  postedDate?: Date;
  deadline?: Date;
  questionDeadline?: Date;
  
  // Location
  location?: string;
  state?: string;
  country?: string;
  isRemoteAllowed?: boolean;
  
  // Classification
  category?: string;
  naicsCode?: string;
  pscCode?: string;
  
  // Budget
  budgetMin?: number;
  budgetMax?: number;
  budgetText?: string;
  
  // Eligibility
  eligibility?: EligibilityInfo;
  
  // Attachments
  attachments?: Attachment[];
  
  // Metadata
  fetchedAt: Date;
  rawData?: string; // JSON of original response
}

interface EligibilityInfo {
  usaOrgOnly: boolean;
  requiresOnshore: boolean;
  setAsideType?: string[];       // "8(a)", "WOSB", "SDVOSB", etc.
  requiredCertifications?: string[];
  securityClearance?: string;
  onsiteRequired?: boolean;
}

enum RfpSource {
  SAM_GOV = "sam.gov",
  RFPMART = "rfpmart",
  EMMA = "emma",
  GOVTRIBE = "govtribe",
  BIDNET = "bidnet",
  DEMANDSTAR = "demandstar",
}
```

## SAM.gov Integration

### API Access

SAM.gov provides a public "Get Opportunities" API:
- **Endpoint**: `https://api.sam.gov/opportunities/v2/search`
- **Rate Limits**: 10-1000 requests/day depending on role
- **Auth**: API key required (register at sam.gov)

### Query Parameters

```typescript
interface SamGovSearchParams {
  api_key: string;
  postedFrom?: string;      // YYYY-MM-DD
  postedTo?: string;
  limit?: number;           // Max 1000
  offset?: number;
  ptype?: string;           // Procurement type: o, p, k, r, s, etc.
  solnum?: string;          // Solicitation number
  title?: string;           // Title keyword
  deptname?: string;        // Department name
  naics?: string;           // NAICS code filter
}
```

### Sample Query

```typescript
async function fetchSamGovOpportunities(params: SamGovSearchParams) {
  const baseUrl = 'https://api.sam.gov/opportunities/v2/search';
  const queryParams = new URLSearchParams({
    api_key: params.api_key,
    limit: String(params.limit ?? 100),
    ...(params.postedFrom && { postedFrom: params.postedFrom }),
    ...(params.title && { title: params.title }),
  });
  
  const response = await fetch(`${baseUrl}?${queryParams}`);
  return response.json();
}
```

### Response Mapping

```typescript
function mapSamGovToNormalized(samRfp: SamGovOpportunity): NormalizedRfp {
  return {
    externalId: samRfp.noticeId,
    source: RfpSource.SAM_GOV,
    title: samRfp.title,
    summary: samRfp.description ?? '',
    url: samRfp.uiLink,
    postedDate: new Date(samRfp.postedDate),
    deadline: samRfp.responseDeadLine ? new Date(samRfp.responseDeadLine) : undefined,
    location: samRfp.placeOfPerformance?.state?.name,
    state: samRfp.placeOfPerformance?.state?.code,
    country: 'USA',
    naicsCode: samRfp.naicsCode,
    eligibility: {
      usaOrgOnly: true, // Federal contracts generally require this
      requiresOnshore: true,
      setAsideType: samRfp.typeOfSetAside ? [samRfp.typeOfSetAside] : undefined,
    },
    fetchedAt: new Date(),
  };
}
```

## Eligibility Gating

### Hard Rejection Rules

Before scoring, check these conditions and auto-reject:

```typescript
interface EligibilityGateResult {
  eligible: boolean;
  reason?: string;
  action: 'ok' | 'reject' | 'partner_needed';
}

function checkEligibility(rfp: NormalizedRfp, companyProfile: CompanyProfile): EligibilityGateResult {
  // Check USA organization requirement
  if (rfp.eligibility?.usaOrgOnly && !companyProfile.isUsaBased) {
    return {
      eligible: false,
      reason: 'Requires USA-based organization',
      action: companyProfile.hasUsPartner ? 'partner_needed' : 'reject',
    };
  }
  
  // Check onshore requirement
  if (rfp.eligibility?.requiresOnshore && !companyProfile.hasOnshoreStaff) {
    return {
      eligible: false,
      reason: 'Requires onshore staffing',
      action: 'partner_needed',
    };
  }
  
  // Check set-aside requirements
  if (rfp.eligibility?.setAsideType?.length) {
    const hasQualification = rfp.eligibility.setAsideType.some(
      type => companyProfile.certifications.includes(type)
    );
    if (!hasQualification) {
      return {
        eligible: false,
        reason: `Set-aside for: ${rfp.eligibility.setAsideType.join(', ')}`,
        action: 'reject',
      };
    }
  }
  
  // Check security clearance
  if (rfp.eligibility?.securityClearance && !companyProfile.hasSecurityClearance) {
    return {
      eligible: false,
      reason: 'Requires security clearance',
      action: 'reject',
    };
  }
  
  return { eligible: true, action: 'ok' };
}
```

### Eligibility Detection Patterns

Keywords to detect in RFP text:

```typescript
const ELIGIBILITY_PATTERNS = {
  usaOrgOnly: [
    /usa\s*(only|organization|based)/i,
    /united states\s*(only|organization|based)/i,
    /must be.*u\.?s\.?\s*(company|organization|entity)/i,
  ],
  requiresOnshore: [
    /onshore\s*(only|requirement|staff)/i,
    /domestic\s*(performance|delivery)/i,
    /work.*performed.*within.*united states/i,
  ],
  securityClearance: [
    /security clearance/i,
    /clearance.*required/i,
    /secret|top secret|ts\/sci/i,
  ],
  certifications: [
    /8\(a\)/i,
    /wosb|women.?owned/i,
    /sdvosb|service.?disabled.?veteran/i,
    /hubzone/i,
    /small.*business/i,
  ],
};

function detectEligibilityFromText(text: string): Partial<EligibilityInfo> {
  const eligibility: Partial<EligibilityInfo> = {};
  
  eligibility.usaOrgOnly = ELIGIBILITY_PATTERNS.usaOrgOnly.some(p => p.test(text));
  eligibility.requiresOnshore = ELIGIBILITY_PATTERNS.requiresOnshore.some(p => p.test(text));
  
  return eligibility;
}
```

## Deduplication

When ingesting from multiple sources, deduplicate:

```typescript
async function deduplicateRfp(newRfp: NormalizedRfp, ctx: MutationCtx): Promise<boolean> {
  // Check by external ID + source
  const existingByExternalId = await ctx.db
    .query("rfps")
    .withIndex("by_external_id", q => 
      q.eq("externalId", newRfp.externalId).eq("source", newRfp.source)
    )
    .first();
  
  if (existingByExternalId) {
    // Update existing
    await ctx.db.patch(existingByExternalId._id, {
      ...newRfp,
      fetchedAt: Date.now(),
    });
    return false; // Not a new RFP
  }
  
  // Check by title similarity (fuzzy match)
  // If same title from different source, link them
  const similar = await findSimilarByTitle(ctx, newRfp.title);
  if (similar) {
    // Insert but mark as potential duplicate
    await ctx.db.insert("rfps", {
      ...newRfp,
      potentialDuplicateOf: similar._id,
    });
    return true;
  }
  
  // Insert as new
  await ctx.db.insert("rfps", newRfp);
  return true;
}
```

## Background Refresh Architecture

Use Convex scheduled functions for automated refresh:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

crons.interval(
  "refresh-sam-gov",
  { hours: 6 }, // Every 6 hours
  internal.rfpIngestion.refreshSamGov
);

crons.interval(
  "refresh-rfpmart", 
  { hours: 24 }, // Daily
  internal.rfpIngestion.refreshRfpmart
);

export default crons;
```

## Service Interface Pattern

Create a connector interface for each source:

```typescript
// services/sourceConnector.ts
interface RfpSourceConnector {
  source: RfpSource;
  fetch(params: FetchParams): Promise<NormalizedRfp[]>;
  healthCheck(): Promise<boolean>;
}

class SamGovConnector implements RfpSourceConnector {
  source = RfpSource.SAM_GOV;
  
  async fetch(params: FetchParams): Promise<NormalizedRfp[]> {
    // Implementation
  }
  
  async healthCheck(): Promise<boolean> {
    // Check API availability
  }
}

// Registry
const connectors: Record<RfpSource, RfpSourceConnector> = {
  [RfpSource.SAM_GOV]: new SamGovConnector(),
  [RfpSource.RFPMART]: new RfpMartConnector(),
  // ...
};
```
