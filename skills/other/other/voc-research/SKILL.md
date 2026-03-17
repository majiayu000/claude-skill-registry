---
name: voc-research
description: Extract Voice of Customer quotes from forums, reviews, and social media. Use when gathering customer language for copywriting, understanding pain points, or building messaging frameworks.
allowed-tools: Read, Write, Bash, WebFetch, mcp__exa__web_search_exa, mcp__playwright__browser_snapshot
---

# VOC Research Skill

## Purpose
Extract EXACT customer quotes from real sources to inform conversion copywriting with authentic customer language.

## Core Principle
**Verbatim quotes only** - Never summarize. Never paraphrase. Capture the exact words customers use.

## Data Sources
- Reddit (industry subreddits)
- ProductHunt (for SaaS)
- Google Reviews
- TrustPilot
- Facebook Groups
- Industry Forums
- Support Tickets (internal)

## Quote Categories (Per Methodology)

### 1. Pain Points
What frustrates them, what's broken, what keeps them up at night.
**Look for:** complaints, rants, "I hate when...", "Why can't...", "This is ridiculous..."

### 2. Symptoms
Observable problems they describe, what they notice going wrong.
**Look for:** descriptions of issues, "I noticed...", "Whenever I...", "The problem is..."

### 3. Dream Outcomes
What they wish for, ideal scenarios, the transformation they want.
**Look for:** "I wish...", "If only...", "Wouldn't it be great if...", "Imagine if..."

### 4. Failed Solutions
Things they've tried that didn't work, past disappointments.
**Look for:** "I tried X but...", "Nothing works", "I've already done..."

### 5. Buying Decisions
What made them choose or not choose, decision factors.
**Look for:** "What sold me was...", "I finally decided because...", "The reason I switched..."

## Gold Pattern Detection
Quotes that appear 3+ times across sources are **GOLD** for messaging.
These represent common customer language that resonates widely.

## Actions
1. Search forums/reviews for target industry
2. Extract exact quotes (copy-paste, no editing)
3. Categorize into 5 categories
4. Identify patterns (frequency analysis)
5. Mark gold quotes (3+ occurrences)
6. Store in `voc_research` table

## When to Use
- Before writing any landing page copy
- Before creating marketing campaigns
- When updating brand messaging
- During client onboarding
- Before A/B test hypothesis creation

## Integration Points
- `src/lib/agents/voc-research-agent.ts` - Main agent
- `voc_research` table - Storage
- ConversionCopywritingEngine - Consumer

## Output Format
```json
{
  "quote": "Exact customer words here",
  "source": "reddit/r/smallbusiness",
  "category": "pain_point",
  "sentiment": -45,
  "keywords": ["invoice", "late", "chasing"],
  "is_gold": true
}
```

## Quality Rules
1. **No AI-generated quotes** - Must be real customer language
2. **Preserve typos and slang** - Authenticity matters
3. **Include context** - Where was this said? Why?
4. **Date quotes** - Customer language evolves
5. **Verify sources** - Cross-reference when possible
