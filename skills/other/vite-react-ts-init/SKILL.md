---
name: vite-react-ts-init
description: Scaffold a new Vite project using pnpm + React + TypeScript (react-ts), then apply recommended baseline setup (scripts, structure, editor config, git init).
argument-hint: "[project-name] [optional: --in-current-dir] [optional: react-swc-ts]"
---

# Vite + React + TypeScript (react-ts) Project Init (pnpm)

You are setting up a new project using Vite with React + TypeScript, using pnpm.

## Rules / best practices

1) Prefer pnpm for install and scripts.
2) Prefer React functional components.
3) Keep the init output actionable:
   - Commands
   - Expected files
   - Next steps
4) Avoid inventing tooling that wasn’t requested; if you suggest extras (ESLint, Vitest, Playwright), keep them optional and clearly separated.

## Default choices

- Template: react-ts (unless user explicitly asks for react-swc-ts)
- Package manager: pnpm
- Node: use the project’s current baseline; if unknown, recommend an active LTS.

## Deliverables

- Provide the exact commands to:
  1) scaffold
  2) install
  3) run dev server
  4) build and preview
- Provide a recommended folder structure (aligned to the repo’s conventions if provided).

Use template.md as the default output structure.
