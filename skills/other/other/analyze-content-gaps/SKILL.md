---
name: analyze-content-gaps
description: Identify content gaps and organizational opportunities. Analyzes missing content areas, redundancies, and consolidation opportunities.
required_roles:
  scribe: roles/scribe.viewer
personas: [information-architect, content-strategist, product-manager]
---

# Analyze Content Gaps Skill

Identify missing, redundant, or underperforming content within a documentation set. This skill compares existing content against user needs and competitive benchmarks to find opportunities for improvement.

## Inputs

- `PATH` - The content documentation to analyze (e.g., "/documentation")
- `USER_NEEDS` - (Optional) Boolean, whether to map against user search queries or support tickets (default: true)
- `COMPETITIVE_ANALYSIS` - (Optional) Boolean, whether to compare against industry standards or competitors (default: false)

## Workflow

### Step 1: Baseline Assessment

Map the current state of content at `PATH`.
- What topics are covered?
- What is the depth of coverage?

### Step 2: Needs Analysis

Determine what *should* be covered.
- **User Needs**: Analyze search logs, support tickets, or user stories (if `USER_NEEDS` is true).
- **Standards**: Compare against standard frameworks or requirements.
- **Competitors**: Compare against competitor documentation (if `COMPETITIVE_ANALYSIS` is true).

### Step 3: Gap Identification

Compare Baseline vs. Needs.
- **Missing**: Topics required but not present.
- **Thin**: Topics present but lacking detail.
- **Redundant**: Multiple pages covering the same topic unnecessarily.
- **Outdated**: Content that no longer matches current needs.

### Step 4: Strategic Recommendations

Prioritize gaps based on impact and effort.

## Required Outputs

A `GAP_ANALYSIS_REPORT` in markdown format containing:
- **Missing Topics**: List of high-priority new content to create.
- **Improvement Areas**: List of existing content needing expansion.
- **Consolidation Targets**: List of redundant content to merge.
- **Strategic Roadmap**: Recommended order of execution.

## Quick Reference

- **Purpose**: Align content with user needs and business goals.
- **Outcome**: Actionable content strategy roadmap.
