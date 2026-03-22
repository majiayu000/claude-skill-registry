---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Lead Research Assistant
description: "Research company and contact information for sales outreach"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: sales
tags:
  - lead
  - research
  - sales
  - prospecting
department: Sales

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - xlsx_to_json

# Skill Capabilities
capabilities:
  - lead_research
  - company_analysis
  - contact_discovery

# Language Support
languages:
  - en
  - zh
---

# Lead Research Assistant

Research and compile information about companies and contacts for effective sales outreach.

## Overview

This skill helps you:
- Research company backgrounds and key metrics
- Find decision-maker information
- Identify pain points and opportunities
- Prepare personalized outreach
- Prioritize leads by fit

## How to Use

### Company Research
```
"Research [Company Name] for a sales call"
"Give me a briefing on [Company]'s recent news and challenges"
"What should I know before contacting [Company]?"
```

### Contact Research
```
"Find information about [Name] at [Company]"
"Who are the key decision makers at [Company] for [Product Type]?"
"Create a contact profile for [Name, Title, Company]"
```

### Batch Research
```
"Research these 5 companies for our outreach campaign"
"Prioritize these leads based on our ICP"
```

## Output Formats

### Company Brief
```markdown
# Company Research: [Company Name]

## Quick Facts
| Attribute | Value |
|-----------|-------|
| **Industry** | [Industry] |
| **Founded** | [Year] |
| **Headquarters** | [Location] |
| **Employees** | [Range] |
| **Revenue** | [Estimate] |
| **Funding** | [Stage/Amount] |
| **Website** | [URL] |

## Business Overview
[2-3 sentence description of what the company does]

## Products/Services
- [Product 1]: [Brief description]
- [Product 2]: [Brief description]

## Target Market
- **Customers**: [Who they sell to]
- **Industries**: [Industries served]
- **Geography**: [Markets]

## Key People
| Name | Title | LinkedIn |
|------|-------|----------|
| [Name] | CEO | [Link] |
| [Name] | [Relevant Title] | [Link] |

## Recent News & Developments
- [Date]: [Headline - brief summary]
- [Date]: [Headline - brief summary]

## Potential Pain Points
1. **[Pain Point]**: [Why this matters to them]
2. **[Pain Point]**: [Why this matters to them]

## Technology Stack
[Known technologies they use - relevant to your product]

## Competitive Landscape
- Current solutions: [What they use today]
- Competitors: [Their competitors]

## Outreach Angle
**Recommended approach**: [Specific angle based on research]

**Talking points**:
1. [Specific point relevant to them]
2. [Specific point relevant to them]

## Fit Score: [1-10]
**Reasoning**: [Why they are/aren't a good fit]
```

### Contact Profile
```markdown
# Contact Profile: [Name]

## Overview
| Attribute | Value |
|-----------|-------|
| **Name** | [Full Name] |
| **Title** | [Current Title] |
| **Company** | [Company] |
| **Location** | [City, Country] |
| **LinkedIn** | [URL] |
| **Email** | [If available] |

## Professional Background
- **Current Role**: [Title] at [Company] since [Date]
- **Previous**: [Previous role] at [Company]
- **Education**: [Degree, School]
- **Experience**: [X] years in [industry/function]

## Responsibilities
[What they likely own/decide based on title]

## Recent Activity
- [LinkedIn post/article summary]
- [Speaking engagement/podcast]
- [News mention]

## Interests & Topics
[Topics they engage with professionally]

## Connection Points
1. **Shared**: [Mutual connections, schools, interests]
2. **Relevant**: [Content they've engaged with]

## Outreach Strategy
**Best channel**: [Email/LinkedIn/Phone]
**Best time**: [Based on timezone/activity patterns]

**Personalization hooks**:
- [Specific thing to mention]
- [Recent activity to reference]

## Sample Opener
"Hi [Name], I noticed [personalized observation]. [Relevant question/value prop]..."
```

### Lead Prioritization
```markdown
# Lead Scoring: [Campaign Name]

## Scoring Criteria
| Factor | Weight | Description |
|--------|--------|-------------|
| Company Size | 25% | [X-Y employees = 10pts] |
| Industry Fit | 20% | [Target industries = 10pts] |
| Tech Stack | 20% | [Using X = 10pts] |
| Timing Signals | 20% | [Funding, hiring = 10pts] |
| Contact Level | 15% | [Decision maker = 10pts] |

## Ranked Leads

### 🔥 Hot (Score: 80-100)
| Company | Score | Key Signal |
|---------|-------|------------|
| [Company A] | 95 | Recent funding, hiring |
| [Company B] | 88 | Expansion announced |

### 🟡 Warm (Score: 60-79)
| Company | Score | Key Signal |
|---------|-------|------------|
| [Company C] | 72 | Good fit, no timing signal |

### 🔵 Nurture (Score: 40-59)
| Company | Score | Next Step |
|---------|-------|-----------|
| [Company D] | 55 | Monitor for triggers |
```

## Research Areas

### Company Information
- Business model and revenue streams
- Company size and growth trajectory
- Recent news and announcements
- Funding history and investors
- Key partnerships and customers
- Technology stack
- Hiring trends
- Competitive positioning

### Contact Information
- Professional background
- Decision-making authority
- Communication style (from content)
- Network and connections
- Recent professional activity
- Interests and topics

### Timing Signals
- Recent funding rounds
- Leadership changes
- Expansion announcements
- Product launches
- Hiring surges
- Contract renewals (industry timing)

## Best Practices

### Research Ethics
- Use publicly available information only
- Respect privacy boundaries
- Don't misrepresent sources
- Verify information accuracy

### Effective Research
1. Start with company website and LinkedIn
2. Check recent news (last 6 months)
3. Review press releases and blog
4. Look at job postings for insights
5. Check review sites (G2, Glassdoor)
6. Analyze social media presence

## Limitations

- Cannot access paid databases (ZoomInfo, etc.)
- Contact details may not be publicly available
- Information accuracy depends on sources
- Private companies have limited data
- Real-time data may be outdated
