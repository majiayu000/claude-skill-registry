---
name: bun-first
description: Use Bun as the primary JavaScript runtime and tooling choice
---

# Bun-First Development Guidelines

Bun is the primary JavaScript runtime and tooling choice for this project.

## Key Preferences

- **PREFER** Bun over Node.js, npm, pnpm, or yarn
- **PREFER** Bun's built-in features over third-party tools when available

## Package Management

Use Bun's package commands:
- `bun install` - Install dependencies
- `bun add` - Add packages
- `bun remove` - Remove packages

## Tool Selection

- **PREFER** Vitest over Bun's test runner
- **PREFER** Vite over Bun's build tool

## Runtime Approach

- Leverage Bun's native APIs (fetch, fs, path, env handling)
- Write code assuming modern Web APIs are available
- Use Node-specific APIs only when necessary

## Philosophy

Prioritize simplicity and directness. Avoid unnecessary abstractions and complex toolchains in favor of straightforward, explicit solutions.
