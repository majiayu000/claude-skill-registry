---
name: pdf-metadata-extractor
description: Extracts specific metadata from PDF documents, particularly academic papers, including author information, affiliations, and institutional details. This skill is triggered by requests involving PDF analysis, academic paper processing, or when precise information extraction from document headers/footers is required. It handles PDF parsing, text extraction from specific pages, and structured data retrieval from academic document formats.
---
# Instructions for PDF Metadata Extraction

## Primary Use Case
This skill is designed to systematically extract first author metadata from academic papers in PDF format. The core workflow involves:
1.  Locating and reading an Excel file containing a list of paper titles.
2.  Searching for and downloading the corresponding PDFs.
3.  Parsing the first pages of the PDFs to extract the first author's full name and their complete institutional affiliation.
4.  Searching for the author's Google Scholar profile.
5.  Writing all extracted data back to the original Excel file.

## Core Workflow

### 1. Locate and Inspect the Target Excel File
- Use the `terminal-run_command` tool to find `.xlsx` or `.xls` files within the `/workspace/dumps/workspace` directory.
- **Security Note:** Do not use file paths outside the allowed directory (e.g., `/dev/null`).
- Use `excel-get_workbook_metadata` to inspect the file's structure (sheet names, used ranges).
- Use `excel-read_data_from_excel` to read the paper titles from the first column (typically starting at cell A2).

### 2. Search for and Acquire Paper PDFs
- For each paper title, perform a web search using `local-web_search` to find the PDF. Common sources include:
    - OpenReview (`openreview.net/pdf?id=`)
    - arXiv (`arxiv.org/pdf/`)
    - Conference proceedings (e.g., `proceedings.mlr.press`).
- Prioritize direct PDF links. If a direct link is not found in search results, look for a paper page (e.g., OpenReview forum) and construct the PDF URL (often by appending `/pdf` to the page URL).

### 3. Extract Metadata from PDFs
- Use `pdf-tools-read_pdf_pages` to read the **first 1-2 pages** of each acquired PDF. This is where author and affiliation information is almost always located.
- **Parsing Strategy:**
    - **First Author Name:** Identify the first listed author in the author block, typically following the title and preceding the abstract. Extract their full name as it appears (e.g., "Aaditya K. Singh", "Amber Yijia Zheng*").
    - **Affiliation:** Extract the complete affiliation string associated with the first author. This often includes the department, university/institution, and sometimes city/country. Capture it exactly as printed, including all listed institutions if multiple are present (e.g., "Gatsby Computational Neuroscience Unit, University College London", "ENSAE, CREST, IP Paris").

### 4. Find Google Scholar Profiles
- For each extracted first author, perform a targeted web search using `local-web_search` with the query format: `"<First Author Full Name>" Google Scholar profile`.
- Extract the direct URL to their Google Scholar citations page from the search results (e.g., `https://scholar.google.com/citations?user=...`).
- If the primary search fails, try a more specific query including their institution (e.g., `"Aaditya K. Singh" University College London Google Scholar`).

### 5. Compile and Write Results
- Structure the extracted data (First Author, Affiliation, Google Scholar URL) into a list of lists, maintaining the same order as the input paper titles.
- Use `excel-write_data_to_excel` to write this data back to the original Excel file. The data should start in column B, row 2 (next to the paper titles).
- Use `excel-read_data_from_excel` to verify the data was written correctly.
- Finally, present a summary table to the user and call `local-claim_done`.

## Error Handling & Assumptions
- **Missing PDFs:** If a PDF cannot be found after a reasonable search, note this and proceed with the next paper. Inform the user.
- **Unclear Author Block:** If the first page parsing does not yield clear author/affiliation data, consider checking the second page or the very end of the PDF (footer).
- **Multiple "First Authors":** Some papers denote joint first authorship with asterisks (*). Extract the first name in the list that is marked as such or the very first name if no markers are present.
- **Affiliation Formatting:** Preserve line breaks, commas, and institutional hierarchies as they appear in the PDF. Do not simplify.

## Key Tools Used
- `terminal-run_command`: File system navigation.
- `excel-get_workbook_metadata` / `excel-read_data_from_excel` / `excel-write_data_to_excel`: Excel I/O.
- `local-web_search`: Finding papers and scholar profiles.
- `pdf-tools-read_pdf_pages`: Core PDF text extraction.
- `local-claim_done`: Signal task completion.
