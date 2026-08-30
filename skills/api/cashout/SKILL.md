---
name: cashout
description: "Sell Base USDC for fiat with cashout from @usdctofiat/offramp. Use when a user wants a non-custodial cash-out from a real Base wallet into Venmo, Revolut, PayPal, Zelle, Monzo, Chime, or Mercado Pago. Require an explicit fast or best mode. Cash App new creation is disabled in the SDK."
---

# USDCtoFiat cash-out

Use `@usdctofiat/offramp` to call `cashout({ mode: "fast" | "best" })` with a real viem `WalletClient` on Base (`chain_id: 8453`). Require the user to choose a mode.

> **Payment-policy boundary:** SDK support proves technical compatibility, not permission from a payment provider. Wise currently prohibits receiving P2P crypto-sale payments. PayPal may require preapproval for cryptocurrency-related payments. Read the provider's current first-party policy before offering a route.

## Fast or Best

| Mode   | Fee                                 | Pricing                    |
| ------ | ----------------------------------- | -------------------------- |
| `fast` | 0% spread / 0 bps                   | Live oracle route (TOFIAT) |
| `best` | Delegate manager fee 10 bps on USDC | Delegate rate-manager path |

```ts
import { cashout } from "@usdctofiat/offramp";
import type { WalletClient } from "viem";

export async function sellUsdc(signer: WalletClient) {
  return cashout({
    mode: "fast",
    signer,
    amount: "100",
    currency: "EUR",
    platform: "revolut",
    payee: "alice",
  });
}
```

```ts
const fast = await cashout({ ...input, mode: "fast" });
const best = await cashout({ ...input, mode: "best" });
```

Strings and numbers are human USDC amounts. A `bigint` is exact six-decimal base units. The helper is production-only and requires an explicit mode.

Persist `depositId` immediately. Fast `depositId` is the composite resume key for `createOfframp().watch()`. Best `depositId` is the numeric EscrowV2 id for `deposits()` / `close()`.

## Amounts

Both floors ship from the package root. Fast rejects an amount under the hard floor before submission; the practical floor is advice the SDK does not enforce.

| Bound                            | Base units | USDC | Meaning                                                                          |
| -------------------------------- | ---------- | ---- | -------------------------------------------------------------------------------- |
| `MIN_CASHOUT_AMOUNT`             | `10000n`   | 0.01 | Hard floor; below one cent a deposit is dust and can never fill                  |
| `RECOMMENDED_MIN_CASHOUT_AMOUNT` | `1000000n` | 1    | Practical floor; a sub-1-USDC deposit forces min==max fills and starves matching |

Ask for a larger amount rather than creating a deposit under the practical floor. Nothing fails loudly, so the deposit is created and then sits unfilled.

## Rails

Every rail in `PLATFORMS`. The Offer column is this skill's routing guidance, not an SDK field: a no rail is still a real `PLATFORMS` entry, so read the reason before assuming the SDK will reject it.

| Rail         | Offer | Why                                                            |
| ------------ | ----- | -------------------------------------------------------------- |
| Venmo        | yes   |                                                                |
| Revolut      | yes   |                                                                |
| PayPal       | yes   | May require provider preapproval for cryptocurrency payments   |
| Zelle        | yes   |                                                                |
| Monzo        | yes   |                                                                |
| Chime        | yes   |                                                                |
| Mercado Pago | yes   |                                                                |
| Wise         | no    | Published P2P crypto-sale prohibition; the SDK still allows it |
| Cash App     | no    | Held in the SDK's own `OFFRAMP_DISABLED_PAYMENT_PLATFORMS`     |

A yes rail is offerable, not preapproved. The payment-policy boundary above still applies, and currencies and payee identifier rules come from the SDK, not from this table.

## Disabled rails

`OFFRAMP_DISABLED_PAYMENT_PLATFORMS` is the SDK's own rail kill-switch and currently holds `cashapp`. A disabled rail is dropped from capability discovery and rejected before any deposit transaction, whatever the host passes, so do not offer Cash App. Test with `isPaymentPlatformDisabled` and surface `DISABLED_PAYMENT_PLATFORM_MESSAGE` instead of inventing copy.

A host adds its own rollout gate with `disabledPlatforms`, on `createOfframp()` or per call. Display names and separator variants canonicalize, so `Cash App`, `cash-app` and `cash_app` all hit the same gate.

```ts
// hostRollout.disabledRails is the host's own list, not an SDK default.
const order = await cashout({ ...input, mode: "fast", disabledPlatforms: hostRollout.disabledRails });
```

## createOfframp()

Attribution is configured by `@usdctofiat/offramp`.

```ts
import { createOfframp } from "@usdctofiat/offramp";

export async function watchCashout(depositId: string) {
  const client = createOfframp();
  for await (const order of client.watch(depositId)) {
    if (!order.isInFlight) return order;
  }
}
```

## Install

```bash
npm install @usdctofiat/offramp@9.0.0
```

```ts
import { OFFRAMP_DEVELOPER_RESOURCES, getOfframpDeveloperResources } from "@usdctofiat/offramp";

OFFRAMP_DEVELOPER_RESOURCES.delegation.required; // false
OFFRAMP_DEVELOPER_RESOURCES.delegation.feeRateBps; // 10
```

## Errors

Managed-path errors extend `OfframpError` with a typed `code`:

| Code                              | Meaning                                  | Recovery                                                       |
| --------------------------------- | ---------------------------------------- | -------------------------------------------------------------- |
| `VALIDATION`                      | Bad input                                | Fix the input                                                  |
| `APPROVAL_FAILED`                 | USDC approve reverted or wallet rejected | Retry or top up gas                                            |
| `REGISTRATION_FAILED`             | Curator rejected the maker               | Surface the `cause`                                            |
| `EXTENSION_REGISTRATION_REQUIRED` | Route needs an extension handshake       | `usePeerExtensionRegistration(platform)` or `peerExtensionSdk` |
| `DEPOSIT_FAILED`                  | Escrow create reverted                   | Check USDC balance, nonce, chain                               |
| `CONFIRMATION_FAILED`             | Post-deposit confirmation missed         | Call `cashout()` again; it resumes                             |
| `DELEGATION_FAILED`               | `setRateManager` failed                  | Call again; Best resumes from delegation                       |
| `USER_CANCELLED`                  | Wallet rejected a prompt                 | Do not retry automatically                                     |
| `UNSUPPORTED`                     | Non-Base chain or missing client         | Switch network / pass a Base `WalletClient`                    |

`usePeerExtensionRegistration` ships from the `@usdctofiat/offramp/react` subpath, not the package root. Non-React callers use the root `peerExtensionSdk`.

Progress callback via `onProgress: (p) => void` with `step` values: `approving`, `registering`, `depositing`, `confirming`, `protecting`, `delegating`, `restricting`, `resuming`, `done`.

## Rules

- Call `cashout({ mode: "fast" | "best" })` on a real Base wallet and require an explicit mode.
- Never log `walletClient` or private keys.
- Do not invent a sandbox. Production Base only.
- Read platform identifier rules from `PLATFORMS`; do not copy a stale list.
- Check the amount against `RECOMMENDED_MIN_CASHOUT_AMOUNT` before creating a deposit; a smaller one is accepted and then starves matching.
- Do not offer Wise while its published P2P crypto-sale prohibition applies.
- Never pass `otcTaker` on a fresh cash-out. The protocol cannot create a deposit paused and private in one transaction, so 9.0.0 rejects it with `UNSUPPORTED`.
- Restrict an already-confirmed undelegated deposit with `enableOtc`, and lift it with `disableOtc`.
