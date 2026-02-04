---
name: academic-benchmark-researcher
description: When the user requests information about academic benchmarks, datasets, or research papers, particularly in machine learning, deep learning, or logical reasoning domains. This skill enables systematic research of academic benchmarks by searching web sources, downloading and analyzing arXiv papers, extracting key metadata (number of tasks, training availability, difficulty levels), and compiling comparative summaries. It triggers on requests involving dataset comparisons, benchmark analysis, or academic paper research for table creation.
---
# Instructions

## Primary Objective
Systematically research academic benchmarks, datasets, or research papers to extract and compile comparative information (e.g., into a summary table). The core workflow involves: 1) Identifying relevant sources, 2) Extracting key metadata, 3) Synthesizing findings into a structured output (like a LaTeX table).

## Core Workflow
1.  **Clarify & Parse Request:** Identify the specific benchmarks/datasets/papers mentioned by the user. Note any required output format (e.g., LaTeX table with specific columns) and constraints (e.g., "no commented lines").
2.  **Initial Information Gathering:** For each identified entity (dataset/paper):
    *   Use `local-web_search` to find general information, official pages (GitHub, project sites), and relevant arXiv IDs.
    *   For arXiv papers, use `arxiv_local-download_paper` or `fetch-fetch_markdown` to obtain the paper content.
    *   Search for specific attributes requested by the user (e.g., "number of tasks," "training set," "difficulty levels").
3.  **Deep Dive & Verification:** Read paper abstracts, introductions, and methodology sections (using `arxiv_local-read_paper` or parsed markdown) to confirm key details. Cross-reference information from multiple sources (official site, paper, blog posts) for accuracy.
4.  **Information Synthesis:** Compile the extracted metadata into a structured format aligned with the user's request. Resolve any ambiguities (e.g., if a "task" count refers to broad categories or individual instances) based on the most authoritative source (typically the original paper).
5.  **Output Generation:** Create the final deliverable (e.g., a `.tex` file). Ensure it strictly adheres to the user's formatting specifications. Optionally, provide a concise textual summary of the findings.

## Key Metadata to Extract
When researching a benchmark/dataset, prioritize finding:
*   **Full Name & Acronym**
*   **Number of Tasks/Categories:** Distinguish between broad task categories and individual task instances.
*   **Training Data Availability:** Does it include a dedicated training set, or is it for evaluation only?
*   **Difficulty Levels:** Does it feature adjustable or tiered difficulty levels?
*   **Core Purpose/Description**
*   **Primary Source (arXiv ID, GitHub repo)**

## Tool Usage Guidelines
*   `local-web_search`: Use for initial discovery and finding high-level descriptions. Employ specific queries combining the dataset name and target attributes (e.g., "BBH training set few-shot examples").
*   `arxiv_local-download_paper` / `fetch-fetch_markdown`: Use to access the canonical source for detailed information. Prefer `arxiv_local-download_paper` for full text analysis when needed.
*   `filesystem-write_file` / `filesystem-read_file`: Use for creating and verifying final output files in the workspace.
*   `local-claim_done`: Use only after successfully delivering the requested output and providing a final summary.

## Output Standards
*   **LaTeX Tables:** Ensure the output contains only the specified table content, without extra comments, document headers, or unrelated text.
*   **Summaries:** Be concise but complete, highlighting the sourced information for each dataset.
*   **Accuracy:** Base conclusions on the original paper or official project documentation where possible. Acknowledge if information is not explicitly stated.

## Common Pitfalls & Resolutions
*   **Ambiguous Task Counts:** If a paper mentions "5 task categories" (like KOR-Bench), report that as the task count unless the user specifies otherwise. Clarify in the summary if needed.
*   **Missing Information:** If a key attribute (e.g., training set) is not mentioned in primary sources, infer based on benchmark type (e.g., many evaluation benchmarks lack training sets) and denote with `\ding{55}`. State the assumption in your summary.
*   **arXiv Paper Processing:** If `arxiv_local-download_paper` returns a "converting" status, use `fetch-fetch_markdown` on the arXiv abstract page as a reliable fallback to get the paper's metadata and abstract.
