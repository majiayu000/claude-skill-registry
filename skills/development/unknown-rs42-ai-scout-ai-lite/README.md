# Accelerator Research Agent

Production-ready Claude Desktop skill for researching accelerator portfolio companies using validated MCP tools.

## 🎯 What This Skill Does

Systematically research and analyze accelerator companies with AI-powered structured extraction:

- **Validated Tech Stack**: Firecrawl Extract (100% success rate) + Tavily Search (90%+ enrichment)
- **Structured Extraction**: JSON schemas tested on Y Combinator (20/20) and Fast Forward (5/5)
- **Impact Methodology**: 5-tier rubric for evaluating mission alignment (customizable for any thesis)
- **Professional Outputs**: CSV exports + markdown reports with documented scoring
- **Research-Focused**: Pure research workflow - does NOT create tracking issues

## 🚀 Quick Start

### 1. Install MCP Servers

This skill requires 2 MCP servers configured in Claude Desktop:

**Required** (Both validated in live testing):
- **Firecrawl MCP** - Structured extraction ([firecrawl.dev](https://firecrawl.dev))
  - Tested: 100% success rate on Y Combinator, Fast Forward
  - Free tier: 500 credits/month

- **Tavily MCP** - AI-optimized search ([tavily.com](https://tavily.com))
  - Tested: 90%+ success on company enrichment
  - Free tier: 100 RPM (6,000/hour)

**NOT Recommended**:
- ❌ Coresignal - Too expensive, doesn't cover new startups

📖 **Setup instructions**: Add to `~/Library/Application Support/Claude/claude_desktop_config.json`

### 2. Upload Skill to Claude Desktop

1. Download this repository as ZIP
2. Extract files
3. Copy `SKILL.md` or reference it in your Claude Desktop workflow

### 3. Try It Out

**Test Setup First** (copy from SKILL.md):
```json
{
  "name": "mcp__MCP_DOCKER__firecrawl_extract",
  "arguments": {
    "urls": ["https://www.ffwd.org/directory?portfolio=true"],
    "prompt": "Extract first 3 companies",
    "schema": { /* see SKILL.md for schema */ }
  }
}
```

**Then Request Research**:
```
"Research 10 companies from YC W25 focused on climate tech"
```

Claude will:
1. **Extract** YC W25 companies using `firecrawl_extract` with validated schema
2. **Filter** to 10 climate tech companies from JSON output
3. **Research** each company using `tavily-search` (batch of 10)
4. **Score** using climate tech impact rubric
5. **Generate** CSV + markdown report

## 📊 What You Get

**Output Files**:
- **CSV**: All company data (Excel/Sheets compatible)
- **Markdown**: Detailed research report with analysis

**No Tracking Issues**: This skill does NOT create Linear/project issues. Use a separate Linear skill for pipeline management.

## 💡 Example Use Cases

### Impact Investor
```
"Research Fast Forward portfolio and score for low-income US impact"
```

### Climate Tech VC
```
"Find climate tech companies from Techstars 2024 and evaluate carbon impact"
```

### Healthcare Focus
```
"Research YC healthcare companies serving Medicaid populations"
```

## 🔧 Features

### Validated MCP Tools
- **Firecrawl Extract** (PRIMARY): Structured JSON extraction with 100% success rate
  - Tested on Y Combinator (20/20 companies)
  - Tested on Fast Forward (5/5 companies)
  - Same cost as scrape, better output
- **Tavily Search**: AI-optimized company research (90%+ success rate)
- **Fallback Tools**: `firecrawl_scrape`, `tavily-extract` if needed

### Production-Ready Schemas
- Ready-to-use templates in `SCHEMA-TEMPLATES.md`
- Validated patterns for YC, Fast Forward, Techstars
- Vertical-specific schemas (healthcare, climate, fintech)
- Comprehensive error handling

### Impact Methodology
- 5-tier rubric (Direct → Minimal alignment)
- Systematic evaluation framework
- Customizable for different theses
- Documented reasoning per company

### Output Formats
- CSV with all research data (Excel/Sheets compatible)
- Markdown detailed reports
- Impact distribution analysis

## 📝 Workflow (3 Phases)

### Phase 1: Portfolio Scraping
**PRIMARY**: Use `firecrawl_extract` with JSON schema (100% success rate)
- Returns structured JSON directly (no parsing needed)
- Validated schemas in `SCHEMA-TEMPLATES.md`
- **FALLBACK**: Use `firecrawl_scrape` if extract fails

### Phase 2: Company Research
Deep research using `tavily-search` (90%+ success rate)
- Founder information
- Mission and target market
- Key metrics (users, funding, employees)
- Batch processing (10 companies at a time)

### Phase 3: Impact Scoring & Reports
- Apply 5-tier rubric with documented reasoning
- Generate CSV (Excel/Sheets compatible)
- Generate markdown report with analysis

## 🎨 Customization

### Adapt Impact Rubric

Default: **Low-income US impact**

Easily adapt for:
- **Climate Tech**: Emissions reduction → Greenwashing
- **Healthcare**: Medicaid focus → Luxury medicine
- **Financial Inclusion**: Unbanked → High-net-worth

See `references/impact-scoring.md` for guide.

## 🔒 Prerequisites

### Required
- **Claude Desktop** installed
- **Docker Desktop** running
- API keys for Tavily + Firecrawl
- (Optional) Coresignal API key

## 💰 API Costs

### Free Tier Research (0-500 companies/month)
- **Firecrawl**: 500 credits free
- **Tavily**: 100 RPM free (6,000/hour)
- **Cost**: $0/month
- **Sufficient for**: 10-20 accelerator portfolios

### Paid Tier Research (500+ companies/month)
- **Firecrawl Starter**: $30/month (5,000 credits)
- **Tavily Pro**: $50/month (unlimited within higher rate limits)
- **Cost**: $80/month total
- **Sufficient for**: 100+ accelerator portfolios

**Performance Benchmarks** (from live testing):
- 10 companies: 2-3 minutes, $0 (free tier)
- 50 companies: 10-15 minutes, $5-10 (paid tier)
- 100+ companies: 30-45 minutes, $10-20 (paid tier)

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Complete skill guide (1,145 lines)
  - Phase 1A: `firecrawl_extract` with validated schemas ⭐ PRIMARY
  - Phase 2: `tavily-search` research patterns
  - Phase 3: Impact scoring & report generation
  - Tool-specific best practices
  - Comprehensive troubleshooting (8 common issues)

- **[SCHEMA-TEMPLATES.md](SCHEMA-TEMPLATES.md)** - Ready-to-use extraction schemas
  - Y Combinator schema (tested 20/20)
  - Fast Forward schema (tested 5/5)
  - Healthcare, climate, fintech vertical schemas
  - Schema design guidelines (5 golden rules)
  - Common errors & fixes

## 🛠️ Troubleshooting

**Extract returns empty array `{"companies": []}`**
1. Improve prompt: "Extract all portfolio companies including name, website, description..."
2. Simplify schema: Only require `"name"` field
3. Add `waitFor: 5000` for JavaScript pages
4. Fallback to `firecrawl_scrape`

**"MCP server not found"**
- Check `~/Library/Application Support/Claude/claude_desktop_config.json`
- Restart Claude Desktop completely
- Verify Docker Desktop is running
- Test with simple query: `mcp__MCP_DOCKER__firecrawl_extract` on example.com

**Full troubleshooting guide**: See SKILL.md Section 10 (8 common issues with solutions)

## 📁 File Structure

```
sourcing-agent-demo-skill/
├── SKILL.md                    # Main skill guide (1,145 lines)
├── SCHEMA-TEMPLATES.md         # Production-tested extraction schemas
└── README.md                   # This file - project overview
```

**Key Sections in SKILL.md**:
- Phase 1A: `firecrawl_extract` (PRIMARY) - Lines 53-170
- Phase 2: `tavily-search` research - Lines 232-284
- Phase 3: Impact scoring - Lines 286-417
- Example scenarios with extract - Lines 422-571
- Troubleshooting (8 issues) - Lines 761-1001
- Validation checklist - Lines 1034-1089

## 🔗 Next Steps

After running research:

1. **Review CSV/Markdown reports**
2. **Import to your preferred system**:
   - Airtable/Google Sheets for database view
   - Use separate Linear skill for tracking (if needed)
   - CRM integration for deal pipeline
3. **Customize impact rubric** for your specific thesis
4. **Scale to multiple accelerators** using batch processing

## 🏆 Why This Skill is Production-Ready

**Validated by Live Testing**:
- ✅ `firecrawl_extract`: 100% success (Y Combinator 20/20, Fast Forward 5/5)
- ✅ `tavily-search`: 90%+ success on enrichment queries
- ✅ Free tier sufficient for 10-20 portfolios/month
- ✅ Comprehensive error handling for common issues
- ✅ Tested on real accelerators (not just examples)

**Based on Obsidian Testing Notes**:
- "Firecrawl MCP Comprehensive Capability Assessment.md"
- "Tavily MCP Comprehensive Capability Assessment.md"
- "MCP Pairing Analysis - Accelerator Scout Optimal Stack.md"

## 📝 Version History

**v2.0 - Production-Ready** (Current)
- ✅ Rewrote Phase 1 to use `firecrawl_extract` as primary (100% success rate)
- ✅ Added SCHEMA-TEMPLATES.md with validated patterns
- ✅ Comprehensive troubleshooting for extract function (8 common issues)
- ✅ Decision trees for tool selection
- ✅ Removed Coresignal (too expensive, doesn't cover new startups)

**v1.0 - Initial** (Deprecated)
- Used `firecrawl_scrape` (required manual parsing)
- No validated schemas
- Generic error handling

## 🔗 Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/download)
- [Firecrawl Docs](https://docs.firecrawl.dev)
- [Tavily Docs](https://docs.tavily.com)

---

**Status**: ✅ Production-Ready | **Testing**: Validated on YC, Fast Forward | **Version**: 2.0

