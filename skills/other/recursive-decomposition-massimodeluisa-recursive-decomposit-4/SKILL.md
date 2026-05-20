---
name: recursive-decomposition
description: Based on the Recursive Language Models (RLM) research by Zhang, Kraska, and Khattab (2025), this skill provides strategies for handling tasks that exceed comfortable context limits through programmatic decomposition and recursive self-invocation. Triggers on phrases like "analyze all files", "process this large document", "aggregate information from", "search across the codebase", or tasks involving 10+ files or 50k+ tokens.
---

# Recursive Decomposition Guidelines

## References

Consult these resources as needed:

- ./references/rlm-strategies.md -- Detailed decomposition patterns from the RLM paper
- ./references/cost-analysis.md -- When to apply recursive vs. direct approaches
- ./references/codebase-analysis.md -- Full walkthrough of codebase-wide analysis
- ./references/document-aggregation.md -- Multi-document information extraction

## Core Principles

**CRITICAL: Treat inputs as environmental variables, not immediate context.**

Most tasks fail when context is overloaded. Instead of loading entire contexts into the processing window, treat inputs as **environmental variables** accessible through code execution. Decompose problems recursively, process segments independently, and aggregate results programmatically.

**Progressive Disclosure**: Load information only when necessary. Start high-level to map the territory, then dive deep into specific areas.

### When Recursive Decomposition is Required

-   Tasks involving 10+ files
-   Input exceeding ~50k tokens where single-prompt context is insufficient
-   Multi-hop questions requiring evidence from multiple scattered sources
-   Codebase-wide pattern analysis or migration planning

### When Direct Processing Works

-   Small contexts (<30k tokens)
-   Single file analysis
-   Linear complexity tasks with manageable inputs

## Operational Rules

-   Always identify the search space size first.
-   Always use `grep` or `glob` before `view_file` on directories.
-   Always partition lists > 10 items into batches.
-   Never read more than 5 files into context without a specific plan.
-   Verify synthesized answers by spot-checking source material.
-   Mitigate "context rot" by verifying answers on smaller windows.
-   **Treat yourself as an autonomous agent, not just a passive responder.**

## Large File Handling Protocols

**CRITICAL**: Do NOT read large files directly into context.

1.  **Check Size First**: Always run `wc -l` (lines) or `ls -lh` (size) before `view_file`.
2.  **Hard Limits**:
    *   **Text/Code**: > 2,000 lines or > 50KB -> **MUST** use `view_file` with `start_line`/`end_line` or `head`/`tail`.
    *   **PDFs**: > 30MB or > 100 pages -> **MUST** be split or processed by metadata only.
3.  **Strategy**:
    *   For code: Read definitions first (`grep -n "function" ...`) then read specific bodies.
    *   For text: Read Table of Contents or Abstract first.

## Tool Preferences

-   `grep` / `glob` not `ls -R` (unless mapping structure).
-   `view_file` with line ranges (offset/limit) not full file reads for huge files.
-   `wc -l` / `ls -lh` before reading unknown files.
-   `run_command` (grep) not `read_file` for searching.
-   `task` tool for sub-agents (recurse).

## Empowering Agentic Behavior

To maximize effectiveness:

-   **Self-Correction**: Always verify your own work. If a result seems empty or wrong, debug the approach (e.g., check grep arguments) before giving up.
-   **Aggressive Context Management**: Regularly clear irrelevant history. Don't let the context window rot with dead ends.
-   **Plan First**: For any task > 3 steps, write a mini-plan.
-   **Safe YOLO Mode**: When appropriate (e.g., read-only searches), proceed with confidence without asking for permission on every single step, but stop for critical actions.

## Cost-Performance Tradeoffs

-   **Smaller contexts**: Direct processing may be more efficient.
-   **Larger contexts**: Recursive decomposition becomes necessary.
-   **Threshold**: Consider decomposition when inputs exceed ~30k tokens or span 10+ files.

Balance thoroughness against computational cost. For time-sensitive tasks, apply aggressive filtering. For comprehensive analysis, prefer exhaustive decomposition.

## Anti-Patterns to Avoid

-   **Excessive sub-calling**: Avoid redundant queries over the same content.
-   **Premature decomposition**: Simple tasks don't need recursive strategies.
-   **Lost context**: Ensure sub-agents have sufficient context for their sub-tasks.
-   **Unverified synthesis**: Always spot-check aggregated results.

## Scalability (Chunking & filtering)

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

-   **Uniform chunking**: Split by line count, character count, or natural boundaries (paragraphs, functions, files).
-   **Semantic chunking**: Partition by logical units (classes, sections, topics).
-   **Keyword-based partitioning**: Group by shared characteristics.

Process each chunk independently, then synthesize results.

### 3. Incremental Output Construction

For generating long outputs:

```
1. Break output into logical sections
2. Generate each section independently
3. Store intermediate results (in memory or files)
4. Stitch sections together with coherence checks
```

## Agent Behavior

### Recursive Sub-Queries

Invoke sub-agents (via Task tool) for independent segments:

```
For large analysis:
1. Partition the problem into independent sub-problems
2. Launch parallel agents for each partition
3. Collect and synthesize sub-agent results
4. Verify synthesized answer if needed
```

### Answer Verification

Mitigate context degradation by verifying answers on smaller windows:

```
1. Generate candidate answer from full analysis
2. Extract minimal evidence needed for verification
3. Re-verify answer against focused evidence subset
4. Resolve discrepancies through targeted re-analysis
```

# Implementation Patterns

## Pattern A: Codebase Analysis

Task: "Find all error handling patterns in the codebase"

**Approach:**
1.  Glob for relevant file types (`*.ts`, `*.py`, etc.)
2.  Grep for error-related keywords (`catch`, `except`, `Error`, `throw`)
3.  Partition matching files into batches of 5-10
4.  Launch parallel Explore agents per batch
5.  Aggregate findings into categorized summary

## Pattern B: Multi-Document QA

Task: "What features are mentioned across all PRD documents?"

**Approach:**
1.  Glob for document files (`*.md`, `*.txt` in `/docs`)
2.  For each document: extract feature mentions via sub-agent
3.  Aggregate extracted features
4.  Deduplicate and categorize
5.  Verify completeness by spot-checking

## Pattern C: Information Aggregation

Task: "Summarize all TODO comments in the project"

**Approach:**
1.  Grep for `TODO`/`FIXME`/`HACK` patterns
2.  Group by file or module
3.  Process each group to extract context and priority
4.  Synthesize into prioritized action list
