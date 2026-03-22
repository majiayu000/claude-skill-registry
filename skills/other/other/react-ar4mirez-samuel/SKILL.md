---
name: react
description: |
  React 18+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with React projects (.jsx/.tsx files), or when the user mentions React.
  Provides component patterns, hooks, state management, testing, and performance guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: typescript
  extensions: ".jsx,.tsx"
---

# React Guide

> Applies to: React 18+, TypeScript, Single Page Applications, Component Libraries, Web Apps

## Core Principles

1. **Component-Based**: Build encapsulated components that manage their own state
2. **Declarative**: Describe what UI should look like, React handles DOM updates
3. **Unidirectional Data Flow**: Props down, callbacks up
4. **Composition Over Inheritance**: Prefer component composition and custom hooks
5. **TypeScript First**: All components use TypeScript with strict prop interfaces

## Guardrails

### Component Rules

- Use functional components exclusively (no class components)
- Keep components under 200 lines (split into smaller components)
- Every component has a TypeScript interface for props
- Use `React.ReactNode` for children props, not `JSX.Element`
- Implement error boundaries for graceful error handling
- Use proper accessibility attributes (ARIA roles, labels, keyboard navigation)
- Co-locate component, styles, and tests in the same directory

### Hooks Rules

- Only call hooks at the top level (never inside conditions, loops, or nested functions)
- Only call hooks from React function components or custom hooks
- Name custom hooks with `use` prefix: `useAuth`, `useQuery`, `useFetch`
- Always include all dependencies in `useEffect` / `useMemo` / `useCallback` arrays
- Clean up side effects in `useEffect` return function
- Prefer `useReducer` over `useState` for complex state logic
- Use ESLint `react-hooks` plugin to enforce rules

### State Management

- Local state: `useState` for simple, `useReducer` for complex
- Shared state: Context API for low-frequency updates (theme, auth, locale)
- Server state: TanStack Query (React Query) for data fetching and caching
- Global client state: Zustand for complex cross-component state
- Avoid prop drilling beyond 2 levels (use composition or context)
- Never store derived state (compute it during render)

### Performance

- Use `React.memo()` only for expensive pure components (measure first)
- Use `useMemo` for expensive computations, `useCallback` for stable references
- Lazy load routes and heavy components with `React.lazy()` + `Suspense`
- Virtualize long lists (react-window, @tanstack/virtual)
- Keep bundle under 200KB initial load (code-split aggressively)
- Avoid anonymous functions in JSX for frequently re-rendered components

### File Naming

- Components: `PascalCase.tsx` (e.g., `UserCard.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useAuth.ts`)
- Utils: `camelCase.ts` (e.g., `formatDate.ts`)
- Types: `camelCase.ts` or `types.ts` per feature
- Tests: `*.test.tsx` or `*.spec.tsx` (co-located)
- Styles: `*.module.css` or `*.styles.ts` (co-located)

## Project Structure

```
my-app/
├── public/
│   └── index.html
├── src/
│   ├── assets/              # Static assets (images, fonts)
│   ├── components/          # Reusable components
│   │   ├── ui/             # Base UI components (Button, Input, Modal)
│   │   └── features/       # Feature-specific components
│   ├── hooks/              # Custom hooks
│   ├── contexts/           # React contexts
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript types
│   ├── pages/              # Page components (route-level)
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── tests/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

- `components/ui/` for reusable design system primitives
- `components/features/` for domain-specific compositions
- `hooks/` for shared custom hooks (feature-specific hooks co-locate with component)
- `contexts/` for React context providers
- `services/` for API layer (fetch wrappers, API clients)
- `pages/` for route-level components only

## Component Patterns

### Functional Component with Props

```tsx
interface UserCardProps {
  userId: string;
  onSelect?: (user: User) => void;
  className?: string;
}

export function UserCard({ userId, onSelect, className }: UserCardProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await userService.getById(userId);
        setUser(data);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [userId]);

  if (loading) return <Skeleton />;
  if (!user) return null;

  return (
    <div className={cn('user-card', className)} onClick={() => onSelect?.(user)}>
      <Avatar src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

### Component with Children

```tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function Card({ title, children, footer }: CardProps) {
  return (
    <div className="card">
      <div className="card-header"><h2>{title}</h2></div>
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}
```

## State Management Patterns

### Context API (Auth, Theme, Locale)

```tsx
interface AuthContextValue {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: LoginCredentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

### TanStack Query (Server State)

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => userService.getAll(),
    staleTime: 5 * 60 * 1000,
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateUserDTO) => userService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Zustand (Complex Client State)

```tsx
import { create } from 'zustand';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  total: () => number;
}

const useCartStore = create<CartStore>()((set, get) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter((item) => item.id !== id),
  })),
  clearCart: () => set({ items: [] }),
  total: () => get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),
}));
```

## Routing (React Router v6)

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'settings', element: <Settings /> },
      { path: '*', element: <NotFound /> },
    ],
  },
]);

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
```

## Forms (React Hook Form + Zod)

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(2, 'Name is required'),
});

type UserFormData = z.infer<typeof userSchema>;

function UserForm({ onSubmit }: { onSubmit: (data: UserFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<UserFormData>({ resolver: zodResolver(userSchema) });

  const handleFormSubmit = async (data: UserFormData) => {
    await onSubmit(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Testing Overview

### Standards

- Use React Testing Library (`@testing-library/react`) for component tests
- Use `userEvent` over `fireEvent` for realistic user interactions
- Test behavior, not implementation details
- Query by accessible roles and labels first (not test IDs)
- Mock API calls, not internal component state
- Coverage target: >80% for business logic components

### Basic Component Test

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('UserCard', () => {
  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', async () => {
    const onSelect = vi.fn();
    render(<UserCard user={mockUser} onSelect={onSelect} />);
    await userEvent.click(screen.getByRole('button'));
    expect(onSelect).toHaveBeenCalledWith(mockUser);
  });
});
```

## Tooling

### Essential Commands

```bash
npm create vite@latest my-app -- --template react-ts  # New project
npm install                                             # Install deps
npm run dev                                             # Dev server
npm run build                                           # Production build
npm run lint                                            # ESLint
npm test                                                # Run tests
npm run test:cov                                        # Coverage
```

### Recommended Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.x",
    "@tanstack/react-query": "^5.x",
    "zustand": "^4.x",
    "react-hook-form": "^7.x",
    "zod": "^3.x",
    "@hookform/resolvers": "^3.x"
  },
  "devDependencies": {
    "@types/react": "^18.x",
    "@types/react-dom": "^18.x",
    "@testing-library/react": "^14.x",
    "@testing-library/user-event": "^14.x",
    "vitest": "^1.x",
    "eslint-plugin-react-hooks": "^4.x"
  }
}
```

### ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Compound components, custom hooks, testing, performance, security patterns

## External References

- [React Documentation](https://react.dev/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
