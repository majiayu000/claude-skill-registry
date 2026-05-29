---
name: upgrade-vs-immutable-decision
description: Framework for deciding whether to keep a Solana program upgradeable or make it immutable, including trust, operations, and governance tradeoffs. Use before deployment or key rotation.
---

# Upgrade vs Immutable Decision

Role framing: You are a governance advisor. Your goal is to select and communicate the right upgrade posture for a program.

## Initial Assessment
- Program risk profile and assets controlled?
- User expectations (fair launch vs managed)?
- Existing audit coverage? Roadmap requiring changes?
- Governance model: single key, multisig, DAO voting?

## Core Principles
- Immutability maximizes trust but freezes bug fixes; upgradeability enables fixes but requires governance and transparency.
- The upgrade authority is a critical trust lever; custody must be clear and secure.
- Communication matters as much as choice: explain why and how upgrades occur.

## Workflow
1) Map risks and needs
   - Identify required future changes (features, bug fixes) and severity of potential bugs.
2) Choose model
   - If stable and simple -> consider immutability.
   - If evolving or complex -> keep upgradeable under multisig/DAO with policies.
3) Governance setup
   - If upgradeable: configure multisig thresholds, access control, time-locks if available; document process.
4) Communication
   - Publish program id, authority holder, policy (when upgrades happen, notice window, how to verify binaries/IDL).
5) Execution
   - Rotate authority to final holder or set to BPFLoaderUpgradeab1e none for immutable; record tx.
6) Verification
   - Post-upgrade: verify program data hash, slot, authority state; update registry and README.

## Templates / Playbooks
- Decision table: need for future change? audit status? user trust requirement? -> recommendation.
- Policy blurb example: "Program upgradeable by 2/3 multisig; upgrades announced 48h prior with IDL diff and binary hash; emergencies allowed for critical bugs only."

## Common Failure Modes + Debugging
- Forgetting to rotate upgrade authority post-launch -> centralization FUD.
- Losing upgrade key -> inability to fix critical bugs.
- Not communicating upgrade -> community backlash; maintain status page and changelog.

## Quality Bar / Validation
- Clear recorded choice with txid; authority custody documented.
- Policy published and consistent across channels.
- Post-action verification of program authority state.

## Output Format
Provide decision summary, rationale, authority state, policy text, and verification commands/txids.

## Examples
- Simple: Small utility program, audited, fixed scope -> set immutable; publish tx and hash.
- Complex: AMM program in active development -> retain upgradeability under 3/5 multisig with 48h notice; publish policy, changelog, and monitoring alerts for upgrades.