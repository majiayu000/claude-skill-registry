---
name: remixjs-best-practices
description: Best practices for Remix (2025-2026 Edition), focusing on React Router v7 migration, server-first data patterns, and error handling.
---

# Remix Best Practices (2025-2026 Edition)

This skill outlines modern best practices for building scalable, high-performance applications with Remix, specifically focusing on the transition to React Router v7 and future-proofing for Remix v3.

## 🚀 Key Trends (2025+)

*   **React Router v7 is Remix:** All Remix features are now part of React Router v7. New projects should start with React Router v7.
*   **Server-First Mental Model:** Loaders and Actions run *only* on the server.
*   **"Future Flags" Adoption:** Always enable v7 future flags in `remix.config.js` or `vite.config.ts` to ensuring smooth migration.
*   **Codemod Migration:** Use `npx codemod remix/2/react-router/upgrade` to migrate existing v2 apps.

## 🏗️ Architecture & Data Loading

### 1. Server-First Data Flow
Avoid client-side fetching (`useEffect`) unless absolutely necessary.
*   **Loaders:** Fetch data server-side.
*   **Actions:** Mutate data server-side.
*   **Components:** render *what* the loader provides.

```typescript
// ✅ Good: Typed loader with single strict return
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const user = await getUser(request);
  if (!user) throw new Response("Unauthorized", { status: 401 });
  return json({ user });
};

// Component gets fully typed data
export default function Dashboard() {
  const { user } = useLoaderData<typeof loader>(); 
  return <h1>Hello, {user.name}</h1>;
}
```

### 2. Form Actions over `onClick`
Use HTML Forms (or Remix `<Form>`) for mutations. This works without JS and handles race conditions automatically.

```tsx
// ✅ Good: Descriptive, declarative mutation
<Form method="post" action="/update-profile">
  <button type="submit">Save</button>
</Form>
```

### 3. Progressive Enhancement
Design features to work without JavaScript first. Remix handles the "hydration" to make it interactive (SPA feel) automatically.

## 🛡️ Error Handling Patterns

### 1. Granular Error Boundaries
Do not rely solely on a root ErrorBoundary. Place boundaries in nested routes to prevent a partial failure from crashing the entire page.

```tsx
// routes/dashboard.tsx (Nested Route)
export function ErrorBoundary() {
  const error = useRouteError();
  return <div className="p-4 bg-red-50">Widget crashed: {error.message}</div>;
}
```

### 2. Expected vs. Unexpected Errors
*   **Expected (404, 401):** `throw new Response(...)`. Caught by specific logic or boundaries.
*   **Unexpected (500):** Let the app crash to the nearest ErrorBoundary.

### 3. Controller Actions (Validation)
Return errors from actions, don't throw them. This preserves user input.

```typescript
// Action
if (name.length < 3) {
  return json({ errors: { name: "Too short" } }, { status: 400 });
}

// Component
const actionData = useActionData<typeof action>();
{actionData?.errors?.name && <span>{actionData.errors.name}</span>}
```

## ⚡ Performance Optimization

### 1. `Cache-Control` Headers
Loaders can output cache headers. Use them for public data.
```typescript
export const loader = async () => {
  return json(data, {
    headers: { "Cache-Control": "public, max-age=3600" }
  });
};
```

### 2. Streaming (Defer)
Use `defer` for slow data (e.g., third-party APIs) to unblock the initial HTML render.
```typescript
export const loader = async () => {
  const critical = await getCriticalData();
  const slow = getSlowData(); // Promise
  return defer({ critical, slow });
};

// UI supports <Suspense> for the slow part
```

## 📚 References

*   [React Router v7 Migration Guide](https://reactrouter.com/v7/upgrading/remix)
*   [Remix "Future Flags" Documentation](https://remix.run/docs/en/main/start/future)
*   [Remix Routing Guide](https://remix.run/docs/en/main/discussion/routes)
