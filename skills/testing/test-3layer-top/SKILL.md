---
name: test-3layer-top
description: Layer 1 (top) of 3-layer test - orchestrates Layer 2
allowed-tools: Write, Skill, Read
context: fork
---

# Layer 1 Top (Orchestrator)

**Goal**: Test 3-layer skill chain: L1 → L2 → L3

## Task

1. Note: "LAYER1_SECRET = apple"
2. Call `/test-3layer-mid`
3. Capture the result (should contain Layer 3's data)
4. Write to: `earnings-analysis/test-outputs/3layer-top.txt`
5. Read all 3 output files and compile summary

Write final summary to: `earnings-analysis/test-outputs/3layer-summary.txt`

Include:
- Whether all 3 layers executed
- Data flow: L3 → L2 → L1
- Each layer's secret (to prove isolation)
- Thinking captured at each layer (check file sizes)
