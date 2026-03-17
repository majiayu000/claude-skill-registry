---
name: aiken-dex-security-audit
description: Adversarial security audit playbook for Plutus V3 Aiken DEX contracts (threat model, invariants, findings, tests, tx repro shapes).
metadata:
  domain: cardano
  language: aiken
  category: security-audit
---

# aiken-dex-security-audit

## When to use

- Auditing Plutus V3 Aiken contracts for a DEX (validators + minting policies)
- You need a rigorous report: threat model, invariants, findings, and reproducible exploit tx shapes

## Non-negotiable rules

- No hallucinations. If something isn't in the repo or inputs, say **unknown** and list exactly what's missing.
- Assume a hostile attacker can craft arbitrary transactions: multi-input, multi-action, weird datums, weird token bundles.
- Never ask for or handle seed phrases / private keys.
- Prefer evidence over vibes: minimal tx shape + failing test + fix + passing test.

## Required inputs (ask for anything missing)

1. Script list + purpose (spend/mint/reward/cert) and which are critical path for swaps/liquidity
2. Datum/redeemer schemas (Aiken types + encoding expectations)
3. Parameters/config: policy IDs, script hashes, upgrade/admin controls, oracle deps (if any)
4. Off-chain tx builder(s) in scope (where swaps/liquidity txs are constructed)
5. Network assumptions (mainnet/preprod) + constraints (tx size, exunits, reference scripts, inline datums)

## Audit workflow (do ALL)

1. Build a system model
   - Map state UTxOs, assets, script addresses, and transitions (inputs/outputs/mint/burn/signees/time).
2. Extract explicit invariants (testable)
   - Value conservation, LP supply rules, fee bounds/rounding, auth rules, "exactly-one state UTxO", bounded datum/value growth.
3. Threat model & attack surface
   - Attacker capabilities in eUTxO; trusted roles; upgrade/emergency keys; oracles; economic/griefing vectors.
4. Manual on-chain review
   - For each validator/policy branch: what must be true about inputs/outputs/minted/signers/time?
   - Hunt: double satisfaction, fake-state UTxOs, asset-class mismatches, optional datum gotchas, unbounded growth, time-range bugs, division/rounding/negative amounts, "exactly one" enforcement bugs.
   - For each issue: minimal exploitable tx shape + why it works (use tx-shapes template).
5. Off-chain review (if in scope)
   - Ensure builder cannot construct valid-but-unsafe txs or mis-hash datums or mis-handle mint fields.
6. Evidence suite (Aiken-first)
   - Add unit tests + property tests for each invariant + each exploit regression test.
7. Budget & DoS analysis
   - Identify evaluation hotspots and griefing paths; recommend safe refactors.
8. Report
   - Use `templates/audit-report.md` and include: scope, assumptions, invariants, findings table, patches, tests, deployment checklist.

## Files to use

- Full framework prompt: `references/audit-framework.md`
- Report template: `templates/audit-report.md`
- Invariants checklist: `templates/invariants-checklist.md`
- Minimal exploit tx shapes: `templates/tx-shapes.md`
