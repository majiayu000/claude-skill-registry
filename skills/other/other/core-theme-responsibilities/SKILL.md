---
name: core-theme-responsibilities
description: |
  Core/Theme/Plugin responsibility assignment system for this application.
  Covers dependency direction, responsibility assignment rules, common anti-patterns, and validation.
  **CRITICAL SKILL** - Read before creating any technical plan involving core and theme/plugin interaction.
  See also: `monorepo-architecture` skill for package distribution and dependency management.
allowed-tools: Read, Glob, Grep
version: 2.0.0
---

# Core/Theme/Plugin Responsibilities Skill

Patterns for correctly assigning responsibilities between Core, Theme, and Plugin components.

## The Fundamental Principle

**"CORE ORCHESTRATES, EXTENSIONS REGISTER"**

- **Core**: Provides mechanisms, initialization, processing, orchestration
- **Theme/Plugin**: Provides configuration, data, UI customization

## Architecture Overview

```
RESPONSIBILITY FLOW:

┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEPENDENCY DIRECTION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                    ┌─────────────────────┐                                   │
│                    │        CORE         │                                   │
│                    │  (Orchestration)    │                                   │
│                    │  - Initialization   │                                   │
│                    │  - Processing       │                                   │
│                    │  - Services         │                                   │
│                    │  - Types/Interfaces │                                   │
│                    └──────────▲──────────┘                                   │
│                               │                                              │
│              ┌────────────────┼────────────────┐                            │
│              │                │                │                             │
│              ▼                ▼                ▼                             │
│     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                     │
│     │    THEME    │   │   PLUGIN    │   │   PLUGIN    │                     │
│     │   (Data)    │◄──│   (Data)    │   │   (Data)    │                     │
│     │ - Config    │   │ - Config    │   │ - Config    │                     │
│     │ - Handlers  │   │ - Handlers  │   │ - Handlers  │                     │
│     │ - UI        │   │ - Logic*    │   │ - Logic*    │                     │
│     └─────────────┘   └─────────────┘   └─────────────┘                     │
│                                                                              │
│  * Plugins can have self-contained logic that doesn't require Core import   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

IMPORT RULES:

  ✅ ALLOWED:                              ❌ PROHIBITED:
  ─────────────────────────────────────    ─────────────────────────────────
  • Core → Core                            • Core → Theme
  • Theme → Core                           • Core → Plugin
  • Plugin → Core                          • Theme → other Theme
  • Theme → Plugin
  • Theme → same Theme
  • Plugin → same Plugin
  • Plugin → other Plugin (allowed!)
```

## When to Use This Skill

- **Planning new features** that span core and theme/plugin
- **Reviewing architectural plans** for responsibility assignment errors
- **Debugging import loops** caused by wrong responsibility placement
- **Creating extension systems** (scheduled actions, hooks, handlers)

## Development Context Awareness

**CRITICAL:** Before applying patterns from this skill, check `.claude/config/context.json` to understand the development environment.

### Context Detection

```typescript
const context = await Read('.claude/config/context.json')

if (context.context === 'monorepo') {
  // Full access to core/, themes/, plugins/
  // You ARE developing the NextSpark framework
} else if (context.context === 'consumer') {
  // Core is READ-ONLY (installed via npm)
  // You are developing an APPLICATION using NextSpark
}
```

### Two Development Contexts

```
┌─────────────────────────────────────────────────────────────────┐
│  MONOREPO CONTEXT                                               │
│  (Developing NextSpark Framework)                               │
├─────────────────────────────────────────────────────────────────┤
│  • context.json: { "context": "monorepo" }                     │
│  • CAN create/modify in core/                                  │
│  • CAN create/modify in any theme                              │
│  • Focus: Abstract, reusable patterns for the platform         │
│  • Examples: core/services/, core/migrations/, core/entities/  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  CONSUMER CONTEXT                                               │
│  (Building App with NextSpark)                                  │
├─────────────────────────────────────────────────────────────────┤
│  • context.json: { "context": "consumer" }                     │
│  • Core is READ-ONLY (in node_modules/)                        │
│  • CAN ONLY create in active theme and plugins                 │
│  • Focus: Project-specific features                            │
│  • Examples: contents/themes/{theme}/services/                 │
└─────────────────────────────────────────────────────────────────┘
```

### Path Translation Rules

When a skill or pattern shows a `core/` path, translate based on context:

| Pattern Shows | Monorepo Creates In | Consumer Creates In |
|---------------|--------------------|--------------------|
| `core/lib/services/` | `core/lib/services/` | `contents/themes/{theme}/services/` |
| `core/migrations/` | `core/migrations/` | `contents/themes/{theme}/migrations/` |
| `core/entities/` | `core/entities/` | `contents/themes/{theme}/entities/` |
| `core/components/` | `core/components/` | `contents/themes/{theme}/components/` |
| `core/hooks/` | `core/hooks/` | `contents/themes/{theme}/hooks/` |
| `core/lib/` | `core/lib/` | `contents/themes/{theme}/lib/` |

### Consumer Context Rules

In consumer context (`context.context === "consumer"`):

1. **Core is READ-ONLY** - Never attempt to create/modify in `core/`
2. **Use existing core services** - Import and use, don't duplicate
3. **Extend, don't replace** - Create theme-specific extensions
4. **Theme migrations run after core** - Use sequence numbers 1001+

### When Consumer Needs Core Functionality

If you discover that a feature truly requires core changes:

```markdown
## Core Enhancement Request

**Feature:** [What you need]
**Why Core:** [Why it can't be in theme]
**Proposed Solution:** [How core could support this]

**Workaround (if possible):**
[Temporary theme-based solution]
```

Document this and either:
1. Implement a workaround in theme
2. Request the enhancement upstream to NextSpark

---

## Responsibility Assignment Rules

### Quick Decision Table

| Question | Answer | Responsibility |
|----------|--------|----------------|
| Does Core need to call this function? | YES | **CORE** |
| Is it system initialization? | YES | **CORE** |
| Does it process data from multiple sources? | YES | **CORE** |
| Does it orchestrate a workflow? | YES | **CORE** |
| Does it define shared interfaces/types? | YES | **CORE** |
| Is it theme-specific configuration? | YES | **THEME** |
| Is it data for a registry? | YES | **THEME/PLUGIN** |
| Is it UI or visual components? | YES | **THEME** (or CORE base) |

### Detailed Responsibility Matrix

| Functionality Type | Core | Theme | Plugin | Notes |
|--------------------|:----:|:-----:|:------:|-------|
| **Feature initialization** | ✅ | ❌ | ❌ | Core ALWAYS initializes |
| **Data processing** | ✅ | ❌ | ❌ | Core processes, extensions provide data |
| **Workflow orchestration** | ✅ | ❌ | ❌ | Core controls the flow |
| **Type/interface definitions** | ✅ | ❌ | ❌ | Contracts live in Core |
| **Services with business logic** | ✅ | ❌ | ⚠️ | Plugin only if self-contained |
| **Build scripts** | ✅ | ❌ | ❌ | Only Core generates registries |
| **Feature configuration** | ❌ | ✅ | ✅ | Data-only configs |
| **Registry data** | ❌ | ✅ | ✅ | Imported only by build script |
| **Handlers/Callbacks** | ❌ | ✅ | ✅ | Registered, not executed directly |
| **UI components** | Base | ✅ | ✅ | Core provides base, extensions extend |
| **Styles/CSS** | Base | ✅ | ❌ | Theme controls presentation |
| **Functionality extensions** | ❌ | ✅ | ✅ | Register via registry |

## Common Anti-Patterns

### Anti-Pattern 1: Initialization in Theme

```typescript
// ❌ INCORRECT - Initialization in Theme
// contents/themes/default/scheduled-actions/init.ts
export function initializeScheduledActions() {
  const actions = loadThemeActions()
  actions.forEach(action => schedule(action))
}

// core/lib/startup.ts
import { initializeScheduledActions } from '@/contents/themes/default/...'
// ^^^ PROHIBITED - Core cannot import from Theme

// ✅ CORRECT - Initialization in Core
// core/lib/scheduled-actions/init.ts
import { SCHEDULED_ACTIONS_REGISTRY } from '@/core/lib/registries'

export function initializeScheduledActions() {
  // Core reads from registry (data-only)
  const actions = Object.values(SCHEDULED_ACTIONS_REGISTRY)
  actions.forEach(action => scheduleAction(action))
}

// contents/themes/default/config/scheduled-actions.ts
export const THEME_SCHEDULED_ACTIONS = [
  { slug: 'daily-report', cron: '0 9 * * *' }
]
// ^^^ This is DATA, imported only by build script
```

### Anti-Pattern 2: Functions in Registry

```typescript
// ❌ INCORRECT - Functions in Registry
export const HANDLERS_REGISTRY = {
  'process-payment': async (data) => {
    // Processing logic
    await chargeCard(data.cardId, data.amount)
  }
}

// ✅ CORRECT - References in Registry, logic in Services
// Registry (data-only)
export const HANDLERS_REGISTRY = {
  'process-payment': {
    slug: 'process-payment',
    handlerPath: 'billing/process-payment',
    description: 'Process a payment'
  }
}

// Service (logic)
// core/lib/services/handler.service.ts
import { HANDLER_IMPLEMENTATIONS } from '@/core/lib/registries/handler-implementations'

export class HandlerService {
  static async execute(slug: string, data: unknown) {
    const handler = HANDLER_IMPLEMENTATIONS[slug]
    return handler(data)
  }
}
```

### Anti-Pattern 3: Core Importing from Theme

```typescript
// ❌ INCORRECT - Core importing from Theme
// core/lib/billing/plans.ts
import { CUSTOM_PLANS } from '@/contents/themes/default/config/plans'

export function getPlan(slug: string) {
  return PLANS[slug] || CUSTOM_PLANS[slug]
}

// ✅ CORRECT - Core reads from unified registry
// core/lib/billing/plans.ts
import { BILLING_REGISTRY } from '@/core/lib/registries/billing-registry'

export function getPlan(slug: string) {
  return BILLING_REGISTRY.plans[slug]
}

// The build script combines core plans + theme plans into BILLING_REGISTRY
```

### Anti-Pattern 4: Theme Processing Data

```typescript
// ❌ INCORRECT - Theme processing data
// contents/themes/default/lib/scheduled-actions/processor.ts
export async function processScheduledActions() {
  const actions = await db.query.scheduledActions.findMany()
  for (const action of actions) {
    await executeAction(action)
  }
}

// ✅ CORRECT - Core processes, Theme configures
// core/lib/scheduled-actions/processor.ts (CORE)
export async function processScheduledActions() {
  const actions = await db.query.scheduledActions.findMany()
  for (const action of actions) {
    await executeAction(action)
  }
}

// contents/themes/default/config/scheduled-actions.ts (THEME - data only)
export const themeScheduledActions = {
  'cleanup-expired': { cron: '0 0 * * *', enabled: true }
}
```

## Correct Patterns

### Pattern 1: Extension Points

```typescript
// PATTERN: Core defines extension points, Theme/Plugin register

// 1. Core defines types and mechanism
// core/lib/hooks/types.ts
export interface HookDefinition {
  slug: string
  event: string
  priority: number
}

// core/lib/hooks/service.ts
import { HOOKS_REGISTRY } from '@/core/lib/registries/hooks-registry'

export class HooksService {
  static trigger(event: string, data: unknown) {
    const hooks = Object.values(HOOKS_REGISTRY)
      .filter(h => h.event === event)
      .sort((a, b) => b.priority - a.priority)

    for (const hook of hooks) {
      const handler = this.getHandler(hook.slug)
      handler(data)
    }
  }
}

// 2. Theme registers hooks (DATA)
// contents/themes/default/config/hooks.ts
export const THEME_HOOKS: HookDefinition[] = [
  { slug: 'log-user-login', event: 'user.login', priority: 10 }
]

// 3. Theme provides handlers (registered via registry)
// contents/themes/default/handlers/hooks/log-user-login.ts
export const logUserLoginHandler = async (data: UserLoginEvent) => {
  console.log(`User logged in: ${data.userId}`)
}
// This handler is imported by build script → HANDLER_IMPLEMENTATIONS registry
```

### Pattern 2: Feature Configuration

```typescript
// PATTERN: Core provides feature, Theme configures

// 1. Core defines the feature with defaults
// core/lib/features/notifications.ts
import { NOTIFICATIONS_CONFIG_REGISTRY } from '@/core/lib/registries'

const DEFAULT_CONFIG = {
  emailEnabled: true,
  pushEnabled: false,
  channels: ['email']
}

export function getNotificationConfig() {
  // Merge: defaults ← theme config
  return {
    ...DEFAULT_CONFIG,
    ...NOTIFICATIONS_CONFIG_REGISTRY.themeConfig
  }
}

// 2. Theme provides specific configuration
// contents/themes/default/config/notifications.ts
export const themeNotificationsConfig = {
  pushEnabled: true,
  channels: ['email', 'push', 'sms']
}
```

### Pattern 3: Handler Registration

```typescript
// PATTERN: Theme provides handlers, Core executes them

// 1. Theme defines handlers (functions, but registered)
// contents/themes/default/handlers/scheduled/send-daily-report.ts
import type { ScheduledHandler } from '@/core/lib/scheduled-actions/types'

export const sendDailyReportHandler: ScheduledHandler = async (context) => {
  const users = await context.db.query.users.findMany()
  for (const user of users) {
    await sendEmail(user.email, 'Daily Report', generateReport())
  }
}

// 2. Build script generates implementations registry
// core/lib/registries/scheduled-handler-implementations.ts (AUTO-GENERATED)
import { sendDailyReportHandler } from '@/contents/themes/default/handlers/scheduled/send-daily-report'

export const SCHEDULED_HANDLER_IMPLEMENTATIONS = {
  'send-daily-report': sendDailyReportHandler
}

// 3. Core executes handlers from registry
// core/lib/scheduled-actions/executor.ts
import { SCHEDULED_HANDLER_IMPLEMENTATIONS } from '@/core/lib/registries'

export async function executeScheduledAction(action: ScheduledAction) {
  const handler = SCHEDULED_HANDLER_IMPLEMENTATIONS[action.handlerSlug]
  if (!handler) throw new Error(`Handler not found: ${action.handlerSlug}`)
  await handler({ db, action })
}
```

## Triple-Check Validation

### Before Creating Any Plan

```markdown
## RESPONSIBILITIES CHECKLIST (MANDATORY)

### 1. Function Identification
For each function/component, answer:

| Function | Who calls it? | What does it do? | Location |
|----------|---------------|------------------|----------|
| `initFeature()` | Core startup | Initializes | CORE |
| `processData()` | Core service | Processes | CORE |
| `featureConfig` | Build script | Data | THEME |

### 2. Import Verification
- [ ] Does Core import from Theme? → ❌ REDESIGN
- [ ] Does Core import from Plugin? → ❌ REDESIGN
- [ ] Does Theme import from another Theme? → ❌ REDESIGN
- [ ] Does Plugin import from another Plugin? → ✅ ALLOWED (use peerDependencies)

### 3. Registry Verification
- [ ] Are registries DATA-ONLY? → ✅
- [ ] Are there functions in registries? → ❌ Extract to Services

### 4. Responsibility Verification
- [ ] Initialization → In Core? ✅
- [ ] Processing → In Core? ✅
- [ ] Orchestration → In Core? ✅
- [ ] Configuration → In Theme/Plugin? ✅
- [ ] UI → In Theme? ✅
```

### Red Flags (Warning Signs)

If the plan contains any of these, **STOP AND REDESIGN**:

1. **"Theme will initialize..."** → Core must initialize
2. **"Core will import from theme..."** → Prohibited
3. **"Registry will contain handler functions..."** → Data-only
4. **"Theme will process the data..."** → Core processes
5. **"Plugin will orchestrate..."** → Core orchestrates (unless self-contained)

## Checklist

Before finalizing any architectural plan:

- [ ] Core does not import from Theme or Plugin
- [ ] Theme does not import from another Theme
- [ ] Plugin does not import from another Plugin
- [ ] Initialization is in Core
- [ ] Processing is in Core
- [ ] Orchestration is in Core
- [ ] Registries are DATA-ONLY
- [ ] Theme/Plugin only provide configuration and registered handlers
- [ ] Build script is the only one that imports from contents/

## Related Skills

- **`monorepo-architecture`** - CRITICAL: Package hierarchy, dependency rules, Model B distribution
- `registry-system` - Data-only registry patterns
- `scope-enforcement` - Path-level scope validation
- `service-layer` - Service patterns in Core
- `plugins` - Plugin development patterns
