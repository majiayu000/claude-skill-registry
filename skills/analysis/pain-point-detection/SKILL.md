---
name: pain-point-detection
description: Identifying buying signals and pain points from public information including job postings, reviews, news, and social media. Triggers when analyzing prospect readiness or searching for opportunities.
---

# Pain Point Detection

## Overview

This skill teaches how to identify buying signals and pain points from publicly available information. It covers signal taxonomy, interpretation, and how to translate signals into conversation angles.

## Usage

The company-researcher sub-agent references this skill when:
- Analyzing job postings for scaling signals
- Reviewing Glassdoor/review site content
- Interpreting news and announcements
- Detecting competitive pressure

## Signal Categories

### High-Intent Signals (Act Now)

| Signal | Source | Interpretation |
|--------|--------|----------------|
| Relevant job posting | LinkedIn, careers page | Active need in your domain |
| RFP/vendor review | Industry sources | Formal buying process |
| Budget cycle timing | Industry knowledge | Decision window open |
| Contract expiration | CRM data, research | Replacement opportunity |

### Medium-Intent Signals (Engage Soon)

| Signal | Source | Interpretation |
|--------|--------|----------------|
| Funding announcement | News, Crunchbase | Budget likely available |
| Leadership change | LinkedIn, news | New priorities possible |
| Expansion news | Press releases | Growth = new needs |
| Competitor mention | Social, reviews | Considering alternatives |

### Low-Intent Signals (Nurture)

| Signal | Source | Interpretation |
|--------|--------|----------------|
| Industry conference | Event listings | Educating themselves |
| Content engagement | Social media | Interest in topic |
| General hiring | Job boards | Company growing |

## Detection Techniques

### Job Posting Analysis

**What to look for:**
- Roles in your domain (suggests need)
- Seniority level (indicates priority)
- Number of similar postings (scale of need)
- Tech requirements (compatibility)

**Example:**
> "Seeking 3 Data Operations Managers" = scaling ops team, likely overwhelmed

### Review Site Analysis

**Glassdoor patterns:**
- "Fast-paced" / "scaling quickly" = growing pains
- "Tool sprawl" / "disconnected systems" = integration need
- "Manual processes" = automation opportunity
- "Communication issues" = collaboration tools

### News Analysis

**Positive signals:**
- Funding (Series B+ especially)
- Expansion to new markets
- Large customer wins
- Strategic partnerships

**Timing signals:**
- Q4 budget planning mentions
- "2024 priorities" articles
- Annual report releases

## Resources

- `resources/signal-taxonomy.md` - Complete signal classification
- `resources/job-posting-signals.md` - Job posting interpretation guide
- `resources/review-sentiment-signals.md` - Review site analysis guide
