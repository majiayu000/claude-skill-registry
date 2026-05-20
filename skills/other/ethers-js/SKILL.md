---
name: ethers-js
cluster: blockchain
description: "JavaScript library for interacting with Ethereum blockchain, including wallet management and smart contract calls."
tags: ["ethereum","javascript","blockchain"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ethereum javascript blockchain smart contracts wallets transactions"
---

# ethers-js

## Purpose
Ethers.js is a JavaScript library for interacting with the Ethereum blockchain, enabling developers to manage wallets, sign transactions, and call smart contracts programmatically. It abstracts low-level Ethereum APIs for easier integration in web and Node.js applications.

## When to Use
Use ethers.js when building Ethereum-based dApps that require wallet operations, transaction handling, or smart contract interactions in JavaScript environments. It's ideal for projects needing a lightweight alternative to Web3.js, especially for browser-based or server-side Ethereum scripting.

## Key Capabilities
- Wallet management: Create, import, and derive wallets using mnemonic phrases or private keys.
- Provider support: Connect to Ethereum nodes via HTTP, WebSocket, or third-party services like Infura.
- Transaction handling: Sign and send transactions, including gas estimation and nonce management.
- Smart contract interactions: Read and write to contracts using ABI definitions, with support for events and multicall.
- Utility functions: Encode/decode data, handle big numbers, and compute hashes for Ethereum-specific tasks.

## Usage Patterns
Always import ethers.js as a module in your JavaScript file. Initialize a provider first, then create a wallet or signer. For asynchronous operations, use async/await patterns. Set up error catching around all blockchain calls to handle network failures. Use environment variables for sensitive data like private keys (e.g., `process.env.PRIVATE_KEY`).

## Common Commands/API
- Create a wallet: Use `ethers.Wallet.createRandom()` to generate a new wallet.
  ```javascript
  const ethers = require('ethers');
  const wallet = ethers.Wallet.createRandom();
  console.log(wallet.address);
  ```
- Connect to a provider: Specify a URL or use Infura with an API key.
  ```javascript
  const provider = new ethers.providers.JsonRpcProvider('https://mainnet.infura.io/v3/' + process.env.INFURA_API_KEY);
  ```
- Call a smart contract: Use `Contract` class with ABI and address.
  ```javascript
  const contract = new ethers.Contract(address, abi, signer);
  const result = await contract.functionName(arg1);
  ```
- Sign and send a transaction: Prepare and broadcast via signer.
  ```javascript
  const tx = await signer.sendTransaction({ to: '0xAddress', value: ethers.utils.parseEther('1.0') });
  ```

## Integration Notes
Integrate ethers.js into Node.js projects by installing via npm: `npm install ethers`. For browser use, include via a CDN or bundle with Webpack. If using third-party providers like Infura, set the API key in an environment variable (e.g., `$INFURA_API_KEY`) and pass it to the provider URL. Handle Web3 compatibility by using ethers.js's `Web3Provider` wrapper if needed. For testing, use Hardhat or Ganache and connect with a local provider like `new ethers.providers.JsonRpcProvider('http://localhost:8545')`.

## Error Handling
Wrap all ethers.js calls in try/catch blocks to handle common errors like network issues or invalid inputs. Check for specific error types, such as `ethers.errors.ServerError` for provider failures. Use `provider.on('error', handler)` for event-based error listening. Example:
```javascript
try {
  await provider.getBlockNumber();
} catch (error) {
  if (error.code === 'SERVER_ERROR') console.error('Network issue:', error.message);
}
```
Always validate inputs before operations, like ensuring addresses are checksummed with `ethers.utils.getAddress(address)`.

## Concrete Usage Examples
1. **Generate and fund a wallet:** Create a new wallet, get its address, and simulate funding it from another account.
   ```javascript
   const ethers = require('ethers');
   const wallet = ethers.Wallet.createRandom();
   const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
   console.log('New wallet address:', wallet.address);
   ```
   Then, use this address in a transaction from a funded wallet to send Ether.

2. **Interact with a ERC-20 token contract:** Connect to a token contract, check balance, and transfer tokens.
   ```javascript
   const abi = [{ "constant": true, "inputs": [{ "name": "_owner", "type": "address" }], "name": "balanceOf", "outputs": [{ "name": "", "type": "uint256" }], "type": "function" }];
   const contract = new ethers.Contract('0xTokenAddress', abi, signer);
   const balance = await contract.balanceOf(signer.address);
   await contract.transfer('0xRecipient', ethers.utils.parseUnits('10', 18));
   ```

## Graph Relationships
- Related to cluster: blockchain (e.g., shares connections with other blockchain tools like web3.js).
- Linked by tags: ethereum (e.g., relates to skills for Ethereum development), javascript (e.g., connects to JS-based libraries), blockchain (e.g., associates with general blockchain utilities).
