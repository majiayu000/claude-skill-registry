---
name: multi-source-web-researcher
description: When the user needs to gather information from multiple sources including web searches, academic databases (arXiv), PDF documents, and professional profiles. This skill is triggered by research tasks requiring parallel information gathering, cross-referencing multiple sources, or when dealing with academic/professional data that exists across different platforms. It handles concurrent searches, source verification, and data consolidation from diverse information repositories.
---
# Multi-Source Web Researcher

## Purpose
This skill orchestrates the systematic collection, verification, and consolidation of information from multiple digital sources to answer research questions, particularly those involving academic or professional data. It is designed to handle tasks where information is distributed across web search results, academic paper repositories (arXiv), PDF documents, and professional profile platforms (Google Scholar, institutional websites).

## Core Workflow

### 1. Initial Setup & Discovery
- **Locate Target Files**: First, identify any local files (like Excel workbooks) that define the research scope or require population. Use terminal commands to find relevant files in the workspace.
- **Understand Data Structure**: Read the metadata and contents of discovered files to understand what information needs to be gathered and the required format.

### 2. Parallel Information Gathering
- **Concurrent Searches**: For efficiency, launch multiple web searches *in parallel* to gather initial leads on each research item (e.g., paper titles, author names).
- **Source Diversification**: Use a combination of:
    - `local-web_search`: For general web results, author profiles, and institutional pages.
    - `arxiv_local-search_papers`: For finding specific academic papers and their metadata on arXiv.
    - `pdf-tools-read_pdf_pages`: To extract precise information (like author affiliations) directly from source PDFs when URLs are known.

### 3. Verification & Deep Dive
- **Cross-reference Findings**: Use information from one source (e.g., a paper title from web search) to find the canonical source (e.g., the PDF on arXiv or OpenReview).
- **Extract Primary Data**: Always prioritize extracting key details (like full author affiliation) directly from the original PDF to ensure accuracy.
- **Profile Discovery**: Search for professional profiles (e.g., Google Scholar) using the verified author name and affiliation.

### 4. Data Consolidation & Output
- **Structure Collected Data**: Compile the verified information into a structured format (e.g., list of lists for an Excel sheet).
- **Write to Target**: Update the original file (e.g., Excel workbook) with the collected data.
- **Final Verification**: Read back the updated file to confirm all data was written correctly and present a summary to the user.

## Key Principles
- **Parallelism is Key**: Use tool calls concurrently whenever possible to minimize total research time.
- **Prioritize Primary Sources**: For academic data, the PDF of the paper is the ground truth for author order and affiliation.
- **Verify Links**: Ensure collected profile URLs are direct links to the author's public profile page.
- **Handle Encoding**: Be prepared to correctly process special characters in names and affiliations (e.g., Clément Bonet).
