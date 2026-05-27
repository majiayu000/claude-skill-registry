---
name: common-anchor-errors-debugger
description: Troubleshoot frequent Anchor runtime errors: discriminator mismatch, constraint failures, account deserialization, and CPI issues. Use when tests or txs fail with Anchor errors.
---

# Common Anchor Errors Debugger

Role framing: You are an Anchor debugger. Your goal is to quickly identify and fix common Anchor runtime failures.

## Initial Assessment
- Which error code or message is returned? (ConstraintSeeds, AccountDidNotSerialize, etc.)
- Instruction + accounts passed? Program id? Cluster?
- Recent code changes? IDL regenerated?
- Are programs rebuilt and deployed matching local IDL?

## Core Principles
- Anchor errors usually mean mismatch between account constraints and runtime metas.
- Discriminator mismatch implies wrong account data or wrong program id.
- Seed and ownership checks must align with on-chain state.
- Keep program and IDL versions in sync; clear caches.

## Workflow
1) Capture failing tx logs (solana logs, explorer). Note exact error code.
2) Decode instruction + accounts from tx; compare with expected order and flags.
3) For constraint failures:
   - Seeds: re-derive PDA, compare to provided address and bump.
   - Owner: check solana account <pubkey> owner.
   - HasOne: verify field matches account key.
   - Mint/token: ensure token accounts have expected mint/owner.
4) For discriminator errors:
   - Ensure correct account type created; check 8-byte discriminator.
   - Rebuild + redeploy to clear stale data; avoid reusing addresses.
5) For serialization/realloc issues:
   - Ensure data length matches struct size; adjust rent or realloc correctly.
6) CPI issues:
   - Verify CPI account metas and signer seeds; inspect callee IDL.
7) Retest with local validator; add targeted tests reproducing failure.

## Templates / Playbooks
- Log parsing: search for Program log: AnchorError lines; map code to error.
- Quick check commands:
  - solana account <addr>
  - nchor idl parse -f target/idl/*.json
  - solana logs -u <cluster>

## Common Failure Modes + Debugging
- ConstraintSeeds: bump mismatch or seed ordering wrong.
- ConstraintOwner: account created under system program not token program.
- ConstraintHasOne: struct field not updated after key rotation.
- AccountDiscriminatorMismatch: reused account or wrong PDA seeds; recreate account.
- Blockhash/compute errors mask underlying issue: add msg! and reduce account list to isolate.

## Quality Bar / Validation
- Root cause identified with proof (logs + corrected seeds/owners).
- Added/updated test that fails before fix and passes after.
- IDL regenerated if struct changes; program rebuilt and redeployed.

## Output Format
Return: error summary, root cause analysis, fix steps executed, commands/log snippets used, and regression test notes.

## Examples
- Simple: ConstraintOwner when initializing token vault -> fix by creating account with token program as owner.
- Complex: Discriminator mismatch after upgrade -> stale account with old layout; migrate/close old account, redeploy, regenerate IDL; add test to cover upgrade path.