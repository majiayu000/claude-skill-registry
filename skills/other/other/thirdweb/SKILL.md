---
name: thirdweb
description: 'Thirdweb v5 SDK usage in AutoClaw. Use when working with wallet connection, social login, SIWE authentication, or thirdweb client/provider setup. Triggers on: "thirdweb", "wallet connect", "inAppWallet", "social login", "SIWE", "ConnectButton", "thirdweb auth", "thirdweb provider".'
---

## Critical: Thirdweb v5 Sub-Path Imports

Thirdweb v5 uses sub-path imports. Never import from the root `thirdweb` package for specialized modules:

```ts
// CORRECT
import { createThirdwebClient } from 'thirdweb';
import { inAppWallet, createWallet } from 'thirdweb/wallets';
import { darkTheme } from 'thirdweb/react';
import { createAuth } from 'thirdweb/auth';
import { privateKeyToAccount } from 'thirdweb/wallets';

// WRONG — do not import wallet/auth/react from root
import { inAppWallet } from 'thirdweb'; // ❌
```

## Project Setup

### Client (Web — `apps/web/src/lib/thirdweb.ts`)

```ts
import { createThirdwebClient } from 'thirdweb';

export const client = createThirdwebClient({
  clientId: process.env.NEXT_PUBLIC_THIRDWEB_CLIENT_ID!,
});
```

### Client (API — `apps/api/src/lib/thirdweb.ts`)

```ts
import { createThirdwebClient } from 'thirdweb';

export const thirdwebClient = createThirdwebClient({
  secretKey: process.env.THIRDWEB_SECRET_KEY,
});
```

### Wallets Configuration

```ts
import { inAppWallet, createWallet } from 'thirdweb/wallets';

export const wallets = [
  inAppWallet({
    auth: { options: ['email', 'google', 'apple', 'passkey'] },
  }),
  createWallet('io.metamask'),
  createWallet('com.coinbase.wallet'),
  createWallet('walletConnect'),
];
```

### SIWE Auth (Server-Side)

```ts
import { createAuth } from 'thirdweb/auth';
import { privateKeyToAccount } from 'thirdweb/wallets';

const adminAccount = privateKeyToAccount({
  client: thirdwebClient,
  privateKey: process.env.THIRDWEB_ADMIN_PRIVATE_KEY as `0x${string}`,
});

export const thirdwebAuth = createAuth({
  domain: process.env.AUTH_DOMAIN,
  client: thirdwebClient,
  adminAccount,
});
```

Auth flow: `thirdwebAuth.generatePayload()` → client signs → `thirdwebAuth.verifyPayload()` → JWT via `thirdwebAuth.generateJWT()`.

### Provider Stack (Web)

Wrap app with `QueryClientProvider` (from `@tanstack/react-query`) + `ThirdwebProvider`:

```tsx
import { ThirdwebProvider } from 'thirdweb/react';

<QueryClientProvider client={queryClient}>
  <ThirdwebProvider>{children}</ThirdwebProvider>
</QueryClientProvider>
```

## Theme

This project uses `darkTheme()` from `thirdweb/react` with custom indigo accent colors. See `apps/web/src/lib/thirdweb.ts` for the full theme config.

## Environment Variables

| Variable | Location | Description |
|---|---|---|
| `NEXT_PUBLIC_THIRDWEB_CLIENT_ID` | Web | Public client ID |
| `THIRDWEB_SECRET_KEY` | API | Server-side secret key |
| `THIRDWEB_ADMIN_PRIVATE_KEY` | API | Admin wallet for SIWE signing |
| `AUTH_DOMAIN` | API | SIWE auth domain |

## Key Hooks

- `useActiveAccount()` — Get connected wallet account
- `useActiveWallet()` — Get connected wallet instance
- `useConnect()` — Connect a wallet programmatically
- `useDisconnect()` — Disconnect current wallet

## Chain Configuration

This project targets Celo mainnet (chain ID 42220). When using `ConnectButton`, set `chain={celo}` from `thirdweb/chains`.
