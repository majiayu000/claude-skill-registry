---
name: token-authority-and-risk
description: Evaluate and configure SPL token authorities (mint/freeze/close) with risk implications and best practices. Use for audits, rotations, or disclosures.
---

# Token Authority and Risk

Role framing: You are a token governance reviewer. Your goal is to set or evaluate authorities so holders understand control and risk.

## Initial Assessment
- Current authority holders for mint/freeze/close? Custody method?
- Supply policy: fixed, capped, or inflationary?
- Any programmatic emissions or burns planned?
- Communication commitments about revocation?

## Core Principles
- Mint authority = inflation lever; freeze authority = censorship lever; close authority = account reclaim lever.
- Multisig/PDA > single hot wallet; publish custody.
- If claiming revocation, execute on-chain and cite tx.
- Align authority posture with narrative (fair launch vs managed).

## Workflow
1) Inventory authorities using spl-token account-info and explorer.
2) Decide posture: revoke, rotate to multisig/PDA, or keep with policy.
3) Execute changes: spl-token authorize ... for mint/freeze; ensure payer funds.
4) Document and disclose: addresses, txids, rationale, timelines.
5) Monitor: set alerts on authority changes and large mints/burns.

## Templates / Playbooks
- Risk disclosure snippet: "Mint authority held by 2/3 multisig for planned emissions; no freeze authority; policy: max 2% monthly with 24h notice."
- Authority log table: authority type | holder | action (keep/rotate/revoke) | txid | timestamp.

## Common Failure Modes + Debugging
- Forgetting to update metadata after rotation; refresh explorers.
- Leaving freeze authority active unintentionally -> blocked transfers.
- Multisig missing signer availability -> stuck rotation.
- PDA authority without signer seeds path -> cannot mint; store seeds + bump.

## Quality Bar / Validation
- Final authority state matches stated policy; txids recorded.
- Disclosure published; holders can verify on-chain.
- Alerts in place for authority or supply changes.

## Output Format
Provide authority audit summary, actions taken/needed, txids, and disclosure text.

## Examples
- Simple: Fixed-supply meme token -> revoke mint/freeze; publish txids.
- Complex: Emission token -> mint authority PDA controlled by program; freeze none; multisig controls program upgrade; disclosures include seeds and policy caps.