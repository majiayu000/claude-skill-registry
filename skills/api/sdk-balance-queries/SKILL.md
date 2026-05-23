---
name: Bankr x402 SDK - Balance Queries
description: This skill should be used when the user asks "what are my balances", "how much ETH do I have", "check my wallet", "show my tokens", "portfolio value", "what tokens do I own", "NFT holdings", "how much USDC", "get token balances", "wallet contents", or any question about token balances, wallet contents, portfolio values, or NFT holdings across chains using the Bankr SDK.
version: 1.1.0
---

# SDK Balance Queries

Query multi-chain token balances and portfolio data using natural language prompts.

## Operations

| Operation | Example Prompt | Notes |
|-----------|----------------|-------|
| Single token balance | "How much USDC do I have?" | Fastest query type |
| Multi-token balance | "Show my ETH, USDC, and DEGEN balances" | Single chain |
| All tokens on chain | "What tokens do I have on Base?" | Lists all holdings |
| Multi-chain balances | "Show my balances across all chains" | Slower, queries all |
| Portfolio value | "What's my total portfolio value in USD?" | USD conversion |
| Token value | "How much is my DEGEN worth?" | Single token USD |
| NFT holdings | "Show me my NFT collections" | Lists collections |
| NFT floor prices | "What's the floor price of my NFTs?" | External API calls |

## Prompt Patterns

```
# Token Balances
"What are my token balances?"
"How much [TOKEN] do I have?"
"Show my [TOKEN] balance on [CHAIN]"
"What's my balance of token 0x..."

# Multi-Chain
"Show my balances across all chains"
"What are my balances on Base and Ethereum?"
"Compare my USDC holdings across all chains"

# Portfolio Value
"What's my total portfolio value in USD?"
"How much is my [TOKEN] worth in USD?"
"What's the total value of my Base holdings?"

# NFTs
"Show me my NFT collections"
"How many Pudgy Penguins do I own?"
"What's the floor price of my NFTs?"
```

## Usage

```typescript
import { BankrClient } from "@bankr/sdk";

const client = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
});

const result = await client.promptAndWait({
  prompt: "What are my token balances on Base?",
});

console.log(result.response);
// "You have 150.5 USDC, 0.25 ETH, 1000 DEGEN on Base..."
```

## Supported Chains

| Chain | Notes |
|-------|-------|
| Base | Default chain, fastest responses |
| Ethereum | Mainnet ERC20 and NFTs |
| Polygon | L2 tokens and NFTs |
| Solana | SPL tokens and NFTs |

Specify chain in prompt: "on Base", "on Ethereum", "on Polygon", "on Solana"

## Related Skills

- **sdk-wallet-operations**: Client setup and configuration
- **sdk-capabilities**: Full list of supported operations
