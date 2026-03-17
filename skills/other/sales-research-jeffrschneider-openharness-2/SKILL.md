---
name: sales-research
description: Best practices for prospect research including company analysis, contact profiling, and signal detection. Triggers when researching companies, contacts, or preparing for sales calls.
---

# Sales Research

## Overview

This skill provides methodology and best practices for researching sales prospects. It covers company research, contact profiling, and signal detection to surface actionable intelligence.

## Usage

The company-researcher and contact-researcher sub-agents reference this skill when:
- Researching new prospects
- Finding company information
- Profiling individual contacts
- Detecting buying signals

## Research Methodology

### Company Research Checklist

1. **Basic Profile**
   - Company name, industry, size (employees, revenue)
   - Headquarters and key locations
   - Founded date, growth stage

2. **Recent Developments**
   - Funding announcements (last 12 months)
   - M&A activity
   - Leadership changes
   - Product launches

3. **Tech Stack**
   - Known technologies (BuiltWith, StackShare)
   - Job postings mentioning tools
   - Integration partnerships

4. **Signals**
   - Job postings (scaling = opportunity)
   - Glassdoor reviews (pain points)
   - News mentions (context)
   - Social media activity

### Contact Research Checklist

1. **Professional Background**
   - Current role and tenure
   - Previous companies and roles
   - Education

2. **Influence Indicators**
   - Reporting structure
   - Decision-making authority
   - Budget ownership

3. **Engagement Hooks**
   - Recent LinkedIn posts
   - Published articles
   - Speaking engagements
   - Mutual connections

## Resources

- `resources/signal-indicators.md` - Taxonomy of buying signals
- `resources/research-checklist.md` - Complete research checklist

## Scripts

- `scripts/company-enricher.py` - Aggregate company data from multiple sources
- `scripts/linkedin-parser.py` - Structure LinkedIn profile data
