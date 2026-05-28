---
name: react-package-builder
description: |
  Create reusable React component packages for the Raamattu Nyt monorepo. Use when:
  (1) Extracting a component from an app into a shared package
  (2) Creating a new reusable UI component library
  (3) Designing props contracts for controlled/uncontrolled components
  (4) Implementing engine abstraction patterns (GSAP, framer-motion)
  (5) Decoupling components from Supabase/Auth/fetching
  Triggers: "create package", "extract component", "make reusable", "shared component", "props contract", "engine abstraction"
---

# React Package Builder

Create decoupled, reusable React packages for the monorepo.

## Workflow

1. **Audit** existing component for app-specific dependencies
2. **Design** props contract (see [props-patterns.md](references/props-patterns.md))
3. **Scaffold** package structure (see [package-structure.md](references/package-structure.md))
4. **Verify** decoupling (see [decoupling-checklist.md](references/decoupling-checklist.md))
5. **Create** adapter in consuming app

## Quick Start

```bash
# Create package directory
mkdir -p packages/<package-name>/src/{ui,hooks,engine,styles}

# Create package.json
cat > packages/<package-name>/package.json << 'EOF'
{
  "name": "@raamattu-nyt/<package-name>",
  "version": "1.0.0",
  "main": "src/index.ts",
  "peerDependencies": { "react": ">=18" }
}
EOF
```

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| No fetching | Data via props, callbacks for mutations |
| No Supabase | Parent adapter handles DB |
| No Auth | Parent provides auth context if needed |
| No persistence | Parent saves progress/preferences |
| Signals only | Emit callbacks, don't execute side effects |

## Props Contract Template

```typescript
interface ComponentProps {
  // ---- Content ----
  title: string;
  items: Item[];

  // ---- Index (controlled/uncontrolled) ----
  currentIndex?: number;
  defaultIndex?: number;
  onIndexChange?: (index: number, meta: { source: string }) => void;

  // ---- Signals (parent handles audio/media) ----
  onToggleAudio?: (enabled: boolean) => void;
  onVolumeChange?: (volume: number) => void;

  // ---- Lifecycle ----
  onExit?: () => void;
}
```

## References

- **[package-structure.md](references/package-structure.md)** — Directory layout, naming conventions
- **[props-patterns.md](references/props-patterns.md)** — Controlled/uncontrolled, engine abstraction
- **[decoupling-checklist.md](references/decoupling-checklist.md)** — Verify no app dependencies
