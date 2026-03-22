---
name: create-theme
description: |
  Guide for creating new themes from preset template.
  CRITICAL: Includes MANDATORY dependency management rules for NPM distribution.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
version: "2.0"
---

# Create Theme Skill

Complete guide for scaffolding and configuring new themes from the preset template.

---

## ⚠️ MANDATORY: Dependency Management Rules

### Principio Fundamental

> **Si `@nextsparkjs/core` tiene una dependencia, los themes DEBEN declararla como `peerDependency`, NUNCA como `dependency`.**

### Template OBLIGATORIO de package.json para Themes

```json
{
  "name": "@nextsparkjs/theme-NOMBRE",
  "version": "1.0.0",
  "private": false,
  "main": "./config/theme.config.ts",
  "dependencies": {
    // Plugins que el theme requiere
    "@nextsparkjs/plugin-langchain": "workspace:*"
  },
  "peerDependencies": {
    "@nextsparkjs/core": "workspace:*",
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "zod": "^4.0.0"
    // Agregar otras de core que el theme use directamente
  }
}
```

### Import Rules

| Package | Can Import From |
|---------|-----------------|
| Theme | Core (peer), plugins (dep/peer), itself (never other themes) |

---

## Prerequisites

- **Command:** `pnpm create:theme <theme-name>`
- **Preset Location:** `core/templates/contents/themes/starter/`
- **Output Location:** `themes/<theme-name>/`

---

## Step 1: Gather Requirements

Before creating ANY theme, collect:

```markdown
Required Information:
1. Theme name (lowercase, hyphenated slug)
2. Display name (human-readable)
3. Description (purpose of the theme)
4. Author (team or individual)
5. Primary use case (SaaS type, industry, features)
6. Color preferences (optional - can use defaults)
```

---

## Step 2: Create Theme from Preset

### Basic Usage

```bash
pnpm create:theme <theme-name>
```

### With Options

```bash
pnpm create:theme <theme-name> \
  --description "Theme description" \
  --author "Author Name" \
  --display-name "Display Name"
```

### Example

```bash
pnpm create:theme project-manager \
  --description "Project management SaaS application" \
  --author "Development Team" \
  --display-name "Project Manager"
```

---

## Step 3: Theme Structure Created

```
contents/themes/<theme-name>/
├── config/
│   ├── theme.config.ts         # Visual configuration
│   ├── app.config.ts           # Application overrides
│   ├── dashboard.config.ts     # Dashboard settings
│   └── permissions.config.ts   # Permission overrides
├── about.md                    # Theme description
├── styles/
│   ├── globals.css             # CSS variables
│   └── components.css          # Component overrides
├── messages/
│   ├── en.json                 # English translations
│   └── es.json                 # Spanish translations
├── migrations/
│   ├── README.md               # Migration docs
│   └── 001_example_schema.sql
├── docs/01-overview/
│   ├── 01-introduction.md
│   └── 02-customization.md
├── blocks/hero/                # Example hero block
├── entities/                   # Data entities (optional)
│   └── [entity]/               # Each entity has 4 required files
│       ├── [entity].config.ts
│       ├── [entity].fields.ts
│       ├── [entity].types.ts
│       ├── [entity].service.ts
│       └── messages/
├── templates/                  # Page overrides
├── public/brand/               # Brand assets
└── tests/                      # Theme tests
```

---

## Step 4: Customize Configuration

### 4.1 theme.config.ts - Visual Identity

```typescript
colors: {
  light: {
    // Blue for corporate/professional
    primary: 'oklch(0.55 0.2 250)',
    // Green for productivity/growth
    // primary: 'oklch(0.55 0.2 150)',
    // Orange for creative/energy
    // primary: 'oklch(0.65 0.2 50)',
    // Purple for premium/luxury
    // primary: 'oklch(0.55 0.2 300)',
  }
}

// Enable required plugins
plugins: [
  // 'plugin-analytics',
  // 'plugin-payments',
]
```

### Color Presets by Use Case

| Use Case | Color | OKLCH Value |
|----------|-------|-------------|
| Corporate/Professional | Blue | `oklch(0.55 0.2 250)` |
| Productivity/Growth | Green | `oklch(0.55 0.2 150)` |
| Creative/Energy | Orange | `oklch(0.65 0.2 50)` |
| Premium/Luxury | Purple | `oklch(0.55 0.2 300)` |
| Healthcare/Trust | Teal | `oklch(0.55 0.15 200)` |
| Finance/Stability | Navy | `oklch(0.45 0.15 260)` |
| E-commerce/Action | Red | `oklch(0.55 0.2 25)` |

### 4.2 app.config.ts - Application Behavior

```typescript
// Multi-tenant SaaS
teams: {
  allowCreation: true,
  maxTeamsPerUser: 5,
}

// Single-tenant Application
teams: {
  allowCreation: false,
  maxTeamsPerUser: 1,
}

// Features
features: {
  enableDocs: true,   // Documentation site
  enableBlog: false,  // Blog functionality
}
```

### 4.3 dashboard.config.ts - Admin Interface

```typescript
topbar: {
  showSearch: true,
  showNotifications: true,
  showMessages: false,
}

sidebar: {
  defaultCollapsed: false,
  showEntityCounts: true,
}

entities: {
  defaultPageSize: 25,
  enableBulkActions: true,
}
```

---

## Step 5: Verify Theme Setup

```bash
# 1. Verify theme structure
ls -la contents/themes/<theme-name>/

# 2. Build registry to include new theme
node core/scripts/build/registry.mjs

# 3. Verify theme appears in registry
grep "<theme-name>" core/lib/registries/theme-registry.ts

# 4. Test theme activation (optional)
# Update .env.local: NEXT_PUBLIC_ACTIVE_THEME='<theme-name>'
# Run: pnpm dev
```

---

## Step 6: Entity Structure (4-File Pattern)

Each theme entity requires 4 files:

| File | Purpose |
|------|---------|
| `[entity].config.ts` | Entity configuration |
| `[entity].fields.ts` | Field definitions |
| `[entity].types.ts` | TypeScript types |
| `[entity].service.ts` | Data access service |

**Reference:** `core/templates/contents/themes/starter/entities/tasks/`

---

## Verification Checklist

### Antes de crear un theme (OBLIGATORIO):

- [ ] Verificar si las dependencias que necesito ya están en core
- [ ] Si están en core → declararlas como `peerDependencies`
- [ ] Si NO están en core → declararlas como `dependencies`
- [ ] Plugins como `dependencies` (workspace:*)
- [ ] NUNCA duplicar: zod, react, next, @tanstack/*, lucide-react, etc.
- [ ] NUNCA importar de otros themes

### Después de crear el theme:

- [ ] Theme name follows naming conventions (lowercase, hyphenated)
- [ ] All preset files created successfully
- [ ] `package.json` created with correct peerDependencies
- [ ] theme.config.ts customized with appropriate colors
- [ ] app.config.ts configured for use case
- [ ] dashboard.config.ts settings appropriate
- [ ] permissions.config.ts reviewed
- [ ] messages/ translations have correct theme name
- [ ] Registry rebuilt: `node core/scripts/build/registry.mjs`
- [ ] Theme appears in THEME_REGISTRY
- [ ] No TypeScript errors

### Validación de Dependencias:

```bash
# Verificar que no hay duplicados
pnpm ls zod
# Debe mostrar UNA sola versión
```

---

## Anti-Patterns

| Pattern | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Manual file creation | Missing files, wrong structure | Use `pnpm create:theme` |
| Skipping registry rebuild | Theme won't be recognized | Always run `node core/scripts/build/registry.mjs` |
| Modifying core files | Architecture violation | Only work in `contents/themes/` |
| Implementing features | Scope creep | Hand off to backend/frontend agents |

---

## Handoff Template

After creating theme, document:

```markdown
## Theme Created: <theme-name>

### Completed Setup:
- Theme scaffolded from preset
- Visual identity configured (primary color: X)
- Application settings configured
- Dashboard layout configured

### Ready for Development:
- Backend: Add custom entities, migrations, API endpoints
- Frontend: Customize UI components, add blocks

### Environment Setup:
NEXT_PUBLIC_ACTIVE_THEME='<theme-name>'
```

---

## Related Documentation

- **`monorepo-architecture` skill** - CRITICAL: Package hierarchy and dependency management rules
- Entity System: `core/docs/04-entities/`
- Theme Config: `core/docs/02-themes/`
- Registry System: `core/docs/03-registry-system/`
