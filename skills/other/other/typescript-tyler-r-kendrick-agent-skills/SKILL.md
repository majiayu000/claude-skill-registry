---
name: typescript
description: |
    Use when configuring dev containers for TypeScript or Node.js projects. Covers the Node feature, package managers, ESLint/Prettier extensions, and frontend dev server setup.
    USE FOR: TypeScript/Node.js dev container setup, Node feature, npm/pnpm/yarn configuration, ESLint/Prettier extensions, frontend dev servers
    DO NOT USE FOR: Python dev containers (use python), .NET dev containers (use dotnet), general devcontainer.json (use devcontainer)
license: MIT
metadata:
  displayName: "Dev Container — TypeScript"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Dev Containers Specification"
    url: "https://containers.dev/"
  - title: "TypeScript Official Documentation"
    url: "https://www.typescriptlang.org/docs/"
  - title: "Node.js Official Documentation"
    url: "https://nodejs.org/docs/latest/api/"
---

# Dev Container — TypeScript

## Overview
Configure a dev container for TypeScript and Node.js development using the official Node feature or base image. Supports version selection, package manager configuration (npm, pnpm, yarn), and frontend tooling.

## Node Feature
```jsonc
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "22"
    }
  }
}
```

### Feature Options
| Option | Default | Description |
|--------|---------|-------------|
| `version` | `lts` | Node.js version (`22`, `20`, `lts`, `latest`, `none`) |
| `nodeGypDependencies` | `true` | Install native build dependencies for node-gyp |
| `pnpmVersion` | `none` | Install pnpm (`latest`, `9`, specific version, `none`) |
| `nvmVersion` | `latest` | nvm version |

## Full Example
```jsonc
{
  "name": "TypeScript Development",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:22",
  "forwardPorts": [3000, 5173],
  "portsAttributes": {
    "3000": { "label": "API", "onAutoForward": "notify" },
    "5173": { "label": "Vite Dev Server", "onAutoForward": "openBrowser" }
  },
  "postCreateCommand": "npm ci",
  "postStartCommand": "npm run dev",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss"
      ],
      "settings": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": "explicit"
        },
        "typescript.tsdk": "node_modules/typescript/lib"
      }
    }
  }
}
```

## Using the Base Image vs Feature
| Approach | When to Use |
|----------|-------------|
| `"image": "mcr.microsoft.com/devcontainers/javascript-node:22"` | Node/TS-only projects |
| `"image": "mcr.microsoft.com/devcontainers/typescript-node:22"` | TypeScript-specific image |
| Base image + `ghcr.io/devcontainers/features/node:1` | Multi-language projects |

## Package Managers
### pnpm
```jsonc
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "22",
      "pnpmVersion": "latest"
    }
  },
  "postCreateCommand": "pnpm install --frozen-lockfile"
}
```

### Yarn
```jsonc
{
  "postCreateCommand": "corepack enable && yarn install --immutable"
}
```

## Monorepo Setup (Turborepo / Nx)
```jsonc
{
  "name": "Monorepo",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:22",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "pnpmVersion": "latest"
    }
  },
  "postCreateCommand": "pnpm install --frozen-lockfile",
  "postStartCommand": "pnpm dev",
  "forwardPorts": [3000, 3001, 5173]
}
```

## Frontend Framework Ports
| Framework | Default Port |
|-----------|-------------|
| Vite | 5173 |
| Next.js | 3000 |
| Angular | 4200 |
| Create React App | 3000 |
| Remix | 5173 |
| Astro | 4321 |

## Best Practices
- Use `npm ci` or `pnpm install --frozen-lockfile` in `postCreateCommand` for deterministic installs.
- Use `postStartCommand` for dev servers so they restart on Codespace resume.
- Forward the dev server port and set `"onAutoForward": "openBrowser"` for quick feedback.
- Set `typescript.tsdk` to the workspace TypeScript for consistent version behavior.
- Add both ESLint and Prettier extensions and configure `formatOnSave` for consistent code style.
- Pin Node.js to a major version (`22`, `20`) rather than `lts` for reproducibility.
- Use `corepack enable` for Yarn v2+ to use the project-local version.
