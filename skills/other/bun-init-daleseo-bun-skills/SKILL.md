---
name: bun-init
description: Initialize a new Bun project with TypeScript and optimal configuration. Use when starting a new Bun project or converting a directory to a Bun project.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Write", "Read"]
metadata:
  author: dale
  category: bun-runtime
  tags: [bun, javascript, typescript, initialization, setup]
---

# Bun Project Initialization

You are assisting with initializing a new Bun project. Follow these steps to create a well-structured project with optimal configurations.

## Workflow

### 1. Check Prerequisites

First, verify Bun is installed:

```bash
bun --version
```

If Bun is not installed, provide installation instructions for the user's platform.

### 2. Determine Project Type

Ask the user which type of project they want to create:

- **CLI Tool**: Command-line application with bin entry point
- **Web App**: Frontend application with React/Vue/etc
- **API Server**: Backend API with routing framework
- **Library**: Reusable package for publishing to npm

### 3. Run Bun Init

Execute the initialization command:

```bash
bun init -y
```

This creates:
- `package.json` with Bun-optimized scripts
- `tsconfig.json` with recommended TypeScript settings
- `index.ts` as the entry point
- `README.md` with basic project info

### 4. Enhance TypeScript Configuration

Read the generated `tsconfig.json` and enhance it based on project type:

**For CLI Tools:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

**For Web Apps:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "types": ["bun-types"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

**For API Servers:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**For Libraries:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "strict": true,
    "declaration": true,
    "declarationMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

### 5. Create Project Structure

Generate appropriate directory structure and files:

**CLI Tool:**
```
project/
├── src/
│   ├── index.ts          # Main CLI entry point
│   ├── commands/         # Command handlers
│   └── utils/            # Shared utilities
├── tests/
│   └── index.test.ts
├── package.json
├── tsconfig.json
├── .gitignore
├── .env.example
└── README.md
```

Create `src/index.ts`:
```typescript
#!/usr/bin/env bun

console.log("Hello from Bun CLI!");

// Example: Parse command line arguments
const args = process.argv.slice(2);
console.log("Arguments:", args);
```

Update `package.json` to add bin field:
```json
{
  "bin": {
    "your-cli-name": "./src/index.ts"
  }
}
```

**Web App:**
```
project/
├── src/
│   ├── index.tsx         # App entry point
│   ├── components/       # React components
│   ├── styles/           # CSS/styles
│   └── utils/            # Utilities
├── public/
│   └── index.html
├── tests/
├── package.json
├── tsconfig.json
├── .gitignore
├── .env.example
└── README.md
```

**API Server:**
```
project/
├── src/
│   ├── index.ts          # Server entry point
│   ├── routes/           # Route handlers
│   ├── middleware/       # Express/Hono middleware
│   ├── services/         # Business logic
│   └── types/            # TypeScript types
├── tests/
├── package.json
├── tsconfig.json
├── .gitignore
├── .env.example
└── README.md
```

Create `src/index.ts`:
```typescript
const server = Bun.serve({
  port: 3000,
  fetch(request) {
    return new Response("Welcome to Bun!");
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

**Library:**
```
project/
├── src/
│   ├── index.ts          # Main export
│   └── types.ts          # Type definitions
├── tests/
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md
```

### 6. Create .gitignore

Generate a comprehensive `.gitignore`:

```gitignore
# Bun
node_modules
bun.lockb
*.bun

# Environment
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.tsbuildinfo

# Logs
logs
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Test coverage
coverage/
.nyc_output/
```

### 7. Create Environment Template

Create `.env.example`:

```bash
# Application
NODE_ENV=development
PORT=3000

# Add your environment variables here
# DATABASE_URL=
# API_KEY=
```

### 8. Update package.json Scripts

Add project-type-specific scripts:

**CLI Tool:**
```json
{
  "scripts": {
    "dev": "bun run src/index.ts",
    "test": "bun test",
    "lint": "bun run --bun eslint src",
    "typecheck": "bun run --bun tsc --noEmit"
  }
}
```

**Web App:**
```json
{
  "scripts": {
    "dev": "bun run --hot src/index.tsx",
    "build": "bun build src/index.tsx --outdir=dist --minify",
    "test": "bun test",
    "typecheck": "bun run --bun tsc --noEmit"
  }
}
```

**API Server:**
```json
{
  "scripts": {
    "dev": "bun run --hot src/index.ts",
    "start": "bun run src/index.ts",
    "test": "bun test",
    "typecheck": "bun run --bun tsc --noEmit"
  }
}
```

**Library:**
```json
{
  "scripts": {
    "build": "bun build src/index.ts --outdir=dist --minify --sourcemap=external",
    "test": "bun test",
    "typecheck": "bun run --bun tsc --noEmit",
    "prepublishOnly": "bun run build && bun test"
  }
}
```

### 9. Install Common Dependencies

Suggest installing common dependencies based on project type:

**CLI Tool:**
```bash
bun add commander chalk ora
bun add -d @types/node
```

**Web App:**
```bash
bun add react react-dom
bun add -d @types/react @types/react-dom
```

**API Server:**
```bash
bun add hono
bun add -d @types/node
```

**Library:**
```bash
# No default dependencies - user will add as needed
```

### 10. Create Initial Test File

Create a basic test file in `tests/`:

```typescript
import { describe, expect, test } from "bun:test";

describe("Initial test", () => {
  test("basic assertion", () => {
    expect(1 + 1).toBe(2);
  });
});
```

## Post-Initialization Checklist

After completing the setup, provide the user with:

1. ✅ Confirmation of project type created
2. ✅ List of generated files and directories
3. ✅ Next steps:
   - Copy `.env.example` to `.env` and configure
   - Run `bun install` if dependencies were suggested
   - Run `bun dev` to start development
   - Run `bun test` to verify tests work

## Key Configuration Principles

- **Module Resolution**: Use `"moduleResolution": "bundler"` for Bun's native resolution
- **TypeScript Types**: Always include `"types": ["bun-types"]`
- **No Emit**: Set `"noEmit": true` since Bun runs TypeScript directly
- **Import Extensions**: Enable `"allowImportingTsExtensions": true` for `.ts` imports
- **Strict Mode**: Enable strict TypeScript checks for better code quality

## Common Adjustments

**If user wants workspaces (monorepo):**

Add to `package.json`:
```json
{
  "workspaces": ["packages/*"]
}
```

**If user wants path aliases:**

Add to `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"]
    }
  }
}
```

**If user wants JSX without React:**

Update `tsconfig.json`:
```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "preact" // or other JSX runtime
  }
}
```

## Completion

Once all files are created, inform the user that initialization is complete and provide a summary of:
- Project structure
- Available npm scripts
- Recommended next steps
- Links to Bun documentation for their project type
