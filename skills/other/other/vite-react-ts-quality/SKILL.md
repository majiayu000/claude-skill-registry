---
name: vite-react-ts-quality
description: Add a best-practice quality baseline to a Vite React-TS project (TypeScript checking, ESLint, formatting, scripts). Keep it minimal and conventional.
argument-hint: "[goal: eslint/prettier/tsc-ci] [strictness]"
allowed-tools: Read, Grep, Glob
---

# Vite React-TS Quality Baseline

You are adding/adjusting code quality tooling and scripts.

## Rules / best practices

1) Always include type-check command:
   - pnpm exec tsc --noEmit
2) ESLint should be minimal and aligned with React + TypeScript.
3) Formatting:
   - If adding Prettier, keep config small.
4) Do not overcomplicate with many plugins unless requested.

## Deliverables

- package.json scripts
- config files added/updated (eslint/prettier/tsconfig tweaks)
- short “how to run” commands

Use template.md as the default structure.
