---
name: academic-bibtex-manager
description: When the user requests to add academic papers to a BibTeX bibliography file while maintaining format consistency and sourcing from appropriate repositories. This skill handles 1) Reading existing BibTeX files to understand formatting conventions, 2) Searching for academic papers across multiple sources (OpenReview for conference papers, arXiv for preprints), 3) Extracting proper BibTeX metadata from conference pages or arXiv entries, 4) Determining appropriate citation format (@article vs @inproceedings) based on publication venue, 5) Appending new entries while preserving existing file structure and formatting. Triggers include requests to 'add to ref.bib', 'update bibliography', 'cite papers', or when working with academic reference files.
---
# Instructions

## Primary Objective
Add requested academic paper entries to a specified BibTeX (.bib) file. Ensure entries are correctly formatted, sourced from authoritative repositories (OpenReview for conferences, arXiv for preprints), and consistent with the existing file's style.

## Core Workflow

### 1. Parse User Request & Identify Target File
- Extract the list of paper titles/identifiers from the user's request.
- Identify the target `.bib` file path (commonly `ref.bib` or specified by the user).
- **First Action:** Always read the existing file (`filesystem-read_file`) to understand its structure, formatting conventions (indentation, line breaks, entry ordering), and to avoid duplicate entries.

### 2. Research & Source BibTeX Data
For each requested paper:
- **Search Strategy:** Use `local-web_search` with queries combining the paper title and key terms like "openreview" or "arxiv".
- **Source Determination:**
    - **Conference Papers:** If the paper appears in search results from `openreview.net`, it is likely a peer-reviewed conference paper (e.g., ICLR, NeurIPS). Fetch the HTML page (`fetch-fetch_html`) to extract the official BibTeX entry from the page's metadata or BibTeX modal.
    - **Preprints/Technical Reports:** If the primary source is `arxiv.org`, it is an arXiv preprint. Fetch the page (`fetch-fetch_markdown` or `fetch-fetch_html`) to obtain authors, title, year, and arXiv ID.
- **Format Selection:** Use `@inproceedings{...}` for confirmed conference papers. Use `@article{...}` for arXiv preprints, reports, or journal articles. Match the citation key style (e.g., `authorYYYYkeyword`) observed in the existing file.

### 3. Construct & Validate New Entries
- **Conference Entries:** Use the exact BibTeX provided by OpenReview. Verify it includes `booktitle`, `year`, and `url` fields.
- **arXiv Entries:** Construct an `@article` entry with fields: `title`, `author`, `journal={arXiv preprint arXiv:XXXX.XXXXX}`, `year`. Ensure author lists are formatted consistently (e.g., "Last, First and Last, First").
- **Check for Duplicates:** Before writing, scan the newly read file content to ensure the paper (by title or likely citation key) isn't already present.

### 4. Write to File
- Use `filesystem-edit_file` to append the new BibTeX entries to the end of the existing file.
- **Formatting:** Insert a blank line before the new block of entries. Maintain the existing file's indentation style (spaces vs. tabs). Ensure each entry ends with a newline.
- **Order:** Add entries in the order they were requested.

### 5. Final Verification & Summary
- Read the tail of the updated file (`filesystem-read_file` with `tail` parameter) to confirm successful addition.
- Provide the user with a concise summary listing each added paper, its citation key, source (arXiv/Conference), and the format used (`@article`/`@inproceedings`).

## Key Decision Rules
- **arXiv vs. Conference:** A paper listed on OpenReview with a conference title (e.g., "ICLR 2024") is a conference paper. A paper only found on arXiv or described as a "technical report" is an `@article`.
- **BibTeX Source Priority:** 1) Official BibTeX from OpenReview page, 2) Constructed entry from arXiv metadata, 3) Fallback to manual construction from search results if needed.
- **File Safety:** Never overwrite the entire file. Always use `edit_file` to append at a specific, safe location (e.g., before the end of the file).

## Common Triggers & User Phrases
- "Please help me add the following article to the ref.bib file..."
- "Update the bibliography with these papers..."
- "Cite these papers in the .bib file..."
- "Add these references, keep the format consistent."

## Error Handling
- **Missing Paper:** If a paper cannot be found via search, inform the user and ask for clarification (e.g., a DOI, arXiv ID, or full author list).
- **File Not Found:** If the target `.bib` file does not exist, ask the user for confirmation before creating a new one.
- **Parsing Error:** If fetched HTML lacks clear BibTeX, proceed to construct a minimal, correct entry from available metadata and note the limitation to the user.
