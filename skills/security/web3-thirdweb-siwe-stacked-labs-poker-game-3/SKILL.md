---
name: web3-thirdweb-siwe
description: Implement and debug wallet connection and authentication in this repo using thirdweb v5 and the SIWE-style flow in `app/hooks/useWalletAuth.ts` and `app/hooks/server_actions.ts`. Use for ConnectButton setup, account state, signature/auth verification, Base/USDC config, and CSP issues with embedded wallet.
---

# Web3 (thirdweb v5) + SIWE Auth (Stacked Poker)

## Repo entry points

- thirdweb client + wallets: `app/thirdwebclient.ts`
- Provider wiring: `app/providers.tsx`
- Connect UI: `app/components/WalletButton.tsx`
- Auth orchestration: `app/hooks/useWalletAuth.ts`, `app/contexts/AuthContext.tsx`
- Backend calls: `app/hooks/server_actions.ts`
- Security headers / embedded wallet frames: `next.config.js`

## Documentation sources (don’t paste full docs)

- thirdweb LLM docs (per repo rules): https://portal.thirdweb.com/llms.txt
- thirdweb full LLM docs: https://portal.thirdweb.com/llms-full.txt
- thirdweb API docs: https://api.thirdweb.com/llms.txt
- Use the `thirdweb-api` MCP server (see `.cursor/mcp.json`) for up-to-date references.

## Debug workflow (common issues)

1. Confirm env is set:
   - `NEXT_PUBLIC_THIRDWEB_CLIENT_ID`
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_WS_URL`
2. Confirm CSP allows thirdweb embedded wallet frames and network:
   - `frame-src` includes `https://embedded-wallet.thirdweb.com`
   - `connect-src` allows required hosts
3. Trace auth flow:
   - `getAuthPayload(address)` → returns `{ payload, message }`
   - `account.signMessage({ message })` (sign the *message string*)
   - `verifySignedPayload({ payload, signature })`
   - On failure, disconnect wallet and clear attempt ref

## Mini App notes (Coinbase Wallet / Base)
- Use `ConnectButton` or `ConnectEmbed` for wallet UI. `ConnectEmbed` is the same UI as the modal, but inline, which is useful for an embedded sign-in screen in a Mini App.
- Configure wallets explicitly via the `wallets` prop; include `inAppWallet()` and any target wallets (ex: `createWallet("com.coinbase.wallet")`).
- The Connect UI supports 500+ wallets and in-app wallets, so keep a short, curated list for Mini App UX.
- The Connect UI can optionally include Auth (SIWE-style), which can be wired to your existing server endpoints.
- Inference: WebViews typically don’t have browser extensions, so don’t rely on auto-detected EIP-6963 extensions; prefer explicit wallet configuration.

## What to load next

- For the repo’s exact auth sequence and edge cases: read `references/auth-flow.md`.
- For CSP gotchas (embedded wallet / Turnstile / Tenor): read `references/csp-and-headers.md`.
- To quickly sanity-check env vars: run `scripts/check-web3-env.sh`.
