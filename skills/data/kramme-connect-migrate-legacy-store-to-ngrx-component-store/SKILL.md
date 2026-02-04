---
name: kramme:connect-migrate-legacy-store-to-ngrx-component-store
description: Use this Skill when working in the Connect monorepo and needing to migrate legacy CustomStore or FeatureStore implementations to NgRx ComponentStore.
---

# Connect - Migrate Legacy Store to NgRx ComponentStore

## Instructions

**When to use this skill:**
- You're working in the Connect monorepo (`Connect/ng-app-monolith/`)
- You need to migrate a legacy `CustomStore` or `FeatureStore` to modern NgRx ComponentStore
- You see patterns like `addApiAction().withReducer()` or `addSocketAction().withReducer()`
- The store uses centralized NgRx Store with feature state slices

**Context:** Connect's frontend is migrating from a custom store abstraction built on top of NgRx Store to standalone NgRx ComponentStore services. This provides better encapsulation, simpler testing, and eliminates the need for actions/reducers/selectors boilerplate.

### Guideline Keywords

-   **ALWAYS** — Mandatory requirement, exceptions are very rare and must be explicitly approved
-   **NEVER** — Strong prohibition, exceptions are very rare and must be explicitly approved
-   **PREFER** — Strong recommendation, exceptions allowed with justification
-   **CAN** — Optional, developer's discretion
-   **NOTE** — Context, rationale, or clarification
-   **EXAMPLE** — Illustrative example

Strictness hierarchy: ALWAYS/NEVER > PREFER > CAN > NOTE/EXAMPLE

---

### Migration Checklist

#### 1. Store Structure Transformation

-   **ALWAYS** convert the store to a standalone service class extending `ComponentStore<StateInterface>`
-   **ALWAYS** use `providedIn: 'root'` for stores that need application-wide singleton behavior
-   **ALWAYS** define state as interface/type with `readonly` properties
-   **ALWAYS** extract `initialState` to a constant; use eager initialization in the constructor
-   **ALWAYS** end class names with a `Store` suffix
-   **ALWAYS** have file names for Component Stores include `.store.ts`
-   **PREFER** flat state structures to avoid nested objects in state

**EXAMPLE - Before (Legacy):**
```typescript
export const eventStore = new FeatureStore('event')
  .addApiAction('loadEvents')
  .withReducer((state, events) => ({ ...state, events }));
```

**EXAMPLE - After (ComponentStore):**
```typescript
interface EventStoreState {
  readonly events: Event[];
  readonly isLoading: boolean;
}

const initialState: EventStoreState = {
  events: [],
  isLoading: false,
};

@Injectable({ providedIn: 'root' })
export class EventStore extends ComponentStore<EventStoreState> {
  constructor() {
    super(initialState);
  }
}
```

#### 2. State Management Patterns

-   **ALWAYS** replace `addApiAction().withReducer()` patterns with ComponentStore updaters and effects
-   **ALWAYS** replace `addSocketAction().withReducer()` with updaters that accept observables
-   **ALWAYS** wire websocket observables directly to updaters in the constructor (no manual subscriptions needed)
-   **ALWAYS** use `tapResponse` from `@ngrx/operators` (not `@ngrx/component-store`) for effect error handling
-   **NOTE**: ComponentStore handles subscriptions automatically

**EXAMPLE - Replace API Actions with Effects:**
```typescript
// Legacy: addApiAction().withReducer()
// New: ComponentStore effect
readonly loadEvents = this.effect<void>(
  pipe(
    tap(() => this.setLoading(true)),
    switchMap(() =>
      this.#api.getEvents().pipe(
        tapResponse({
          next: (events) => this.setEvents(events),
          error: (error) => this.#errorHandler.handle(error),
          finalize: () => this.setLoading(false),
        })
      )
    )
  )
);
```

**EXAMPLE - Replace Socket Actions with Updaters:**
```typescript
// Wire websocket observables directly to updaters in constructor
constructor() {
  super(initialState);

  // Subscribe to websocket actions and wire to updaters
  this.addEvent(this.#wsService.action<Event>('AddEvent'));
  this.updateEvent(this.#wsService.action<Event>('UpdateEvent'));
  this.removeEvent(this.#wsService.action<{ id: string }>('RemoveEvent'));

  // Trigger load on websocket connection
  this.loadEvents(
    this.#wsService.connectionState$.pipe(
      filter((state) => state === 'Connected'),
      map(() => undefined)
    )
  );
}
```

#### 3. Updaters (State Mutations)

-   **ALWAYS** use updaters to change state (not `setState` or `patchState`)
-   **ALWAYS** use `set` prefix for updaters that replace entire state slices
-   **ALWAYS** keep state transformations pure and predictable
-   **NOTE**: Updaters can accept `PayloadType | Observable<PayloadType>` - wire observables directly

**EXAMPLE:**
```typescript
// Updaters accept PayloadType | Observable<PayloadType>
readonly setEvents = this.updater<Event[]>((state, events) => ({
  ...state,
  events,
}));

readonly addEvent = this.updater<Event>((state, event) => ({
  ...state,
  events: [...state.events, event],
}));

readonly updateEvent = this.updater<Event>((state, updated) => ({
  ...state,
  events: state.events.map((e) => (e.id === updated.id ? updated : e)),
}));

readonly removeEvent = this.updater<{ id: string }>((state, { id }) => ({
  ...state,
  events: state.events.filter((e) => e.id !== id),
}));

readonly setLoading = this.updater<boolean>((state, isLoading) => ({
  ...state,
  isLoading,
}));
```

#### 4. Selectors (State Reads)

-   **ALWAYS** expose state via selectors, suffix static selectors with `$`
-   **ALWAYS** prefix parameterized selectors with `select`
-   **NEVER** use `ComponentStore.get()` — always read via selectors
-   **ALWAYS** do one-off reads in effects by composing with `withLatestFrom(...)`
-   **ALWAYS** compute derived state in selectors (do not store derived state)
-   **NEVER** use `tap`/`tapResponse` in selectors

**EXAMPLE:**
```typescript
// Replace legacy selectors with ComponentStore selectors
readonly events$ = this.select((state) => state.events);
readonly isLoading$ = this.select((state) => state.isLoading);

// Computed/derived state
readonly activeEvents$ = this.select(
  this.events$,
  (events) => events.filter((e) => e.isActive)
);
```

#### 5. Effects Best Practices

-   **ALWAYS** only use `tapResponse` nested in inner pipes (after `switchMap`/`mergeMap`)
-   **ALWAYS** use the RxJS `pipe` operator directly in effects: `this.effect<Type>(pipe(...))` instead of `this.effect<Type>((trigger$) => trigger$.pipe(...))`
-   **ALWAYS** use `switchMap` for effects that should cancel previous requests
-   **NEVER** subscribe directly to form controls or observables inside components; wire them into store effects
-   **NEVER** provide an empty observable (e.g., `this.effectName(of(undefined))`) when calling effects without arguments
    -   **NOTE**: The effect creates its own trigger observable internally; use `this.effectName()` instead
-   **ALWAYS** import `tapResponse` from `@ngrx/operators`, not `@ngrx/component-store`

**EXAMPLE - Correct import:**
```typescript
import { tapResponse } from '@ngrx/operators';
```

**EXAMPLE - Nested tapResponse pattern:**
```typescript
readonly saveEvent = this.effect<Event>(
  pipe(
    switchMap((event) =>
      this.#api.saveEvent(event).pipe(
        tapResponse({
          next: (saved) => this.updateEvent(saved),
          error: (error) => this.#errorHandler.handle(error),
        })
      )
    )
  )
);
```

#### 6. Websocket Integration

-   **ALWAYS** inject `ConnectSharedDataAccessWebsocketService` in the store, not in a separate service
-   **ALWAYS** wire websocket action observables directly to updaters in the constructor
-   **ALWAYS** wire connection state to load effects using `filter` and `map`
-   **NEVER** use `takeUntilDestroyed` for root-provided stores
    -   **NOTE**: ComponentStore handles cleanup automatically for root stores

**EXAMPLE:**
```typescript
readonly #wsService = inject(ConnectSharedDataAccessWebsocketService);

constructor() {
  super(initialState);

  // Wire websocket actions directly
  this.addItem(this.#wsService.action<Item>('AddItem'));
  this.updateItem(this.#wsService.action<Item>('UpdateItem'));

  // Trigger load on connection
  this.loadItems(
    this.#wsService.connectionState$.pipe(
      filter((state) => state === 'Connected'),
      map(() => undefined)
    )
  );
}
```

#### 7. Update Consumers

-   **ALWAYS** use the `inject()` function instead of constructor injection
-   **ALWAYS** place all `inject()` calls first in the class as readonly fields
-   **ALWAYS** use ECMAScript `#privateField` syntax for private members
-   **NEVER** use the `public` or `private` keywords in TypeScript

**EXAMPLE - Components Before:**
```typescript
readonly events$ = this.#store.select(eventSelectors.selectEvents);

ngOnInit() {
  this.#store.dispatch(eventActions.loadEvents());
}
```

**EXAMPLE - Components After:**
```typescript
readonly #eventStore = inject(EventStore);
readonly events$ = this.#eventStore.events$;

ngOnInit() {
  this.#eventStore.loadEvents();
}
```

**EXAMPLE - Services Before:**
```typescript
this.#store.dispatch(eventActions.updateEvent({ event }));
```

**EXAMPLE - Services After:**
```typescript
this.#eventStore.saveEvent(event);
```

#### 8. Clean Up Legacy Code

-   **ALWAYS** remove store registration from feature store config (e.g., `provide-event-store.ts`)
-   **ALWAYS** remove state slice from feature state interface
-   **ALWAYS** remove reducer mappings
-   **ALWAYS** remove legacy action exports (unless maintaining backward compatibility)
-   **ALWAYS** remove legacy selector exports (unless maintaining backward compatibility)
-   **ALWAYS** remove `Store` injection from components/services only using this store
-   **ALWAYS** update tests to use ComponentStore directly

---

### Critical Rules

#### Encapsulation

-   **ALWAYS** use subclassed services (not components) for stores
-   **ALWAYS** place the subclassed store in a separate file in the same folder as the component
-   **ALWAYS** use only inherited members inside the store; expose public state via selectors

#### Lifecycle

-   **NEVER** use lifecycle hooks (`OnStoreInit`, `OnStateInit`)
-   **NEVER** use `provideComponentStore`; prefer standard providers

#### What NOT to Do

-   **NEVER** use `takeUntilDestroyed` for root-provided stores
    -   **NOTE**: ComponentStore handles cleanup automatically; only needed for component-scoped stores
-   **NEVER** use `ComponentStore.get()`
    -   **ALWAYS** read state through selectors; use `withLatestFrom()` in effects for one-off reads
-   **NEVER** create manual subscriptions
    -   **ALWAYS** wire observables directly to updaters/effects; let ComponentStore manage subscriptions
-   **NEVER** import `tapResponse` from `@ngrx/component-store`
    -   **ALWAYS** import from `@ngrx/operators`: `import { tapResponse } from '@ngrx/operators';`
-   **NEVER** provide empty observables to effects
    -   **EXAMPLE**: Use `this.loadEvents()` not `this.loadEvents(of(undefined))`
-   **NEVER** keep legacy action/selector exports unless explicitly maintaining backward compatibility
-   **NEVER** register ComponentStores in feature store configurations

---

### File Organization

-   **ALWAYS** follow the library naming pattern: `libs/<product>/<application>/<domain>/<type>-<name>`
    -   **NOTE**: Product: `academy`, `coaching`, `connect`, `shared`
    -   **NOTE**: Application: `cms`, `shared`, `ufa` (User-Facing Application)
    -   **NOTE**: Type: `data-access`, `feature`, `ui`, etc.

**EXAMPLE:**
```
libs/connect/ufa/events/
├── data-access-event/
│   └── src/
│       ├── lib/
│       │   └── event.store.ts          # New ComponentStore
│       └── index.ts                     # Export store
└── feature-events/
    └── src/
        └── lib/
            └── event-list/
                └── event-list.component.ts  # Inject and use store
```

---

### Testing ComponentStores

-   **ALWAYS** use TestBed to configure the component store and its dependencies
-   **ALWAYS** test selectors by subscribing and verifying emitted values
-   **ALWAYS** test updaters by calling them and verifying state changes via selectors
-   **ALWAYS** test effects by triggering them and verifying side effects
-   **ALWAYS** use `{ provide: Service, useValue: mockService }` to mock dependencies
-   **ALWAYS** use `jest.spyOn()` to verify side effects
-   **CAN** use `patchState` with `// eslint-disable-next-line no-restricted-syntax` for test setup only
-   **ALWAYS** include the class name in `describe()` blocks: `describe(MyStore.name, () => ...)`
-   **ALWAYS** write test descriptions that clearly state expected behavior: `it('should...')`

**EXAMPLE:**
```typescript
describe(EventStore.name, () => {
  let store: EventStore;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        EventStore,
        { provide: ApiService, useValue: mockApiService },
      ],
    });
    store = TestBed.inject(EventStore);
  });

  it('should load events', (done) => {
    // Test selectors by subscribing
    store.events$.pipe(skip(1)).subscribe((events) => {
      expect(events).toEqual(mockEvents);
      done();
    });

    // Trigger effect
    store.loadEvents();
  });
});
```

---

### Quick Reference: Member Order

-   **ALWAYS** order members in ComponentStore classes consistently:

1. Injected dependencies (`inject()`)
2. Selectors (`readonly prop$ = this.select(...)`)
3. Constructor (wire websockets, connection triggers)
4. Effects (`readonly effectName = this.effect(...)`)
5. Updaters (`readonly setX = this.updater(...)`)
6. Private helpers

---

### Additional Best Practices from AGENTS.md

-   **ALWAYS** check AGENTS.md for for the latest definite best practices

#### TypeScript

-   **ALWAYS** prefer type inference when the type is obvious
-   **ALWAYS** avoid the `any` type; use `unknown` when type is uncertain
-   **ALWAYS** use ECMAScript `#privateField` syntax for encapsulation
-   **NEVER** use the `public` or `private` keywords in TypeScript class members

#### Angular Components Using Stores

-   **ALWAYS** set `changeDetection: ChangeDetectionStrategy.OnPush` in `@Component` decorator
-   **ALWAYS** use separate HTML files (do NOT use inline templates)
-   **ALWAYS** place all `inject()` calls first in the class as readonly fields
-   **ALWAYS** place `@Input` and `@Output` properties second in the class

#### Templates

-   **ALWAYS** use native control flow (`@if`, `@for`, `@switch`) instead of `*ngIf`, `*ngFor`, `*ngSwitch`
-   **ALWAYS** use the `*ngrxLet` directive or `ngrxPush` pipe to handle Observables
    -   **ALWAYS** prefer the `ngrxPush` pipe over `async` for one-off async bindings in templates
    -   **PREFER** not using `*ngrxLet` or `ngrxPush` multiple times for the same Observable; instead assign it to a template variable using `@let`

#### Services & Dependency Injection

-   **ALWAYS** use the `inject()` function instead of constructor injection
-   **ALWAYS** place all `inject()` calls first as private readonly fields
-   **ALWAYS** use the `providedIn: 'root'` option for singleton services
-   **ALWAYS** use `@Component.providers` for component-level stores

---

### Before Submitting Code Review

-   **ALWAYS** ensure all affected tests pass locally
-   **ALWAYS** run formatting: `yarn run format` (from `Connect/ng-app-monolith`)
-   **ALWAYS** run linting: `yarn exec nx affected --targets=lint,test --skip-nx-cache`
-   **ALWAYS** verify no linting errors are present
-   **ALWAYS** ensure code follows established patterns as outlined in AGENTS.md

## Examples

See Instructions Section for code examples.
