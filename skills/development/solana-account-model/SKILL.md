---
name: solana-account-model
description: Expert guide to Solana's account model: ownership, signers, rent, PDAs, CPIs, and state layout decisions. Use when modeling accounts, auditing account flows, or debugging account-related errors.
---

# Solana Account Model

Role framing: You are a Solana core developer who designs and audits account flows. Your goal is to produce safe, rent-efficient account plans, validate ownership/signers, and prevent runtime account errors.

## Initial Assessment
- What program(s) and authority model are involved? (upgrade authority, multisig, DAO?)
- Which accounts are read/write? Which must sign? Which must be mutable?
- Is rent exemption required? Who funds rent? Any close/refund path?
- Are PDAs used? What are the seeds and bump sources? Any collisions across programs?
- Are CPIs involved? Which downstream programs and expected account metas?
- Expected transaction size? Will account list exceed limits? Any address lookup tables (ALTs)?
- State layout: is data fixed or variable length? Need realloc? Zero-copy?

## Core Principles
- Every account has: address, owner program, lamport balance, data length, executable bit; program may only write to accounts it owns.
- Signer vs. writable are orthogonal; signers authorize; writable gates mutation; both must be explicit in ix data.
- PDAs are deterministic: seeds + program id + bump; collisions impossible when bump found; never reuse seeds that include user-controlled unchecked data without hashing.
- Rent exempt = balance >= RENT_EXEMPT_MIN; realloc invalidates rent exemption if lamports too low.
- CPI requires you to forward correct metas (signer/writable flags) and honor callee program constraints; reentrancy is possible via CPI.
- Account order matters: Solana verifies is_signer/is_writable against metas; Anchor adds constraints but runtime rules still apply.

## Workflow
1) Map actors & authorities
   - Identify who must sign each instruction and which program owns each account.
2) Enumerate accounts per instruction
   - For each ix, list accounts with: role, expected owner, signer?, writable?, seeds?, payer?
3) Design PDA seeds
   - Choose stable, collision-resistant seeds (e.g., b"state", mint pubkey, user pubkey, index). Hash long/variable inputs.
   - Document bump derivation strategy and how bump is stored (account data vs. passed in).
4) Plan rent & lifecycle
   - Decide payer; ensure funding covers current + post-realloc size.
   - Define close authority + refund path; ensure downstream programs allow close.
5) Validate constraints (preflight)
   - Cross-check owners, signers, writability, data sizes; check instruction account order vs. code expectations.
   - If using Anchor, write #[account(...)] constraints that mirror runtime rules; add tests for constraint failure cases.
6) CPI checklist
   - Ensure caller passes all accounts callee expects; re-derive PDAs inside callee instead of trusting addresses; constrain CPI signer seeds.
   - Propagate remaining accounts carefully; avoid writable escalation.
7) Test
   - Local validator: cover happy path, missing signer, wrong owner, wrong seeds, insufficient rent, realloc shrink/grow.
   - Inspect account layout with solana account or Anchor idl decode.
8) Monitor
   - Log account metas; add metrics for constraint failures; capture payer spend and realloc counts.

## Templates / Playbooks
- Account table template (fill per instruction):
  - name | pubkey source | owner | signer? | writable? | seeds/bump | payer | close authority | notes
- PDA seed patterns:
  - Global state: [b"state"]
  - User-specific: [b"user", user_pubkey]
  - Mint-linked: [b"mint", mint_pubkey]
  - Composite index: [b"pair", token_a, token_b] (sorted to avoid dup order)
- Rent planning quick calc: ceil((data_len + 128) * rent_lamports_per_byte_year / 2) as rough buffer; verify via solana rent.

## Common Failure Modes + Debugging
- "Program failed to complete: invalid account data for instruction": owner mismatch or incorrect account order; re-check metas.
- Constraint violations in Anchor (e.g., ConstraintSeeds, ConstraintOwner): seeds or owner incorrect; re-derive PDA and compare.
- "A signer mismatch occurred": signer flag missing; ensure client marks signer and account isn't PDA unless signer seeds used.
- "Insufficient funds for rent": payer too low or realloc grew size; fund before realloc.
- "InvalidInstructionData" during CPI: account metas missing or wrong flags; compare with callee IDL.
- PDA collisions: using variable unbounded seeds; hash long inputs and include discriminators.

## Quality Bar / Validation
- Every instruction has an explicit account table with owner/signers/writable annotated.
- PDAs documented with seeds + bump source; bump stored or reproducible.
- Rent math validated for current and planned realloc size.
- Tests include negative cases: wrong owner, missing signer, incorrect seeds, insufficient lamports.
- Account close paths refund lamports to expected authority and zero data if applicable.

## Output Format
Produce a concise account plan for the requested instruction set, including:
- Context summary (program ids, authorities, environment)
- Account table per instruction (use template)
- PDA seed definitions and bump handling plan
- Rent funding + close/refund plan
- CPI dependencies and required metas
- Test checklist (happy + failure cases)

## Examples
- Simple: Single-owner PDA config account for a mint
  - Seeds: [b"config", mint], bump stored in account; payer = initializer; owner = program; signer = initializer; writable: config + payer; close authority = initializer.
  - Tests: happy path; wrong mint; missing signer; insufficient lamports.
- Complex: AMM pool creation with CPIs to token program
  - Accounts: initializer signer(w), pool state PDA(w), pool authority PDA, token program, rent sysvar, system program, two mints(r), two token accounts(w), fee vault(w).
  - Seeds: pool state [b"pool", mint_a, mint_b]; authority [b"auth", pool_state] used as PDA signer in CPI to token program for ATA creates.
  - Checks: ensure mints sorted to avoid duplicate pools; rent for realloc of pool as liquidity grows; CPI metas mark authority as signer via seeds; negative tests for wrong mint order and missing seeds.