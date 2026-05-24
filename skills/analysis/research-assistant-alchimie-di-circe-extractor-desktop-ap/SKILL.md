---
name: research_assistant
description: Search academic papers, find citations, and explore research using Semantic Scholar. Use when user asks about scientific papers, research, citations, or academic topics.
version: 1.0.0
author: Workshop Team
---

# Research Assistant Skill

Search and explore academic research using the Semantic Scholar API. Access over 214 million papers, 2.49 billion citations, and 79 million authors across all fields of science.

## When to Use

- User asks about scientific or academic papers
- User wants to find research on a topic
- User asks for citations or references
- User wants to understand the state of research in a field
- User asks "what does the research say about..."
- User wants to find papers by a specific author
- User needs to find papers related to another paper

## Available Operations

1. **Paper Search**: Find papers by keywords, title, or abstract
2. **Author Lookup**: Find papers by a specific researcher
3. **Citation Exploration**: Find papers that cite or are cited by a paper
4. **Paper Recommendations**: Get papers similar to a given paper
5. **Paper Details**: Get full metadata including abstract, authors, venue, year

## Instructions

When a user asks about research or academic papers:

### Step 1: Understand the Query

Identify what the user wants:
- **Topic search**: "papers about transformer architectures"
- **Author search**: "papers by Geoffrey Hinton"
- **Citation search**: "what papers cite this one"
- **Recommendations**: "papers similar to Attention Is All You Need"

### Step 2: Load API Reference

ALWAYS read `references/api_reference.md` before making API calls to ensure you use the correct endpoints and parameters.

### Step 3: Construct the Search

**IMPORTANT: Make ONE well-constructed search query.** Do not make multiple API calls with variations of the same query. The API has rate limits, and multiple calls waste quota.

For topic searches, use the paper search endpoint:
```
https://api.semanticscholar.org/graph/v1/paper/search?query=YOUR_QUERY
```

Tips for effective single queries:
- Use specific, focused keywords (e.g., "transformer attention mechanism" not just "transformer")
- Include relevant filters like `year`, `minCitationCount`, or `fieldsOfStudy` to narrow results
- Request enough fields in one call: `title,authors,year,citationCount,abstract,tldr`
- If the first query returns no results, ask the user to refine their search rather than trying variations

Key parameters:
- `query`: Search terms (required)
- `fields`: Which data to return (see API reference)
- `limit`: Number of results (default 10, max 100)
- `offset`: For pagination

### Step 4: Present Results

Format results clearly with:
- Paper title
- Authors (first author et al. if many)
- Year published
- Citation count
- Brief abstract or TLDR if available
- Link to paper (use paperId to construct URL)

### Common City Coordinates (for reference, similar to weather skill pattern)

Not applicable - this skill uses text-based search queries.

### Paper ID Formats

Semantic Scholar accepts multiple ID formats:
| Format | Example |
|--------|---------|
| Semantic Scholar ID | `649def34f8be52c8b66281af98ae884c09aef38b` |
| DOI | `DOI:10.18653/v1/N18-3011` |
| ArXiv | `ARXIV:2106.15928` |
| ACL | `ACL:W12-3903` |
| PubMed | `PMID:19872477` |
| Corpus ID | `CorpusId:215416146` |

## Resources

ALWAYS read these before making API calls:
- `references/api_reference.md` - Complete Semantic Scholar API documentation
- `references/search_tips.md` - Advanced search techniques and query optimization

## Examples

### Example 1: Topic Search
User asks: "Find papers about large language models from 2023"

1. Load API reference
2. Call: `https://api.semanticscholar.org/graph/v1/paper/search?query=large+language+models&year=2023&fields=title,authors,year,citationCount,abstract&limit=10`
3. Format results with titles, authors, years, and citation counts

### Example 2: Author Search
User asks: "What has Yann LeCun published recently?"

1. First find author ID via author search
2. Then get author's papers via author endpoint
3. Filter/sort by year for recent work

### Example 3: Citation Analysis
User asks: "What papers cite 'Attention Is All You Need'?"

1. Find paper ID for "Attention Is All You Need"
2. Use citations endpoint to get citing papers
3. Present most influential citations (by citation count)

### Example 4: Research Overview
User asks: "What does the research say about sleep and memory?"

1. Search for papers on "sleep memory consolidation"
2. Get top cited papers to find influential work
3. Summarize key findings from abstracts
4. Provide references for further reading

## Notes

- The API is free and does not require authentication for basic use
- Rate limit: 1000 requests/second shared among unauthenticated users
- For heavy use, request an API key for dedicated rate limits
- Always include the `fields` parameter to get useful data back
- Papers include TLDRs (AI-generated summaries) when available
- Citation counts are updated regularly but may lag slightly
