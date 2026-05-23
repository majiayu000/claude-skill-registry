---
name: deploy-react-frontend
description: Create React frontends for Algorand dApps with wallet integration. Use when creating React frontends that interact with smart contracts, setting up wallet connections (Pera, Defly, Exodus), integrating typed app clients with wallet signers, or building dApp UIs that call contract methods. Strong triggers include "create a frontend for my contract", "add wallet connection to my React app", "how do I call my contract from the frontend?", "set up use-wallet with my typed client", "connect Pera wallet to my dApp", "algorand.setSigner".
---

# Deploying React Frontends for Algorand

Build React applications that connect to Algorand wallets and interact with smart contracts using typed clients.

## Prerequisites

Before using this skill, ensure:

1. **Smart contract is deployed** with a known App ID
2. **ARC-56/ARC-32 app spec exists** (e.g., `MyContract.arc56.json`)
3. **React project is set up** (Vite, Next.js, or Create React App)

## Core Workflow: The "Signer Handoff" Pattern

The key insight is passing the wallet's transaction signer to AlgorandClient, which then provides it to typed app clients:

```
Wallet (use-wallet) → transactionSigner
                              ↓
                    AlgorandClient.setSigner()
                              ↓
                    Typed App Client (defaultSender)
                              ↓
                    Contract Method Calls (auto-signed)
```

## How to proceed

### Step 1: Generate Typed Client

Generate a TypeScript client from your contract's app spec:

```bash
algokit generate client path/to/MyContract.arc56.json --output src/contracts/MyContractClient.ts
```

This creates a typed client with full IntelliSense for your contract's methods.

### Step 2: Install Dependencies

Core packages:
```bash
npm install @algorandfoundation/algokit-utils @txnlab/use-wallet-react algosdk
```

Wallet peer dependencies (install only for wallets you're using):

| Wallet | Package |
|--------|---------|
| Pera | `@perawallet/connect` |
| Defly | `@blockshake/defly-connect` |
| Kibisis | `@agoralabs-sh/avm-web-provider` |
| Lute | `lute-connect` |

Example for Pera + Defly:
```bash
npm install @perawallet/connect @blockshake/defly-connect
```

### Step 3: Set Up WalletProvider

Wrap your app with `WalletProvider` at the root level:

```tsx
import { NetworkId, WalletId, WalletManager, WalletProvider } from '@txnlab/use-wallet-react'

const walletManager = new WalletManager({
  wallets: [WalletId.PERA, WalletId.DEFLY, WalletId.EXODUS],
  defaultNetwork: NetworkId.TESTNET,
})

export default function App() {
  return (
    <WalletProvider manager={walletManager}>
      <YourApp />
    </WalletProvider>
  )
}
```

### Step 4: Create Wallet Connection UI

Use the `useWallet()` hook to display available wallets:

```tsx
import { useWallet } from '@txnlab/use-wallet-react'

function ConnectWallet() {
  const { wallets, activeAddress } = useWallet()

  if (activeAddress) {
    return <p>Connected: {activeAddress}</p>
  }

  return (
    <div>
      {wallets.map((wallet) => (
        <button key={wallet.id} onClick={() => wallet.connect()}>
          Connect {wallet.metadata.name}
        </button>
      ))}
    </div>
  )
}
```

### Step 5: Integrate Typed Client with Wallet Signer

This is the critical integration step. Register the wallet's signer with AlgorandClient:

```tsx
import { useWallet } from '@txnlab/use-wallet-react'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import { MyContractClient } from './contracts/MyContractClient'

function ContractInteraction() {
  const { transactionSigner, activeAddress } = useWallet()

  const callContract = async () => {
    if (!activeAddress || !transactionSigner) {
      alert('Please connect your wallet first')
      return
    }

    // 1. Create AlgorandClient for the network
    const algorand = AlgorandClient.testNet()

    // 2. Register wallet signer with AlgorandClient
    algorand.setSigner(activeAddress, transactionSigner)

    // 3. Create typed client with wallet as default sender
    const appClient = algorand.client.getTypedAppClientById(MyContractClient, {
      appId: 12345n, // Your deployed App ID
      defaultSender: activeAddress,
    })

    // 4. Call contract methods - signer is used automatically
    const result = await appClient.send.myMethod({ args: { value: 42n } })
    console.log('Result:', result.return)
  }

  return <button onClick={callContract}>Call Contract</button>
}
```

### Step 6: Deploy New Contracts (Optional)

If deploying from the frontend (less common), use the Factory pattern:

```tsx
import { MyContractFactory } from './contracts/MyContractClient'

const factory = new MyContractFactory({
  algorand,
  defaultSender: activeAddress,
})

const { appClient } = await factory.deploy({
  onSchemaBreak: 'append',
  onUpdate: 'append',
})
```

## Important Rules / Guidelines

1. **Always call setSigner() before creating clients** - The signer must be registered with AlgorandClient first
2. **Check for null activeAddress and transactionSigner** - They are null when no wallet is connected
3. **Use TypeScript** - Typed clients provide full type safety and IntelliSense
4. **Match networks** - Ensure AlgorandClient network matches WalletManager network
5. **React only** - This skill covers React; other frameworks have different patterns

## Getting the App Client

Three ways to get a typed app client:

| Method | Use Case |
|--------|----------|
| `getTypedAppClientById()` | Known App ID (most common for frontends) |
| `getTypedAppClientByCreatorAndName()` | Resolve by creator address and app name |
| `factory.deploy()` | Deploy new instance and get client |

```tsx
// By App ID (recommended for frontends)
const appClient = algorand.client.getTypedAppClientById(MyContractClient, {
  appId: 12345n,
  defaultSender: activeAddress,
})

// By Creator and Name
const appClient = await algorand.client.getTypedAppClientByCreatorAndName(
  MyContractClient,
  {
    creatorAddress: 'CREATORADDRESS...',
    appName: 'MyContract',
  }
)
```

## Common Errors / Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `activeAddress is null` | Wallet not connected | Check wallet connection before contract calls |
| `transactionSigner is undefined` | No active wallet | Prompt user to connect wallet first |
| `signer not found for address` | Signer not registered | Call `algorand.setSigner(activeAddress, transactionSigner)` |
| `app does not exist` | Wrong App ID | Verify App ID matches deployed contract |
| `Method not found` | Wrong method name or signature | Check typed client API; ensure args match ABI |
| `Network mismatch` | Different networks | Ensure AlgorandClient and WalletManager use same network |
| `User rejected transaction` | User cancelled in wallet | Handle rejection gracefully in UI |
| `global is not defined` | algosdk references `global` in browser | Add to vite.config.ts: `define: { global: 'globalThis' }` |
| TypeScript errors in generated client | Strict TS mode incompatibility | Set `verbatimModuleSyntax: false` in tsconfig.json |

## Wallet Disconnect

Handle wallet disconnection:

```tsx
function DisconnectButton() {
  const { wallets } = useWallet()

  const disconnect = async () => {
    const activeWallet = wallets.find((w) => w.isActive)
    if (activeWallet) {
      await activeWallet.disconnect()
    }
  }

  return <button onClick={disconnect}>Disconnect</button>
}
```

## References / Further Reading

- [REFERENCE.md](./references/REFERENCE.md) - Detailed API reference
- [EXAMPLES.md](./references/EXAMPLES.md) - Complete code examples
- [use-wallet Documentation](https://txnlab.gitbook.io/use-wallet)
- [AlgoKit Utils TypeScript](https://dev.algorand.co/algokit/utils/typescript/algorand-client/)
- [Typed App Clients](https://dev.algorand.co/algokit/utils/typescript/typed-app-clients/)
