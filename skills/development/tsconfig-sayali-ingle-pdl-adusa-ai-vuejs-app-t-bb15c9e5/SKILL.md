---
name: tsconfig
description: Generates tsconfig.json for TypeScript compilation configuration. Includes path aliases (@/ for src/), Jest types, and Vite client types.
---

# TypeScript Config Skill

## Purpose
Generate the `tsconfig.json` file for TypeScript compilation configuration.

## Output
Create the file: `tsconfig.json`

## Template
See: `examples.md` in this directory for complete template and detailed examples.

## Notes
- The `paths` configuration enables `@/` alias for the `src/` directory
- Jest types are included for testing support
- Vite client types are included for import.meta.env support
- Experimental decorators are enabled for Vue class components
