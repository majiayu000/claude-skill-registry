---
name: one-ui-migration
description: Migrating Angular 16 to 20 with DDD architecture and SignalStore patterns. Use when converting components, structuring features, or following One-UI migration standards.
license: MIT
compatibility: Requires Angular 20+ project with @ngrx/signals, @one-ui/shared dependencies
allowed-tools: Read, Bash, Edit, Write, Glob, Grep
---

# One-UI Migration Skill

> **Core Principle**: MIGRATE, DON'T INNOVATE — 100% behavior parity with Legacy

## Task Router

### What tool do I need?

| I need to... | Check this |
|--------------|------------|
| **Add form validation** | `rules/tools/one-validators.md` |
| **Create a form** | `rules/tools/form-builder.md` |
| **Manage state (Store)** | `rules/tools/signal-store.md` |
| **Handle loading states** | `rules/tools/loading-states.md` |
| **Create a table** | `rules/tools/common-table.md` |
| **Create a dialog** | `rules/tools/dialog.md` |
| **Use MX components** | `rules/tools/mx-components.md` |
| **Page structure** | `rules/tools/page-layout.md` |
| **Configure routes** | `rules/tools/routing.md` |
| **Translate text** | `rules/tools/transloco.md` |
| **Handle authentication** | `rules/tools/auth.md` |

### What do I need to build?

| I need to... | Check this guide |
|--------------|------------------|
| **Create a complete page** | `rules/guides/create-page.md` |
| **Create a dialog** | `rules/guides/create-dialog.md` |
| **Create a table** | `rules/guides/create-table.md` |

### Reference

| I need to... | Check this |
|--------------|------------|
| **DDD layer rules** | `rules/reference/ddd-architecture.md` |
| **Angular 20 syntax transforms** | `rules/reference/angular-20-syntax.md` |
| **Pre-PR checklist** | `rules/reference/checklist.md` |

---

## Quick Reference

### Essential Transforms

| Angular 16 | Angular 20 |
|------------|------------|
| `*ngIf="x"` | `@if (x) { }` |
| `*ngFor="let i of items"` | `@for (i of items; track i.id) { }` |
| `constructor(private x)` | `inject()` |
| `@Input()` | `input()` / `input.required()` |
| `@Output()` | `output()` |
| `BehaviorSubject` | `signal()` |
| `get x()` | `computed()` |
| `Validators` | `OneValidators` |

### DDD 4-Layer Quick Decision

```
HTTP/Business logic?  → domain/
Injects Store?        → features/
Pure I/O?             → ui/
Route definitions?    → shell/
```

### Forbidden Patterns

```
❌ Add features not in Legacy
❌ "Improve" Legacy behavior
❌ Create new API endpoints
❌ Use `any` type
❌ Use BehaviorSubject
❌ Use constructor injection
❌ Use mat-raised-button (use mat-flat-button)
❌ Use text icons (use svgIcon="icon:xxx")
❌ Add padding to page components
❌ Create new translation keys
```

---

## Activation Triggers

- "migrate this component"
- "convert to standalone"
- "how should I structure this"
- "where should this go"
- "what's the pattern for"
- "check migration rules"

---

## Rules Directory Structure

```
rules/
├── index.md                    # Router entry
├── tools/                      # Tool reference (11 files)
│   ├── one-validators.md
│   ├── form-builder.md
│   ├── signal-store.md
│   ├── loading-states.md
│   ├── common-table.md
│   ├── dialog.md
│   ├── mx-components.md
│   ├── page-layout.md
│   ├── routing.md
│   ├── transloco.md
│   └── auth.md
├── guides/                     # Integration guides (3 files)
│   ├── create-page.md
│   ├── create-dialog.md
│   └── create-table.md
└── reference/                  # Reference (3 files)
    ├── ddd-architecture.md
    ├── angular-20-syntax.md
    └── checklist.md
```

---

## Migration Planning

For complex migrations, use **migration-planning** skill:

```
/one-ui-migration:plan {feature-name}
```

This integrates `superpowers:brainstorming` and `superpowers:writing-plans` with tool reference checklists.

See: `skills/migration-planning/SKILL.md`

---

## Post-Migration Validation

Use **one-ui-migration-checker** agent:

```
"check migration for libs/mxsecurity/{feature}"
```
