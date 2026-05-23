---
name: nextjs-api-patterns
description: Next.js Route Handlers and Server Actions patterns — validation, error handling, middleware, auth, and rate limiting
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[file path or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: nextjs, api, patterns
---

# Next.js API Patterns

## Overview

Reference guide for building robust API layers in Next.js using Route Handlers and Server Actions. Apply these patterns for validation, error handling, auth, and correct use of each mechanism.

## Route Handler Design

### Basic CRUD Route Handler

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { db } from "@/lib/db";
import { auth } from "@/lib/auth";

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
});

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const page = parseInt(searchParams.get("page") ?? "1");
  const limit = Math.min(parseInt(searchParams.get("limit") ?? "20"), 100);

  const posts = await db.post.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: "desc" },
  });

  const total = await db.post.count();

  return NextResponse.json({
    data: posts,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
  });
}

export async function POST(request: NextRequest) {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const parsed = CreatePostSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const post = await db.post.create({
    data: { ...parsed.data, authorId: session.user.id },
  });

  return NextResponse.json({ data: post }, { status: 201 });
}
```

### Dynamic Route Handler

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from "next/server";

type RouteParams = { params: { id: string } };

export async function GET(_request: NextRequest, { params }: RouteParams) {
  const post = await db.post.findUnique({ where: { id: params.id } });

  if (!post) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json({ data: post });
}

export async function PUT(request: NextRequest, { params }: RouteParams) {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const parsed = UpdatePostSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const post = await db.post.update({
    where: { id: params.id },
    data: parsed.data,
  });

  return NextResponse.json({ data: post });
}

export async function DELETE(_request: NextRequest, { params }: RouteParams) {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  await db.post.delete({ where: { id: params.id } });
  return new NextResponse(null, { status: 204 });
}
```

## Server Actions for Mutations

Server Actions are the preferred way to handle form submissions and mutations in App Router.

### Basic Server Action with Zod

```tsx
// app/posts/actions.ts
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import { db } from "@/lib/db";

const CreatePostSchema = z.object({
  title: z.string().min(1, "Title is required").max(200),
  content: z.string().min(1, "Content is required"),
});

export type ActionState = {
  errors?: Record<string, string[]>;
  message?: string;
};

export async function createPost(
  prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  const session = await auth();
  if (!session) {
    return { message: "Unauthorized" };
  }

  const parsed = CreatePostSchema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  await db.post.create({
    data: { ...parsed.data, authorId: session.user.id },
  });

  revalidatePath("/posts");
  redirect("/posts");
}
```

### Using Server Actions in Client Components

```tsx
// app/posts/CreatePostForm.tsx
"use client";

import { useActionState } from "react";
import { createPost, type ActionState } from "./actions";

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState<ActionState, FormData>(
    createPost,
    {}
  );

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="title">Title</label>
        <input id="title" name="title" required />
        {state.errors?.title && (
          <p className="text-red-500">{state.errors.title[0]}</p>
        )}
      </div>

      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" required />
        {state.errors?.content && (
          <p className="text-red-500">{state.errors.content[0]}</p>
        )}
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Post"}
      </button>

      {state.message && <p className="text-red-500">{state.message}</p>}
    </form>
  );
}
```

## Zod Validation Pattern

Centralize schemas and reuse between client and server.

```tsx
// lib/validations/post.ts
import { z } from "zod";

export const PostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
  tags: z.array(z.string()).max(10).default([]),
});

export const UpdatePostSchema = PostSchema.partial();

export type CreatePostInput = z.infer<typeof PostSchema>;
export type UpdatePostInput = z.infer<typeof UpdatePostSchema>;
```

## Error Handling

### Consistent Error Responses

```tsx
// lib/api-utils.ts
import { NextResponse } from "next/server";

export function apiError(message: string, status: number, details?: unknown) {
  return NextResponse.json(
    { error: message, ...(details && { details }) },
    { status }
  );
}

export function notFound(resource = "Resource") {
  return apiError(`${resource} not found`, 404);
}

export function unauthorized() {
  return apiError("Unauthorized", 401);
}

export function badRequest(message: string, details?: unknown) {
  return apiError(message, 400, details);
}
```

### Route Handler with Error Handling

```tsx
export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const post = await db.post.findUnique({ where: { id: params.id } });
    if (!post) return notFound("Post");
    return NextResponse.json({ data: post });
  } catch (error) {
    console.error("Failed to fetch post:", error);
    return apiError("Internal server error", 500);
  }
}
```

## Middleware Patterns

```tsx
// middleware.ts
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get("session")?.value;
  if (request.nextUrl.pathname.startsWith("/dashboard") && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // CORS headers for API routes
  if (request.nextUrl.pathname.startsWith("/api/")) {
    const response = NextResponse.next();
    response.headers.set("Access-Control-Allow-Origin", "https://myapp.com");
    response.headers.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    response.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
    return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*"],
};
```

## Auth Patterns

### next-auth Session in Route Handlers

```tsx
// app/api/protected/route.ts
import { auth } from "@/auth"; // next-auth v5

export const GET = auth(async function GET(request) {
  if (!request.auth) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const userId = request.auth.user.id;
  const data = await db.userProfile.findUnique({ where: { userId } });
  return NextResponse.json({ data });
});
```

### Auth in Server Actions

```tsx
"use server";

import { auth } from "@/auth";

async function requireAuth() {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error("Unauthorized");
  }
  return session.user;
}

export async function updateProfile(formData: FormData) {
  const user = await requireAuth();
  // ... safe to use user.id
}
```

## Rate Limiting

> **Note:** The in-memory example below is for demonstration only. In serverless or distributed environments (e.g., Vercel), the `Map` resets with each function invocation. For production, use Redis, Upstash, or a similar persistent store.

```tsx
// lib/rate-limit.ts
const rateLimit = new Map<string, { count: number; resetTime: number }>();

export function checkRateLimit(
  key: string,
  limit: number = 10,
  windowMs: number = 60_000
): boolean {
  const now = Date.now();
  const record = rateLimit.get(key);

  if (!record || now > record.resetTime) {
    rateLimit.set(key, { count: 1, resetTime: now + windowMs });
    return true;
  }

  if (record.count >= limit) return false;
  record.count++;
  return true;
}

// Usage in Route Handler
export async function POST(request: NextRequest) {
  const ip = request.headers.get("x-forwarded-for") ?? "unknown";
  if (!checkRateLimit(`post:${ip}`, 5, 60_000)) {
    return apiError("Too many requests", 429);
  }
  // ... handle request
}
```

## Anti-patterns

### Server Actions for Read Operations

Server Actions are for mutations. Use server components or route handlers for reads.

```tsx
// BAD: Server Action to fetch data
"use server";
export async function getUsers() {
  return db.user.findMany(); // This is a read, not a mutation
}

// GOOD: Fetch in a server component directly
export default async function UsersPage() {
  const users = await db.user.findMany();
}
```

### No Input Validation

Never trust client input. Always validate with Zod before touching the database.

### Catching Errors Silently

```tsx
// BAD: Error swallowed
try { await db.post.create({ data }); }
catch (e) { /* silence */ }

// GOOD: Log and return meaningful error
try { await db.post.create({ data }); }
catch (error) {
  console.error("Failed to create post:", error);
  return apiError("Failed to create post", 500);
}
```

### Using API Routes When Server Actions Are Simpler

If a form submission only needs to mutate data and revalidate a path, a Server Action is simpler than building a Route Handler + client-side fetch + loading state.
