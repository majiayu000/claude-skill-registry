---
name: overleaf-frontend-patterns
description: Frontend development patterns for Overleaf CE codebase. Use when adding UI components to the Overleaf editor, creating new modules in services/web/modules/, implementing React components with contexts/hooks, writing SCSS styles with theme variables, or running frontend tests in Docker. Triggers on queries about Overleaf architecture, import paths (@/features, @/shared, @modules), component structure, CSS variables, testing patterns, or Docker webpack workflow.
---

# Overleaf Frontend Development Patterns

## Quick Architecture Overview

```
overleaf/
├── services/              # Microservices
│   └── web/              # Main app (focus here)
│       ├── app/src/      # Backend (Node.js/Express)
│       │   └── Features/ # 58 domain modules
│       ├── frontend/js/  # Frontend (React/TS)
│       │   ├── features/ # 45+ UI features
│       │   └── shared/   # Reusable components
│       └── modules/      # Custom plugins (your code!)
├── libraries/            # Shared packages
└── develop/              # Docker dev environment
```

**Full architecture**: See [references/architecture.md](references/architecture.md)

## Directory Structure (services/web/)

```
services/web/
├── frontend/js/
│   ├── features/           # Feature modules (@/features)
│   ├── shared/             # Reusable components (@/shared)
│   └── infrastructure/     # Core utilities (@/infrastructure)
├── modules/                # External plugins (@modules - NO slash)
│   └── evidence-panel/     # Custom modules here
├── macros/                 # Webpack macros
└── locales/en.json         # i18n (alphabetically sorted)
```

## Import Path Aliases

```typescript
import X from '@/features/pdf-preview/...'      // Feature
import X from '@/shared/components/...'         // Shared
import X from '@/infrastructure/error-boundary' // Infrastructure
import X from '@modules/evidence-panel/...'     // Module (NO slash after @)
import getMeta from '@/utils/meta'              // Utilities
```

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Component | `kebab-case.tsx` | `pdf-logs-viewer.tsx` |
| Hook | `use-*.ts` | `use-compile-triggers.ts` |
| Context | `*-context.tsx` | `evidence-context.tsx` |
| Test | `*.test.tsx` | `evidence-panel.test.tsx` |

## Quick Reference

### Component Pattern
```typescript
import { memo } from 'react'
import { useTranslation } from 'react-i18next'
import MaterialIcon from '@/shared/components/material-icon'
import withErrorBoundary from '@/infrastructure/error-boundary'

function MyComponent({ prop }: Props) {
  const { t } = useTranslation()
  return <div className="my-component">{t('key')}</div>
}

export default memo(withErrorBoundary(MyComponent, Fallback))
```

### Context Pattern
```typescript
const MyContext = createContext<Value | undefined>(undefined)

export function useMyContext() {
  const ctx = useContext(MyContext)
  if (!ctx) throw new Error('useMyContext must be used within MyProvider')
  return ctx
}
```

### CSS Variables
```scss
color: var(--content-primary);
background: var(--bg-light-secondary);
border: 1px solid var(--border-color);
color: var(--green-50);  // Accent
```

## Development Workflow

**NEVER run npm on host machine** - Always use Docker.

```bash
# Start dev server
cd overleaf/develop && bin/dev web webpack

# Restart webpack after new files
docker compose restart webpack

# Check compilation
docker compose logs webpack --tail 20 | grep -E "compiled|error"

# Run tests
docker exec develop-web-1 sh -c \
  "cd /overleaf/services/web && npm run test:frontend -- --grep 'MyFeature'"
```

### Verification Loop (CRITICAL)

Webpack compile success ≠ Frontend working

1. **Webpack logs**: Syntax/import errors
2. **Browser F12 Console**: Runtime/React errors
3. **Visual test**: UI renders correctly

## New Editor Compatibility

```typescript
import { useIsNewEditorEnabled } from '@/features/ide-redesign/utils/new-editor-utils'
const newEditor = useIsNewEditorEnabled()
return newEditor ? <NewVariant /> : <OldVariant />
```

## i18n

Add to `locales/en.json` (alphabetically sorted):
```typescript
const { t } = useTranslation()
<span>{t('my_key')}</span>
```

## Detailed References

- **Architecture overview**: See [references/architecture.md](references/architecture.md)
- **Component patterns**: See [references/component-patterns.md](references/component-patterns.md)
- **CSS patterns**: See [references/css-patterns.md](references/css-patterns.md)
- **Testing patterns**: See [references/testing-patterns.md](references/testing-patterns.md)
