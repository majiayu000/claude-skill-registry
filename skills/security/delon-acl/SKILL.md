---
name: delon-acl
description: '@delon/acl skill - Access Control List for role-based permissions and UI element visibility. For ng-events construction site progress tracking system.'
---

# @delon/acl - Access Control List

Trigger patterns: "ACL", "permission", "role", "access control", "@delon/acl", "can", "ability"

## Overview

@delon/acl provides a role-based access control (RBAC) system for ng-alain applications, controlling UI element visibility and feature access based on user roles and permissions.

**Package**: @delon/acl@20.1.0  
**Integrated with**: @delon/auth for authentication

## Core Concepts

### 1. ACLService - Permission Management

```typescript
import { inject } from '@angular/core';
import { ACLService } from '@delon/acl';

@Component({
  selector: 'app-dashboard',
  standalone: true
})
export class DashboardComponent {
  private aclService = inject(ACLService);
  
  ngOnInit(): void {
    // Set user roles and permissions
    this.aclService.setRole(['admin', 'user']);
    this.aclService.setAbility(['task:create', 'task:edit', 'task:delete']);
    
    // Set full ACL configuration
    this.aclService.set({
      role: ['admin'],
      ability: ['task:create', 'task:edit'],
      mode: 'oneOf' // 'allOf' or 'oneOf'
    });
  }
  
  canEditTask(): boolean {
    return this.aclService.can('task:edit');
  }
  
  isAdmin(): boolean {
    return this.aclService.can({ role: ['admin'] });
  }
}
```

### 2. ACL Directives - Conditional UI

#### *aclIf Directive

```typescript
import { ACLIfDirective } from '@delon/acl';

@Component({
  imports: [ACLIfDirective],
  template: `
    <!-- Show only if user has admin role -->
    <button *aclIf="'admin'" nz-button nzType="primary">
      管理設定
    </button>
    
    <!-- Show only if user has task:create ability -->
    <button *aclIf="'task:create'" nz-button>
      建立任務
    </button>
    
    <!-- Complex condition: admin OR task:delete permission -->
    <button *aclIf="deletePermission" nz-button nzDanger>
      刪除
    </button>
  `
})
export class TaskListComponent {
  deletePermission = {
    role: ['admin'],
    ability: ['task:delete'],
    mode: 'oneOf'
  };
}
```

#### ACL with @if (Angular 20)

```typescript
@Component({
  template: `
    @if (canCreate()) {
      <button nz-button (click)="createTask()">
        建立任務
      </button>
    }
    
    @if (isAdmin()) {
      <nz-card>
        <h3>管理員面板</h3>
        <!-- admin-only content -->
      </nz-card>
    }
  `
})
export class DashboardComponent {
  private aclService = inject(ACLService);
  
  canCreate = signal(this.aclService.can('task:create'));
  isAdmin = signal(this.aclService.can({ role: ['admin'] }));
}
```

### 3. ACL Guards - Route Protection

```typescript
import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { ACLService } from '@delon/acl';
import { Router } from '@angular/router';

// Role-based guard
export const adminGuard: CanActivateFn = () => {
  const aclService = inject(ACLService);
  const router = inject(Router);
  
  if (aclService.can({ role: ['admin'] })) {
    return true;
  }
  
  return router.parseUrl('/403');
};

// Ability-based guard
export const taskCreateGuard: CanActivateFn = () => {
  const aclService = inject(ACLService);
  const router = inject(Router);
  
  if (aclService.can('task:create')) {
    return true;
  }
  
  return router.parseUrl('/403');
};

// Complex permission guard
export const blueprintEditGuard: CanActivateFn = () => {
  const aclService = inject(ACLService);
  const router = inject(Router);
  
  const canEdit = aclService.can({
    role: ['admin', 'owner'],
    ability: ['blueprint:edit'],
    mode: 'oneOf'
  });
  
  return canEdit || router.parseUrl('/403');
};
```

**Route Configuration**:
```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'admin',
    canActivate: [adminGuard],
    loadComponent: () => import('./admin/admin.component')
  },
  {
    path: 'tasks/create',
    canActivate: [taskCreateGuard],
    loadComponent: () => import('./tasks/create.component')
  },
  {
    path: 'blueprints/:id/edit',
    canActivate: [blueprintEditGuard],
    loadComponent: () => import('./blueprints/edit.component')
  }
];
```

## Real-World Blueprint Integration

### Permission Structure for ng-events(GigHub)

```typescript
import { Injectable, inject } from '@angular/core';
import { ACLService } from '@delon/acl';
import { AuthService } from '@core/services/auth.service';
import { BlueprintMemberRepository } from '@core/data-access/blueprint-member.repository';

/**
 * ng-events(GigHub) permission format:
 * - Roles: 'owner', 'admin', 'member', 'viewer'
 * - Abilities: 'module:action' format
 *   Examples: 'task:create', 'task:edit', 'task:delete'
 *             'blueprint:edit', 'member:invite'
 */
@Injectable({ providedIn: 'root' })
export class PermissionService {
  private aclService = inject(ACLService);
  private authService = inject(AuthService);
  private memberRepo = inject(BlueprintMemberRepository);
  
  /**
   * Initialize permissions for a blueprint
   */
  async initBlueprintPermissions(blueprintId: string): Promise<void> {
    const userId = this.authService.currentUserId();
    if (!userId) {
      this.aclService.set({ role: [], ability: [] });
      return;
    }
    
    // Get user's membership
    const member = await this.memberRepo.findByUserAndBlueprint(
      userId,
      blueprintId
    );
    
    if (!member || member.status !== 'active') {
      this.aclService.set({ role: [], ability: [] });
      return;
    }
    
    // Set roles and permissions
    this.aclService.set({
      role: [member.role],
      ability: member.permissions || [],
      mode: 'oneOf'
    });
  }
  
  /**
   * Check if user can perform action
   */
  can(ability: string): boolean {
    return this.aclService.can(ability);
  }
  
  /**
   * Check if user has role
   */
  hasRole(role: string | string[]): boolean {
    return this.aclService.can({ role: Array.isArray(role) ? role : [role] });
  }
  
  /**
   * Check if user can edit task
   */
  canEditTask(task: Task): boolean {
    // Owner or admin can always edit
    if (this.hasRole(['owner', 'admin'])) {
      return true;
    }
    
    // Member can edit if they have permission AND are assigned
    return this.can('task:edit') && 
           task.assignedTo === this.authService.currentUserId();
  }
  
  /**
   * Check if user can delete task
   */
  canDeleteTask(): boolean {
    return this.hasRole(['owner', 'admin']) || this.can('task:delete');
  }
}
```

### Component with Blueprint Permissions

```typescript
import { Component, signal, computed, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PermissionService } from '@core/services/permission.service';
import { TaskService } from '@core/services/task.service';
import { ACLIfDirective } from '@delon/acl';

@Component({
  selector: 'app-task-detail',
  standalone: true,
  imports: [ACLIfDirective],
  template: `
    <nz-card>
      <h2>{{ task()?.title }}</h2>
      
      <!-- Show edit button if user can edit -->
      @if (canEdit()) {
        <button nz-button (click)="editTask()">
          編輯任務
        </button>
      }
      
      <!-- Show delete button if user can delete -->
      @if (canDelete()) {
        <button nz-button nzDanger (click)="deleteTask()">
          刪除任務
        </button>
      }
      
      <!-- Alternative: Using *aclIf directive -->
      <button *aclIf="'task:edit'" nz-button>
        編輯
      </button>
      
      <!-- Show admin panel if user is owner/admin -->
      @if (isOwnerOrAdmin()) {
        <nz-card>
          <h3>管理面板</h3>
          <!-- admin features -->
        </nz-card>
      }
    </nz-card>
  `
})
export class TaskDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private taskService = inject(TaskService);
  private permissionService = inject(PermissionService);
  
  task = signal<Task | null>(null);
  
  canEdit = computed(() => {
    const t = this.task();
    return t ? this.permissionService.canEditTask(t) : false;
  });
  
  canDelete = computed(() => 
    this.permissionService.canDeleteTask()
  );
  
  isOwnerOrAdmin = computed(() => 
    this.permissionService.hasRole(['owner', 'admin'])
  );
  
  async ngOnInit(): Promise<void> {
    const taskId = this.route.snapshot.params['id'];
    const blueprintId = this.route.snapshot.params['blueprintId'];
    
    // Initialize permissions for this blueprint
    await this.permissionService.initBlueprintPermissions(blueprintId);
    
    // Load task
    const task = await this.taskService.getTask(taskId);
    this.task.set(task);
  }
  
  editTask(): void {
    // Implementation
  }
  
  deleteTask(): void {
    // Implementation
  }
}
```

## Best Practices

### 1. Initialize ACL Early

✅ **DO**: Initialize in app initialization or route resolver
```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    {
      provide: APP_INITIALIZER,
      useFactory: (acl: ACLService, auth: AuthService) => () => {
        // Initialize ACL after auth
        return auth.getCurrentUser().then(user => {
          if (user) {
            acl.set({
              role: [user.role],
              ability: user.permissions
            });
          }
        });
      },
      deps: [ACLService, AuthService],
      multi: true
    }
  ]
};
```

### 2. Use Signals with ACL

✅ **DO**: Create reactive permission checks
```typescript
canCreate = computed(() => this.aclService.can('task:create'));
isAdmin = computed(() => this.aclService.can({ role: ['admin'] }));
```

### 3. Combine with Security Rules

✅ **DO**: Use ACL for UI + Firestore Security Rules for data
```typescript
// UI: Hide button if no permission
@if (permissionService.can('task:delete')) {
  <button (click)="delete()">刪除</button>
}

// Firestore Security Rules: Enforce permission
match /tasks/{taskId} {
  allow delete: if isBlueprintMember(resource.data.blueprintId) 
                && hasPermission(resource.data.blueprintId, 'task:delete');
}
```

## Integration Checklist

- [ ] Install @delon/acl@20.1.0
- [ ] Initialize ACL in APP_INITIALIZER
- [ ] Define role and permission structure
- [ ] Integrate with @delon/auth
- [ ] Create route guards for protected routes
- [ ] Use *aclIf or @if with can() for UI
- [ ] Combine with Firestore Security Rules
- [ ] Test permission edge cases

## Anti-Patterns

❌ **Hardcoding Permissions in Components**:
```typescript
if (user.role === 'admin') { /* ... */ }
```

✅ **Use ACL Service**:
```typescript
if (this.aclService.can({ role: ['admin'] })) { /* ... */ }
```

---

❌ **Only Client-Side Permission Checks**:
```typescript
// UI only - insecure!
@if (canDelete()) { <button (click)="delete()">刪除</button> }
```

✅ **Client + Server Validation**:
```typescript
// UI check
@if (canDelete()) { <button (click)="delete()">刪除</button> }

// Firestore Security Rules
allow delete: if hasPermission('task:delete');
```

## Cross-References

- **delon-auth** - Authentication integration
- **firestore-security-rules** - Server-side validation
- **blueprint-integration** - Multi-tenant permissions
- `.github/instructions/ng-ng-events(GigHub)-architecture.instructions.md` - Permission architecture

---

**Version**: 1.0  
**Created**: 2025-12-25  
**Maintainer**: ng-events(GigHub) Development Team
