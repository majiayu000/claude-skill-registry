---
name: viem-celo
description: 'Viem with Celo chain configuration. Use when working with Celo blockchain interactions, public client setup, contract reads/writes, transaction encoding, or feeCurrency. Triggers on: "viem", "celo client", "publicClient", "readContract", "writeContract", "encodeFunctionData", "feeCurrency", "celo RPC".'
---

## Project Setup

### Public Client (`apps/api/src/lib/celo-client.ts`)

```ts
import { createPublicClient, http } from 'viem';
import { celo } from 'viem/chains';

export const celoClient = createPublicClient({
  chain: celo,
  transport: http(process.env.CELO_RPC_URL || 'https://forno.celo.org'),
});
```

## Chain Config

- **Chain**: Celo Mainnet
- **Chain ID**: 42220
- **Import**: `import { celo } from 'viem/chains'`
- **Default RPC**: `https://forno.celo.org`
- **Block time**: ~5 seconds

## Common Patterns

### Reading Contracts

```ts
const result = await celoClient.readContract({
  address: CONTRACT_ADDRESS,
  abi: contractAbi,
  functionName: 'someFunction',
  args: [arg1, arg2],
});
```

### Encoding Transaction Data

```ts
import { encodeFunctionData } from 'viem';

const data = encodeFunctionData({
  abi: contractAbi,
  functionName: 'swapIn',
  args: [provider, exchangeId, tokenIn, tokenOut, amountIn, minAmountOut],
});
```

### Format / Parse Units

```ts
import { formatUnits, parseUnits } from 'viem';

// Mento tokens: 18 decimals
formatUnits(1000000000000000000n, 18); // "1.0"
parseUnits('100', 18); // 100000000000000000000n

// USDC/USDT: 6 decimals
formatUnits(1000000n, 6); // "1.0"
parseUnits('100', 6); // 100000000n
```

### Address Types

Always use `Address` type from viem for addresses:

```ts
import type { Address } from 'viem';

const addr: Address = '0x765DE816845861e75A25fCA122bb6898B8B1282a';
```

## Celo-Specific: feeCurrency (CIP-64)

Celo supports paying gas fees in tokens other than CELO. Use the `feeCurrency` field:

```ts
const hash = await walletClient.sendTransaction({
  to: '0x...',
  data: '0x...',
  feeCurrency: '0x765DE816845861e75A25fCA122bb6898B8B1282a', // Pay gas in USDm
});
```

Common fee currencies on Celo:
- USDm (cUSD): `0x765DE816845861e75A25fCA122bb6898B8B1282a`
- USDC: `0xcebA9300f2b948710d2653dD7B07f33A8B32118C`

## Environment Variables

| Variable | Description |
|---|---|
| `CELO_RPC_URL` | Celo RPC endpoint (defaults to `https://forno.celo.org`) |

## Important Notes

- All Mento stablecoin tokens use 18 decimals
- USDC and USDT on Celo use 6 decimals
- Use `getTokenDecimals()` from `packages/shared` to get correct decimals
- Always lowercase addresses when using them as map keys
- The project uses viem v2 — check `package.json` for exact version
