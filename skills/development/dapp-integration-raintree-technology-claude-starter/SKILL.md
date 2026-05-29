---
name: aptos-dapp-integration
description: Expert on building decentralized applications on Aptos with frontend integration, wallet connectivity (Petra, Martian, Pontem), TypeScript SDK, transaction submission, and wallet adapter patterns. Triggers on keywords wallet connect, petra, martian, pontem, typescript sdk, aptos sdk, dapp, frontend integration, wallet adapter, transaction, sign
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos DApp Integration Expert

## Purpose

Provide expert guidance on integrating Aptos blockchain with frontend applications, including wallet connectivity, transaction submission, account management, and using the TypeScript SDK for building decentralized applications.

## When to Use

Auto-invoke when users mention:
- **Wallets** - Petra, Martian, Pontem, wallet connection, wallet adapter
- **Frontend Integration** - React, Next.js, Vue, dApp UI
- **TypeScript SDK** - @aptos-labs/ts-sdk, aptos client, API calls
- **Transactions** - sign transaction, submit transaction, transaction builder
- **Accounts** - account creation, authentication, user session
- **Smart Contract Calls** - view functions, entry functions, payload

## Core Integration Concepts

### Wallet Connection Flow

```
1. Detect wallet extension (Petra, Martian, etc.)
2. Request connection approval from user
3. Get connected account address
4. Listen for account/network changes
5. Sign and submit transactions
6. Handle wallet disconnection
```

### TypeScript SDK Architecture

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

// Initialize client
const config = new AptosConfig({ network: Network.TESTNET });
const aptos = new Aptos(config);

// Query blockchain
const account = await aptos.getAccountInfo({ accountAddress: "0x..." });

// Submit transactions
const transaction = await aptos.transaction.build.simple({...});
```

## Process

When a user asks about DApp integration:

### 1. Identify Integration Need

```
Common scenarios:
- Connecting wallet to React/Next.js app
- Reading on-chain data (account info, resources, events)
- Submitting transactions from frontend
- Handling wallet switching/disconnection
- Managing user authentication
- Displaying NFTs or token balances
- Building transaction UI
```

### 2. Choose Integration Approach

**Option A: Wallet Adapter (Recommended)**
- Use @aptos-labs/wallet-adapter-react
- Supports multiple wallets
- Standard hooks and components
- Best for production apps

**Option B: Direct Wallet Integration**
- Integrate with specific wallet (Petra, Martian)
- More control, less abstraction
- Good for custom requirements

**Option C: SDK Only (Read-Only)**
- Use TypeScript SDK
- No wallet needed
- Query blockchain data
- Good for analytics, explorers

### 3. Provide Integration Solution

Structure your response:
- **Setup** - installation and configuration
- **Code example** - working integration code
- **Wallet handling** - connection/disconnection logic
- **Transaction flow** - how to build and submit
- **Error handling** - common issues and solutions
- **Best practices** - security and UX considerations

## Wallet Adapter Integration

### Installation

```bash
npm install @aptos-labs/wallet-adapter-react \
            @aptos-labs/wallet-adapter-ant-design \
            petra-plugin-wallet-adapter \
            @martianwallet/aptos-wallet-adapter
```

### React Setup

```typescript
import { AptosWalletAdapterProvider } from "@aptos-labs/wallet-adapter-react";
import { PetraWallet } from "petra-plugin-wallet-adapter";
import { MartianWallet } from "@martianwallet/aptos-wallet-adapter";

function App() {
  const wallets = [new PetraWallet(), new MartianWallet()];

  return (
    <AptosWalletAdapterProvider
      plugins={wallets}
      autoConnect={true}
      onError={(error) => console.error(error)}
    >
      <YourApp />
    </AptosWalletAdapterProvider>
  );
}
```

### Using Wallet Hooks

```typescript
import { useWallet } from "@aptos-labs/wallet-adapter-react";

function WalletButton() {
  const {
    connect,
    disconnect,
    account,
    connected,
    wallet,
    signAndSubmitTransaction
  } = useWallet();

  const handleConnect = async () => {
    try {
      await connect("Petra"); // or wallet.name
    } catch (error) {
      console.error("Failed to connect:", error);
    }
  };

  if (connected) {
    return (
      <div>
        <p>Connected: {account?.address}</p>
        <button onClick={disconnect}>Disconnect</button>
      </div>
    );
  }

  return <button onClick={handleConnect}>Connect Wallet</button>;
}
```

## TypeScript SDK Patterns

### Initialize Client

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

// Mainnet
const mainnetConfig = new AptosConfig({ network: Network.MAINNET });
const mainnet = new Aptos(mainnetConfig);

// Testnet
const testnetConfig = new AptosConfig({ network: Network.TESTNET });
const testnet = new Aptos(testnetConfig);

// Custom node
const customConfig = new AptosConfig({
  fullnode: "https://custom-node.example.com",
  indexer: "https://custom-indexer.example.com",
});
const custom = new Aptos(customConfig);
```

### Read Blockchain Data

```typescript
// Get account info
const accountInfo = await aptos.getAccountInfo({
  accountAddress: "0x1234..."
});

// Get account resources
const resources = await aptos.getAccountResources({
  accountAddress: "0x1234..."
});

// Get specific resource
const coinResource = await aptos.getAccountResource({
  accountAddress: "0x1234...",
  resourceType: "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
});

// Get account modules
const modules = await aptos.getAccountModules({
  accountAddress: "0x1234..."
});

// Get events
const events = await aptos.getAccountEventsByEventType({
  accountAddress: "0x1234...",
  eventType: "0x1::coin::WithdrawEvent"
});
```

### View Functions (Read-Only)

```typescript
// Call view function to read state
const result = await aptos.view({
  payload: {
    function: "0x1234::my_module::get_balance",
    typeArguments: [],
    functionArguments: ["0xabcd..."],
  },
});

console.log("Balance:", result[0]);
```

## Transaction Patterns

### Simple Transaction (Entry Function)

```typescript
import { useWallet } from "@aptos-labs/wallet-adapter-react";

function TransferButton() {
  const { signAndSubmitTransaction } = useWallet();

  const handleTransfer = async () => {
    try {
      const response = await signAndSubmitTransaction({
        data: {
          function: "0x1::coin::transfer",
          typeArguments: ["0x1::aptos_coin::AptosCoin"],
          functionArguments: [
            "0xrecipient...", // recipient address
            "100000000",     // amount (in octas)
          ],
        },
      });

      // Wait for transaction
      await aptos.waitForTransaction({
        transactionHash: response.hash,
      });

      console.log("Transfer successful:", response.hash);
    } catch (error) {
      console.error("Transfer failed:", error);
    }
  };

  return <button onClick={handleTransfer}>Transfer APT</button>;
}
```

### Transaction with SDK (More Control)

```typescript
import { Account, Aptos } from "@aptos-labs/ts-sdk";

async function submitTransaction(aptos: Aptos, sender: Account) {
  // Build transaction
  const transaction = await aptos.transaction.build.simple({
    sender: sender.accountAddress,
    data: {
      function: "0x1234::my_module::my_function",
      typeArguments: [],
      functionArguments: [arg1, arg2],
    },
  });

  // Sign transaction
  const senderAuthenticator = aptos.transaction.sign({
    signer: sender,
    transaction,
  });

  // Submit transaction
  const committedTxn = await aptos.transaction.submit.simple({
    transaction,
    senderAuthenticator,
  });

  // Wait for confirmation
  const executedTransaction = await aptos.waitForTransaction({
    transactionHash: committedTxn.hash,
  });

  return executedTransaction;
}
```

### Multi-Agent Transaction

```typescript
const transaction = await aptos.transaction.build.multiAgent({
  sender: sender.accountAddress,
  secondarySignerAddresses: [secondSigner.accountAddress],
  data: {
    function: "0x1234::escrow::create_escrow",
    functionArguments: [/* ... */],
  },
});

const senderAuth = aptos.transaction.sign({ signer: sender, transaction });
const secondAuth = aptos.transaction.sign({ signer: secondSigner, transaction });

const response = await aptos.transaction.submit.multiAgent({
  transaction,
  senderAuthenticator: senderAuth,
  additionalSignersAuthenticators: [secondAuth],
});
```

## Common DApp Patterns

### Pattern 1: Check Token Balance

```typescript
async function getAptBalance(address: string): Promise<number> {
  try {
    const resource = await aptos.getAccountResource({
      accountAddress: address,
      resourceType: "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
    });

    return Number(resource.coin.value);
  } catch (error) {
    console.error("Error fetching balance:", error);
    return 0;
  }
}
```

### Pattern 2: Display NFTs

```typescript
async function getUserNFTs(address: string) {
  const nfts = await aptos.getAccountOwnedTokens({
    accountAddress: address,
  });

  return nfts.map(nft => ({
    name: nft.current_token_data?.token_name,
    description: nft.current_token_data?.description,
    uri: nft.current_token_data?.token_uri,
    collection: nft.current_token_data?.collection_name,
  }));
}
```

### Pattern 3: Transaction Status Tracking

```typescript
import { useState } from "react";

function useTransactionStatus() {
  const [status, setStatus] = useState<"idle" | "pending" | "success" | "error">("idle");
  const [hash, setHash] = useState<string | null>(null);

  const submitTransaction = async (txn: any) => {
    try {
      setStatus("pending");
      const response = await signAndSubmitTransaction(txn);
      setHash(response.hash);

      await aptos.waitForTransaction({ transactionHash: response.hash });
      setStatus("success");

      return response;
    } catch (error) {
      setStatus("error");
      throw error;
    }
  };

  return { status, hash, submitTransaction };
}
```

### Pattern 4: Network Switching

```typescript
import { Network } from "@aptos-labs/ts-sdk";
import { useWallet } from "@aptos-labs/wallet-adapter-react";

function NetworkSwitch() {
  const { network, changeNetwork } = useWallet();

  const switchToMainnet = async () => {
    try {
      await changeNetwork(Network.MAINNET);
    } catch (error) {
      console.error("Failed to switch network:", error);
    }
  };

  return (
    <div>
      <p>Current: {network?.name}</p>
      <button onClick={switchToMainnet}>Switch to Mainnet</button>
    </div>
  );
}
```

## Direct Wallet Integration (Petra)

### Detect and Connect

```typescript
declare global {
  interface Window {
    aptos?: any;
  }
}

async function connectPetra() {
  if (!window.aptos) {
    throw new Error("Petra wallet not installed");
  }

  try {
    const response = await window.aptos.connect();
    const account = await window.aptos.account();

    return {
      address: account.address,
      publicKey: account.publicKey,
    };
  } catch (error) {
    throw new Error("User rejected connection");
  }
}
```

### Sign and Submit with Petra

```typescript
async function signAndSubmit(payload: any) {
  const pendingTransaction = await window.aptos.signAndSubmitTransaction(payload);

  // Wait for confirmation
  const client = new Aptos(new AptosConfig({ network: Network.MAINNET }));
  const txn = await client.waitForTransaction({
    transactionHash: pendingTransaction.hash,
  });

  return txn;
}
```

## Error Handling

### Common Errors

```typescript
try {
  await signAndSubmitTransaction(txn);
} catch (error: any) {
  if (error.code === 4001) {
    console.error("User rejected transaction");
  } else if (error.message.includes("INSUFFICIENT_BALANCE")) {
    console.error("Insufficient balance for transaction");
  } else if (error.message.includes("SEQUENCE_NUMBER_TOO_OLD")) {
    console.error("Transaction nonce issue - retry");
  } else {
    console.error("Transaction failed:", error);
  }
}
```

### Wallet Detection

```typescript
function detectWallets() {
  const wallets = {
    petra: !!window.aptos,
    martian: !!window.martian,
    pontem: !!window.pontem,
  };

  if (!Object.values(wallets).some(Boolean)) {
    return { installed: false, wallets };
  }

  return { installed: true, wallets };
}
```

## UI/UX Best Practices

### Loading States

```typescript
function TransactionButton() {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      await submitTransaction();
    } finally {
      setLoading(false);
    }
  };

  return (
    <button disabled={loading} onClick={handleClick}>
      {loading ? "Processing..." : "Submit Transaction"}
    </button>
  );
}
```

### Transaction Confirmation UI

```typescript
function TransactionStatus({ hash }: { hash: string }) {
  const explorerUrl = `https://explorer.aptoslabs.com/txn/${hash}?network=mainnet`;

  return (
    <div className="success-message">
      <p>✅ Transaction Successful!</p>
      <a href={explorerUrl} target="_blank" rel="noopener noreferrer">
        View on Explorer
      </a>
    </div>
  );
}
```

### Account Display

```typescript
function AccountDisplay({ address }: { address: string }) {
  const shortened = `${address.slice(0, 6)}...${address.slice(-4)}`;

  return (
    <div className="account">
      <span title={address}>{shortened}</span>
      <button onClick={() => navigator.clipboard.writeText(address)}>
        📋 Copy
      </button>
    </div>
  );
}
```

## Security Considerations

### ✅ Best Practices

- Always validate user input before building transactions
- Show transaction details to user before signing
- Use HTTPS for all API calls
- Don't store private keys in frontend
- Verify transaction success before updating UI
- Handle wallet disconnection gracefully
- Check network before submitting transactions

### ❌ Avoid

- Never ask users for private keys
- Don't auto-submit transactions without user action
- Avoid hardcoding sensitive data
- Don't ignore error handling
- Never bypass wallet confirmation dialogs

## Testing DApp Integration

### Mock Wallet for Tests

```typescript
const mockWallet = {
  connect: jest.fn().mockResolvedValue({ address: "0x123..." }),
  disconnect: jest.fn(),
  signAndSubmitTransaction: jest.fn().mockResolvedValue({ hash: "0xabc..." }),
};
```

### Testing with Testnet

```typescript
// Use testnet for development
const config = new AptosConfig({ network: Network.TESTNET });

// Get testnet APT from faucet
await aptos.fundAccount({
  accountAddress: account.accountAddress,
  amount: 100000000, // 1 APT
});
```

## Framework-Specific Examples

### Next.js App Router

```typescript
// app/providers.tsx
"use client";

import { AptosWalletAdapterProvider } from "@aptos-labs/wallet-adapter-react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AptosWalletAdapterProvider plugins={wallets} autoConnect>
      {children}
    </AptosWalletAdapterProvider>
  );
}
```

### React Query Integration

```typescript
import { useQuery } from "@tanstack/react-query";

function useAccountBalance(address: string | undefined) {
  return useQuery({
    queryKey: ["balance", address],
    queryFn: () => getAptBalance(address!),
    enabled: !!address,
    refetchInterval: 10000, // Refetch every 10s
  });
}
```

## Response Style

- **Code-first** - Show working integration examples
- **Framework-aware** - Adapt to React/Next.js/Vue
- **Security-conscious** - Highlight security considerations
- **UX-focused** - Suggest good user experience patterns
- **Error handling** - Always include error handling

## Follow-up Suggestions

After helping with integration, suggest:
- Error handling improvements
- Loading and success states
- Transaction simulation before submission
- Event listening for real-time updates
- Mobile wallet integration (wallet connect)
- Testing strategies for DApp
