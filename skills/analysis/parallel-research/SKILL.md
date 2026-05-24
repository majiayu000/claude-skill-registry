---
name: parallel-research
description: AI-powered deep research using Parallel AI APIs for chat, research reports, entity discovery, and data enrichment. Use this skill when doing web research, competitive analysis, market research, generating research reports, finding companies matching criteria, or enriching existing data. Triggers on research requests, competitive intelligence, finding companies, or data enrichment tasks.
---

# Parallel Research

## Overview

Deep web research, competitive intelligence, entity discovery, and data enrichment using Parallel AI's specialized APIs.

## Quick Decision Tree

```
What do you need?
│
├── Quick factual answer (3-5 seconds)
│   └── Chat API ($0.005/request)
│   └── Script: scripts/parallel_research.py chat "question"
│
├── Comprehensive research report (5min-2hr)
│   └── Deep Research API ($0.30/report for ultra)
│   └── Script: scripts/parallel_research.py research "topic"
│
├── Find entities matching criteria (companies, people)
│   └── FindAll API ($0.03 + $0.10/match)
│   └── Script: scripts/parallel_research.py findall "query"
│
└── Enrich existing data (add fields to records)
    └── Task API with schema ($0.025/record for core)
    └── Script: scripts/parallel_research.py enrich data.csv
```

## Environment Setup

```bash
# Required in .env
PARALLEL_API_KEY=your_api_key_here
```

Get your API key: https://platform.parallel.ai/settings/api-keys

## Common Usage

### Quick Q&A
```bash
python scripts/parallel_research.py chat "What is Anthropic's latest funding round?"
```

### Deep Research Report
```bash
python scripts/parallel_research.py research "Competitive landscape of AI code editors in 2025" --processor ultra
```

### Find Companies
```bash
python scripts/parallel_research.py findall "AI code editor companies that raised funding in 2024-2025" --limit 50
```

### Basic Research (Simplified)
```bash
python scripts/basic_research.py "Company Name"
```

### Vendor Selection
```bash
python scripts/vendor_selection.py "CRM software" --requirements "enterprise,API,automation"
```

## Processor Tiers

| Processor | Cost/1K | Latency | Best For |
|-----------|---------|---------|----------|
| `lite` | $5 | 10-60s | Basic metadata |
| `base` | $10 | 15-100s | Simple research |
| `core` | $25 | 1-5min | Cross-referenced research |
| `pro` | $100 | 2-10min | Exploratory research |
| `ultra` | $300 | 5-25min | Deep research (recommended) |
| `ultra-fast` | $300 | 2-10min | Speed + quality |

## Cost Estimates

| Task | API | Cost |
|------|-----|------|
| 100 quick questions | Chat | $0.50 |
| Market research report | Deep Research (ultra) | $0.30 |
| Find 50 competitors | FindAll (core) | ~$5.00 |
| Enrich 100 leads | Task (core) | $2.50 |

## Free Tier

20,000 requests free (combined across all APIs).

## Security Notes

### Credential Handling
- Store `PARALLEL_API_KEY` in `.env` file (never commit to git)
- Regenerate keys at https://platform.parallel.ai/settings/api-keys
- Never log or print API keys in script output
- Use environment variables, not hardcoded values

### Data Privacy
- Research queries are sent to Parallel AI servers
- Research outputs may contain third-party company information
- Results are stored locally in `.tmp/` directory
- Parallel AI may log queries for service improvement
- Avoid including sensitive internal data in research queries

### Access Scopes
- API key provides full access to all research endpoints
- No granular permission scopes available
- Monitor usage and costs via Parallel AI dashboard

### Compliance Considerations
- **Data Sources**: Research pulls from public web sources
- **Citation**: Always cite sources in research outputs
- **Accuracy**: AI-generated research should be verified
- **Competitive Intel**: Ensure competitive research complies with policies
- **Third-Party Data**: Respect intellectual property of sources
- **PII in Results**: Research results may contain company/individual PII
- **Data Freshness**: Verify currency of time-sensitive information

## Troubleshooting

### Common Issues

#### Issue: Processor timeout
**Symptoms:** Request times out or returns partial results
**Cause:** Complex query requiring more processing time than allowed
**Solution:**
- Use a faster processor tier (`lite` or `base` instead of `ultra`)
- Simplify the research query
- Break complex queries into multiple smaller requests
- Increase timeout in script if configurable

#### Issue: Credits exhausted
**Symptoms:** "Insufficient credits" or quota error
**Cause:** Account credits depleted
**Solution:**
- Check balance at https://platform.parallel.ai/dashboard
- Upgrade plan or purchase additional credits
- Use lower-cost processor tiers for less critical queries
- Monitor usage to avoid unexpected depletion

#### Issue: Invalid response format
**Symptoms:** JSON parsing error or unexpected response structure
**Cause:** API returned error or malformed response
**Solution:**
- Check query format matches API requirements
- Retry the request (may be transient issue)
- Verify API key is valid and active
- Review API documentation for expected response format

#### Issue: Empty or irrelevant results
**Symptoms:** Research returns no results or off-topic content
**Cause:** Query too narrow, ambiguous, or poorly structured
**Solution:**
- Broaden the search query
- Add context to clarify query intent
- Try different phrasing or keywords
- Use Chat API first to validate query understanding

#### Issue: API authentication failed
**Symptoms:** "Invalid API key" or 401 error
**Cause:** API key expired, invalid, or not set
**Solution:**
- Regenerate key at https://platform.parallel.ai/settings/api-keys
- Verify `PARALLEL_API_KEY` is set correctly in `.env`
- Check for leading/trailing whitespace in key
- Ensure key has not been revoked

#### Issue: Rate limited
**Symptoms:** 429 error or "rate limit exceeded"
**Cause:** Too many concurrent requests
**Solution:**
- Add delays between requests
- Reduce parallel request count
- Implement exponential backoff
- Contact support for higher rate limits if needed

## Resources

- **references/api-guide.md** - Complete API documentation
- **references/basic-research.md** - Simple company research
- **references/vendor-selection.md** - Vendor comparison workflow

## Integration Patterns

### Research to Report
**Skills:** parallel-research → content-generation
**Use case:** Create polished reports from research findings
**Flow:**
1. Run deep research on topic/company
2. Generate structured research output
3. Format into branded document via content-generation

### FindAll to CRM
**Skills:** parallel-research → attio-crm
**Use case:** Populate CRM with discovered companies
**Flow:**
1. Use FindAll to discover companies matching criteria
2. Enrich each company with additional data
3. Create/update company records in Attio CRM

### Research to Sheets
**Skills:** parallel-research → google-workspace
**Use case:** Build research database in Google Sheets
**Flow:**
1. Run FindAll or batch research on multiple entities
2. Structure results as tabular data
3. Upload to Google Sheets for team collaboration
