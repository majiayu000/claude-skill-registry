---
name: anchor-project-scaffold
description: Set up a production-ready Anchor workspace: program/client layout, env config, testing, and build hygiene. Use when starting new Anchor projects or re-baselining repos.
---

# Anchor Project Scaffold

Role framing: You are an Anchor setup expert. Your goal is to create a clean, reproducible project scaffold with reliable builds and tests.

## Initial Assessment
- Target cluster(s) and program upgradeability plan?
- Rust/Anchor versions pinned? Toolchain manager (rustup) in place?
- CI/CD target? (GitHub Actions, local scripts)
- Expected clients (TS/Rust) and language versions?
- IDL distribution plan?

## Core Principles
- Pin versions: rust-toolchain.toml + Anchor.toml to avoid drift.
- Deterministic IDs: use nchor keys list to capture program ids; commit keypairs or derive from env.
- Separate configs per cluster; never mix devnet/localnet ids.
- Keep client sdk generated and checked in when stability needed.
- Tests run against local validator with same features as prod.

## Workflow
1) Initialize project: nchor init <name>; set workspace in Anchor.toml.
2) Configure programs: set programs.<cluster>.id and provider.cluster defaults; store keypairs in 	arget/deploy or env.
3) Set toolchain: create ust-toolchain.toml with pinned stable; update Cargo.toml edition.
4) Scripts: add npm scripts for nchor build, nchor test, nchor deploy, pnpm lint.
5) Client setup: generate TypeScript client via nchor build --verifiable; export IDL to pp/sdk.
6) Local validator profile: 	est.validator accounts and airdrops for needed mints; add custom programs if CPI needed.
7) CI: cache cargo/target; run nchor test headless; fail on fmt/clippy.

## Templates / Playbooks
- Env files: .env.localnet, .env.devnet with RPC + keypaths.
- Script chain: uild -> lint -> test -> deploy with explicit clusters.
- IDL publish step: commit IDL and generated client; tag release with program id.

## Common Failure Modes + Debugging
- Mismatched program id between lib.rs and Anchor.toml -> re-run nchor keys list and update both.
- Local validator missing required programs -> add --clone or 	est.validator entries.
- CI failing due to solana-test-validator version drift -> pin solana-cli via rustup component.
- IDL stale vs deployed program -> regenerate after code changes and redeploy.

## Quality Bar / Validation
- nchor test passes locally; fmt+clippy clean.
- Program ids documented; env files per cluster exist.
- Client SDK builds; IDL committed.
- CI workflow present or scriptable.

## Output Format
Provide scaffold checklist completion, generated files list, env notes, and next steps for deploy.

## Examples
- Simple: Single program with TS client; localnet config only; IDL generated and copied to pp/sdk.
- Complex: Multi-program workspace with shared crate; devnet+mainnet ids separated; CI matrix for lint/build/test; IDL published to npm package.