---
name: map-reduce
description: |
  Orchestration pattern for large-scale processing where work is distributed,
  processed independently, then combined. Map phase splits and processes,
  Reduce phase aggregates results. Use for codebase-wide analysis, bulk
  transformations, or any task where "do X to everything, then summarize."
allowed-tools: |
  bash: ls, cat, grep, find
  file: read, write
  mcp: task
---

# Map-Reduce

<purpose>
Some tasks are too large for single-pass processing: analyze every file in a
codebase, check all endpoints for issues, transform all components to new
pattern. Map-Reduce handles this: split the work (map), process in parallel,
combine results (reduce). It's batch processing for Claude.
</purpose>

## When To Activate

Trigger when:

- Task involves "all files" or "every X"
- Processing a large number of similar items
- Need aggregate statistics or summaries across many items
- Transformation must be applied uniformly
- Analysis must cover entire codebase/dataset

Do NOT trigger for:

- Small number of items (just do them directly)
- Items requiring different processing logic
- When intermediate results affect how later items are processed

## The Pattern

```
                 MAP PHASE                          REDUCE PHASE
              ┌────────────┐
              │ Process A  │──→ Result A ─┐
[All Items]   ├────────────┤              │    ┌─────────────┐
     │        │ Process B  │──→ Result B ─┼──→ │  Aggregate  │──→ [Final]
     │        ├────────────┤              │    └─────────────┘
     └──Split─│ Process C  │──→ Result C ─┘
              ├────────────┤
              │ Process D  │──→ Result D ─┘
              └────────────┘
```

## Instructions

### Step 1: Define the Job

Specify what you're processing:

```
Map-Reduce Job: [Name]

Input: [What collection of items]
Map function: [What to do to each item]
Reduce function: [How to combine results]
Expected output: [What the final result looks like]
```

### Step 2: Enumerate Items (Map Input)

List everything to process:

```
Items to process:
1. [Item 1] - [brief description]
2. [Item 2] - [brief description]
3. [Item 3] - [brief description]
...
Total: [N] items
```

For large sets, use patterns:
```
Items: All files matching src/**/*.ts
Count: ~150 files
Batching: Groups of 10
```

### Step 3: Execute Map Phase

Process each item (parallel when possible):

```
═══════════════════════════════════════
MAP PHASE: Processing [N] items
═══════════════════════════════════════

Batch 1 (items 1-10):
[Processing...]
- Item 1: [Result]
- Item 2: [Result]
...

Batch 2 (items 11-20):
[Processing...]
...

Map phase complete: [N] items processed
- Succeeded: [X]
- Failed: [Y]
- Skipped: [Z]
```

### Step 4: Collect Intermediate Results

Gather all map outputs:

```
Intermediate results:
┌──────────┬─────────────────────────────┐
│ Item     │ Map Result                  │
├──────────┼─────────────────────────────┤
│ Item 1   │ [Result summary]            │
│ Item 2   │ [Result summary]            │
│ ...      │ ...                         │
└──────────┴─────────────────────────────┘
```

### Step 5: Execute Reduce Phase

Aggregate results:

```
═══════════════════════════════════════
REDUCE PHASE: Aggregating results
═══════════════════════════════════════

Reduction strategy: [How combining]

Aggregating...

Categories identified:
- Category A: [N] items
- Category B: [M] items

Statistics:
- Total processed: [X]
- Issues found: [Y]
- Patterns detected: [Z]
```

### Step 6: Produce Final Output

Present combined results:

```
═══════════════════════════════════════
MAP-REDUCE COMPLETE: [Job Name]
═══════════════════════════════════════

## Summary
[High-level findings]

## Statistics
- Items processed: [N]
- [Metric 1]: [Value]
- [Metric 2]: [Value]

## Categories/Groups
[Breakdown by category]

## Notable Items
[Specific items worth highlighting]

## Recommendations
[Actions based on findings]
```

## Batching Strategies

<batching>
**By count:**
```
Items: 150 files
Batch size: 10
Batches: 15
```

**By directory:**
```
Items: All TypeScript files
Batches: src/api/*, src/components/*, src/utils/*
```

**By type:**
```
Items: All source files
Batches: *.ts, *.tsx, *.css
```

**Adaptive:**
```
Start with batch of 20
If too slow → reduce to 10
If fast → increase to 30
```
</batching>

## Reduce Functions

<reduce-functions>
**Count:** Total items matching criteria
**Sum:** Aggregate numeric values
**Group:** Categorize by attribute
**Filter:** Surface items matching condition
**Top-N:** Highest/lowest by metric
**Histogram:** Distribution across buckets
**Merge:** Combine into single artifact
</reduce-functions>

## NEVER

- Process items that depend on other items' results (use pipeline)
- Ignore failed items - always report what couldn't be processed
- Reduce without the map phase (need individual results first)
- Skip batching for large sets (will timeout/overwhelm)
- Assume uniform results - expect variation

## ALWAYS

- Define map and reduce functions before starting
- Batch appropriately for the workload
- Track success/failure per item
- Produce actionable summary, not just raw data
- Include "notable items" - outliers worth attention

## Examples

### Example 1: Security Audit

User: "Check all API endpoints for authentication issues"

```
Map-Reduce Job: API Security Audit

Input: All files in src/api/**/*.ts
Map function: Check each file for auth patterns
Reduce function: Group by issue severity

═══════════════════════════════════════
MAP PHASE: Processing 23 files
═══════════════════════════════════════

- users.ts: [Missing rate limit on /login]
- orders.ts: [No auth on /history endpoint]
- products.ts: [Clean]
- admin.ts: [Deprecated auth method]
...

═══════════════════════════════════════
REDUCE PHASE: Aggregating results
═══════════════════════════════════════

By severity:
- Critical: 2 files (orders.ts, payments.ts)
- Warning: 5 files
- Clean: 16 files

═══════════════════════════════════════
MAP-REDUCE COMPLETE: API Security Audit
═══════════════════════════════════════

Summary: 7 of 23 endpoints have auth issues

Critical (fix immediately):
1. orders.ts:45 - GET /history has no auth check
2. payments.ts:23 - POST /refund missing admin check

Recommendations:
1. Add auth middleware to orders router
2. Implement admin check on payments
```

### Example 2: Codebase Metrics

User: "How complex is our codebase? Get metrics on all files."

```
Map-Reduce Job: Codebase Complexity Analysis

Input: All source files
Map function: Count lines, functions, cyclomatic complexity
Reduce function: Aggregate statistics, find outliers

═══════════════════════════════════════
MAP PHASE: Processing 234 files
═══════════════════════════════════════

[Batched processing of all files...]

═══════════════════════════════════════
REDUCE PHASE: Aggregating results
═══════════════════════════════════════

Totals:
- Lines of code: 45,230
- Functions: 1,847
- Average complexity: 4.2

Distribution:
- Low complexity (<5): 78%
- Medium (5-10): 18%
- High (>10): 4%

═══════════════════════════════════════
MAP-REDUCE COMPLETE
═══════════════════════════════════════

Notable outliers (high complexity):
1. src/utils/parser.ts - complexity 23
2. src/api/legacy/converter.ts - complexity 19

Recommendations:
Consider refactoring top 5 complex files.
```

### Example 3: Bulk Transformation

User: "Convert all class components to functional components"

```
Map-Reduce Job: Class → Functional Conversion

Input: All React component files
Map function: Convert class to functional if applicable
Reduce function: Track conversions, summarize changes

═══════════════════════════════════════
MAP PHASE
═══════════════════════════════════════

- Header.tsx: Converted (was class)
- Button.tsx: Already functional (skipped)
- Modal.tsx: Converted (was class)
- LegacyForm.tsx: Cannot convert (uses getDerivedStateFromProps)
...

═══════════════════════════════════════
REDUCE PHASE
═══════════════════════════════════════

Summary:
- Converted: 34 components
- Already functional: 56 components
- Cannot convert: 3 components
- Failed: 1 component

Changes made to 34 files.
```

<failed-attempts>
What DOESN'T work:
- No batching on 500+ files: Timeout, context overflow
- Vague map function: "Check for issues" → inconsistent results
- No reduce strategy: End up with 200 disconnected bullet points
- Processing order-dependent items: Results inconsistent
- Ignoring failures: Miss important edge cases
</failed-attempts>

## Why This Elixir Exists

"Check everything" is easy to say, hard to do well. Without structure, you get
incomplete coverage, inconsistent analysis, and no useful summary.

Map-Reduce brings discipline to bulk operations: every item processed uniformly,
failures tracked, results aggregated meaningfully. It's the difference between
"I looked at some files" and "I analyzed all 234 files, here's what I found."

Scale requires structure. This is that structure.
