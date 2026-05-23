---
name: UXR Report Analyzer
description: Analyzes UXR report PDFs and generates structured analysis documents with key findings, recommendations, and strategic connections. Use when given a UXR report to analyze.
version: 1.0.0
allowed-tools: [Read, Write, Bash]
---

## Overview
This Skill takes a User Experience Research (UXR) report in PDF format, extracts and analyzes its content, and generates a comprehensive structured analysis document. The analysis follows a consistent framework designed for strategic planning and cross-research synthesis, with sections covering metadata, big picture insights, key findings, metrics, recommendations, and connections to related research.

## When to Apply
Use this Skill when:
- User provides a UXR report PDF that needs analysis
- User requests analysis of research documents for strategic planning
- User asks to process reports in the "Reports to Review" folder
- A new research document needs to be catalogued and summarized

Do NOT use this Skill when:
- User wants to read an existing analysis (just use Read tool)
- User is asking general questions about research (use existing analyses)
- Report is not a UXR/research document

## Inputs
- **PDF Report Path**: Absolute path to the UXR report PDF file
- **Original URL**: URL of the source document (will prompt user if not provided)
- **Project Context**: Information about HubSpot's Overall Data Strategy and strategic objectives (available in project resources)

## Outputs
- Structured markdown analysis file saved to `~/Projects/writing/resources/UXR Reports/Analysis/`
- Filename format: `[Report_Name]_Analysis_[MM-YYYY].md`
- HTML comment summary at top for quick reference
- Original PDF moved to `Reviewed Reports/` folder after analysis

## Instructions for Claude

### 1. Initial Setup and Information Gathering
1. Use `mcp__prometheus__prometheus_info` to assess the PDF structure and complexity
2. Ask user for the original URL of the report using AskUserQuestion tool:
   - Question: "What is the URL of the original research report?"
   - Header: "Source URL"
   - Provide option to skip if URL doesn't exist
3. Determine current month and year for filename (format: MM-YYYY)

### 2. Extract Report Content
1. Use `mcp__prometheus__prometheus_extract_text` with appropriate settings:
   - `max_tokens_per_chunk`: 8000 (adjust based on prometheus_info recommendations)
   - `include_page_numbers`: true
   - `clean_text`: true
2. If report is very large (>50 pages), consider using `prometheus_split` first
3. Review all extracted chunks to understand full report scope

### 3. Analyze Report Using Master Framework
Read the project context from `~/Projects/writing/resources/CLAUDE.md` to understand HubSpot's Overall Data Strategy and strategic objectives.

Apply deep analysis to identify:
- **Core research questions and methodology**
- **Key findings that challenge assumptions or reveal gaps**
- **Quantitative metrics and data points (specific numbers, percentages, correlations)**
- **Customer pain points and unmet needs**
- **Strategic implications for product/business strategy**
- **Connections to other research in the catalog**
- **Contradictions with existing research**

### 4. Structure the Analysis Document
Use the template in `resources/ANALYSIS_TEMPLATE.md` to create a comprehensive analysis with these sections:

#### HTML Comment Summary (Lines 1-9)
```markdown
<!-- SUMMARY
Title: [Report Title]
Type: [Research Type - e.g., Qualitative UXR Study, Market Analysis, JTBD Framework]
Key Themes: [3-5 core themes, comma-separated]
Core Insights: [2-3 sentences capturing the most critical findings]
Relevance: [How this connects to strategic objectives - SO1-SO5]
Quality: [Assessment: High/Medium/Low - methodology rigor, sample size, actionability]
Last Reviewed: [YYYY-MM-DD]
-->
```

#### Main Document Structure
1. **Title**: `# [Report Name] Analysis`

2. **Metadata**
   - Study Name
   - Created By (researchers/team)
   - Study URL (from user input or "URL not available")

3. **The Big Picture**
   - 2-3 paragraph summary of findings
   - Explicit connection to HubSpot Overall Data Strategy
   - How findings align with or challenge current strategic direction

4. **Key Findings**
   - Itemized list with descriptive headers
   - Each finding includes quick description
   - Group related findings under themes when appropriate

5. **Interesting Metrics** (if applicable)
   - Bullet list of critical data points
   - Format: "X% of Y do Z" or "Metric shows correlation with outcome"
   - Only include if highly significant numbers surface in research

6. **Recommendations**
   - Split into "Strategic Initiatives" and "Tactical Actions"
   - Each recommendation should be actionable and specific
   - Connect to findings explicitly

7. **Connected Research**
   - List 3-5 related studies from the catalog
   - For each: title, brief description of connection
   - Use actual research from `~/Projects/writing/resources/UXR Reports/Analysis/claude.md`

8. **Disconnected Research** (if applicable)
   - Highlight contradictions or challenges aligning with previous research
   - Explain the nature of the contradiction
   - Only include if genuine conflicts exist

9. **Slide/Section Index**
   - Create searchable index of major sections/slides
   - Format: "Slide X: [Key concept]" or "Section: [Key concept]"

### 5. Quality Standards
- **Be Specific**: Use exact numbers, percentages, quotes from the research
- **Be Strategic**: Connect every insight to business implications
- **Be Honest**: Note research limitations, sample size issues, methodology gaps
- **Be Connected**: Reference other research; build knowledge graph
- **Use Clear Language**: Avoid jargon; explain frameworks simply
- **Quote Customers**: When research includes customer quotes, use them to add authenticity

### 6. Save Analysis and Move Original PDF

**Step 1: Generate filename**
- Format: `[Report_Name]_Analysis_[MM-YYYY].md`
- Remove special characters, use underscores
- Include current month-year (e.g., `11-2025`)

**Step 2: Save analysis file**
- Location: `~/Projects/writing/resources/UXR Reports/Analysis/`
- Use Write tool to create the analysis markdown file

**Step 3: Move original PDF to archive**
After successfully creating the analysis, move the original PDF:
- Source: `~/Projects/writing/resources/UXR Reports/Reports to Review/[original_filename].pdf`
- Destination: `~/Projects/writing/resources/UXR Reports/Reviewed Reports/[original_filename].pdf`
- Use Bash tool with `mv` command:
  ```bash
  mv "~/Projects/writing/resources/UXR Reports/Reports to Review/[original_filename].pdf" "~/Projects/writing/resources/UXR Reports/Reviewed Reports/[original_filename].pdf"
  ```
- Confirm the move was successful before proceeding
- Report to user: "Original PDF moved to Reviewed Reports folder"

### 7. Update Catalog
After creating analysis:
1. Add entry to `~/Projects/writing/resources/UXR Reports/Analysis/claude.md`
2. Include in appropriate category
3. Update resource count and statistics

## Reference Materials
- **Analysis Template**: See `resources/ANALYSIS_TEMPLATE.md` for detailed section structure
- **Example Analysis**: See `resources/EXAMPLE_ANALYSIS.md` for a reference implementation
- **UXR Catalog**: `~/Projects/writing/resources/UXR Reports/Analysis/claude.md`
- **Project Context**: `~/Projects/writing/resources/CLAUDE.md`
- **Strategic Objectives**: `~/Projects/writing/resources/2026 S7/claude.md`

## Examples

### Example 1: Basic Usage
**User Input**:
```
Analyze this report: ~/Projects/writing/resources/UXR Reports/Reports to Review/Admin_Journey_Research.pdf
```

**Claude Actions**:
1. Use prometheus_info to assess PDF (39 pages, ~4000 tokens)
2. Ask user for original URL via AskUserQuestion
3. Extract text using prometheus_extract_text
4. Read project context and strategic objectives
5. Analyze content, identifying key themes (setup complexity, learning curves, time pressures)
6. Generate analysis file: `Admin_Journey_Research_Analysis_11-2025.md`
7. Save to Analysis folder using Write tool
8. Move original PDF using Bash:
   ```bash
   mv "~/Projects/writing/resources/UXR Reports/Reports to Review/Admin_Journey_Research.pdf" "~/Projects/writing/resources/UXR Reports/Reviewed Reports/Admin_Journey_Research.pdf"
   ```
9. Update catalog in claude.md
10. Report completion to user

### Example 2: Large Report
**User Input**:
```
Process this 150-page report: ~/Projects/writing/resources/UXR Reports/Reports to Review/Comprehensive_Market_Study.pdf
```

**Claude Actions**:
1. Use prometheus_info (150 pages, high complexity)
2. Use prometheus_split with 20 pages per chunk
3. Extract text from each chunk
4. Synthesize across all chunks for comprehensive analysis
5. Generate analysis with extensive section index
6. Save analysis file to Analysis folder
7. Move original PDF to Reviewed Reports folder using Bash mv command
8. Update catalog in claude.md

## Testing Checklist
- [ ] YAML frontmatter includes name (≤64 chars) and description (≤200 chars)
- [ ] Description clearly states when to use ("Use when given a UXR report to analyze")
- [ ] Instructions specify tool usage (Prometheus, AskUserQuestion, Read, Write)
- [ ] Template files exist in resources folder
- [ ] Examples show input → output flow
- [ ] Security consideration: No hardcoded paths that include secrets
- [ ] File handling: Clear instructions for moving PDFs between folders
- [ ] Updates catalog after completion

## Security and Privacy
- **No Secrets**: Never hardcode API keys or credentials
- **Local Files Only**: All operations on local filesystem paths
- **User Consent**: Ask for URL; don't fabricate links
- **Data Handling**: Research reports may contain sensitive customer information; keep analysis files in designated project folders only
- **No External Sharing**: Generated analyses stay within project directory structure

## Notes
- This Skill integrates with existing project organization (see `~/Projects/writing/CLAUDE.md`)
- Follows established UXR report workflow: Reports to Review → Analysis → Reviewed Reports
- Analysis structure designed for strategic planning and cross-research synthesis
- Prometheus MCP tools handle PDF parsing and text extraction
- Generated analyses become reference materials for future writing projects
