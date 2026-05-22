---
name: react-component-architecture-rsc
description: |
  React Server Components vs Client Components decision framework, "use client" criteria, and composition patterns.
  Keywords: "server component", "client component", "use client", "rsc", "interactive", "useState"
---

# React Component Architecture - RSC

## Core Principle: RSC as Default

All components in Next.js App Router are **Server Components** by default.

### Server Components

- Async functions
- Can fetch data directly
- Cannot use state or effects
- Cannot use event handlers
- Cannot use browser APIs
- Run only on server

\`\`\`tsx
// Server Component (no 'use client')
export default async function PostPage({ params }) {
  const post = await fetchPost(params.id);
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
\`\`\`

### Client Components

Add \`'use client'\` directive when component needs:

1. **State**: \`useState\`, \`useReducer\`
2. **Effects**: \`useEffect\`, \`useLayoutEffect\`
3. **Event handlers**: \`onClick\`, \`onChange\`
4. **Browser APIs**: \`window\`, \`localStorage\`
5. **React Context consumers**

\`\`\`tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

export function LikeButton({ postId, initialLikes }) {
  const [likes, setLikes] = useState(initialLikes);
  
  return (
    <Button onClick={() => setLikes(likes + 1)}>
      👍 {likes}
    </Button>
  );
}
\`\`\`

## Island Architecture Pattern

Keep Client Components small and at leaves:

\`\`\`tsx
// ✅ GOOD: Server parent, small Client leaf
// app/posts/[id]/page.tsx (Server Component)
export default async function PostPage({ params }) {
  const post = await fetchPost(params.id);
  
  return (
    <article>
      {/* Server-rendered content */}
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      
      {/* Small interactive island */}
      <LikeButton postId={post.id} initialLikes={post.likes} />
    </article>
  );
}

// ❌ BAD: Entire page as Client Component
'use client';
export default function PostPage() {
  const [post, setPost] = useState(null);
  
  useEffect(() => {
    fetchPost().then(setPost);
  }, []);
  
  // All content client-rendered, larger bundle
}
\`\`\`

## Data Flow: Server to Client

Pass data as **serializable props**:

\`\`\`tsx
// Server Component
export default async function Page() {
  const data = await fetchData();
  
  return <ClientComponent data={data} />; // ✅ Serializable
}

// Cannot pass functions (unless Server Actions)
<ClientComponent onClick={handleClick} /> // ❌ Function not serializable
\`\`\`

## Anti-Patterns

❌ \`'use client'\` on page.tsx/layout.tsx - Forces entire route client
❌ Data fetching in \`useEffect\` - Creates waterfall
❌ Large Client Components - Increases bundle size

✅ Server Components by default
✅ Extract only interactive parts to Client Components
✅ Fetch data in Server Components, pass as props

---

**Token Estimate**: ~3,000 tokens
