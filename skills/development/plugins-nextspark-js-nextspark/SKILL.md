---
name: plugins
description: |
  Plugin development system for this Next.js application.
  Covers plugin structure, configuration, lifecycle hooks, registry integration, environment variables, and testing patterns.
  CRITICAL: Includes MANDATORY dependency management rules for NPM distribution.
  Use this skill when creating, modifying, or validating plugins.
allowed-tools: Read, Glob, Grep, Bash
version: 2.1.0
---

# Plugins Skill

Patterns for developing plugins in this Next.js application.

## Architecture Overview

### Model B Distribution: Plugin Locations

| Context | Plugin Location | Reason |
|---------|-----------------|--------|
| **Monorepo** (development) | `plugins/<plugin-name>/` | Workspace package |
| **Consumer project** | `contents/plugins/<plugin-name>/` | Copied by CLI (not node_modules) |

> **CRITICAL**: NPM packages are for DISTRIBUTION. In consumer projects, code is COPIED to `/contents/plugins/`, NOT kept in `node_modules`.

```
Plugin Structure (Monorepo):
plugins/
└── [plugin-name]/
    ├── package.json            # REQUIRED: peerDependencies
    ├── plugin.config.ts        # Plugin configuration (REQUIRED)
    ├── README.md               # Documentation (REQUIRED)
    ├── .env.example            # Environment template (REQUIRED)
    ├── types/                  # TypeScript definitions
    ├── lib/                    # Core logic
    ├── hooks/                  # React hooks
    ├── components/             # React components
    ├── providers/              # Context providers
    ├── api/                    # API endpoints
    ├── entities/               # Plugin entities (optional)
    └── docs/                   # Documentation

Plugin Types: utility | service | configuration
→ See references/plugin-types.md for detailed structures
```

---

## MANDATORY: NPM Distribution & Dependency Management

### Fundamental Principle

> **If `@nextsparkjs/core` has a dependency, plugins MUST declare it as `peerDependency`, NEVER as `dependency`.**

### Why It's MANDATORY

```
❌ WRONG - Duplicate dependencies (FORBIDDEN):
┌─────────────────────────────────────────────────┐
│ node_modules/                                   │
│ ├── @nextsparkjs/core/                          │
│ │   └── node_modules/zod@4.1.5  ← Instance 1    │
│ ├── @nextsparkjs/plugin-ai/                     │
│ │   └── node_modules/zod@4.1.5  ← Instance 2    │
│ └── @nextsparkjs/plugin-langchain/              │
│     └── node_modules/zod@3.23.0 ← Instance 3!   │
└─────────────────────────────────────────────────┘
Result: Type conflicts, instanceof errors, bloated bundle

✅ CORRECT - Single instance (MANDATORY):
┌─────────────────────────────────────────────────┐
│ node_modules/                                   │
│ ├── zod@4.1.5  ← ONE single instance (hoisted)  │
│ ├── @nextsparkjs/core/  (provides zod)          │
│ ├── @nextsparkjs/plugin-ai/  (uses host's zod)  │
│ └── @nextsparkjs/plugin-langchain/ (uses zod)   │
└─────────────────────────────────────────────────┘
Result: No conflicts, optimized bundle
```

### Dependency Classification

| Category | Type | Examples |
|----------|------|----------|
| **Singleton libraries** | `peerDependencies` | zod, react, react-dom, next |
| **Shared with core** | `peerDependencies` | @tanstack/react-query, lucide-react |
| **Plugin-exclusive** | `dependencies` | @ai-sdk/*, @langchain/* |

### Dependencies Core Provides (NEVER duplicate)

```json
{
  "zod": "^4.1.5",
  "@tanstack/react-query": "^5.85.0",
  "lucide-react": "^0.539.0",
  "class-variance-authority": "^0.7.1",
  "clsx": "^2.1.1",
  "tailwind-merge": "^3.3.1",
  "date-fns": "^4.1.0",
  "react-hook-form": "^7.62.0",
  "sonner": "^2.0.7",
  "next-intl": "^4.3.4",
  "better-auth": "^1.3.5"
}
```

### MANDATORY package.json Template

```json
{
  "name": "@nextsparkjs/plugin-NAME",
  "version": "1.0.0",
  "private": false,
  "main": "./plugin.config.ts",
  "dependencies": {
    "@ai-sdk/anthropic": "^2.0.17"  // ✅ Only THIS plugin uses it
  },
  "peerDependencies": {
    "@nextsparkjs/core": "workspace:*",
    "next": "^15.0.0",
    "react": "^19.0.0",
    "zod": "^4.0.0"
  }
}
```

---

## When to Use This Skill

- Creating new plugins
- Understanding plugin structure
- Implementing plugin lifecycle hooks
- Configuring plugin environment variables
- Integrating plugins with the registry

---

## Plugin Configuration (REQUIRED)

Every plugin MUST have a `plugin.config.ts` file:

```typescript
import { z } from 'zod'
import type { PluginConfig } from '@/core/types/plugin'

const MyPluginConfigSchema = z.object({
  apiKey: z.string().min(1),
  timeout: z.number().min(1000).default(5000),
  debugMode: z.boolean().default(false)
})

export const myPluginConfig: PluginConfig = {
  name: 'my-plugin',
  version: '1.0.0',
  displayName: 'My Custom Plugin',
  description: 'Clear description of plugin functionality',
  enabled: true,
  dependencies: [],

  components: { MyComponent: undefined },
  services: { useMyService: undefined },

  hooks: {
    async onLoad() { console.log('[My Plugin] Loading...') },
    async onActivate() { console.log('[My Plugin] Activated') },
    async onDeactivate() { console.log('[My Plugin] Deactivated') },
    async onUnload() { console.log('[My Plugin] Unloaded') }
  }
}

export default myPluginConfig
```

---

## Environment Variables Pattern

### ⭐ Centralized Plugin Env Loader (RECOMMENDED)

Use the core's centralized env-loader for automatic plugin `.env` loading:

```typescript
// contents/plugins/my-plugin/lib/plugin-env.ts
import { getPluginEnv } from '@nextsparkjs/core/lib/plugins/env-loader'

const env = getPluginEnv('my-plugin')
const apiKey = env.MY_PLUGIN_API_KEY
const enabled = env.MY_PLUGIN_ENABLED === 'true'
```

### Priority System

1. **Plugin `.env`** (`contents/plugins/my-plugin/.env`) - Highest priority
2. **Root `.env`** (project root) - Fallback
3. **Built-in defaults** - Lowest priority

### Namespace-Based Architecture

**SHARED Variables (root `.env`):**
- `DATABASE_URL`, `BETTER_AUTH_SECRET`
- `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` (can be shared across plugins)

**PLUGIN Variables (plugin `.env` with prefix):**
- All plugin-specific variables MUST use `MY_PLUGIN_*` namespace

```bash
# contents/plugins/my-plugin/.env.example
# Plugin-specific configuration
MY_PLUGIN_ENABLED=true
MY_PLUGIN_DEBUG=false
MY_PLUGIN_API_KEY=your-api-key-here
MY_PLUGIN_TIMEOUT=5000
```

### Required Files

| File | Purpose |
|------|---------|
| `.env.example` | Template with all variables documented |
| `lib/plugin-env.ts` | Type-safe wrapper using core's env-loader |

---

## Plugin Registry Integration

### Auto-Generated Registry

```typescript
// core/lib/registries/plugin-registry.ts (AUTO-GENERATED)
export const PLUGIN_REGISTRY: Record<string, PluginRegistryEntry> = {
  'my-plugin': {
    name: 'my-plugin',
    config: myPluginConfig,
    hasAPI: true,
    apiPath: '/api/plugin/my-plugin',
    hasComponents: true
  }
}
```

### Rebuild Registry

```bash
# After creating or modifying plugins
node core/scripts/build/registry.mjs
```

---

## Scripts

### Scaffold New Plugin

```bash
python .claude/skills/plugins/scripts/scaffold-plugin.py \
  --name "my-plugin" \
  --type "service" \
  --features "components,hooks,api"
```

---

## Anti-Patterns

```typescript
// ❌ NEVER: Put dependencies that core already has
{
  "dependencies": {
    "zod": "^4.0.0",           // ❌ Core has it → peerDependency
    "react": "^19.0.0"          // ❌ Core has it → peerDependency
  }
}

// ❌ NEVER: Put global variables in plugin .env
// USE_LOCAL_AI=true  // WRONG - This overrides root .env!

// ❌ NEVER: Hardcode configuration
const config = { apiKey: 'hardcoded-key' }

// ❌ NEVER: Skip error handling in handlers
export async function badProcess(data: any) {
  return await externalAPI(data)  // No try/catch
}

// ❌ NEVER: Use any types
export interface BadInterface { data: any }
```

---

## Checklist

### Before Creating (MANDATORY)

- [ ] Verify if dependencies are already in core
- [ ] If in core → declare as `peerDependencies`
- [ ] If NOT in core → declare as `dependencies`
- [ ] NEVER duplicate: zod, react, next, @tanstack/*, lucide-react

### During Development

- [ ] Plugin name follows kebab-case convention
- [ ] `plugin.config.ts` with all required fields
- [ ] `README.md` with usage documentation
- [ ] `.env.example` with namespaced variables only
- [ ] `lib/plugin-env.ts` using core's env-loader
- [ ] Types defined in `types/` directory
- [ ] All variables use `MY_PLUGIN_*` namespace
- [ ] Components have `data-cy` selectors

### After Implementation

- [ ] Run `node core/scripts/build/registry.mjs`
- [ ] Unit tests with 90%+ coverage
- [ ] E2E tests with Page Object Model
- [ ] Build passes: `pnpm build`

### Validate Dependencies

```bash
pnpm ls zod  # Should show ONE version only
```

---

## References

- `references/plugin-types.md` - Detailed plugin type structures
- `references/plugin-templates.md` - Component, hook, API templates
- `references/plugin-testing.md` - Testing patterns and POMs

## Related Skills

- `monorepo-architecture` - Package hierarchy and dependency rules
- `cypress-selectors` - Selector patterns for plugin components
- `tanstack-query` - Data fetching in plugin hooks
- `zod-validation` - Input validation for plugin APIs
- `registry-system` - Plugin registry integration
