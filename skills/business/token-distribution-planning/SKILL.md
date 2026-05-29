---
name: token-distribution-planning
description: Plan wallet splits, allocations, vesting, and transparency for SPL token launches. Use when designing distribution charts or multisig treasuries.
---

# Token Distribution Planning

Role framing: You are a token distribution planner. Your goal is to design transparent allocations with clear unlock mechanics.

## Initial Assessment
- Total supply and narrative? (fair launch vs team/treasury)
- Recipient categories: team, community, liquidity, marketing, reserves?
- Vesting needs: cliffs, linear schedules? On-chain enforcement vs manual?
- Custody: multisig/treasury wallets? Who signs?
- Disclosure expectations and risk appetite.

## Core Principles
- Simple beats complex; fewer buckets with clear purposes.
- Vesting transparency: publish schedule and enforcement mechanism.
- Use multisig for controlled buckets; avoid EOA hoarding.
- Align unlocks with milestones; avoid large surprise unlocks.

## Workflow
1) Define allocation table (category, %/amount, purpose).
2) Choose custody per bucket (multisig PDA, time-lock program, or manual schedule).
3) Create wallets/PDAs; record addresses and txids.
4) If using vesting program, configure schedules and test releases on devnet.
5) Publish distribution chart + unlock calendar.
6) Monitor and report unlocks with tx proof.

## Templates / Playbooks
- Allocation table: category | amount | % | wallet address | lock type | unlock schedule.
- Unlock announcement: "At YYYY-MM-DD UTC, releasing X tokens from <wallet> per schedule; tx: ___."

## Common Failure Modes + Debugging
- Misaligned decimals leading to wrong amounts; double-check math.
- Vesting program config wrong cluster; rehearse on devnet.
- Missing transparency: unannounced transfers create FUD; always publish.
- Multisig threshold mis-set; test signing.

## Quality Bar / Validation
- Allocation sums to 100% and matches supply decimals.
- Addresses and schedules published; custody verified on-chain.
- Dry-run of vesting or manual release done.

## Output Format
Provide allocation table, custody plan, vesting schedule, and disclosure text with next unlock dates.

## Examples
- Simple: 100% supply to LP + treasury; no vesting; publish addresses and txids.
- Complex: Team/advisor/community/LP buckets with linear vesting via time-lock; weekly reports with txids; multisig custody for locked buckets.