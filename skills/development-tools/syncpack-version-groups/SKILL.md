---
name: syncpack-version-groups
description: Use when defining version policies, banning dependencies, pinning versions, or creating partitioned version groups in syncpack. Covers advanced version management patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Syncpack Version Groups

Version groups allow you to define sophisticated dependency version policies in your monorepo. This skill covers advanced patterns for version management.

## Version Group Structure

```js
export default {
  versionGroups: [
    {
      label: 'Description of this group',
      dependencies: ['package-name', '@scope/**'],
      dependencyTypes: ['prod', 'dev'],
      packages: ['apps/**'],
      specifierTypes: ['exact', 'range'],
      // Policy options (choose one)
      preferVersion: 'highestSemver',
      // pinVersion: '1.0.0',
      // isBanned: true,
      // isIgnored: true,
    },
  ],
};
```

## Filter Options

### dependencies

Match specific packages by name or glob:

```js
dependencies: [
  'react',           // exact match
  'react-*',         // wildcard
  '@types/**',       // scoped packages
  '{react,vue}',     // either/or
]
```

### dependencyTypes

Filter by where dependencies appear:

```js
dependencyTypes: [
  'dev',           // devDependencies
  'local',         // workspace: protocol
  'overrides',     // npm overrides
  'peer',          // peerDependencies
  'pnpmOverrides', // pnpm.overrides
  'prod',          // dependencies
  'resolutions',   // yarn resolutions
]
```

### packages

Filter by which package.json files:

```js
packages: [
  'apps/**',      // all apps
  'packages/core', // specific package
  '!packages/legacy', // exclude pattern
]
```

### specifierTypes

Filter by version specifier format:

```js
specifierTypes: [
  'exact',        // 1.2.3
  'range',        // ^1.2.3, ~1.0.0, >=2.0.0
  'tag',          // latest, next, canary
  'url',          // https://, git://
  'file',         // file:../path
  'workspace',    // workspace:*
]
```

## Version Policies

### preferVersion

Choose which version wins when mismatches exist:

```js
// Use the highest semver version found
preferVersion: 'highestSemver'

// Use the lowest semver version found
preferVersion: 'lowestSemver'

// Use whatever a specific package has
preferVersion: 'packages/core'

// Use local workspace version
preferVersion: 'local'
```

### pinVersion

Force all matches to use a specific version:

```js
{
  label: 'Pin TypeScript to LTS',
  dependencies: ['typescript'],
  pinVersion: '5.3.3',
}
```

### isBanned

Prevent packages from being used:

```js
{
  label: 'Ban deprecated packages',
  dependencies: ['moment', 'request'],
  isBanned: true,
}
```

### isIgnored

Exclude from version checking:

```js
{
  label: 'Ignore local packages',
  dependencyTypes: ['local'],
  isIgnored: true,
}
```

## Common Patterns

### Monorepo Single Version Policy

```js
export default {
  versionGroups: [
    {
      label: 'Ignore local workspace packages',
      dependencyTypes: ['local'],
      isIgnored: true,
    },
    {
      label: 'Use highest version for everything else',
      preferVersion: 'highestSemver',
    },
  ],
};
```

### Framework Pinning

```js
export default {
  versionGroups: [
    {
      label: 'Pin React version across all packages',
      dependencies: ['react', 'react-dom', '@types/react', '@types/react-dom'],
      pinVersion: '18.2.0',
    },
  ],
};
```

### Different Rules for Apps vs Libraries

```js
export default {
  versionGroups: [
    {
      label: 'Apps can have any version',
      packages: ['apps/**'],
      isIgnored: true,
    },
    {
      label: 'Libraries must have consistent versions',
      packages: ['packages/**'],
      preferVersion: 'highestSemver',
    },
  ],
};
```

### Ban Security Vulnerabilities

```js
export default {
  versionGroups: [
    {
      label: 'Ban packages with known vulnerabilities',
      dependencies: [
        'lodash', // use lodash-es instead
        'moment', // use date-fns instead
        'request', // use axios/fetch instead
      ],
      isBanned: true,
    },
  ],
};
```

### Peer Dependency Flexibility

```js
export default {
  versionGroups: [
    {
      label: 'Allow peer dependency flexibility',
      dependencyTypes: ['peer'],
      isIgnored: true,
    },
    {
      label: 'Strict versions for prod/dev',
      dependencyTypes: ['prod', 'dev'],
      preferVersion: 'highestSemver',
    },
  ],
};
```

### Scoped Package Ownership

```js
export default {
  versionGroups: [
    {
      label: 'Core team owns @myorg/core',
      dependencies: ['@myorg/core'],
      preferVersion: 'packages/core',
    },
    {
      label: 'UI team owns @myorg/ui-*',
      dependencies: ['@myorg/ui-*'],
      preferVersion: 'packages/ui',
    },
  ],
};
```

## CLI Commands for Version Groups

```bash
# List all version mismatches
npx syncpack list-mismatches

# Fix version mismatches
npx syncpack fix

# Only fix specific dependencies
npx syncpack fix --dependencies react

# Only fix specific dependency types
npx syncpack fix --dependency-types prod,peer
```

## Debugging Version Groups

Use labels and run with verbose output:

```bash
npx syncpack list-mismatches --log-levels warn,error
```

## Order Matters

Version groups are evaluated in order. First matching group wins:

```js
export default {
  versionGroups: [
    // Specific rule first
    { dependencies: ['react'], pinVersion: '18.2.0' },
    // General rule second
    { preferVersion: 'highestSemver' },
  ],
};
```
