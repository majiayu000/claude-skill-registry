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

## Usage

Run the python script `search_papers.py` to perform searches.

### Arguments

*   `query` (required): The search term.
*   `--limit` (optional): Max results (default 5).
*   `--year` (optional): Year range (e.g., "2023-2025").
*   `--sort` (optional): Sort by "relevance" or "citationCount" (default "relevance").
*   `--open-access` (optional): Only return open access papers.

### Example

```bash
# Find top 5 seminal papers on "Large Language Models"
python3 search_papers.py "Large Language Models" --sort citationCount --limit 5

# Find recent research on "RAG" from 2024
python3 search_papers.py "Retrieval Augmented Generation" --year 2024-2025
```

## Output Format

The script outputs a JSON object (or JSON-lines) containing:
*   `title`
*   `authors`
*   `year`
*   `abstract` (truncated if too long)
*   `citationCount`
*   `url`
*   `pdf_url` (if available)

## Tips for the Agent

*   **Be Skeptical**: High citation count doesn't always mean "correct," but it means "influential."
*   **Check Recency**: For fast-moving fields (AI), prioritize year > citations.
*   **Contextualize**: When summarizing, mention *who* wrote it (e.g., "DeepMind," "Stanford") and *when*.
