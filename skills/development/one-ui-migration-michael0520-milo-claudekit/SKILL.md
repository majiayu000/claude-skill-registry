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
| **Use shared helpers** | `rules/tools/shared-helpers.md` |
| **Manage state (Store)** | `rules/tools/signal-store.md` |
| **Handle loading states** | `rules/tools/loading-states.md` |
| **Create a table** | `rules/tools/common-table.md` |
| **Simplify table columns** | `rules/tools/tables/auto-generate.md` |
| **Create a dialog** | `rules/tools/ui/dialogs.md` |
| **Use MX components** | `rules/tools/mx-components.md` |
| **Page structure** | `rules/tools/ui/page-layout.md` |
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
| **Common migration mistakes** | `rules/reference/pitfalls.md` |
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

### Critical Migration Rules (NEW)

**Form Validation Error Display**:
```
✅ Basic validators (required, maxLength, range) → Use oneUiFormError directive
❌ Pattern validators → MUST use @if/@else with custom messages
❌ Custom validators → MUST use @if/@else with custom messages
```

**DDD Violations to Avoid** (see `rules/reference/pitfalls.md`):
```
❌ Violation 0: Page form template in features/ (MOST COMMON!)
❌ Violation 1: UI component injecting Store
❌ Violation 2: Dialog in ui/ layer
❌ Violation 3: Business logic in features/
❌ Violation 4: UI form making HTTP calls
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
├── index.md
├── tools/
│   ├── one-validators.md
│   ├── form-builder.md
│   ├── signal-store.md
│   ├── loading-states.md
│   ├── common-table.md
│   ├── mx-components.md
│   ├── routing.md
│   ├── transloco.md
│   ├── auth.md
│   ├── shared-helpers.md
│   ├── forms/
│   │   ├── validators.md
│   │   ├── error-handling.md
│   │   └── patterns.md
│   ├── tables/
│   │   ├── basics.md
│   │   ├── columns.md
│   │   ├── advanced.md
│   │   └── auto-generate.md
│   └── ui/
│       ├── page-layout.md
│       ├── forms.md
│       ├── buttons.md
│       ├── components.md
│       └── dialogs.md
├── guides/
│   ├── create-page.md
│   ├── create-dialog.md
│   └── create-table.md
└── reference/
    ├── ddd-architecture.md
    ├── angular-20-syntax.md
    ├── api-types.md
    ├── checklist.md
    ├── migration-checklist.md
    ├── migration-context.md
    ├── migration-workflow.md
    ├── shared-stores.md
    ├── state-management.md
    ├── pitfalls.md
    └── pitfalls/
        ├── index.md
        ├── angular-syntax.md
        ├── ddd-violations.md
        ├── forms-services.md
        └── translation-layout.md
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
