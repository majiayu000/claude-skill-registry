---
name: react-router-setup
description: Add URL routing to React Vite SPAs using react-router-dom v6. Use when asked to "add routing", "add URL navigation", "make URLs work", "add deep linking", "enable browser back/forward", or when converting state-based navigation to URL-based routing. Covers installation, BrowserRouter configuration with basename, route definitions, nested routes, Link components, useNavigate hooks, redirects, and SPA server fallback.
---

# React Router Setup for Vite SPAs

Add react-router-dom v6 to existing React Vite projects.

## Installation

```bash
npm install react-router-dom
# or
pnpm add react-router-dom
```

## Setup Steps

### 1. Wrap App with BrowserRouter

In `main.tsx`:

```tsx
import { BrowserRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter basename="/app">
      {' '}
      {/* basename for SPA base path */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

**basename**: Set to your SPA's base path (e.g., `/dashboard`, `/app`). All routes become relative to this.

### 2. Create Route Constants

Create `routes.ts` for type-safe route management:

```ts
export const ROUTES = {
  HOME: '/',
  USERS: '/users',
  USER_DETAIL: '/users/:id',
  SETTINGS: '/settings',
  SETTINGS_PROFILE: '/settings/profile',
} as const;

// Derive state from URL path
export function getRouteState(pathname: string) {
  if (pathname.startsWith('/users')) return { view: 'users' };
  if (pathname.startsWith('/settings')) return { view: 'settings' };
  return { view: 'home' };
}
```

### 3. Add Routes Component

Using `Routes` and `Route`:

```tsx
import { Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" replace />} />
      <Route path="/home" element={<Home />} />
      <Route path="/users" element={<Users />} />
      <Route path="/users/:id" element={<UserDetail />} />
      <Route path="/settings" element={<Navigate to="/settings/profile" replace />} />
      <Route path="/settings/profile" element={<SettingsProfile />} />
      <Route path="/settings/account" element={<SettingsAccount />} />
      <Route path="*" element={<Navigate to="/home" replace />} />
    </Routes>
  );
}
```

### 4. Convert Navigation

**Replace buttons with Link:**

```tsx
// Before
<button onClick={() => setView('users')}>Users</button>;

// After
import { Link } from 'react-router-dom';
<Link to="/users">Users</Link>;
```

**Use navigate() for programmatic navigation:**

```tsx
import { useNavigate } from 'react-router-dom';

function Component() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/users'); // push
    navigate('/users', { replace: true }); // replace
    navigate(-1); // back
  };
}
```

### 5. Derive State from URL

Replace state variables with URL-derived state:

```tsx
import { useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();

  // Before: const [activeView, setActiveView] = useState('home');
  // After: derive from URL
  const activeView = useMemo(() => {
    if (location.pathname.startsWith('/users')) return 'users';
    if (location.pathname.startsWith('/settings')) return 'settings';
    return 'home';
  }, [location.pathname]);
}
```

### 6. Active Link Styling

```tsx
import { useLocation, Link } from 'react-router-dom';

function NavLink({ to, children }) {
  const location = useLocation();
  const isActive = location.pathname.startsWith(to);

  return (
    <Link to={to} className={isActive ? 'active' : ''}>
      {children}
    </Link>
  );
}
```

### 7. URL Parameters

```tsx
import { useParams, useSearchParams } from 'react-router-dom';

function UserDetail() {
  const { id } = useParams(); // from /users/:id
  const [searchParams, setSearchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'profile';

  return (
    <div>
      User {id}, Tab: {tab}
    </div>
  );
}
```

## Server SPA Fallback

The server must serve `index.html` for all non-API routes.

**Express:**

```js
app.get('/*', (req, res, next) => {
  if (req.path.startsWith('/api')) return next();
  res.sendFile(path.join(staticPath, 'index.html'));
});
```

**Vite dev server** handles this automatically.

**Nginx:**

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

## Common Pitfalls

1. **Missing basename**: If SPA is at `/app`, set `basename="/app"` in BrowserRouter
2. **Hash vs History**: Use BrowserRouter (history API), not HashRouter, for clean URLs
3. **Refresh fails**: Server must return index.html for all routes (SPA fallback)
4. **Link vs anchor**: Always use `<Link>` not `<a>` for internal navigation
5. **State not updating**: Derive state from `location.pathname`, don't maintain separate state

## Testing Checklist

- [ ] Direct URL access works (e.g., `/app/users/123`)
- [ ] Browser back/forward navigation works
- [ ] Page refresh on nested routes works
- [ ] Sidebar/nav highlighting matches URL
- [ ] Redirects work (root → default route)
