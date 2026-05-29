---
name: dojo-wallets
description: |
  Use when managing wallets and accounts in dojo.js games.
  Triggers: burner wallet, useBurner, create wallet, connect wallet, BurnerProvider,
  account management, predeployed, session wallet
---

# Dojo.js Wallet & Account Management

## When to Use

Use this skill when:

- Setting up burner wallets for development
- Managing player accounts
- Connecting external wallets
- Implementing account switching

## BurnerProvider Setup

```tsx
import { BurnerProvider, useBurner } from "@dojoengine/create-burner";

const burnerConfig = {
  masterAddress: "0x...", // Prefunded account
  masterPrivateKey: "0x...", // Private key
  accountClassHash: "0x...", // Account class hash
  rpcUrl: "http://localhost:5050",
  feeTokenAddress: "0x...", // ETH contract address
};

function App() {
  return (
    <BurnerProvider initOptions={burnerConfig}>
      <Game />
    </BurnerProvider>
  );
}
```

## useBurner Hook

```tsx
import { useBurner } from "@dojoengine/create-burner";

function AccountManager() {
  const {
    account, // Current active account
    isDeploying, // True while creating new burner
    count, // Number of burners

    create, // Create new burner
    list, // List all burners
    select, // Select burner by address
    get, // Get burner by address
    clear, // Clear all burners

    listConnectors, // Get starknet-react connectors
    copyToClipboard,
    applyFromClipboard,
    generateAddressFromSeed,
  } = useBurner();

  return (
    <div>
      <p>Current: {account?.address}</p>
      <button onClick={() => create()} disabled={isDeploying}>
        {isDeploying ? "Creating..." : "New Burner"}
      </button>
    </div>
  );
}
```

# Creating Burners

```tsx
const { create } = useBurner();

// Create random burner
const newAccount = await create();

// Create deterministic burner from seed
const deterministicAccount = await create({
  secret: "my-secret-seed",
  index: 0,
});
```

## Listing & Selecting Burners

```tsx
function BurnerSelector() {
  const { list, select, account } = useBurner();
  const burners = list();

  return (
    <select value={account?.address} onChange={(e) => select(e.target.value)}>
      {burners.map((burner) => (
        <option key={burner.address} value={burner.address}>
          {burner.address.slice(0, 10)}...
        </option>
      ))}
    </select>
  );
}
```

## Starknet-React Integration

```tsx
import { StarknetConfig, InjectedConnector } from "@starknet-react/core";

function Providers({ children }) {
  const { listConnectors } = useBurner();

  const connectors = [
    new InjectedConnector({ options: { id: "argentX" } }),
    new InjectedConnector({ options: { id: "braavos" } }),
    ...listConnectors(), // Add burner connectors
  ];

  return <StarknetConfig connectors={connectors}>{children}</StarknetConfig>;
}
```

## PredeployedConnector (Dev Mode)

For Katana predeployed accounts:

```tsx
import {
  PredeployedConnector,
  usePredeployedAccounts,
} from "@dojoengine/predeployed-connector";

const predeployed = new PredeployedConnector({
  rpcUrl: "http://localhost:5050",
  accounts: [
    {
      address: "0x...",
      privateKey: "0x...",
      name: "Account 1",
    },
  ],
});
```

## Account Export/Import

Share burners between devices:

```tsx
const { copyToClipboard, applyFromClipboard } = useBurner();

// Export all burners
await copyToClipboard();

// Import from clipboard
await applyFromClipboard();
```

## Deterministic Addresses

Generate addresses without deploying:

```tsx
const { generateAddressFromSeed } = useBurner();

const address = generateAddressFromSeed({
  secret: "game-specific-seed",
  index: playerIndex,
});
```

## WithAccount HOC

Require account connection:

```tsx
import { WithAccount } from "@dojoengine/sdk/react";

const ProtectedComponent = WithAccount(
  ({ account, address }) => <div>Connected: {address}</div>,
  () => <div>Please connect wallet</div>,
);
```

## Full Provider Hierarchy

```tsx
function App() {
  return (
    <StarknetConfig connectors={connectors}>
      <BurnerProvider initOptions={burnerConfig}>
        <DojoSdkProvider sdk={sdk} dojoConfig={config}>
          <Game />
        </DojoSdkProvider>
      </BurnerProvider>
    </StarknetConfig>
  );
}
```

## Common Pitfalls

1. **Master account funding**: Ensure master account has enough ETH to deploy burners
2. **Class hash mismatch**: Use correct account class hash for your Starknet version
3. **Provider order**: BurnerProvider should wrap DojoSdkProvider if using both
4. **Local storage**: Burners persist in localStorage - clear for fresh start
5. **RPC URL mismatch**: Ensure all configs point to same network
