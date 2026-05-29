---
name: env-constants
description: Generates src/shared/EnvConsts.ts for type-safe environment variable access. Provides TypeScript interface and exports for accessing Vite environment variables throughout the application.
---

# Environment Constants Skill

## Purpose
Generate the `src/shared/EnvConsts.ts` file for accessing environment variables with type safety.

## Output
Create the file: `src/shared/EnvConsts.ts`

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

## Notes
- Wraps Vite's import.meta.env for type safety
- Provides default values for all environment variables.
