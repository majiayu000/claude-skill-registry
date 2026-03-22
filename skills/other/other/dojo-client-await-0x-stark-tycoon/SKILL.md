---
name: dojo-client
description: Integrate Dojo with game clients for JavaScript, Unity, Unreal, Rust, and other platforms. Generate typed bindings and connection code. Use when connecting frontends or game engines to your Dojo world.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Dojo Client Integration

Connect your game client or frontend to your deployed Dojo world across multiple platforms.

## When to Use This Skill

- "Set up JavaScript SDK for my Dojo game"
- "Integrate Dojo with Unity"
- "Generate TypeScript bindings"
- "Connect React app to my world"

## What This Skill Does

Handles client integration for:
- JavaScript/TypeScript SDK (primary)
- Unity, Unreal, Godot, Bevy (game engines)
- Typed binding generation
- Query/subscription patterns

## Supported Platforms

| Platform | Language | Package |
|----------|----------|---------|
| JavaScript/TypeScript | JS/TS | `@dojoengine/sdk` |
| Unity | C# | `dojo.unity` |
| Unreal Engine | C++ | `dojo.unreal` |
| Godot | GDScript | `dojo.godot` |
| Bevy | Rust | `dojo.bevy` |
| C/C++ | C/C++ | `dojo.c` |

## JavaScript/TypeScript Integration

### Quick Start

Use the quickstart wizard:

```bash
pnpx @dojoengine/create-dojo start
```

### Manual Setup

1. **Install dependencies:**

```bash
# Essential packages
pnpm add @dojoengine/core @dojoengine/sdk @dojoengine/torii-client

# Controller + starknet-react (recommended)
pnpm add @cartridge/connector @cartridge/controller @starknet-react/core @starknet-react/chains starknet

# For state management
pnpm add @dojoengine/state zustand immer

# Build tools for WASM support
pnpm add -D vite-plugin-wasm vite-plugin-top-level-await
```

2. **Create `dojoConfig.ts`:**

```typescript
import { createDojoConfig } from "@dojoengine/core";
import manifest from "../path/to/manifest_dev.json";

export const dojoConfig = createDojoConfig({ manifest });
```

3. **Generate TypeScript bindings:**

```bash
DOJO_MANIFEST_PATH="../path/to/Scarb.toml" sozo build --typescript
```

4. **Initialize the SDK:**

```typescript
import { init } from "@dojoengine/sdk";
import { DojoSdkProvider } from "@dojoengine/sdk/react";
import { dojoConfig } from "./dojoConfig.ts";
import { setupWorld } from "./bindings/typescript/contracts.gen.ts";
import type { SchemaType } from "./bindings/typescript/models.gen.ts";

async function main() {
    const sdk = await init<SchemaType>({
        client: {
            worldAddress: dojoConfig.manifest.world.address,
            toriiUrl: "http://localhost:8080",
            relayUrl: "/ip4/127.0.0.1/tcp/9090",
        },
        domain: {
            name: "MyDojoProject",
            version: "1.0",
            chainId: "KATANA",
            revision: "1",
        },
    });

    // Use in React
    createRoot(document.getElementById("root")!).render(
        <DojoSdkProvider sdk={sdk} dojoConfig={dojoConfig} clientFn={setupWorld}>
            <StarknetProvider>
                <App />
            </StarknetProvider>
        </DojoSdkProvider>
    );
}
```

### Controller Integration (starknet-react)

[Cartridge Controller](https://docs.cartridge.gg/controller/getting-started) is the recommended way to handle account management in Dojo games.
It provides session-based authentication via starknet-react.

**Define policies and create the connector (outside React components):**

```typescript
import { ControllerConnector } from "@cartridge/connector";
import { SessionPolicies } from "@cartridge/controller";

const policies: SessionPolicies = {
    contracts: {
        [ACTIONS_CONTRACT_ADDRESS]: {
            methods: [
                { name: "spawn", entrypoint: "spawn" },
                { name: "move", entrypoint: "move" },
            ],
        },
    },
};

const connector = new ControllerConnector({ policies });
```

**Wrap your app with StarknetConfig:**

```typescript
import { StarknetConfig } from "@starknet-react/core";
import { sepolia, mainnet } from "@starknet-react/chains";

function StarknetProvider({ children }: { children: React.ReactNode }) {
    return (
        <StarknetConfig
            autoConnect
            chains={[mainnet, sepolia]}
            connectors={[connector]}
            provider={provider}
        >
            {children}
        </StarknetConfig>
    );
}
```

**Connect/disconnect:**

```typescript
import { useConnect, useDisconnect, useAccount } from "@starknet-react/core";

function ConnectWallet() {
    const { connect, connectors } = useConnect();
    const { disconnect } = useDisconnect();
    const { address } = useAccount();

    return address ? (
        <button onClick={() => disconnect()}>Disconnect</button>
    ) : (
        <button onClick={() => connect({ connector: connectors[0] })}>
            Connect
        </button>
    );
}
```

The `useAccount()` hook used in the "Executing Systems" section below returns the Controller session account once connected.

### Querying Entities

```typescript
import { ToriiQueryBuilder, KeysClause, MemberClause } from "@dojoengine/sdk";

// Simple query: Find a specific player
const entities = await sdk.getEntities({
    query: new ToriiQueryBuilder().withClause(
        KeysClause(["dojo_starter-Player"], ["0xabcde..."], "FixedLen").build()
    ),
});

// Access the results
entities.items.forEach((entity) => {
    const player = entity.models.dojo_starter.Player;
    console.log(`Player: ${player?.name}, Score: ${player?.score}`);
});
```

### Complex Queries

```typescript
const entities = await sdk.getEntities({
    query: new ToriiQueryBuilder()
        .withClause(
            MemberClause("dojo_starter-Player", "score", "Gt", 0).build()
        )
        .withLimit(10)
        .withOffset(0)
        .withOrderBy([{ field: "score", direction: "Desc" }]),
});
```

### Subscribing to Changes

```typescript
const [initialEntities, subscription] = await sdk.subscribeEntityQuery({
    query: new ToriiQueryBuilder()
        .withClause(
            MemberClause("dojo_starter-Player", "score", "Gt", 100).build()
        )
        .includeHashedKeys(),
    callback: ({ data, error }) => {
        if (data) {
            data.forEach((entity) => {
                const player = entity.models.dojo_starter.Player;
                console.log(`Player ${player?.id}: ${player?.score} points`);
            });
        }
    },
});

// Cancel later
// subscription.cancel();
```

### React Hooks

```typescript
import { useEntityQuery, useModels, useModel, useEntityId } from "@dojoengine/sdk/react";

function MyComponent() {
    // Subscribe to entity changes
    useEntityQuery(
        new ToriiQueryBuilder()
            .withClause(MemberClause("dojo_starter-Item", "durability", "Eq", 2).build())
            .includeHashedKeys()
    );

    // Get all items from the store
    const items = useModels("dojo_starter-Item");

    // Get a single item by entity ID
    const entityId = useEntityId(1);
    const item = useModel(entityId, "dojo_starter-Item");

    return (
        <div>
            {Object.entries(items).map(([id, item]) => (
                <div key={id}>Item {id}: durability {item?.durability}</div>
            ))}
        </div>
    );
}
```

### Executing Systems

```typescript
import { useDojoSDK } from "@dojoengine/sdk/react";
import { useAccount } from "@starknet-react/core";

function GameActions() {
    const { client } = useDojoSDK();
    const { account } = useAccount();

    async function spawn() {
        await client.actions.spawn({ account });
    }

    async function move(direction: number) {
        await client.actions.move({ account, direction });
    }

    return (
        <div>
            <button onClick={spawn}>Spawn</button>
            <button onClick={() => move(1)}>Move Right</button>
        </div>
    );
}
```

## Game Engine Integration

### Unity

See [dojo.unity documentation](https://github.com/dojoengine/dojo.unity) for:
- Package installation via Unity Package Manager
- C# bindings generation
- Entity synchronization patterns
- Transaction handling

### Unreal Engine

See [dojo.unreal documentation](https://github.com/dojoengine/dojo.unreal) for:
- Plugin installation
- Blueprint integration
- C++ SDK usage

### Godot

See [dojo.godot documentation](https://github.com/dojoengine/dojo.godot) for:
- GDScript integration
- Signal-based subscriptions

## Client Integration Checklist

### Pre-Integration
- [ ] World deployed (`dojo-deploy` skill)
- [ ] Torii indexer running (`dojo-indexer` skill)
- [ ] World address recorded
- [ ] RPC endpoint accessible

### Setup
- [ ] SDK/package installed
- [ ] Bindings generated (`sozo build --typescript`)
- [ ] Manifest imported
- [ ] SDK initialized
- [ ] Test queries work

### Integration
- [ ] Entity reads working
- [ ] System executions working
- [ ] Subscriptions configured
- [ ] Error handling added

## Troubleshooting

### "Cannot connect to RPC"
- Verify RPC URL is correct
- Check Katana/Torii is running
- Verify network is reachable

### "World not found"
- Check world address is correct
- Verify world is deployed
- Check RPC is pointing to correct network

### "Model not found"
- Ensure model is deployed
- Check model name includes namespace (`dojo_starter-Position`)
- Verify entity exists with that key

## Next Steps

After client integration:
1. Test end-to-end workflow
2. Implement optimistic updates
3. Add error handling
4. Connect wallet for transactions

## Related Skills

- **dojo-deploy**: Deploy world first
- **dojo-indexer**: Set up Torii for queries
- **dojo-world**: Configure permissions
- **dojo-migrate**: Update client after migrations
