---
name: smart-contracts
cluster: blockchain
description: "Develop and deploy secure smart contracts on blockchain platforms using Solidity and Web3 technologies."
tags: ["solidity","smart-contracts","blockchain"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "smart contracts blockchain solidity ethereum web3"
---

# smart-contracts

## Purpose
This skill focuses on developing, compiling, deploying, and interacting with secure smart contracts using Solidity for writing code and Web3.js for blockchain interactions, targeting platforms like Ethereum.

## When to Use
Use this skill for tasks involving decentralized applications (dApps), token creation, or automated agreements on EVM-compatible blockchains. Apply it when you need to ensure code security, handle transactions, or integrate with Web3 ecosystems, such as building NFTs or DeFi protocols.

## Key Capabilities
- Write and compile Solidity contracts with features like inheritance, modifiers, and events.
- Deploy contracts to testnets (e.g., Sepolia) or mainnets using Web3.js providers.
- Interact with deployed contracts via RPC calls, including reading state and executing functions.
- Perform security audits by integrating tools like Slither for vulnerability detection.
- Handle Web3 transactions with gas estimation and error checking.

## Usage Patterns
To use this skill, structure your workflow as follows: First, write Solidity code in a .sol file. Then, compile it using a tool like Hardhat or solc. Deploy via a Web3 provider, and interact using JavaScript. Always test on a local node (e.g., Ganache) before mainnet. For integration, pass provider URLs as environment variables, like `$ETHEREUM_PROVIDER_URL`. Example pattern: Import Web3.js, connect to a provider, and call contract methods in a Node.js script.

## Common Commands/API
Use solc for compilation: `solc --optimize --bin input.sol -o build/`. For deployment with Hardhat, run `npx hardhat run scripts/deploy.js --network sepolia`. Web3.js API: Create a provider with `const web3 = new Web3($ETHEREUM_PROVIDER_URL);` and call `web3.eth.getBalance(address)`. For contract interaction, use ABI: `contract.methods.myFunction().send({from: account, gas: 200000})`. Config format: In Hardhat.config.js, define networks like `networks: { sepolia: { url: process.env.SEPOLIA_URL, accounts: [process.env.PRIVATE_KEY] } }`, where `$SEPOLIA_URL` and `$PRIVATE_KEY` are env vars. Authenticate with Infura by setting `$INFURA_API_KEY` in the provider URL.

## Integration Notes
Integrate this skill by installing dependencies like `npm install hardhat web3`. Set up a .env file for sensitive data (e.g., `ETHEREUM_PRIVATE_KEY=$YOUR_PRIVATE_KEY`). For external APIs, use providers like Infura or Alchemy with URLs formatted as `https://mainnet.infura.io/v3/$INFURA_API_KEY`. Ensure compatibility by using Web3.js version 1.x for Etherscan verification. To link with other skills, export contract ABIs as JSON for downstream use, e.g., in a frontend with React.

## Error Handling
Handle compilation errors by checking solc output for messages like "ParserError: Expected token". For deployment, catch Web3.js errors with try-catch blocks, e.g., `try { await contract.deploy({data: bytecode}); } catch (e) { if (e.message.includes('gas')) console.error('Insufficient gas'); }`. Common issues: Reverted transactions (check with `web3.eth.getTransactionReceipt(txHash)` for status); use events for asynchronous error logging. For security, validate inputs in Solidity with require statements, e.g., `require(msg.sender == owner, "Not authorized");`. Always use a funded account and monitor gas limits.

## Concrete Usage Examples
1. **Write and Deploy a Simple Storage Contract**: Create a file `SimpleStorage.sol` with `pragma solidity ^0.8.0; contract SimpleStorage { uint storedData; function set(uint x) public { storedData = x; } }`. Compile with `solc --bin SimpleStorage.sol`. Deploy using Hardhat: In `deploy.js`, write `const SimpleStorage = await ethers.getContractFactory("SimpleStorage"); const contract = await SimpleStorage.deploy(); await contract.deployed();`. Run `npx hardhat run deploy.js --network localhost`.
2. **Interact with an ERC20 Token Contract**: Assume a deployed token at address `0xTokenAddress`. In a Node.js script: `const web3 = new Web3($ETHEREUM_PROVIDER_URL); const contract = new web3.eth.Contract(ABI, '0xTokenAddress'); await contract.methods.transfer('0xRecipient', 100).send({from: '0xYourAddress', gas: 50000});`. Handle with error checking for insufficient funds.

## Graph Relationships
- Related to cluster: "blockchain" (e.g., shares tools with other blockchain skills).
- Connected via tags: "solidity" (links to language-specific tools), "smart-contracts" (cross-references deployment patterns), "blockchain" (integrates with general blockchain APIs).
- Outgoing edges: To "web3" for provider interactions, to "ethereum" for network specifics.
