---
name: launch-readiness-checklist
description: End-to-end pre-flight checklist for launching a Solana token/app: infra, wallets, liquidity, comms, security, and rollback planning. Use before mainnet launch or major release.
---

# Launch Readiness Checklist

Role framing: You are a Solana launch operator. Your goal is to verify the build, infra, liquidity, and comms are ready, with clear abort criteria.

## Initial Assessment
- Launch scope: token only, dApp, or both? What chain (mainnet/devnet)?
- Timeline and freeze window? Who is on-call? War room comms channel?
- Dependency map: RPC providers, indexer, bots, multisigs, token accounts funded?
- Liquidity plan: AMM/DEX target, initial LP size, pricing strategy, custody of LP keys?
- Security posture: audits? known risks? mitigations? kill-switches?
- Comms plan: announcement assets ready? FAQs? status page? pinned message?
- Rollback plan: what conditions trigger pause/abort? who decides?

## Core Principles
- Single source of truth: maintain a shared checklist with owners + timestamps.
- Dry-run everything on devnet with same scripts and signer paths.
- Minimize secret sprawl: hardware wallets/multisigs for critical steps; no ad-hoc key exports.
- Observability first: logs/alerts live before launch; know what "healthy" looks like.
- Explicit go/no-go gates with authority to stop.

## Workflow (Go/No-Go)
1) Environment lock-in
   - Confirm program IDs, mints, addresses; pin versions of CLI, Anchor, SDK.
2) Infra validation
   - RPC primary + fallback tested; rate-limit expectations documented; health alerts set.
   - Indexer/webhook endpoints returning expected data; backfill complete.
3) Program + token state
   - Deployments verified (slot, txid); upgrade authority holder documented; immutability decision recorded.
   - Token authorities set per plan; ATAs funded; metadata live.
4) Liquidity + markets
   - Create LP positions/whirlpools/raydium pools with scripted tx; record txids; test swaps for slippage and price impact.
   - Set anti-sniper params if used (delays, caps) and document rationale.
5) Frontend + bots
   - Wallet connect/sign flows tested on target wallets (Phantom, Solflare, Backpack); error banners show meaningful copy.
   - Monitoring/alert bots running (RPC health, tx fail rate, pool events) with safe output formatting.
6) Security + keys
   - Multisig thresholds confirmed; signers reachable; hardware wallets charged.
   - Secrets stored; no private keys on CI logs; revocation paths rehearsed.
7) Comms + legal
   - Announcement thread/pinned messages ready; risk disclosures clear; support channel staffed.
   - Status page or fallback broadcast plan defined.
8) Final go/no-go
   - Run tabletop: simulate fail cases (RPC down, swap revert, UI 500, bot spam).
   - Decision meeting: record go/no-go with timestamp and approvers.

## Templates / Playbooks
- Checklist table: item | owner | status | proof (link/txid) | timestamp
- War room runbook: channels, who can page whom, escalation ladder, decision authority.
- Rollback triggers: e.g., RPC error rate > X, pool imbalance > Y, critical bug -> pause frontends + halt mint/LP adds.
- Comms pack: launch thread outline, FAQ (fees, risks, contract addresses), pinned TG/Discord message, block explorers links.

## Common Failure Modes + Debugging
- RPC rate limits -> tx stuck: switch to fallback, enable priority fees, reduce burst.
- Wrong mint/program IDs in frontend: verify env files, redeploy configs, clear cache.
- Liquidity mispriced: redo pool with correct initial price; communicate clearly; consider closing bad LP and recreating.
- Missing signer for critical step (multisig offline): have standby signer; reschedule if quorum fails.
- Bots spamming or leaking secrets: enforce logging redaction; rate limit; rotate keys.

## Quality Bar / Validation
- Every checklist item has owner, status, evidence link/txid, and timestamp.
- Dry-run recorded on devnet with same scripts.
- Fallbacks tested once (RPC, CDN, indexer, bots).
- Comms assets reviewed by at least two people; addresses consistent across artifacts.
- Explicit go/no-go record stored in output.

## Output Format
Deliver a launch packet containing:
- Context summary (scope, date/time in UTC, teams on-call)
- Completed checklist table
- Address registry (program IDs, mints, pools, treasuries)
- Fallback matrix (RPC, indexer, bots, comms)
- Go/No-Go decision log with approvers and timestamp
- Risks + rollback triggers

## Examples
- Simple: Token-only fair launch with Raydium pool
  - Devnet dry-run of mint + pool create; authorities revoked per plan; announcement pinned; go at 18:00 UTC; fallback RPC tested.
- Complex: dApp + token with multisig upgrade and bots
  - Programs deployed immutably; mint authority PDA retained for emissions; Orca Whirlpool seeded; monitoring bots streaming to PagerDuty; frontend toggles maintenance mode flag; rollback triggers defined for pool imbalance and RPC failure; go/no-go logged.