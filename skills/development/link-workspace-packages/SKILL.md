---
name: link-workspace-packages
description: 'Link workspace packages in the Hedgehog pnpm monorepo. USE WHEN: (1) you just created or generated new packages and need to wire up their dependencies, (2) code imports from a sibling package and needs it added as a dependency, (3) you get resolution errors for workspace packages (@org/*) like "cannot find module", "failed to resolve import", "TS2307", or "cannot resolve". DO NOT patch around with tsconfig paths or manual package.json edits - use pnpm''s workspace commands to fix actual linking.'
---

# Link Workspace Packages

Add dependencies between packages in the workspace using pnpm's `workspace:` protocol — symlinks are only created when a dependency is explicitly declared this way.

## Workflow

1. Identify consumer package (the one importing)
2. Identify provider package(s) (being imported)
3. Add the dependency:

   ```bash
   # From consumer directory
   pnpm add @org/ui --workspace

   # Or with --filter from anywhere
   pnpm add @org/ui --filter @org/app --workspace
   ```

   Result in `package.json`:

   ```json
   { "dependencies": { "@org/ui": "workspace:*" } }
   ```

4. Verify the symlink was created in the consumer's `node_modules/@org/<package>`

## Debugging "Cannot find module"

1. Check if the dependency is declared in the consumer's `package.json`
2. If not, add it using the command above
3. Run `pnpm install`

## Notes

- pnpm uses strict isolation (no hoisting) — a package must be an explicit dependency to be resolvable, even if it's installed elsewhere in the workspace. This prevents phantom deps.
- Root `package.json` should have `"private": true` to prevent accidental publish.
