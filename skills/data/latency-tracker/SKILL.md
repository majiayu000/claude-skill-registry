---
name: latency-tracker
description: 'Per-call and aggregated latency tracking for MEV infrastructure. Use
  when implementing performance monitoring or debugging slow operations. Triggers
  on: latency, timing, performance, slow, speed, inst'
---

---
name: latency-tracker
description: Per-call and aggregated latency tracking for MEV infrastructure. Use when implementing performance monitoring or debugging slow operations. Triggers on: latency, timing, performance, slow, speed, instrumentation.
---

# Latency Tracker

Per-call and aggregated latency tracking for MEV infrastructure.

## When to Use

- Implementing performance monitoring
- Debugging slow operations
- Adding instrumentation to code paths
- Tracking end-to-end latency
- Setting up alerting thresholds

## Workflow

### Step 1: Define Span Hierarchy

Structure spans from e2e_flow down to individual calls.

### Step 2: Instrument Code

Wrap operations in tracker.span() calls.

### Step 3: Set Alert Thresholds

Configure alerts for latency exceeding expected ranges.

---

## Span Hierarchy
e2e_flow (root)
├── rust_hotpath_call (5-15ms)
│   └── rpc_eth_call (5-20ms)
├── tx_submit
└── tx_confirm (1-15s)

## Usage
```typescript
const e2e = tracker.startE2E('liq');

await e2e.span('rust_call', async () => {
  return await callRust();
});

e2e.complete({ success: true });
```

## Alert Thresholds

| Span | Expected | Alert |
|------|----------|-------|
| rust_hotpath | 5-15ms | >30ms |
| rpc_eth_call | 5-20ms | >50ms |
| e2e_to_submit | 10-50ms | >100ms |
