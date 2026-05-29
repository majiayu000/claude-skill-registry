---
name: finding-duplicate-functions
description: Use when auditing a codebase for semantic duplication - functions that do the same thing but have different names or implementations. Especially useful for LLM-generated codebases where new functions are often created rather than reusing existing ones.
---

# Finding Duplicate-Intent Functions

## Overview

LLM-generated codebases accumulate semantic duplicates: functions that serve the same purpose but were implemented independently. Classical copy-paste detectors (jscpd) find syntactic duplicates but miss "same intent, different implementation."

This skill uses a two-phase approach: classical extraction followed by LLM-powered intent clustering.

## When to Use

- Codebase has grown organically with multiple contributors (human or LLM)
- You suspect utility functions have been reimplemented multiple times
- Before major refactoring to identify consolidation opportunities
- After jscpd has been run and syntactic duplicates are already handled

## Quick Reference

| Phase | Tool | Model | Output |
|-------|------|-------|--------|
| 1. Extract | `scripts/extract-functions.sh` | - | `catalog.json` |
| 2. Categorize | `scripts/categorize-prompt.md` | haiku | `categorized.json` |
| 3. Split | `scripts/prepare-category-analysis.sh` | - | `categories/*.json` |
| 4. Detect | `scripts/find-duplicates-prompt.md` | opus | `duplicates/*.json` |
| 5. Report | `scripts/generate-report.sh` | - | `report.md` |

## Process

```dot
digraph duplicate_detection {
  rankdir=TB;
  node [shape=box];

  extract [label="1. Extract function catalog\n./scripts/extract-functions.sh"];
  categorize [label="2. Categorize by domain\n(haiku subagent)"];
  split [label="3. Split into categories\n./scripts/prepare-category-analysis.sh"];
  detect [label="4. Find duplicates per category\n(opus subagent per category)"];
  report [label="5. Generate report\n./scripts/generate-report.sh"];
  review [label="6. Human review & consolidate"];

  extract -> categorize -> split -> detect -> report -> review;
}
```

### Phase 1: Extract Function Catalog

```bash
./scripts/extract-functions.sh src/ -o catalog.json
```

Options:
- `-o FILE`: Output file (default: stdout)
- `-c N`: Lines of context to capture (default: 15)
- `-t GLOB`: File types (default: `*.ts,*.tsx,*.js,*.jsx`)
- `--include-tests`: Include test files (excluded by default)

Test files (`*.test.*`, `*.spec.*`, `__tests__/**`) are excluded by default since test utilities are less likely to be consolidation candidates.

### Phase 2: Categorize by Domain

Dispatch a **haiku** subagent using the prompt in `scripts/categorize-prompt.md`.

Insert the contents of `catalog.json` where indicated in the prompt template. Save output as `categorized.json`.

### Phase 3: Split into Categories

```bash
./scripts/prepare-category-analysis.sh categorized.json ./categories
```

Creates one JSON file per category. Only categories with 3+ functions are worth analyzing.

### Phase 4: Find Duplicates (Per Category)

For each category file in `./categories/`, dispatch an **opus** subagent using the prompt in `scripts/find-duplicates-prompt.md`.

Save each output as `./duplicates/{category}.json`.

### Phase 5: Generate Report

```bash
./scripts/generate-report.sh ./duplicates ./duplicates-report.md
```

Produces a prioritized markdown report grouped by confidence level.

### Phase 6: Human Review

Review the report. For HIGH confidence duplicates:
1. Verify the recommended survivor has tests
2. Update callers to use the survivor
3. Delete the duplicates
4. Run tests

## High-Risk Duplicate Zones

Focus extraction on these areas first - they accumulate duplicates fastest:

| Zone | Common Duplicates |
|------|-------------------|
| `utils/`, `helpers/`, `lib/` | General utilities reimplemented |
| Validation code | Same checks written multiple ways |
| Error formatting | Error-to-string conversions |
| Path manipulation | Joining, resolving, normalizing paths |
| String formatting | Case conversion, truncation, escaping |
| Date formatting | Same formats implemented repeatedly |
| API response shaping | Similar transformations for different endpoints |

## Common Mistakes

**Extracting too much**: Focus on exported functions and public methods. Internal helpers are less likely to be duplicated across files.

**Skipping the categorization step**: Going straight to duplicate detection on the full catalog produces noise. Categories focus the comparison.

**Using haiku for duplicate detection**: Haiku is cost-effective for categorization but misses subtle semantic duplicates. Use Opus for the actual duplicate analysis.

**Consolidating without tests**: Before deleting duplicates, ensure the survivor has tests covering all use cases of the deleted functions.

## How to use this skill

Refer to the instructions above or standard agent usage for this skill type.
