---
name: nextjs-code-review
description: Provides comprehensive code review capability for Next.js applications, validates Server Components, Client Components, Server Actions, caching strategies, metadata, API routes, middleware, and performance patterns. Use when reviewing Next.js App Router code changes, before merging pull requests, after implementing new features, or for architecture validation. Triggers on "review Next.js code", "Next.js code review", "check my Next.js app".
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Next.js Code Review

## Overview

This skill provides structured, comprehensive code review for Next.js applications built with the App Router. It evaluates code against Next.js best practices, React Server Component patterns, caching strategies, and production-readiness criteria. The review produces actionable findings categorized by severity (Critical, Warning, Suggestion) with concrete code examples for improvements.

This skill delegates to the `typescript-software-architect-review` agent for deep architectural analysis when invoked through the agent system.

## When to Use

- Reviewing Next.js pages, layouts, and route segments before merging
- Validating Server Component vs Client Component boundaries
- Checking Server Actions for security and correctness
- Reviewing data fetching patterns (fetch, cache, revalidation)
- Evaluating caching strategies (static generation, ISR, dynamic rendering)
- Assessing middleware implementations (authentication, redirects, rewrites)
- Reviewing API route handlers for proper request/response handling
- Validating metadata configuration for SEO
- Checking loading, error, and not-found page implementations
- After implementing new Next.js features or migrating from Pages Router

## Instructions

1. **Identify Scope**: Determine which Next.js route segments and components are under review. Use `glob` to discover `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `route.ts`, and `middleware.ts` files.

2. **Analyze Component Boundaries**: Verify proper Server Component / Client Component separation. Check that `'use client'` is placed only where necessary and as deep in the component tree as possible. Ensure Server Components don't import client-only modules.

3. **Review Data Fetching**: Validate fetch patterns — check for proper `cache` and `revalidate` options, parallel data fetching with `Promise.all`, and avoidance of request waterfalls. Verify that server-side data fetching doesn't expose sensitive data to the client.

4. **Evaluate Caching Strategy**: Review static vs dynamic rendering decisions. Check `generateStaticParams` usage for static generation, `revalidatePath`/`revalidateTag` for on-demand revalidation, and proper cache headers for API routes.

5. **Assess Server Actions**: Review form actions for proper validation (both client and server-side), error handling, optimistic updates with `useOptimistic`, and security (ensure actions don't expose sensitive operations without authorization).

6. **Check Middleware**: Review middleware for proper request matching, authentication/authorization logic, response modification, and performance impact. Verify it runs only on necessary routes.

7. **Review Metadata & SEO**: Check `generateMetadata` functions, Open Graph tags, structured data, `robots.txt`, and `sitemap.xml` configurations. Verify dynamic metadata is properly implemented for pages with variable content.

8. **Produce Review Report**: Generate a structured report with severity-classified findings (Critical, Warning, Suggestion), positive observations, and prioritized recommendations with code examples.

## Examples

### Example 1: Server/Client Component Boundaries

```tsx
// ❌ Bad: Entire page marked as client when only a button needs interactivity
'use client';

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetch(`/api/products/${params.id}`);
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <button onClick={() => addToCart(product.id)}>Add to Cart</button>
    </div>
  );
}

// ✅ Good: Server Component with isolated Client Component
// app/products/[id]/page.tsx (Server Component)
import { AddToCartButton } from './add-to-cart-button';

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  );
}

// app/products/[id]/add-to-cart-button.tsx (Client Component)
'use client';

export function AddToCartButton({ productId }: { productId: string }) {
  return <button onClick={() => addToCart(productId)}>Add to Cart</button>;
}
```

### Example 2: Data Fetching Patterns

```tsx
// ❌ Bad: Sequential data fetching creates waterfall
export default async function DashboardPage() {
  const user = await getUser();
  const orders = await getOrders(user.id);
  const analytics = await getAnalytics(user.id);
  return <Dashboard user={user} orders={orders} analytics={analytics} />;
}

// ✅ Good: Parallel data fetching with proper Suspense boundaries
export default async function DashboardPage() {
  const user = await getUser();
  const [orders, analytics] = await Promise.all([
    getOrders(user.id),
    getAnalytics(user.id),
  ]);
  return <Dashboard user={user} orders={orders} analytics={analytics} />;
}

// ✅ Even better: Streaming with Suspense for independent sections
export default async function DashboardPage() {
  const user = await getUser();
  return (
    <div>
      <UserHeader user={user} />
      <Suspense fallback={<OrdersSkeleton />}>
        <OrdersSection userId={user.id} />
      </Suspense>
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsSection userId={user.id} />
      </Suspense>
    </div>
  );
}
```

### Example 3: Server Actions Security

```tsx
// ❌ Bad: Server Action without validation or authorization
'use server';

export async function deleteUser(id: string) {
  await db.user.delete({ where: { id } });
}

// ✅ Good: Server Action with validation, authorization, and error handling
'use server';

import { z } from 'zod';
import { auth } from '@/lib/auth';
import { revalidatePath } from 'next/cache';

const deleteUserSchema = z.object({ id: z.string().uuid() });

export async function deleteUser(rawData: { id: string }) {
  const session = await auth();
  if (!session || session.user.role !== 'admin') {
    throw new Error('Unauthorized');
  }

  const { id } = deleteUserSchema.parse(rawData);
  await db.user.delete({ where: { id } });
  revalidatePath('/admin/users');
}
```

### Example 4: Caching and Revalidation

```tsx
// ❌ Bad: No cache control, fetches on every request
export default async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());
  return <PostList posts={posts} />;
}

// ✅ Good: Explicit caching with time-based revalidation
export default async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600, tags: ['blog-posts'] },
  }).then(r => r.json());
  return <PostList posts={posts} />;
}

// Revalidation in Server Action
'use server';
export async function publishPost(data: FormData) {
  await db.post.create({ data: parseFormData(data) });
  revalidateTag('blog-posts');
}
```

### Example 5: Middleware Review

```typescript
// ❌ Bad: Middleware runs on all routes including static assets
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
// Missing config.matcher

// ✅ Good: Scoped middleware with proper matcher
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};
```

## Review Output Format

Structure all code review findings as follows:

### 1. Summary
Brief overview with an overall quality score (1-10) and key observations.

### 2. Critical Issues (Must Fix)
Issues causing security vulnerabilities, data exposure, or broken functionality.

### 3. Warnings (Should Fix)
Issues that violate best practices, cause performance problems, or reduce maintainability.

### 4. Suggestions (Consider Improving)
Improvements for code organization, performance, or developer experience.

### 5. Positive Observations
Well-implemented patterns and good practices to acknowledge.

### 6. Recommendations
Prioritized next steps with code examples for the most impactful improvements.

## Best Practices

- Keep `'use client'` boundaries as deep in the tree as possible
- Fetch data in Server Components — avoid client-side fetching for initial data
- Use parallel data fetching (`Promise.all`) to avoid request waterfalls
- Implement proper loading, error, and not-found states for every route segment
- Validate all Server Action inputs with Zod or similar libraries
- Use `revalidatePath`/`revalidateTag` instead of time-based revalidation when possible
- Scope middleware to specific routes with `config.matcher`
- Implement `generateMetadata` for dynamic pages with variable content
- Use `generateStaticParams` for static pages with known parameters
- Avoid importing server-only code in Client Components — use the `server-only` package

## Constraints and Warnings

- This skill targets Next.js App Router — Pages Router patterns may differ significantly
- Respect the project's Next.js version — some features are version-specific
- Do not suggest migrating from Pages Router to App Router unless explicitly requested
- Caching behavior differs between development and production — validate in production builds
- Server Actions must never expose sensitive operations without proper authentication checks
- Focus on high-confidence issues — avoid false positives on style preferences

## References

See the `references/` directory for detailed review checklists and pattern documentation:
- `references/app-router-patterns.md` — App Router best practices and patterns
- `references/server-components.md` — Server Component and Client Component boundary guide
- `references/performance.md` — Next.js performance optimization checklist
