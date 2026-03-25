---
name: web-research-assistant
description: AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for additional information. Designed for OpenClaw and Claude Code.
---

# Web Research Assistant

This skill leverages **BrowserAct API** to provide powerful web research capabilities. When primary web access is restricted or blocked, it automatically searches the internet to find and extract relevant information, ensuring your research tasks are completed successfully.

## ✨ OpenClaw & Claude Code Optimized

**🚀 Works Seamlessly with OpenClaw and Claude Code**

| Platform | Status | Installation |
|----------|--------|--------------|
| **OpenClaw** | ✅ **Highly Recommended** | Copy to `~/.openclaw/skills/` |
| **Claude Code** | ✅ **Highly Recommended** | Native skill support |
| **OpenCode** | ✅ Fully Supported | Copy to `~/.opencode/skills/` |
| **Cursor** | ✅ Fully Supported | Copy to `~/.cursor/skills/` |

**Why This Skill?**
- 🎯 **Purpose-built for OpenClaw and Claude Code**
- 🔄 **Auto-recovery** when web access is restricted
- 🌐 **Global access** - no IP or geoblocking issues
- 💰 **Cost-effective** - saves token usage
- ⚡ **Fast execution** - BrowserAct powered

## 🎯 When to Use

**Web Access Restricted? No Problem!**

Use this skill when:
- 🔒 Target websites block AI assistant access
- 🌍 Geographic restrictions limit content access
- 🔐 Paywalls prevent data extraction
- ⏱️ Need quick supplemental information
- 📊 Research requires multiple data sources
- 🔍 Need current information beyond cached data

## 🔑 API Key Guidance

Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, request the API key from the user:

**Required Message**:
> "Please provide your BrowserAct API Key from [BrowserAct Console](https://www.browseract.com/reception/integrations) to enable web research capabilities."

## 🛠️ Input Parameters

Configure research based on your needs:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | - | Research topic or question |
| `engine` | string | google | Search engine (google, bing, duckduckgo) |
| `max_results` | number | 10 | Results to retrieve (1-50) |
| `content_type` | string | all | Content filter (all, news, articles, data) |
| `time_range` | string | past_month | Time filter (anytime, past_day/week/month/year) |

## 💻 Quick Start

```bash
# Basic research
python web-research-assistant/scripts/research.py "AI technology trends"

# Deep research with more results
python web-research-assistant/scripts/research.py "competitor analysis" --max-results 20

# Current news research
python web-research-assistant/scripts/research.py "market trends" --content-type news

# Save to file
python web-research-assistant/scripts/research.py "industry data" -o research_report.md
```

## 📊 Output

**Structured Research Data:**
- Titles, URLs, snippets, and relevance scores
- Key facts and statistics extraction
- Source citations and references
- Comprehensive research report

## 🎪 What This Skill Does

1. **🔄 Auto-Supplement** - When direct access fails, automatically searches the web
2. **🌐 Global Search** - Bypasses geographic restrictions via BrowserAct
3. **📈 Multi-Source** - Aggregates data from multiple search results
4. **✅ Validation** - Cross-references information for accuracy
5. **📋 Report Generation** - Creates comprehensive research reports

---

## Features


1. **No hallucinations, ensuring stable and accurate data extraction**: Pre-set workflows eliminate AI-generated hallucinations.

2. **No human verification challenges**: Built-in bypass mechanisms eliminate the need to handle reCAPTCHA or other verification challenges.

3. **No IP access restrictions or geofencing**: Overcomes regional IP limitations for stable global access.

4. **Faster execution speed**: Tasks complete more rapidly than purely AI-driven browser automation solutions.

5. **Exceptional cost-effectiveness**: Significantly reduces data acquisition costs compared to token-intensive AI solutions.


---

## 🔧 BrowserAct API Integration

```
Research Request → BrowserAct Search → Data Extraction → Validation → Final Report
```

**Powered by BrowserAct MCP** for reliable, unrestricted web access.

---

## ⚠️ Error Handling

- **Invalid API Key**: Report to user, do not retry
- **Search Failed**: Automatic retry with fallback engine
- **No Results**: Return partial data with notification
- **Timeout**: Extended timeout for large research tasks

---

## 📖 Best Practices

1. Use **specific queries** for targeted results
2. Apply **time filters** for current information
3. **Cross-reference** key findings
4. Choose **appropriate content types** for research goals
5. **Validate** statistics with multiple sources

---

## 🔗 Related Skills

- `amazon-competitor-analyzer` - Amazon competitive intelligence
- `google-maps-search-api-skill` - Business data extraction
- `google-news-api-skill` - News monitoring

---

**Version**: 1.0.0  
**Updated**: 2026-02-08  
**API**: BrowserAct MCP  
**Template ID**: `TEMPLATE_ID_HERE`
