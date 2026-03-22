---
name: review-pr
description: Review a GitHub PR. Use when PRs are open, at integration checkpoints, or before deploying contracts to mainnet. Checks protocol/client boundary, schema consistency, and contract security.
---

# Review PR

Review a pull request, checking that changes work correctly within their layer and across the protocol/client boundary.

## Arguments

Takes an optional PR number: `/review-pr 3`

If no number given, list open PRs and review the most recent one:
```bash
gh pr list --state open
```

## System Layers

| Layer | What | Where |
|-------|------|-------|
| **Protocol** | Onchain contracts | `contracts/` |
| **Client** | Off-chain tooling (arena, fighters, CLI, signing) | `nojohns/`, `games/`, `arena/`, `fighters/` |
| **Frontend** | Website (read-only) | `web/` |
| **Shared** | Docs, tests, root files | `docs/`, `tests/`, root |

See `docs/ARCHITECTURE.md` for the full diagram.

## Steps

### 1. Get the PR

```bash
gh pr view <number> --json title,body,author,files,additions,deletions
gh pr diff <number>
```

### 2. Identify which layers the PR touches

Flag if a PR crosses layer boundaries — this isn't wrong, but cross-layer changes need extra attention at the integration boundary.

### 3. Review criteria

**For all PRs:**
- Does the code do what the PR description says?
- Any obvious bugs, logic errors, or missing error handling?
- Does it follow existing patterns in the codebase?
- Are there test changes? Should there be?

**For protocol PRs (contracts/) — extra scrutiny:**
- Reentrancy: does any function send ETH/MON before updating state?
- Access control: who can call each function? Are there missing checks?
- Escrow safety: can funds get locked permanently? Are there escape hatches (timeout, cancel)?
- Admin keys: does any contract have an owner or admin who can control funds? (This is a design violation — the protocol should never have discretion over escrowed funds.)
- EIP-712 signature validation: are signatures checked against the correct struct hash and domain separator?
- Gas: anything unusually expensive? (Loops over unbounded arrays, excessive storage writes)
- Events: are key state changes emitted? The frontend indexes these.

**For client PRs (nojohns/, games/, arena/):**
- Does it break existing CLI commands?
- Are new dependencies justified?
- Does signing code match the protocol's EIP-712 domain and struct?

**For frontend PRs (web/):**
- Does it read from the correct contract addresses?
- Does it handle RPC errors gracefully?
- Lighter review — frontend is read-only, low risk.

### 4. Protocol/client boundary check

This is the most important review step for cross-layer changes. If the PR touches anything related to match results, signatures, or contract interaction, verify consistency across the boundary:

- `contracts/src/MatchProof.sol` — the Solidity struct and EIP-712 typehash
- `nojohns/wallet.py` — the Python EIP-712 type definitions and domain
- `docs/HANDOFF-SCAVIEFAE.md` — the documented spec

Check specifically:
- Do the struct field names, types, and order match exactly?
- Is the EIP-712 domain (`name`, `version`, `chainId`, `verifyingContract`) consistent?
- Does the client's signing produce signatures the protocol will accept?
- Are addresses real (not `address(0)` placeholders)?

Mismatches here cause silent failures — signatures won't verify on-chain.

### 5. Post the review

Use PR comments for code-specific feedback (attached to the diff, resolved on update). Use issues only for standalone bugs or integration gaps that exist beyond the PR.

```bash
# Approve
gh pr review <number> --approve --body "..."

# Request changes
gh pr review <number> --request-changes --body "..."

# Comment only (no approval/rejection)
gh pr review <number> --comment --body "..."
```

**Review format:**

```markdown
## Review: <PR title>

**Layers:** [which layers this PR touches]

**Schema:** [OK — consistent / WARNING — MatchResult struct changed / N/A — no schema-related changes]

### Findings

- [list of observations, concerns, suggestions]

### Verdict

[approve / request changes / comment]
```

### 6. Contract deploy gate

If the PR includes Solidity changes AND targets mainnet deployment:
- Do NOT approve without reading every line of the contract
- Verify forge tests pass: `cd contracts && forge test -vv`
- Check deployment script uses correct RPC and chain ID
- Flag any contract that hasn't been tested on testnet first

Testnet deploys can be approved with lighter review.

## What NOT to do

- Don't edit files in the PR. If you see something that needs changing, request changes and describe what's needed.
- Don't block PRs over style. This is a hackathon.
- Don't review your own PRs with this skill — that defeats the purpose.
