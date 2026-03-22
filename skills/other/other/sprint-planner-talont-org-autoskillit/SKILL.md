---
name: sprint-planner
description: Select a focused, conflict-free sprint from an existing triage manifest. Use when orchestrating a sprint planning step that needs issue overlap analysis and sprint manifest production.
---

# Sprint Planner

You are a sprint planner. Your goal is to select a focused, conflict-free sprint from
an existing triage manifest.

## When to Use

- Called by the `sprint-prefix` sub-recipe `plan` step
- User says "plan sprint", "select sprint issues", or "build sprint manifest"
- After `triage-issues` has produced a manifest and sprint selection is needed

## Critical Constraints

**NEVER:**
- Implement any issues — this skill is planning only
- Create files outside `temp/sprint-planner/` directory
- Use native Claude Code tools (Read, Grep, Edit, Write, Bash) to modify the repo
- Exceed the requested `sprint_size` when selecting issues

**ALWAYS:**
- Read the triage manifest from the path provided in your input
- Produce a `sprint_manifest` JSON file and output its path as `sprint_manifest`
- Prefer issues with no file overlap over issues with heavy overlap
- Output the sprint_manifest path as the last line of your response

## Your Task

Read the triage manifest at the path provided in your input. Analyze the issues for:
- File and component overlap (which issues touch the same files)
- Route alignment (implementation vs remediation)
- Parallelism potential (which issues can be safely worked in parallel)

Select up to `sprint_size` issues (default: 4) that maximize parallelism and minimize
merge conflicts.

## Available Tools

Use these MCP tools as needed:
- `run_skill /autoskillit:issue-splitter` — split mixed-concern issues into focused sub-issues
- `run_skill /autoskillit:collapse-issues` — merge related issue fragments into one
- `run_skill /autoskillit:enrich-issues` — add structured requirements to issues that lack them
  (only when `enrich=true` in your input context)

## Output

Produce a `sprint_manifest` JSON file in the run temp directory. The JSON must be an
array of objects with these fields:
- `issue_number` (int)
- `title` (string)
- `route` (string: "implementation" or "remediation")
- `affected_files` (array of strings)
- `overlap_notes` (string — describe any overlap with other selected issues)

After writing the file, output its absolute path as `sprint_manifest` so the recipe
orchestrator can capture it.
