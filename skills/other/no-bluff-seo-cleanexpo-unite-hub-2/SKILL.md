---
name: no-bluff-seo-skill
description: Enforce the No-Bluff SEO/GEO protocol using DataForSEO and SEMRush. Use when generating or modifying any SEO-related copy, claims, or structured data for Synthex or client sites.
allowed-tools: Read, Write, Search
---

# No-Bluff SEO Skill

## Purpose
Ensure every SEO/GEO claim Synthex makes is:
- Verifiable via search/SEO APIs
- Tagged with a confidence score
- Clearly separated between fact, forecast, and opinion

## Data Sources
- DataForSEO API
- SEMRush API
- Internal `seo_providers` and related tables

## Actions
1. Fetch and cross-check keyword metrics.
2. Validate positioning statements against real data.
3. Attach `source`, `metric_type`, and `confidence_score` to generated SEO insights.
4. Update or generate structured data (JSON-LD) where needed.

## When to Use
- Creating landing page copy
- Building comparison pages
- Generating audit reports
- Enriching client reports in the managed services engine

## No-Bluff Protocol Rules

### Rule 1: Source Everything
Every claim must have a source:
- SEMRush data
- DataForSEO data
- Google Search Console
- Ahrefs data
- Direct citation

### Rule 2: Confidence Scoring
All metrics must have confidence:
- `high` (90%+): Direct measurement
- `medium` (70-89%): Derived/calculated
- `low` (50-69%): Estimated/projected
- `uncertain` (<50%): Flagged for review

### Rule 3: No Vanity Metrics
Reject:
- "We're #1 in the industry"
- "Top-rated by customers"
- "Best-in-class solution"

Accept only:
- Specific, measurable claims
- Dated statistics
- Verifiable rankings

### Rule 4: Audit Trail
Every SEO action must be logged:
- What was checked
- What data was found
- What changes were made
- When and by whom

## Structured Data Requirements
- JSON-LD for all product pages
- LocalBusiness schema for service businesses
- Article schema for blog posts
- FAQ schema for common questions
- Review schema (only with real reviews)
