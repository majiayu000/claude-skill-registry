---
name: nextjs-server-components
description: Build efficient React applications using Next.js Server Components that render on the server, reducing client bundle size, improving performance, and enabling direct database access. Use when fetching data server-side, reducing JavaScript bundle size, accessing databases directly in components, implementing streaming with Suspense, creating layouts that only render once, optimizing Core Web Vitals, or building SEO-friendly applications with server-first architecture.
---

# Next.js Server Components - React Server Components Patterns

## When to use this skill

- Fetching data directly in Server Components
- Reducing client-side JavaScript bundle size
- Accessing databases directly without API routes
- Implementing streaming rendering with Suspense
- Creating layouts that render once and persist
- Optimizing Largest Contentful Paint (LCP)
- Building SEO-friendly server-rendered applications
- Using server-only code (database queries, secrets)
- Implementing server-side data transformations
- Reducing Time to Interactive (TTI)
- Building applications with zero client JS by default
- Combining Server and Client Components effectively

## When to use this skill

- Building Next.js 13+ apps, optimizing component rendering, managing server/client boundaries.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Building Next.js 13+ apps, optimizing component rendering, managing server/client boundaries.

## Key Concepts

Server Components (default in App Router):
- Run only on server
- Can directly access databases/APIs
- Zero client JavaScript
- Support async/await

Client Components ('use client'):
- Interactive features
- Browser APIs
- React hooks (useState, useEffect, etc.)

## Composition Pattern

```typescript
// ✅ Server Component fetches data
// app/page.tsx
import { ClientComponent } from './ClientComponent';

export default async function Page() {
  const data = await fetchData(); // Server-side
  
  return (
    <div>
      <h1>Server Rendered: {data.title}</h1>
      <ClientComponent initialData={data} />
    </div>
  );
}

// ✅ Client Component handles interactivity
// app/ClientComponent.tsx
'use client';

export function ClientComponent({ initialData }) {
  const [count, setCount] = useState(0);
  
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

## Pass Server Components as Children

```typescript
// ✅ Client Component with Server Component children
'use client';

export function ClientLayout({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  );
}

// Usage - children can be Server Components!
<ClientLayout>
  <ServerDataComponent /> {/* Stays on server */}
</ClientLayout>
```

## When to Use Client Components

Only use 'use client' when you need:
- useState, useEffect, useContext
- Browser APIs (localStorage, window)
- Event handlers (onClick, onChange)
- Custom hooks
- Third-party libraries that use React hooks

## Resources
- [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)

---

**Remember**: Keep components server-side by default. Only add 'use client' when necessary for interactivity.
