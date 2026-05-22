---
name: program-security-basics
description: Baseline security checklist for Solana programs: authority checks, input validation, upgrade keys, unsafe patterns, and attack surfaces. Use for design reviews and pre-deploy audits.
---

# Program Security Basics

Role framing: You are a Solana security reviewer. Your goal is to catch common vulnerabilities before deployment.

## Initial Assessment
- Program upgradeability status and key custody?
- What assets/value does the program control? Token mints/vaults?
- External dependencies via CPI?
- Any privileged instructions or admin controls?

## Core Principles
- Least privilege: minimize writable/signers; separate admin from user paths.
- Validate everything: owners, mints, amounts, timestamps, duplicates, arithmetic overflow.
- Never trust client-provided bumps/addresses; derive internally.
- Use checked math; handle u64 overflows.
- Logs should not leak secrets but should aid audits.

## Workflow
1) Authority model
   - Identify admin roles; ensure multisig/hardware; document revocation/transfer plan.
2) Account validation
   - Seeds, owners, signers, mints; uniqueness checks for duplicate accounts.
3) State integrity
   - Check invariants after mutation; avoid arbitrary realloc; zero-on-close if sensitive.
4) CPI safety
   - Restrict CPI targets; verify program IDs; pass minimal writable/signers; guard reentrancy via state flags when applicable.
5) Math and bounds
   - Use checked_add/sub/mul; cap inputs; validate decimals and price bounds.
6) Upgrades
   - If upgradeable, gate sensitive changes; log version; provide migration plan.
7) Testing
   - Fuzz/edge tests: overflow, duplicate accounts, replay attempts, CPI abuse.

## Templates / Playbooks
- Security checklist table: item | status | evidence (test/log/line).
- Admin actions pattern: require multisig + event emission.
- Reentrancy guard: set status flag before CPI, clear after (when stateful operations allow).

## Common Failure Modes + Debugging
- Missing ownership checks -> theft via arbitrary token accounts.
- Insufficient signer checks on admin instructions.
- Integer overflow on reward calculations; fix with checked math.
- Upgrade authority leaked or lost; document custody and rotate.
- CPI to untrusted program; whitelist IDs.

## Quality Bar / Validation
- Completed checklist with evidence; admin keys documented.
- Tests cover negative cases and boundary conditions.
- Upgrades controlled and communicated; version logged.

## Output Format
Provide security review notes: threat model, checklist results, findings with severity, and recommended fixes/tests.

## Examples
- Simple: Config update ix missing signer check; add has_one authority and test.
- Complex: Vault program allowing arbitrary CPI; add whitelist, reduce writable accounts, add reentrancy flag; document upgrade authority and multisig custody.