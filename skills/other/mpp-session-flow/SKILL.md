---
name: mpp-session-flow
description: Implement MPP session-based streaming payment flows — authorize-once pay-as-you-go patterns for continuous data feeds, per-token billing, and micropayment aggregation. Use when building streaming APIs or services that charge incrementally.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Session Flow (Streaming Payments)

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.npmjs.com/package/mppx` for the session middleware API and payment channel configuration
2. Fetch `https://paymentauth.org/` for the canonical session intent specification
3. Web-search `mpp session streaming micropayments payment channel` for session implementation patterns
4. Web-search `site:mpp.dev session` for session-specific documentation

## Conceptual Architecture

### What Session Intent Is

The session intent implements **streaming micropayments** — often described as **"OAuth for money"**. The agent authorizes a spending limit upfront, then streams micropayments continuously as it consumes resources:

```
1. Client opens session with spending cap
2. Server creates payment channel
3. Client makes requests — each deducts from the spending cap
4. Micropayments stream at sub-cent costs, sub-millisecond latency
5. Session closes — final settlement on-chain (single transaction)
```

### When to Use Session

- **Per-token billing** — LLM inference charged per token generated
- **Continuous data feeds** — Real-time market data, sensor streams
- **Compute metering** — Pay for actual CPU/GPU seconds used
- **Bandwidth metering** — Pay per KB transferred
- **Any high-frequency, low-value access pattern**

### Session vs Charge Comparison

| Dimension | Charge | Session |
|-----------|--------|---------|
| Settlement | Per-request on-chain/card | Aggregated at session close |
| Latency | Includes payment settlement per call | Sub-millisecond after session open |
| Cost | One tx per request | One tx for entire session |
| Pricing | Fixed per request | Variable, metered |
| Use case | Infrequent, high-value calls | Frequent, low-value calls |

### Server-Side Implementation

```typescript
// Protect a route with a session payment gate
app.get('/api/stream', mppx.session({ maxAmount: '10000' }), async (c) => {
  // Deducts from the session's spending cap
  return c.json({ data: 'streaming content' });
});
```

### Session Lifecycle

1. **Open** — Client sends initial request; server returns 402 with session challenge
2. **Authorize** — Client authorizes spending cap (e.g., 10,000 units)
3. **Active** — Client makes requests; each deducts from the cap
4. **Refill** — Client can extend the cap before it runs out
5. **Close** — Either party closes; final settlement happens on-chain
6. **Settled** — Single on-chain transaction for the total consumed amount

### Payment Channel

Session payments use a **payment channel** — an off-chain mechanism where:
- Funds are locked upfront in a channel
- Each micropayment updates the channel state without on-chain transactions
- Only the opening and closing transactions go on-chain
- This enables thousands of sub-cent payments at sub-millisecond latency

### Spending Cap Management

- Agent sets the maximum they're willing to spend in the session
- Server deducts from this cap per request/unit consumed
- Agent can monitor remaining balance
- If cap is exhausted, server returns 402 for a new session
- Agent can proactively extend the cap

### Metering Patterns

| Pattern | Description |
|---------|-------------|
| Fixed per request | Each request costs a fixed amount |
| Per-unit | Cost varies by units consumed (tokens, bytes, seconds) |
| Time-based | Cost accrues per time interval |
| Tiered | Rate decreases with volume (first 100 at $X, next 1000 at $Y) |

### Best Practices

- Set reasonable default spending caps (not too high for safety, not too low for UX)
- Implement cap exhaustion warnings before the cap runs out
- Log metering data for billing reconciliation
- Handle session interruptions gracefully (network drops, server restarts)
- Implement session resumption where possible
- Monitor session durations and spending patterns for pricing optimization

Fetch the latest mppx SDK documentation and MPP specification for exact session API, payment channel mechanics, and configuration options before implementing.
