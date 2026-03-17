---
name: nft
cluster: blockchain
description: "Skill for creating, managing, and interacting with Non-Fungible Tokens (NFTs) on blockchain networks."
tags: ["blockchain","nft","crypto"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "nft blockchain crypto tokens web3 smart-contracts"
---

## Purpose

This skill allows OpenClaw to handle NFT-related tasks on blockchain networks, including minting, transferring, querying, and managing NFTs using web3 protocols.

## When to Use

- When building applications that require NFT creation, such as digital art marketplaces or collectibles.
- For querying NFT ownership or metadata in blockchain projects.
- In scenarios involving crypto wallets or smart contracts where NFTs need to be transferred or verified.
- During integration with dApps to automate NFT interactions on networks like Ethereum or Solana.

## Key Capabilities

- Mint new NFTs on supported blockchains (e.g., Ethereum via ERC-721 standard).
- Transfer NFTs between wallet addresses with gas fee estimation.
- Retrieve and display NFT metadata, including token URI and owner details.
- Validate NFT existence and ownership using blockchain queries.
- Interact with smart contracts for advanced operations, like approving transfers.
- Specific: Supports networks via flags (e.g., --network ethereum for EVM chains or --network solana for SPL tokens).

## Usage Patterns

Always initialize with authentication by setting the environment variable `$NFT_API_KEY` before commands. For scripts, wrap calls in error-handling blocks to manage network failures.

To mint an NFT programmatically:
1. Export the key: `export NFT_API_KEY=your_api_key`
2. Use in a script: `claw nft create --network ethereum --wallet 0xYourWalletAddress`

For querying, chain commands: First, fetch metadata, then process it. Example pattern for automation: Use `claw nft query` in loops for batch ownership checks, ensuring rate limits (e.g., <10 calls/min on Ethereum).

Config format: Use JSON files for metadata, e.g., `{"name": "MyNFT", "description": "Token description", "image": "ipfs://hash"}`. Load via `--metadata path/to/file.json`.

## Common Commands/API

- CLI Command: `claw nft create --network <chain> --wallet <address> --metadata <file.json>`  
  Flags: `--network` (e.g., ethereum, solana), `--gas-limit 210000` for custom gas, `--dry-run` to simulate without executing.
  Example: `claw nft create --network ethereum --wallet 0x123abc --metadata nft_data.json` (creates and returns token ID).

- CLI Command: `claw nft transfer --network <chain> --from <sender_address> --to <receiver_address> --tokenId <id>`  
  Flags: `--approve-first` to handle approvals, `--gas-price 20gwei` for priority.
  Example: `claw nft transfer --network ethereum --from 0x123abc --to 0x456def --tokenId 1`

- API Endpoint: POST /api/nft/create  
  Body: `{"network": "ethereum", "wallet": "0x123abc", "metadata": {"name": "ArtPiece"}}`  
  Headers: Include `Authorization: Bearer $NFT_API_KEY`. Response: JSON with { "tokenId": "123", "transactionHash": "0xhash" }.

- API Endpoint: GET /api/nft/{tokenId}/metadata  
  Query Params: ?network=ethereum. Example: `curl -H "Authorization: Bearer $NFT_API_KEY" https://api.openclaw.com/api/nft/123/metadata`

Authentication: Required for all; set `$NFT_API_KEY` as an environment variable. For config, use a .env file: `NFT_API_KEY=sk_123abc`.

## Integration Notes

Integrate by importing the skill in OpenClaw workflows, e.g., via `import skill nft` in scripts. Ensure blockchain RPC endpoints are configured, like setting `$ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your_project_id`.

For smart contracts: Provide ABI in a JSON config file, e.g., `{"abi": [{"constant": true, "inputs": [], "name": "ownerOf", "outputs": [{"name": "", "type": "address"}], "type": "function"} ] }`, and pass with `--abi path/to/abi.json`.

Combine with other skills: Use alongside "blockchain" cluster skills for wallet management—e.g., first call `claw wallet balance` to check funds, then `claw nft create`.

Testing: Run in a testnet environment by adding `--testnet` flag, which switches to networks like Goerli (for Ethereum).

## Error Handling

Always use try-catch blocks for commands, e.g., in Python scripts: `try: subprocess.run(['claw', 'nft', 'create', '--network', 'ethereum']) except subprocess.CalledProcessError as e: print(e.output)`.

Common errors:
- Network issues: Check for "connection refused" by verifying `$ETHEREUM_RPC_URL` and retry with exponential backoff (e.g., wait 5s, then 10s).
- Invalid inputs: Validate wallet addresses with regex (e.g., `if not re.match(r'^0x[a-fA-F0-9]{40}$', address): raise ValueError` before commands.
- Authentication failures: If `$NFT_API_KEY` is missing, commands return 401; handle by prompting for setup or exiting gracefully.
- Gas errors: For "insufficient funds", advise checking balances first with `claw nft estimate-gas --network ethereum --command create`.

Prescriptive: Before any operation, run a health check: `claw nft status --network ethereum` to verify node connectivity.

## Concrete Usage Examples

1. **Minting an NFT on Ethereum:**  
   Set up: `export NFT_API_KEY=your_key` and prepare metadata in `metadata.json` as `{"name": "OpenClawArt", "description": "AI-generated piece"}`.  
   Command: `claw nft create --network ethereum --wallet 0xYourWallet --metadata metadata.json`  
   This mints the NFT, outputs the token ID, and signs the transaction using your wallet.

2. **Transferring an NFT:**  
   Prerequisites: Ensure the sender has approved the transfer.  
   Command: `claw nft transfer --network ethereum --from 0xSenderWallet --to 0xReceiverWallet --tokenId 42 --approve-first`  
   This transfers the specified NFT, handles gas automatically, and returns the transaction hash for verification.

## Graph Relationships

- Related to: blockchain cluster (e.g., shares dependencies with wallet and smart-contract skills).
- Tags: blockchain, nft, crypto (connects to other skills via these for combined queries).
- Connected skills: wallet (for funding operations), smart-contracts (for custom NFT logic), and web3 (for broader ecosystem integration).
