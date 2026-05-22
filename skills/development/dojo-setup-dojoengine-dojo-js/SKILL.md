---
name: dojo-setup
description: |
  Use when setting up dojo.js SDK in a frontend project.
  Triggers: setup dojo, initialize dojo, configure dojo, dojoengine setup, sdk init,
  DojoSdkProvider, world address, torii url, dojo config
---

# Dojo.js SDK Setup

## When to Use

Use this skill when:
- Setting up dojo.js in a new frontend project
- Configuring the SDK with world address and Torii URL
- Setting up the React provider hierarchy
- Generating TypeScript types from ABIs

## SDK Initialization

```typescript
import { init } from "@dojoengine/sdk";
import { DojoConfig } from "@dojoengine/core";
import { schema } from "./models.gen"; // Generated from ABI

const sdk = await init<typeof schema>({
    client: {
        worldAddress: "0x...",
        toriiUrl: "http://localhost:8080",
    },
    domain: {
        name: "MyGame",
        version: "1.0.0",
        chainId: "SN_MAIN", // or "SN_SEPOLIA"
    },
});
```

## React Provider Setup

> **Note**: `masterAddress` and `masterPrivateKey` are for local development only. In production, use wallet connections instead.

```tsx
import { DojoSdkProvider } from "@dojoengine/sdk/react";
import { DojoConfig, DojoProvider } from "@dojoengine/core";

const dojoConfig: DojoConfig = {
    manifest: manifest, // From manifest.json
    rpcUrl: process.env.VITE_RPC_URL || "http://localhost:5050",
    toriiUrl: process.env.VITE_TORII_URL || "http://localhost:8080",
    // For local development only - never hardcode in production
    masterAddress: process.env.VITE_MASTER_ADDRESS || "0x...",
    masterPrivateKey: process.env.VITE_MASTER_PRIVATE_KEY || "",
};

function App() {
    return (
        <DojoSdkProvider
            dojoConfig={dojoConfig}
            sdk={sdk}
            // clientFn is a user-provided factory to create your game client
            clientFn={(provider) => new GameClient(provider)}
        >
            {children}
        </DojoSdkProvider>
    );
}
```

## Environment Variables

```env
VITE_WORLD_ADDRESS=0x...
VITE_TORII_URL=http://localhost:8080
VITE_RPC_URL=http://localhost:5050
VITE_CHAIN_ID=SN_SEPOLIA
```

## Key Configuration Options

| Option | Description |
|--------|-------------|
| `worldAddress` | Deployed world contract address |
| `toriiUrl` | Torii indexer URL (default: `http://localhost:8080`) |
| `rpcUrl` | Starknet RPC URL |
| `chainId` | `SN_MAIN`, `SN_SEPOLIA`, or custom |
| `manifest` | Dojo manifest.json for contract ABIs |

## Using DojoContext

```tsx
import { useDojoSDK } from "@dojoengine/sdk/react";

function GameComponent() {
    const { sdk, config, provider, useDojoStore } = useDojoSDK();
    // sdk: SDK instance for queries/subscriptions
    // config: DojoConfig
    // provider: DojoProvider for contract calls
    // useDojoStore: Zustand store hook
}
```

## Common Pitfalls

1. **Missing schema types**: Generate types from ABI using `@dojoengine/core` CLI
2. **CORS issues**: Ensure Torii is configured to allow your frontend origin
3. **Wrong chain ID**: Must match the deployed world's chain
4. **Provider hierarchy**: `DojoSdkProvider` must wrap all Dojo-consuming components
