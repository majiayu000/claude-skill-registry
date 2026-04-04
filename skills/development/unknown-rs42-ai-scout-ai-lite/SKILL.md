---
name: accelerator-research-agent
description: Research accelerator portfolio companies using Firecrawl and Tavily MCPs. Generates structured CSV and markdown reports with systematic impact scoring. Optimized for token efficiency.
---

# Accelerator Research Agent

A token-optimized Claude Desktop skill for researching accelerator portfolio companies with systematic impact analysis.

## When to Use This Skill

Activate when user asks to:
- **"Research companies from [accelerator name]"**
- **"Analyze [accelerator] portfolio"**
- **"Score companies for impact"** or **"evaluate mission alignment"**
- Mentions: YC, Techstars, Fast Forward, 500 Global, a16z

## Prerequisites

**Required MCP Servers** (both tested and validated):

1. **Firecrawl MCP** - Structured extraction
   - Free tier: 500 credits/month
   - Use `firecrawl_extract` for JSON extraction

2. **Tavily MCP** - AI-optimized search
   - Free tier: 100 RPM (6,000/hour)
   - Use `tavily-search` for company research

## Core Workflow (3 Phases)

### Phase 1: Portfolio Extraction

**Goal**: Get company list from accelerator portfolio page

**Tool**: `firecrawl_extract` (PRIMARY - 100% success rate)

**Schema Pattern**: See `SCHEMA-TEMPLATES.md` for tested schemas (YC, Fast Forward, Healthcare, Climate, Fintech)

**Quick Schema** (customize based on accelerator):
```json
{
  "name": "mcp__MCP_DOCKER__firecrawl_extract",
  "arguments": {
    "urls": ["PORTFOLIO_URL"],
    "prompt": "Extract all portfolio companies including name, website, description, industry",
    "schema": {
      "type": "object",
      "properties": {
        "companies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "website": {"type": "string"},
              "description": {"type": "string"},
              "industry": {"type": "string"}
            },
            "required": ["name"]
          }
        }
      },
      "required": ["companies"]
    }
  }
}
```

**Token Optimization**:
- Only require `"name"` field
- Use string types for all fields (more flexible)
- Add `"maxAge": 604800000` for caching (7 days)

**If Extract Fails** - Use fallback:
```json
{
  "name": "mcp__MCP_DOCKER__firecrawl_scrape",
  "arguments": {
    "url": "PORTFOLIO_URL",
    "formats": ["markdown"]
  }
}
```
Then manually parse the markdown.

### Phase 2: Company Research

**Goal**: Research each company using web search

**Tool**: `tavily-search` with token-efficient parameters

**CRITICAL - Token Optimization**:
```json
{
  "name": "mcp__MCP_DOCKER__tavily-search",
  "arguments": {
    "query": "[company name] mission target market",
    "max_results": 3,                    // ✅ NOT 10! Saves 70% tokens
    "search_depth": "basic",             // ✅ NOT "advanced"! Faster
    "include_raw_content": false         // ✅ Critical - saves massive tokens
  }
}
```

**Batch Processing** (IMPORTANT):
- Research 3-5 companies at a time (not 10-20)
- Generate incremental reports to avoid token limits

**Research Query Pattern**:
```
"[Company Name] mission target market product"
```

**Extract from Results**:
- Founder names
- Mission/tagline
- Target market demographic
- Product/service description
- Key metrics (users, funding, team size)

### Phase 3: Impact Scoring

**Goal**: Score companies using 5-tier rubric

**5-Tier Impact Rubric** (Customizable):

**⭐⭐⭐⭐⭐ Tier 1 - Direct Impact**
- Primary target: Underserved populations
- Core product addresses fundamental challenges
- Impact central to business model

**⭐⭐⭐⭐ Tier 2 - Strong Alignment**
- Significant focus on underserved
- Clear pathway to reach target communities
- Impact is key differentiator

**⭐⭐⭐ Tier 3 - Moderate Alignment**
- Serves underserved as secondary market
- Impact through indirect channels
- Mixed revenue model

**⭐⭐ Tier 4 - Weak Alignment**
- Minimal underserved focus
- Impact is incidental or aspirational
- Primarily serves mainstream markets

**⭐ Tier 5 - Minimal Alignment**
- No focus on underserved
- Luxury/premium positioning
- Opposite of mission

**Customization Examples**:
- Climate Tech: Direct emissions reduction → Greenwashing
- Healthcare: Medicaid focus → Luxury medicine
- Fintech: Unbanked → High-net-worth

### Phase 4: Report Generation

**CSV Format** (Excel/Sheets compatible):
```csv
Company Name,Website,Description,Industry,Impact Tier,Impact Reasoning,Founder,Funding
```

**Markdown Format**:
```markdown
# [Accelerator] Portfolio Research Report

## Executive Summary
- Total companies researched: X
- Impact distribution: Tier 1 (X), Tier 2 (X), etc.

## High-Impact Companies (Tier 1-2)

### Company Name
- **Website**: [URL]
- **Impact Tier**: ⭐⭐⭐⭐⭐
- **Mission**: [Brief mission]
- **Target Market**: [Demographics]
- **Why High Impact**: [Reasoning]
- **Metrics**: [Users, funding, etc.]

[Repeat for each high-impact company]

## Moderate Impact Companies (Tier 3)
[Summarized list]

## Lower Priority Companies (Tier 4-5)
[Brief list]
```

## Token Management Best Practices

**Critical for Avoiding Limits**:

1. **Batch Processing**: Research 3-5 companies at a time
2. **Tavily Parameters**:
   - `max_results: 3` (not 10)
   - `search_depth: "basic"` (not "advanced")
   - `include_raw_content: false` (saves massive tokens)
3. **Incremental Reports**: Generate partial results, then continue
4. **Schema Efficiency**: Only require essential fields
5. **Caching**: Use `maxAge` parameter for portfolio pages

## Common Scenarios

### Scenario 1: YC Research
```
User: "Research 10 YC W25 climate tech companies"

Steps:
1. Extract YC W25 companies (firecrawl_extract + YC schema)
2. Filter to climate tech vertical (JSON filtering)
3. Research FIRST 5 companies (tavily-search, max_results=3)
4. Score and generate partial report
5. Research NEXT 5 companies (new batch)
6. Append to report
```

### Scenario 2: Fast Forward Impact
```
User: "Score Fast Forward portfolio for low-income US impact"

Steps:
1. Extract Fast Forward companies (firecrawl_extract)
2. Research in batches of 3 (tavily-search)
3. Apply low-income US impact rubric
4. Generate CSV + markdown report
```

### Scenario 3: Healthcare Medicaid
```
User: "Find healthcare startups serving Medicaid populations"

Steps:
1. Extract with healthcare vertical schema (see SCHEMA-TEMPLATES.md)
2. Research with query: "[company] Medicaid low-income healthcare"
3. Filter to Medicaid focus
4. Score using healthcare impact rubric
```

## Troubleshooting

**Token Limit Hit**:
- Reduce batch size to 3 companies
- Use `search_depth: "basic"`
- Set `include_raw_content: false`
- Generate incremental reports

**Extract Returns Empty**:
- Check SCHEMA-TEMPLATES.md for validated schemas
- Improve prompt specificity
- Try fallback to `firecrawl_scrape`

**Search Returns Poor Results**:
- Refine query: "[company name] mission target market"
- Reduce `max_results` to 3
- Try alternative search: "[company name] about"

## Files Reference

- **SCHEMA-TEMPLATES.md**: Production-tested extraction schemas
- **README.md**: Setup instructions and MCP configuration

## Output Deliverables

This skill generates **ONLY research outputs**:
- ✅ CSV file with all company data
- ✅ Markdown report with analysis

This skill does **NOT**:
- ❌ Create Linear/project tracking issues
- ❌ Integrate with CRM systems
- ❌ Send notifications

Use separate skills for pipeline management if needed.

---

**Version**: 2.1 (Token-Optimized) | **Testing**: Validated on YC, Fast Forward
