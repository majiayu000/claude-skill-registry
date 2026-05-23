---
name: phantom-wallet-mcp
description: Execute wallet operations through the Phantom MCP server — get addresses, sign transactions, transfer tokens, buy tokens, and sign messages across Solana, Ethereum, Bitcoin, and Sui
---

# Phantom Wallet MCP

Use the `phantom` MCP server to interact with the user's Phantom wallet directly.

## Available Tools

| Tool | Description |
|------|-------------|
| `get_wallet_addresses` | Get blockchain addresses (Solana, Ethereum, Bitcoin, Sui) for the connected wallet |
| `sign_transaction` | Sign a transaction (base64url for Solana, RLP hex for Ethereum) |
| `transfer_tokens` | Transfer SOL or SPL tokens on Solana — builds, signs, and sends the transaction |
| `buy_token` | Fetch Solana swap quotes from Phantom API; optionally sign and send |
| `sign_message` | Sign a UTF-8 message with automatic chain-specific routing |

## Setup

The `phantom` MCP server requires a `PHANTOM_APP_ID` environment variable from [Phantom Portal](https://phantom.com/portal). On first use, it opens a browser for OAuth authentication via Google or Apple login.

## Supported Networks

| Chain | Networks |
|-------|----------|
| Solana | mainnet, devnet, testnet |
| Ethereum | Mainnet, Sepolia, Polygon, Base, Arbitrum |
| Bitcoin | Mainnet |
| Sui | Mainnet, Testnet |

Networks use CAIP-2 format (e.g., `solana:mainnet`, `eip155:1`).

## Examples

### Get wallet addresses

Ask the `phantom` MCP to retrieve the user's wallet addresses, then use them for transactions.

### Transfer SOL

Use `transfer_tokens` to send SOL to a recipient address. The MCP handles transaction building, signing, and submission.

### Sign a message

Use `sign_message` for wallet verification or authentication flows. The MCP routes to the correct chain based on the network parameter.

## Important Notes

- Sessions persist locally in `~/.phantom-mcp/session.json`
- This is preview software — use a separate wallet with minimal funds for testing
- The MCP server runs via stdio transport (launched by `npx -y @phantom/mcp-server`)
