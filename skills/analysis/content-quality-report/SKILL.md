---
name: content-quality-report
description: Generate comprehensive content quality report with competitive SERP analysis
argument-hint: [content-path] [target-keyword]
disable-model-invocation: true
---

Generate content quality report: $ARGUMENTS

## Step 1: Parse Arguments

**Format:** First argument = path or identifier for the content to analyze. Second argument = target keyword for SERP competitive analysis.

If no path provided, use available tools to discover recent drafts or content the user might mean, or ask the user to specify.

If no keyword provided, infer from the content's title or H1, or ask the user to provide the target keyword.

## Step 2: Load Content

Use available tools (Read, or search/list tools) to load the content at the given path. If the path doesn't exist or isn't accessible, report clearly and suggest alternatives.

## Step 3: Run Quality Analysis

Perform or delegate a comprehensive content quality analysis:

- Evaluate against standard quality dimensions (readability, structure, citations, depth, etc.)
- If SERP/keyword analysis tools are available, run competitive analysis for the target keyword
- Produce both structured data (e.g. JSON) and a human-readable markdown report

## Step 4: Save Reports

Save the report outputs where the user's environment expects them (e.g. a reports folder, or alongside the content). Use timestamps or versioning so reports are not overwritten. If the environment has no prescribed location, create a sensible one (e.g. `_reports/quality/`) or ask the user.

## Step 5: Present Summary

Present a concise summary to the user:

- Content analyzed and target keyword
- Overall score and dimension breakdown
- Top issues and top strengths
- SERP competitive insights (if available)
- Where reports were saved
- Next steps (address critical issues, add missing topics, re-run after fixes)

## Notes

- Reports should be timestamped/versioned (never overwritten)
- Use whatever tools are available in the environment for SERP or keyword analysis
- All quality dimensions that apply should be evaluated in every report
