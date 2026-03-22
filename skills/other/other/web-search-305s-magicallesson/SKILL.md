---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Web Search
# ═══════════════════════════════════════════════════════════════════════════════

name: web-search
description: "Formulate effective web search queries, analyze search results, and synthesize findings. Optimize search strategies for different types of information needs."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: research
tags:
  - search
  - web
  - information-retrieval
  - query-optimization
  - research
department: Research

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
  - query_formulation
  - search_strategy
  - result_analysis
  - source_evaluation
  - information_synthesis

languages:
  - en
  - zh

related_skills:
  - deep-research
  - academic-search
  - news-monitor
---

# Web Search Skill

## Overview

I help you formulate effective web search queries and strategies to find the information you need. I can optimize search queries, suggest alternative approaches, evaluate sources, and synthesize findings.

**What I can do:**
- Formulate optimized search queries
- Suggest search operators and techniques
- Recommend specialized search engines
- Analyze and evaluate search results
- Identify reliable sources
- Synthesize information from multiple sources

**What I cannot do:**
- Execute actual web searches (need external tools)
- Access real-time search results
- Access paywalled content
- Guarantee source accuracy

---

## How to Use Me

### Step 1: Describe Your Information Need

Tell me:
- What you're trying to find
- Why you need this information
- What you've already tried
- Any constraints (time period, source type, language)

### Step 2: Get Search Strategy

I'll provide:
- Optimized search queries
- Alternative query formulations
- Recommended search engines/tools
- Search operators to use

### Step 3: Evaluate Results

If you share results, I can:
- Assess source reliability
- Extract key information
- Identify gaps
- Suggest follow-up searches

---

## Search Query Optimization

### Google Search Operators

| Operator | Usage | Example |
|----------|-------|---------|
| `"exact phrase"` | Exact match | `"climate change policy"` |
| `site:` | Search within site | `site:reddit.com AI tools` |
| `filetype:` | Find specific files | `filetype:pdf annual report` |
| `-word` | Exclude term | `apple -fruit` |
| `OR` | Either term | `startup OR entrepreneur` |
| `intitle:` | Word in title | `intitle:guide python` |
| `inurl:` | Word in URL | `inurl:blog marketing` |
| `before:` | Before date | `AI before:2023-01-01` |
| `after:` | After date | `ChatGPT after:2024-01-01` |
| `*` | Wildcard | `"how to * in python"` |
| `related:` | Similar sites | `related:techcrunch.com` |

### Query Formulation Techniques

#### 1. Start Broad, Then Narrow
```
Broad: electric vehicles
Narrow: electric vehicle battery technology 2024
More narrow: solid-state battery EV range comparison 2024
```

#### 2. Use Synonyms and Variations
```
Original: AI writing tools
Variations:
- artificial intelligence writing software
- AI content generator
- machine learning writing assistant
- GPT writing tool
```

#### 3. Question-Based Queries
```
How: "how to implement SSO"
What: "what is zero trust security"
Why: "why companies use kubernetes"
Best: "best practices API design"
Compare: "AWS vs Azure vs GCP comparison"
```

#### 4. Source-Specific Queries
```
Academic: site:edu OR site:ac.uk [topic]
Government: site:gov [topic]
News: [topic] site:reuters.com OR site:bbc.com
Forum: [topic] site:reddit.com OR site:stackoverflow.com
```

---

## Specialized Search Engines

| Search Engine | Best For | URL |
|---------------|----------|-----|
| Google Scholar | Academic papers | scholar.google.com |
| Semantic Scholar | AI-powered paper search | semanticscholar.org |
| PubMed | Medical/biomedical | pubmed.ncbi.nlm.nih.gov |
| arXiv | Preprints (CS, physics) | arxiv.org |
| Perplexity | AI-powered research | perplexity.ai |
| Wolfram Alpha | Computations, data | wolframalpha.com |
| Statista | Statistics | statista.com |
| Crunchbase | Company data | crunchbase.com |
| Product Hunt | New products | producthunt.com |
| GitHub | Code/projects | github.com |
| Stack Overflow | Programming Q&A | stackoverflow.com |

---

## Source Evaluation Framework

### CRAAP Test

| Criterion | Questions to Ask |
|-----------|-----------------|
| **Currency** | When was it published? Updated? |
| **Relevance** | Does it relate to your topic? Audience? |
| **Authority** | Who is the author? Credentials? |
| **Accuracy** | Is it supported by evidence? Verifiable? |
| **Purpose** | Why was it written? Bias? |

### Source Reliability Tiers

| Tier | Source Type | Reliability |
|------|-------------|-------------|
| Tier 1 | Peer-reviewed journals, official statistics | Highest |
| Tier 2 | Quality news (Reuters, AP), industry reports | High |
| Tier 3 | Company blogs, trade publications | Medium |
| Tier 4 | Social media, forums, wikis | Verify required |
| Tier 5 | Anonymous sources, content farms | Low |

---

## Output Format

```markdown
# Web Search Strategy: [Topic]

**Information Need**: [What you're looking for]
**Search Date**: [Date]

---

## Recommended Search Queries

### Primary Query
```
[Optimized search query with operators]
```
**Rationale**: [Why this query works]

### Alternative Queries
1. `[Alternative query 1]`
   - Use when: [Scenario]
2. `[Alternative query 2]`
   - Use when: [Scenario]
3. `[Alternative query 3]`
   - Use when: [Scenario]

---

## Recommended Search Engines

| Engine | Why | Query Modification |
|--------|-----|-------------------|
| [Engine 1] | [Reason] | [Any modifications] |
| [Engine 2] | [Reason] | [Any modifications] |

---

## Search Strategy

### Step 1: [First search approach]
- Query: `[query]`
- Expected results: [What to look for]

### Step 2: [Second search approach]
- Query: `[query]`
- Expected results: [What to look for]

### Step 3: [Third search approach]
- Query: `[query]`
- Expected results: [What to look for]

---

## Expected Source Types

| Source Type | What to Look For |
|-------------|-----------------|
| [Type 1] | [Specifics] |
| [Type 2] | [Specifics] |

---

## Verification Strategy

1. [How to verify finding 1]
2. [How to verify finding 2]

---

## Potential Challenges

- [Challenge 1]: [How to address]
- [Challenge 2]: [How to address]

---

*Use multiple sources and cross-reference findings for accuracy.*
```

---

## Example Use Cases

### Case 1: Finding Recent Statistics
**Need**: Latest global EV sales figures
**Strategy**:
```
Query: global electric vehicle sales 2024 statistics
Operators: after:2024-01-01 (filetype:pdf OR site:statista.com)
Sources: IEA, Bloomberg NEF, industry reports
```

### Case 2: Technical How-To
**Need**: How to implement OAuth 2.0
**Strategy**:
```
Query: "OAuth 2.0" implementation tutorial
Site-specific: site:stackoverflow.com OR site:auth0.com
Filter: Look for official docs, recent posts
```

### Case 3: Competitive Intelligence
**Need**: Information about a competitor's product
**Strategy**:
```
Query: "[Company name]" product launch OR announcement
Sources: Press releases, news, Product Hunt
Social: site:twitter.com OR site:linkedin.com "[Company]"
```

---

## Tips for Better Results

1. **Start with the end in mind** - know what type of answer you need
2. **Use quotes** for exact phrases
3. **Combine operators** for precision
4. **Try multiple query variations**
5. **Check source dates** - information expires
6. **Cross-reference** findings across sources
7. **Use specialized engines** for specific content types

---

## Limitations

- Cannot execute actual searches
- Cannot access real-time results
- Cannot access paywalled content
- Search engines change their algorithms
- Results vary by location and personalization

---

*Built by the Claude Office Skills community. Contributions welcome!*
