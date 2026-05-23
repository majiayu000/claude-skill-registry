---
name: web-navigation
description: Navigation and routing patterns for React web applications. Use when implementing React Router, Next.js routing, deep links, or handling navigation state.
---

# Web Navigation (React)

## React Router (v6)

### Basic Setup

```typescript
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/users/:id" element={<UserDetailPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Nested Routes & Layouts

```typescript
// Layout with shared UI
function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}

// Routes
<Routes>
  <Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<DashboardHome />} />
    <Route path="analytics" element={<Analytics />} />
    <Route path="settings" element={<Settings />} />
  </Route>
</Routes>
```

### Dynamic Routes

```typescript
import { useParams, useSearchParams } from 'react-router-dom';

// Route: /users/:id
function UserDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [searchParams, setSearchParams] = useSearchParams();

  const tab = searchParams.get('tab') || 'profile';

  return (
    <div>
      <h1>User {id}</h1>
      <TabBar
        active={tab}
        onChange={(t) => setSearchParams({ tab: t })}
      />
    </div>
  );
}
```

### Programmatic Navigation

```typescript
import { useNavigate, useLocation } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();

  async function handleLogin() {
    await login(credentials);

    // Redirect to intended page or default
    const from = location.state?.from?.pathname || '/dashboard';
    navigate(from, { replace: true });
  }

  // Other navigation methods
  navigate('/users');           // Push to history
  navigate('/users', { replace: true }); // Replace current entry
  navigate(-1);                 // Go back
  navigate(1);                  // Go forward
}
```

### Link Component

```typescript
import { Link, NavLink } from 'react-router-dom';

// Basic link
<Link to="/about">About</Link>

// With state
<Link to="/checkout" state={{ cartId: '123' }}>
  Checkout
</Link>

// NavLink - active styling
<NavLink
  to="/dashboard"
  className={({ isActive }) =>
    isActive ? 'nav-link active' : 'nav-link'
  }
>
  Dashboard
</NavLink>
```

---

## Next.js App Router

### File-Based Routing

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # / route
├── about/
│   └── page.tsx        # /about route
├── users/
│   ├── page.tsx        # /users route
│   └── [id]/
│       └── page.tsx    # /users/:id route
├── (auth)/             # Route group (no URL segment)
│   ├── login/
│   │   └── page.tsx    # /login route
│   └── register/
│       └── page.tsx    # /register route
└── dashboard/
    ├── layout.tsx      # Dashboard layout
    ├── page.tsx        # /dashboard
    └── settings/
        └── page.tsx    # /dashboard/settings
```

### Layouts

```typescript
// app/layout.tsx - Root layout
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Header />
          {children}
          <Footer />
        </Providers>
      </body>
    </html>
  );
}

// app/dashboard/layout.tsx - Nested layout
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

### Dynamic Routes

```typescript
// app/users/[id]/page.tsx
interface Props {
  params: { id: string };
  searchParams: { tab?: string };
}

export default function UserPage({ params, searchParams }: Props) {
  const { id } = params;
  const tab = searchParams.tab || 'profile';

  return (
    <div>
      <h1>User {id}</h1>
      <Tabs active={tab} />
    </div>
  );
}

// Generate static params (optional)
export async function generateStaticParams() {
  const users = await getUsers();
  return users.map((user) => ({
    id: user.id,
  }));
}
```

### Programmatic Navigation

```typescript
'use client';

import { useRouter, usePathname, useSearchParams } from 'next/navigation';

function SearchForm() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  function handleSearch(query: string) {
    const params = new URLSearchParams(searchParams);
    params.set('q', query);
    router.push(`${pathname}?${params.toString()}`);
  }

  // Navigation methods
  router.push('/dashboard');      // Navigate
  router.replace('/dashboard');   // Replace without history
  router.back();                  // Go back
  router.forward();               // Go forward
  router.refresh();               // Refresh server components
}
```

### Link Component

```typescript
import Link from 'next/link';

// Basic link
<Link href="/about">About</Link>

// With dynamic route
<Link href={`/users/${user.id}`}>
  {user.name}
</Link>

// With query params
<Link href={{ pathname: '/search', query: { q: 'react' } }}>
  Search
</Link>

// Prefetching (default: true)
<Link href="/dashboard" prefetch={false}>
  Dashboard
</Link>
```

---

## Route Groups & Organization

### Auth-Protected vs Public Routes

```typescript
// React Router
<Routes>
  {/* Public routes */}
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />

  {/* Protected routes */}
  <Route element={<RequireAuth />}>
    <Route path="/dashboard" element={<DashboardPage />} />
    <Route path="/settings" element={<SettingsPage />} />
  </Route>
</Routes>

// Next.js - use route groups
// app/(public)/login/page.tsx
// app/(protected)/dashboard/page.tsx
// app/(protected)/layout.tsx - add auth check
```

---

## Loading & Error States

### React Router

```typescript
import { Suspense } from 'react';
import { Await, useLoaderData, defer } from 'react-router-dom';

// Loader
export async function loader({ params }) {
  return defer({
    user: getUser(params.id), // Promise
  });
}

// Component
function UserPage() {
  const { user } = useLoaderData();

  return (
    <Suspense fallback={<Spinner />}>
      <Await resolve={user} errorElement={<ErrorFallback />}>
        {(resolvedUser) => <UserProfile user={resolvedUser} />}
      </Await>
    </Suspense>
  );
}
```

### Next.js

```typescript
// app/users/[id]/loading.tsx
export default function Loading() {
  return <Spinner />;
}

// app/users/[id]/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// app/users/[id]/not-found.tsx
export default function NotFound() {
  return <div>User not found</div>;
}
```

---

## Scroll Restoration

### React Router

```typescript
import { ScrollRestoration } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>{/* ... */}</Routes>
      <ScrollRestoration />
    </BrowserRouter>
  );
}
```

### Manual Scroll to Top

```typescript
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}
```

---

## Deep Linking / Query Params

```typescript
// Custom hook for type-safe query params
import { useSearchParams } from 'react-router-dom';

interface Filters {
  category?: string;
  sort?: 'asc' | 'desc';
  page?: number;
}

function useFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters: Filters = {
    category: searchParams.get('category') || undefined,
    sort: (searchParams.get('sort') as 'asc' | 'desc') || undefined,
    page: Number(searchParams.get('page')) || 1,
  };

  function setFilters(newFilters: Partial<Filters>) {
    const params = new URLSearchParams(searchParams);

    Object.entries(newFilters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.set(key, String(value));
      } else {
        params.delete(key);
      }
    });

    setSearchParams(params);
  }

  return { filters, setFilters };
}

// Usage
function ProductList() {
  const { filters, setFilters } = useFilters();

  return (
    <div>
      <CategorySelect
        value={filters.category}
        onChange={(cat) => setFilters({ category: cat })}
      />
      <ProductGrid products={products} />
      <Pagination
        page={filters.page}
        onChange={(p) => setFilters({ page: p })}
      />
    </div>
  );
}
```

---

## Navigation Guards

```typescript
// Prevent navigation with unsaved changes
import { useBlocker } from 'react-router-dom';

function EditForm() {
  const [isDirty, setIsDirty] = useState(false);

  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) =>
      isDirty && currentLocation.pathname !== nextLocation.pathname
  );

  return (
    <>
      <form onChange={() => setIsDirty(true)}>
        {/* form fields */}
      </form>

      {blocker.state === 'blocked' && (
        <ConfirmDialog
          message="You have unsaved changes. Leave anyway?"
          onConfirm={() => blocker.proceed()}
          onCancel={() => blocker.reset()}
        />
      )}
    </>
  );
}
```

---

## Common Patterns

### Redirect After Action

```typescript
// After form submission
async function handleSubmit(data: FormData) {
  const result = await createItem(data);
  navigate(`/items/${result.id}`);
}

// After login
async function handleLogin() {
  await login(credentials);
  const redirectTo = searchParams.get('redirect') || '/dashboard';
  navigate(redirectTo, { replace: true });
}
```

### Tab Navigation with URL

```typescript
function UserProfile() {
  const [searchParams, setSearchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';

  const tabs = ['overview', 'activity', 'settings'];

  return (
    <div>
      <nav>
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setSearchParams({ tab: t })}
            className={tab === t ? 'active' : ''}
          >
            {t}
          </button>
        ))}
      </nav>
      <TabContent tab={tab} />
    </div>
  );
}
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Route not matching | Check route order (specific before dynamic) |
| Back button doesn't work | Use `navigate()` not `window.location` |
| State lost on refresh | Store in URL params, not just state |
| Scroll position wrong | Add `ScrollRestoration` component |
| 404 in production (SPA) | Configure server for SPA fallback |
