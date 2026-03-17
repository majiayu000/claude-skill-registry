---
name: justice-matrix-research
description: Ralph research agent for discovering global youth justice cases and advocacy campaigns
---

# Justice Matrix Research Agent

## When to Use
- Discovering new global youth justice cases
- Finding advocacy campaigns worldwide
- Updating the Justice Matrix database
- Checking source health and coverage gaps
- Running scheduled research cycles

## Commands

| Command | Purpose | Duration |
|---------|---------|----------|
| `/ralph-matrix-scan` | Run discovery across active sources | 10-30 min |
| `/ralph-matrix-extract` | Process pending discoveries | 5-15 min |
| `/ralph-matrix-status` | Show pipeline status and stats | Instant |
| `/ralph-matrix-source [name]` | Deep dive specific source | 10 min |

## Workflow

```
DISCOVER → EXTRACT → QUEUE → REVIEW → APPROVE
   ↓          ↓         ↓        ↓         ↓
Sources    AI Parse  Pending   Admin    Database
```

### 1. Source Scan (`/ralph-matrix-scan`)

```typescript
// Query active sources by priority
const sources = await supabase
  .from('justice_matrix_sources')
  .select('*')
  .eq('is_active', true)
  .order('scrape_priority', { ascending: true });

// For each source:
// 1. Fetch pages
// 2. Extract case/campaign links
// 3. Check for duplicates
// 4. Queue new discoveries
```

### 2. AI Extraction (`/ralph-matrix-extract`)

For each pending discovery:
1. Fetch full content from source URL
2. Run AI extraction using patterns from PRD
3. Geocode to lat/lng
4. Categorize by legal themes
5. Calculate confidence score
6. Check for duplicates

### 3. Review Queue

Discoveries go to `/admin/justice-matrix/discoveries` where admins can:
- Preview extracted data
- Edit before approval
- Approve → creates case/campaign
- Reject → marks as rejected with notes
- Merge → links to existing item

## Source Types

| Type | Extraction Focus |
|------|------------------|
| `court_database` | Citation, year, court, holding, outcome |
| `advocacy_org` | Campaign name, orgs, goals, tactics, status |
| `legal_database` | Case analysis, precedent value |
| `regional_body` | Regional jurisdiction, treaty basis |

## Extraction Patterns

### Court Database
```json
{
  "required": ["case_citation", "jurisdiction", "year", "court"],
  "extract": ["strategic_issue", "key_holding", "outcome"],
  "infer": ["categories", "precedent_strength", "lat/lng"]
}
```

### Advocacy Organization
```json
{
  "required": ["campaign_name", "country_region", "lead_organizations"],
  "extract": ["goals", "tactics", "outcome_status"],
  "infer": ["is_ongoing", "categories", "lat/lng"]
}
```

## Quality Scoring

| Signal | Weight | Description |
|--------|--------|-------------|
| Relevance | 30% | Youth justice / child rights focus |
| Precedent | 25% | Significance for future work |
| Coverage | 20% | Fills geographic/thematic gap |
| Recency | 15% | How current is this? |
| Actionable | 10% | Useful for practitioners |

## Database Tables

| Table | Purpose |
|-------|---------|
| `justice_matrix_sources` | Scraping source configuration |
| `justice_matrix_discovered` | Pending review queue |
| `justice_matrix_scrape_logs` | Run history and stats |
| `justice_matrix_cases` | Approved cases |
| `justice_matrix_campaigns` | Approved campaigns |

## PRD Reference

Full source configuration: `ralph/justice-matrix-prd.json`

## Sacred Boundaries

**Never scrape:**
- Sealed juvenile records
- Private case files
- Paywalled content without permission
- Individual identifying information

**Always mark:**
- Indigenous rights cases
- First Nations advocacy
- Community-controlled campaigns

**Always check:**
- Publication permissions
- Child privacy protections
- Cultural sensitivity

## Example Usage

```bash
# Quick status check
/ralph-matrix-status

# Run full discovery cycle
/ralph-matrix-scan

# Process discoveries
/ralph-matrix-extract

# Deep dive on specific source
/ralph-matrix-source "ECHR HUDOC"
```
