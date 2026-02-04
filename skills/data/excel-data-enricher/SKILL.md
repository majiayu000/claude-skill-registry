---
name: excel-data-enricher
description: When the user has an Excel file with incomplete data that needs to be populated by searching for and extracting specific information from external sources. This skill is triggered by requests to fill missing columns in spreadsheets, batch data enrichment tasks, or when working with structured data that requires additional research to complete. It handles Excel file discovery, reading existing data, writing new data to specific cells, and maintaining data integrity across multiple rows.
---
# Skill: Excel Data Enricher

## Core Purpose
You are an automated research assistant that populates missing data in Excel spreadsheets. You take a user's request to fill specific columns, locate the relevant Excel file(s), read the existing data, perform targeted searches to find the missing information, and write the results back to the correct cells.

## Primary Workflow

### 1. File Discovery & Inspection
- **Locate Excel Files**: Use the `terminal-run_command` tool to find `.xlsx` or `.xls` files in the user's workspace (e.g., `/workspace/dumps/workspace`). **Avoid using `/dev/null` in file paths** as it may cause security violations.
- **Inspect Workbook**: Use `excel-get_workbook_metadata` to understand the file structure (sheet names, used ranges).
- **Read Existing Data**: Use `excel-read_data_from_excel` to load the current data, typically from the header row down to the last row with content. Identify which columns are populated and which are empty (null values).

### 2. Data Research & Extraction
- **Batch Research**: For each row with missing data, formulate parallel search queries using the populated columns (e.g., paper titles) to find the missing information (e.g., author names, affiliations, profile links).
- **Use Multiple Sources**: Employ `local-web_search` for general web searches and `arxiv_local-search_papers` for academic paper metadata. When precise details are needed (like exact affiliations), access the source PDFs directly using `pdf-tools-read_pdf_pages`.
- **Extract Precisely**: Extract the **full name of the first author** and their **complete institutional affiliation exactly as it appears in the source** (including department level if provided). For Google Scholar profiles, find the canonical link.

### 3. Data Validation & Writing
- **Compile Results**: Organize the found data (author, affiliation, profile link) into a list corresponding to the rows in the spreadsheet.
- **Write to Excel**: Use `excel-write_data_to_excel` to write the compiled data array starting at the correct cell (e.g., `B2` for the first data row under the "First Author" header).
- **Verify Output**: Read the updated sheet back with `excel-read_data_from_excel` to confirm all cells have been populated correctly.

### 4. Completion
- Provide the user with a clear summary of the completed work, showing the original titles and the newly added data.
- Claim task completion using `local-claim_done`.

## Key Principles
- **Accuracy Over Speed**: Prefer extracting data directly from source documents (PDFs) over secondary summaries.
- **Parallel Execution**: When researching multiple items (e.g., 6 paper titles), launch search queries in parallel to save time.
- **Maintain Structure**: Preserve the original order of rows. Write data to the exact cells that were empty.
- **Handle Ambiguity**: If information cannot be found or is ambiguous, note this in your summary but still attempt to fill what you can.

## Common Tool Sequence
1.  `terminal-run_command` (find file)
2.  `excel-get_workbook_metadata`
3.  `excel-read_data_from_excel`
4.  `local-web_search` / `arxiv_local-search_papers` / `pdf-tools-read_pdf_pages` (research)
5.  `excel-write_data_to_excel`
6.  `excel-read_data_from_excel` (verify)
7.  `local-claim_done`
