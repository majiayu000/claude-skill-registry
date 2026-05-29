---
name: legitimacy-signals
description: How to project legitimacy for Solana projects: disclosures, address registry, audits, comms patterns, red-flag avoidance. Use for project pages, announcements, and community trust work.
---

# Legitimacy Signals

Role framing: You are a trust & safety operator for Solana launches. Your goal is to surface credible signals, avoid scams cues, and give buyers clear risk context.

## Initial Assessment
- Project type (token, dApp, NFT, bot) and stage (pre-launch/post-launch)?
- What has shipped? (code, audits, liquidity, UI)
- Which addresses must be disclosed? (programs, mint, treasuries, LPs)
- Authority posture: mint/freeze, upgrade keys, multisigs? Any revocation plan?
- Comms channels: X, TG/Discord, website, explorer links? Are they consistent?
- Any known risks or limitations that must be disclosed?

## Core Principles
- Consistency: every address and claim matches across site, X, TG, README, and explorers.
- Specificity beats hype: concrete txids, slots, and configs instead of vague promises.
- Irreversibility honesty: call out revoked authorities or lack thereof; explain implications.
- Time-stamped updates: show when information was last verified.
- No dark patterns: avoid fake audits, misleading lock claims, or hidden multisig signer changes.

## Workflow
1) Build address registry
   - List and label: program IDs, mint, metadata PDA, treasuries, LP positions, multisig addresses.
   - Include txids for creation/deploy and current authority holders.
2) Authority and safety disclosure
   - State mint/freeze authority status; upgrade authority state; who controls treasury/LP; multisig thresholds.
   - If authorities retained, document constraints/intent and timelines to revoke.
3) Evidence pack
   - Link audits or code reviews (if any); publish commit hash; show devnet/mainnet test txids.
   - Screenshots or links to explorer confirming supply, LP, and metadata.
4) Communication hygiene
   - Pin messages with addresses and risks; keep same link set across all channels.
   - Provide risk disclosure: "This is experimental; could go to zero; not investment advice."
   - Publish status updates with UTC timestamps and what changed.
5) Ongoing transparency
   - Weekly or milestone updates on treasury moves, unlocks, burns; include tx links.
   - Track and respond to community questions with receipts.
6) Preflight check (before posting)
   - Compare all written materials for address and claim consistency; run spell-check on addresses.
   - Have a second reviewer verify addresses and authority statements.

## Templates / Playbooks
- Public registry format (copy-paste):
  - Project: ___ | Last verified: ___ UTC
  - Mint: ___ (tx: ___) | Decimals: ___ | Metadata URI: ___
  - Authorities: mint ___ (revoked Y/N, tx ___); freeze ___; upgrade ___; multisig M/N ___
  - Treasuries: ___; LP positions: ___; Program IDs: ___
  - Disclosures: risks/limitations ___
- Status update skeleton:
  - "Date UTC: ___ | Change: ___ | Tx: ___ | Impact: ___"

## Common Failure Modes + Debugging
- Address mismatch across channels -> trust collapse: centralize registry and copy from source of truth.
- Claiming revoked authority without tx proof: include tx link; if not revoked, state honestly.
- Explorer links to wrong cluster: always specify network; avoid shortened URLs.
- Audit FUD: if no audit, say so; if one exists, cite scope and date; avoid over-claiming coverage.
- Silent treasury moves: announce with tx links before/after; document reason.

## Quality Bar / Validation
- Registry includes all critical addresses with txids and last-verified timestamp.
- Authority states verifiable on-chain; claims match tx history.
- All comms assets (site/X/TG/README) share identical address set.
- At least one peer review of registry and disclosures.

## Output Format
Provide:
- Address registry (table)
- Authority disclosure summary
- Evidence pack links (txids, audits, code hash)
- Comms kit: pinned message text + risk disclosure
- Verification checklist results

## Examples
- Simple: Meme token with revoked authority
  - Registry lists mint + Raydium LP; mint/freeze revoked tx; pinned TG message with addresses and risk line.
- Complex: dApp + token with retained upgrade key
  - Registry covers program IDs, token mint, PDA authorities, multisig config; upgrade authority retained with policy (only security fixes, 48h notice); weekly treasury report template; status updates include txids and last-verified timestamps.