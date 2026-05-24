---
name: academic-research
description: Search academic papers across arXiv, PubMed, Semantic Scholar, bioRxiv, medRxiv, Google Scholar, and more. Get BibTeX citations, download PDFs, analyze citation networks. Use for literature reviews, finding papers, and academic research.
version: 1.0.0
---


# Academic Research Papers

Search and retrieve academic papers via multiple MCP servers.

## Available Servers

### paper-search
Multi-source paper search covering:
- arXiv, PubMed, bioRxiv, medRxiv
- Google Scholar, IACR, Semantic Scholar
- BibTeX export support

### semantic-scholar  
Full Semantic Scholar API access:
- Citation network analysis
- Author search
- Paper recommendations
- BibTeX, APA, MLA, Chicago formats

### arxiv
arXiv-specific search:
- Advanced search filters
- Citation analysis
- BibTeX, JSON, CSV, Markdown export

## When to Use

- Literature reviews
- Finding related papers
- Getting BibTeX citations
- Checking who cited a paper
- Finding papers by author
- Searching for specific topics

## Example Usage

### Search for Papers
```
paper_search(query="transformer attention mechanism", sources=["arxiv", "semantic_scholar"])
```

### Get Citations
```
semantic_scholar_citations(paper_id="...")
```

### arXiv Specific
```
arxiv_search(query="quantum computing", max_results=10)
```

## Other Available Servers (Not Installed)

From your `/Users/alice/worlds/l/mcp_servers.json`:
- `research-hub-mcp` - 11 sources + Unpaywall PDF access
- `zotero-mcp` - Connect to Zotero library
- `openalex-mcp` - 250M+ works database
- `crossref-mcp` - DOI metadata

Add more with:
```json
"server-name": {
  "command": "npx",
  "args": ["-y", "server-package-name"]
}
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `algorithms`: 19 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.