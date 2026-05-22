---
name: "Next.js UI Generator"
description: "Generate responsive Next.js components and pages (task tables with sort/filter, forms, auth pages) using App Router, TypeScript, Tailwind when user needs frontend UI"
version: "1.0.0"
---

# Next.js UI Generator Skill

## Purpose

Automatically generate production-ready Next.js frontend components, pages, and layouts using App Router, TypeScript, and Tailwind CSS when the user requests UI implementation for the Phase II full-stack todo application.

## When This Skill Triggers

Use this skill when the user asks to:
- "Create a todo list page"
- "Build the login/register UI"
- "Generate a task form component"
- "Make the dashboard responsive"
- "Add a todo table with filters"
- Any request to build frontend pages, components, or UI

## Prerequisites

Before generating UI:
1. Read `specs/phase-2/spec.md` for UI/UX requirements
2. Read `.specify/memory/constitution.md` for code standards
3. Verify Next.js project exists in `frontend/` directory
4. Check existing component patterns for consistency

## Step-by-Step Procedure

### Step 1: Analyze Requirements
- Identify what UI component/page is needed
- Check spec.md for specific requirements (user stories, acceptance criteria)
- Determine if it's a page (app/) or reusable component (components/)
- Identify data requirements (API calls needed)

### Step 2: Choose Component Type
**Server Component (default):**
- Static content
- Data fetching on server
- No user interactivity
- Example: Dashboard layout, todo list display

**Client Component ('use client'):**
- Interactive forms
- State management (useState, useEffect)
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Example: TodoForm, LoginForm, filters

### Step 3: Create TypeScript Interfaces

```typescript
// types/todo.ts
export interface Todo {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  tags: string[];
  created_at: string;
  updated_at: string;
  user_id: number;
}

export interface TodoFormData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}
```

### Step 4: Generate Component Structure

**For Pages (app/ directory):**
```typescript
// app/dashboard/page.tsx
import { getTodos } from '@/lib/api';
import { TodoList } from '@/components/todos/TodoList';

export default async function DashboardPage() {
  const todos = await getTodos(); // Server-side fetch

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">My Todos</h1>
      <TodoList todos={todos} />
    </main>
  );
}
```

**For Interactive Components:**
```typescript
// components/todos/TodoForm.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createTodo } from '@/lib/api';
import type { TodoFormData } from '@/types/todo';

export function TodoForm() {
  const router = useRouter();
  const [formData, setFormData] = useState<TodoFormData>({
    title: '',
    description: '',
    priority: 'medium',
    tags: [],
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.title.trim()) {
      setErrors({ title: 'Title is required' });
      return;
    }

    setIsSubmitting(true);
    try {
      await createTodo(formData);
      router.refresh(); // Refresh server component data
      setFormData({ title: '', description: '', priority: 'medium', tags: [] });
    } catch (error) {
      setErrors({ submit: 'Failed to create todo' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Form fields */}
    </form>
  );
}
```

### Step 5: Apply Tailwind Styling

**Design Principles:**
- Mobile-first responsive design
- Use utility classes exclusively
- Consistent spacing (4px grid: p-4, m-2, gap-4)
- Semantic color scheme from constitution

**Responsive Grid Example:**
```tsx
<div className="
  grid
  grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  gap-4
  p-4
">
  {todos.map(todo => (
    <TodoCard key={todo.id} todo={todo} />
  ))}
</div>
```

**Form Styling:**
```tsx
<input
  type="text"
  className="
    w-full
    px-4 py-2
    border border-gray-300 rounded-lg
    focus:ring-2 focus:ring-blue-500 focus:border-transparent
    disabled:opacity-50 disabled:cursor-not-allowed
  "
/>
```

### Step 6: Add Accessibility Features

- Semantic HTML (`<main>`, `<nav>`, `<article>`)
- ARIA labels for icon buttons
- Keyboard navigation support
- Focus states for all interactive elements
- Proper heading hierarchy (h1 → h2 → h3)

**Example:**
```tsx
<button
  aria-label="Delete todo"
  onClick={handleDelete}
  className="p-2 hover:bg-red-100 rounded focus:ring-2 focus:ring-red-500"
>
  <TrashIcon className="w-5 h-5 text-red-600" />
</button>
```

### Step 7: Implement Loading and Error States

**Loading UI:**
```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-gray-200 rounded w-1/4"></div>
      <div className="h-20 bg-gray-200 rounded"></div>
      <div className="h-20 bg-gray-200 rounded"></div>
    </div>
  );
}
```

**Error Boundary:**
```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({ error, reset }: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <h2 className="text-xl font-bold text-red-800 mb-2">
        Something went wrong!
      </h2>
      <p className="text-red-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Try again
      </button>
    </div>
  );
}
```

## Output Format

### Generated Files Structure
```
frontend/
├── app/
│   ├── dashboard/
│   │   ├── page.tsx         # Generated page
│   │   ├── loading.tsx      # Loading state
│   │   └── error.tsx        # Error boundary
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── components/
│   ├── todos/
│   │   ├── TodoList.tsx     # Display component
│   │   ├── TodoCard.tsx     # Individual todo
│   │   ├── TodoForm.tsx     # Create/edit form
│   │   └── TodoFilters.tsx  # Filter controls
│   └── ui/
│       ├── Button.tsx
│       └── Input.tsx
└── types/
    └── todo.ts              # TypeScript interfaces
```

### Code Quality Standards

Every generated component MUST:
- ✅ Use TypeScript with strict typing (no `any`)
- ✅ Follow Next.js App Router conventions
- ✅ Be responsive (mobile, tablet, desktop)
- ✅ Include loading/error states for async operations
- ✅ Have proper accessibility (ARIA, keyboard nav)
- ✅ Use semantic HTML5 elements
- ✅ Style with Tailwind exclusively (no CSS modules)
- ✅ Include clear prop types/interfaces
- ✅ Handle edge cases (empty states, errors)

## Quality Criteria

**Before Completing, Verify:**

1. **TypeScript Compilation**
   ```bash
   npm run type-check  # Should pass with no errors
   ```

2. **Responsive Design**
   - Test on mobile (320px), tablet (768px), desktop (1024px+)
   - All content readable and accessible at all sizes

3. **Accessibility**
   - Can navigate entire UI with keyboard only
   - Screen reader friendly (proper labels)
   - Focus states visible

4. **Performance**
   - Use Server Components for static content
   - Client Components only when needed
   - Lazy load heavy components

5. **Consistency**
   - Matches existing component patterns
   - Follows constitution design system
   - Uses established utility patterns

## Examples

### Example 1: Todo Table with Filters

**User Request:** "Create a todo table with filtering and sorting"

**Generated Output:**
```tsx
// components/todos/TodoTable.tsx
'use client';

import { useState } from 'react';
import type { Todo } from '@/types/todo';

interface TodoTableProps {
  todos: Todo[];
}

export function TodoTable({ todos }: TodoTableProps) {
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [sortBy, setSortBy] = useState<'created' | 'priority'>('created');

  const filteredTodos = todos.filter(todo => {
    if (filter === 'all') return true;
    return filter === 'completed' ? todo.completed : !todo.completed;
  });

  const sortedTodos = [...filteredTodos].sort((a, b) => {
    if (sortBy === 'priority') {
      const priority = { high: 3, medium: 2, low: 1 };
      return priority[b.priority] - priority[a.priority];
    }
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex gap-2">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value as any)}
          className="px-3 py-2 border rounded"
        >
          <option value="all">All</option>
          <option value="completed">Completed</option>
          <option value="pending">Pending</option>
        </select>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as any)}
          className="px-3 py-2 border rounded"
        >
          <option value="created">Sort by Date</option>
          <option value="priority">Sort by Priority</option>
        </select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-3 text-left">Title</th>
              <th className="p-3 text-left">Priority</th>
              <th className="p-3 text-left">Status</th>
              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedTodos.map(todo => (
              <tr key={todo.id} className="border-b hover:bg-gray-50">
                <td className="p-3">{todo.title}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-sm ${
                    todo.priority === 'high' ? 'bg-red-100 text-red-800' :
                    todo.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {todo.priority}
                  </span>
                </td>
                <td className="p-3">
                  {todo.completed ? '✓ Complete' : '○ Pending'}
                </td>
                <td className="p-3">
                  <button className="text-blue-600 hover:underline">
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

### Example 2: Login Page

**User Request:** "Build the login page"

**Generated Output:**
```tsx
// app/login/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-2xl font-bold text-center mb-6">
            Sign In to Todo App
          </h1>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center mt-4 text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="/register" className="text-blue-600 hover:underline">
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </main>
  );
}
```

## Success Indicators

The skill execution is successful when:
- ✅ All generated files compile without TypeScript errors
- ✅ Components render correctly on all screen sizes
- ✅ Accessibility requirements met (keyboard nav, ARIA labels)
- ✅ Loading and error states implemented
- ✅ Code follows Next.js App Router best practices
- ✅ Matches spec.md requirements
- ✅ Consistent with existing codebase patterns
