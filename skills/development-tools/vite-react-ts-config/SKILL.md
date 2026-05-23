---
name: vite-react-ts-config
description: Create or update vite.config.ts for a Vite React-TS project, following best practices (defineConfig, aliases, env usage, server/build defaults).
argument-hint: "[goal: aliases/proxy/base-path/build-options] [paths]"
allowed-tools: Read, Grep, Glob
---

# Vite Config (React-TS) Skill

You are editing a Vite + React + TypeScript project’s configuration.

## Rules / best practices

1) Use vite.config.ts and export via defineConfig().
2) Keep config minimal; only add what’s needed for the user’s stated goal.
3) Prefer stable patterns:
   - path aliases via resolve.alias (and also ensure tsconfig paths match if used)
   - environment variables via import.meta.env (VITE_ prefix)
4) Avoid relying on obscure plugins unless requested.

## Deliverables

- Show the intended vite.config.ts contents (or diff-style summary).
- If adding aliases, also update tsconfig.json paths (and mention restarting TS server).
- If adding env usage, show .env.example and safe usage notes.

Use template.md as the default structure.
