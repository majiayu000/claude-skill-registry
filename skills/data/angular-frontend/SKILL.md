---
name: angular-frontend
description: Build and implement Angular 18 standalone components, TypeScript services
  with Signals and RxJS, routing with guards, and Tailwind CSS styling for Photo Map
  MVP. Use when creating, developing, or impl
---

---
name: angular-frontend
description: Build and implement Angular 18 standalone components, TypeScript services with Signals and RxJS, routing with guards, and Tailwind CSS styling for Photo Map MVP. Use when creating, developing, or implementing TypeScript components, services, guards, forms, HTTP calls, map integration (Leaflet.js), or responsive UI layouts with Tailwind utilities. File types: .ts, .html, .css, .scss
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular Frontend Development - Photo Map MVP

## Project Context

**Photo Map MVP** - Single Page Application (SPA) for managing photos with geolocation.

**Frontend Stack:**
- **Angular:** 18.2.0+ (standalone components, NO NgModules!)
- **TypeScript:** 5.5.2+ (strict mode)
- **Styling:** Tailwind CSS 3.4.17 (NOT v4 - Angular 18 incompatibility!)
- **Map:** Leaflet.js 1.9.4 + marker clustering
- **State:** RxJS 7.8.0 (BehaviorSubject pattern, no NgRx)
- **Build:** Angular CLI 18.2.0 (esbuild)

**Core Features:**
1. **Authentication:** Login/Register with JWT storage, route guards
2. **Gallery:** Responsive grid with lazy loading, rating, filtering
3. **Map View:** Leaflet integration with GPS markers, popups, clustering
4. **Admin Panel:** User management (ADMIN role only)

**Key Constraints:**
- **Standalone components ONLY** - NO NgModules anywhere!
- **Tailwind 3.4.17** - NOT 4.x (incompatibility with Angular 18)
- **inject() function** - NOT constructor injection (modern Angular 18)
- **Signals** - reactive state (Angular 16+)
- **BehaviorSubject** - service state management (no NgRx)

---

## Architecture Principles

### Standalone Components

ALL components MUST be standalone (`standalone: true`). Explicitly import dependencies in `imports` array. NO `@NgModule` anywhere.

Check: `references/angular-patterns.md` for complete patterns.

### State Management Strategy

**Decision Tree:**
- **Component-local state** → Use Signals (`signal()`, `computed()`, `effect()`)
- **Shared state (cross-component)** → Use BehaviorSubject in Services

**Pattern:** `private BehaviorSubject` → `public Observable` → Component subscribes

Check: `references/state-management.md` for detailed patterns.

### Dependency Injection

Use `inject()` function (modern Angular 18), NOT constructor injection. Make all injected services `readonly`.

Example: `private readonly photoService = inject(PhotoService);`

---

## When to Use What

### Signals vs BehaviorSubject

| Use Case | Solution |
|----------|----------|
| Component-local state (counters, UI flags, filters) | **Signals** |
| Computed values (derived state) | **Signals** (`computed()`) |
| Shared state (cross-component, services) | **BehaviorSubject** |
| Async operations (HTTP, timers) | **BehaviorSubject** |
| Complex RxJS pipelines | **BehaviorSubject** |

### Smart vs Dumb Components

| Type | Characteristics |
|------|-----------------|
| **Smart** (Container) | Inject services, manage state, business logic, fetch data |
| **Dumb** (Presentational) | NO service injection, @Input/@Output only, pure presentation |

Check: `references/component-patterns.md` for detailed examples.

---

## Implementation Workflows

### Creating Component

1. **Use checklist:** `templates/component-template.md`
2. **Standalone setup:**
   - `@Component({ standalone: true })`
   - Import dependencies: `CommonModule`, `RouterLink`, child components
3. **Dependency injection:** Use `inject()`, make services `readonly`
4. **State:** Signals for local state, BehaviorSubject consumption for shared state
5. **Template:** Use @if, @for (NOT *ngIf, *ngFor), add `data-testid` attributes
6. **Examples:**
   - Smart component → `examples/photo-gallery.component.ts`
   - Dumb component → `examples/photo-card.component.ts`

Check: `references/component-patterns.md` for Smart vs Dumb patterns.

### Creating Service

1. **Use checklist:** `templates/service-template.md`
2. **State management:**
   - Private: `private readonly itemsSubject = new BehaviorSubject<T>([])`
   - Public: `readonly items$ = itemsSubject.asObservable()`
3. **HTTP methods:** All return `Observable<T>` with explicit types
4. **Error handling:** Use `catchError`, log errors, transform to user-friendly messages
5. **Example:** `examples/photo.service.ts` (BehaviorSubject + HTTP)

Check: `references/service-patterns.md` for HTTP patterns and interceptors.

### Routing Setup

1. **Use checklist:** `templates/route-template.md`
2. **Configure routes:** `app.routes.ts` with flat Routes array
3. **Functional guards:** Use `CanActivateFn`, inject services with `inject()`
4. **Register:** `provideRouter(routes)` in `app.config.ts`
5. **Examples:**
   - Routes → `examples/app.routes.ts`
   - Guards → `examples/auth.guard.ts`

Check: `references/angular-patterns.md` for routing and guards.

### Patterns and Best Practices

- **TypeScript quality:** Check `references/typescript-quality.md` (readonly, const, strict mode)
- **RxJS patterns:** Check `references/rxjs-patterns.md` (operators, async pipe, error handling)
- **Tailwind CSS:** Check `references/tailwind-patterns.md` (utility-first, responsive, constraints)
- **Leaflet integration:** Check `references/leaflet-integration.md` (map setup, markers, clustering)
- **SOLID principles:** Check `references/solid-principles.md` (when complexity justifies it)
- **Testing:** Check `references/testing-patterns.md` (Jasmine + Karma, test IDs)
- **Responsive design:** Check `references/responsive-design.md` (mobile-first, touch-friendly)

---

## Key Reminders

**Critical Constraints:**
- ✅ ALWAYS `standalone: true` (NO NgModules!)
- ✅ Use `inject()` NOT constructor injection
- ✅ Tailwind 3.4.17 (NOT 4 - incompatibility!)
- ✅ `data-testid` on all interactive elements (kebab-case)
- ✅ `readonly` for services, `const` for variables
- ✅ Explicit return types (TypeScript strict)

**State Management:**
- ✅ Signals → component-local state
- ✅ BehaviorSubject → service state (shared)
- ✅ Async pipe in templates (automatic cleanup)

**Component Structure:**
- ✅ Smart components: inject services, manage state
- ✅ Dumb components: @Input/@Output only
- ✅ Use @if, @for, @switch (NOT *ngIf, *ngFor)

**Routing:**
- ✅ Functional guards (`CanActivateFn`)
- ✅ Return `true | false | UrlTree`
- ✅ Use `inject()` in guards

---

## Quick Reference

### Pattern Lookup

| Need | Check |
|------|-------|
| Angular patterns (standalone, control flow, inject) | `references/angular-patterns.md` |
| State management (Signals vs BehaviorSubject) | `references/state-management.md` |
| TypeScript quality (readonly, const, strict) | `references/typescript-quality.md` |
| RxJS patterns (operators, async pipe) | `references/rxjs-patterns.md` |
| Tailwind styling (utility-first, responsive) | `references/tailwind-patterns.md` |
| Leaflet maps (setup, markers, clustering) | `references/leaflet-integration.md` |
| Component patterns (Smart vs Dumb) | `references/component-patterns.md` |
| Service patterns (HTTP, BehaviorSubject) | `references/service-patterns.md` |
| SOLID principles | `references/solid-principles.md` |
| Testing (Jasmine, Karma) | `references/testing-patterns.md` |
| Responsive design (mobile-first, RWD) | `references/responsive-design.md` |

### Example Lookup

| Need | Check |
|------|-------|
| Smart component (with Signals + Services) | `examples/photo-gallery.component.ts` |
| Dumb component (@Input/@Output) | `examples/photo-card.component.ts` |
| Service (BehaviorSubject + HTTP) | `examples/photo.service.ts` |
| Filter service (state management) | `examples/filter.service.ts` |
| Map component (Leaflet integration) | `examples/map.component.ts` |
| Functional guards | `examples/auth.guard.ts` |
| Route configuration | `examples/app.routes.ts` |
| TypeScript interfaces | `examples/photo.interface.ts` |
| HTTP interceptors | `examples/jwt.interceptor.ts` |

### Template Lookup (Checklists)

| Need | Check |
|------|-------|
| Creating standalone component | `templates/component-template.md` |
| Creating service with state | `templates/service-template.md` |
| Routing + guards setup | `templates/route-template.md` |
| Writing tests (Jasmine + Karma) | `templates/test-template.md` |
