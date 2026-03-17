---
name: performance-optimisation
description: Analyses and optimises performance across frontend, backend and database interactions. Identifies bottlenecks and implements solutions to enhance speed and efficiency.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Performance Optimisation Skill

## Tooling Notes

This skill should only use read-only commands and avoid modifying files.

## Workflow

Copy this checklist and use it to track your progress through the performance optimisation process:

```markdown
Performance Optimisation Checklist

- [ ] Measure Baseline Performance
  - [ ] Use profiling tools to gather performance metrics.
  - [ ] Identify slow functions, database queries, and network requests.
- [ ] Identify Bottlenecks
  - [ ] Analyse profiling data to pinpoint performance issues.
  - [ ] Prioritise issues based on impact and ease of resolution.
- [ ] Implement Optimisations
  - [ ] Optimise algorithms and data structures.
  - [ ] Improve database query efficiency.
  - [ ] Reduce network latency and payload sizes.
  - [ ] Implement caching strategies where appropriate.
- [ ] Validate Improvements
  - [ ] Re-measure performance after optimisations.
  - [ ] Ensure that optimisations have led to measurable improvements.
- [ ] Document Changes
  - [ ] Update documentation to reflect performance changes.
  - [ ] Provide explanations for significant optimisations.
```

### Profiling Commands

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-0x*.log > processed.txt

# Python profiling
python -m cProfile -o profile.out app.py
snakeviz profile.out

# Database query analysis (PostgreSQL example)
EXPLAIN ANALYZE SELECT * FROM your_table WHERE condition;

# Web performance analysis
lighthouse https://yourwebsite.com --output html --output-path report.html
```

### Common Bottlenecks and Ways to Fix Them

- **Inefficient Algorithms**: Replace with more efficient algorithms or data structures.
- **Database Query Performance**: Optimize queries, add indexes, or denormalize data.
- **Network Latency**: Minimize requests, use CDNs, and compress payloads.
- **Unnecessary Computations**: Cache results of expensive operations.
- **Memory Leaks**: Identify and fix memory leaks to improve performance over time.
