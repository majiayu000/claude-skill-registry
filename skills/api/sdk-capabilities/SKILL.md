---
name: Bankr x402 SDK - Capabilities
description: This skill should be used when the user asks "what can the SDK do", "what prompts does Bankr support", "SDK features", "supported operations", "what can I build with Bankr", "Bankr SDK capabilities", "what chains are supported", "what tokens can I trade", "SDK supported commands", or wants to understand the full range of operations available through the Bankr SDK.
version: 1.1.0
---

# SDK Capabilities

Complete guide to operations supported by the Bankr SDK. The SDK accepts natural language prompts and returns transaction data for execution.

## Supported Operations

| Category | Operation | Example Prompt |
|----------|-----------|----------------|
| **Swaps** | Token swap | "Swap 0.1 ETH to USDC" |
| | Value-based buy | "Buy $100 of DEGEN" |
| | Percentage swap | "Swap 50% of my ETH to USDC" |
| **Transfers** | ERC20 transfer | "Send 100 USDC to 0x..." |
| | ETH transfer | "Send 0.1 ETH to @username" |
| | NFT transfer | "Send my Bored Ape #123 to 0x..." |
| **Wrapping** | Wrap ETH | "Wrap 1 ETH" |
| | Unwrap WETH | "Unwrap 1 WETH" |
| **Cross-Chain** | Bridge (EVM only) | "Bridge 100 USDC from Ethereum to Base" |
| **Leverage** | Long position | "Buy $50 of ETH/USD with 5x leverage" |
| | Short position | "Short $10 of GOLD" |
| | Close position | "Close all my BTC/USD positions" |
| **NFTs** | Buy NFT | "Buy the cheapest Tiny Dino NFT" |
| | List for sale | "List my Bored Ape for 10 ETH" |
| | Mint (Manifold) | "Mint from Manifold at 0x..." |
| | Mint (SeaDrop) | "Mint from SeaDrop at 0x..." |
| **Staking** | Stake BNKR | "Stake 1000 BNKR" |
| | Unstake | "Unstake my BNKR" |
| **Queries** | Balances | "What are my balances?" |
| | NFT holdings | "What NFTs do I own?" |
| | Token price | "Price of ETH" |
| | Token analysis | "Analyze DEGEN" |

## NOT Supported

| Feature | Alternative |
|---------|-------------|
| Polymarket betting | Use https://bankr.bot directly |
| Limit orders | Use https://swap.bankr.bot |
| DCA/TWAP orders | Use https://swap.bankr.bot |
| Solana cross-chain | EVM chains only |
| Bankr Earn | Use Bankr terminal |

## Supported Chains

| Chain | Native Token | Default |
|-------|-------------|---------|
| Base | ETH | Yes |
| Ethereum | ETH | No |
| Polygon | MATIC | No |

## Usage

```typescript
import { BankrClient } from "@bankr/sdk";

const client = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
});

const result = await client.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC on Base",
});

if (result.status === "completed" && result.transactions?.length) {
  // Execute the returned transaction with your wallet
  await wallet.sendTransaction(result.transactions[0].metadata.transaction);
}
```

## Cost

Each request costs $0.01 USDC via x402 micropayments. Gas fees for transactions are paid separately.

## Related Skills

- **sdk-token-swaps**: Token swap patterns and approval handling
- **sdk-transaction-builder**: Building transfers, NFT ops, bridges
- **sdk-balance-queries**: Portfolio and balance queries
