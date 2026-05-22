---
name: vendix-frontend
description: >
  Angular 20 + NgRx patterns for Vendix frontend.
  Trigger: When editing files in apps/frontend/, creating components, or working with NgRx store.
license: MIT
metadata:
  author: vendix
  version: "1.0"
---

## When to Use

Use this skill when:
- Creating or modifying Angular components
- Adding NgRx features (store, effects, entities)
- Working with frontend architecture
- Implementing state management patterns

## Critical Patterns

### Pattern 1: Feature Folder Structure

All features MUST follow this structure:

```
apps/frontend/src/app/features/
└── my-feature/
    ├── state/
    │   ├── reducers/
    │   │   └── my-feature.reducer.ts
    │   ├── actions/
    │   │   └── my-feature.actions.ts
    │   ├── selectors/
    │   │   └── my-feature.selectors.ts
    │   ├── effects/
    │   │   └── my-feature.effects.ts
    │   └── my-feature.state.ts
    ├── components/
    │   ├── my-feature.component.ts
    │   ├── my-feature.component.html
    │   └── my-feature.component.scss
    └── pages/
        └── my-feature-page/
```

### Pattern 2: NgRx Feature State

State definition with TypeScript interfaces:

```typescript
// state/my-feature.state.ts
export interface MyFeatureState {
  items: Item[];
  loading: boolean;
  error: string | null;
}

export const initialMyFeatureState: MyFeatureState = {
  items: [],
  loading: false,
  error: null,
};
```

### Pattern 3: Component with NgRx

Components use selectors and dispatch actions:

```typescript
import { Store } from '@ngrx/store';
import { selectMyFeatureItems, selectMyFeatureLoading } from './state/selectors/my-feature.selectors';

@Component({
  selector: 'vendix-my-feature',
  template: `
    @if (loading$ | async) {
      <vendix-loading />
    } @else {
      <vendix-item-list [items]="items$ | async" />
    }
  `,
})
export class MyFeatureComponent implements OnInit {
  items$ = this.store.select(selectMyFeatureItems);
  loading$ = this.store.select(selectMyFeatureLoading);

  constructor(private store: Store) {}

  ngOnInit() {
    this.store.dispatch(MyFeatureActions.loadItems());
  }
}
```

### Pattern 4: Standalone Components (Angular 20)

Angular 20 uses standalone components:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'vendix-my-component',
  standalone: true,
  imports: [CommonModule],
  template: `...`,
})
export class MyComponent {}
```

## Decision Tree

```
Creating a new feature?
├── Generate feature folder structure
├── Create state files (reducer, actions, selectors, effects)
├── Register state in app.config.ts
└── Create components and pages

Adding API call?
├── Create action (load, success, failure)
├── Create effect to call service
├── Update reducer with success/failure
└── Create selector for data

Modifying existing component?
├── Check if using standalone pattern
├── Use async pipe for observables
└── Dispatch actions for state changes
```

## Code Examples

### Example 1: Creating NgRx Actions

```typescript
// state/actions/my-feature.actions.ts
import { createAction, props } from '@ngrx/store';

export const loadItems = createAction('[MyFeature] Load Items');
export const loadItemsSuccess = createAction(
  '[MyFeature] Load Items Success',
  props<{ items: Item[] }>()
);
export const loadItemsFailure = createAction(
  '[MyFeature] Load Items Failure',
  props<{ error: string }>()
);
```

### Example 2: Creating Reducer

```typescript
// state/reducers/my-feature.reducer.ts
import { createReducer, on } from '@ngrx/store';
import * as MyFeatureActions from '../actions/my-feature.actions';
import { initialMyFeatureState, MyFeatureState } from '../my-feature.state';

export const myFeatureReducer = createReducer(
  initialMyFeatureState,
  on(MyFeatureActions.loadItems, (state): MyFeatureState => ({
    ...state,
    loading: true,
    error: null,
  })),
  on(MyFeatureActions.loadItemsSuccess, (state, { items }): MyFeatureState => ({
    ...state,
    items,
    loading: false,
  })),
  on(MyFeatureActions.loadItemsFailure, (state, { error }): MyFeatureState => ({
    ...state,
    loading: false,
    error,
  }))
);
```

### Example 3: Creating Selectors

```typescript
// state/selectors/my-feature.selectors.ts
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { MyFeatureState } from '../my-feature.state';

export const selectMyFeatureState = createFeatureSelector<MyFeatureState>('myFeature');

export const selectMyFeatureItems = createSelector(
  selectMyFeatureState,
  (state: MyFeatureState) => state.items
);

export const selectMyFeatureLoading = createSelector(
  selectMyFeatureState,
  (state: MyFeatureState) => state.loading
);
```

### Example 4: Creating Effects

```typescript
// state/effects/my-feature.effects.ts
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, mergeMap } from 'rxjs/operators';
import { of } from 'rxjs';
import * as MyFeatureActions from '../actions/my-feature.actions';
import { MyFeatureService } from '../../services/my-feature.service';

@Injectable()
export class MyFeatureEffects {
  loadItems$ = createEffect(() =>
    this.actions$.pipe(
      ofType(MyFeatureActions.loadItems),
      mergeMap(() =>
        this.myFeatureService.getItems().pipe(
          map((items) => MyFeatureActions.loadItemsSuccess({ items })),
          catchError((error) =>
            of(MyFeatureActions.loadItemsFailure({ error: error.message }))
          )
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private myFeatureService: MyFeatureService
  ) {}
}
```

## Commands

```bash
# Generate new component
cd apps/frontend
ng generate component components/my-component --standalone

# Generate new feature (manual - create folder structure)
mkdir -p src/app/features/my-feature/{state/{reducers,actions,selectors,effects},components,pages}

# Run frontend
npm run start -w apps/frontend

# Build frontend for production
npm run build:prod -w apps/frontend

# Run tests
npm run test -w apps/frontend

# Format code
npm run format -w apps/frontend
```

## Resources

- **Frontend**: See [apps/frontend/README.md](../../../apps/frontend/README.md)
- **NgRx Docs**: https://ngrx.ai
- **Angular Docs**: https://angular.dev
