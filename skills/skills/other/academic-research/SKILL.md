---
name: academic-research
description: This skill should be used for academic paper search, literature reviews, and research synthesis. Combines Exa MCP (research_paper category, arxiv.org filtering) with arxiv-mcp-server for paper discovery, download, and deep analysis. Use when searching for papers, conducting literature reviews, analyzing research trends, or synthesizing findings across multiple papers.
---

# Academic Research

This skill provides comprehensive guidance for academic paper search, literature reviews, and research synthesis using Exa MCP and arxiv-mcp-server.

## When to Use This Skill

- Searching for academic papers on a topic
- Conducting literature reviews
- Finding papers by specific authors
- Discovering recent research in a field
- Downloading and analyzing arXiv papers
- Synthesizing findings across multiple papers
- Tracking citation networks and influential papers
- Researching state-of-the-art methods in AI/ML

## Available Tools

### Exa MCP Server (Web Search with Academic Filtering)

**Tools**: `mcp__exa__web_search_exa`, `mcp__exa__get_code_context_exa`, `mcp__exa__deep_search_exa`

**Key Parameters for Academic Search**:
- `category: "research_paper"` - Filter results to academic papers
- `includeDomains: ["arxiv.org"]` - Restrict to arXiv
- `startPublishedDate` / `endPublishedDate` - Filter by publication date

### ArXiv MCP Server (Paper Search, Download, Analysis)

**Tools**: `search_papers`, `download_paper`, `list_papers`, `read_paper`

**Capabilities**:
- Search arXiv by keyword, author, or category
- Download papers locally (~/.arxiv-papers)
- Read paper content directly
- Deep paper analysis with built-in prompts

## Core Workflows

### Workflow 1: Quick Paper Discovery

**Use case**: Find papers on a specific topic quickly

```
Step 1: Use Exa with research_paper category
mcp__exa__web_search_exa({
  query: "transformer attention mechanisms survey",
  category: "research_paper",
  numResults: 10
})

Step 2: Review titles and abstracts
Step 3: Note arXiv IDs for deeper analysis
```

### Workflow 2: ArXiv-Focused Search

**Use case**: Search specifically within arXiv

```
Step 1: Use arxiv MCP search_papers
search_papers({
  query: "large language models reasoning",
  max_results: 20,
  sort_by: "relevance"
})

Step 2: Download papers
download_paper({ arxiv_id: "2301.00234" })

Step 3: Read and analyze
read_paper({ arxiv_id: "2301.00234" })
```

### Workflow 3: Comprehensive Literature Review

```
Step 1: Broad discovery with Exa (category: "research_paper")
Step 2: Identify key papers and authors
Step 3: Deep dive with arXiv MCP (download + read_paper)
Step 4: Synthesize findings by methodology/approach
```

### Workflow 4: Recent Developments Tracking

```
Step 1: Time-filtered Exa search
mcp__exa__web_search_exa({
  query: "multimodal large language models",
  category: "research_paper",
  startPublishedDate: "2024-01-01"
})

Step 2: Sort arXiv by submitted_date
search_papers({ query: "multimodal LLM", sort_by: "submitted_date" })
```

## ArXiv Categories Reference

| Category | Description |
|----------|-------------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language (NLP) |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.NE | Neural and Evolutionary Computing |
| stat.ML | Statistics - Machine Learning |
| cs.RO | Robotics |

## Academic Domain Filtering

For Exa searches, restrict to academic sources:

```
includeDomains: [
  "arxiv.org",
  "aclanthology.org",
  "openreview.net",
  "proceedings.mlr.press",
  "papers.nips.cc",
  "openaccess.thecvf.com"
]
```

## Tool Selection Guide

| Task | Primary Tool | Alternative |
|------|--------------|-------------|
| Broad topic search | Exa (research_paper) | arXiv search_papers |
| ArXiv-specific | arXiv search_papers | Exa with includeDomains |
| Download paper | arXiv download_paper | - |
| Full paper content | arXiv read_paper | - |
| Code implementations | Exa get_code_context | - |
| Very recent papers | arXiv (submitted_date) | Exa with date filter |

## Best Practices

1. **Start broad** with Exa's research_paper category, then narrow
2. **Use date filtering** for recent developments
3. **Download key papers** via arXiv MCP for persistent access
4. **Cross-reference** multiple search approaches
5. **Use technical terms** in queries for better results

## Reference Documentation

For detailed parameters and advanced usage:
- `references/exa-academic-search.md` - Exa parameters for academic search
- `references/arxiv-mcp-tools.md` - ArXiv MCP server tool reference
