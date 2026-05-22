---
name: ngrx-store
description: Use when creating NgRx Signals Stores for state management. Triggers on requests to "create store", "add state management", "new store", "signal store", or when implementing state patterns with NgRx Signals.
---

# NgRx Signals Store Guide

Create NgRx Signals Stores following project patterns.

## Store File Location

```
src/app/
  <domain>/
    data/
      state/
        <domain>-store.ts      # Store definition (dash separator)
      models/
        <domain>.model.ts      # State interfaces
      infrastructure/
        <domain>.ts            # API service
```

## Basic Store Template

```typescript
import { computed, inject } from "@angular/core";
import {
  signalStore,
  withState,
  withComputed,
  withMethods,
  patchState,
} from "@ngrx/signals";
import { rxMethod } from "@ngrx/signals/rxjs-interop";
import { tapResponse } from "@ngrx/operators";
import { pipe, switchMap } from "rxjs";

import { ItemService } from "../infrastructure/item";
import { Item } from "../models/item.model";

// State interface
export interface ItemState {
  items: Item[];
  selectedItemId: string | null;
  loading: boolean;
  error: string | null;
}

// Initial state
const initialState: ItemState = {
  items: [],
  selectedItemId: null,
  loading: false,
  error: null,
};

// Store definition
export const ItemStore = signalStore(
  { providedIn: "root" },
  withState(initialState),

  withComputed(({ items, selectedItemId }) => ({
    selectedItem: computed(() => {
      const id = selectedItemId();
      return items().find((item) => item.id === id);
    }),
    itemCount: computed(() => items().length),
  })),

  withMethods((store, itemService = inject(ItemService)) => ({
    // Synchronous method
    selectItem(id: string | null): void {
      patchState(store, { selectedItemId: id });
    },

    // Async method using rxMethod for Observable-based APIs
    loadItems: rxMethod<void>(
      pipe(
        switchMap(() => {
          patchState(store, { loading: true, error: null });
          return itemService.getItems().pipe(
            tapResponse({
              next: (items) => patchState(store, { items, loading: false }),
              error: (error: Error) =>
                patchState(store, {
                  loading: false,
                  error: error.message,
                }),
            }),
          );
        }),
      ),
    ),

    // Async method with parameter
    loadItemById: rxMethod<string>(
      pipe(
        switchMap((id) => {
          patchState(store, { loading: true });
          return itemService.getItemById(id).pipe(
            tapResponse({
              next: (item) =>
                patchState(store, (state) => ({
                  items: [...state.items.filter((i) => i.id !== id), item],
                  loading: false,
                })),
              error: () => patchState(store, { loading: false }),
            }),
          );
        }),
      ),
    ),
  })),
);
```

## Entity Store Template

```typescript
import { computed, inject } from "@angular/core";
import {
  signalStore,
  withState,
  withComputed,
  withMethods,
  patchState,
  type,
} from "@ngrx/signals";
import {
  withEntities,
  entityConfig,
  addEntity,
  updateEntity,
  removeEntity,
  setAllEntities,
} from "@ngrx/signals/entities";
import { rxMethod } from "@ngrx/signals/rxjs-interop";
import { tapResponse } from "@ngrx/operators";
import { pipe, switchMap } from "rxjs";

import { TaskService } from "../infrastructure/task";
import { Task } from "../models/task.model";

// State for non-entity properties
export interface TaskState {
  selectedTaskId: string | null;
  filter: "all" | "pending" | "completed";
  loading: boolean;
  error: string | null;
}

const initialState: TaskState = {
  selectedTaskId: null,
  filter: "all",
  loading: false,
  error: null,
};

// Entity configuration
const taskEntityConfig = entityConfig({
  entity: type<Task>(),
  collection: "tasks",
  selectId: (task: Task) => task.id,
});

export const TaskStore = signalStore(
  { providedIn: "root" },
  withState(initialState),
  withEntities(taskEntityConfig),

  withComputed(({ tasksEntities, tasksEntityMap, selectedTaskId, filter }) => ({
    selectedTask: computed(() => {
      const id = selectedTaskId();
      return id ? tasksEntityMap()[id] : undefined;
    }),

    filteredTasks: computed(() => {
      const tasks = tasksEntities();
      const currentFilter = filter();

      switch (currentFilter) {
        case "pending":
          return tasks.filter((t) => !t.completed);
        case "completed":
          return tasks.filter((t) => t.completed);
        default:
          return tasks;
      }
    }),

    taskCount: computed(() => tasksEntities().length),
  })),

  withMethods((store, taskService = inject(TaskService)) => ({
    setFilter(filter: "all" | "pending" | "completed"): void {
      patchState(store, { filter });
    },

    selectTask(id: string | null): void {
      patchState(store, { selectedTaskId: id });
    },

    loadTasks: rxMethod<void>(
      pipe(
        switchMap(() => {
          patchState(store, { loading: true, error: null });
          return taskService.getTasks().pipe(
            tapResponse({
              next: (tasks) =>
                patchState(store, setAllEntities(tasks, taskEntityConfig), {
                  loading: false,
                }),
              error: (error: Error) =>
                patchState(store, {
                  loading: false,
                  error: error.message,
                }),
            }),
          );
        }),
      ),
    ),

    addTask: rxMethod<Omit<Task, "id">>(
      pipe(
        switchMap((task) => {
          patchState(store, { loading: true });
          return taskService.createTask(task).pipe(
            tapResponse({
              next: (newTask) =>
                patchState(store, addEntity(newTask, taskEntityConfig), {
                  loading: false,
                }),
              error: () => patchState(store, { loading: false }),
            }),
          );
        }),
      ),
    ),

    updateTask: rxMethod<{ id: string; changes: Partial<Task> }>(
      pipe(
        switchMap(({ id, changes }) => {
          return taskService.updateTask(id, changes).pipe(
            tapResponse({
              next: () =>
                patchState(
                  store,
                  updateEntity({ id, changes }, taskEntityConfig),
                ),
              error: () => console.error("Update failed"),
            }),
          );
        }),
      ),
    ),

    deleteTask: rxMethod<string>(
      pipe(
        switchMap((id) => {
          return taskService.deleteTask(id).pipe(
            tapResponse({
              next: () => patchState(store, removeEntity(id, taskEntityConfig)),
              error: () => console.error("Delete failed"),
            }),
          );
        }),
      ),
    ),
  })),
);
```

## Store with Hooks

```typescript
import { withHooks } from "@ngrx/signals";

export const ItemStore = signalStore(
  { providedIn: "root" },
  withState(initialState),
  withMethods(/* ... */),
  withHooks({
    onInit: (store) => {
      // Called when store is initialized
      store.loadItems();
    },
    onDestroy: (store) => {
      // Cleanup if needed
    },
  }),
);
```

## Custom Store Properties

```typescript
import { withProps } from "@ngrx/signals";
import { toObservable } from "@angular/core/rxjs-interop";

export const ItemStore = signalStore(
  withState(initialState),
  withProps(({ loading }) => ({
    // Expose as Observable for RxJS interop
    loading$: toObservable(loading),

    // Inject dependencies
    itemService: inject(ItemService),
    logger: inject(Logger),
  })),
  withMethods((store) => ({
    // Access via store.itemService, store.logger
  })),
);
```

## Component Integration

```typescript
import {
  Component,
  inject,
  OnInit,
  ChangeDetectionStrategy,
} from "@angular/core";
import { TaskStore } from "../data/state/task-store";

@Component({
  selector: "app-task-list",
  template: `
    @if (taskStore.loading()) {
      <app-spinner />
    } @else {
      @for (task of taskStore.filteredTasks(); track task.id) {
        <app-task-item
          [task]="task"
          (toggle)="
            taskStore.updateTask({
              id: task.id,
              changes: { completed: $event },
            })
          "
          (delete)="taskStore.deleteTask(task.id)"
        />
      } @empty {
        <p>No tasks found</p>
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TaskList implements OnInit {
  readonly taskStore = inject(TaskStore);

  ngOnInit(): void {
    this.taskStore.loadTasks();
  }
}
```

## Store Testing

```typescript
import { TestBed } from "@angular/core/testing";
import { provideZonelessChangeDetection } from "@angular/core";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { of } from "rxjs";

import { TaskStore } from "./task-store";
import { TaskService } from "../infrastructure/task";

describe("TaskStore", () => {
  let store: InstanceType<typeof TaskStore>;
  let mockService: Partial<TaskService>;

  beforeEach(() => {
    mockService = {
      getTasks: vi.fn().mockReturnValue(of([])),
      createTask: vi.fn(),
    };

    TestBed.configureTestingModule({
      providers: [
        TaskStore,
        provideZonelessChangeDetection(),
        { provide: TaskService, useValue: mockService },
      ],
    });

    store = TestBed.inject(TaskStore);
  });

  it("should initialize with default state", () => {
    expect(store.loading()).toBe(false);
    expect(store.tasksEntities()).toEqual([]);
  });

  it("should load tasks", () => {
    const tasks = [{ id: "1", title: "Test", completed: false }];
    vi.mocked(mockService.getTasks).mockReturnValue(of(tasks));

    store.loadTasks();

    expect(store.tasksEntities()).toEqual(tasks);
  });
});
```

## Checklist

- [ ] Store file in `data/state/` folder
- [ ] State interface defined with proper types
- [ ] Initial state with meaningful defaults
- [ ] Using `rxMethod` for Observable-based API calls
- [ ] Using `tapResponse` for error handling
- [ ] Entity stores using `withEntities` and entity operations
- [ ] Computed properties for derived state
- [ ] Store is `providedIn: 'root'` or properly scoped
