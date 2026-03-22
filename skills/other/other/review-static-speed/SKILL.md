---
name: review-static-speed
description: Review static analysis checks for runtime optimization opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Investigate static analysis runtime and find optimization opportunities.

1. Run `.\tests\test.ps1 --timing` to get the timing report. Identify the most time-consuming checks.
2. For each check, investigate the implementation for potential optimizations. Optimizations must be **internal only** — no change to output, function, or contract of the checker.
3. Consider these optimization vectors:
   - Should any standalone checks be batched together to reduce PowerShell overhead?
   - Can existing batches share a single file cache across sub-checks?
   - Should any checks move between batches for better cache locality?
   - Should any batch sub-check be broken out to standalone (if it's an outlier)?
   - Any other internal speedups (regex precompilation, pipeline vs loop, etc.)?
4. For each recommendation, include an analysis statement explaining why it's internal-only and doesn't change the checker's job or contract.

Research the production code and static analysis deeply. Write a plan for all optimizations found. Ignore any existing plans — create a fresh one.

Include in the plan a verification step - Run timing comparison (before vs after) each change. Theoretical changes have provably been hidden regressions. Validate. 