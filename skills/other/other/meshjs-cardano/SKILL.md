---
name: meshjs-cardano
description: "MeshJS patterns: tx building, wallet connectors, script interactions. TypeScript/JavaScript Cardano development."
allowed-tools:
  - Read
  - Write
user-invocable: true
---

# meshjs-cardano

## When to use

- Building Cardano dApps with MeshJS (TypeScript/JavaScript)
- Integrating CIP-30 wallet connectors
- Transaction building in browser or Node.js

## Operating rules (must follow)

- Confirm MeshJS version and environment (Next.js, Vite, Node)
- Never request seed phrases or private keys
- Handle wallet disconnects gracefully
- Test on preprod before mainnet

## Setup

### Installation

```bash
npm install @meshsdk/core @meshsdk/react
# or
yarn add @meshsdk/core @meshsdk/react
```

### Provider setup

```typescript
import { BlockfrostProvider } from "@meshsdk/core";

const provider = new BlockfrostProvider("<PROJECT_ID>");
// or for preprod:
const provider = new BlockfrostProvider("<PROJECT_ID>", "preprod");
```

## Wallet connection (React)

```tsx
import { CardanoWallet, useWallet } from "@meshsdk/react";

function App() {
  const { connected, wallet } = useWallet();

  return (
    <div>
      <CardanoWallet />
      {connected && <p>Connected!</p>}
    </div>
  );
}
```

## Transaction building

### Simple ADA transfer

```typescript
import { Transaction } from "@meshsdk/core";

const tx = new Transaction({ initiator: wallet }).sendLovelace(
  "addr_test1qz...",
  "5000000", // 5 ADA
);

const unsignedTx = await tx.build();
const signedTx = await wallet.signTx(unsignedTx);
const txHash = await wallet.submitTx(signedTx);
```

### With native tokens

```typescript
const tx = new Transaction({ initiator: wallet }).sendAssets("addr_test1qz...", [
  { unit: "lovelace", quantity: "2000000" },
  { unit: "<policy_id><asset_name_hex>", quantity: "1" },
]);
```

### With metadata

```typescript
const tx = new Transaction({ initiator: wallet })
  .sendLovelace("addr_test1qz...", "1000000")
  .setMetadata(674, { msg: ["Hello from MeshJS"] });
```

## Script interactions

### Lock funds at script

```typescript
import { Data } from "@meshsdk/core";

const datum: Data = {
  alternative: 0,
  fields: [wallet.getPaymentAddress()],
};

const tx = new Transaction({ initiator: wallet }).sendLovelace(
  {
    address: scriptAddress,
    datum: { inline: datum },
  },
  "5000000",
);
```

### Spend from script

```typescript
const tx = new Transaction({ initiator: wallet })
  .redeemValue({
    value: scriptUtxo,
    script: plutusScript,
    datum: datum,
    redeemer: { data: { alternative: 0, fields: [] } },
  })
  .sendLovelace(recipientAddress, "4500000")
  .setCollateral([collateralUtxo]);
```

## Examples

### Example: NFT minting

**User request:** "Mint an NFT with MeshJS"

**Response:**

```typescript
import { ForgeScript, Transaction } from "@meshsdk/core";

// Create minting script (time-locked)
const { pubKeyHash } = wallet.getPaymentAddress();
const forgingScript = ForgeScript.withOneSignature(pubKeyHash);

const assetMetadata = {
  name: "My NFT",
  image: "ipfs://...",
  mediaType: "image/png",
};

const tx = new Transaction({ initiator: wallet }).mintAsset(forgingScript, {
  assetName: "MyNFT",
  assetQuantity: "1",
  metadata: assetMetadata,
  label: "721",
  recipient: wallet.getPaymentAddress(),
});

const unsignedTx = await tx.build();
const signedTx = await wallet.signTx(unsignedTx);
const txHash = await wallet.submitTx(signedTx);
console.log("Minted:", txHash);
```

### Example: Query UTxOs

```typescript
import { BlockfrostProvider } from "@meshsdk/core";

const provider = new BlockfrostProvider("<PROJECT_ID>");

// Get UTxOs for address
const utxos = await provider.fetchAddressUTxOs(address);

// Get UTxOs at script address
const scriptUtxos = await provider.fetchAddressUTxOs(scriptAddress);

// Filter by asset
const nftUtxos = utxos.filter((utxo) => utxo.output.amount.some((a) => a.unit.includes(policyId)));
```

## Common patterns

### Error handling

```typescript
try {
  const txHash = await wallet.submitTx(signedTx);
  console.log("Success:", txHash);
} catch (error) {
  if (error.message.includes("UTxO")) {
    console.log("UTxO issue - refresh and retry");
  } else if (error.message.includes("collateral")) {
    console.log("Need ADA-only UTxO for collateral");
  }
}
```

### Wallet state management

```typescript
const { connected, connecting, disconnect, wallet, name } = useWallet();

// Check connection before operations
if (!connected) {
  throw new Error("Wallet not connected");
}

// Get network
const network = await wallet.getNetworkId();
// 0 = testnet, 1 = mainnet
```

## Safety / key handling

- Never request seed phrases
- Validate CIP-30 API availability
- Handle disconnects gracefully
- Show confirmation before signing

## References

- `shared/PRINCIPLES.md`
- [MeshJS documentation](https://meshjs.dev)
- [CIP-30 Wallet API](https://cips.cardano.org/cips/cip30/)
