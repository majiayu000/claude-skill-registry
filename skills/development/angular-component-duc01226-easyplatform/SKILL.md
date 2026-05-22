---
name: angular-component
description: Use when creating or modifying Angular components in WebV2 (Angular 19) with proper base class inheritance, state management, and platform patterns.
---

# Angular Component Development

## Required Reading

**For comprehensive TypeScript/Angular patterns, you MUST read:**

- **`docs/claude/frontend-typescript-complete-guide.md`** - Complete patterns for components, stores, forms, API services
- **`docs/claude/scss-styling-guide.md`** - SCSS patterns, mixins, BEM conventions

---

## 🎨 Design System Documentation (MANDATORY)

**Before creating any component, read the design system documentation for your target application:**

| Application                       | Design System Location                           |
| --------------------------------- | ------------------------------------------------ |
| **WebV2 Apps**                    | `docs/design-system/`                            |
| **TextSnippetClient**             | `src/PlatformExampleAppWeb/apps/playground-text-snippet/docs/design-system/` |

**Key docs to read:**

- `README.md` - Component overview, base classes, library summary
- `02-component-catalog.md` - Available components and usage examples
- `01-design-tokens.md` - Colors, typography, spacing tokens
- `07-technical-guide.md` - Implementation checklist

## Component Hierarchy

```
PlatformComponent                    # Base: lifecycle, subscriptions, signals
├── PlatformVmComponent             # + ViewModel injection
├── PlatformFormComponent           # + Reactive forms integration
└── PlatformVmStoreComponent        # + ComponentStore state management

AppBaseComponent                     # + Auth, roles, company context
├── AppBaseVmComponent              # + ViewModel + auth context
├── AppBaseFormComponent            # + Forms + auth + validation
└── AppBaseVmStoreComponent         # + Store + auth + loading/error
```

## Component Type Decision

| Scenario             | Base Class                | Use When                      |
| -------------------- | ------------------------- | ----------------------------- |
| Simple display       | `AppBaseComponent`        | Static content, no state      |
| With ViewModel       | `AppBaseVmComponent`      | Needs mutable view model      |
| Form with validation | `AppBaseFormComponent`    | User input forms              |
| Complex state/CRUD   | `AppBaseVmStoreComponent` | Lists, dashboards, multi-step |

## File Location

```
src/PlatformExampleAppWeb/apps/{app-name}/src/app/
└── features/{feature}/
    ├── {feature}.component.ts
    ├── {feature}.component.html
    ├── {feature}.component.scss
    └── {feature}.store.ts (if using store)
```

## Component HTML Template Standard (BEM Classes)

**All UI elements in component templates MUST have BEM classes, even without styling needs.** This makes HTML self-documenting like OOP class hierarchy.

```html
<!-- ✅ CORRECT: All elements have BEM classes for structure clarity -->
<div class="feature-card">
    <div class="feature-card__header">
        <h3 class="feature-card__title">{{ feature.name }}</h3>
        <span class="feature-card__badge">{{ feature.status }}</span>
    </div>
    <div class="feature-card__body">
        <p class="feature-card__description">{{ feature.description }}</p>
    </div>
    <div class="feature-card__footer">
        <button class="feature-card__btn --edit" (click)="onEdit.emit(feature)">Edit</button>
        <button class="feature-card__btn --delete" (click)="onDelete.emit(feature)">Delete</button>
    </div>
</div>

<!-- ❌ WRONG: Elements without classes - structure unclear -->
<div class="feature-card">
    <div>
        <h3>{{ feature.name }}</h3>
        <span>{{ feature.status }}</span>
    </div>
    <div>
        <p>{{ feature.description }}</p>
    </div>
    <div>
        <button (click)="onEdit.emit(feature)">Edit</button>
        <button (click)="onDelete.emit(feature)">Delete</button>
    </div>
</div>
```

**BEM Naming Convention:**

- **Block**: Component name (e.g., `feature-card`)
- **Element**: Child using `block__element` (e.g., `feature-card__header`)
- **Modifier**: Separate class with `--` prefix (e.g., `feature-card__btn --edit --small`)

## Component SCSS Standard

Always style both the **host element** (Angular selector) and the **main wrapper class**:

```scss
@import '~assets/scss/variables';

// Host element styling - ensures Angular element is a proper block container
my-component {
    display: flex;
    flex-direction: column;
}

// Main wrapper class with full styling
.my-component {
    display: flex;
    flex-direction: column;
    width: 100%;
    flex-grow: 1;

    &__header {
        // BEM child elements...
    }

    &__content {
        flex: 1;
        overflow-y: auto;
    }
}
```

**Why both?**

- **Host element**: Makes the Angular element a real layout element (not an unknown element without display)
- **Main class**: Contains the full styling, matches the wrapper div in HTML

## Pattern 1: List Component with Store

### Store

```typescript
@Injectable()
export class FeatureListStore extends PlatformVmStore<FeatureListState> {
    protected override vmConstructor = (data?: Partial<FeatureListState>) => ({ items: [], filters: {}, ...data }) as FeatureListState;

    public readonly items$ = this.select(state => state.items);

    public loadItems = this.effectSimple(
        () => this.featureApi.getList(this.currentVm().filters).pipe(this.tapResponse(items => this.updateState({ items }))),
        'loadItems'
    );

    constructor(private featureApi: FeatureApiService) {
        super();
    }
}
```

### Component

```typescript
@Component({
    selector: 'app-feature-list',
    providers: [FeatureListStore]
})
export class FeatureListComponent extends AppBaseVmStoreComponent<FeatureListState, FeatureListStore> {
    trackByItem = this.ngForTrackByItemProp<FeatureDto>('id');

    constructor(store: FeatureListStore) {
        super(store);
    }

    ngOnInit(): void {
        this.store.loadItems();
    }
}
```

### Template

```html
<app-loading-and-error-indicator [target]="this">
    @if (vm(); as vm) { @for (item of vm.items; track trackByItem) {
    <div>{{ item.name }}</div>
    } @empty {
    <div>No items found</div>
    } }
</app-loading-and-error-indicator>
```

## Pattern 2: Form Component

```typescript
@Component({
    selector: 'app-feature-form'
})
export class FeatureFormComponent extends AppBaseFormComponent<FeatureFormVm> {
    protected initialFormConfig = () => ({
        controls: {
            name: new FormControl(this.currentVm().name, [Validators.required, noWhitespaceValidator]),
            code: new FormControl(this.currentVm().code, [], [ifAsyncValidator(() => !this.isViewMode(), this.checkCodeUnique())])
        },
        dependentValidations: { code: ['status'] }
    });

    protected initOrReloadVm = (isReload: boolean) => {
        return this.mode === 'create' ? of<FeatureFormVm>({ name: '', code: '' }) : this.featureApi.getById(this.featureId);
    };

    onSubmit(): void {
        if (!this.validateForm()) return;
        this.featureApi.save(this.currentVm()).pipe(this.observerLoadingErrorState('save'), this.untilDestroyed()).subscribe();
    }
}
```

## Key Platform APIs

```typescript
// Auto-cleanup subscription
this.data$.pipe(this.untilDestroyed()).subscribe();

// Track request state
observable.pipe(this.observerLoadingErrorState('requestKey'));

// Check states
isLoading$('requestKey')();
getErrorMsg$('requestKey')();

// Track-by for @for loops
trackByItem = this.ngForTrackByItemProp<Item>('id');
```

## Code Responsibility Hierarchy (CRITICAL)

**Components should only handle UI events - delegate all logic to lower layers:**

| Layer            | Responsibility                                                      |
| ---------------- | ------------------------------------------------------------------- |
| **Entity/Model** | Display helpers, dropdown options, defaults, static factory methods |
| **Service**      | API calls, command factories                                        |
| **Component**    | UI event handling ONLY                                              |

```typescript
// ❌ WRONG: Logic in component (causes duplication)
readonly statusOptions = [{ value: 1, label: 'Active' }, ...];
getStatusClass(item) { return item.isActive ? 'active' : 'inactive'; }

// ✅ CORRECT: Delegate to entity
readonly statusOptions = Entity.getStatusOptions();
getStatusClass(item) { return item.getStatusCssClass(); }
```

## Anti-Patterns to AVOID

- Using wrong base class (PlatformComponent when auth needed)
- Manual subscription management without untilDestroyed()
- Direct HttpClient usage (use API services)
- Missing loading states (use app-loading-and-error-indicator)
- Putting reusable logic in component instead of entity/model
