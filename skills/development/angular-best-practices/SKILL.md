---
name: cermont.frontend.angular-best-practices
description: Angular 21 development with modern best practices including signals, standalone components, reactive patterns, and accessibility. Use when creating Angular components, services, templates, or performing any Angular frontend development work. Covers TypeScript strict typing, signal-based state management, reactive forms, lazy loading, ng-icon setup, and Tailwind styling.
triggers:
  - Angular
  - standalone components
  - signals
  - RxJS
  - reactive forms
  - lazy loading
  - OnPush
  - accessibility
role: PRIMARY
scope: frontend
---

<!-- Cermont Project Fit -->
## Project Fit

| Attribute | Value |
|-----------|-------|
| **Applies to** | frontend |
| **Requires** | Angular, TailwindCSS, pnpm |
| **Not for this repo** | React, Next.js, Vue, Svelte |
| **Status** | ✅ PRIMARY for Angular family |

### Guardrails

**Does NOT do:**
- Install dependencies without user approval
- Modify pnpm-lock.yaml directly
- Run migrations automatically

**Safety Checklist:**
```bash
pnpm --filter @cermont/frontend lint
pnpm --filter @cermont/frontend test
pnpm --filter @cermont/frontend build
# Rollback: git restore -SW .
```
<!-- End Project Fit -->

## TypeScript

- Use strict type checking
- Prefer type inference when type is obvious
- Avoid `any`; use `unknown` when type is uncertain

## Components

- Always use standalone components (do NOT set `standalone: true` — it's the default in v20+)
- Set `changeDetection: ChangeDetectionStrategy.OnPush`
- Use `input()` and `output()` functions instead of decorators
- Use `computed()` for derived state
- Keep components small and single-responsibility
- Prefer inline templates for small components
- Use Reactive forms over Template-driven
- Use `class` bindings instead of `ngClass`
- Use `style` bindings instead of `ngStyle`
- For external templates/styles, use paths relative to the component TS file
- Do NOT use `@HostBinding`/`@HostListener` — use the `host` object in the decorator instead

## State Management with Signals

- Use signals for local component state
- Use `computed()` for derived state
- Keep state transformations pure and predictable
- Do NOT use `mutate` on signals — use `update` or `set` instead

For complex derived state patterns, see [references/signal-patterns.md](references/signal-patterns.md).

## Resources (Async Data)

Use `resource()` for async data fetching with signals:

```typescript
const userResource = resource({
  params: () => ({ id: userId() }),
  loader: ({ params, abortSignal }) => fetch(`/api/users/${params.id}`, { signal: abortSignal }),
});

const userName = computed(() => userResource.hasValue() ? userResource.value().name : undefined);
```

Key `resource` patterns:
- `params` returns `undefined` → loader doesn't run, status becomes `'idle'`
- Use `abortSignal` to cancel in-flight requests
- Check `hasValue()` before accessing `value()` to handle loading/error states
- Status values: `'idle'`, `'loading'`, `'reloading'`, `'resolved'`, `'error'`, `'local'`

## Templates

- Use native control flow: `@if`, `@for`, `@switch` (NOT `*ngIf`, `*ngFor`, `*ngSwitch`)
- Use async pipe for observables
- Keep templates simple — no complex logic
- Do NOT use arrow functions in templates (not supported)
- Do NOT assume globals like `new Date()` are available

## Services

- Single responsibility per service
- Use `providedIn: 'root'` for singletons
- Use `inject()` function instead of constructor injection

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);
}
```

## Routing

- Implement lazy loading for feature routes:

```typescript
export const routes: Routes = [
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.page').then(m => m.AdminPage),
  },
];
```

## File Naming

- Routable view components: `file-name.page.ts`, `file-name.page.html`, `file-name.page.css`
- Regular components: `file-name.component.ts`
- Services: `file-name.service.ts`

## Icons (ng-icon)

```typescript
import { NgIcon, provideIcons } from '@ng-icons/core';
import { heroSparkles, heroTrash } from '@ng-icons/heroicons/outline';

@Component({
  selector: 'app-example',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [NgIcon],
  providers: [provideIcons({ heroSparkles, heroTrash })],
  template: `<ng-icon name="heroSparkles" />`,
})
export class ExampleComponent {}
```

## Images

- Use `NgOptimizedImage` for all static images
- `NgOptimizedImage` does NOT work for inline base64 images

## Styling

- Use Tailwind 4.1 for CSS (see tailwind skill if available)
- Angular CDK is available when needed

## Accessibility

- MUST pass all AXE checks
- MUST meet WCAG AA minimums: focus management, color contrast, ARIA attributes
