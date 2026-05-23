---
name: rpc-selection-and-resilience
description: Playbook for selecting Solana RPC providers and building resilient client access (fallbacks, timeouts, rate limits, caching, cost control). Use when designing infra or debugging RPC issues.
---

# RPC Selection and Resilience

Role framing: You are a Solana infra engineer. Your goal is to choose the right RPC mix and make clients robust to rate limits, outages, and latency spikes.

## Initial Assessment
- Traffic profile: reads vs writes, peak TPS, burstiness, geographic distribution.
- Critical paths: which features are user-facing vs background? Latency SLOs?
- Budget: monthly cap? willingness to pay for priority lanes?
- Data needs: logs/blocks historical depth, filters, WebSocket support, state compression?
- Clients: browser, server, bots? Using connection pooling? Using Jito? Alchemy/Helius/QuickNode/own node?
- Observability stack: how to measure RPC errors/latency; alert thresholds.

## Core Principles
- Separate read/write: use high-quality paid endpoints for writes; cache-friendly endpoints for reads.
- Multi-provider strategy: primary + failover with health checks; avoid single vendor lock.
- Backpressure and rate limits: exponential backoff, jitter, and circuit breakers > blind retries.
- Timeouts tuned: short for UX-critical reads, longer for archival queries; prefer abortable fetch.
- Deterministic commitment: specify processed/confirmed/inalized per use case; avoid defaults.
- Security: pin RPC URLs; avoid leaking API keys to clients; prefer server-proxied writes.

## Workflow
1) Provider comparison
   - Evaluate: reliability SLA, included features (webhooks, state compression, enhanced APIs), geo, price per million requests, burst limits.
   - Select primary + two fallbacks; note auth schemes.
2) Endpoint configuration
   - Define per-use-case endpoints: READ_PRIMARY, READ_CACHE, WRITE_TX, WEBSOCKET.
   - Store in env with rotation ability; never hardcode keys in client bundles.
3) Client resilience
   - Implement health checks (ping, slot distance, error rate); auto-failover when thresholds breached.
   - Use request hedging for latency-sensitive reads (send to two, pick fastest) with caps.
   - For writes: add priority fees and preflight; on BlockhashNotFound or NodeBehind, refresh blockhash and retry to another endpoint.
4) Performance controls
   - Batch RPC calls (getMultipleAccounts, getProgramAccounts with filters) instead of per-account fetches.
   - Cache layer (CDN/kv) for idempotent reads; invalidate on slot interval.
   - Use ALTs for tx with many accounts to reduce size + retries.
5) Cost management
   - Track request volume per method; throttle noisy endpoints; move polling to webhooks/WS where cheaper.
   - Compress/trim logs; prefer enhanced APIs when they reduce query count.
6) Monitoring & alerting
   - Metrics: p50/p95 latency, error codes (429, -32005), slot lag, WebSocket drop rate.
   - Alerts with runbooks: switch to fallback, raise priority fee, reduce polling.

## Templates / Playbooks
- Health check thresholds: error rate >3% or slot lag >30 slots for 2 mins -> failover.
- Retry policy example: max 3 attempts; backoff 200ms * 2^n with jitter; switch provider after first rate-limit.
- Env layout:
  - RPC_READ_PRIMARY=https://...
  - RPC_READ_FALLBACK=https://...
  - RPC_WRITE=https://...
  - RPC_WS=wss://...
- Cost quick estimate: requests/day * price per 1M / 1,000,000.

## Common Failure Modes + Debugging
- 429 / rate limit: reduce concurrency, add caching, switch endpoint tier.
- Stale blockhash causing tx drop: refresh via getLatestBlockhash with commitment; add priority fee.
- Slot lag on provider: monitor; switch read path; avoid mixing commitments across providers if lagging.
- WebSocket disconnect loops: implement heartbeat + auto-resubscribe with backoff.
- API key leaked in frontend: proxy writes through backend; rotate keys; monitor referrers.

## Quality Bar / Validation
- Config includes at least primary + one fallback with health logic.
- Timeouts and retries defined per operation type; no infinite retries.
- Metrics/alerts wired with documented thresholds.
- Keys not exposed in client bundles; env documented.
- Load test or simulation shows graceful degradation under throttling.

## Output Format
Return:
- Provider comparison table + chosen stack
- Endpoint map (read/write/ws) with commitments and timeouts
- Retry/failover policy description
- Monitoring plan with metrics + alert thresholds
- Cost estimate and knobs to stay within budget

## Examples
- Simple: Frontend-only meme site
  - Read-only endpoint via public RPC; cached responses; writes proxied to single paid endpoint; fallback public RPC for reads; minimal telemetry.
- Complex: High-volume trading bot + dApp
  - Primary paid provider with priority fees; secondary provider for hedged reads; ALTs for large tx; WebSocket stream with heartbeats; caching layer reduces getAccountInfo spam; alerts on slot lag and 429s; monthly budget forecast with throttle switches.