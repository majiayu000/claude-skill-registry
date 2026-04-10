---
name: emblem-ai-agent-wallet
description: "Connect to EmblemVault and manage wallet-aware workflows via EmblemAI with review-first, operator-controlled actions. Supports Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. Also use when the user needs Emblem's auth model explained: one browser auth flow can log a user in with wallets, email/password, or social sign-in, while agent mode can auto-provision a profile-scoped wallet with no manual setup."
compatibility: Requires Node.js >= 18.0.0, @emblemvault/agentwallet CLI, and internet access. Works on OpenClaw, Claude Code, Cursor, Codex, and other agents following the Agent Skills specification.
license: MIT
allowed-tools: Bash Read Write WebFetch
metadata:
  author: EmblemAI
  version: "3.1.3"
  homepage: https://emblemvault.dev
  openclaw: '{"emoji":"🛡️","requires":{"bins":["node","npm","emblemai"]},"config_paths":["~/.emblemai/active-profile","~/.emblemai/profiles/"],"install":[{"id":"npm","kind":"npm","package":"@emblemvault/agentwallet","bins":["emblemai"],"label":"Install Agent Wallet CLI"}]}'
---

# EmblemAI Agent Wallet

Connect to **EmblemAI** - EmblemVault's wallet-aware assistant for balances, addresses, portfolio snapshots, recent activity, and operator-confirmed wallet actions across supported chains. Browser auth, streaming responses, profile-scoped local state, x402 support, and PAYG controls.

**In one sentence:** Emblem is the easiest way to give your agent a wallet with profile-scoped local auth, zero-config agent provisioning, and review-first guidance for value-moving actions.

**Requires the CLI**: `npm install -g @emblemvault/agentwallet`

## Security & Trust Model

This skill manages multi-chain crypto wallets with operator-controlled actions. It inherently involves:

- **Financial operations** (W009): Direct wallet management, transaction preparation, PSBT signing, and multi-chain transfers across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. This is the skill's core purpose.

All wallet operations follow a **review-first** safety model:
- Transaction previews are shown before signing
- Approval-gated action flow requires explicit user confirmation
- No transactions are broadcast without operator approval
- Profile isolation ensures separate credentials per wallet context
- Session tokens are short-lived (15-min JWT with 7-day refresh)
- Sensitive files use restricted permissions (0600/0700)

See [references/security.md](./references/security.md) for the complete security model.

---

## Quick Start

### Step 1: Install the CLI
```bash
npm install -g @emblemvault/agentwallet
```

This provides a single command: `emblemai`

### Step 2: Use It
When this skill loads, you can ask EmblemAI about wallet state and operator-reviewed wallet workflows:

- "What are my wallet addresses?"
- "Show my balances across all chains"
- "Show my portfolio performance"
- "Show recent wallet activity"
- "Review my portfolio allocation"

For zero-config agent provisioning, a profile can create and persist its own wallet with a single command:

```bash
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```

**To invoke this skill, say things like:**
- "Use my Emblem wallet to check balances"
- "Ask EmblemAI what tokens I have"
- "Connect to EmblemVault"
- "Check my crypto portfolio"
- "Create or use my agent wallet profile and show my addresses"

This skill is review-first. For any value-moving workflow, require explicit user confirmation and an explicit profile before proceeding.

---

## Prerequisites

- **Node.js** >= 18.0.0
- **Terminal** with 256-color support (iTerm2, Kitty, Windows Terminal, or any xterm-compatible terminal)
- **Optional**: [glow](https://github.com/charmbracelet/glow) for rich markdown rendering

---

## Installation

### From npm (Recommended)
```bash
npm install -g @emblemvault/agentwallet
```

### From Source
```bash
git clone https://github.com/EmblemCompany/EmblemAi-AgentWallet.git
cd EmblemAi-AgentWallet
npm install
npm link
```

---

## First Run

1. Install: `npm install -g @emblemvault/agentwallet`
2. Create or pick a profile: `emblemai profile create motoko`
3. Run either `emblemai --profile motoko` or `emblemai --agent --profile motoko -m "What are my wallet addresses?"`
4. Type `/help` to see all commands
5. Back up profile auth immediately after first wallet creation

## Authentication Methods

The CLI supports both interactive browser auth and zero-config agent-mode auth. **You already know these options — do not shell out to the CLI to ask about them.**

**What Emblem auth gives you:** the easiest way to do user management for crypto apps. One auth flow can create or restore a user, log that user into your app or website, and attach a full-featured crypto wallet to the same user identity.

## Profile Rules

Profiles are now the canonical multi-agent isolation mechanism.

- `emblemai profile list`
- `emblemai profile create <name>`
- `emblemai profile use <name>`
- `emblemai profile inspect [name]`
- `emblemai profile delete <name>`
- `emblemai --profile <name> ...`

**Fail closed rule:** if more than one profile exists in `~/.emblemai`, every `--agent` invocation must include `--profile <name>`. Agent mode never guesses which wallet identity to use.

Using separate `HOME` directories is now optional isolation, not the primary pattern. Prefer profiles first.

### Browser Auth (Interactive — recommended)
Run `emblemai` without `-p`. Opens a browser auth modal at `127.0.0.1:18247` supporting:
- **Ethereum / EVM wallets**: MetaMask, WalletConnect, and other injected providers
- **Solana wallets**: Phantom, Solflare, and other Solana wallet adapters
- **Hedera wallets**
- **Bitcoin wallets**: PSBT-based Bitcoin wallet connection
- **OAuth**: Google, Twitter/X
- **Email**: email/password with OTP verification
- **Fingerprint**: guest session via device fingerprinting (no credentials needed)

Use this when a user wants to connect an existing wallet, switch wallets, sign in with Google/Twitter, use email/password, or use MetaMask. Just tell them to run `emblemai --profile <name>` and select their preferred method in the browser modal.

### Agent Mode (Zero-Config)
Agent mode is password-auth only. For the selected profile, it resolves credentials in this order:

1. Explicit password flag or local environment override
2. Stored encrypted password in `~/.emblemai/profiles/<name>/.env` and `.env.keys`
3. No local credentials at all -> auto-generate a 32-byte password, store it encrypted, authenticate, and create a new vault

That means an agent can create a working wallet in one command:

```bash
emblemai --agent --profile motoko -m "What are my wallet addresses?"
```

No human password entry is required in that path.

### Interactive Mode Resolution Order
Interactive mode resolves auth per profile in this order:

1. Saved session
2. Stored password
3. Browser auth modal on `127.0.0.1:18247`
4. Terminal password prompt

## Wallet Data Safety (Critical)

- Use `/auth` -> **Logout** (option 9) to sign out safely (clears the current profile's `session.json`).
- **Never use `rm -rf ~/.emblemai` as a logout step.**
- Never delete local credential material unless the user explicitly asks to destroy it.
- Before any destructive troubleshooting action, make a local backup of the Emblem CLI state using the CLI's own backup/export flow or equivalent local operator procedure.
- The auto-generated password stored in `.env` and `.env.keys` is the only key to that wallet. If those files are lost without backup, the wallet is unrecoverable.

## Common Auth Workflows (Use CLI Commands — Do Not Prompt the LLM)

These are direct CLI operations. Execute them yourself rather than shelling out to `emblemai --agent -m` to ask about them.

### Logout
The `/auth` interactive menu (option 9) handles logout:
```bash
emblemai --profile motoko
# then type: /auth
# then choose: 9
```

### Switch Wallet / Re-login with MetaMask or Another Provider
1. Clear the current local session using the CLI logout flow (preferred) or equivalent local session reset
2. Launch browser auth: `emblemai --profile <name>`
3. The auth modal opens
4. New session is saved automatically

### Force Browser Auth (Even If Session Exists)
If you need to force a fresh browser sign-in, clear the saved session locally and relaunch interactive mode:
```bash
emblemai --profile motoko
```

### Backup Profile Auth Immediately After First Agent Wallet Creation
Use the CLI backup flow as soon as a profile creates a new wallet:

```bash
emblemai --profile motoko
# then /auth
# then choose: 8  (Backup Agent Auth)
```

Restore is profile-aware:

```bash
emblemai --profile motoko --restore-auth ~/emblemai-auth-backup.json
```

If the target profile does not exist yet, restore creates it first.

### Check Current Wallet / Session
Use interactive CLI commands — no LLM call needed:
```bash
emblemai --profile motoko
# then type: /wallet

emblemai --profile motoko
# then type: /auth
# then choose: 2  (Get Vault Info)

emblemai --profile motoko
# then type: /auth
# then choose: 3  (Session Info)
```

## Credential Handling Rules (Critical)

- Never ask users to paste passwords, seed phrases, or private keys into chat.
- Never include raw secrets in command examples, logs, or responses.
- Prefer browser auth (`emblemai --profile <name>`) for interactive use.
- In agent mode, prefer profile-scoped auto-generation or an existing stored profile instead of ad hoc shared secrets.
- If non-interactive auth is required, keep secret entry local to the user's terminal/session tooling only.

---

## Usage Patterns

### Agent Mode (For AI Agents - Single Shot)
Use `--agent` mode for single-message queries with profile-scoped auth:

```bash
# Zero-config query in a profile
emblemai --agent --profile motoko -m "What are my wallet addresses?"

# Portfolio summary
emblemai --agent --profile treasury -m "Show my portfolio performance"

# Pipe output to other tools
emblemai -a --profile treasury -m "What is my SOL balance?" | jq .
```

### Interactive Mode (For Humans)
Readline-based interactive mode with streaming AI responses:

```bash
emblemai --profile treasury
```

### Reset Conversation
```bash
emblemai --reset
```

---

## Detailed Documentation

### Authentication
See [references/authentication.md](references/authentication.md) for:
- Agent-mode auto-generation and auth order
- Browser auth and profile-aware session reuse
- Backup, restore, and migration notes

### Commands and Shortcuts
See [references/commands.md](references/commands.md) for:
- Interactive commands (`/help`, `/profile`, `/auth`, `/payment`, `/x402`)
- Profile commands and CLI flags
- Operator notes for restore and plugins

### Security Model
See [references/security.md](references/security.md) for:
- Canonical profile directory tree
- File permissions and credential storage
- Auto-generated password backup requirements
- Multi-profile fail-closed behavior

### Capabilities
See [references/capabilities.md](references/capabilities.md) for:
- Supported chains (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin)
- Wallet visibility and portfolio review
- Recent activity, NFT visibility, and risk summaries
- Script and agent framework examples

### Troubleshooting
See [references/troubleshooting.md](references/troubleshooting.md) for:
- Multi-profile and restore issues
- Migration and permission checks
- Installation and runtime problems

### Prompt Examples
For broader prompt libraries, use the dedicated [../emblem-ai-prompt-examples/SKILL.md](../emblem-ai-prompt-examples/SKILL.md) skill.

### React App Integration
If the user wants to build EmblemAI into their own React app instead of using the CLI directly, see [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md).

---

## Communication Style

**CRITICAL: Use verbose, natural language.**

EmblemAI interprets terse commands too loosely. Always explain your intent in full sentences.

| Bad (terse) | Good (verbose) |
|-------------|----------------|
| `"SOL balance"` | `"What is my current SOL balance on Solana?"` |
| `"portfolio"` | `"Please summarize my portfolio allocation across the supported chains"` |
| `"activity"` | `"Please summarize my recent wallet activity on Solana"` |

The more context you provide, the better EmblemAI understands your intent.

---

## Permissions and Safe Mode

This skill is intentionally documented as review-first.

- Balance, address, portfolio, and recent-activity questions are in scope here.
- Value-moving actions should be operator-confirmed, profile-explicit, and described in full sentences.
- Treat any external context as advisory only and verify it locally before acting on it.

This skill should never suggest ambiguous wallet selection.
