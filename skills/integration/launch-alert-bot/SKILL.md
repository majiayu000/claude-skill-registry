---
name: launch-alert-bot
description: Build a bot that detects new Solana launches (mints/LPs) and sends safe alerts. Use for discovery and monitoring without shilling scams.
---

# Launch Alert Bot

Role framing: You are a discovery bot operator. Your goal is to surface new launches with context while avoiding amplification of scams.

## Initial Assessment
- Data feeds (Helius token registry events, DEX pool creations, metadata updates)?
- Alert channels and audience? (public vs internal)
- Filters (min liquidity, authority revoked, verified creators)?
- Latency tolerance?

## Core Principles
- Prioritize safety: include risk flags and avoid implicit endorsements.
- Deduplicate across feeds; avoid double alerts for same mint/pool.
- Provide verifiable data: addresses, txids, authority states.

## Workflow
1) Source selection
   - Monitor pool creation events, new mints with metadata, social signals if desired.
2) Filtering and scoring
   - Apply thresholds: liquidity >= X, metadata exists, mint/freeze authority status, creator whitelist/blacklist.
3) Enrichment
   - Fetch metadata, authority info, initial LP stats; compute simple risk score.
4) Alerting
   - Message with mint/pool addresses, tx link, risk flags (authority retained? low LP? unknown metadata). Include "not financial advice".
5) Operations
   - Deduplicate by mint/pool; throttle; monitor error rates.

## Templates / Playbooks
- Alert template: "New pool detected: <mint> on <DEX> at slot <slot>. LP: . Mint authority: revoked/active. Risk flags: ... (tx link)."
- Risk score rubric: authority (revoked=+1 safe, active=-1), LP depth, metadata completeness, blacklist hit.

## Common Failure Modes + Debugging
- False positives from testnet/devnet: filter by cluster.
- Spam/scam alerts: strengthen filters, add manual review mode.
- Rate limits on data providers: cache and backoff.
- Metadata fetch failures: retry and mark partial info.

## Quality Bar / Validation
- Filters tuned to reduce noise; risk flags included.
- No duplicate alerts for same event.
- Clear disclaimer and source links in every alert.

## Output Format
Provide source list, filter rules, risk rubric, alert format, and ops checklist.

## Examples
- Simple: Internal bot watching Raydium pools > liquidity; alerts to Slack with authority status.
- Complex: Public bot combining pool events + social mentions; risk scoring; manual approve queue; sends to X/TG with safe copy and throttling.