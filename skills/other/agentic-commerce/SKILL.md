---
name: agentic-commerce
description: Create, fund, and settle on-chain agent jobs via ERC-8183 Agentic Commerce Protocol.
metadata: { "cryptoclaw": { "emoji": "💼", "always": true } }
---

# Agentic Commerce (ERC-8183)

On-chain job escrow protocol for AI agent commerce. A client posts a job, locks funds in escrow, a provider executes the work, and an evaluator approves or rejects — settlement is automatic and trustless.

## Tools

- `job_create` — Create a new job (specify evaluator, description, deadline)
- `job_set_provider` — Assign or change provider (Open state only)
- `job_set_budget` — Set or negotiate budget in USDC (Open state only)
- `job_fund` — Lock USDC into escrow (Open → Funded, auto-approves ERC-20)
- `job_submit` — Provider submits deliverable hash/IPFS CID (Funded → Submitted)
- `job_complete` — Evaluator approves, releasing funds to provider (Submitted → Completed)
- `job_reject` — Reject job with reason (client when Open, evaluator when Funded/Submitted)
- `job_claim_refund` — Claim refund for expired job (permissionless)
- `job_query` — Query job details by ID
- `job_list` — List jobs related to active wallet (filter by role)

## Job Lifecycle

```
Open → Funded → Submitted → Completed (funds → provider)
  ↘      ↘         ↘
  Rejected  Expired   Rejected/Expired (funds → client)
```

## Roles

- **Client** — Creates and funds jobs; receives refunds on rejection/expiry
- **Provider** — Executes work and submits deliverables; receives payment on completion
- **Evaluator** — Immutable per-job judge; only address that can approve or reject after funding

## Workflow

1. **Create job**: "Create an agentic commerce job for a DeFi analysis report, evaluator 0x..., deadline 2026-04-01"
2. **Set budget**: "Set job #1 budget to 100 USDC"
3. **Fund escrow**: "Fund job #1"
4. **Provider submits**: "Submit deliverable for job #1: QmXoypiz..."
5. **Evaluator decides**: "Complete job #1" or "Reject job #1"

## Supported Networks

- **Base Mainnet** (primary, USDC payment)
- **Base Sepolia** (testnet)

## Contract Addresses

| Network      | ACPCore Contract                             | Payment Token (USDC)                         |
| ------------ | -------------------------------------------- | -------------------------------------------- |
| Base Mainnet | `0x16213AB6a660A24f36d4F8DdACA7a3d0856A8AF5` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Base Sepolia | `0x16213AB6a660A24f36d4F8DdACA7a3d0856A8AF5` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

## ERC-8004 Integration

ERC-8183 composes with ERC-8004 (Trustless Agents). Use `agent_identity` to verify a provider's on-chain identity and `agent_reputation` to check their trust score before creating or accepting a job.

## Security

- State-changing tools (`job_create`, `job_fund`, `job_submit`, `job_complete`, `job_reject`) require confirmation
- `job_claim_refund` is permissionless and cannot be blocked by hooks — guaranteed refund recovery
- Funds are held in the ACPCore contract until a terminal state (Completed/Rejected/Expired)
- `job_fund` includes slippage protection (expectedBudget must match current budget)
