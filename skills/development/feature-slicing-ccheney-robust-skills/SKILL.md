---
name: feature-slicing
description: Apply Feature-Sliced Design (FSD) architecture to frontend projects. Use when creating new frontend features, components, pages, or restructuring existing code. Triggers on tasks involving React/Next.js/Vue project organization, layer architecture, feature isolation, module boundaries, or when user mentions FSD, feature slicing, or scalable frontend structure.
---

# Feature-Sliced Design Architecture

## Overview

Feature-Sliced Design (FSD) is an architectural methodology for scaffolding frontend applications with rules and conventions for organizing code to remain understandable and stable amid changing business requirements.

**Official Documentation:** https://feature-sliced.design/llms.txt

## Core Principles

1. **Layers** - 7 standardized horizontal levels (top to bottom):
   - `app/` → routing, entrypoints, global styles, providers
   - `processes/` → (deprecated) complex cross-page scenarios
   - `pages/` → full pages or nested routing sections
   - `widgets/` → self-contained UI blocks delivering complete use cases
   - `features/` → reused product functionality with business value
   - `entities/` → business domain objects (user, product, order)
   - `shared/` → reusable, project-detached functionality

2. **Import Rule** - Modules can only import from layers strictly below them. Never import sideways or upward.

3. **Slices** - Business-domain partitions within layers (e.g., `user`, `product`, `cart`). Cannot reference other slices at the same layer.

4. **Segments** - Purpose-based groupings within slices:
   - `ui/` → components, formatters, styles
   - `api/` → backend interactions, data types
   - `model/` → schemas, stores, business logic
   - `lib/` → slice-specific utilities
   - `config/` → feature flags, configuration

5. **Public API** - Each slice exposes functionality via `index.ts` barrel file.

## Quick Reference Structure

```
src/
├── app/              # Layer: Application initialization
│   ├── providers/    # Context providers, store setup
│   ├── routes/       # Router configuration
│   └── styles/       # Global styles
├── pages/            # Layer: Route-based screens
│   └── {page-name}/
│       ├── ui/
│       ├── api/
│       └── index.ts  # Public API
├── widgets/          # Layer: Complex reusable blocks
│   └── {widget-name}/
│       ├── ui/
│       └── index.ts
├── features/         # Layer: User interactions
│   └── {feature-name}/
│       ├── ui/
│       ├── api/
│       ├── model/
│       └── index.ts
├── entities/         # Layer: Business entities
│   └── {entity-name}/
│       ├── ui/
│       ├── api/
│       ├── model/
│       └── index.ts
└── shared/           # Layer: Shared infrastructure
    ├── ui/           # UI kit, design system
    ├── api/          # API client, request functions
    ├── lib/          # Utilities (dates, validation)
    ├── config/       # Environment, constants
    └── i18n/         # Internationalization
```

## When Implementing FSD

1. **Creating a new feature**: Place in `features/` if reused across pages, otherwise keep in `pages/`
2. **Creating a new entity**: Place in `entities/` with `ui/`, `api/`, `model/` segments
3. **Creating shared utilities**: Place in `shared/lib/` or `shared/ui/`
4. **Integrating with Next.js**: Place App Router in `src/app/` (no root `app/`), which serves as both routing and FSD app layer

## Reference Documentation

For detailed implementation guidance, consult these reference files:

- **[Layer Details](references/LAYERS.md)** - Complete layer specifications and guidelines
- **[Public API Patterns](references/PUBLIC-API.md)** - Export patterns, barrel files, cross-imports
- **[Implementation Patterns](references/IMPLEMENTATION.md)** - Code examples, entity/feature patterns
- **[Next.js Integration](references/NEXTJS.md)** - App Router and Pages Router setup
- **[Migration Guide](references/MIGRATION.md)** - Migrating existing projects to FSD
- **[Cheatsheet](references/CHEATSHEET.md)** - Quick decision guide and common patterns

## Key Anti-Patterns to Avoid

- Importing from higher layers (breaks unidirectional flow)
- Cross-slice imports at the same layer (use lower layers instead)
- Generic segment names like `components/`, `hooks/`, `types/`
- Wildcard exports (`export * from`) in public APIs
- Storing business logic in `shared/` layer
