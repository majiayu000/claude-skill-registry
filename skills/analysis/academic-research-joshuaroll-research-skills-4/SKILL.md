---
name: academic-research
description: A tool for rigorous academic research using Semantic Scholar and ArXiv. Focuses on finding highly-cited papers, retrieving abstracts, and following citation trails to understand the provenance of ideas.
---

# Academic Research Skill

This skill allows you to function as an academic researcher, finding and analyzing scholarly papers with a focus on impact and provenance.

## Capabilities

1.  **Search Papers**: Find papers by keyword, ensuring relevance.
2.  **Analyze Impact**: Filter by citation count to identify seminal works.
3.  **Trace Provenance**: (Optional) Find papers that cite a target paper to seeing how the field evolved.
4.  **Get Details**: Retrieve abstracts and direct PDF links.
5.  **Velocity Metrics**: See citations per year to identify "trending" papers.
6.  **BibTeX Export**: Generate citations for your references.

## Usage

Run the python script `search_papers.py` to perform searches.

### Arguments

*   `query` (required): The search term.
*   `--limit` (optional): Max results (default 5).
*   `--year` (optional): Year range (e.g., "2023-2025").
*   `--sort` (optional): Sort by "relevance", "citationCount", or "velocity" (new!).
*   `--open-access` (optional): Only return open access papers.
*   `--format` (optional): Output "json" (default) or "bibtex".

### Example

```bash
# Find "hot" papers on LLMs (high velocity)
python3 search_papers.py "Large Language Models" --sort velocity

# Get BibTeX for a specific search
python3 search_papers.py "Attention is All You Need" --format bibtex
```

## Output Format

The script outputs a JSON object (or JSON-lines) containing:
*   `title`
*   `authors`
*   `year`
*   `citationCount`
*   `citationsPerYear`: Velocity metric.
*   `tldr`: Semantic Scholar's generated summary (if available).
*   `url`
*   `pdf_url` (if available)

## Tips for the Agent

*   **TLDR vs Abstract**: The `tldr` field is often shorter and easier to digest for quick summaries.
*   **Velocity**: A paper from 2024 with 100 citations is often more relevant than a 2010 paper with 500 citations. Use sort="velocity".
