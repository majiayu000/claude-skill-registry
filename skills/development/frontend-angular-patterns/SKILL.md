---
name: frontend-angular-patterns
description: Use when editing Angular TypeScript files (.ts, .tsx) in src/Frontend/ or libs/. Provides component hierarchy, state management with PlatformVmStore, API services, reactive forms, and platform utilities for EasyPlatform Angular 19 development.
---

# Frontend Angular Code Patterns

When implementing frontend Angular code in EasyPlatform, follow these patterns exactly.

## Full Pattern Reference

See the complete code patterns with examples: [frontend-code-patterns.md](.ai/docs/frontend-code-patterns.md)

## Quick Reference

### Pattern Index

| #   | Pattern             | Key Interface/Contract                                                                 |
| --- | ------------------- | -------------------------------------------------------------------------------------- |
| 1   | Component Hierarchy | `PlatformComponent → AppBaseComponent → Feature` (never extend Platform* directly)     |
| 2   | Component API       | `observerLoadingErrorState()`, `untilDestroyed()`, `tapResponse()`, `isLoading$()`     |
| 3   | State Store         | `PlatformVmStore<T>`, `effectSimple()`, `updateState()`, `select()`                    |
| 4   | API Service         | Extend `PlatformApiService`, `get apiUrl`, typed CRUD methods                          |
| 5   | Forms               | `PlatformFormComponent`, `initialFormConfig()`, `validateForm()`, FormArray support    |
| 6   | Advanced            | `@Watch`, `skipDuplicates()`, `distinctUntilObjectValuesChanged()`, platform utilities |

## Critical Rules

1. **Component Hierarchy:** Extend `AppBaseComponent`, `AppBaseVmStoreComponent`, or `AppBaseFormComponent` - NEVER raw `Component`
2. **State Management:** Use `PlatformVmStore` for state management - NEVER manual signals
3. **API Services:** Extend `PlatformApiService` for HTTP calls - NEVER direct `HttpClient`
4. **Subscriptions:** Always use `.pipe(this.untilDestroyed())` for subscriptions - NEVER manual unsubscribe
5. **BEM Classes:** All template elements MUST have BEM classes (`block__element --modifier`)
6. **API Calls:** Use `effectSimple()` for API calls - auto-handles loading/error state

## Component Hierarchy

```typescript
PlatformComponent → PlatformVmComponent → PlatformFormComponent
                  → PlatformVmStoreComponent

AppBaseComponent → AppBaseVmComponent → AppBaseFormComponent
                 → AppBaseVmStoreComponent

FeatureComponent extends AppBaseVmStoreComponent<State, Store>
```

## Platform Component API

```typescript
// PlatformComponent
status$: WritableSignal<'Pending'|'Loading'|'Success'|'Error'>;
observerLoadingErrorState<T>(key?: string): OperatorFunction<T, T>;
isLoading$(key?: string): Signal<boolean | null>;
untilDestroyed<T>(): MonoTypeOperatorFunction<T>;
tapResponse<T>(next?, error?, complete?): OperatorFunction<T, T>;

// PlatformVmStoreComponent
constructor(public store: TStore) {}
vm: Signal<T | undefined>;
reload(): void;

// PlatformFormComponent
form: FormGroup<PlatformFormGroupControls<T>>;
mode: 'create'|'update'|'view';
validateForm(): boolean;
abstract initialFormConfig: () => PlatformFormConfig<T>;
```

## Anti-Patterns

```typescript
// ❌ Direct HttpClient → ✅ Extend PlatformApiService
// ❌ Manual signals → ✅ Use PlatformVmStore
// ❌ Missing untilDestroyed() → ✅ Always use .pipe(this.untilDestroyed())
// ❌ No BEM classes → ✅ Every element needs BEM class
```

## Templates

### Component with Store Template

```typescript
@Component({
    selector: 'app-{entity}-list',
    template: `
        <app-loading [target]="this">
            @if (vm(); as vm) {
                @for (item of vm.items; track item.id) {
                    <div class="{entity}-list__item">{{item.name}}</div>
                }
            }
        </app-loading>
    `,
    providers: [{Entity}Store]
})
export class {Entity}Component extends AppBaseVmStoreComponent<{Entity}State, {Entity}Store> {
    ngOnInit() {
        this.store.load();
    }
}
```

### API Service Template

```typescript
@Injectable({ providedIn: 'root' })
export class {Entity}ApiService extends PlatformApiService {
    protected get apiUrl() {
        return environment.apiUrl + '/api/{Entity}';
    }

    getAll(query?: Query): Observable<{Entity}[]> {
        return this.get('', query);
    }

    save(cmd: SaveCommand): Observable<Result> {
        return this.post('', cmd);
    }
}
```

## Detailed Instructions

For task-specific guidance, also reference:

- [frontend-angular.instructions.md](instructions/frontend-angular.instructions.md) - Angular patterns
- [scss-styling.instructions.md](instructions/scss-styling.instructions.md) - SCSS/BEM styling
