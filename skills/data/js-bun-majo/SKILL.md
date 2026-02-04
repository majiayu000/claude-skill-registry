---
name: js-bun-majo
description: Use Bun instead of Node.js and npm for JavaScript and TypeScript development.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# JavaScript/TypeScript with Bun

**Goal**: Ensure Bun is used as the runtime, tooling, and package manager for all JavaScript and TypeScript development, completely replacing Node.js and npm.

## When to Use This Skill

- **Initializing a new JS/TS project**
- **Migrating from Node.js/npm to Bun**
- **Running JavaScript or TypeScript code**
- **Installing packages or dependencies**
- **Building or bundling JS/TS projects**
- **Writing scripts in package.json equivalents**

## When NOT to Use This Skill

- **Project explicitly requires Node.js runtime** (e.g., specific Node APIs)
- **Legacy project with npm-specific configurations that can't migrate**
- **Working with Deno instead of Bun**

## Process

1. **Check for existing Node/npm usage** - Look for `package-lock.json`, `node_modules`, npm scripts
2. **Install Bun if not present** - Use system package manager or `curl -fsSL https://bun.sh/install | bash`
3. **Initialize with Bun** - Use `bun init` instead of `npm init`
4. **Install dependencies** - Use `bun install` instead of `npm install`
5. **Run scripts** - Use `bun run <script>` instead of `npm run`
6. **Execute files** - Use `bun <file>` instead of `node <file>`
7. **Add dependencies** - Use `bun add <pkg>` instead of `npm install <pkg>`
8. **Update AGENTS.md** - Document Bun usage for the project

## Constraints

- **ALWAYS prefer Bun** over Node.js and npm in all circumstances
- **NEVER use npm commands** (`npm install`, `npm run`, `npx`) when Bun alternatives exist
- **NEVER create `package-lock.json`** - Bun uses `bun.lockb` instead
- **Check `package.json` exists** before assuming Bun is initialized
- **If uncertain on Bun commands**, use `bun --help` or command line for assistance

**Use Bun as the runtime, tooling, and package manager in lieu of Node and npm.**

This applies to both JavaScript and TypeScript projects.

If uncertain on how to invoke Bun commands, use the command line for help.

## Testing Skills

- Verify Bun is installed: `bun --version`
- Test script execution: `bun run <script-name>`
- Check lockfile: `bun.lockb` should exist, not `package-lock.json`
- Ensure no npm commands in documentation or scripts

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `git-majo` — For committing JavaScript/TypeScript changes
- `writing-docs-majo` — For writing JavaScript/TypeScript documentation
