---
name: diff-analysis
description: |
  Methodology for categorizing changes, assessing risks, and creating summaries
  from any changeset.

  Triggers: diff analysis, changeset review, risk assessment, change categorization,
  semantic analysis, release preparation, change summary, git diff

  Use when: analyzing specific changesets, assessing risk of changes, preparing
  release notes, categorizing changes by type and impact

  DO NOT use when: quick context catchup - use catchup instead.
  DO NOT use when: full PR review - use review-core with pensive skills.

  Use this skill for systematic change analysis with risk scoring.
category: analysis-methods
tags: [changes, semantic-analysis, risk-assessment, categorization, summaries]
dependencies: [imbue:evidence-logging]
tools: [git, diff-tools]
usage_patterns:
  - change-analysis
  - risk-assessment
  - release-preparation
complexity: intermediate
progressive_loading: true
module_strategy: workflow-based
estimated_tokens: 800
---

# Diff Analysis Methodology

## Overview

Structured method for analyzing changesets: categorize changes, assess risks, generate insights. Works for git diffs, configuration changes, API migrations, schema updates, or document revisions.

## When to Use
- Extracting insights from raw change data
- Categorizing and prioritizing changes before code reviews
- Preparing release notes or changelogs
- Assessing migration scope and risk

## Activation Patterns
**Trigger Keywords**: diff, changes, release notes, changelog, migration, impact, risk assessment

**Auto-Load When**: Git diffs present, change analysis requested, impact assessment needed.

## Progressive Loading

Load modules based on workflow stage:

### Always Load
- `modules/semantic-categorization.md` for change categorization workflow

### Conditional Loading
- `modules/risk-assessment-framework.md` when risk assessment is needed
- `modules/git-diff-patterns.md` when working with git repositories

### Integration
- Use `sanctum:git-workspace-review` for git data gathering
- Use `imbue:evidence-logging` for capturing analysis evidence
- Use `imbue:structured-output` for formatting final deliverables

## Required TodoWrite Items
1. `diff-analysis:baseline-established`
2. `diff-analysis:changes-categorized`
3. `diff-analysis:risks-assessed`
4. `diff-analysis:summary-prepared`

Mark each item complete as you finish the corresponding step.

## 4-Step Methodology

### Step 1: Establish Baseline (`diff-analysis:baseline-established`)
Define comparison scope: what states are being compared, boundary of analysis, and scale metrics.

For git contexts, load `modules/git-diff-patterns.md`. For other contexts, compare relevant artifacts.

### Step 2: Categorize Changes (`diff-analysis:changes-categorized`)
Group changes by semantic type. Load `modules/semantic-categorization.md` for change categories, semantic categories, and prioritization.

### Step 3: Assess Risks (`diff-analysis:risks-assessed`)
Evaluate impact. Load `modules/risk-assessment-framework.md` for risk indicators, levels, and scoring methodology.

### Step 4: Prepare Summary (`diff-analysis:summary-prepared`)
Synthesize findings: theme, scope with counts, risk level, review focus, dependencies. Format for downstream consumption (PR descriptions, release notes, reviews).

## Exit Criteria
- All TodoWrite items completed with categorized changes and risk assessment
- Downstream workflows have semantic understanding of the changeset
- Summary ready for appropriate consumption (review, release notes, planning)
