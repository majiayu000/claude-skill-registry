---
name: business-consistency
description: Maintain NAP (Name, Address, Phone) consistency across all platforms. Use when managing citations, updating business info, or generating schema markup.
allowed-tools: Read, Write, Edit
---

# Business Consistency Skill

## Purpose
Ensure 100% consistency of business information across all platforms for NAP accuracy, which directly impacts local SEO rankings.

## The Consistency Master

The `business_consistency_master` table is the SINGLE SOURCE OF TRUTH for all business data.

### Tier 1: Critical NAP (MUST be identical everywhere)
- **Legal Business Name** - Exactly as registered
- **Trading Name** - If different from legal
- **Street Address** - Full formatted address
- **Suburb/City** - Correct suburb name
- **State** - Abbreviation (e.g., QLD)
- **Postcode** - 4 digits
- **Country** - Australia (default)
- **Primary Phone** - Main contact number
- **Phone Format** - Standard format to use

### Tier 2: Essential
- **Website URL** - Primary domain
- **Email Address** - Main contact email
- **Business Hours** - JSON format
- **Primary Category** - Main business type
- **Secondary Categories** - Additional categories

### Tier 3: Important
- **Short Description** - 50 words (for limited platforms)
- **Medium Description** - 100 words
- **Long Description** - 250 words (for platforms that allow it)
- **Service Areas** - Geographic coverage
- **Payment Methods** - Accepted payments

### Tier 4: Australia-Specific
- **ABN** - Format: XX XXX XXX XXX
- **ACN** - Format: XXX XXX XXX
- **License Numbers** - QBCC, electrical, etc.

## Platform Tiers

### Tier 1: Mandatory (Must be claimed and verified)
- Google Business Profile
- Bing Places for Business
- Apple Maps Connect
- Facebook Business Page

### Tier 2: Essential - Australia
- Yellow Pages AU
- True Local
- Hotfrog AU
- StartLocal

### Tier 3: Social Profiles
- LinkedIn Company Page
- Instagram Business
- Twitter/X
- YouTube Channel

### Tier 4: Australian Directories
- Yelp AU
- White Pages AU
- Word of Mouth
- Fyple
- Localsearch
- Find AU

### Tier 5: Industry Specific
- **Trades:** HiPages, ServiceSeeking, Oneflare, Airtasker
- **Healthcare:** HealthEngine, Healthdirect, RateMDs
- **Legal:** LawyersGuide, LawPath, MyBusiness
- **Real Estate:** RealEstate.com.au, Domain, Homely

## Schema.org Markup

### LocalBusiness Schema
Automatically generated from Consistency Master:
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {...},
  "telephone": "+61...",
  "openingHoursSpecification": [...],
  "geo": {...},
  "url": "...",
  "sameAs": [social profiles]
}
```

### Organization Schema
For corporate/larger businesses:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Business Name",
  "legalName": "Legal Entity Name",
  "taxID": "ABN",
  ...
}
```

## Audit Process

### Weekly Spot Check
- Check 1-2 random Tier 1 platforms
- Verify NAP matches master

### Monthly Full Audit
- Check all Tier 1 platforms
- Check 50% of Tier 2-3 platforms
- Generate audit report

### Audit Report Contents
- Overall consistency score (0-100)
- Tier 1 score (weighted 40%)
- Tier 2 score (weighted 30%)
- Platform-by-platform status
- Inconsistencies found
- Recommendations

## When to Use
- Business info changes (address, phone, hours)
- Opening new locations
- Claiming citations
- Generating schema markup
- Monthly NAP audits
- Before SEO campaigns

## Integration Points
- `src/lib/consistency/business-consistency-service.ts` - Main service
- `business_consistency_master` table - Source of truth
- `citation_listings` table - Platform tracking
- `consistency_audit_log` table - Audit history
- ConversionCopywritingEngine - Claim verification

## Citation Listing Status
```
not_claimed → claimed → pending_verification → verified
                                              ↓
                                         needs_update
                                              ↓
                                         suspended
```

## GEO Optimization
For AI search engines (Perplexity, ChatGPT, etc.):
- Entity disambiguation in schema
- Consistent entity references
- Structured data markup
- AI-friendly content

## Output Format
```json
{
  "audit_result": {
    "overall_score": 94,
    "tier1_score": 100,
    "tier2_score": 87,
    "issues_found": 3,
    "recommendations": [...]
  }
}
```
