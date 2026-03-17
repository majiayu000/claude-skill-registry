---
name: cost-accrual-tracker
description: Track real-time API cost accrual during LLM execution. Activate on 'cost tracking', 'token usage', 'API costs', 'budget monitoring', 'usage metrics'. NOT for cost estimation, pricing tiers, or billing systems.
allowed-tools: Read,Write,Edit
---

# Cost Accrual Tracker

Real-time tracking of API costs during LLM execution with support for partial costs on abort.

## When to Use

✅ **Use for**:
- Implementing real-time cost tracking during execution
- Capturing partial costs when executions are aborted
- Building cost display widgets for execution UIs
- Integrating token counting into execution pipelines
- Adding budget thresholds with auto-stop

❌ **NOT for**:
- Cost estimation before execution (use pricing calculators)
- Billing system design (use billing-system skill)
- Price tier management or discounts
- Historical cost analytics dashboards

## Core Patterns

### 1. Token-Based Cost Calculation

```typescript
interface TokenUsage {
  inputTokens: number;
  outputTokens: number;
  cacheReadTokens?: number;   // Prompt caching hits
  cacheWriteTokens?: number;  // Prompt caching misses
}

interface CostCalculation {
  inputCostUsd: number;
  outputCostUsd: number;
  cacheSavingsUsd?: number;
  totalCostUsd: number;
}

function calculateCost(usage: TokenUsage, model: string): CostCalculation {
  const pricing = MODEL_PRICING[model];

  const inputCostUsd = (usage.inputTokens / 1_000_000) * pricing.inputPerMTok;
  const outputCostUsd = (usage.outputTokens / 1_000_000) * pricing.outputPerMTok;

  return {
    inputCostUsd,
    outputCostUsd,
    totalCostUsd: inputCostUsd + outputCostUsd,
  };
}
```

### 2. Incremental Accrual Pattern

Track costs as they accrue, not just at completion:

```typescript
class CostAccrualTracker {
  private totalInputTokens = 0;
  private totalOutputTokens = 0;
  private accruedCostUsd = 0;
  private readonly model: string;

  constructor(model: string) {
    this.model = model;
  }

  /**
   * Called after each API response (streaming or complete)
   */
  recordUsage(usage: TokenUsage): void {
    this.totalInputTokens += usage.inputTokens;
    this.totalOutputTokens += usage.outputTokens;

    const cost = calculateCost(usage, this.model);
    this.accruedCostUsd += cost.totalCostUsd;
  }

  /**
   * Get current accrued cost (for real-time display)
   */
  getCurrentCost(): number {
    return this.accruedCostUsd;
  }

  /**
   * Finalize on completion or abort
   */
  finalize(reason: 'completed' | 'aborted' | 'failed'): CostReport {
    return {
      totalInputTokens: this.totalInputTokens,
      totalOutputTokens: this.totalOutputTokens,
      totalCostUsd: this.accruedCostUsd,
      completionReason: reason,
      finalizedAt: Date.now(),
    };
  }
}
```

### 3. Abort-Aware Cost Capture

**Critical**: Always capture partial costs on abort:

```typescript
// In execution handler
const tracker = new CostAccrualTracker(model);

try {
  for await (const chunk of executeStream(request)) {
    if (abortSignal.aborted) {
      // CRITICAL: Capture cost BEFORE throwing
      const partialCost = tracker.finalize('aborted');
      onCostUpdate(partialCost);
      throw new AbortError('Execution aborted');
    }

    tracker.recordUsage(chunk.usage);
    onCostUpdate(tracker.getCurrentCost());
  }

  return tracker.finalize('completed');
} catch (error) {
  if (error instanceof AbortError) {
    throw error; // Already handled
  }
  return tracker.finalize('failed');
}
```

### 4. Budget Threshold Pattern

Auto-stop execution when budget is exceeded:

```typescript
interface BudgetConfig {
  maxCostUsd: number;
  warnAtPercentage: number;  // e.g., 0.8 for 80%
  onWarn?: (current: number, max: number) => void;
  onExceed?: (current: number, max: number) => void;
}

function createBudgetGuard(config: BudgetConfig) {
  return {
    check(currentCostUsd: number): 'ok' | 'warn' | 'exceed' {
      const percentage = currentCostUsd / config.maxCostUsd;

      if (percentage >= 1.0) {
        config.onExceed?.(currentCostUsd, config.maxCostUsd);
        return 'exceed';
      }

      if (percentage >= config.warnAtPercentage) {
        config.onWarn?.(currentCostUsd, config.maxCostUsd);
        return 'warn';
      }

      return 'ok';
    }
  };
}
```

## Anti-Patterns

### Lost Costs on Abort

**Novice thinking**: "Just throw an error when aborted"

**Reality**: If you don't capture costs before aborting, you lose:
- Token usage data for partial execution
- Accurate cost reporting for billing
- Audit trail for debugging

**Timeline**: Always been an issue, but became critical with expensive models (GPT-4, Claude Opus)

**Correct approach**: Always call `finalize()` with partial data BEFORE throwing abort errors.

### Polling Without Debounce

**Novice thinking**: "Poll cost endpoint every 100ms for real-time updates"

**Reality**:
- Wastes bandwidth and CPU
- Cost updates only happen after API responses
- Polling faster than response rate is pointless

**Correct approach**: Poll at 1-2 second intervals, or use event-driven updates from the execution stream.

### Ignoring Prompt Caching

**Novice thinking**: "Just multiply tokens by price per token"

**Reality**: Claude's prompt caching changes the cost model:
- Cache reads are 90% cheaper
- Cache writes cost extra on first use
- Ignoring caching leads to inaccurate costs

**Timeline**:
- Pre-2024: No caching, simple calculation
- 2024+: Claude prompt caching requires separate tracking

**Correct approach**: Track `cache_read_input_tokens` and `cache_creation_input_tokens` separately.

### Per-Request Cost Objects

**Novice thinking**: "Create new tracker for each request"

**Reality**: For DAG execution with multiple nodes:
- Need aggregate cost across all nodes
- Need to attribute costs to specific nodes
- Need rollup for parent execution

**Correct approach**: Hierarchical tracking - per-node trackers that roll up to execution-level.

## State Flow

```
                    ┌─────────────────────────────────────────┐
                    │           CostAccrualTracker            │
                    └─────────────────────────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │  recordUsage()  │     │ getCurrentCost()│     │   finalize()    │
    │                 │     │                 │     │                 │
    │ After each API  │     │ For real-time   │     │ On completion,  │
    │ response        │     │ display         │     │ abort, or fail  │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
              │                         │                         │
              │                         │                         │
              ▼                         ▼                         ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                        CostReport                               │
    │  { inputTokens, outputTokens, totalCostUsd, completionReason }  │
    └─────────────────────────────────────────────────────────────────┘
```

## UI Display Pattern

For real-time cost display in execution UIs:

```typescript
// Poll every 2 seconds while executing
useEffect(() => {
  if (status !== 'running') return;

  const interval = setInterval(async () => {
    const response = await fetch(`/api/execute/${executionId}`);
    const data = await response.json();
    setAccruedCost(data.cost.accruedUsd);
    setTokens({
      input: data.cost.inputTokens,
      output: data.cost.outputTokens,
    });
  }, 2000);

  return () => clearInterval(interval);
}, [executionId, status]);

// Display format
<div className="cost-display">
  <span className="cost-amount">${accruedCost.toFixed(4)}</span>
  <span className="token-count">
    {tokens.input.toLocaleString()} in / {tokens.output.toLocaleString()} out
  </span>
</div>
```

## Integration Points

| Component | Responsibility |
|-----------|----------------|
| `CostAccrualTracker` | Per-execution token counting and cost calculation |
| `ExecutionManager` | Aggregates costs across DAG executions |
| `BudgetGuard` | Threshold monitoring and auto-stop |
| `/api/execute/:id` | Exposes current cost via polling |
| Cost Display Widget | Real-time UI rendering |

## References

See `/references/claude-api-pricing.md` for current Claude API pricing.
