---
name: aacode
description: Write code like Ahmad Awais.
license: Apache-2.0
metadata:
  author: ahmadawais
  version: "0.0.1"
---

## Stack

- TypeScript with strict mode (`strict: true`, `noUncheckedIndexedAccess: true`)
- Zod for runtime validation at system boundaries
- Biome for linting and formatting
- Vitest for tests
- pnpm as package manager

## TypeScript

- Every function gets an explicit return type
- Never use `any` — use `unknown` with type guards
- Define interfaces for all objects
- Use branded types for IDs
- Default to `readonly` for arrays and objects

## Functional Only

- Don't use classes or OOP patterns use pure functions
- No `class`, `this`, or `new` (except `Map`/`Set`/`Error`)
- No prototypes, inheritance, instance methods, or stateful objects with methods
- Pure functions that take data and return data
- Plain objects or/and arrays for data
- Compose functions instead of inheriting
- Pass state explicitly as parameters
- Keep data transforms immutable

## Code Style

- Errors first, happy path last
- If guard clauses up top, main logic at the bottom
- Never nest deeper than 2-3 levels (ideally 1 level max)
- Flatten with early `return`, `continue`, `break`
- Avoid switch/case and else — use if guards almost always

## CLI Development

- Always use pnpm — never npm or yarn
- tsup for bundling
- Commander.js for commands
- clack for interactive input
- picocolors for colors
- ora for spinners
- Ink + ink-spinner for interactive UIs
- One file per command inside `commands/`
- Pull version from `package.json` — never hardcode
- Always start at `0.0.1`
- Lowercase flags only: `-v`/`--version`, `-h`/`--help`
- `-v` prints version number and nothing else
- Hide internal flags: `.addOption(new Option('--local').hideHelp())`
- 150px ASCII art banner with CLI name
- ANSI Shadow font on wide terminals, ANSI Compact on narrow
- White, gray, black colors only
- Check for name conflicts before `pnpm link`

## Dev Loop

- Write tests for new functionality
- `pnpm test`
- `pnpm lint`
- `pnpm typecheck` (`tsc --noEmit`)
- `pnpm build` — catches circular deps and export issues other checks miss
- Commit

## Commits

- Format: `<type>: <description>` with optional body
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## npm Package Publishing

- Use npx npm-name-cli to check for name availability before `npm publish` (also check common - variations like tdot is not taken but can't publish coz of t-do-t or t-dot)
