---
name: academic-research
description: Search academic papers, build literature reviews, and synthesize research findings — combines Exa MCP (research_paper category, arxiv filtering) with arxiv-mcp-server for paper discovery, download, and deep analysis. Triggers on academic paper, literature review, research synthesis, arxiv, find papers, scholarly search.
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
| Bot-protected sites | Obscura `--stealth` | Scrapling (Turnstile) |
| Batch stealth scrape | Obscura `scrape` | - |

### Source Extraction Escalation

When a source isn't on ArXiv or Exa can't reach it, escalate through:

1. **ArXiv MCP** → paper is on arXiv (free, full text, best quality)
2. **Exa contents** → URL known, site allows crawling
3. **Firecrawl** → JS-heavy site, no anti-bot
4. **Obscura `--stealth`** → site fingerprints headless browsers (JSTOR, Scholar, Persée, PubMed, Academia.edu)
5. **Scrapling** → site uses Cloudflare Turnstile

### Obscura Stealth Extraction (Tier 3)

For gated academic sources that block standard headless browsers via canvas/WebGL fingerprinting. Not for bypassing paywalls — for extracting publicly visible metadata, abstracts, and open-access content.

**Verified sites** (2026-04-24): Google Scholar, JSTOR, Persée, PubMed, Academia.edu, Perseus Digital Library.

```bash
# Quick metadata extraction (auto-detects site type from URL)
bash ~/.claude/skills/academic-research/scripts/academic_stealth_fetch.sh URL

# With explicit site type
bash ~/.claude/skills/academic-research/scripts/academic_stealth_fetch.sh URL scholar

# Direct Obscura usage
obscura fetch --stealth --quiet URL --eval "JS_EXPRESSION"
```

See `references/obscura-academic-patterns.md` for site-specific JS extraction patterns and gotchas.

## Best Practices

1. **Start broad** with Exa's research_paper category, then narrow
2. **Use date filtering** for recent developments
3. **Download key papers** via arXiv MCP for persistent access
4. **Cross-reference** multiple search approaches
5. **Use technical terms** in queries for better results

## Domain: Subquadratic Attention

Research domain for post-transformer attention mechanisms that break the O(n^2) barrier. Active area with rapid publication cadence (2024–2026).

### Key Papers

| Paper | Year | Key Contribution |
|-------|------|------------------|
| FlashAttention-2 (Dao) | 2023 | IO-aware exact attention — foundation for all subsequent work |
| DuoAttention | 2024 | Split attention heads into retrieval (sparse) vs streaming (full) |
| Ring Attention | 2024 | Distributed sequence parallelism across devices |
| MoBA (Mixture of Block Attention) | 2025 | Block-sparse top-k gating with Triton kernel, 1M tokens |
| NSA (Native Sparse Attention, DeepSeek) | 2025 | Hardware-aligned sparse attention patterns |
| TokenSelect | 2025 | Dynamic per-layer token pruning |

### Pre-Built Search Queries

```
# Exa (research_paper category)
"subquadratic attention mechanism" --category "research paper" --after 2024-01-01
"block sparse attention triton kernel" --category "research paper"
"mixture of attention heads sparse" --category "research paper"
"linear attention transformer approximation" --category "research paper" --after 2024-06-01

# ArXiv (cs.LG + cs.CL)
search_papers({ query: "subquadratic attention sparse transformer", max_results: 20, sort_by: "submitted_date" })
search_papers({ query: "block sparse FlashAttention kernel", max_results: 10 })
```

### Evaluation Criteria

When comparing subquadratic attention mechanisms, benchmark on:

| Criterion | What to Measure |
|-----------|-----------------|
| Quality | Perplexity degradation vs full attention at target sequence length |
| Speed | Wall-clock speedup on consumer GPUs (RTX 4090, M4 Max) |
| Memory | Reduction factor at 128K / 512K / 1M context |
| Compatibility | Drop-in replacement vs requires retraining |
| Sparsity | How much computation is actually skipped (e.g., 95% at 1M tokens) |

### Local Implementation Reference

Working MoBA implementation with Triton kernels: `~/Desktop/Aldea/01-Repos/perplexity-clone/model/moba_block_sparse.py`

---

## Reference Documentation

For detailed parameters and advanced usage:
- `references/exa-academic-search.md` - Exa parameters for academic search
- `references/arxiv-mcp-tools.md` - ArXiv MCP server tool reference
- `references/obscura-academic-patterns.md` - Site-specific Obscura extraction patterns with JS expressions and gotchas
