---
name: solid-router-navigation
description: "Solid Router navigation: use <A> component for links with activeClass, useNavigate for programmatic navigation, useParams/useSearchParams for route params, redirect for server-side navigation."
metadata:
  globs:
    - "**/*router*"
    - "**/routes/**/*"
---

# Solid Router Navigation & Parameters

## Navigation

### A Component

Use `<A>` for navigation links (preferred over `<a>`):

```tsx
import { A } from "@solidjs/router";

<A href="/">Home</A>
<A href="/about" activeClass="active" inactiveClass="inactive" end={true}>
  About
</A>
<A href="users">Users</A> {/* Relative path */}
```

**Props:**
- `href`: Path to navigate to
- `activeClass`: CSS class when active (default: `"active"`)
- `inactiveClass`: CSS class when inactive (default: `"inactive"`)
- `end`: Only active for exact match (default: `false`)

Active links match current route or descendant routes unless `end={true}`.

### useNavigate

Programmatic navigation:

```tsx
import { useNavigate } from "@solidjs/router";

function Login() {
  const navigate = useNavigate();
  
  const handleLogin = () => {
    navigate("/dashboard", { replace: true });
  };
  
  return <button onClick={handleLogin}>Login</button>;
}
```

**Options:**
- `replace: true` - Replace current history entry instead of pushing

### redirect Function

Redirect from queries or actions (server-side):

```tsx
import { query, redirect } from "@solidjs/router";

const checkAuth = query(async () => {
  if (!isAuthenticated()) {
    throw redirect("/login");
  }
  return getUserData();
}, "auth");
```

### reload Function (Response Helper)

Use `reload` by returning or throwing it from queries or actions:

```tsx
import { action, reload } from "@solidjs/router";

const savePreferences = action(async () => {
  // ...persist changes...
  return reload({ revalidate: ["userPreferences"] });
}, "savePreferences");
```

For client-side revalidation, use `revalidate` instead:

```tsx
import { revalidate } from "@solidjs/router";

const refreshData = () => {
  revalidate(["userPreferences"]);
};
```

## Route Parameters

### Path Parameters

```tsx
import { useParams } from "@solidjs/router";

// Route: /users/:id
function UserPage() {
  const params = useParams();
  return <div>User {params.id}</div>;
}
```

### Search Parameters

```tsx
import { useSearchParams } from "@solidjs/router";

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  return (
    <div>
      <input 
        value={searchParams.q || ""} 
        onInput={(e) => setSearchParams({ q: e.target.value })}
      />
      <button onClick={() => setSearchParams({ q: "", page: "1" })}>
        Clear
      </button>
    </div>
  );
}
```

## Utilities

### useLocation

```tsx
import { useLocation } from "@solidjs/router";

function Breadcrumb() {
  const location = useLocation();
  return <div>Current path: {location.pathname}</div>;
}
```

### useMatch

```tsx
import { useMatch } from "@solidjs/router";

function NavLink({ href, children }) {
  const match = useMatch(() => href);
  return (
    <A href={href} class={match() ? "active" : ""}>
      {children}
    </A>
  );
}
```

### useIsRouting

```tsx
import { useIsRouting } from "@solidjs/router";

function NavigationIndicator() {
  const isRouting = useIsRouting();
  return isRouting() ? <div>Navigating...</div> : null;
}
```

### useBeforeLeave

```tsx
import { useBeforeLeave } from "@solidjs/router";

function FormPage() {
  useBeforeLeave((e) => {
    if (hasUnsavedChanges()) {
      if (!confirm("Leave without saving?")) {
        e.preventDefault();
      }
    }
  });
}
```

### Navigate Component

Immediate navigation when component renders. Useful for redirects:

```tsx
import { Navigate } from "@solidjs/router";

// Simple redirect
<Route path="/redirect" component={() => <Navigate href="/target" />} />

// Dynamic redirect
function getPath({ navigate, location }) {
  return "/some-path";
}
<Route path="/redirect" component={() => <Navigate href={getPath} />} />
```

### useCurrentMatches

Access all matched route information (useful for breadcrumbs):

```tsx
import { useCurrentMatches } from "@solidjs/router";

const matches = useCurrentMatches();
const breadcrumbs = createMemo(() =>
  matches().map((m) => m.route.info.breadcrumb)
);
```

### usePreloadRoute

Manually preload routes programmatically:

```tsx
import { usePreloadRoute } from "@solidjs/router";

function Component() {
  const preload = usePreloadRoute();
  
  const handleClick = () => {
    preload("/users/settings", { preloadData: true });
  };
  
  return <button onClick={handleClick}>Preload Settings</button>;
}
```

## Best Practices

1. Use `<A>` instead of `<a>` - Better router integration and features
2. Use relative paths in nested routes - More maintainable
3. Use `end={true}` for exact matches when needed
4. Use `redirect` for server-side navigation (authentication, etc.)
5. Handle search params reactively with `useSearchParams`
