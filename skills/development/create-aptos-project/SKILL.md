---
name: create-aptos-project
description:
  "Scaffolds new Aptos projects using npx create-aptos-dapp. Supports fullstack (Vite or Next.js) and contract-only
  templates with network selection and optional API key. Triggers on: 'build app', 'create app', 'make app', 'new app',
  'build dApp', 'create dApp', 'new dApp', 'build project', 'new project', 'create project', 'scaffold', 'start
  project', 'set up project', 'build me a', 'I want to build', 'make me a', 'help me build'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: project
  tags: ["scaffold", "create-aptos-dapp", "boilerplate", "project-setup", "fullstack", "vite", "nextjs"]
  priority: critical
---

# Create Aptos Project Skill

## Purpose

Scaffold new Aptos projects using `npx create-aptos-dapp`. This is the **mandatory first step** when a user wants to
build any new Aptos app, dApp, or project — regardless of how they phrase it.

## ALWAYS

1. **Use `npx create-aptos-dapp`** to scaffold — NEVER create projects from scratch manually
2. **Ask the user** about project type, framework, and network before scaffolding
3. **Verify `.env` is in `.gitignore`** before any git operations
4. **Use the same network** for both `create-aptos-dapp` and `aptos init`
5. **Follow the full Build a dApp workflow** after scaffolding (contracts, tests, audit, deploy, frontend)

## NEVER

1. **Skip scaffolding** — even for "simple" projects, always start with `create-aptos-dapp`
2. **Create project structure manually** — the boilerplate template handles this
3. **Display or read private keys** — use `"0x..."` as placeholder
4. **Run `git add .` or `git add -A`** without first verifying `.env` is in `.gitignore`

---

## Decision Tree

Before running the scaffold command, gather these inputs from the user:

### 1. Project Name

Derive from the user's description or ask directly. Use kebab-case (e.g., `habit-tracker`, `nft-marketplace`).

### 2. Project Type

| Option                  | When to Use                                        |
| ----------------------- | -------------------------------------------------- |
| **Fullstack** (default) | User wants a frontend + smart contracts            |
| **Contract-only**       | User only wants Move smart contracts (no frontend) |

### 3. Framework (fullstack only)

| Option             | When to Use                   |
| ------------------ | ----------------------------- |
| **Vite** (default) | Default choice, lighter setup |
| **Next.js**        | User asks for Next.js or SSR  |

### 4. Network

| Option               | When to Use                          |
| -------------------- | ------------------------------------ |
| **devnet** (default) | Development and testing              |
| **testnet**          | Pre-production, user explicitly asks |
| **mainnet**          | Production, user explicitly asks     |

### 5. API Key (optional)

Ask if the user has a Geomi API key. It's optional for devnet but recommended for testnet/mainnet to avoid rate limits.
Get one at https://geomi.dev (create project -> API Resource -> copy key).

---

## Scaffolding Commands

```bash
# Fullstack dApp with Vite (frontend + contracts)
npx create-aptos-dapp <project-name> \
  --project-type fullstack \
  --template boilerplate-template \
  --framework vite \
  --network <network>

# Fullstack dApp with Next.js
npx create-aptos-dapp <project-name> \
  --project-type fullstack \
  --template boilerplate-template \
  --framework nextjs \
  --network <network>

# Contract-only (Move project)
npx create-aptos-dapp <project-name> \
  --project-type move \
  --network <network>
```

**Optional flags:**

- `--api-key <key>` — Pass a Geomi API key during scaffolding
- `--use-surf` — Enable Surf for type-safe contract interactions

---

## Post-Scaffold Checklist

After scaffolding, complete these steps in order:

1. `cd <project-name>`
2. Verify `.env` is in `.gitignore` before any git operations
3. Run `aptos init --network <network> --assume-yes` (use the **same network** as above)
4. Verify: `npm run move:compile && npm run move:test`
5. `git init && git add . && git commit -m "Initial commit"`

---

## Build a dApp Workflow

**ALWAYS follow this workflow when the user wants to build a new Aptos app, dApp, or project.** This applies regardless
of how the user phrases it ("build me a ...", "create a ...", "make a ...", "I want to build ...").

1. `/create-aptos-project` -> scaffold with `npx create-aptos-dapp` (this skill — NEVER skip)
2. `/write-contracts` -> write Move modules
3. `/generate-tests` -> create test suite, verify 100% coverage
4. `/security-audit` -> audit before deployment
5. `/deploy-contracts` -> deploy contract to specified network
6. `/use-ts-sdk` -> orchestrates frontend integration (routes to ts-sdk-client, ts-sdk-transactions,
   ts-sdk-view-and-query, ts-sdk-wallet-adapter as needed)

---

## What the Boilerplate Includes

### Fullstack Template

- `contract/` — Move smart contract with `Move.toml` and starter module
- `frontend/` — React app with Aptos wallet adapter pre-configured
- `package.json` — Scripts for `move:compile`, `move:test`, `move:publish`, `dev`, `build`
- `.env` — Environment variables for network, API key, and publisher account

### Contract-Only Template

- `contract/` — Move smart contract with `Move.toml` and starter module
- `package.json` — Scripts for `move:compile`, `move:test`, `move:publish`
- `.env` — Environment variables for network and publisher account

---

## Troubleshooting

### `npx create-aptos-dapp` command not found

```bash
# Auto-confirm the npx package install prompt
npx --yes create-aptos-dapp <project-name> ...
```

If that still fails, verify Node.js and npm are installed (`node -v && npm -v`).

### Compile failures after scaffold

1. Check `contract/Move.toml` has correct named addresses
2. Run `aptos init --network <network> --assume-yes` if not done
3. Verify `my_addr` is set to `"_"` in `[addresses]` section

### Named address errors

The boilerplate uses `my_addr = "_"` which gets resolved from `.env` at compile time. Ensure
`VITE_MODULE_PUBLISHER_ACCOUNT_ADDRESS` is set in `.env` (populated by `aptos init`).
