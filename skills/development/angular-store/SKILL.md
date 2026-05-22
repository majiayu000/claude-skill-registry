---
name: angular-store
description: Use when implementing state management with PlatformVmStore for complex components requiring reactive state, effects, and selectors.
---

# Angular Store Development

## Required Reading

**For comprehensive TypeScript/Angular patterns, you MUST read:**

- **`docs/claude/frontend-typescript-complete-guide.md`** - Complete patterns for stores, effects, selectors, API services
- **`docs/claude/scss-styling-guide.md`** - SCSS patterns, mixins, BEM conventions

---

## 🎨 Design System Documentation (MANDATORY)

**Before creating any store, read the design system documentation for your target application:**

| Application                       | Design System Location                           |
| --------------------------------- | ------------------------------------------------ |
| **WebV2 Apps**                    | `docs/design-system/`                            |
| **TextSnippetClient**             | `src/PlatformExampleAppWeb/apps/playground-text-snippet/docs/design-system/` |

**Key docs to read:**

- `README.md` - Component overview, base classes, library summary
- `06-state-management.md` - State management patterns (NgRx, PlatformVmStore)
- `07-technical-guide.md` - Implementation checklist, best practices

## Component Hierarchy

| Base Class                 | Use Case                        |
| -------------------------- | ------------------------------- |
| `PlatformVmStoreComponent` | Basic store without auth        |
| `AppBaseVmStoreComponent`  | Store with auth, roles, company |

## Store Pattern

```typescript
// Store definition
@Injectable()
export class EmployeeListStore extends PlatformVmStore<EmployeeListVm> {
    constructor(private employeeApi: EmployeeApiService) {
        super();
    }

    // Optional: Enable caching
    protected get enableCaching() {
        return true;
    }
    protected cachedStateKeyName = () => 'EmployeeListStore';

    // ViewModel constructor
    protected vmConstructor = (data?: Partial<EmployeeListVm>) => new EmployeeListVm(data);

    // Effects
    public loadEmployees = this.effectSimple(
        () => this.employeeApi.getEmployees().pipe(this.tapResponse(employees => this.updateState({ employees }))),
        'loadEmployees'
    );

    public deleteEmployee = this.effectSimple(
        (id: string) =>
            this.employeeApi.delete(id).pipe(
                this.tapResponse(() =>
                    this.updateState(state => ({
                        employees: state.employees.filter(e => e.id !== id)
                    }))
                )
            ),
        'deleteEmployee'
    );

    // Selectors
    public readonly employees$ = this.select(state => state.employees);
    public readonly activeCount$ = this.select(state => state.employees.filter(e => e.isActive).length);
    public readonly isLoading$ = this.isLoading$('loadEmployees');
}
```

## Component Usage

```typescript
@Component({
    selector: 'app-employee-list',
    template: `
        <app-loading-and-error-indicator [target]="this">
            @if (vm(); as vm) {
                @for (emp of vm.employees; track emp.id) {
                    <div>{{ emp.name }}</div>
                }
            }
        </app-loading-and-error-indicator>
    `,
    providers: [EmployeeListStore]
})
export class EmployeeListComponent extends AppBaseVmStoreComponent<EmployeeListVm, EmployeeListStore> {
    constructor(store: EmployeeListStore) {
        super(store);
    }

    ngOnInit() {
        this.store.loadEmployees();
    }

    onRefresh() {
        this.reload(); // Reloads all store effects
    }

    onDelete(id: string) {
        this.store.deleteEmployee(id);
    }
}
```

## Key APIs

| Store Method                     | Purpose                       |
| -------------------------------- | ----------------------------- |
| `effectSimple(fn)`               | Create side effect            |
| `updateState(partial)`           | Update store state            |
| `select(selector)`               | Create selector               |
| `observerLoadingErrorState(key)` | Track loading/error state     |
| `tapResponse(next, error?)`      | Handle response               |
| `isLoading$(key)`                | Get loading signal for effect |

| Component Method    | Purpose                       |
| ------------------- | ----------------------------- |
| `vm()`              | Get current view model signal |
| `currentVm()`       | Get current view model value  |
| `updateVm(partial)` | Update view model             |
| `reload()`          | Reload all store effects      |

## ViewModel Pattern

```typescript
export class EmployeeListVm {
    employees: EmployeeDto[] = [];
    selectedId?: string;
    filters: EmployeeFilters = new EmployeeFilters();

    constructor(data?: Partial<EmployeeListVm>) {
        Object.assign(this, data);
    }
}
```

## Anti-Patterns

- Direct state mutation (use `updateState()`)
- Not providing store in component `providers`
- Manual subscription management
- Not using `observerLoadingErrorState` for API calls
