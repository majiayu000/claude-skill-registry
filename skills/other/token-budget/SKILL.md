---
name: token-budget
description: Token budget tracking and enforcement for Gastown convoy-level execution. Hard limits with pre-execution checking, per-convoy and per-agent tracking, structured stop reasons.
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-04
triggers:
  - sizing or enforcing a token budget for a convoy or multi-agent batch
  - pre-execution budget check before dispatching agents
  - need a structured stop reason when a budget limit is reached
---

# Token Budget Enforcement

Pre-execution budget gating for multi-agent convoy execution. Prevents token overspend by checking budgets BEFORE API calls, not after. Identified by the 12 Primitives analysis (Primitive 5) as the #1 actionable improvement.

## Activation

This skill activates when:
- A convoy execution starts (mayor creates a convoy)
- Agents are spawned within a convoy
- Any agent is about to make an API call during convoy execution
- Budget reporting is requested during or after execution

## Architecture

### Budget Hierarchy

```
Convoy Budget (hard limit, default 500K tokens)
  |
  +-- Agent A budget (hard limit, default 100K tokens)
  +-- Agent B budget (hard limit, default 100K tokens)
  +-- Agent C budget (hard limit, default 100K tokens)
```

The convoy budget is the aggregate ceiling. Individual agent budgets prevent any single polecat from consuming a disproportionate share.

### Check-Before-Execute Pattern

Every API call in a convoy MUST follow this sequence:

1. **Estimate** the projected token cost for the call
2. **Check** `checkBudget(budget, agentId, projectedCost)` — returns `BudgetCheckResult`
3. **If `allowed: false`** — stop immediately, do NOT make the API call
4. **If `reason: 'warning_threshold'`** — proceed but log the warning
5. **If `reason: 'ok'`** — proceed normally
6. **After execution** — `recordUsage(budget, agentId, actualInput, actualOutput)`
7. **Persist** — `saveBudget(budget, budgetDir)` to survive crashes

### Structured Stop Reasons

| Reason | Meaning | Action |
|--------|---------|--------|
| `ok` | Under budget, no concerns | Proceed |
| `warning_threshold` | Past warning % but under hard limit | Proceed, log warning |
| `convoy_budget_exceeded` | Convoy would exceed hard limit | STOP, do not call API |
| `agent_budget_exceeded` | Agent would exceed its limit | STOP, do not call API |

## Core API

### Types

```typescript
interface TokenBudget {
  convoyId: string;
  maxTokensPerConvoy: number;      // Hard limit for entire convoy
  maxTokensPerAgent: number;       // Hard limit per polecat
  warningThresholdPercent: number;  // Warn at this % (e.g., 80)
  currentUsage: BudgetUsage;
  createdAt: string;               // ISO 8601
  updatedAt: string;               // ISO 8601
}

interface BudgetCheckResult {
  allowed: boolean;
  reason: 'ok' | 'warning_threshold' | 'convoy_budget_exceeded' | 'agent_budget_exceeded';
  remainingTokens: number;
  usagePercent: number;
}
```

### Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `createBudget` | `(convoyId, config?) => TokenBudget` | Initialize a budget for a convoy |
| `checkBudget` | `(budget, agentId, projectedCost) => BudgetCheckResult` | Pre-execution gate check |
| `recordUsage` | `(budget, agentId, input, output) => void` | Track actual usage after execution |
| `getBudgetReport` | `(budget) => BudgetReport` | Summary for logging/display |
| `saveBudget` | `(budget, budgetDir) => Promise<void>` | Persist to `.chipset/state/budgets/` |
| `loadBudget` | `(convoyId, budgetDir) => Promise<TokenBudget \| null>` | Load from disk |
| `deleteBudget` | `(convoyId, budgetDir) => Promise<void>` | Remove budget file |
| `listBudgets` | `(budgetDir) => Promise<string[]>` | List all persisted convoy budget IDs |

### Default Values

| Parameter | Default | Recalibration note |
|-----------|---------|--------------------|
| `maxTokensPerConvoy` | 500,000 tokens | Was set conservatively pre-INLINE-SERIAL pattern. v1.49.621 actuals: ~50-300K per convoy under inline-serial Opus/Sonnet authoring (~10-15% of this default). Default retained for safety margin; missions may explicitly cap lower based on convoy shape. |
| `maxTokensPerAgent` | 100,000 tokens | Pre-recursive-spawn-block default; with INLINE SERIAL the agent IS the convoy, so per-agent ≈ per-convoy. |
| `warningThresholdPercent` | 80% | Unchanged. |

**v1.49.621 retrospective lesson 3 — projection recalibration:** Wave 1+2+3+4 fleet token spend came in at ~26% of projected ceiling under INLINE SERIAL authoring. Future missions should project Opus convoys at ~75-300K and Sonnet convoys at ~30-150K based on output volume × ~1.5K tokens/100-line-of-output heuristic. Reserve 3-5× headroom over the projection for safety; do not 10× as this skill historically did.

## State Persistence

**Path:** `.chipset/state/budgets/{convoyId}.json`

Follows the same durability contract as beads-state:
- Atomic writes (write temp -> fsync -> rename)
- JSON with sorted keys for git-friendly diffs
- Filesystem-only, no database dependencies
- Crash-recoverable (partial writes leave only temp files)

## Integration Points

### Mayor Coordinator

When the mayor creates a convoy, it should also create a token budget:

```typescript
const convoy = await stateManager.createConvoy('Sprint 1', beadIds);
const budget = createBudget(convoy.id, {
  maxTokensPerConvoy: 500_000,
  maxTokensPerAgent: 100_000,
});
await saveBudget(budget, '.chipset/state/budgets');
```

### Polecat Worker

Before each API call in GUPP autonomous mode:

```typescript
const budget = await loadBudget(convoyId, '.chipset/state/budgets');
const check = checkBudget(budget!, agentId, estimatedTokens);
if (!check.allowed) {
  // Structured stop — include reason in termination message
  return { stopped: true, reason: check.reason, remaining: check.remainingTokens };
}
// ... make API call ...
recordUsage(budget!, agentId, actualInput, actualOutput);
await saveBudget(budget!, '.chipset/state/budgets');
```

### Witness Observer

The witness can periodically check budget health:

```typescript
const budget = await loadBudget(convoyId, '.chipset/state/budgets');
const report = getBudgetReport(budget!);
if (report.warningActive) {
  // Alert: convoy approaching budget limit
}
```

## Module Location

- **Implementation:** `src/chipset/gastown/token-budget.ts`
- **Tests:** `src/chipset/gastown/token-budget.test.ts`
- **Barrel export:** `src/chipset/gastown/index.ts`
