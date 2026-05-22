---
name: kramme:connect-modernize-legacy-angular-component
description: Use this Skill when working in the Connect monorepo and needing to modernize legacy Angular components.
---

# Connect - Modernize Legacy Angular Component

## Instructions

**When to use this skill:**

- You're working in the Connect monorepo
- You need to refactor legacy Angular components to modern patterns
- Component extends legacy `FormComponent` or `BaseComponent`
- Component uses `@Select` decorators for state management
- Component uses `FormNode` instead of typed `FormGroup`
- Component doesn't use `ChangeDetectionStrategy.OnPush`
- Component has manual subscription management
- Component dispatches actions directly instead of using ComponentStore

**Context:** Connect's frontend is modernizing Angular components to use NgRx ComponentStore for state management, OnPush change detection, standalone components, and proper TypeScript typing. This provides better type safety, performance, and maintainability.

### Guideline Keywords

- **ALWAYS** — Mandatory requirement, exceptions are very rare and must be explicitly approved
- **NEVER** — Strong prohibition, exceptions are very rare and must be explicitly approved
- **PREFER** — Strong recommendation, exceptions allowed with justification
- **CAN** — Optional, developer's discretion
- **NOTE** — Context, rationale, or clarification
- **EXAMPLE** — Illustrative example

Strictness hierarchy: ALWAYS/NEVER > PREFER > CAN > NOTE/EXAMPLE

---

### Reference Implementation

- **ALWAYS** refer to the Q&A components refactoring as the reference implementation:
  - `libs/connect/cms/qa/feature/src/lib/edit-topic/` - Edit topic component with form management
  - `libs/connect/cms/qa/feature/src/lib/settings-page/` - Settings page with conditional form logic
  - `libs/connect/cms/qa/feature/src/lib/topics-page/` - Topics page with complex state

---

### Migration Process

#### Phase 1: Assessment

- **ALWAYS** read all component files before starting:

  - Component TypeScript file
  - Component template
  - Component styles (if any)
  - Related store/state files

- **ALWAYS** identify patterns to migrate:

  - Legacy base class usage (`extends FormComponent`, `extends BaseComponent`)
  - `@Select` decorators for state
  - `FormNode` usage
  - Manual subscriptions (`subscribe()`, `takeUntil()`)
  - Direct action dispatching
  - Lifecycle hooks (`onInit()` vs `ngOnInit()`)

- **ALWAYS** identify business logic:
  - Form management
  - State updates
  - API calls
  - Conditional field logic
  - User interactions

---

#### Phase 2: Create ComponentStore

- **ALWAYS** create the store file in the same directory as the component (e.g., `component-name.store.ts`)
- **ALWAYS** define form controls interface separately from state
- **ALWAYS** define forms as class properties, NOT in state
- **ALWAYS** extract `initialState` as a constant
- **ALWAYS** use `readonly` for immutability
- **ALWAYS** use ECMAScript `#privateFields` for encapsulation
- **ALWAYS** use proper type narrowing in effects with filter: `(tuple): tuple is [void, DataType] => tuple[1] !== null`
- **ALWAYS** use `pipe()` directly in effects: `this.effect<Type>(pipe(...))` not `this.effect<Type>((param$) => param$.pipe(...))`

**EXAMPLE:**

```typescript
import { inject, Injectable } from "@angular/core";
import { ComponentStore } from "@ngrx/component-store";
import { Store } from "@ngrx/store";
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { filter, pipe, switchMap, tap, withLatestFrom } from "rxjs";

// Define form controls interface
export interface ComponentNameFormControls {
  field1: FormControl<string>;
  field2: FormControl<boolean>;
}

// Define state interface
interface ComponentNameState {
  readonly currentData: DataType | null;
}

const initialState: ComponentNameState = {
  currentData: null,
};

@Injectable()
export class ComponentNameStore extends ComponentStore<ComponentNameState> {
  readonly #store = inject(Store);

  // Selectors
  readonly currentData$ = this.select((state) => state.currentData);
  readonly externalData$ = this.#store.select(getExternalData.selector);

  // Form definition
  readonly form = new FormGroup<ComponentNameFormControls>({
    field1: new FormControl<string>("", {
      validators: [Validators.required],
      nonNullable: true,
    }),
    field2: new FormControl<boolean>(false, { nonNullable: true }),
  });

  // Updaters
  readonly setCurrentData = this.updater<DataType>(
    (state, data): ComponentNameState => ({
      ...state,
      currentData: data,
    })
  );

  // Effects - use pipe() directly
  readonly initializeForm = this.effect<DataType>(
    pipe(
      tap((data: DataType) => {
        this.setCurrentData(data);
        this.form.reset(data);
        this.#applyConditionalLogic(this.form);
      })
    )
  );

  readonly saveChanges = this.effect<void>(
    pipe(
      tap(() => {
        this.#store.dispatch(updateAction.start(this.form.getRawValue()));
      })
    )
  );

  readonly cancelChanges = this.effect<void>(
    pipe(
      withLatestFrom(this.currentData$),
      filter((tuple): tuple is [void, DataType] => tuple[1] !== null),
      tap(([, data]) => {
        this.form.reset(data);
        this.#applyConditionalLogic(this.form);
      })
    )
  );

  // Private methods
  #applyConditionalLogic(form: FormGroup<ComponentNameFormControls>): void {
    // Conditional enabling/disabling logic
  }

  constructor() {
    super(initialState);
    // Initialize effects that don't take parameters
    this.applyConditionalDisabling();
  }
}
```

---

#### Phase 3: Refactor Component

- **ALWAYS** add `ChangeDetectionStrategy.OnPush`
- **ALWAYS** add `standalone: true`
- **ALWAYS** add ComponentStore to `providers` array
- **ALWAYS** use `inject()` for dependency injection
- **ALWAYS** place all `inject()` calls first in the class as readonly fields
- **ALWAYS** use ECMAScript `#privateField` syntax for private members
- **NEVER** use the `public` or `private` keywords in TypeScript
- **ALWAYS** remove base class extensions
- **ALWAYS** remove `@Select` decorators
- **ALWAYS** remove manual subscriptions
- **ALWAYS** remove `DestroyRef` and `takeUntilDestroyed` (ComponentStore handles cleanup)

**EXAMPLE:**

```typescript
import {
  ChangeDetectionStrategy,
  Component,
  inject,
  Input,
} from "@angular/core";
import { animate, style, transition, trigger } from "@angular/animations";
import { ComponentNameStore } from "./component-name.store";

@Component({
  selector: "co-component-name",
  templateUrl: "./component-name.component.html",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [ComponentNameStore],
  imports: [
    // Only what you need
  ],
  animations: [
    trigger("slideDown", [
      transition(":enter", [
        style({ height: "0", opacity: 0, overflow: "hidden" }),
        animate("300ms ease-out", style({ height: "*", opacity: 1 })),
      ]),
      transition(":leave", [
        style({ height: "*", opacity: 1, overflow: "hidden" }),
        animate("300ms ease-in", style({ height: "0", opacity: 0 })),
      ]),
    ]),
  ],
})
export class ComponentNameComponent {
  readonly #componentStore = inject(ComponentNameStore);

  @Input() set data(data: DataType) {
    if (data) {
      this.#componentStore.initializeForm(data);
    }
  }

  readonly form = this.#componentStore.form;
  readonly data$ = this.#componentStore.currentData$;

  saveChanges(): void {
    this.#componentStore.saveChanges();
  }

  cancelChanges(): void {
    this.#componentStore.cancelChanges();
  }
}
```

---

#### Phase 4: Update Template

- **ALWAYS** use native control flow (`@if`, `@for`, `@switch`) instead of `*ngIf`, `*ngFor`, `*ngSwitch`
- **ALWAYS** use the `*ngrxLet` directive or `ngrxPush` pipe to handle Observables
  - **ALWAYS** prefer the `ngrxPush` pipe over `async` for one-off async bindings
  - **PREFER** not using `*ngrxLet` or `ngrxPush` multiple times for the same Observable; instead assign it to a template variable using `@let`
- **PREFER** adding animations for conditional UI
- **ALWAYS** use form bindings with proper type checking

**EXAMPLE - Native control flow with animation:**

```html
@if (form.controls.parentField.value) {
<div @slideDown>
  <mat-slide-toggle formControlName="childField">
    Child Field
  </mat-slide-toggle>
</div>
}
```

**EXAMPLE - Form bindings:**

```html
<form [formGroup]="form" class="tw-space-y-4">
  <mat-form-field class="tw-w-full" subscriptSizing="fixed">
    <mat-label>Field Name</mat-label>
    <input matInput formControlName="fieldName" required />
    @if (form.controls.fieldName.hasError("required")) {
    <mat-error>Field is required</mat-error>
    }
  </mat-form-field>
</form>
```

---

#### Phase 5: UX Enhancements

##### Confirmation Modals

- **ALWAYS** add confirmation modals for destructive actions
- **ALWAYS** use MatDialog to open modals
- **ALWAYS** subscribe to `afterClosed()` and only proceed if confirmed

**EXAMPLE:**

```typescript
deleteItem(): void {
  this.#dialog
    .open(ConfirmDeleteModalComponent, {
      data: { itemName: this.data$.value?.name },
    })
    .afterClosed()
    .subscribe((confirmed) => {
      if (confirmed) {
        this.#componentStore.deleteItem();
      }
    });
}
```

##### User Feedback

- **ALWAYS** use `successMessage` in ApiAction definitions (not manual toasts in stores)
- **ALWAYS** use `CoSnackService` only for local operations (cancel, info messages)
- **NEVER** show success before API call completes

**EXAMPLE - Success Messages:**

```typescript
// ❌ WRONG - shows before API completes
readonly saveChanges = this.effect<void>(
  pipe(
    tap(() => {
      this.#store.dispatch(updateAction.start(this.form.getRawValue()));
      this.#snacks.success('Saved!'); // ← BAD
    })
  )
);

// ✅ CORRECT - shows only on actual success
export const updateAction = new ApiAction<State, Input, Output>(
  'Entity',
  'Update',
  'Feature',
  {
    showErrors: true,
    successMessage: 'Saved!', // ← GOOD
  }
);
```

##### Copy to Clipboard

- **PREFER** adding copy-to-clipboard buttons for IDs

**EXAMPLE:**

```html
<button
  matSuffix
  mat-icon-button
  matTooltip="Copy to clipboard"
  [cdkCopyToClipboard]="form.controls.id.value"
  (cdkCopyToClipboardCopied)="onIdCopied($event)"
>
  <fa-icon [icon]="copyIcon" />
</button>
```

---

#### Phase 6: Verification

- **ALWAYS** run lint: `corepack yarn nx lint <library-name>`
- **ALWAYS** check for:
  - No manual subscriptions in components
  - All effects use `pipe()` directly
  - Forms have proper type annotations
  - No `any` types
  - Proper change detection strategy
- **ALWAYS** test:
  - Form initialization
  - Save/cancel flows
  - Conditional field logic
  - Error handling
  - User feedback

---

### Common Patterns

#### Conditional Field Disabling

- **ALWAYS** create a private method for conditional logic
- **ALWAYS** use `{ emitEvent: false }` when programmatically enabling/disabling controls
- **ALWAYS** call after form reset and in an effect watching the parent field

**EXAMPLE:**

```typescript
#applyConditionalDisabling(form: FormGroup<FormControls>): void {
  const parentValue = form.controls.parentField.value;

  if (!parentValue) {
    form.controls.childField.disable({ emitEvent: false });
  } else {
    form.controls.childField.enable({ emitEvent: false });
  }
}

// Call after form reset and in an effect watching the parent field
readonly applyConditionalDisabling = this.effect<void>(
  pipe(
    switchMap(() => this.form.controls.parentField.valueChanges),
    tap(() => {
      this.#applyConditionalDisabling(this.form);
    })
  )
);
```

#### Form Controls with nonNullable

- **ALWAYS** add `nonNullable: true` to form controls to ensure type safety
- **NOTE**: This prevents the form control value from being `null` after reset

**EXAMPLE:**

```typescript
readonly form = new FormGroup<ComponentNameFormControls>({
  field1: new FormControl<string>('', {
    validators: [Validators.required],
    nonNullable: true // ← ALWAYS include this
  }),
  field2: new FormControl<boolean>(false, { nonNullable: true }),
});
```

---

### Critical Rules

#### Forms

- **NEVER** store forms in ComponentStore state
  - **ALWAYS** define forms as class properties in the store
- **ALWAYS** add `nonNullable: true` to form controls
- **ALWAYS** use typed `FormGroup` and `FormControl` (not `FormNode`)
- **ALWAYS** define form controls interface

#### Effects

- **ALWAYS** use `pipe()` directly: `this.effect<Type>(pipe(...))`
- **NEVER** use arrow functions: `this.effect<Type>((param$) => param$.pipe(...))`
- **ALWAYS** use proper type narrowing with filter

#### Subscriptions

- **NEVER** use manual subscriptions in components
  - **NOTE**: ComponentStore handles cleanup automatically
- **NEVER** use `DestroyRef` and `takeUntilDestroyed` for ComponentStore subscriptions
- **ALWAYS** wire observables directly to updaters/effects

#### User Feedback

- **NEVER** show success toasts before API calls complete
- **ALWAYS** use `successMessage` in ApiAction definitions
- **ALWAYS** use `CoSnackService` only for local operations

#### TypeScript

- **NEVER** use `any` types
  - **ALWAYS** use `unknown` when type is uncertain
- **ALWAYS** use ECMAScript `#privateField` syntax for encapsulation
- **NEVER** use the `public` or `private` keywords in TypeScript class members

#### State Management

- **NEVER** use `ComponentStore.get()`
  - **ALWAYS** read state via selectors
- **NEVER** keep empty effects

---

### Migration Checklist

- [ ] Phase 1: Read all component files and identify patterns
- [ ] Phase 2: Create ComponentStore
  - [ ] Defined state interface with `readonly` properties
  - [ ] Defined form controls interface
  - [ ] Created form as class property (not in state)
  - [ ] All selectors use `$` suffix
  - [ ] All effects use `pipe()` directly
  - [ ] Proper type narrowing in effects
- [ ] Phase 3: Refactor component
  - [ ] Component uses `OnPush` change detection
  - [ ] Component is `standalone: true`
  - [ ] ComponentStore in providers array
  - [ ] Removed base class extensions
  - [ ] Removed `@Select` decorators
  - [ ] Removed manual subscriptions
  - [ ] All `inject()` calls first in class
  - [ ] Using `#privateField` syntax
- [ ] Phase 4: Update template
  - [ ] Updated template to use native control flow
  - [ ] Added animations for conditional UI
  - [ ] Proper form bindings
- [ ] Phase 5: UX enhancements
  - [ ] Added confirmation dialogs for destructive actions
  - [ ] Success messages in ApiAction (not manual toasts)
  - [ ] Copy-to-clipboard for IDs (if applicable)
- [ ] Phase 6: Verification
  - [ ] Lint passes
  - [ ] No manual subscriptions in components
  - [ ] Forms have proper type annotations
  - [ ] No `any` types
  - [ ] Tested all workflows

---

### Additional Best Practices from AGENTS.md

- **ALWAYS** check AGENTS.md for the latest definite best practices

#### Angular Components

- **ALWAYS** set `changeDetection: ChangeDetectionStrategy.OnPush` in `@Component` decorator for new components
- **ALWAYS** use separate HTML files (do NOT use inline templates)
- **ALWAYS** place all `inject()` calls first in the class as readonly fields
- **ALWAYS** place `@Input` and `@Output` properties second in the class
- **ALWAYS** use `class` bindings instead of `ngClass`
- **ALWAYS** use `style` bindings instead of `ngStyle`
- **ALWAYS** use pipes for data transformation in templates, not methods in the component class

#### UI and Styling

- **PREFER** Angular Material/CDK for complex, interactive UI
- **NEVER** override internal APIs in Angular Material components
- **ALWAYS** use Tailwind for layout, spacing, and simple styling
- **ALWAYS** use `tw-` prefix (enforced in `libs/co/ui-tailwind-preset/tailwind.config.js`)
- **ALWAYS** define repeated patterns in CSS layer using `@apply` directive

#### FontAwesome Icons

- **ALWAYS** use FontAwesome icons via the `@fortawesome/angular-fontawesome` package
- **ALWAYS** use `<fa-icon>` component, not `<i>` tags with CSS classes
- **ALWAYS** import from `@fortawesome/pro-*-svg-icons` (not free packages)
- **ALWAYS** store icons as readonly component properties; prefer regular style by default

---

### Before Submitting Code Review

- **ALWAYS** ensure all affected tests pass locally
- **ALWAYS** run formatting: `yarn run format` (from `Connect/ng-app-monolith`)
- **ALWAYS** run linting: `yarn exec nx affected --targets=lint,test --skip-nx-cache`
- **ALWAYS** verify no linting errors are present
- **ALWAYS** ensure code follows established patterns as outlined in AGENTS.md

---

### Reference Files

**ALWAYS** refer to these files for complete examples:

- `libs/connect/cms/qa/feature/src/lib/edit-topic/cms-qa-edit-topic.store.ts`
- `libs/connect/cms/qa/feature/src/lib/settings-page/cms-qa-settings-page.store.ts`
- `libs/connect/cms/qa/feature/src/lib/topics-page/cms-qa-topics-page.store.ts`
- `AGENTS.md` - Angular Development Patterns section

### Examples

See the Instructions section.
