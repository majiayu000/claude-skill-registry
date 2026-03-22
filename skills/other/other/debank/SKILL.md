---
name: debank
description: Query DeBank OpenAPI for wallet portfolios, token holdings, DeFi positions, and transaction history.
metadata:
  {
    "cryptoclaw":
      { "emoji": "🏦", "requires": { "env": ["DEBANK_API_KEY"] }, "primaryEnv": "DEBANK_API_KEY" },
  }
---

# DeBank OpenAPI

Query wallet portfolios, token balances, DeFi protocol positions, NFTs, and transaction history across 100+ EVM chains.

## Base URL

```
https://pro-openapi.debank.com/v1
```

Requires API key: set `DEBANK_API_KEY`. Paid plans at https://cloud.debank.com/open-api

Pass via header: `AccessKey: {key}`

## Endpoints

### Total Balance

```
GET /user/total_balance?id={address}
```

Returns total USD value across all chains.

### Chain Balances

```
GET /user/chain_list?id={address}
```

Returns per-chain balance breakdown with chain name, logo, and USD value.

### Token List

```
GET /user/all_token_list?id={address}&is_all=true
```

Returns all token holdings across all chains with:

- `chain` — chain identifier
- `name`, `symbol`, `decimals`
- `amount` — raw balance
- `price` — current USD price
- `logo_url`

Filter by chain: `GET /user/token_list?id={address}&chain_id={chain}`

Chain IDs: `bsc`, `eth`, `matic`, `arb`, `op`, `base`, `avax`, `ftm`

### DeFi Protocol Positions

```
GET /user/all_complex_protocol_list?id={address}
```

Returns all DeFi positions grouped by protocol:

- Lending (supply/borrow)
- Liquidity pools (LP positions)
- Farming (staked tokens + rewards)
- Vesting / locked tokens

Each position includes USD value, APY (when available), and health factor for lending.

Filter by chain: `GET /user/complex_protocol_list?id={address}&chain_id={chain}`

### NFT List

```
GET /user/all_nft_list?id={address}&is_all=true
```

Returns NFT holdings with collection name, floor price, and image.

### Transaction History

```
GET /user/history_list?id={address}&chain_id={chain}&page_count=20
```

Returns parsed transaction history with human-readable descriptions:

- Swap, Send, Receive, Approve, Contract Interaction
- Token amounts and counterparties
- Pagination via `start_time` parameter

### Token Info

```
GET /token?id={address}&chain_id={chain}
```

Returns token metadata: name, symbol, price, market cap, holders, logo.

### Protocol Info

```
GET /protocol?id={protocol_id}
```

Returns protocol details: TVL, chains, site URL, logo.

### Protocol List

```
GET /protocol/list
```

Returns all tracked protocols. **Large payload** — filter output.

## Usage Notes

- DeBank tracks 100+ EVM chains automatically — no need to query each chain separately when using `all_*` endpoints
- Always use `all_token_list` and `all_complex_protocol_list` for full portfolio overview
- For transaction history, `chain_id` is required — ask user which chain or iterate through their active chains
- DeFi positions include detailed breakdowns (supply vs borrow, LP composition) — present clearly
- Combine with `coingecko` for price charts and `security-check` for token risk assessment
- Rate limits depend on plan tier — avoid unnecessary repeated calls

## Example Interactions

User: "What's in my wallet?"
→ Call `all_token_list` for active wallet, present holdings sorted by USD value

User: "Show my DeFi positions"
→ Call `all_complex_protocol_list`, group by protocol, show value and APY

User: "What's the portfolio of 0x...?"
→ Call `total_balance` for overview, then `all_token_list` for details

User: "Show my recent transactions on BSC"
→ Call `history_list` with `chain_id=bsc`, present last 20 parsed transactions
