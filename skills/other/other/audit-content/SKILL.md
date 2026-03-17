---
name: audit-content
description: Comprehensive content quality and maintenance assessment. Evaluates documentation quality, relevance, maintenance needs, and provides actionable recommendations.
required_roles:
  scribe: roles/scribe.editor
personas: [information-architect, content-strategist, editor]
---

# Content Audit Skill

Perform a comprehensive quality and maintenance assessment of documentation or content. This skill evaluates content against quality standards, checks for freshness, identifies maintenance needs, and provides actionable recommendations.

## Inputs

- `PATH` - The directory or file path to audit (e.g., "/docs")
- `SEVERITY` - (Optional) Minimum severity level to report: "low", "medium", "high" (default: "medium")
- `CATEGORY` - (Optional) Categories to audit: "all", "quality", "relevance", "links", "metadata" (default: "all")
- `FIX_MODE` - (Optional) Boolean, whether to suggest or apply automated fixes where possible (default: false)

## Workflow

### Step 1: Inventory & Freshness Check

Scan the target `PATH` to list all content assets.
- Check "Last Modified" dates.
- Identify outdated content (e.g., > 6 months old).
- Verify author/owner metadata.

### Step 2: Quality Assessment

Evaluate content against quality metrics:
- **Clarity & Readability**: Is the content easy to understand? (e.g., plain language).
- **Completeness**: Does it cover the topic sufficiently?
- **Accuracy**: Are there broken links, deprecated terms, or incorrect instructions?
- **Structure**: Does it follow standard templates and formatting?

### Step 3: Issues & Recommendations

Generate a report of identified issues, categorized by severity:
- **High**: Broken paths, critical misinformation, missing required sections.
- **Medium**: Outdated styling, poor readability, minor inaccuracies.
- **Low**: Typos, inconsistent formatting.

If `FIX_MODE` is enabled, generate or apply suggestions for fixes.

## Required Outputs

A `CONTENT_AUDIT_REPORT` in markdown format containing:
- **Summary**: Total files, overall quality score, critical issues count.
- **Detailed Findings**: Table of issues per file with severity.
- **Action Items**: Prioritized list of recommended changes.
- **Freshness Report**: List of stale or outdated documents.

## Quick Reference

- **Purpose**: Support content maintenance planning and quality improvement.
- **Key Metrics**: Quality Score (0-100), Freshness (Age in days), Link Health (% valid).
