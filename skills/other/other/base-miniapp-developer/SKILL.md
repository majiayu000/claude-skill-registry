---
name: base-miniapp-developer
description: Build or migrate React/Next.js apps into Base/Coinbase Wallet Mini Apps using MiniKit + OnchainKit, while keeping thirdweb as the primary wallet/onboarding/payment integration; manage farcaster.json manifests, readiness, and gasless transactions.
---

# Base Mini App Developer

## Trigger
Use when the user needs to build, migrate, or troubleshoot Base Mini Apps, Coinbase Wallet Mini Apps, MiniKit, OnchainKit, Farcaster Mini Apps/Frames, or `farcaster.json` manifests; or when gasless Base transactions with Paymaster/Bundler are required.

## Guardrails
- Keep thirdweb as the primary wallet/onboarding/payment layer unless the user requests otherwise.
- No email/password auth. Wallet connection is the session.
- Do not use `window.ethereum` or `window.location`/`window.open`.
- MiniKit/OnchainKit hooks must be in client components (`'use client'`).
- Manifest must be reachable at `https://<domain>/.well-known/farcaster.json` over HTTPS.
- Call `setFrameReady()` once the UI is ready.

## Default conversion workflow (React/Next.js)
1. Identify router (App Router vs Pages) and where providers live.
2. Keep the existing thirdweb provider and add `OnchainKitProvider` with `miniKit.enabled`; import OnchainKit CSS.
3. Add a small `FrameReady` component to call `setFrameReady()` after mount.
4. Create and sign `farcaster.json`, then redeploy.
5. Keep thirdweb wallet/onboarding UI; only use OnchainKit UI components that do not replace wallet UX.
6. Replace external links with `useOpenUrl()` or MiniKit actions.
7. Add gasless tx flow (thirdweb AA/paymaster or OnchainKit Transaction + Paymaster).
8. Validate in Base Build Preview and test on device.

## Provider guidance
- Preferred Mini App context: `OnchainKitProvider` (`@coinbase/onchainkit`) with `miniKit={{ enabled: true }}`.
- Keep the thirdweb provider intact; make sure its connectors do not rely on injected `window.ethereum`.
- If the app already uses `@coinbase/minikit-react`, keep it unless asked to migrate.

## Thirdweb-first guidance
- Use thirdweb for onboarding and payments; do not replace with OnchainKit Wallet/Identity components unless requested.
- Prefer thirdweb connectors that work in a WebView (no injected provider assumption).
- Keep thirdweb chain config set to Base and reuse existing contract hooks/components.

## When the user says "convert this app"
- Install deps: `@coinbase/onchainkit`, `viem`, plus `@coinbase/minikit-react` only if needed.
- Keep existing thirdweb setup (providers, hooks, UI).
- Add manifest and placeholder assets; remind user to update domain and re-sign.
- Wire providers and readiness.
- Audit for `window.ethereum`/`window.location` usage and replace.

## References
- Manifest schema + signing: `references/manifest.md`
- Providers + readiness: `references/provider.md`
- MiniKit context & safety: `references/minikit.md`
- Navigation & social actions: `references/navigation.md`
- OnchainKit UI components: `references/onchainkit-components.md`
- Paymaster & gasless tx: `references/paymaster.md`
- thirdweb integration notes: `references/thirdweb.md`
