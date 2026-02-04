---
name: policy-document-parser
description: Extracts and structures company policy information from PDF documents, particularly travel expense policies with destination-specific caps. Reads policy PDFs, extracts structured data about expense limits by location and employee level, and converts policy tables into machine-readable formats for automated validation.
---
# Policy Document Parser

## When to Use
Use this skill when you need to:
- Analyze company policy documents (PDF format)
- Extract structured expense limits from travel policy tables
- Parse destination-specific caps by employee level
- Convert policy tables into machine-readable formats (JSON/CSV)
- Prepare policy data for automated expense validation systems

## Core Workflow

### 1. Initial Setup & Document Discovery
- Scan the workspace for policy documents (typically PDF files)
- Identify the main policy document (look for files like `policy_en.pdf`, `travel_policy.pdf`, etc.)
- Use `filesystem-list_directory` to explore the workspace structure

### 2. Policy Document Analysis
- Read the PDF document using `pdf-tools-read_pdf_pages`
- Extract the full text content for analysis
- Identify the document structure and locate policy tables

### 3. Table Extraction & Parsing
- Focus on sections containing destination-specific expense caps
- Look for tables with the following structure:
  - Destination cities/countries
  - Employee levels (L1, L2, L3, L4, etc.)
  - Category caps (Accommodation, Meals, Transportation, Communication, Miscellaneous)
  - Per-day or per-trip limits

### 4. Data Structuring
- Convert extracted tables into structured JSON format
- Organize data by: `city → employee_level → category → limit`
- Include global rules (receipt thresholds, airfare policies, etc.) as separate metadata

### 5. Output Generation
- Create machine-readable policy files (JSON preferred)
- Generate summary reports of extracted policy limits
- Prepare data for integration with expense validation systems

## Key Patterns from Trajectory

### Document Structure Recognition
The policy PDF typically contains:
1. Header with policy name, effective date, currency
2. Global rules section (airfare, receipt thresholds, exceptions)
3. Destination-specific tables with caps by employee level
4. Multiple pages with consistent table formatting

### Data Extraction Strategy
- Extract all pages first to understand full document scope
- Look for patterns like "Destination-Specific Caps" headers
- Parse tables with city names followed by level-based caps
- Capture per-day vs per-trip limits (Transportation vs Communication/Miscellaneous)

### Error Handling
- Handle missing or malformed tables gracefully
- Validate extracted data against expected structure
- Log parsing issues for manual review

## Output Formats

### Primary Output: Structured Policy JSON
