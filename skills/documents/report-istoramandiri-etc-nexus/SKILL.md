---
name: report
description: Create structured reports for technical findings, test results, and analysis.
argument-hint: "<topic>"
---

# Report Skill

Create technical reports with Discord-friendly summaries for sharing findings.

## Arguments

- `<topic>`: Brief description of what the report covers (e.g., "CREATE2 collision resolution")

## Output

Reports are saved to `reports/YYMMDD_SLUG.md` where:
- `YYMMDD` is the current date (e.g., 260130 for 2026-01-30)
- `SLUG` is a brief descriptive name in SCREAMING_SNAKE_CASE

## Report Structure

Every report has two parts:

### 1. Discord Summary (top of file)

Wrapped in HTML comment markers for easy copy-paste. Must follow these rules:

**Character Limit:** Maximum 1900 characters (buffer under Discord's 2000 limit)

**Formatting Rules:**
- NO TABLES - Discord doesn't render markdown tables
- Use code blocks for tabular data instead
- Use `**bold**` for emphasis
- Use `### Headings` for sections
- Wrap URLs in angle brackets: `<https://example.com>`

**Required Sections:**
1. Title with key metric
2. Metadata line (client, suite, counts)
3. Brief summary (1-2 sentences)
4. Key findings in code block format
5. Analysis (root cause in 2-3 sentences)
6. Impact assessment
7. Next steps (numbered list)
8. Link to full report

**Template:**

```markdown
<!-- DISCORD SUMMARY (paste everything between the markers) -->
## [Title]: [Key Metric]

**[Context]:** [value] | **[Metric]:** [numbers]

[1-2 sentence summary]

### [Section Name]

```
[Data in code block - NOT a table]
```

### Analysis

**Root cause:** [Brief explanation]

### Impact

**[Severity] for [context]** - [Practical implications]

### Next Steps
1. [Action item]
2. [Action item]

**Full report:** <[URL]>
<!-- END DISCORD SUMMARY -->
```

### 2. Full Report (below the summary)

After a horizontal rule (`---`), include the detailed report:

**Required Sections:**
1. Title and metadata (date, test suite, client version)
2. Executive summary
3. Context (why this report exists)
4. Detailed findings (tables, logs, specifics)
5. Root cause analysis
6. Impact assessment
7. Recommendations (short/medium/long-term)
8. References (links to specs, repos)
9. Appendix (log locations, raw data)

**Formatting:**
- Tables are fine in full report (GitHub renders them)
- Include code blocks for log excerpts
- Link to specific files with `file:line` notation
- Reference external specs with full URLs

## Workflow

1. Gather all relevant data (logs, test results, metrics)
2. Analyze root cause and impact
3. Draft Discord summary first (ensures conciseness)
4. Verify Discord summary is under 1900 characters
5. Write full report with complete details
6. Save to `reports/YYMMDD_SLUG.md`
7. Output the Discord summary for easy copy-paste
