---
name: vite-react-ts-env
description: Add environment variables in a Vite React-TS project correctly (VITE_ prefix, typing, .env files, safe usage in React components).
argument-hint: "[env keys] [where used] [dev/prod]"
allowed-tools: Read, Grep, Glob
---

# Vite Env Variables (React-TS) Skill

Implement environment variables correctly in Vite.

## Rules / best practices

1) Client-exposed env vars MUST be prefixed with VITE_.
2) Access via import.meta.env (not process.env).
3) Document variables in .env.example.
4) Do not commit secrets; if asked, recommend server-side storage instead.
5) Provide TypeScript types for env when helpful (vite-env.d.ts).

## Deliverables

- .env.example entries
- Optional: env typing augmentation
- Usage snippet in a React component

Use template.md as the default structure.
