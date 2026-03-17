---
name: monorepo-deps
description: pnpm monorepo dependency management patterns. Use when adding, updating, or aligning package versions.
license: MIT
---

# Monorepo Dependency Management

## When to Use

Activate when:

- Adding new dependencies
- Updating package versions
- Fixing "multiple React instances" errors
- Aligning versions across packages

## Workspace Structure

```
ReactSpacesMonoRepo/
├── package.json          # Root - shared deps, overrides
├── pnpm-workspace.yaml   # Workspace definition
├── pnpm-lock.yaml        # Lock file (DO NOT npm install)
├── packages/
│   ├── shared/           # @disruptive-spaces/shared
│   ├── webgl/            # @disruptive-spaces/webgl
│   ├── chat/             # @disruptive-spaces/chat
│   ├── header-auth-links/
│   ├── testing/          # Dev harness
│   └── website/
└── functions/            # Firebase (separate deps)
```

## Commands

```bash
# Install all deps
pnpm install

# Add to specific package
pnpm add lodash --filter @disruptive-spaces/webgl

# Add to root (shared)
pnpm add -w typescript

# Update all instances of a package
pnpm update react --recursive

# Check for outdated
pnpm outdated --recursive
```

## Version Alignment

### Current Issues

| Package           | Should Be | Check                       |
| ----------------- | --------- | --------------------------- |
| firebase          | ^11.5.0   | All packages                |
| agora-rtc-sdk-ng  | ^4.24.0   | webgl, website, root        |
| react-unity-webgl | ^10.1.6   | webgl, header-auth, testing |
| vite              | ^6.2.2    | All packages with vite      |

### Enforcing Versions

In root `package.json`:

```json
{
  "pnpm": {
    "overrides": {
      "react": "^18.2.0",
      "react-dom": "^18.2.0"
    }
  }
}
```

## Hoisting Common Dependencies

Dependencies used in 3+ packages should be hoisted to root:

```json
// Root package.json
{
  "dependencies": {
    "@chakra-ui/react": "^2.8.2",
    "@emotion/react": "^11.11.3",
    "framer-motion": "^11.0.0",
    "react-icons": "^5.0.0"
  }
}
```

Then in workspace packages:

```json
// packages/webgl/package.json
{
  "dependencies": {
    "@chakra-ui/react": "workspace:*"
  }
}
```

## Workspace References

```json
// packages/webgl/package.json
{
  "dependencies": {
    "@disruptive-spaces/shared": "workspace:*"
  }
}
```

## React Deduplication

### Problem

Multiple React instances cause:

- Hooks errors (`Invalid hook call`)
- Context not working across packages
- `useEffect` running twice unexpectedly

### Solution

1. **Root overrides** (already set):

```json
{
  "pnpm": {
    "overrides": {
      "react": "^18.2.0",
      "react-dom": "^18.2.0"
    }
  }
}
```

2. **Vite alias** (in each vite.config.js):

```javascript
resolve: {
  alias: {
    'react': path.resolve(rootDir, 'node_modules/react'),
    'react-dom': path.resolve(rootDir, 'node_modules/react-dom'),
  },
  dedupe: ['react', 'react-dom', 'framer-motion', '@chakra-ui/react']
}
```

## Adding New Packages

### To a workspace package

```bash
# Correct
pnpm add axios --filter @disruptive-spaces/webgl

# Wrong (uses npm, breaks lock)
cd packages/webgl && npm install axios
```

### Shared dependency

```bash
# Add to root
pnpm add -w lodash

# Reference from package
# packages/webgl/package.json: "lodash": "workspace:*"
```

## Checking for Issues

```bash
# Find duplicate packages
pnpm why react

# List all versions of a package
pnpm list react --recursive

# Find mismatched versions
pnpm outdated --recursive
```

## TypeScript in Monorepo

### Root tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@disruptive-spaces/shared/*": ["packages/shared/*"]
    }
  }
}
```

### Package tsconfig.json

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

## Common Issues

| Issue                       | Cause                    | Fix                               |
| --------------------------- | ------------------------ | --------------------------------- |
| Lock file conflict          | Used npm instead of pnpm | Delete node_modules, pnpm install |
| Multiple React              | Missing dedupe config    | Add Vite alias + dedupe           |
| Type errors across packages | Missing path aliases     | Update tsconfig paths             |
| Version mismatch            | Added without workspace: | Use `workspace:*` references      |

## Related Skills

- `vite-config` - Vite build configuration
- `frontend-development` - React patterns
