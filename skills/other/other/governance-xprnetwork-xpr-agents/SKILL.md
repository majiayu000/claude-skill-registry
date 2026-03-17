---
name: governance
description: XPR Network governance — communities, proposals, voting on the gov contract
---

## XPR Network Governance

You have tools to interact with XPR Network's on-chain governance system via the `gov` contract. Communities create proposals, and token holders vote on them.

### Key Concepts

- **Communities** — governance groups (XPR Network, Metal DAO, LOAN Protocol, XPR Grants, Metal X, D.O.G.E.). Each has its own voting strategy, proposal fee, and quorum.
- **Proposals** — on-chain records with candidates (voting options), start/end times, and an approval status. Proposal content (title, description) is stored off-chain in the Gov API.
- **Voting Strategies** — determine who can vote and how vote weight is calculated:
  - `xpr-unstaked-and-staked-balances` — weight = XPR balance (staked + unstaked)
  - `xmt-balances` — weight = XMT balance
  - `loan-and-sloan-balances` — weight = LOAN + sLOAN balance
  - `kyc-verification` — 1 vote per KYC-verified account
- **Voting Systems** — `"0"` = single choice, `"1"` = multiple choice, `"2"` = ranked choice, `"5"` = approval voting
- **Quorum** — minimum participation threshold (basis points, e.g. 300 = 3%)
- **Proposal Fee** — token payment required to create a proposal (varies by community, e.g. 20,000 XPR, 100 XMT, 50,000 LOAN)

### Active Communities

| ID | Name | Strategy | Fee | Quorum |
|----|------|----------|-----|--------|
| 3 | XPR Network | XPR balances | 20,000 XPR | 3% |
| 4 | Metal DAO | XMT balances | 100 XMT | 3% |
| 5 | LOAN Protocol | LOAN+sLOAN | 50,000 LOAN | 25% |
| 6 | XPR Grants | XPR balances | 20,000 XPR | 3% |
| 7 | Metal X | XPR balances | 20,000 XPR | 3% |
| 8 | D.O.G.E. | KYC verification | 1 XDOGE | 0.01% |

### Read-Only Tools (safe, no signing)

- `gov_list_communities` — list all governance communities with strategies, fees, quorum, and admins
- `gov_list_proposals` — list proposals with optional community and status filters
- `gov_get_proposal` — get full proposal details including title and description from Gov API, plus vote totals per candidate
- `gov_get_votes` — get individual votes cast on a proposal (scans from most recent)
- `gov_get_config` — get governance global config (paused state, total counts)

### Write Tools (require `confirmed: true`)

- `gov_vote` — vote on an active proposal. Specify the candidate(s) and weight.
- `gov_post_proposal` — create a new governance proposal. Requires paying the community's proposal fee (token transfer + postprop action in one transaction).

### Voting

To vote, you need the `communityId`, `proposalId`, and `winners` (array of candidate IDs with weights). For simple Yes/No proposals, use `[{id: 0, weight: 100}]` for Yes or `[{id: 1, weight: 100}]` for No.

### Creating Proposals

Creating a proposal requires:
1. A `content` ID — created via the Gov API (`https://gov.api.xprnetwork.org`)
2. Paying the community's proposal fee (token transfer to `gov`)
3. Calling `postprop` with all proposal parameters

The `gov_post_proposal` tool handles steps 2 and 3 (fee + postprop). You must provide the content ID from step 1.

### Proposal URLs

Proposals can be viewed at: `https://gov.xprnetwork.org/communities/{communityId}/proposals/{proposalId}`

### Safety Rules

- Proposals have start and end times — voting is only allowed during the active period
- Each community has different fee tokens — check the community's `proposalFee` before creating proposals
- Quorum is in basis points (300 = 3%) — proposals need sufficient participation to pass
- Admins can approve/decline proposals — the `approve` field shows the final status
