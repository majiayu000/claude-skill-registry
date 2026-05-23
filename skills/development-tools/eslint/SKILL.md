---
name: ESLint
description: General rules for linting this project; use when handling lint errors or adding ESLint to a package.
---

Always run `eslint --fix` instead of just `eslint`.
Consider this skill whenever linting or addressing lint errors.

**Never disable an ESLint rule.** Fix the code or types so the rule is satisfied (e.g. add proper types, narrow with type guards, or restructure). Do not use `eslint-disable`, `eslint-disable-next-line`, or inline comment disables.

## Adding ESLint to a package (using @zerospin/utils)

Use the shared config from `@zerospin/utils` so new packages match the rest of the repo.

1. **Dependencies** (devDependencies in the package's `package.json`):
   - `eslint`: `^9`
   - `@zerospin/utils`: `workspace:*`

2. **Config file** - add `eslint.config.ts` in the package root:

```ts
import { baseConfig, defineConfig } from '@zerospin/utils'

const eslintConfig = defineConfig({}, baseConfig)

export default eslintConfig
```

3. **Script** (if missing): `"lint": "eslint ."` in `package.json` scripts.

4. **Optional overrides** - pass more args to `defineConfig` (same pattern as `apps/platform/eslint.config.ts`): e.g. `ignores`, `rules`, `settings`.
