---
name: 2026-legal-research-agent
description: >
  Expert legal research agent for finding and scraping expungement data state by state.
  Knows authoritative sources, URL patterns, Firecrawl configuration, and 2026 legal landscape.
  Activate on "find expungement data", "scrape state laws", "legal research", "court URLs",
  "statute sources", "Clean Slate laws", "automatic expungement research".
  NOT for interpreting laws (use national-expungement-expert), building UI, or legal advice.
category: Uncategorized
tags:
  - imported
  - needs-review
---

# 2026 Legal Research Agent

---

## When to Use This Skill

Use this skill when you need to:

- **Find authoritative legal sources** for a specific state's expungement laws
- **Configure Firecrawl jobs** to scrape court systems, legislatures, or legal aid sites
- **Validate scraped data** for accuracy and completeness
- **Research 2026 law changes** including Clean Slate acts and marijuana expungement
- **Build URL patterns** for systematic state-by-state data collection
- **Identify gaps** in existing scraped data coverage

**Do NOT use this skill for:**
- Interpreting what laws mean (use `national-expungement-expert`)
- Building user interfaces or components
- Providing legal advice to users
- General web scraping unrelated to legal data

---

## Core Instructions

### 1. Authoritative Source Hierarchy

When researching expungement laws, prioritize sources in this order:

```
Tier 1 (Primary Authority):
├── State Legislature websites (statute text)
├── State Court Administrative Office
└── State Attorney General publications

Tier 2 (Official Secondary):
├── State Bar Association guides
├── Court self-help centers
└── Public law databases (public.law, justia.com)

Tier 3 (Tertiary but Valuable):
├── Legal aid organizations (LSC grantees)
├── Law school clinics
└── Reentry organizations (CCRC, NACDL)

Tier 4 (Verification Only):
├── Commercial legal databases
├── News articles about law changes
└── Attorney blog posts
```

**Shibboleth**: A novice scrapes the first Google result. An expert knows that `courts.{state}.gov` contains the self-help forms while `legislature.{state}.gov` contains the statute text—and both are needed.

### 2. URL Pattern Knowledge by State Type

States organize their legal resources differently. Know the patterns:

**Unified Court Systems** (courts own everything):
```
California: courts.ca.gov/selfhelp-expungement.htm
Oregon: courts.oregon.gov/programs/exp/Pages/default.aspx
Washington: courts.wa.gov/forms/?fa=forms.contribute&formID=101
```

**Split Systems** (legislature + court separate):
```
Texas: txcourts.gov (forms) + texas.public.law (statutes)
New York: nycourts.gov (forms) + nysenate.gov/legislation/laws (statutes)
Florida: flcourts.gov (forms) + leg.state.fl.us/statutes (statutes)
```

**Public.law States** (excellent statute hosting):
```
oregon.public.law, california.public.law, texas.public.law
michigan.public.law, washington.public.law
```

**Shibboleth**: Knowing that `apps.leg.wa.gov/RCW/` is Washington's statute database while `leg.wa.gov` is the general legislature site—the RCW subdomain is where the actual law text lives.

### 3. 2026 Legal Landscape Awareness

As of 2026, these major changes affect research:

**Clean Slate States** (automatic expungement passed):
- Pennsylvania (2018), Utah (2019), New Jersey (2019), Michigan (2020)
- California (2020), Connecticut (2021), Delaware (2021), Virginia (2021)
- Oklahoma (2022), Colorado (2022), New York (2023), Minnesota (2023)
- Maryland (2024), Illinois (2024), Oregon (2025)

**Marijuana Expungement** (specific statutes):
- Most states now have separate marijuana expungement provisions
- Search for "cannabis conviction" alongside "expungement"
- Check for retroactive application dates

**2025-2026 Law Changes to Verify**:
- Oregon HB 2316 (expanded eligibility)
- California AB 1076 (automatic relief expansion)
- Check CCRC's Restoration of Rights Project for current status

**Shibboleth**: Knowing that "automatic expungement" doesn't mean immediate—Pennsylvania's Clean Slate has a 10-year waiting period for arrests and varies by offense. Research must capture these nuances.

### 4. Firecrawl Configuration Expertise

When configuring scrape jobs:

**Extraction Schema Design**:
```typescript
// For statute pages, extract:
{
  statuteCitation: "string",   // e.g., "ORS 137.225"
  title: "string",             // e.g., "Setting aside conviction"
  fullText: "string",          // Complete statute text
  effectiveDate: "string",     // When current version took effect
  lastAmended: "string",       // Most recent amendment date
  subsections: "array",        // Parsed subsections
}

// For court self-help pages, extract:
{
  stateName: "string",
  expungementPageUrl: "string",
  formsLibraryUrl: "string",
  selfHelpUrl: "string",
  contactPhone: "string",
  feeScheduleUrl: "string",
}

// For forms, extract:
{
  formNumber: "string",        // e.g., "MC-440"
  formTitle: "string",
  pdfUrl: "string",
  applicableTo: "array",       // ["misdemeanor", "arrest"]
  lastUpdated: "string",
}
```

**Rate Limiting for Government Sites**:
```typescript
rateLimit: 2,  // 2 requests/second max for .gov sites
timeout: 90000,  // Government sites can be slow
maxRetries: 3,  // Retry on timeout
waitFor: 3000,  // Wait for JavaScript on modern court sites
```

**Shibboleth**: Knowing to set `onlyMainContent: true` for statute pages (to skip navigation chrome) but `onlyMainContent: false` for forms pages (where the form links are often in sidebars).

### 5. Data Validation Checklist

After scraping, validate:

```
□ Statute citations match official format (e.g., "ORS" not "Or. Rev. Stat.")
□ Effective dates are parseable and reasonable (not future, not too old)
□ URLs are live and return 200 status
□ PDF form links actually download PDFs (not HTML error pages)
□ Phone numbers are in consistent format
□ Fee amounts are numeric and reasonable ($0-$500 typical range)
□ State code extracted correctly (watch for ambiguous URLs)
```

**Common Extraction Errors**:
- "oregon.public.law" matching "la" (Louisiana) instead of "or" (Oregon)
- Statute text truncated at 10,000 characters (increase limit)
- Form "last updated" dates in inconsistent formats
- County-specific URLs mistaken for state-level

### 6. Gap Analysis Process

To identify missing data for a state:

```bash
# Check what we have
ls src/data/scraped/states/{state}/

# Expected files for complete coverage:
# - statutes.json (eligibility rules from statute text)
# - court-system.json (court URLs, contacts, forms links)
# - forms/ (actual PDF forms)
# - fees.json (filing fee amounts)
# - counties/ (county-specific court data)

# Cross-reference with state data file
grep -l "waitingPeriods\|eligibilityRules" src/data/states/{state}.ts
```

**Priority order for filling gaps**:
1. Statutes (foundation for all rules)
2. Court forms (what users actually need to file)
3. Fee information (users need to budget)
4. County contacts (where to file)
5. Spanish resources (accessibility)

---

## Anti-Patterns

### Never Do These:

1. **Scrape without rate limiting** - Government sites will block you
2. **Trust secondary sources for statute text** - Always verify against primary
3. **Assume URL patterns are consistent** - Each state is different
4. **Ignore effective dates** - Laws change; scraped data needs timestamps
5. **Scrape county sites without state context** - County rules supplement, not replace, state law
6. **Skip the self-help sections** - Often have the clearest eligibility summaries
7. **Treat all states the same** - Clean Slate states have fundamentally different processes

### Common Mistakes:

```
❌ Scraping Wikipedia for statute text
✅ Scraping the state legislature's official code

❌ Using findlaw.com as primary source
✅ Using findlaw.com to find the citation, then scraping the official source

❌ Assuming "expungement" is the only term
✅ Searching for: expungement, sealing, set-aside, dismissal, destruction, pardons

❌ Treating waiting periods as simple numbers
✅ Capturing offense-specific waiting periods (felonies vs misdemeanors vs arrests)
```

---

## Project-Specific Context

This skill is designed for the **National Expungement Guide** project:

### Existing Infrastructure

- **Firecrawl scripts**: `scripts/firecrawl/`
- **Job definitions**: `scripts/firecrawl/jobs.ts` (P0-P4 priority jobs)
- **URL config**: `scripts/firecrawl/config.ts` (all 50 states)
- **Output path**: `src/data/scraped/states/{state}/`
- **State data**: `src/data/states/` (TypeScript files per state)

### Running Scrapes

```bash
# Set API key first
export FIRECRAWL_API_KEY=your_key

# Run P0 (state statutes + courts) - ~$0.20 cost
npx tsx scripts/firecrawl/run-p0.ts

# Dry run to preview
npx tsx scripts/firecrawl/run-p0.ts --dry-run

# Check reports
cat scripts/firecrawl/reports/p0-*.json
```

### Data Flow

```
Firecrawl scrape → src/data/scraped/{state}/*.json
       ↓
Manual review + cleanup
       ↓
Integrated into src/data/states/{state}.ts
       ↓
Used by eligibility wizard + PDF generator
```

---

## References

See `references/` folder for:
- `url-patterns-by-state.md` - Complete URL patterns for all 50 states
- `clean-slate-timeline.md` - When each Clean Slate law passed and took effect
- `firecrawl-schemas.md` - All extraction schemas used

---

## Example Workflow

**User request**: "Research California's 2026 expungement laws and scrape the latest data"

**Agent workflow**:
1. Check existing data: `ls src/data/scraped/states/ca/`
2. Verify current statute version at `california.public.law`
3. Check for 2025-2026 law changes via CCRC or news search
4. Update `scripts/firecrawl/config.ts` if URLs changed
5. Run targeted scrape: add CA-specific URLs to P0 job
6. Validate extracted data against known statute citations
7. Document any gaps or changes found
