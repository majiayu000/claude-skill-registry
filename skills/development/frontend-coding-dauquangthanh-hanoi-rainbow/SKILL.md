---
name: frontend-coding
description: Expert frontend development guidance covering React, Vue, Angular, TypeScript, state management, component architecture, performance optimization, accessibility, testing, and modern web APIs. Produces production-ready, maintainable, and performant frontend code with best practices. Use when building web applications, implementing UI components, managing application state, optimizing performance, or when users mention React, Vue, Angular, TypeScript, hooks, state management, components, or frontend development.
---


# Frontend Coding

## Overview

Expert frontend development guidance covering React, Vue, Angular, TypeScript, state management, component architecture, performance optimization, accessibility, testing, and modern web APIs.

## Core Capabilities

1. **Framework Expertise** - React, Vue, Angular, Svelte
2. **TypeScript** - Type-safe development
3. **State Management** - Redux, Vuex, Pinia, Context API
4. **Component Patterns** - Composition, hooks, composables
5. **Performance** - Code splitting, lazy loading, optimization
6. **Accessibility** - WCAG compliance, ARIA
7. **Testing** - Jest, Testing Library, Cypress

## Quick Start

**React Component Example:**

```tsx
import React, { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
}

export const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

## Critical Tips

1. **Use TypeScript** - Type safety prevents runtime errors
2. **Component composition** - Build reusable, composable components
3. **Performance matters** - Memoization, lazy loading, code splitting
4. **Accessibility first** - WCAG compliance from the start
5. **Test thoroughly** - Unit, integration, E2E testing

## Framework-Specific Guidance

**React Development** - See [react-development.md](references/react-development.md) for:

- Functional components and hooks (useState, useEffect, useCallback, useMemo)
- Custom hooks and composition patterns
- Context API and prop drilling solutions
- React Server Components and Next.js

**React Advanced Patterns** - See [react-patterns.md](references/react-patterns.md) for:

- Custom hooks patterns (data fetching, form handling, debouncing)
- Higher-order components (HOC) and render props
- Compound components and controlled/uncontrolled patterns
- Error boundaries and suspense

**Vue.js Development** - See [vuejs-development.md](references/vuejs-development.md) for:

- Composition API and Options API
- Composables and reactivity system
- Vue Router, Pinia state management
- Nuxt.js and server-side rendering

**Vue Advanced Patterns** - See [vue-patterns.md](references/vue-patterns.md) for:

- Composables organization and reusability
- Provide/inject pattern and plugin development
- Custom directives and render functions
- Advanced reactivity patterns

## Cross-Framework Topics

**Component Patterns** - See [component-patterns.md](references/component-patterns.md) for:

- Compound components (tabs, accordions, modals)
- Render props and slots patterns
- Controlled vs uncontrolled components
- Container/presentational component separation

**State Management** - See [state-management.md](references/state-management.md) for:

- Redux, Zustand, Jotai (React)
- Pinia, Vuex (Vue)
- NgRx, Akita (Angular)
- Server state management (React Query, SWR, TanStack Query)

**TypeScript Best Practices** - See [typescript-best-practices.md](references/typescript-best-practices.md) for:

- Type safety, inference, and utility types
- Generics and advanced type patterns
- Type guards and narrowing
- Framework-specific TypeScript patterns

**Best Practices** - See [best-practices.md](references/best-practices.md) for:

- Project structure and code organization
- Naming conventions and file naming
- Testing strategies (unit, integration, E2E)
- Security best practices (XSS, CSRF, input validation)

**Performance & Accessibility** - See [performance-testing.md](references/performance-testing.md) for:

- Code splitting and lazy loading
- Bundle optimization and tree shaking
- Performance monitoring and profiling
- WCAG compliance and accessibility testing
