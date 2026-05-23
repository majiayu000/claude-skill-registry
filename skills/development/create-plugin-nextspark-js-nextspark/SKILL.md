---
name: create-plugin
description: |
  Guide for creating new plugins from preset template.
  CRITICAL: Includes MANDATORY dependency management and Model B distribution rules.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
version: "2.0"
---

# Create Plugin Skill

Complete guide for scaffolding and configuring new plugins from the preset template.

---

## ⚠️ MANDATORY: Model B Distribution

> **Los paquetes NPM son para DISTRIBUCIÓN. En proyectos de usuario, el código se COPIA a `/contents/plugins/`.**

### Estructura según contexto:

| Contexto | Plugin Location |
|----------|-----------------|
| **Monorepo** (desarrollo) | `plugins/<plugin-name>/` |
| **Proyecto usuario** | `contents/plugins/<plugin-name>/` (copiado por CLI) |

---

## ⚠️ MANDATORY: package.json Template

Cada plugin DEBE tener un `package.json` con esta estructura:

```json
{
  "name": "@nextsparkjs/plugin-NOMBRE",
  "version": "1.0.0",
  "private": false,
  "main": "./plugin.config.ts",
  "requiredPlugins": [],
  "dependencies": {
    // SOLO dependencias EXCLUSIVAS de este plugin que NO están en core
  },
  "peerDependencies": {
    "@nextsparkjs/core": "workspace:*",
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "zod": "^4.0.0"
  }
}
```

**REGLA CRÍTICA**: Si core tiene una dependencia, el plugin DEBE declararla como `peerDependency`, NUNCA como `dependency`.

---

## Prerequisites

- **Command:** `pnpm create:plugin <plugin-name>`
- **Preset Location:** `core/templates/contents/plugins/starter/`
- **Output Location (monorepo):** `plugins/<plugin-name>/`
- **Output Location (user project):** `contents/plugins/<plugin-name>/`

---

## Step 1: Gather Requirements

Before creating ANY plugin, collect:

```markdown
Required Information:
1. Plugin name (lowercase, hyphenated slug)
2. Display name (human-readable)
3. Description (purpose of the plugin)
4. Author (team or individual)
5. Complexity level (utility | service | full)
6. Primary functionality (what problem does it solve?)
7. Has entities? (yes/no)
```

### Complexity Levels

| Level | Includes | Use When |
|-------|----------|----------|
| `utility` | lib/core.ts, types | Simple helper functions, utilities |
| `service` | API + components + hooks | Most plugins - external API integration |
| `full` | Entities + migrations + everything | Complex plugins with own database tables |

---

## Step 2: Create Plugin from Preset

### Basic Usage

```bash
pnpm create:plugin <plugin-name>
```

### With Options

```bash
pnpm create:plugin <plugin-name> \
  --description "Plugin description" \
  --author "Author Name" \
  --display-name "Display Name" \
  --complexity service
```

### Example

```bash
pnpm create:plugin analytics \
  --description "User analytics and metrics tracking" \
  --author "Development Team" \
  --display-name "Analytics" \
  --complexity service
```

---

## Step 3: Plugin Structure Created

```
plugins/<plugin-name>/              # Monorepo location
├── plugin.config.ts        # Plugin configuration
├── README.md               # Plugin documentation
├── .env.example            # Environment variables template
├── api/
│   └── example/route.ts    # Example API endpoint
├── lib/
│   ├── core.ts             # Core plugin logic
│   ├── types.ts            # TypeScript types
│   └── plugin-env.ts       # Env loader wrapper (REQUIRED)
├── components/
│   └── ExampleWidget.tsx   # Example UI component
├── hooks/
│   └── usePlugin.ts        # Custom React hook
├── entities/               # (if complexity: full)
│   └── [entity]/           # Each entity has 4 required files
│       ├── [entity].config.ts
│       ├── [entity].fields.ts
│       ├── [entity].types.ts
│       ├── [entity].service.ts
│       └── messages/
├── migrations/             # (if complexity: full)
│   └── README.md
├── messages/
│   ├── en.json             # English translations
│   └── es.json             # Spanish translations
└── tests/
    └── plugin.test.ts      # Unit tests
```

---

## Step 4: Customize Configuration

### 4.1 plugin.config.ts - Plugin Identity

```typescript
import type { PluginConfig } from '@/core/types/plugins'
import { exampleFunction } from './lib/core'

export const myPluginConfig: PluginConfig = {
  name: 'my-plugin',
  displayName: 'My Plugin',
  version: '1.0.0',
  description: 'Plugin description',
  enabled: true,

  // Dependencies on other plugins
  dependencies: [],  // e.g., ['auth', 'analytics']

  // Exported API
  api: {
    exampleFunction,
  },

  // Lifecycle hooks
  hooks: {
    onLoad: async () => {
      console.log('[My Plugin] Loading...')
    },
    onActivate: async () => {
      console.log('[My Plugin] Activated')
    },
    onDeactivate: async () => {
      console.log('[My Plugin] Deactivated')
    },
    onUnload: async () => {
      console.log('[My Plugin] Unloaded')
    },
  },
}
```

### 4.2 lib/types.ts - TypeScript Definitions

```typescript
export interface MyPluginConfig {
  apiKey?: string
  baseUrl?: string
  debug?: boolean
}

export interface MyPluginResult {
  success: boolean
  data?: unknown
  message: string
  timestamp: number
}
```

### 4.3 .env.example - Environment Variables

```bash
# ============================================
# MY PLUGIN CONFIGURATION
# ============================================
# Copy this file to .env
# Priority: Plugin .env > Root .env > Defaults

# Required for production
MY_PLUGIN_API_KEY=your-api-key-here

# Optional configuration
MY_PLUGIN_BASE_URL=https://api.example.com
MY_PLUGIN_DEBUG=false
MY_PLUGIN_ENABLED=true
```

### 4.4 lib/plugin-env.ts - Centralized Env Loader (REQUIRED)

Every plugin MUST use the core's centralized env-loader:

```typescript
// plugins/my-plugin/lib/plugin-env.ts
import { getPluginEnv } from '@nextsparkjs/core/lib/plugins/env-loader'

interface MyPluginEnvConfig {
  MY_PLUGIN_API_KEY?: string
  MY_PLUGIN_BASE_URL?: string
  MY_PLUGIN_DEBUG?: string
  MY_PLUGIN_ENABLED?: string
}

class PluginEnvironment {
  private static instance: PluginEnvironment
  private config: MyPluginEnvConfig = {}
  private loaded = false

  private constructor() {
    this.loadEnvironment()
  }

  public static getInstance(): PluginEnvironment {
    if (!PluginEnvironment.instance) {
      PluginEnvironment.instance = new PluginEnvironment()
    }
    return PluginEnvironment.instance
  }

  private loadEnvironment(): void {
    if (this.loaded) return

    const env = getPluginEnv('my-plugin')
    this.config = {
      MY_PLUGIN_API_KEY: env.MY_PLUGIN_API_KEY,
      MY_PLUGIN_BASE_URL: env.MY_PLUGIN_BASE_URL || 'https://api.example.com',
      MY_PLUGIN_DEBUG: env.MY_PLUGIN_DEBUG || 'false',
      MY_PLUGIN_ENABLED: env.MY_PLUGIN_ENABLED || 'true',
    }
    this.loaded = true
  }

  public getApiKey(): string | undefined {
    return this.config.MY_PLUGIN_API_KEY
  }

  public getBaseUrl(): string {
    return this.config.MY_PLUGIN_BASE_URL || 'https://api.example.com'
  }

  public isDebugEnabled(): boolean {
    return this.config.MY_PLUGIN_DEBUG === 'true'
  }

  public isPluginEnabled(): boolean {
    return this.config.MY_PLUGIN_ENABLED !== 'false'
  }
}

export const pluginEnv = PluginEnvironment.getInstance()
```

**Benefits:**
- ✅ Plugin .env takes priority over root .env
- ✅ Automatic fallback to root .env for shared variables
- ✅ Type-safe configuration access
- ✅ Singleton pattern for performance

---

## Step 5: Register Plugin in Sandbox Theme

**Critical Step**: Add the plugin to the plugin-sandbox theme for testing.

```typescript
// contents/themes/plugin-sandbox/config/theme.config.ts
export const pluginSandboxThemeConfig: ThemeConfig = {
  plugins: [
    'my-plugin',  // <-- Add your new plugin here
  ],
}
```

Then rebuild the registry:

```bash
node core/scripts/build/registry.mjs
```

---

## Step 6: Verify Plugin Setup

```bash
# 1. Verify plugin structure
ls -la plugins/<plugin-name>/

# 2. Verify package.json has correct peerDependencies
cat plugins/<plugin-name>/package.json

# 3. Build registry to include new plugin
node core/scripts/build/registry.mjs

# 4. Verify plugin appears in registry
grep "<plugin-name>" core/lib/registries/plugin-registry.ts

# 5. Verify no duplicate dependencies
pnpm ls zod  # Should show ONE version

# 6. Verify no TypeScript errors
pnpm tsc --noEmit

# 7. Test plugin activation (optional)
# Set NEXT_PUBLIC_ACTIVE_THEME=plugin-sandbox in .env.local
# Run: pnpm dev
```

---

## Entity Structure (for full complexity plugins)

Each entity requires 4 files:

| File | Purpose |
|------|---------|
| `[entity].config.ts` | Entity configuration |
| `[entity].fields.ts` | Field definitions |
| `[entity].types.ts` | TypeScript types |
| `[entity].service.ts` | Data access service |

**Reference:** `core/templates/contents/themes/starter/entities/tasks/`

---

## Verification Checklist

### Antes de crear (OBLIGATORIO):
- [ ] Verificar si las dependencias que necesito ya están en core
- [ ] Si están en core → declararlas como `peerDependencies`
- [ ] Si NO están en core → declararlas como `dependencies`

### Después de crear:
- [ ] Plugin name follows naming conventions (lowercase, hyphenated)
- [ ] All preset files created successfully
- [ ] **package.json** tiene nombre `@nextsparkjs/plugin-<name>`
- [ ] **package.json** tiene `peerDependencies` correctas (no duplicar core)
- [ ] plugin.config.ts has correct metadata
- [ ] lib/types.ts has appropriate interfaces
- [ ] **lib/plugin-env.ts** uses core's env-loader
- [ ] .env.example documents all environment variables
- [ ] Plugin registered in plugin-sandbox theme
- [ ] Registry rebuilt: `node core/scripts/build/registry.mjs`
- [ ] Plugin appears in PLUGIN_REGISTRY
- [ ] No duplicate dependencies: `pnpm ls zod` shows ONE version
- [ ] No TypeScript errors: `pnpm tsc --noEmit`

---

## Anti-Patterns

| Pattern | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Manual file creation | Missing files, wrong structure | Use `pnpm create:plugin` |
| Skipping sandbox registration | Can't test plugin | Add to plugin-sandbox theme |
| Skipping registry rebuild | Plugin won't be recognized | Run `node core/scripts/build/registry.mjs` |
| Modifying core files | Architecture violation | Only work in `contents/plugins/` |

---

## Next Steps After Creation

After scaffolding the plugin, continue with implementation:

1. **Implement core business logic** in `lib/`
2. **Create API endpoints** if needed
3. **Build UI components** in `components/`
4. **Add entities** if the plugin manages data
5. **Run verification checklist** above

### Environment Setup
```bash
NEXT_PUBLIC_ACTIVE_THEME='plugin-sandbox'
```

---

## Related Documentation

- **`monorepo-architecture` skill** - CRITICAL: Package hierarchy, dependency rules, Model B distribution
- **`plugins` skill** - Plugin development patterns and dependency management
- Entity System: `core/docs/04-entities/`
- Registry System: `core/docs/03-registry-system/`
