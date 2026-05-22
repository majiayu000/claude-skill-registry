---
name: test-3layer-mid
description: Layer 2 (middle) of 3-layer test - calls Layer 3
allowed-tools: Write, Skill
context: fork
---

# Layer 2 Middle

**Goal**: Call Layer 3 skill and pass result to Layer 1.

## Task

1. Note: "LAYER2_SECRET = orange"
2. Call `/test-3layer-bottom`
3. Capture the result
4. Write to: `earnings-analysis/test-outputs/3layer-mid.txt`

Return format: "LAYER2_RECEIVED: [what Layer 3 returned] | LAYER2_SECRET: orange"
