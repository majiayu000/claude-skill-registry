---
name: review-tool-speed
description: Review query tools for runtime optimization opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Investigate query tool runtime and find optimization opportunities.

The query tools (`query_*.ps1` in `tools/`) are critical for keeping context bloat down and getting programmatic answers.

1. Investigate each query tool for potential optimizations to decrease runtime. Optimizations must be **internal only** — no change to output, function, or contract of the tool.
2. For each recommendation, include an analysis statement explaining why it's internal-only and doesn't change the tool's job or contract.
3. Consider: caching, pipeline vs loop, regex precompilation, redundant file reads, shared parsing, startup overhead, etc.

Research the query tools deeply. Write a plan for all optimizations found. Ignore any existing plans — create a fresh one.

## Measurement & Verification Tools

Two tools in `tools/` support this workflow. Use them — do not reinvent timing or golden-output infrastructure.

### `tools/bench_query.ps1` — Timing benchmark
Runs all query tools with representative args, reports external and internal timing.
```
powershell -File tools/bench_query.ps1                  # 3 iterations, full report
powershell -File tools/bench_query.ps1 -InternalOnly    # internal timing only
powershell -File tools/bench_query.ps1 -Iterations 5    # more iterations for stability
```

### `tools/verify_query.ps1` — Golden output capture & verification
Captures tool output before changes, verifies output is unchanged after. Strips timing lines automatically. 22 test cases across all query tools.
```
powershell -File tools/verify_query.ps1 -Capture        # save golden (prints dir path)
powershell -File tools/verify_query.ps1 -Verify <dir>   # compare against golden
```

### Required workflow
1. **Before changes:** Run `verify_query.ps1 -Capture` and `bench_query.ps1` for baseline
2. **After each change:** Run `verify_query.ps1 -Verify <golden-dir>` — must pass
3. **After all changes:** Run `bench_query.ps1` — compare against baseline, no regressions
