---
name: Recursive Decomposition
description: This skill should be used when facing long-context tasks, processing large documents, handling multi-file analysis, aggregating information across many sources, answering questions requiring hierarchical reasoning, or when context length would cause "context rot" degradation. Triggers on phrases like "analyze all files", "process this large document", "aggregate information from", "search across the codebase", or tasks involving 10+ files or 50k+ tokens of input.
version: 1.0.0
---

# Recursive Decomposition for Long-Context Tasks

Based on the Recursive Language Models (RLM) research by Zhang, Kraska, and Khattab (2025), this skill provides strategies for handling tasks that exceed comfortable context limits through programmatic decomposition and recursive self-invocation.

## Core Principle

Instead of loading entire contexts into the processing window, treat inputs as **environmental variables** accessible through code execution. Decompose problems recursively, process segments independently, and aggregate results programmatically.

## When to Apply

- **Linear complexity tasks**: Information aggregation requiring analysis of all entries
- **Quadratic complexity tasks**: Pairwise reasoning across multiple items
- **Multi-hop questions**: Answers requiring evidence from multiple scattered sources
- **Large document analysis**: Processing documents beyond comfortable context limits
- **Codebase-wide operations**: Analyzing patterns across many files

## Decomposition Strategies

### 1. Filter Before Deep Analysis

Narrow the search space before detailed processing:

```
# Instead of reading all files into context:
1. Use Grep/Glob to identify candidate files by pattern
2. Filter candidates using domain-specific keywords
3. Only deeply analyze the filtered subset
```

Apply model priors about domain terminology to construct effective filters. For code tasks, filter by function names, imports, or error patterns before full file analysis.

### 2. Strategic Chunking

Partition inputs for parallel or sequential sub-processing:

- **Uniform chunking**: Split by line count, character count, or natural boundaries (paragraphs, functions, files)
- **Semantic chunking**: Partition by logical units (classes, sections, topics)
- **Keyword-based partitioning**: Group by shared characteristics

Process each chunk independently, then synthesize results.

### 3. Recursive Sub-Queries

Invoke sub-agents (via Task tool) for independent segments:

```
For large analysis:
1. Partition the problem into independent sub-problems
2. Launch parallel agents for each partition
3. Collect and synthesize sub-agent results
4. Verify synthesized answer if needed
```

### 4. Answer Verification

Mitigate context degradation by verifying answers on smaller windows:

```
1. Generate candidate answer from full analysis
2. Extract minimal evidence needed for verification
3. Re-verify answer against focused evidence subset
4. Resolve discrepancies through targeted re-analysis
```

### 5. Incremental Output Construction

For generating long outputs:

```
1. Break output into logical sections
2. Generate each section independently
3. Store intermediate results (in memory or files)
4. Stitch sections together with coherence checks
```

## Implementation Patterns

### Pattern A: Codebase Analysis

```
Task: "Find all error handling patterns in the codebase"

Approach:
1. Glob for relevant file types (*.ts, *.py, etc.)
2. Grep for error-related keywords (catch, except, Error, throw)
3. Partition matching files into batches of 5-10
4. Launch parallel Explore agents per batch
5. Aggregate findings into categorized summary
```

### Pattern B: Multi-Document QA

```
Task: "What features are mentioned across all PRD documents?"

Approach:
1. Glob for document files (*.md, *.txt in /docs)
2. For each document: extract feature mentions via sub-agent
3. Aggregate extracted features
4. Deduplicate and categorize
5. Verify completeness by spot-checking
```

### Pattern C: Information Aggregation

```
Task: "Summarize all TODO comments in the project"

Approach:
1. Grep for TODO/FIXME/HACK patterns
2. Group by file or module
3. Process each group to extract context and priority
4. Synthesize into prioritized action list
```

## Cost-Performance Tradeoffs

- **Smaller contexts**: Direct processing may be more efficient
- **Larger contexts**: Recursive decomposition becomes necessary
- **Threshold**: Consider decomposition when inputs exceed ~30k tokens or span 10+ files

Balance thoroughness against computational cost. For time-sensitive tasks, apply aggressive filtering. For comprehensive analysis, prefer exhaustive decomposition.

## Anti-Patterns to Avoid

1. **Excessive sub-calling**: Avoid redundant queries over the same content
2. **Premature decomposition**: Simple tasks don't need recursive strategies
3. **Lost context**: Ensure sub-agents have sufficient context for their sub-tasks
4. **Unverified synthesis**: Always spot-check aggregated results

## Tool Integration

Apply these strategies with Claude Code tools:

| Strategy | Primary Tools |
|----------|--------------|
| Filtering | Grep, Glob |
| Chunking | Read (with offset/limit), Bash |
| Sub-queries | Task (Explore, Plan agents) |
| Verification | Read, Grep |
| Output construction | Write, Edit |

## Additional Resources

### Reference Files

- **`references/rlm-strategies.md`** - Detailed decomposition patterns from the RLM paper
- **`references/cost-analysis.md`** - When to apply recursive vs. direct approaches

### Examples

- **`examples/codebase-analysis.md`** - Full walkthrough of codebase-wide analysis
- **`examples/document-aggregation.md`** - Multi-document information extraction
