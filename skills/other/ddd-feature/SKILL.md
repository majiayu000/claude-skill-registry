---
name: ddd-feature
description: Use when creating new domain features or adding new business capabilities. Triggers on requests to "create feature", "add new domain", "new module", "scaffold feature", or when implementing complete business features.
---

# DDD Feature Creation Guide

Create new domain features following the project's Domain-Driven Design structure.

## Domain Structure

```
src/app/
  <domain>/                    # Business domain (tasks, user, order, etc.)
    feature/                   # Feature/container components
      <feature-name>/
        <feature-name>.ts
        <feature-name>.html
        <feature-name>.scss
        <feature-name>.spec.ts
    ui/                        # Presentational components
      <component-name>/
        <component-name>.ts
        ...
    data/                      # Data access layer
      models/
        <domain>.model.ts      # Domain models/interfaces
      infrastructure/
        <domain>.ts            # API service
      state/
        <domain>-store.ts      # NgRx Signals Store
    util/                      # Domain utilities
      <util-name>/
        <util-name>.ts
```

## Step-by-Step Feature Creation

### 1. Create Domain Model

`src/app/tasks/data/models/task.model.ts`:

```typescript
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  dueDate: string | null;
  createdAt: string;
  updatedAt: string;
}

export type CreateTaskDto = Omit<Task, "id" | "createdAt" | "updatedAt">;
export type UpdateTaskDto = Partial<CreateTaskDto>;
```

### 2. Create Infrastructure Service

`src/app/tasks/data/infrastructure/task.ts`:

```typescript
import { inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

import { Task, CreateTaskDto, UpdateTaskDto } from "../models/task.model";

@Injectable({ providedIn: "root" })
export class TaskInfrastructure {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = "http://localhost:3000/tasks";

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.baseUrl);
  }

  getTaskById(id: string): Observable<Task> {
    return this.http.get<Task>(`${this.baseUrl}/${id}`);
  }

  createTask(task: CreateTaskDto): Observable<Task> {
    return this.http.post<Task>(this.baseUrl, task);
  }

  updateTask(id: string, changes: UpdateTaskDto): Observable<Task> {
    return this.http.patch<Task>(`${this.baseUrl}/${id}`, changes);
  }

  deleteTask(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
```

### 3. Create Signal Store

`src/app/tasks/data/state/task-store.ts`:

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

import { TaskInfrastructure } from "../infrastructure/task";
import { Task, CreateTaskDto, UpdateTaskDto } from "../models/task.model";

export interface TaskState {
  selectedTaskId: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: TaskState = {
  selectedTaskId: null,
  loading: false,
  error: null,
};

const taskEntityConfig = entityConfig({
  entity: type<Task>(),
  collection: "tasks",
  selectId: (task: Task) => task.id,
});

export const TaskStore = signalStore(
  { providedIn: "root" },
  withState(initialState),
  withEntities(taskEntityConfig),

  withComputed(({ tasksEntities, tasksEntityMap, selectedTaskId }) => ({
    selectedTask: computed(() => {
      const id = selectedTaskId();
      return id ? tasksEntityMap()[id] : undefined;
    }),
    taskCount: computed(() => tasksEntities().length),
  })),

  withMethods((store, taskService = inject(TaskInfrastructure)) => ({
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

    createTask: rxMethod<CreateTaskDto>(
      pipe(
        switchMap((dto) => {
          patchState(store, { loading: true });
          return taskService.createTask(dto).pipe(
            tapResponse({
              next: (task) =>
                patchState(store, addEntity(task, taskEntityConfig), {
                  loading: false,
                }),
              error: () => patchState(store, { loading: false }),
            }),
          );
        }),
      ),
    ),

    updateTask: rxMethod<{ id: string; changes: UpdateTaskDto }>(
      pipe(
        switchMap(({ id, changes }) => {
          return taskService.updateTask(id, changes).pipe(
            tapResponse({
              next: (task) =>
                patchState(
                  store,
                  updateEntity({ id, changes: task }, taskEntityConfig),
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

### 4. Create UI Component (Presentational)

`src/app/tasks/ui/task-item/task-item.ts`:

```typescript
import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
} from "@angular/core";
import { MatCardModule } from "@angular/material/card";
import { MatCheckboxModule } from "@angular/material/checkbox";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";

import { Task } from "../../data/models/task.model";

@Component({
  selector: "app-task-item",
  templateUrl: "./task-item.html",
  styleUrl: "./task-item.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatCardModule, MatCheckboxModule, MatIconModule, MatButtonModule],
})
export class TaskItem {
  readonly task = input.required<Task>();

  readonly toggle = output<boolean>();
  readonly delete = output<void>();
  readonly edit = output<void>();

  onToggle(completed: boolean): void {
    this.toggle.emit(completed);
  }

  onDelete(): void {
    this.delete.emit();
  }

  onEdit(): void {
    this.edit.emit();
  }
}
```

### 5. Create Feature Component (Container)

`src/app/tasks/feature/task-list/task-list.ts`:

```typescript
import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
} from "@angular/core";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";

import { TaskStore } from "../../data/state/task-store";
import { TaskItemComponent } from "../../ui/task-item/task-item";

@Component({
  selector: "app-task-list",
  templateUrl: "./task-list.html",
  styleUrl: "./task-list.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatProgressSpinnerModule, TaskItem],
})
export class TaskList implements OnInit {
  readonly taskStore = inject(TaskStore);

  ngOnInit(): void {
    this.taskStore.loadTasks();
  }

  onToggleTask(taskId: string, completed: boolean): void {
    this.taskStore.updateTask({ id: taskId, changes: { completed } });
  }

  onDeleteTask(taskId: string): void {
    this.taskStore.deleteTask(taskId);
  }
}
```

### 6. Create Routes

`src/app/tasks/feature/tasks.routes.ts`:

```typescript
import { Routes } from "@angular/router";

export const TASK_ROUTES: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./task-list/task-list").then((m) => m.TaskListComponent),
  },
  {
    path: ":id",
    loadComponent: () =>
      import("./task-detail/task-detail").then((m) => m.TaskDetailComponent),
  },
];
```

## Important Rules

1. **No Barrel Files**: Do NOT create `index.ts` files for re-exporting
2. **Component Subfolders**: Each component MUST be in its own subfolder
3. **Separation of Concerns**:
   - `feature/` = Container components (smart, connected to store)
   - `ui/` = Presentational components (dumb, input/output only)
   - `data/` = State, models, and API services
4. **Naming Conventions**:
   - Files: `kebab-case.ts` (e.g., `task-list.ts`) - no type suffix
   - Stores: `kebab-case-store.ts` (e.g., `task-store.ts`) - dash separator
   - Classes: `PascalCase` (e.g., `TaskListComponent`)
   - Models: `kebab-case.model.ts` (e.g., `task.model.ts`) - keep .model suffix

## Checklist for New Feature

- [ ] Domain model created in `data/models/`
- [ ] Infrastructure service created in `data/infrastructure/`
- [ ] Signal store created in `data/state/`
- [ ] UI components created in `ui/` (each in own subfolder)
- [ ] Feature components created in `feature/` (each in own subfolder)
- [ ] Routes defined with lazy loading
- [ ] All components using OnPush change detection
- [ ] Tests created for components, store, and service
- [ ] No barrel files (index.ts) created
