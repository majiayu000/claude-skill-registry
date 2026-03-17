---
name: react-core
description: Comprehensive React application development guidance covering project architecture, state management, performance optimization, security, and modern best practices including React 19 features. Use when (1) Working in React codebases (.jsx/.tsx files), (2) Architecting React applications (project structure, state management strategies), (3) Optimizing React performance (code splitting, memoization, virtualization), (4) Implementing security best practices (auth, XSS prevention, CSRF protection), (5) Applying React 19 features (Server Components, Actions, new hooks), (6) Setting up build configurations and tooling. Automatically triggered when working with React projects or addressing React-specific architecture, performance, or security concerns.
---

# React Core

Comprehensive guidance for building scalable, performant, and secure React applications with modern best practices.

## Quick Start

### New Project Setup

1. **Initialize with Vite:**
   ```bash
   pnpm create vite my-app --template react-ts
   cd my-app
   pnpm install
   ```

2. **Use configuration templates:**
   - Vite: [assets/config-templates/vite.config.ts](assets/config-templates/vite.config.ts)
   - Vitest: [assets/config-templates/vitest.config.ts](assets/config-templates/vitest.config.ts)
   - ESLint: [assets/config-templates/.eslintrc.react.json](assets/config-templates/.eslintrc.react.json)

3. **Install essential dependencies:**
   ```bash
   # Routing
   pnpm add react-router-dom

   # Data fetching
   pnpm add @tanstack/react-query

   # Forms
   pnpm add react-hook-form @hookform/resolvers zod

   # State management (if needed)
   pnpm add zustand
   ```

4. **Organize by feature:**
   See [project-structure.md](references/project-structure.md) for complete layouts

### Common Workflows

**Resolving Performance Issues:**
1. Check [performance.md](references/performance.md) for optimization techniques
2. Profile with React DevTools
3. Implement code splitting, virtualization, or memoization as needed

**Setting Up State Management:**
1. Review [state-management.md](references/state-management.md) decision framework
2. Choose appropriate solution (component state, Context, Zustand, React Query)
3. Implement following documented patterns

**Implementing Authentication:**
1. Follow security guidelines in [security.md](references/security.md)
2. Use HttpOnly cookies for tokens
3. Implement protected routes and authorization

## Project Architecture

### Project Structure

Organize code by feature, not by technical type:

```
src/
├── app/                   # App-level routing
├── features/             # Feature modules (self-contained)
│   ├── authentication/
│   ├── users/
│   └── dashboard/
├── components/           # Shared components
├── hooks/               # Shared hooks
├── lib/                 # Third-party setup
└── utils/               # Shared utilities
```

**Key principles:**
- Feature isolation with clear public APIs
- Unidirectional dependency flow (app → features → shared)
- Absolute imports via path aliases
- Consistent naming conventions

See [project-structure.md](references/project-structure.md) for complete guide including:
- Feature module organization
- Shared code structure
- Enforcing architectural boundaries with ESLint
- Monorepo considerations

### State Management

Choose the right state solution for each use case:

| State Type | Tool | Example |
|------------|------|---------|
| Component | useState, useReducer | Form inputs, toggles |
| Application | Context, Zustand, Jotai | Theme, auth status |
| Server Cache | React Query, SWR | API data |
| Form | React Hook Form | Form values, validation |
| URL | React Router | Filters, pagination |

**Decision framework:**
1. Server data? → Use React Query
2. Form data? → Use React Hook Form
3. Should be in URL? → Use useSearchParams
4. Shared across app? → Use Zustand/Context
5. Otherwise → Component state

See [state-management.md](references/state-management.md) for complete patterns including:
- useState vs useReducer
- Context optimization
- Zustand and Jotai examples
- React Query patterns
- State colocation best practices

## Performance

### Critical Optimizations

1. **Code Splitting** - Load code on demand
   ```tsx
   const Dashboard = lazy(() => import('./routes/Dashboard'));
   ```

2. **List Virtualization** - Render only visible items
   ```tsx
   import { useVirtualizer } from '@tanstack/react-virtual';
   ```

3. **Image Optimization** - Lazy load and use modern formats
   ```tsx
   <img src="/image.jpg" loading="lazy" />
   ```

4. **Bundle Optimization** - Analyze and reduce bundle size
   ```bash
   npx vite-bundle-visualizer
   ```

### React 19 Compiler

React 19's compiler automatically memoizes - remove manual `React.memo`, `useMemo`, `useCallback` when using the compiler.

See [performance.md](references/performance.md) for complete guide including:
- Component optimization (memoization)
- List virtualization with examples
- Web Vitals optimization
- Data prefetching strategies
- Performance monitoring tools

## API Layer

Structure API calls for maintainability and type safety:

```tsx
// features/users/api/get-user.ts
import { z } from 'zod';
import { useQuery } from '@tanstack/react-query';

const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

export type User = z.infer<typeof userSchema>;

export async function getUser(userId: string): Promise<User> {
  const response = await apiClient.get(`/users/${userId}`);
  return userSchema.parse(response.data);
}

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),
  });
}
```

See [api-layer.md](references/api-layer.md) for complete patterns including:
- API client setup (Axios/Fetch)
- Request organization
- Error handling
- TypeScript integration
- Authentication patterns

## Testing

Follow the testing pyramid:

```
     /\
    /E2E\      ← Few
   /------\
  /Integr.\   ← Some
 /----------\
/   Unit     \ ← Many
```

**Tools:**
- Vitest (test runner)
- React Testing Library (component testing)
- Playwright (E2E testing)
- MSW (API mocking)

**Example:**
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('button calls onClick when clicked', async () => {
  const handleClick = vi.fn();
  const user = userEvent.setup();

  render(<Button onClick={handleClick}>Click me</Button>);

  await user.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

See [testing.md](references/testing.md) for complete guide including:
- Component testing patterns
- Hook testing
- Integration tests
- MSW setup
- E2E with Playwright

## Security

### Key Security Practices

1. **Authentication** - Use HttpOnly cookies
2. **Authorization** - Implement RBAC/PBAC
3. **XSS Prevention** - Sanitize user content
4. **CSRF Protection** - Use SameSite cookies
5. **Input Validation** - Validate client and server-side

**Example:**
```tsx
// ✅ Secure token storage
// Server sets HttpOnly cookie
res.cookie('auth_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
});

// ✅ Sanitize user content
import DOMPurify from 'dompurify';
const sanitized = DOMPurify.sanitize(userContent);
```

See [security.md](references/security.md) for complete guide including:
- Token storage best practices
- Protected routes
- Role and permission-based access control
- XSS and CSRF prevention
- CSP configuration

## React 19 Features

### Major Improvements

1. **React Compiler** - Automatic memoization
2. **Server Components** - Render on server
3. **Actions** - Simplified form handling
4. **New Hooks** - use(), useFormStatus(), useOptimistic()
5. **Simplified refs** - No more forwardRef

**Example:**
```tsx
'use client';

import { useActionState } from 'react';

async function createUserAction(prevState, formData) {
  const user = await api.createUser(formData);
  return { success: true, user };
}

export function CreateUserForm() {
  const [state, formAction, isPending] = useActionState(createUserAction, null);

  return (
    <form action={formAction}>
      <input name="email" required />
      <button disabled={isPending}>
        {isPending ? 'Creating...' : 'Create'}
      </button>
    </form>
  );
}
```

See [react-19-best-practices.md](references/react-19-best-practices.md) for complete guide.

## Build & Tooling

### Vite Configuration

Optimized build setup with code splitting, minification, and tree shaking.

See [build-and-bundling.md](references/build-and-bundling.md) for:
- Complete Vite configuration
- Code splitting strategies
- Bundle analysis
- Production optimizations

### Essential Tools

See [ecosystem-tools.md](references/ecosystem-tools.md) for recommended packages:
- Routing (React Router, TanStack Router)
- Data fetching (React Query, SWR)
- Forms (React Hook Form)
- State (Zustand, Jotai)
- Styling (Tailwind, CSS Modules)
- UI Components (Radix UI, shadcn/ui)

## Common Pitfalls

Avoid these frequent mistakes:

1. **Stale closures** in useEffect
2. **Missing dependencies** in dependency arrays
3. **Unnecessary useEffect** for derived state
4. **Mutating state** directly
5. **Using index as key** in lists

See [common-pitfalls.md](references/common-pitfalls.md) for examples and solutions.

## TypeScript Integration

Type your React components properly:

```tsx
type ButtonProps = {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
};

export function Button({ children, variant = 'primary', onClick }: ButtonProps) {
  return <button className={variant} onClick={onClick}>{children}</button>;
}
```

See [typescript-react.md](references/typescript-react.md) for complete patterns including:
- Component typing
- Event handlers
- Hooks with TypeScript
- React Query types
- Utility types

## Reference Files

**Architecture & Organization:**
- [project-structure.md](references/project-structure.md) - Feature-based organization, imports, naming
- [state-management.md](references/state-management.md) - State categories, decision framework, patterns

**Performance & Optimization:**
- [performance.md](references/performance.md) - Code splitting, virtualization, Web Vitals
- [build-and-bundling.md](references/build-and-bundling.md) - Vite config, bundle optimization

**API & Data:**
- [api-layer.md](references/api-layer.md) - API client, request patterns, error handling

**Testing & Quality:**
- [testing.md](references/testing.md) - Component tests, integration tests, E2E
- [security.md](references/security.md) - Auth, authorization, XSS/CSRF prevention

**React 19 & Modern Features:**
- [react-19-best-practices.md](references/react-19-best-practices.md) - Compiler, Server Components, Actions

**Tools & Ecosystem:**
- [ecosystem-tools.md](references/ecosystem-tools.md) - Recommended packages by category
- [typescript-react.md](references/typescript-react.md) - TypeScript patterns for React

**Troubleshooting:**
- [common-pitfalls.md](references/common-pitfalls.md) - Frequent mistakes and solutions

## Configuration Templates

Pre-configured files for quick project setup:

- [vite.config.ts](assets/config-templates/vite.config.ts) - Optimized Vite configuration
- [vitest.config.ts](assets/config-templates/vitest.config.ts) - Testing setup
- [.eslintrc.react.json](assets/config-templates/.eslintrc.react.json) - React linting rules

## Best Practices Summary

1. **Organize by feature** - Keep related code together
2. **Choose state wisely** - Use React Query for server data
3. **Optimize strategically** - Profile before optimizing
4. **Test behavior** - Test what users see and do
5. **Secure by default** - HttpOnly cookies, sanitize input
6. **Type everything** - Leverage TypeScript fully
7. **Stay modern** - Adopt React 19 features
8. **Keep it simple** - Avoid premature optimization

Build React applications that are fast, secure, and maintainable.
