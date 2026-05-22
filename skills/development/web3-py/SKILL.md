---
name: web3-py
cluster: blockchain
description: "Python library for interacting with Ethereum blockchain via Web3 protocols."
tags: ["web3","python","ethereum"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "web3 python ethereum blockchain smart-contracts"
---

# web3-py

## Purpose
web3-py is a Python library for interacting with the Ethereum blockchain using Web3 protocols. It enables programmatic access to blockchain data, smart contracts, and transactions.

## When to Use
Use this skill when building Python applications that need to query Ethereum data, deploy smart contracts, or handle transactions. Applicable for dApps, blockchain analytics, or automated scripts interacting with Ethereum nodes.

## Key Capabilities
- Connect to Ethereum nodes via HTTP, WebSocket, or IPC providers.
- Manage accounts, sign transactions, and handle gas estimates.
- Interact with smart contracts using ABI definitions.
- Query blockchain state, including balances, blocks, and events.
- Support for Ethereum-compatible chains like Binance Smart Chain.

## Usage Patterns
Always import web3-py and initialize a Web3 instance with a provider. Use environment variables for sensitive keys, e.g., set `INFURA_API_KEY` in your shell. Structure code to handle asynchronous operations with `web3.async` for better performance. For production, wrap calls in try-except blocks and use a reliable provider URL.

## Common Commands/API
- To get an account balance: Use `web3.eth.get_balance(address)`. Example:
  ```python
  from web3 import Web3
  w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + os.getenv('INFURA_API_KEY')))
  balance = w3.eth.get_balance('0xYourAddress')
  ```
- To send a transaction: Use `w3.eth.send_transaction(transaction)`. Example:
  ```python
  tx = {'from': account.address, 'to': '0xRecipient', 'value': w3.to_wei(1, 'ether')}
  signed_tx = w3.eth.account.sign_transaction(tx, private_key=os.getenv('ETH_PRIVATE_KEY'))
  tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  ```
- To call a smart contract function: Use `contract.functions.myFunction().call()`. Example:
  ```python
  contract = w3.eth.contract(address='0xContractAddress', abi=contract_abi)
  result = contract.functions.balanceOf('0xAddress').call()
  ```
- To estimate gas: Use `w3.eth.estimate_gas(transaction)`. Pass a dictionary with 'from', 'to', and 'data' keys.

## Integration Notes
Integrate web3-py by installing via `pip install web3`. Configure providers with URLs like `https://mainnet.infura.io/v3/$INFURA_API_KEY` for Infura. Use env vars for keys: e.g., `os.getenv('INFURA_API_KEY')` for API access. For local nodes, use IPC: `Web3(Web3.IPCProvider('/path/to/geth.ipc'))`. Ensure compatibility with Ethereum versions; specify chain ID in transactions to prevent replay attacks. Test integrations in a sandbox like Ganache before production.

## Error Handling
Handle connection errors with try-except for `ConnectionError`, e.g.:
```python
try:
    w3.eth.get_block('latest')
except web3.exceptions.ConnectionError:
    print("Node unreachable; check provider URL and network status.")
```
For transaction failures, catch `ValueError` for insufficient funds or gas issues:
```python
try:
    tx_hash = w3.eth.send_transaction(tx)
except ValueError as e:
    if 'insufficient funds' in str(e):
        raise Exception("Add funds to account before retrying.")
```
Validate inputs like addresses with `w3.is_address(address)` before use. Log errors with details like error codes (e.g., RPC errors from providers) for debugging.

## Concrete Usage Examples
1. Querying token balance: To get the ERC-20 balance of an address on Ethereum mainnet, initialize Web3 with Infura, load the token contract, and call the balanceOf function. Example usage in a script: Set `INFURA_API_KEY` env var, then run the snippet above under Common Commands/API for contract calls.
2. Deploying a simple smart contract: Compile a Solidity contract to ABI and bytecode, then use `w3.eth.contract` to deploy. Example: In code, create a contract instance and send a transaction with the bytecode, handling gas limits as shown in the send_transaction example.

## Graph Relationships
- Related to cluster: blockchain (e.g., shares capabilities with other blockchain tools).
- Connected to tags: web3 (direct API interactions), python (Python-based implementation), ethereum (specific to Ethereum ecosystem).
- Links to: smart-contracts (via contract handling features), as indicated in embedding hint.
