---
name: bun
description: "Bun runtime patterns and best practices. Fast JavaScript/TypeScript execution, bundling, testing, and edge deployment. Trigger: When using Bun for server-side apps, scripts, or tooling."
skills:
  - conventions
  - typescript
  - javascript
dependencies:
  bun: ">=1.0.0 <2.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Bun Skill

## When to Use

- Running JS/TS apps with Bun
- Using Bun for fast bundling or testing
- Deploying edge/serverless apps

## Critical Patterns

- Use bun run/test for scripts
- Leverage Bun's native APIs
- Prefer Bun's bundler for speed

## Decision Tree

- Need fast startup? → Use Bun
- Bundling? → Use bun build
- Testing? → Use bun test

## Edge Cases

- Node.js compatibility gaps
- Native module support
- Edge deployment limits
