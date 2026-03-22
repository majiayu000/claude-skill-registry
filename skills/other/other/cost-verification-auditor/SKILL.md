---
name: cost-verification-auditor
description: Audit LLM token cost estimates against actual API usage. Activate on 'cost verification', 'token estimate accuracy', 'API cost audit', 'estimation variance'. NOT for pricing lookups, budget planning, or cost optimization strategies.
allowed-tools: Read,Write,Bash
---

# Cost Verification Auditor

Verify that token cost estimates are within ±20% of actual Claude API usage.

## When to Use

✅ **Use for**:
- Validating token estimation systems after implementation
- Pre-deployment cost accuracy checks
- Debugging unexpected API bills
- Periodic estimation drift detection

❌ **NOT for**:
- Looking up model pricing (use pricing docs)
- Budget planning or forecasting
- Cost optimization strategies
- Comparing models by price

## Core Audit Process

### Decision Tree

```
Has estimator? ──No──→ Build estimator first (see Calibration Guidelines)
      │
     Yes
      ↓
Define 3+ test cases (simple/medium/complex)
      ↓
Estimate BEFORE execution (no peeking!)
      ↓
Execute against real API
      ↓
Calculate variance: (actual - estimated) / estimated
      ↓
Variance ≤ ±20%? ──Yes──→ PASS ✓
      │
     No
      ↓
Apply fixes from Anti-Patterns section
      ↓
Re-run verification
```

### Variance Formula

```typescript
const inputVariance = (actual.inputTokens - estimate.inputTokens) / estimate.inputTokens;
const outputVariance = (actual.outputTokens - estimate.outputTokens) / estimate.outputTokens;
const costVariance = (actual.totalCost - estimate.totalCost) / estimate.totalCost;

// PASS if both input AND output within ±20%
const passed = Math.abs(inputVariance) <= 0.20 && Math.abs(outputVariance) <= 0.20;
```

## Common Anti-Patterns

### Anti-Pattern: The 500-Token Overhead Myth

**Novice thinking**: "Claude Code adds ~500 tokens overhead, so add that to every estimate."

**Reality**: Direct API calls have ~10 token overhead. The 500+ overhead is ONLY when using Claude Code's full context (system prompts, tools, conversation history).

**Timeline**:
- Pre-2025: Many tutorials used 500+ token estimates
- 2025+: Direct API overhead is minimal (~10 tokens)

**What to use instead**:
| Context | Overhead |
|---------|----------|
| Direct API call | ~10 tokens |
| With system prompt | 50-200 tokens |
| With tools/functions | 100-500 tokens |
| Claude Code full context | 500-2000 tokens |

**How to detect**: Consistent 40-90% overestimation = overhead too high.

---

### Anti-Pattern: Per-Node Accuracy Obsession

**Novice thinking**: "Every node must be within ±20% or the estimator is broken."

**Reality**: LLM output length is non-deterministic. Per-node output variance of 30-50% is normal. What matters is **aggregate cost accuracy**.

**What to use instead**:
- Focus on total DAG cost variance (should be ±20%)
- Accept per-node output variance up to ±40%
- Use constrained prompts ("list exactly 3") to reduce variance

**How to detect**: Input estimates accurate, output varies wildly = normal LLM behavior.

---

### Anti-Pattern: Peeking Before Estimating

**Novice thinking**: "Let me run the API call first to see what tokens we get, then build the estimator."

**Reality**: This produces perfectly-fitted estimates that fail on new prompts. Estimation must happen BEFORE execution.

**Correct approach**:
1. Estimate based on prompt length and heuristics
2. Execute API call
3. Compare variance
4. Adjust heuristics if needed

## Calibration Guidelines

### Input Token Estimation

```typescript
// Calibrated 2026-01-30
const inputTokens = Math.ceil(prompt.length / CHARS_PER_TOKEN) + OVERHEAD;
```

| Text Type | CHARS_PER_TOKEN | Notes |
|-----------|-----------------|-------|
| English prose | 4.0 | Most consistent |
| Code | 3.0-3.5 | Symbols tokenize differently |
| Mixed | 3.5 | Balanced (recommended default) |
| JSON/structured | 3.0 | Punctuation heavy |

### Output Token Estimation

| Prompt Constraint | Multiplier | Notes |
|-------------------|------------|-------|
| "List exactly N items" | 0.8x input | Highly constrained |
| "Brief summary" | 1.0x input | Moderate |
| "Explain in detail" | 2-3x input | Expansive |
| Unconstrained | 1.5x input | Variable |

**Always**: Minimum 100 output tokens for any meaningful response.

### Model Behavior

| Model | Output Tendency |
|-------|-----------------|
| Claude Opus | Longer, more detailed |
| Claude Sonnet | Balanced |
| Claude Haiku | Concise, efficient |

## Quick Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Overestimating by 40%+ | Overhead too high | Reduce from 500 → 10 |
| Underestimating inputs | Chars/token too high | Reduce from 4.0 → 3.5 |
| Output wildly varies | LLM non-determinism | Use constrained prompts |
| Total cost accurate but per-node off | Normal aggregation | Accept it, focus on totals |

## Verification Checklist

- [ ] 3+ test cases (simple, medium, complex)
- [ ] Estimates run BEFORE API calls
- [ ] Variance formula: `(actual - estimated) / estimated`
- [ ] Target: ±20% for input AND output
- [ ] Report includes actionable recommendations

## References

See `/references/calibration-data.md` for detailed calibration tables and historical data.
