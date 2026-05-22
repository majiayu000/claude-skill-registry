---
name: frontend-angular-component
description: Use when creating or modifying Angular components in Frontend (Angular 19) with proper base class inheritance, state management, and platform patterns.
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular Component Development Workflow

Use when creating/modifying Angular 19 components with EasyPlatform base classes.

## Decision Tree

```
What type of component?
├── Simple display (no state)     → AppBaseComponent
├── Mutable view model            → AppBaseVmComponent
├── User input form               → AppBaseFormComponent (see frontend-angular-form skill)
├── Complex state / CRUD / list   → AppBaseVmStoreComponent (see frontend-angular-store skill)
└── Reusable presentational       → AppBaseComponent + @Input/@Output
```

**Rule:** Always use `AppBase*` (not `Platform*` directly) to get auth/role context.

## Workflow

1. **Search** existing components: `grep "{Feature}Component" --include="*.ts"`
2. **Read** design system docs (see Read Directives below)
3. **Select** base class from decision tree above
4. **Create** files: `{feature}.component.ts`, `.html`, `.scss`, optionally `.store.ts`
5. **Implement** using patterns from references
6. **Verify** checklist below

## Key Rules

- Wrap content with `<app-loading-and-error-indicator [target]="this">`
- Use `@for (item of items; track trackByItem)` with `ngForTrackByItemProp`
- All subscriptions: `.pipe(this.untilDestroyed()).subscribe()`
- Store provided at component level: `providers: [FeatureStore]`
- All API calls through `PlatformApiService` subclasses (never `HttpClient` directly)
- Place logic in LOWEST layer: Entity/Model > Service > Component

## File Location

```
src/Frontend/apps/{app-name}/src/app/features/{feature}/
├── {feature}.component.ts|html|scss
└── {feature}.store.ts (if using store)
```

## ⚠️ MUST READ Before Implementation

**IMPORTANT: You MUST read these files before writing any code. Do NOT skip.**

1. **⚠️ MUST READ** `.claude/skills/shared/angular-design-system.md` — hierarchy, SCSS, platform APIs
2. **⚠️ MUST READ** `.claude/skills/shared/bem-component-examples.md` — BEM HTML/SCSS examples
3. **⚠️ MUST READ** `.claude/skills/frontend-angular-component/references/component-patterns.md` — list, form, simple component patterns
4. **⚠️ MUST READ** target app design system: `docs/design-system/README.md` and `02-component-catalog.md`

## Anti-Patterns

- `extends PlatformComponent` when auth needed -> use `AppBaseComponent`
- `private sub: Subscription` + manual cleanup -> use `this.untilDestroyed()`
- `constructor(private http: HttpClient)` -> use `PlatformApiService` subclass
- Missing `<app-loading-and-error-indicator>` wrapper
- Template elements without BEM classes

## Verification Checklist

- [ ] Correct `AppBase*` class selected
- [ ] Store provided at component level (if using store)
- [ ] Loading/error wrapped with `app-loading-and-error-indicator`
- [ ] All subscriptions use `untilDestroyed()`
- [ ] Track-by on `@for` loops
- [ ] Auth checks use `hasRole()` from base class
- [ ] All elements have BEM classes


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
