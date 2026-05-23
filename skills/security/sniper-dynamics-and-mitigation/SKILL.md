---
name: sniper-dynamics-and-mitigation
description: Understand sniper bots in Solana launches and implement defensive measures without harming fair access. Use before token or LP go-live.
---

# Sniper Dynamics and Mitigation

Role framing: You are a launch defender. Your goal is to anticipate sniper behavior and mitigate harm while staying fair.

## Initial Assessment
- Launch mechanism (mint, LP go-live, auction)?
- Time of launch and publicity level?
- Infrastructure: RPC capacity, rate limits, bot detection available?
- Tolerance for delays or caps?

## Core Principles
- Snipers exploit speed and predictable times; randomness and caps reduce edge.
- Defenses must not break legitimate users.
- Publish rules clearly; avoid hidden blocklists where possible.

## Workflow
1) Threat model
   - Identify likely bot vectors: pre-announced time, predictable tx, mempool monitoring.
2) Choose mitigations
   - Options: per-wallet caps, staggered windows, randomized start within small window, delayed LP trading, higher fees first block, allowlist/raffle.
3) Technical controls
   - RPC rate limits per IP/API key; captcha on UI; proof-of-work or queue.
   - Monitor mempool/logs for bursts; auto-pausing if error rate spikes.
4) Execution
   - Implement in UI + backend; test with bot-like scripts on devnet.
5) Communication
   - State mitigations and rationale; publish what is allowed; avoid surprise blocks.
6) Post-launch response
   - Track top buyers; if overwhelming, consider additional liquidity or caps for future drops; share data transparently.

## Templates / Playbooks
- Launch window plan: e.g., 5-minute randomized start within 30-minute window.
- Cap policy: max X tokens per wallet for first Y minutes; enforced on-chain or via UI + backend validation.
- Monitoring dashboard: tx success rate, unique wallets, top buyers, RPC errors.

## Common Failure Modes + Debugging
- Over-aggressive filters blocking real users: test on varied devices; provide fallback path.
- Mitigations only in UI; bots hit RPC directly: enforce on-chain when possible.
- Randomized start without communicating window -> confusion; be explicit.
- Snipers bypass caps via multiple wallets: acknowledge limitation; monitor and publish stats.

## Quality Bar / Validation
- Mitigations implemented and tested; false-positive rate low.
- Rules published pre-launch with clear timelines.
- Monitoring active during launch; post-mortem produced if bots dominate.

## Output Format
Provide threat model, chosen mitigations, implementation notes, comms copy, and monitoring plan.

## Examples
- Simple: Per-wallet cap 1 mint, captcha on UI, randomized start within 10 minutes; post stats showing distribution.
- Complex: LP go-live with delayed trading 2 minutes, API rate limits, bot watch dashboard, and fallback RPC; publish post-launch report on top wallets and mitigation effectiveness.