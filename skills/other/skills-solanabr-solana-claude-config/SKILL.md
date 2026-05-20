---
name: solana-dev
description: End-to-end Solana development playbook (Jan 2026). Prefer Solana Foundation framework-kit (@solana/client + @solana/react-hooks) for React/Next.js UI. Prefer @solana/kit for all new client/RPC/transaction code. When legacy dependencies require web3.js, isolate it behind @solana/web3-compat (or @solana/web3.js as a true legacy fallback). Covers wallet-standard-first connection (incl. ConnectorKit), Anchor/Pinocchio programs, Codama-based client generation, LiteSVM/Mollusk/Surfpool testing, and security checklists.
user-invocable: true
---

# Solana Development Skill (framework-kit-first)

## What this Skill is for

Use this Skill when the user asks for:
- Solana dApp UI work (React / Next.js)
- Wallet connection + signing flows
- Transaction building / sending / confirmation UX
- On-chain program development (Anchor or Pinocchio)
- Client SDK generation (typed program clients)
- Local testing (LiteSVM, Mollusk, Surfpool)
- Security hardening and audit-style reviews
- Backend services (indexers, APIs, RPC integration)
- Deployment workflows (devnet → mainnet)

## Default stack decisions (opinionated)

### 1) UI: framework-kit first
- Use `@solana/client` + `@solana/react-hooks`
- Prefer Wallet Standard discovery/connect via the framework-kit client
- Use `create-solana-dapp` for new projects

### 2) SDK: @solana/kit first
- Prefer Kit types (`Address`, `Signer`, transaction message APIs, codecs)
- Prefer `@solana-program/*` instruction builders over hand-rolled instruction data
- Use BigInt for u64/u128 values

### 3) Legacy compatibility: web3.js only at boundaries
- If you must integrate a library that expects web3.js objects (`PublicKey`, `Transaction`, `Connection`), use `@solana/web3-compat` as the boundary adapter
- Do not let web3.js types leak across the entire app; contain them to adapter modules
- See kit-web3-interop.md for adapter patterns

### 4) Programs
- **Default**: Anchor (fast iteration, IDL generation, mature tooling)
- **Performance/footprint**: Pinocchio when you need CU optimization, minimal binary size, zero dependencies, or fine-grained control over parsing/allocations

### 5) Testing
- **Default**: LiteSVM or Mollusk for unit tests (fast feedback, runs in-process)
- Use Surfpool for integration tests against realistic cluster state (mainnet/devnet) locally
- Use solana-test-validator only when you need specific RPC behaviors not emulated by LiteSVM

### 6) Backend
- **Framework**: Axum 0.8+ with Tokio 1.40+
- **Critical**: Use `spawn_blocking` for Solana RPC calls (they block!)
- **Database**: sqlx with compile-time checked queries
- **Caching**: Redis for RPC response caching

## Operating procedure (how to execute tasks)

### 1. Classify the task layer
- UI/wallet/hook layer
- Client SDK/scripts layer
- Program layer (+ IDL)
- Testing/CI layer
- Backend (indexer/API)
- Infra (RPC/deployment)

### 2. Pick the right building blocks

| Layer | Primary Tool | Alternative |
|-------|-------------|-------------|
| UI + hooks | @solana/react-hooks | ConnectorKit (headless) |
| Client SDK | @solana/kit | web3-compat adapter |
| Programs | Anchor | Pinocchio (CU-critical) |
| Testing | LiteSVM/Mollusk | Surfpool (integration) |
| Backend | Axum 0.8+ | - |

### 3. Implement with Solana-specific correctness

Always be explicit about:
- Cluster + RPC endpoints + websocket endpoints
- Fee payer + recent blockhash
- Compute budget + prioritization (where relevant)
- Expected account owners + signers + writability
- Token program variant (SPL Token vs Token-2022) and any extensions

### 4. Add tests
- Unit test: LiteSVM or Mollusk
- Integration test: Surfpool
- For "wallet UX", add mocked hook/provider tests where appropriate
- Profile CU usage during development

### 5. Deliverables expectations

When implementing changes, provide:
- Exact files changed + diffs (or patch-style output)
- Commands to install/build/test
- A short "risk notes" section for anything touching signing/fees/CPIs/token transfers

## Progressive disclosure (read when needed)

### Frontend & Client
- [frontend-framework-kit.md](frontend-framework-kit.md) - React hooks, wallet connection, React Query, error handling, performance patterns
- [kit-web3-interop.md](kit-web3-interop.md) - Kit ↔ web3.js boundary patterns, Anchor adapter examples
- [idl-codegen.md](idl-codegen.md) - Codama/Shank client generation

### Programs (also check security.md)
- [programs-anchor.md](programs-anchor.md) - Anchor patterns, testing pyramid, IDL generation, deployment
- [programs-pinocchio.md](programs-pinocchio.md) - Zero-copy, CU optimization, TryFrom validation

### Testing & Security
- [testing.md](testing.md) - LiteSVM, Mollusk, Surfpool, CI guidance
- [security.md](security.md) - Vulnerability categories, program + client checklists

### Backend & Deployment
- [backend-async.md](backend-async.md) - Axum 0.8/Tokio patterns, spawn_blocking, RPC integration, Redis caching
- [deployment.md](deployment.md) - Devnet/mainnet workflows, verifiable builds, multisig, CI/CD

### Ecosystem & Reference
- [ecosystem.md](ecosystem.md) - Token standards, DeFi protocols, NFT infrastructure, data indexing
- [payments.md](payments.md) - Commerce Kit, Kora (gasless), payment UX
- [resources.md](resources.md) - Official documentation links

### Unity & Game Development
- [unity.md](unity.md) - Solana.Unity-SDK, wallet integration, NFT loading, transaction building in C#
- [playsolana.md](playsolana.md) - PlaySolana ecosystem, PSG1 console, PlayDex, PlayID, SvalGuard

## Task routing guide

| User asks about... | Primary file(s) |
|--------------------|-----------------|
| Wallet connection, React hooks | frontend-framework-kit.md |
| Transaction building, Kit types | kit-web3-interop.md |
| Anchor program code | programs-anchor.md |
| CU optimization, Pinocchio | programs-pinocchio.md |
| Unit testing, CU benchmarks | testing.md |
| Security review, audit | security.md |
| Backend API, indexer | backend-async.md |
| Deploy to devnet/mainnet | deployment.md |
| DeFi integration, NFTs | ecosystem.md |
| Payment flows, checkout | payments.md |
| Generated clients, IDL | idl-codegen.md |
| Unity game development | unity.md |
| PlaySolana, PSG1 console | playsolana.md |
