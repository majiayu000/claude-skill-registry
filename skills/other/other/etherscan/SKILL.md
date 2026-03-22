---
name: etherscan
description: Query block explorer APIs (Etherscan, BSCScan, Polygonscan, etc.) for transactions, contracts, and gas data.
metadata:
  {
    "cryptoclaw":
      {
        "emoji": "🔍",
        "requires": { "env": ["ETHERSCAN_API_KEY"] },
        "primaryEnv": "ETHERSCAN_API_KEY",
      },
  }
---

# Multi-chain Explorer API

Query Etherscan-compatible block explorer APIs for transaction history, contract source code, ABIs, and gas data.

## Supported Explorers

| Chain    | Base URL                                  | Env Var (optional override)   |
| -------- | ----------------------------------------- | ----------------------------- |
| Ethereum | `https://api.etherscan.io/api`            | `ETHERSCAN_API_KEY`           |
| BSC      | `https://api.bscscan.com/api`             | `BSCSCAN_API_KEY` or same key |
| Polygon  | `https://api.polygonscan.com/api`         | `POLYGONSCAN_API_KEY`         |
| Arbitrum | `https://api.arbiscan.io/api`             | `ARBISCAN_API_KEY`            |
| Optimism | `https://api-optimistic.etherscan.io/api` | `OPTIMISM_API_KEY`            |
| Base     | `https://api.basescan.org/api`            | `BASESCAN_API_KEY`            |

All explorers accept the `apikey` parameter. Many share a single Etherscan key, but some chains require separate registration.

**Rate limit**: 5 calls/second per key.

## Modules & Actions

### Account — Transaction History

```
?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&apikey={key}
```

Returns normal transactions for an address.

### Account — Token Transfers (ERC-20)

```
?module=account&action=tokentx&address={addr}&page=1&offset=20&sort=desc&apikey={key}
```

Filter by contract: add `&contractaddress={token}`

### Account — ERC-721 Transfers

```
?module=account&action=tokennfttx&address={addr}&page=1&offset=20&sort=desc&apikey={key}
```

### Account — Balance

```
?module=account&action=balance&address={addr}&tag=latest&apikey={key}
```

Returns balance in wei. Divide by 1e18 for ETH/BNB.

### Contract — Get ABI

```
?module=contract&action=getabi&address={addr}&apikey={key}
```

Returns the contract ABI as a JSON string. **Tip**: Parse the result and pass it to `read_contract` or `write_contract` for dynamic contract interaction.

### Contract — Get Source Code

```
?module=contract&action=getsourcecode&address={addr}&apikey={key}
```

Returns source code, compiler version, constructor arguments, and proxy implementation address if applicable.

### Gas Tracker (Ethereum only)

```
?module=gastracker&action=gasoracle&apikey={key}
```

Returns SafeGasPrice, ProposeGasPrice, FastGasPrice in gwei.

## Workflow: Dynamic Contract Interaction

1. User provides a contract address
2. Call `getabi` to fetch the ABI
3. Parse the ABI to list available read/write functions
4. Use `read_contract` with the ABI and function name to query
5. Use `write_contract` for state-changing calls (with user confirmation)

This enables interacting with ANY verified contract without pre-built tools.

## Usage Notes

- Always include `&apikey={key}` — requests without it are heavily rate-limited
- Use `offset` and `page` for pagination; don't fetch more than needed
- The `getabi` endpoint only works for verified contracts
- For proxy contracts, `getsourcecode` includes the implementation address — fetch that ABI too
- Cross-reference contract data with `security-check` skill for risk assessment

## Example Queries

User: "Show my recent transactions on BSC"
→ Call BSCScan `txlist` for active wallet, present last 10 with value and status

User: "Get the ABI for this contract: 0x..."
→ Call `getabi`, parse result, summarize available functions

User: "What's the current gas price on Ethereum?"
→ Call `gasoracle`, present safe/standard/fast prices
