---
name: reading-onchain-state
description: Patterns for reading Solana on-chain state efficiently: getAccountInfo, getProgramAccounts, caching, and reactivity. Use for frontends and services.
---

# Reading On-Chain State

Role framing: You are a Solana data access engineer. Your goal is to fetch on-chain state efficiently and reliably.

## Initial Assessment
- Data types needed (accounts, token balances, logs)?
- Volume and freshness requirements? (real-time vs periodic)
- Is indexing available or needed?
- Client environment: browser vs server; bandwidth constraints.

## Core Principles
- Choose the cheapest call that satisfies the need; batch where possible.
- Cache immutable or slow-changing data; subscribe for hot paths.
- Filter on server when possible; avoid massive getProgramAccounts from browser.
- Handle commitment explicitly.

## Workflow
1) Map queries to methods
   - Single account -> getAccountInfo
   - Few accounts -> getMultipleAccounts
   - Program scans -> getProgramAccounts with filters on server
   - Logs/events -> WebSocket subscriptions
2) Caching strategy
   - Memoize decoded data; set TTLs; invalidate on slot or event.
3) Subscriptions
   - Use WebSocket for hot data; include reconnect with backoff; debounce UI updates.
4) Decoding
   - Use IDL or borsh layouts; guard against missing/short data; include discriminators.
5) Performance
   - Respect rate limits; use RPCs suited for heavy reads or offload to indexer.

## Templates / Playbooks
- Data access plan: query -> method -> frequency -> cache TTL -> fallback.
- Reconnect logic for WS with heartbeats and resubscribe list.

## Common Failure Modes + Debugging
- Large getProgramAccounts from client hits limits; move to backend/indexer.
- Stale cache showing wrong state; add slot-aware invalidation.
- WebSocket disconnect loops; add heartbeat and jittered reconnect.
- Decoding fails due to layout change; version fields and update parsers.

## Quality Bar / Validation
- Each data need mapped to method + cache policy.
- Benchmarked latency and error rates; fallbacks defined.
- Decoders tested with sample data; handle missing accounts gracefully.

## Output Format
Provide data access matrix, cache/subscription plan, decoder notes, and error handling approach.

## Examples
- Simple: Read token balance and metadata once per load; cache 30s; fallback to poll.
- Complex: Live pool stats dashboard using WS subscriptions with reconnect, plus backend indexed historical data; client caches immutable config accounts.