---
name: solid-router-components
description: "Solid Router components: A for links, Route for route config, Router for setup, Navigate for redirects, active states, soft navigation."
metadata:
  globs:
    - "**/routes/**/*"
    - "**/*router*"
---

# Solid Router Components

Complete guide to Solid Router components. Use these components for navigation, routing setup, and redirects.

## A - Navigation Links

The `<A>` component provides enhanced anchor tags with automatic base path support, active states, and soft navigation.

### Basic Usage

```tsx
import { A } from "@solidjs/router";

function Navigation() {
  return (
    <nav>
      <A href="/">Home</A>
      <A href="/about">About</A>
      <A href="/contact">Contact</A>
    </nav>
  );
}
```

### Active States

```tsx
<A href="/users" activeClass="active" inactiveClass="inactive">
  Users
</A>
```

**Default behavior:**
- `active` class when href matches current location
- `inactive` class otherwise
- Matches descendants by default (e.g., `/users` matches `/users/123`)

### Exact Matching

```tsx
<A href="/" end>
  Home
</A>
```

**end prop:**
- `true`: Only active when exact match
- `false`: Active for descendants (default)
- Useful for root route `/`

### Props

| Prop | Type | Description |
|------|------|-------------|
| `href` | string | Route path (relative or absolute) |
| `noScroll` | boolean | Disable scroll to top on navigation |
| `replace` | boolean | Replace history entry (no back button) |
| `state` | unknown | Push state to history stack |
| `activeClass` | string | Class when link is active |
| `inactiveClass` | string | Class when link is inactive |
| `end` | boolean | Exact match only (no descendants) |

### Soft Navigation

Both `<A>` and `<a>` support soft navigation when JavaScript is present. To disable:

```tsx
<A href="/page" target="_self">Link</A>
```

## Route - Route Configuration

Configure routes with preloading and other options.

### Basic Route

```tsx
import { Route } from "@solidjs/router";

<Route path="/users/:id" component={UserProfile} />
```

### Route with Preload

```tsx
<Route
  path="/users/:id"
  component={UserProfile}
  preload={({ params }) => {
    void getUserQuery(params.id);
  }}
/>
```

### Route Props

| Prop | Type | Description |
|------|------|-------------|
| `path` | string | Route path pattern |
| `component` | Component | Component to render |
| `preload` | function | Preload function |

## Router - Router Setup

Set up the router with base path and root component.

### Basic Setup

```tsx
import { Router, A } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";

function App() {
  return (
    <Router
      root={(props) => (
        <>
          <nav>
            <A href="/">Home</A>
            <A href="/about">About</A>
          </nav>
          <Suspense>{props.children}</Suspense>
        </>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
```

### With Base Path

```tsx
<Router base="/app">
  <FileRoutes />
</Router>
```

**Base path:**
- Prepended to all routes
- `<A>` components respect base
- Native `<a>` tags don't

### Router Props

| Prop | Type | Description |
|------|------|-------------|
| `base` | string | Base path for all routes |
| `root` | Component | Root component wrapper |
| `data` | object | Router data |

## Navigate - Programmatic Redirects

Redirect to a route programmatically.

### Basic Redirect

```tsx
import { Navigate } from "@solidjs/router";

function Redirect() {
  return <Navigate href="/home" />;
}
```

### Replace History

```tsx
<Navigate href="/home" replace />
```

### With State

```tsx
<Navigate href="/home" state={{ from: "/login" }} />
```

### Conditional Redirect

```tsx
function ProtectedRoute() {
  const isAuthenticated = useAuth();
  
  return (
    <Show when={isAuthenticated()} fallback={<Navigate href="/login" />}>
      <ProtectedContent />
    </Show>
  );
}
```

## Common Patterns

### Navigation Menu

```tsx
function Navigation() {
  return (
    <nav>
      <A href="/" end activeClass="active">
        Home
      </A>
      <A href="/about" activeClass="active">
        About
      </A>
      <A href="/contact" activeClass="active">
        Contact
      </A>
    </nav>
  );
}
```

### Breadcrumbs

```tsx
function Breadcrumbs() {
  const location = useLocation();
  const path = location.pathname.split("/").filter(Boolean);
  
  return (
    <nav>
      <A href="/">Home</A>
      <For each={path}>
        {(segment, index) => (
          <>
            <span> / </span>
            <A href={`/${path.slice(0, index() + 1).join("/")}`}>
              {segment}
            </A>
          </>
        )}
      </For>
    </nav>
  );
}
```

### Protected Routes

```tsx
function ProtectedRoute({ children }) {
  const isAuthenticated = useAuth();
  
  return (
    <Show when={isAuthenticated()} fallback={<Navigate href="/login" />}>
      {children}
    </Show>
  );
}
```

### Route with Data

```tsx
<Route
  path="/users/:id"
  component={UserProfile}
  preload={({ params }) => {
    void getUserQuery(params.id);
  }}
/>
```

## Best Practices

1. **Use `<A>` for navigation:**
   - Automatic active states
   - Base path support
   - Soft navigation

2. **Wrap router with Suspense:**
   - Routes are lazy-loaded
   - Suspense handles loading

3. **Use `end` prop for root:**
   - Prevents `/` matching everything
   - Exact match only

4. **Preload route data:**
   - Use preload function
   - Seed caches early

5. **Use Navigate for redirects:**
   - Programmatic navigation
   - Conditional redirects

## Summary

- **A**: Enhanced anchor with active states
- **Route**: Route configuration
- **Router**: Router setup with base path
- **Navigate**: Programmatic redirects
- **Active states**: Automatic class management
- **Soft navigation**: Enhanced performance

