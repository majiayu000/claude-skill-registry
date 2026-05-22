---
name: agent-frontend
description: Angular 21+ expert for .ts .html .css files, @Component, UI, components, pages, services, routing, forms, templates, signals, RxJS, HttpClient, inject(), reactive forms, validators, accessibility, WCAG, AXE, browser testing, Karma, Jasmine, e2e, Playwright
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Development Skill

Expert in Angular 21+ frontend development following project conventions.

## When to Use This Skill

Use this skill when:

- Implementing UI components or pages
- Creating or modifying Angular services
- Working with forms and validation
- Implementing routing or guards
- Any frontend-related task

## Core Principles

### Angular 21+ Patterns

- **Standalone components only** (no NgModules)
- **Signals for state** (`signal()`, `computed()`)
- **OnPush change detection** (always)
- **inject() for DI** (not constructor injection)
- **Native control flow** (`@if`, `@for`, `@switch`)
- **input()/output() functions** (not decorators)

### Naming Conventions

- **camelCase everywhere** - variables, properties, all naming
- **NEVER use snake_case**

## Mandatory Local Testing (CRITICAL)

**BEFORE EVERY PUSH, run ALL checks from apps/frontend:**

```bash
cd apps/frontend

# 1. Lint check
npm run lint

# 2. Format check
npm run format:check

# 3. Tests
npm run test:ci

# 4. Build
npm run build
```

**If ANY check fails:**

1. STOP - Do not proceed
2. Fix the issue
3. Re-run ALL checks
4. Only push when ALL pass

**Why:** CI feedback loop takes 3-5 minutes vs local checks in <1 minute. Debugging locally is 10x faster.

## Component Guidelines

### Component Size Management

- **Small components (<50 lines template):** Inline templates OK
- **All components:** CSS in separate files (NEVER inline styles)
- **Large components (>200 lines):** Break into smaller components
- **Large controllers (>100 lines):** Extract utility functions

### TypeScript Best Practices

- **NEVER use `any`** - use `unknown` instead
- Prefer type inference when obvious
- Use proper generics for type safety
- Leverage TypeScript utility types (Partial, Required, Pick, Omit)

## Templates

### Control Flow

```typescript
// ✅ CORRECT - Native control flow
@if (user()) {
  <p>Welcome {{user().name}}</p>
}

@for (item of items(); track item.id) {
  <div>{{item.name}}</div>
}

// ❌ WRONG - Old structural directives
*ngIf="user"
*ngFor="let item of items"
```

### Class Bindings

```html
<!-- ✅ CORRECT -->
<div [class.active]="isActive()">
  <!-- ❌ WRONG -->
  <div [ngClass]="{'active': isActive()}"></div>
</div>
```

## State Management

**⚠️ CRITICAL - Read Before Implementing**:

### Shared State (Multi-Component)

If data is needed across multiple pages/components:

- **MUST use centralized store** (NgRx SignalStore or custom signal-based store)
- **NEVER duplicate API calls** across components
- Examples: household, user, tasks, assignments

### Local Component State

```typescript
// Simple local state with signals
export class MyComponent {
  // Local state
  private count = signal(0);

  // Derived state
  doubleCount = computed(() => this.count() * 2);

  // Update state
  increment() {
    this.count.update((c) => c + 1);
    // Or: this.count.set(5);
  }
}
```

### Async Data Loading

**Use AsyncState utility instead of manual loading/error/data signals**:

```typescript
import { AsyncState } from '../utils/async-state';

export class MyComponent {
  protected readonly dataState = new AsyncState<Data[]>();

  async loadData(): Promise<void> {
    await this.dataState.execute(async () => {
      return this.dataService.getData();
    });
  }
}
```

**Benefits**: Eliminates 15+ lines of boilerplate, type-safe, consistent

### localStorage

**NEVER use localStorage directly** - use StorageService:

```typescript
// ❌ WRONG
localStorage.setItem('key', JSON.stringify(value));

// ✅ CORRECT
this.storageService.set('key', value);
```

**See**: GitHub Issues #255 (State), #258 (AsyncState), #259 (Storage)

## Services

```typescript
// Use inject() instead of constructor injection
export class MyService {
  private http = inject(HttpClient);
  private router = inject(Router);

  getData() {
    return this.http.get('/api/data');
  }
}
```

## Accessibility (WCAG AA Compliance)

- All implementations MUST pass AXE checks
- Implement proper focus management
- Ensure sufficient color contrast
- Add appropriate ARIA attributes
- Support keyboard navigation

## Workflow

1. **Read** the optimized agent spec: `.claude/agents/agent-frontend.md`
2. **Understand** requirements and acceptance criteria
3. **Research** existing patterns in the codebase
4. **Implement** following all conventions above
5. **Test** locally with ALL checks (lint, format, tests, build)
6. **Only then** commit and push

## Common Patterns

### Creating Components

```bash
# Always use Angular CLI
ng generate component my-component
# Or shorthand:
ng g c my-component
```

### API Integration

```typescript
export class DataService {
  private api = inject(ApiService);

  async fetchData(): Promise<Data[]> {
    return this.api.get<Data[]>('/api/data');
  }
}
```

### Forms

```typescript
export class FormComponent {
  form = new FormGroup({
    name: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
  });

  onSubmit() {
    if (this.form.invalid) return;
    // Process form
  }
}
```

## Reference Files

For detailed patterns and examples:

- `.github/agents/frontend-agent.md` - Complete agent specification with architectural improvements
- `CLAUDE.md` - Project-wide conventions

**Specialized Skills** (use these for specific patterns):

- `.claude/skills/state-management/` - Centralized stores, AsyncState, localStorage abstraction
- `.claude/skills/http-interceptors/` - Auth, error handling, retry logic, caching
- `.claude/skills/testing-infrastructure/` - Fixtures, mocks, component harness
- `.claude/skills/storybook/` - Component development and visual testing

**Architecture Improvement Issues** (reference these for best practices):

- #253: Routing Architecture (layout components)
- #254: Performance Optimizations (pagination, virtual scrolling, caching)
- #255: State Management (centralized store)
- #256: Service Layer Boundaries (single responsibility)
- #257: HTTP Layer Improvements (interceptors)
- #258: Eliminate Code Duplication (AsyncState utility)
- #259: Abstract localStorage (StorageService)
- #260: Component Organization (presentational vs container)
- #261: Testing Infrastructure (shared utilities)

## Success Criteria

Before marking work complete:

- [ ] All local checks pass (lint, format, tests, build)
- [ ] Accessibility verified with AXE
- [ ] Follows Angular 21+ patterns
- [ ] Uses signals for state management
- [ ] camelCase naming throughout
- [ ] No `any` types used
