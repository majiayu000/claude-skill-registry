---
name: sql-query-optimization
description: A skill for optimizing SQL queries, focusing on PostgreSQL. It provides a checklist for query analysis, guidance on reading EXPLAIN plans, and patterns for common optimization problems like N+1 queries, JOINs, and pagination. Includes templates for benchmarking and recommending indexes. Use this skill when a user wants to improve the performance of a SQL query.
---

# SQL Query Optimization (PostgreSQL)

This skill provides a structured workflow and resources for optimizing PostgreSQL queries.

## Workflow

1.  **Understand the Query and Goal**: Clarify what the query does and what the performance goal is (e.g., reduce latency, reduce resource usage).
2.  **Establish a Baseline**: Use `assets/benchmarking-template.md` to record the current performance of the query.
3.  **Analyze and Optimize**: Follow the `references/checklist.md` to analyze the query and identify optimization opportunities. This checklist will guide you through using the other reference documents.
4.  **Benchmark the Optimized Query**: Record the performance of the new query in the benchmarking document to verify the improvement.
5.  **Present the Solution**: Explain the changes made and the performance impact, using the before/after examples and benchmark results.

## Bundled Resources

### References (`references/`)

Use these documents as guided by the `references/checklist.md`.

*   **`checklist.md`**: The main guide. Start here for any optimization task.
*   **`explain-plan-analysis.md`**: Deep dive into reading `EXPLAIN` and `EXPLAIN ANALYZE` output.
*   **`index-optimization.md`**: How to identify and create effective indexes.
*   **`n-plus-one-queries.md`**: Guide to fixing N+1 query issues.
*   **`join-optimization.md`**: Best practices for `JOIN` performance.
*   **`subquery-vs-join.md`**: Comparison and trade-offs between subqueries and `JOIN`s.
*   **`pagination.md`**: Implementing efficient cursor-based (keyset) pagination.
*   **`caching.md`**: Strategies for caching query results.
*   **`examples.md`**: A collection of before-and-after optimization examples.

### Assets (`assets/`)

*   **`benchmarking-template.md`**: A template for documenting performance benchmarks. Copy this file to a new location for use.
