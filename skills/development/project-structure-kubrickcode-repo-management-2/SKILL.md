---
name: project-structure
description: |
  Provides comprehensive project folder structure design guidelines and best practices. Defines standard directory organizations for diverse project types including monorepos, web frameworks, backend services, libraries, and extensions. Ensures scalable, maintainable architecture through consistent file organization patterns. Specializes in separation of concerns, modular architecture, and tooling integration.
  Use when: designing new project structures, organizing monorepo workspaces with tools like Turborepo/Nx, structuring NestJS backend projects, organizing React/Next.js frontend applications, designing Go service architectures, creating NPM package structures, organizing VSCode extension projects, structuring Chrome extension codebases, planning directory hierarchies, migrating legacy project structures, or establishing code organization conventions for teams.
---

# Project Structure Guide

## Monorepo

```
project-root/
├── src/                         # All services/apps
├── infra/                       # Shared infrastructure
├── docs/                        # Documentation
├── .devcontainer/               # Dev Container configuration
├── .github/                     # Workflows, templates
├── .vscode/                     # VSCode settings
├── .claude/                     # Claude settings
├── .gemini/                     # Gemini settings
├── package.json                 # Root package.json. For releases, version management
├── go.work                      # Go workspace (when using Go)
├── justfile                     # Just task runner
├── .gitignore
├── .prettierrc
├── .prettierignore
└── README.md
```

## NestJS

```
project-root/
├── src/
│   ├── domains/
│   ├── common/
│   ├── config/
│   ├── database/
│   ├── app.module.ts
│   └── main.ts
├── tests/
├── package.json
└── tsconfig.json
```

## React

```
project-root/
├── src/
│   ├── pages/              # Page modules
│   ├── domains/            # Domain-shared code
│   ├── components/         # Common UI components
│   ├── layouts/            # Layout-related
│   ├── libs/               # Feature libraries (auth, api, theme)
│   ├── shared/             # Pure utilities
│   ├── app.tsx
│   └── main.tsx
├── public/
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Next.js

```
project-root/
├── app/
│   ├── (routes)/           # Pages (route groups)
│   ├── actions/            # Server Actions (internal mutations)
│   └── api/                # API Routes (external integrations only)
├── components/             # Shared components
├── lib/                    # Utilities and clients
├── public/                 # Static assets
├── middleware.ts           # Edge/Node.js middleware
├── next.config.js
├── package.json
└── tsconfig.json
```

## Go

```
project-root/
├── cmd/                    # Execution entry points (main.go)
├── internal/               # Private packages
├── pkg/                    # Public packages
├── configs/                # Configuration files
├── scripts/                # Utility scripts
├── tests/                  # Integration tests
├── docs/                   # Documentation
├── go.mod
└── go.sum
```

## NPM

```
project-root/
├── cli/                        # CLI execution entry point
├── internal/                   # Private packages
├── pkg/                        # Public packages
├── configs/                    # Configuration files
├── scripts/                    # Utility scripts
├── tests/                      # Integration tests
├── docs/                       # Documentation
├── dist/                       # Build artifacts
├── package.json
├── tsconfig.json
└── README.md
```

## IDE Extension

```
project-root/
├── extension/                   # Extension entry point (activate/deactivate)
├── internal/                    # Private packages
├── pkg/                         # Public packages
├── view/                        # WebView (if applicable)
├── configs/                     # Configuration files
├── scripts/                     # Utility scripts
├── tests/                       # Integration tests
├── public/                      # Static resources (icons, etc.)
├── dist/                        # Build artifacts
├── package.json
├── tsconfig.json
└── .vscodeignore
```

## Chrome Extension

```
project-root/
├── background/                  # Service Worker (Background Script)
├── content/                     # Content Scripts
├── popup/                       # Popup (Extension UI)
├── internal/                    # Private packages
├── pkg/                         # Public packages
├── configs/                     # Configuration files
├── scripts/                     # Utility scripts
├── tests/                       # Integration tests
├── public/                      # Static resources
├── dist/                        # Build artifacts
├── package.json
└── tsconfig.json
```
