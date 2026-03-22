---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - News Monitor
# ═══════════════════════════════════════════════════════════════════════════════

name: news-monitor
description: "Set up news monitoring strategies, analyze news coverage, and synthesize current events. Create news digests and media analysis reports."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: research
tags:
  - news
  - monitoring
  - media
  - alerts
  - current-events
department: Marketing/PR/Research

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

mcp:
  server: office-mcp
  tools:
    - create_docx

capabilities:
  - news_monitoring_setup
  - media_analysis
  - news_synthesis
  - alert_configuration
  - digest_creation

languages:
  - en
  - zh

related_skills:
  - web-search
  - deep-research
  - competitive-analysis
---

# News Monitor Skill

## Overview

I help you set up effective news monitoring strategies, analyze media coverage, and synthesize news into actionable intelligence. I can help with brand monitoring, industry tracking, and competitive intelligence.

**What I can do:**
- Design news monitoring strategies
- Recommend monitoring tools and RSS feeds
- Create news digest templates
- Analyze media coverage patterns
- Synthesize news into briefings
- Set up alert configurations

**What I cannot do:**
- Access real-time news feeds
- Execute actual monitoring
- Provide breaking news
- Access paywalled news sources

---

## How to Use Me

### Step 1: Define Monitoring Objectives

Tell me what you want to track:
- Company/brand mentions
- Industry news
- Competitor activity
- Specific topics or keywords
- Executive/person mentions
- Regulatory/policy changes

### Step 2: Set Parameters

Specify:
- Geographic scope
- Language preferences
- Source types (news, social, blogs)
- Frequency (real-time, daily, weekly)
- Alert thresholds

### Step 3: Choose Output

- Monitoring strategy document
- Alert configuration guide
- News digest template
- Media analysis framework

---

## Monitoring Strategy Framework

### 1. Keyword Strategy

#### Primary Keywords
```
Brand/Company: "Company Name", CompanyName, @CompanyHandle
Products: "Product Name", product-name
Executives: "CEO Name", "CTO Name"
```

#### Boolean Combinations
```
Simple: "Company Name" OR "Product Name"
Filtered: "Company Name" AND (launch OR announcement OR partnership)
Exclusion: "Company Name" NOT jobs NOT careers
```

#### Competitor Monitoring
```
"Competitor A" OR "Competitor B" AND (funding OR acquisition OR launch)
```

### 2. Source Strategy

| Source Type | Examples | Best For |
|-------------|----------|----------|
| Newswires | Reuters, AP, AFP | Breaking news |
| Business | Bloomberg, FT, WSJ | Financial/corporate |
| Tech | TechCrunch, Verge, Wired | Technology |
| Industry | Trade publications | Sector-specific |
| Social | Twitter, LinkedIn | Real-time sentiment |
| Blogs | Medium, Substack | Thought leadership |
| Forums | Reddit, HN | Community sentiment |

### 3. Tool Recommendations

| Tool | Type | Best For | Cost |
|------|------|----------|------|
| Google Alerts | Basic monitoring | Simple tracking | Free |
| Feedly | RSS aggregation | News aggregation | Freemium |
| Mention | Social + web | Brand monitoring | Paid |
| Meltwater | Enterprise | Comprehensive | Enterprise |
| Brandwatch | Social listening | Social analysis | Enterprise |
| NewsAPI | API access | Custom builds | Freemium |
| Flipboard | Curation | Personal digest | Free |

---

## News Digest Template

```markdown
# [Company/Topic] News Digest

**Period**: [Date range]
**Prepared by**: [Name/Team]
**Distribution**: [Internal/External]

---

## Headlines Summary

### Top Stories This Period
1. **[Headline 1]** - [Source], [Date]
   - Key point: [Summary]
   - Impact: [High/Medium/Low]
   
2. **[Headline 2]** - [Source], [Date]
   - Key point: [Summary]
   - Impact: [High/Medium/Low]

3. **[Headline 3]** - [Source], [Date]
   - Key point: [Summary]
   - Impact: [High/Medium/Low]

---

## Coverage by Category

### Company News
| Date | Headline | Source | Sentiment |
|------|----------|--------|-----------|
| | | | Positive/Neutral/Negative |

### Industry News
| Date | Headline | Source | Relevance |
|------|----------|--------|-----------|
| | | | High/Medium/Low |

### Competitor News
| Date | Headline | Source | Competitor |
|------|----------|--------|------------|
| | | | |

---

## Sentiment Analysis

| Category | Positive | Neutral | Negative | Total |
|----------|----------|---------|----------|-------|
| Company | | | | |
| Products | | | | |
| Executives | | | | |

**Overall Sentiment Trend**: [Improving/Stable/Declining]

---

## Key Themes

### Theme 1: [Name]
[Description and relevant articles]

### Theme 2: [Name]
[Description and relevant articles]

---

## Action Items

1. [ ] [Action based on coverage]
2. [ ] [Action based on coverage]
3. [ ] [Action based on coverage]

---

## Upcoming Events to Watch

| Date | Event | Potential Impact |
|------|-------|-----------------|
| | | |

---

## Sources Monitored

- [List of sources]

---

*Next digest: [Date]*
```

---

## Media Analysis Framework

### Coverage Metrics

| Metric | Description | Calculation |
|--------|-------------|-------------|
| Volume | Number of mentions | Count of articles |
| Reach | Potential audience | Sum of publication reach |
| Share of Voice | Your mentions vs competitors | Your mentions / Total market mentions |
| Sentiment | Tone of coverage | Positive:Neutral:Negative ratio |
| Message Pull-Through | Key message presence | % of articles with key messages |

### Sentiment Classification

| Sentiment | Indicators |
|-----------|------------|
| Positive | Praise, success, growth, innovation |
| Neutral | Factual reporting, announcements |
| Negative | Criticism, problems, failures, concerns |

### Source Authority Tiers

| Tier | Examples | Weight |
|------|----------|--------|
| Tier 1 | WSJ, NYT, Reuters, FT | 10x |
| Tier 2 | Industry leaders, major outlets | 5x |
| Tier 3 | Regional, specialized | 2x |
| Tier 4 | Blogs, small outlets | 1x |

---

## Alert Configuration Guide

### Google Alerts Setup

```
1. Go to google.com/alerts
2. Enter search query:
   "Your Company" OR "Your Product"
3. Show options:
   - How often: As-it-happens / Daily / Weekly
   - Sources: Automatic / News / Blogs / Web
   - Language: [Select]
   - Region: [Select]
   - How many: All results / Best results
4. Create alert
```

### Recommended Alert Categories

| Category | Query Example | Frequency |
|----------|---------------|-----------|
| Brand mentions | "Company Name" | As-it-happens |
| Product mentions | "Product Name" | Daily |
| Executive mentions | "CEO Name" | Weekly |
| Competitor news | "Competitor" AND launch | Daily |
| Industry trends | [industry] AND "trends 2025" | Weekly |
| Negative monitoring | "Company Name" AND (problem OR issue OR complaint) | As-it-happens |

---

## Output Format: Monitoring Strategy

```markdown
# News Monitoring Strategy: [Topic/Brand]

**Prepared**: [Date]
**Review Cycle**: [Quarterly]

---

## Monitoring Objectives

1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

---

## Keyword Strategy

### Primary Keywords
```
[keyword 1]
[keyword 2]
"[exact phrase]"
```

### Boolean Queries

**Brand Monitoring**:
```
"Company Name" OR "Product Name" OR @handle
```

**Competitor Tracking**:
```
("Competitor A" OR "Competitor B") AND (funding OR launch OR partnership)
```

**Industry News**:
```
[industry] AND (trends OR innovation OR market)
```

### Exclusion Terms
```
NOT (jobs OR careers OR hiring)
```

---

## Source Matrix

| Category | Sources | Priority |
|----------|---------|----------|
| Tier 1 News | [List] | High |
| Industry | [List] | High |
| Tech | [List] | Medium |
| Social | [List] | Medium |
| Blogs | [List] | Low |

---

## Tool Configuration

### Primary Tool: [Tool Name]
- Setup instructions
- Query configuration
- Alert settings

### Secondary Tools
- [Tool 2]: [Purpose]
- [Tool 3]: [Purpose]

---

## Workflow

### Daily
1. Review real-time alerts
2. Triage by priority
3. Flag for action

### Weekly
1. Compile digest
2. Analyze trends
3. Share with stakeholders

### Monthly
1. Full analysis report
2. Strategy review
3. Keyword refinement

---

## Distribution

| Stakeholder | Content | Frequency |
|-------------|---------|-----------|
| Executives | Summary | Weekly |
| PR Team | Full digest | Daily |
| Marketing | Competitor intel | Weekly |
| Sales | Battle card updates | As needed |

---

## Success Metrics

1. Coverage volume vs baseline
2. Share of voice vs competitors
3. Sentiment ratio improvement
4. Response time to mentions
```

---

## Tips for Better Results

1. **Be specific** about what you want to monitor
2. **Prioritize sources** based on relevance
3. **Use Boolean operators** to reduce noise
4. **Set appropriate frequency** - not everything needs real-time
5. **Review and refine** keywords regularly
6. **Establish escalation criteria** for urgent mentions

---

## Limitations

- Cannot execute actual monitoring
- Cannot access real-time news
- Cannot access paywalled sources
- Cannot provide breaking news
- Strategy needs manual implementation

---

*Built by the Claude Office Skills community. Contributions welcome!*
