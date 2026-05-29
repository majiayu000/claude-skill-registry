---
name: use-algokit-utils
description: AlgoKit Utils library for interacting with the Algorand blockchain from TypeScript or Python applications. Use when connecting to Algorand networks (LocalNet, TestNet, MainNet), sending payments or transferring assets, creating and managing accounts, deploying or interacting with smart contracts from client code, or composing transaction groups. NOT for writing smart contract code (use build-smart-contracts skill). Strong triggers include "How do I connect to Algorand?", "send a payment transaction", "create an account", "deploy my contract", "get an AlgorandClient", "AlgorandClient.fromEnvironment".
---

# AlgoKit Utils

Use AlgoKit Utils to interact with the Algorand blockchain from TypeScript or Python applications.

## Overview / Core Workflow

1. Create an `AlgorandClient` instance
2. Get or create accounts for signing
3. Send transactions using `algorand.send.*` methods
4. Or compose groups using `algorand.newGroup()`

## How to proceed

1. **Initialize AlgorandClient:**

   TypeScript:
   ```typescript
   import { AlgorandClient } from '@algorandfoundation/algokit-utils'

   const algorand = AlgorandClient.fromEnvironment()
   // Or: AlgorandClient.defaultLocalNet()
   // Or: AlgorandClient.testNet()
   // Or: AlgorandClient.mainNet()
   ```

   Python:
   ```python
   from algokit_utils import AlgorandClient

   algorand = AlgorandClient.from_environment()
   # Or: AlgorandClient.default_localnet()
   # Or: AlgorandClient.testnet()
   # Or: AlgorandClient.mainnet()
   ```

2. **Get accounts:**

   TypeScript:
   ```typescript
   const account = await algorand.account.fromEnvironment('DEPLOYER')
   ```

   Python:
   ```python
   account = algorand.account.from_environment("DEPLOYER")
   ```

3. **Send transactions:**

   TypeScript:
   ```typescript
   await algorand.send.payment({
     sender: account.addr,
     receiver: 'RECEIVERADDRESS',
     amount: algo(1),
   })
   ```

   Python:
   ```python
   algorand.send.payment(PaymentParams(
     sender=account.address,
     receiver="RECEIVERADDRESS",
     amount=AlgoAmount(algo=1),
   ))
   ```

## Important Rules / Guidelines

- **Use AlgorandClient** — It's the main entry point; avoid deprecated function-based APIs
- **Default to fromEnvironment()** — Works locally and in production via env vars
- **Register signers** — Use `algorand.account` to get accounts; signers are auto-registered
- **Use algo() helper** — For TypeScript, use `algo(1)` instead of raw microAlgos

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| LocalNet development | `AlgorandClient.defaultLocalNet()` |
| TestNet/MainNet | `AlgorandClient.testNet()` or `.mainNet()` |
| Custom node | `AlgorandClient.fromConfig({ algodConfig: {...} })` |
| Deploy contract | Use typed app client factory (see app-client docs) |
| Transaction groups | `algorand.newGroup().addPayment(...).addAssetOptIn(...).send()` |

## References / Further Reading

Language-specific references are organized in subfolders:

- **TypeScript** (`references/typescript/`): [AlgorandClient](./references/typescript/algorand-client.md)
- **Python** (`references/python/`): [AlgorandClient](./references/python/algorand-client.md)

External documentation:
- [AlgoKit Utils TS Docs](https://dev.algorand.co/algokit/utils/typescript/overview/)
- [AlgoKit Utils Python Docs](https://dev.algorand.co/algokit/utils/python/overview/)
