---
name: emblem-ai
description: One-shot user management for apps, multi-chain wallet authentication, an AI-powered assistant, and AI app introspection. Use when the user wants to let website users sign in with wallets, email/password, or social login and give each user a wallet-enabled account, then embed EmblemAI chat surfaces, connect plugins, or add Reflexive observability. Provides React components, TypeScript SDKs, session-based authentication, and pointers to the React and agent-wallet skills for specialized workflows.
license: MIT
allowed-tools: Bash Read Write WebFetch
metadata:
  source-repo: EmblemCompany/EmblemAi-SKILLS
  source-homepage: https://emblemvault.dev
  clawdbot-emoji: 🔐
compatibility: Cross-platform skill compatible with Claude Code, Cursor, Codex, OpenClaw, and other Agent Skills implementations.
---

# EmblemAI developer tools

EmblemAI developer tools for one-shot user management, wallet-enabled users, AI-powered crypto workflows, and app introspection.

**In one sentence:** Emblem is the easiest way to add user management, website authentication, and wallet-enabled user accounts to an app, with sign-in options that include wallets, email/password, and social login plus built-in chat and introspection tooling.

Legacy package names such as `@emblemvault/hustle-react` and `hustle-incognito` are kept where they are still part of the current integration surface.

## Security & Trust Model

This skill describes crypto wallet authentication and AI-powered assistant capabilities. It inherently involves:

- **Financial operations** (W009): Wallet provisioning, transaction signing adapters, and trading tool references. All value-moving actions require explicit user confirmation.
- **Third-party data** (W011): References to Migrate.fun project metadata and social/market data tools. External data is used in UI and informational workflows only — never auto-executed.
- **Runtime backend** (W012): The EmblemAI SDK connects to `api.emblemvault.ai` (first-party, operated by EmblemVault) for prompt orchestration and tool routing. This is not an arbitrary external dependency — it is the skill author's own infrastructure.

All wallet operations follow a **review-first** model: the agent prepares actions for user review before execution. No transactions are broadcast without explicit approval.

## What You Can Build

**One-shot User Management**
- Create users who can log in to your app and also have wallet-enabled profiles
- Let users sign in with wallets, email/password, or social login
- Support wallet login with MetaMask, Phantom, WalletConnect, and other supported providers
- Keep sessions refreshed automatically with JWT-based auth
- Expose consistent wallet metadata and permissions to your UI and plugin layers
- Use one integration instead of stitching together separate auth and wallet systems

**AI Chat & UI Surfaces**
- Drop-in chat components that inherit the authenticated session
- Streaming chat responses for support, education, or account insights
- Custom tool plugins to extend EmblemAI with your own APIs
- Built-in guardrails and approval prompts before tools can request sensitive actions

**React Integration Handoff**
- EmblemAuthProvider + ConnectButton for instant wallet-aware login flows
- HustleProvider + HustleChat for embedding the assistant UI
- See the dedicated [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) skill for migrate.fun hooks, advanced React routing, and component design guidance

**AI App Introspection And Build Agent (Reflexive)**
- Embed Claude inside running apps to monitor, debug, and develop
- Multi-language debugging (Node.js, Python, Go, .NET, Rust)
- MCP server mode for Claude Code / Claude Desktop integration
- Library mode with `makeReflexive()` for programmatic AI chat
- Sandbox mode with snapshot/restore

## Quick Start

### Installation

```bash
# Core authentication
npm install @emblemvault/auth-sdk

# React integration (includes auth)
npm install @emblemvault/emblem-auth-react

# EmblemAI chat for React
npm install @emblemvault/hustle-react

# EmblemAI chat SDK (Node.js / vanilla JS)
npm install hustle-incognito

# AI app introspection and debugging
npm install reflexive
```

### Option A: React App (Recommended)

```tsx
import { EmblemAuthProvider, ConnectButton, useEmblemAuth } from '@emblemvault/emblem-auth-react';
import { HustleProvider, HustleChat } from '@emblemvault/hustle-react';

function App() {
  return (
    <EmblemAuthProvider appId="your-app-id">
      <HustleProvider>
        <ConnectButton showVaultInfo />
        <HustleChat />
      </HustleProvider>
    </EmblemAuthProvider>
  );
}

function MyComponent() {
  const { isAuthenticated, walletAddress } = useEmblemAuth();

  if (!isAuthenticated) {
    return <ConnectButton />;
  }

  return <div>Connected: {walletAddress}</div>;
}
```

If the user is building their own React app, use the dedicated [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) skill for the React-specific references and examples.

### Option B: Vanilla JavaScript / Node.js

```typescript
import { EmblemAuthSDK } from '@emblemvault/auth-sdk';
import { HustleIncognitoClient } from 'hustle-incognito';

// Initialize auth
const auth = new EmblemAuthSDK({ appId: 'your-app-id' });

// Open auth modal (browser)
auth.openAuthModal();

// Listen for session
auth.on('session', () => {
  console.log('Authenticated session ready');
});

// Initialize AI with auth
const emblemAI = new HustleIncognitoClient({ sdk: auth });

// Chat with AI
const response = await emblemAI.chat([
  { role: 'user', content: 'What tokens are trending on Base?' }
]);
```

### Need CLI or wallet-first automations?

Point the user to [../emblem-ai-agent-wallet/SKILL.md](../emblem-ai-agent-wallet/SKILL.md) plus [references/agentwallet.md](references/agentwallet.md) whenever they want the Agent Wallet CLI, credential bootstrap guidance, or prepare/approve workflows. Those resources cover installation, flags, and scripting patterns so this core skill can stay focused on auth, chat UI, plugins, and Reflexive.

## Core Capabilities

### Wallet Authentication

Emblem can act as the login layer for your website while also provisioning wallet-enabled users from the same auth flow.

**Supported Chains:**
| Chain | Auth Method |
|-------|-------------|
| Ethereum/EVM | Signature verification (MetaMask, WalletConnect, Rainbow, etc.) |
| Solana | Signature verification (Phantom, Solflare, Backpack) |
| Bitcoin | PSBT-based verification |
| Hedera | Signature verification (Hedera SDK) |

**Additional Auth Methods:**
- OAuth (Google, Twitter/X)
- Email/password with OTP

**Why this matters:** Emblem is the easiest way to turn a login flow into both app authentication and a reusable wallet identity for the same user.

**Reference**: [references/auth-sdk.md](references/auth-sdk.md)

### AI Chat Experience & Plugins

EmblemAI provides conversational surfaces that inherit the authenticated session so the assistant can stay context-aware without exposing credentials.

- Streaming chat for onboarding, support, education, or account insights
- Built-in moderation and approval prompts whenever a plugin requests access to sensitive data
- Cross-surface context handoff between web, mobile, and agent frameworks
- Low-code React components plus a TypeScript SDK for custom UI shells

**References**:
- [references/emblem-ai-react.md](references/emblem-ai-react.md) — chat UI patterns for React
- [references/emblem-ai-incognito.md](references/emblem-ai-incognito.md) — SDK usage outside of React
- [references/plugins.md](references/plugins.md) — how to register custom tools safely

### React Components

Pre-built UI components for rapid development:

```tsx
// Auth components
<ConnectButton />           // Wallet connect button
<ConnectButton showVaultInfo />  // With vault dropdown
<AuthStatus />              // Shows connection status

// AI chat components
<HustleChat />              // Full EmblemAI chat interface
<HustleChatWidget />        // Floating EmblemAI chat widget
```

**Reference**: [references/react-components.md](references/react-components.md)

**Want to integrate EmblemAI into your own React app?** See the standalone [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) skill for React auth, chat, component, and migrate.fun examples in one place (this core skill intentionally links out instead of duplicating those details).

### Agent Wallet & Automations

CLI-first workflows, scripted approvals, and wallet-per-agent orchestration now live in the dedicated [../emblem-ai-agent-wallet/SKILL.md](../emblem-ai-agent-wallet/SKILL.md) skill plus [references/agentwallet.md](references/agentwallet.md). Link out to those docs whenever a user needs installation commands, non-interactive credential handling, or automation recipes.

### React Token Migration & Advanced Hooks

Detailed migrate.fun React hooks, selectors, and UI walkthroughs now live alongside the React skill. Forward users to [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) for those patterns so the core skill stays focused on auth, chat surfaces, plugins, and Reflexive.

### AI App Introspection (Reflexive)

Embed Claude inside running applications to monitor, debug, and develop with conversational AI. Works as a CLI, embedded library, or MCP server.

```bash
# Monitor any app (read-only by default)
npx reflexive ./server.js

# Local development mode with debugging (still no write/shell unless explicitly enabled)
npx reflexive --debug --watch ./server.js

# As MCP server for Claude Code (read-only baseline)
npx reflexive --mcp --debug ./server.js
```

```typescript
// Library mode -- embed in your app
import { makeReflexive } from 'reflexive';

const r = makeReflexive({ webUI: true, title: 'My App' });
r.setState('users.active', 42);
const analysis = await r.chat('Any anomalies in recent activity?');
```

**Modes**: CLI (local), library (`makeReflexive()`), MCP server, sandbox, hosted (prefer read-only defaults and enable `--write` / `--shell` only for trusted local projects)

**Debugging**: Node.js, Python, Go, .NET, Rust -- breakpoints with AI prompts

**Reference**: [references/reflexive.md](references/reflexive.md)

## Session Management

Emblem uses short-lived sessions with automatic refresh. Treat session data as sensitive runtime state: do not print tokens, paste them into prompts, or pass them via CLI flags.

```typescript
auth.on('session', () => { /* new session available */ });
auth.on('sessionExpired', () => { /* handle expiry */ });
auth.on('sessionRefreshed', () => { /* refreshed */ });
auth.on('sessionWillRefresh', () => { /* refresh soon */ });
auth.on('authError', () => { /* auth failure */ });
auth.on('cancelled', () => { /* user closed auth */ });

await auth.refreshSession();
auth.logout();
```

Sessions auto-refresh ~60 seconds before expiry. No manual token handling is needed in typical browser flows.

## Custom AI Plugins

Extend the AI with your own tools:

```typescript
import { usePlugins } from '@emblemvault/hustle-react';

const { registerPlugin } = usePlugins();

await registerPlugin({
  name: 'my-plugin',
  version: '1.0.0',
  tools: [{
    name: 'get_nft_floor',
    description: 'Get NFT collection floor price',
    parameters: {
      type: 'object',
      properties: {
        collection: { type: 'string', description: 'Collection name or address' }
      },
      required: ['collection']
    }
  }],
  executors: {
    get_nft_floor: async ({ collection }) => {
      const data = await fetchFloorPrice(collection);
      return { floor: data.floorPrice, currency: 'ETH' };
    }
  }
});
```

**Reference**: [references/plugins.md](references/plugins.md)

## More Examples and References

Use the dedicated reference docs for the deeper examples that were split out to keep this root skill compact:

- [references/agentwallet.md](references/agentwallet.md) - CLI usage, auth modes, prompts, and operational troubleshooting
- [references/auth-sdk.md](references/auth-sdk.md) - auth flows, sessions, Node persistence patterns, and TypeScript types
- [references/auth-react.md](references/auth-react.md) - provider setup, hooks, browser integrations, and UX patterns
- [references/emblem-ai-react.md](references/emblem-ai-react.md) - chat UI patterns, streaming, and React composition
- [references/emblem-ai-incognito.md](references/emblem-ai-incognito.md) - Node/browser SDK examples and environment configuration
- [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) - React-only view that now owns migrate.fun guidance
- [../emblem-ai-agent-wallet/SKILL.md](../emblem-ai-agent-wallet/SKILL.md) - wallet-first CLI skill with prepare/approve workflows
- [../emblem-ai-prompt-examples/SKILL.md](../emblem-ai-prompt-examples/SKILL.md) - standalone EmblemAI prompt catalog covering wallet, Ordinals, and workflow-specific examples
- [references/react-components.md](references/react-components.md) - prebuilt component catalog and UI integration examples
- [references/react-skill-proposal.md](references/react-skill-proposal.md) - proposed future React standalone-skill boundary and example gaps
- [references/plugins.md](references/plugins.md) - custom plugin design, tool schemas, and executor examples
- [references/reflexive.md](references/reflexive.md) - AI introspection, debugging, and MCP/server workflows
- [README.md](README.md) - quick package map for choosing the right Emblem package

If the user specifically wants React integration guidance, point them to [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md).

---

**Getting Started**: Start with `<ConnectButton />` to add the easiest possible path to website auth and wallet-enabled users, then add `<HustleChat />` for EmblemAI capabilities.

**Need Help?**: Check the reference docs in the `references/` folder for detailed API documentation.
