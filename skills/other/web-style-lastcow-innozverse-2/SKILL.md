---
name: innozverse-web-style
description: Follow Next.js web development patterns including App Router conventions, client/server components, API client usage, and environment variables. Use when building web features, creating pages, or working with Next.js code.
---

# innozverse Web Development Style (Next.js)

Follow these patterns when building web features in apps/web.

## Next.js App Router

Use App Router (`src/app/`), not Pages Router.

### Page Structure
```typescript
// apps/web/src/app/users/page.tsx
export default function UsersPage() {
  return <div>Users</div>;
}
```

### Layout
```typescript
// apps/web/src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

## API Client Usage

```typescript
'use client';

import { useState, useEffect } from 'react';
import { ApiClient } from '@innozverse/api-client';

const apiClient = new ApiClient(
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080'
);

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient.getUsers()
      .then(setUsers)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <div>{/* render users */}</div>;
}
```

## Client vs Server Components

- **Server Component** (default): No state, no effects, server-side rendering
- **Client Component** (`'use client'`): Interactive, state, effects, API calls

## Environment Variables

- Client-side: `NEXT_PUBLIC_*`
- Server-side: Any variable name

```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
```

## Best Practices

- Prefer server components when possible
- Use client components for interactivity
- Handle loading and error states
- Type all props and state
- Use TypeScript strict mode
