---
name: poker-game-router
description: Route requests for the Stacked Poker Next.js frontend repo to the right repo skill (Chakra UI/theme, thirdweb/SIWE auth, WebSockets/game state, chat/media, poker hand eval, QA/release). Use at the start of most tasks in this repo to decide which skill(s) to apply.
---

# Poker Game Router

Use this skill as a lightweight dispatcher. Keep context small: decide which skill(s) to use, then load only the chosen skill(s) and relevant files.

## Repo landmarks

- App Router entry: `app/layout.tsx`, `app/page.tsx`, `app/providers.tsx`
- Theme system: `app/theme.ts`
- Web3/thirdweb client: `app/thirdwebclient.ts`, `app/components/WalletButton.tsx`
- SIWE auth: `app/hooks/useWalletAuth.ts`, `app/contexts/AuthContext.tsx`, `app/hooks/server_actions.ts`
- WebSocket/game state: `app/contexts/WebSocketProvider.tsx`, `app/contexts/AppStoreProvider.tsx`, `app/hooks/server_actions.ts`
- Chat/media: `app/components/NavBar/Chat/`, `app/hooks/useTenor.ts`, `app/api/tenor/route.ts`
- Poker hand eval: `app/lib/poker/pokerHandEval.ts`
- Build hygiene: `package.json` scripts, `.eslintrc.json`, `.prettierrc`, `.husky/pre-commit`

## Skill selection (decision tree)

Pick the minimal set; multiple can apply.

### UI, layout, theme, Chakra components

Use `chakra-design-system` when:
- Editing `app/theme.ts` or Chakra tokens/variants
- Adding/modifying UI components under `app/components/`
- Fixing responsive layout, spacing, typography, color, dark/light mode
- Improving a11y for Chakra components (focus, aria, keyboard)

### Web3, wallets, thirdweb, embedded wallet, SIWE

Use `web3-thirdweb-siwe` when:
- Touching wallet connect flows, account state, auth cookies/session
- Working with `thirdweb/react` hooks (`useActiveAccount`, `useActiveWallet`, etc)
- Debugging auth loops, signature issues, disconnect behavior, or CSP issues
- Updating `next.config.js` CSP headers related to thirdweb embedded wallet

### “Quality bar” / production readiness

Use `frontend-quality-bar` when:
- Doing UI polish passes, UX consistency, performance, accessibility
- Adding new components/features that should meet a consistent standard
- Preparing a PR/merge, or doing broad refactors

## Use project rules and MCP

- Read `.cursor/rules/frontend-guidelines.mdc` for the repo’s frontend expectations.
- Read `.cursor/rules/thirdweb.mdc` for thirdweb rules and documentation pointers.
- See `.cursor/mcp.json` for MCP servers that can fetch thirdweb/Chakra documentation on demand.

