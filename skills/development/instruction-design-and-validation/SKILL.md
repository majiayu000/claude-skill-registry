---
name: instruction-design-and-validation
description: Design Solana/Anchor instructions with clear inputs, constraints, authority checks, and invariants. Use when defining or reviewing instruction APIs.
---

# Instruction Design and Validation

Role framing: You are an instruction architect. Your goal is to define minimal, safe instruction interfaces with explicit constraints and thorough validation.

## Initial Assessment
- What state changes are needed? Which accounts and authorities are involved?
- Are inputs fixed-size or variable? Any untrusted user data?
- Cross-program interactions? Which programs and CPIs?
- Performance needs: expected tx size, compute budget, number of accounts?

## Core Principles
- Keep instructions single-responsibility; avoid multi-mode flags when possible.
- Validate all caller-provided addresses; re-derive PDAs inside program.
- Enforce authority at the smallest scope: signer + owner + custom invariants.
- Fail fast with descriptive errors; keep error enum tight.
- Bound untrusted data lengths; avoid realloc unless necessary.

## Workflow
1) Define intent: describe state transition in one sentence.
2) Specify inputs
   - Accounts table (role, owner, signer, writable, seeds).
   - Instruction data struct with versioning field if necessary.
3) Write validation logic
   - Ownership, signer, seeds/bump, data length bounds, relationship checks (e.g., same mint).
   - Custom invariants (e.g., price bounds, timestamp windows).
4) Compute budget planning
   - Estimate compute; add ComputeBudgetInstruction if needed; minimize account count.
5) Error design
   - Add specific errors for each validation step; map to user-facing messages.
6) Tests
   - Happy path; each validation failure; edge sizes; CPI failure propagation.

## Templates / Playbooks
- Account table format (reuse from solana-account-model).
- Validation pattern in Anchor:
  - #[account(mut, seeds = [...], bump, has_one = ...)]
  - Manual checks in handler for cross-account relationships.
- Versioned instruction data: include u8 version + enum payload.

## Common Failure Modes + Debugging
- Missing signer/writable flags causing runtime failure: align Anchor constraints with client metas.
- Seed mismatch between client and program: recompute seeds and confirm bump.
- Data length overflow on realloc: pre-calc size, fund rent.
- CPI returns Constraint... errors: inspect callee IDL and account order.

## Quality Bar / Validation
- Instruction spec includes account table + data schema + invariants.
- All validations covered by tests with clear errors.
- Compute budget measured; no unnecessary accounts.
- Versioning/compatibility plan noted when needed.

## Output Format
Deliver instruction spec containing intent, accounts table, data schema, validation steps, error list, and test checklist.

## Examples
- Simple: Update config parameter
  - Accounts: config PDA (w), authority signer; validation: seeds, has_one authority.
- Complex: Place order on orderbook via CPI
  - Accounts: user, market, event queue, bids/asks, token accounts; validation of owner/mint match; compute budget ix; error mapping for CPI failures; tests for bad mints and missing signer.