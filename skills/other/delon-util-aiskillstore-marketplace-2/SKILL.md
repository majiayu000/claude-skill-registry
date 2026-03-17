---
name: delon-util
description: '@delon/util skill - Utility functions library for array, string, date, number manipulation. For ng-events construction site progress tracking system.'
---

# @delon/util - Utility Functions Library

Trigger patterns: "utility", "helper", "@delon/util", "format", "deepCopy", "deepMerge"

## Overview

@delon/util provides a comprehensive collection of utility functions for common data manipulation tasks in ng-alain applications.

**Package**: @delon/util@20.1.0

## Categories

### 1. Array Utilities (`array/`)

#### deepCopy - Deep Copy Arrays/Objects

```typescript
import { deepCopy } from '@delon/util/array';

const original = { name: '任務', items: [1, 2, 3], meta: { id: 1 } };
const copy = deepCopy(original);

// Changes to copy won't affect original
copy.items.push(4);
console.log(original.items); // [1, 2, 3]
console.log(copy.items);     // [1, 2, 3, 4]
```

**Use Cases**:
- Clone state objects for immutability
- Create independent copies before mutations
- Deep cloning form data

#### deepMerge - Deep Merge Objects

```typescript
import { deepMerge } from '@delon/util/array';

const defaults = {
  config: { theme: 'light', size: 'default' },
  features: ['dashboard']
};

const custom = {
  config: { theme: 'dark' },
  features: ['reports']
};

const merged = deepMerge(defaults, custom);
// Result: {
//   config: { theme: 'dark', size: 'default' },
//   features: ['dashboard', 'reports']
// }
```

#### Other Array Functions

```typescript
import { 
  groupBy,     // Group array by property
  uniq,        // Remove duplicates
  uniqBy,      // Remove duplicates by property
  orderBy      // Sort array by properties
} from '@delon/util/array';

// Group tasks by status
const grouped = groupBy(tasks, 'status');
// { pending: [...], completed: [...] }

// Remove duplicate IDs
const uniqueIds = uniq([1, 2, 2, 3]); // [1, 2, 3]

// Remove duplicate tasks by ID
const uniqueTasks = uniqBy(tasks, 'id');

// Sort tasks
const sorted = orderBy(tasks, ['priority', 'createdAt'], ['asc', 'desc']);
```

### 2. String Utilities (`string/`)

#### format - String Formatting

```typescript
import { format } from '@delon/util/string';

// Template interpolation
const message = format('任務 {0} 已指派給 {1}', taskName, userName);

// Named parameters
const message2 = format('任務 {name} 的狀態為 {status}', { 
  name: '地基施工', 
  status: '進行中' 
});
```

#### Other String Functions

```typescript
import { 
  toCamelCase,    // Convert to camelCase
  toPascalCase,   // Convert to PascalCase
  toKebabCase,    // Convert to kebab-case
  toSnakeCase,    // Convert to snake_case
  truncate        // Truncate with ellipsis
} from '@delon/util/string';

toCamelCase('task-name');     // 'taskName'
toPascalCase('task-name');    // 'TaskName'
toKebabCase('TaskName');      // 'task-name'
toSnakeCase('TaskName');      // 'task_name'
truncate('Long text...', 10); // 'Long te...'
```

### 3. Date Utilities (`date/`)

#### getTimeDistance - Get Time Ranges

```typescript
import { getTimeDistance } from '@delon/util/date';

// Get today's date range
const today = getTimeDistance('today');
// [Date(2024-12-25 00:00:00), Date(2024-12-25 23:59:59)]

// Get this week's date range
const week = getTimeDistance('week');

// Get this month's date range
const month = getTimeDistance('month');

// Get this year's date range
const year = getTimeDistance('year');

// Custom range with offset
const lastWeek = getTimeDistance('week', -1);
```

**Supported Types**:
- `'today'` - Current day
- `'week'` - Current week (Sunday to Saturday)
- `'month'` - Current month
- `'year'` - Current year
- Custom offset (negative for past, positive for future)

#### formatDistanceToNow - Relative Time

```typescript
import { formatDistanceToNow } from '@delon/util/date';

const createdAt = new Date('2024-12-20');
const relative = formatDistanceToNow(createdAt);
// "5 days ago"

const futureDate = new Date('2024-12-30');
const future = formatDistanceToNow(futureDate);
// "in 5 days"
```

### 4. Number Utilities (`number/`)

#### currency - Currency Formatting

```typescript
import { currency } from '@delon/util/number';

// Format as currency
currency(1234567.89);              // "$1,234,567.89"
currency(1234567.89, { unit: '¥' }); // "¥1,234,567.89"
currency(1234.5, { precision: 0 });  // "$1,235"
```

#### Other Number Functions

```typescript
import { 
  toFixed,      // Round to fixed decimals
  toPercent,    // Convert to percentage
  toThousands   // Add thousands separators
} from '@delon/util/number';

toFixed(1.2345, 2);           // "1.23"
toPercent(0.1234);            // "12.34%"
toPercent(0.1234, 1);         // "12.3%"
toThousands(1234567);         // "1,234,567"
```

### 5. Browser Utilities (`browser/`)

#### copyToClipboard - Copy to Clipboard

```typescript
import { copy } from '@delon/util/browser';

async copyTaskLink(taskId: string) {
  const link = `${window.location.origin}/tasks/${taskId}`;
  const success = await copy(link);
  
  if (success) {
    this.messageService.success('連結已複製');
  } else {
    this.messageService.error('複製失敗');
  }
}
```

#### Other Browser Functions

```typescript
import { 
  scrollToTop,    // Smooth scroll to top
  deepGet,        // Get nested object property
  deepSet,        // Set nested object property
  isEmpty,        // Check if value is empty
  isEqual,        // Deep equality check
  updateHostClass // Update host element classes
} from '@delon/util/browser';

scrollToTop();
scrollToTop({ duration: 500 });

const value = deepGet(obj, 'user.profile.name');
deepSet(obj, 'user.profile.name', 'New Name');

isEmpty(null);      // true
isEmpty('');        // true
isEmpty([]);        // true
isEmpty({});        // true

isEqual({ a: 1 }, { a: 1 }); // true
```

## Real-World Examples

### Task Management Utilities

```typescript
import { Component, signal, computed, inject } from '@angular/core';
import { deepCopy, groupBy, orderBy } from '@delon/util/array';
import { format } from '@delon/util/string';
import { getTimeDistance } from '@delon/util/date';
import { copy } from '@delon/util/browser';
import { NzMessageService } from 'ng-zorro-antd/message';

@Component({
  selector: 'app-task-list',
  standalone: true,
  template: `
    <nz-card>
      <div nz-row [nzGutter]="16">
        @for (group of groupedTasks() | keyvalue; track group.key) {
          <div nz-col [nzSpan]="8">
            <h3>{{ group.key }} ({{ group.value.length }})</h3>
            @for (task of group.value; track task.id) {
              <nz-card>
                <h4>{{ task.title }}</h4>
                <p>{{ formatTaskInfo(task) }}</p>
                <button nz-button (click)="copyTaskLink(task.id)">
                  複製連結
                </button>
              </nz-card>
            }
          </div>
        }
      </div>
    </nz-card>
  `
})
export class TaskListComponent {
  private messageService = inject(NzMessageService);
  
  // Original tasks from service
  tasks = signal<Task[]>([]);
  
  // Group tasks by status using @delon/util
  groupedTasks = computed(() => 
    groupBy(this.sortedTasks(), 'status')
  );
  
  // Sort tasks by priority and date
  sortedTasks = computed(() => 
    orderBy(
      this.tasks(),
      ['priority', 'createdAt'],
      ['asc', 'desc']
    )
  );
  
  // Format task information
  formatTaskInfo(task: Task): string {
    return format(
      '優先級: {priority}, 建立於 {date}',
      {
        priority: task.priority,
        date: this.formatDate(task.createdAt)
      }
    );
  }
  
  // Copy task link to clipboard
  async copyTaskLink(taskId: string): Promise<void> {
    const link = `${window.location.origin}/tasks/${taskId}`;
    const success = await copy(link);
    
    if (success) {
      this.messageService.success('任務連結已複製');
    } else {
      this.messageService.error('複製失敗，請手動複製');
    }
  }
  
  // Clone task for editing
  cloneTaskForEdit(task: Task): Task {
    return deepCopy(task);
  }
  
  // Get this week's tasks
  getThisWeekTasks(): Task[] {
    const [start, end] = getTimeDistance('week');
    return this.tasks().filter(t => 
      t.createdAt >= start && t.createdAt <= end
    );
  }
  
  private formatDate(date: Date): string {
    return format(
      '{year}-{month}-{day}',
      {
        year: date.getFullYear(),
        month: String(date.getMonth() + 1).padStart(2, '0'),
        day: String(date.getDate()).padStart(2, '0')
      }
    );
  }
}
```

### Form Data Utilities

```typescript
import { Component, signal } from '@angular/core';
import { deepCopy, deepMerge } from '@delon/util/array';
import { isEmpty } from '@delon/util/browser';

@Component({
  selector: 'app-task-form',
  standalone: true,
  template: `
    <form nz-form (ngSubmit)="handleSubmit()">
      <!-- form fields -->
      <button nz-button [disabled]="hasEmptyRequired()">
        提交
      </button>
    </form>
  `
})
export class TaskFormComponent {
  // Default form values
  private defaults = {
    priority: 'medium',
    status: 'pending',
    assignee: null,
    tags: []
  };
  
  // Form data with defaults
  formData = signal(deepCopy(this.defaults));
  
  // Original task (for editing)
  originalTask = signal<Task | null>(null);
  
  // Load task for editing
  loadTask(task: Task): void {
    // Merge task data with defaults
    const merged = deepMerge(this.defaults, task);
    this.formData.set(merged);
    this.originalTask.set(deepCopy(task));
  }
  
  // Check if required fields are empty
  hasEmptyRequired(): boolean {
    const data = this.formData();
    return isEmpty(data.title) || isEmpty(data.assignee);
  }
  
  // Check if form has changes
  hasChanges(): boolean {
    const original = this.originalTask();
    if (!original) return true;
    
    return !isEqual(original, this.formData());
  }
  
  handleSubmit(): void {
    if (!this.hasEmptyRequired()) {
      // Create clean copy for submission
      const submitData = deepCopy(this.formData());
      // Submit...
    }
  }
}
```

## Best Practices

### 1. Use Utilities for Immutability

✅ **DO**:
```typescript
const taskCopy = deepCopy(task);
taskCopy.status = 'completed';
this.tasks.update(tasks => [...tasks, taskCopy]);
```

❌ **DON'T**:
```typescript
task.status = 'completed';
this.tasks.update(tasks => [...tasks, task]); // Mutates original
```

### 2. Leverage Computed Signals with Utilities

✅ **DO**:
```typescript
groupedTasks = computed(() => groupBy(this.tasks(), 'status'));
sortedTasks = computed(() => orderBy(this.tasks(), ['priority'], ['asc']));
```

### 3. Use Type-Safe Utilities

✅ **DO**:
```typescript
import { deepCopy } from '@delon/util/array';

const copy: Task = deepCopy<Task>(originalTask);
```

## Performance Considerations

1. **deepCopy**: Expensive for large objects - use sparingly
2. **groupBy/orderBy**: Wrap in computed() to avoid recalculation
3. **getTimeDistance**: Cache results if used frequently
4. **copy**: Async operation - handle loading states

## Integration Checklist

- [ ] Install @delon/util@20.1.0
- [ ] Import specific utilities (tree-shaking friendly)
- [ ] Use with Angular Signals for reactivity
- [ ] Add TypeScript generics for type safety
- [ ] Handle async operations (copy)
- [ ] Test edge cases (null, undefined, empty)

## Cross-References

- **angular-component** - Signals integration
- **delon-form** - Form utilities for validation
- **firebase-repository** - deepCopy for state management

---

**Version**: 1.0  
**Created**: 2025-12-25  
**Maintainer**: ng-events(GigHub) Development Team
