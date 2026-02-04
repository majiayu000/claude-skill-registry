---
name: arxiv
description: Fetch and summarize arXiv papers. Search by topic, read specific papers by ID or URL, and get plain-language summaries. Use when the user mentions arXiv, asks about research papers, wants to find recent academic work on a topic, or is discussing algorithmic or architectural choices that could benefit from literature review.
allowed-tools: WebFetch, WebSearch
---

# arXiv

Fetch, search, and summarize academic papers from arXiv.

## Usage

- `/arxiv <query>` - Search for recent papers on a topic
- `/arxiv 2401.12345` - Fetch a specific paper by ID
- `/arxiv https://arxiv.org/abs/2401.12345` - Fetch a paper by URL

## Workflow

### Search by Topic

1. Use the arXiv API to search for papers:
   ```
   https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending
   ```
2. Parse the Atom XML response to extract: title, authors, abstract, published date, arxiv ID, categories
3. Present results in a scannable format

### Fetch Specific Paper

When given an arXiv ID (e.g., `2401.12345`) or URL:

1. Extract the ID from the input
   - URL formats: `arxiv.org/abs/XXXX.XXXXX`, `arxiv.org/pdf/XXXX.XXXXX`
   - Raw ID: `XXXX.XXXXX` or `XXXX.XXXXXvN`
2. Fetch the abstract page:
   ```
   https://export.arxiv.org/api/query?id_list={id}
   ```
3. Parse and present the paper details

### Read Full Paper (HTML)

Many recent papers have HTML versions available:
```
https://arxiv.org/html/{id}
```

If the user asks to "read" or "summarize the full paper", try fetching the HTML version first. If unavailable, note that only the abstract is accessible and summarize from that.

## Output Formats

### Search Results

```
ARXIV SEARCH: {query}
═══════════════════════════════════════════════════════════════════

1. {Title}
   {Authors (first 3, et al. if more)}
   {Date} · {Primary category}
   {2-3 sentence plain-language summary of the abstract}
   https://arxiv.org/abs/{id}

2. {Title}
   ...

═══════════════════════════════════════════════════════════════════
```

### Single Paper

```
{Title}
═══════════════════════════════════════════════════════════════════
Authors:    {Full author list}
Published:  {Date}
Categories: {categories}
URL:        https://arxiv.org/abs/{id}

ABSTRACT
───────────────────────────────────────────────────────────────────
{Original abstract}

PLAIN-LANGUAGE SUMMARY
───────────────────────────────────────────────────────────────────
{3-5 sentence summary accessible to a technical but non-specialist reader.
Explain what problem the paper addresses, the approach, and the key results.
Avoid jargon where possible; define it when unavoidable.}

═══════════════════════════════════════════════════════════════════
```

## API Notes

- The arXiv API returns Atom XML. Parse `<entry>` elements for results.
- Rate limit: be respectful, no rapid-fire queries. One search per invocation is fine.
- The API supports boolean queries: `cat:cs.RO AND all:autonomous` (category + keyword)
- Common categories:
  - `cs.RO` - Robotics
  - `cs.AI` - Artificial Intelligence
  - `cs.LG` - Machine Learning
  - `cs.CV` - Computer Vision
  - `cs.CL` - Computation and Language (NLP)
  - `cs.SE` - Software Engineering
  - `stat.ML` - Statistics / Machine Learning
  - `eess.SY` - Systems and Control
  - `math.OC` - Optimization and Control
- For category-specific searches: `search_query=cat:cs.RO+AND+all:{query}`

## Examples

```
User: /arxiv behavioral cloning robotics

Claude: [Fetches arXiv API with query "behavioral cloning robotics"]

ARXIV SEARCH: behavioral cloning robotics
═══════════════════════════════════════════════════════════════════

1. Learning to Navigate Sidewalks from Demonstration
   J. Smith, A. Lee, et al.
   2026-01-15 · cs.RO
   Proposes a behavioral cloning approach for sidewalk navigation
   using teleoperation demonstrations. Achieves 94% success rate
   on unseen environments using a lightweight MLP policy.
   https://arxiv.org/abs/2601.09876

...
```

```
User: /arxiv 2401.12345

Claude: [Fetches specific paper]

Some Paper Title
═══════════════════════════════════════════════════════════════════
Authors:    Jane Doe, John Smith
Published:  2024-01-23
Categories: cs.RO, cs.AI
URL:        https://arxiv.org/abs/2401.12345

ABSTRACT
───────────────────────────────────────────────────────────────────
{abstract text}

PLAIN-LANGUAGE SUMMARY
───────────────────────────────────────────────────────────────────
{accessible summary}
═══════════════════════════════════════════════════════════════════
```
