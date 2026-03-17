---
name: dojo-transactions
description: |
  Use when executing game actions and sending transactions in dojo.js.
  Triggers: send transaction, execute action, dojo action, contract call, DojoProvider,
  execute, sendMessage, batch transaction, invoke
---

# Dojo.js Transactions & Actions

## When to Use

Use this skill when:
- Executing game actions on-chain
- Sending typed messages
- Batching multiple transactions
- Handling transaction lifecycle

## DojoProvider.execute()

Execute contract calls using the DojoProvider:

```tsx
import { useDojoSDK } from "@dojoengine/sdk/react";
import { useAccount } from "@starknet-react/core";

function GameActions() {
    const { provider } = useDojoSDK();
    const { account } = useAccount();

    const spawn = async () => {
        const tx = await provider.execute(
            account,
            {
                contractName: "actions",
                entrypoint: "spawn",
                calldata: []
            },
            "game" // namespace
        );

        console.log("Transaction hash:", tx.transaction_hash);
    };

    const move = async (direction: number) => {
        const tx = await provider.execute(
            account,
            {
                contractName: "actions",
                entrypoint: "move",
                calldata: [direction]
            },
            "game"
        );
    };
}
```

## Batch Transactions

Execute multiple calls in a single transaction:

```tsx
const executeBatch = async () => {
    const tx = await provider.execute(
        account,
        [
            {
                contractName: "actions",
                entrypoint: "collect_resources",
                calldata: []
            },
            {
                contractName: "actions",
                entrypoint: "build_structure",
                // Calldata must match contract ABI types (u32, felt252, etc.)
                calldata: [structureType, x, y]
            }
        ],
        "game"
    );
};
```

## Typed Messages (Off-chain Signing)

Send signed messages without on-chain transactions:

```tsx
const { sdk } = useDojoSDK();

// Generate typed data
const typedData = sdk.generateTypedData(
    "game-Move", // namespace-ModelName
    {
        player: account.address,
        direction: 1,
        timestamp: Date.now()
    }
);

// Send signed message
const result = await sdk.sendMessage(typedData, account);

if (result.isOk()) {
    console.log("Message sent:", result.value);
} else {
    console.error("Failed:", result.error);
}
```

## Batch Messages

```tsx
const messages = [
    sdk.generateTypedData("game-Move", { direction: 1 }),
    sdk.generateTypedData("game-Move", { direction: 2 }),
    sdk.generateTypedData("game-Move", { direction: 3 })
];

const result = await sdk.sendMessageBatch(messages, account);
```

## Transaction with Optimistic Updates

```tsx
async function executeWithOptimism(action: string, calldata: any[]) {
    const { provider, useDojoStore } = useDojoSDK();
    const store = useDojoStore.getState();
    const transactionId = `${action}-${Date.now()}`;

    // Apply optimistic update - draft is a mutable copy of your store state
    store.applyOptimisticUpdate(transactionId, (draft) => {
        // Example: update player position optimistically
        const player = draft.entities[account.address];
        if (player?.models?.game?.Position) {
            player.models.game.Position.x = newX;
            player.models.game.Position.y = newY;
        }
    });

    try {
        const tx = await provider.execute(
            account,
            { contractName: "actions", entrypoint: action, calldata },
            "game"
        );

        // Wait for transaction to be accepted
        await account.waitForTransaction(tx.transaction_hash);

        store.confirmTransaction(transactionId);
    } catch (error) {
        store.revertOptimisticUpdate(transactionId);
        throw error;
    }
}
```

## Direct Contract Calls (Read-only)

```tsx
const { provider } = useDojoSDK();

// Call view function
const result = await provider.call(
    "game", // namespace
    {
        contractName: "actions",
        entrypoint: "get_player_stats",
        calldata: [playerAddress]
    }
);
```

## Auto-generated Action Methods

DojoProvider generates typed methods from your manifest.json at initialization. Available methods correspond to your contract's systems - check your manifest or use TypeScript autocomplete to discover them.

```tsx
// Methods are generated based on your contract definitions in manifest.json
// If your contract has a "spawn" system, you can call it directly:
const tx = await provider.spawn(account);

// For actions with arguments:
const tx = await provider.move(account, { direction: 1 });

// For view functions (no account needed):
const stats = await provider.get_stats({ player: address });
```

## Transaction Options

```tsx
const tx = await provider.execute(
    account,
    call,
    "game",
    {
        maxFee: "0x1000000000", // Max fee in wei
        nonce: 5,              // Explicit nonce
        version: 1,            // Transaction version
    }
);
```

## Error Handling

```tsx
try {
    const tx = await provider.execute(account, call, "game");
    await account.waitForTransaction(tx.transaction_hash);
} catch (error) {
    if (error.message.includes("insufficient funds")) {
        console.error("Not enough ETH for gas");
    } else if (error.message.includes("nonce")) {
        console.error("Nonce mismatch - retry");
    } else {
        console.error("Transaction failed:", error);
    }
}
```

## Common Pitfalls

1. **Missing account**: Always check account is connected before executing
2. **Wrong namespace**: Must match the contract's namespace in manifest
3. **Calldata format**: Use proper types (BigInt for felts, strings for addresses)
4. **Gas estimation**: For complex operations, set explicit maxFee
5. **Nonce issues**: Don't send multiple transactions without waiting for confirmation
