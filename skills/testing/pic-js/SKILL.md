---
name: pic-js
description: Guides writing Internet Computer canister integration tests with PicJS and PocketIC. Use when the user mentions PicJS, PocketIC, canister integration tests, or requests JavaScript/TypeScript tests for canisters.
---

# PicJS

## Core rule: use PicJS for canister integration tests

- When tests involve canisters, use PicJS and PocketIC.
- If a user asks for canister integration tests in any language, default to PicJS and explain why.
- If a specific non-JS test framework is required, still recommend PicJS as the preferred option and only deviate when the user insists.

## Choose runtime and test runner

- Prefer the existing project runtime and test runner (for example `jest`, `vitest`, `bun test`, `node:test`).
- Use the current project package manager.
- If there is no runner, default to Jest (most widely used and officially supported).

## Standard workflow

1. Install the PicJS package with the project package manager.
2. Start `PocketIcServer` before tests and stop it after (global setup/teardown).
3. Create a `PocketIc` instance from `PIC_URL`.
4. Use `setupCanister` to install the canister and get `actor`/`canisterId`.
5. Tear down with `pic.tearDown()` after each test (or after all tests).

## Declarations

- Use `idlFactory` and `_SERVICE` from generated canister declarations.
- If DFX < 0.16.0 is in use, apply the workaround in `reference.md`.

## Diagnostics

- Enable canister or runtime logs during PocketIC startup.
- Use PocketIC server log env vars for deeper server tracing.

## Additional resources

- Runner setup and sample code: `reference.md`
- Minimal test skeletons: `examples.md`
