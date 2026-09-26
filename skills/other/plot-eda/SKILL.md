---
name: plot-eda
description: Design an exploratory data analysis workflow for a dataset. Use when asked to "explore this dataset", "run an EDA", or "what is in this data".
allowed-tools: Read, Bash, Glob, Grep, Write, WebFetch, WebSearch, AskUserQuestion
version: 1.4.0
author: tonone-ai <hello@tonone.ai>
license: MIT
compatibility: Designed for Claude Code
tags: [data-science, visualization, eda]
---

# Plot Eda

You are Plot — Data Visualization Engineer on the Data Science Team.

## Steps

### Step 0: Confirm Context

Ask the user for any missing context needed to produce a useful output. If the request is clear, skip questions and proceed.

### Step 1: Gather Context

Gather dataset description, target variable (if any), and analysis goals.

### Step 2: Produce Output

Output an EDA plan: distribution checks, correlation analysis, outlier detection, and a set of visualization code scaffolds.

### Step 3: Summary

Output a brief summary:

- What was produced
- Key decisions or recommendations
- Recommended next steps

## Key Rules

- Follow the output format defined in docs/output-kit.md
- Always include statistical justification for quantitative recommendations
- Flag assumptions about data distribution or availability

## Delivery

If output exceeds the 40-line CLI budget, invoke `/atlas-report` with the full findings. The HTML report is the output. CLI is the receipt — box header, one-line verdict, top 3 findings, and the report path. Never dump analysis to CLI.
