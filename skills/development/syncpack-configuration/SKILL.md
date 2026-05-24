---
name: syncpack-configuration
description: Use when setting up or configuring syncpack for a monorepo. Covers configuration files, workspace detection, and custom rule definitions for dependency version management.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Syncpack Configuration

Syncpack is a tool for managing consistent dependency versions across JavaScript/TypeScript monorepos. This skill covers configuration best practices.

## Configuration File Locations

Syncpack searches for configuration in these locations (in order):

1. `syncpack.config.js` / `.cjs` / `.mjs` / `.ts`
2. `syncpack.config.json` / `.yaml` / `.yml`
3. `.syncpackrc` / `.syncpackrc.json` / `.syncpackrc.yaml` / `.syncpackrc.yml`

## Basic Configuration

```js
// syncpack.config.js
export default {
  // Glob patterns to find package.json files
  source: [
    'package.json',
    'packages/*/package.json',
    'apps/*/package.json',
  ],
};
```

## Workspace Detection

Syncpack automatically detects workspaces:

- **npm/Yarn**: Reads `workspaces` from `./package.json`
- **pnpm**: Reads `packages` from `./pnpm-workspace.yaml`
- **Lerna**: Reads `packages` from `./lerna.json`

Override with explicit `source` patterns when needed.

## Dependency Types

Control which dependency types to check:

```js
export default {
  dependencyTypes: [
    'dev',           // devDependencies
    'local',         // workspace: protocol dependencies
    'overrides',     // npm overrides / yarn resolutions
    'peer',          // peerDependencies
    'pnpmOverrides', // pnpm overrides
    'prod',          // dependencies
    'resolutions',   // yarn resolutions
  ],
};
```

## Semver Groups

Define rules for semver range consistency:

```js
export default {
  semverGroups: [
    {
      // Require exact versions for React
      dependencies: ['react', 'react-dom'],
      range: '',  // exact version
    },
    {
      // Allow caret ranges for dev tools
      dependencyTypes: ['dev'],
      range: '^',
    },
  ],
};
```

### Range Options

| Range | Example | Meaning |
|-------|---------|---------|
| `''` | `1.2.3` | Exact version |
| `^` | `^1.2.3` | Compatible with |
| `~` | `~1.2.3` | Approximately equivalent |
| `>=` | `>=1.2.3` | Greater than or equal |
| `*` | `*` | Any version |

## Version Groups

Partition dependencies into groups with separate version policies:

```js
export default {
  versionGroups: [
    {
      // Pin specific dependencies
      dependencies: ['typescript'],
      pinVersion: '5.3.3',
    },
    {
      // Ban certain packages
      dependencies: ['moment'],
      isBanned: true,
    },
    {
      // Use workspace version as source of truth
      dependencies: ['@myorg/*'],
      preferVersion: 'highestSemver',
    },
  ],
};
```

## Formatting Options

Control package.json formatting:

```js
export default {
  formatBugs: true,
  formatRepository: true,
  sortAz: [
    'contributors',
    'dependencies',
    'devDependencies',
    'keywords',
  ],
  sortFirst: [
    'name',
    'version',
    'description',
    'main',
  ],
};
```

## Common Patterns

### Single Version Policy

Enforce one version per dependency across all packages:

```js
export default {
  versionGroups: [
    {
      label: 'Use highest version everywhere',
      preferVersion: 'highestSemver',
    },
  ],
};
```

### Allow Development Exceptions

```js
export default {
  versionGroups: [
    {
      label: 'Ignore dev dependencies',
      dependencyTypes: ['dev'],
      isIgnored: true,
    },
    {
      label: 'Consistent versions for production',
      dependencyTypes: ['prod', 'peer'],
      preferVersion: 'highestSemver',
    },
  ],
};
```

### Scoped Package Source of Truth

```js
export default {
  versionGroups: [
    {
      label: 'Internal packages use local version',
      dependencies: ['@myorg/**'],
      dependencyTypes: ['local'],
      preferVersion: 'local',
    },
  ],
};
```

## Best Practices

1. **Start with defaults** - Syncpack works well without configuration
2. **Add rules incrementally** - Only add rules as you encounter issues
3. **Document exceptions** - Use `label` field to explain why rules exist
4. **Commit config file** - Keep version policy in version control
5. **Run in CI** - Use `syncpack list-mismatches --fail-fast` in CI pipelines
