---
name: workleap-web-configs
description: |
  Guide for Workleap's shared web configuration packages: @workleap/eslint-configs, @workleap/typescript-configs, @workleap/rsbuild-configs, @workleap/rslib-configs, @workleap/stylelint-configs, and @workleap/browserslist-config.

  Use this skill when:
  (1) Setting up or modifying shared web tooling configs in a Workleap project
  (2) ESLint config with @workleap/eslint-configs (defineWebApplicationConfig, defineReactLibraryConfig, defineTypeScriptLibraryConfig, defineMonorepoWorkspaceConfig)
  (3) TypeScript config with @workleap/typescript-configs (web-application, library, monorepo-workspace)
  (4) Rsbuild config with @workleap/rsbuild-configs (defineDevConfig, defineBuildConfig, defineStorybookConfig)
  (5) Rslib config with @workleap/rslib-configs for libraries
  (6) Stylelint and Browserslist shared configs
  (7) Extending configs or monorepo (Turborepo) vs polyrepo strategies
  (8) Troubleshooting wl-web-configs, ESM/ESNext constraints, or Storybook with Rsbuild/Rslib
---

# wl-web-configs

Workleap's shared configuration library for web tooling. Provides pre-configured packages for ESLint, TypeScript, Rsbuild, Rslib, Stylelint, and Browserslist.

## Philosophy

- **No lock-in**: Default configurations can always be extended or overridden
- **By project type**: Configurations are composed internally and offered per project type for simplicity
- **ESM/ESNext by default**: Targets modern JavaScript environments
- **Distributed via NPM**: Easy to adopt new features by bumping package versions

## Supported Tools (Active)

| Tool | Package | Purpose |
|------|---------|---------|
| Browserslist | `@workleap/browserslist-config` | Browser targets for apps |
| ESLint | `@workleap/eslint-configs` | Code linting |
| Stylelint | `@workleap/stylelint-configs` | CSS linting |
| TypeScript | `@workleap/typescript-configs` | Type checking (linting only) |
| Rsbuild | `@workleap/rsbuild-configs` | Web application bundling |
| Rslib | `@workleap/rslib-configs` | Library bundling |

**In maintenance mode** (do not recommend): PostCSS, SWC, webpack, tsup

## Quick Reference

### Which Configuration to Use?

| Project Type | ESLint | TypeScript | Bundler |
|--------------|--------|------------|---------|
| Web app with React | `defineWebApplicationConfig` | `web-application.json` | `@workleap/rsbuild-configs` |
| React library | `defineReactLibraryConfig` | `library.json` | `@workleap/rslib-configs` |
| TypeScript library (no React) | `defineTypeScriptLibraryConfig` | `library.json` | `@workleap/rslib-configs` |
| Monorepo workspace root | `defineMonorepoWorkspaceConfig` | `monorepo-workspace.json` | N/A |

### Browserslist (Apps Only)

```bash
pnpm add -D @workleap/browserslist-config browserslist
```

```text
# .browserslistrc
extends @workleap/browserslist-config
```

Only for projects emitting application bundles. Libraries should NOT include Browserslist.

To add custom browser targets while still using the shared config:

```text
# .browserslistrc
extends @workleap/browserslist-config
IE 11
last 2 OperaMobile 12.1 versions
```

## Detailed Documentation

For comprehensive setup guides and options, read the appropriate reference file:

- **ESLint**: See [references/eslint.md](references/eslint.md)
- **TypeScript**: See [references/typescript.md](references/typescript.md)
- **Rsbuild**: See [references/rsbuild.md](references/rsbuild.md)
- **Rslib**: See [references/rslib.md](references/rslib.md)
- **Stylelint**: See [references/stylelint.md](references/stylelint.md)

## Common Patterns

### Customizing Default Rules

All `define*` functions accept a second argument for customization:

```ts
// ESLint example
export default defineWebApplicationConfig(import.meta.dirname, {
    core: { "no-var": "off" },
    typescript: { "@stylistic/quote-props": "off" }
});
```

```json
// TypeScript example - tsconfig.json
{
    "extends": ["@workleap/typescript-configs/web-application.json"],
    "compilerOptions": { "strict": false },
    "exclude": ["dist", "node_modules"]
}
```

### Configuration Transformers (Advanced)

For full control over Rsbuild/Rslib configs:

```ts
import { defineDevConfig, type RsbuildConfigTransformer } from "@workleap/rsbuild-configs";

const customTransformer: RsbuildConfigTransformer = (config) => {
    config.tools = config.tools ?? {};
    // modify config
    return config;
};

export default defineDevConfig({
    transformers: [customTransformer]
});
```

## Critical Rules

1. **Never invent APIs**: Only suggest documented options and patterns
2. **Respect maintenance mode**: Do not recommend PostCSS, SWC, webpack, or tsup configs
3. **ESM by default**: All configs target ESM/ESNext unless migrating legacy code
4. **Browserslist for apps only**: Libraries should not include Browserslist config
5. **TypeScript for linting**: The shared TypeScript configs focus on linting; bundlers handle transpilation
