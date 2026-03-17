---
name: trpc-api
description: tRPC end-to-end type-safe API patterns. Router setup, procedures, middleware, context, client configuration. Use when building type-safe APIs with tRPC.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# tRPC API - End-to-End Type Safety

## Purpose

Expert guidance for tRPC v11:

- **Router Setup** - Modular router architecture
- **Procedures** - Queries, mutations, subscriptions
- **Middleware** - Auth, logging, rate limiting
- **Context** - Session, database, utilities
- **Client** - React Query integration

---

## Project Structure

```
server/
├── trpc/
│   ├── index.ts           # Router exports
│   ├── trpc.ts            # tRPC instance
│   ├── context.ts         # Context creation
│   └── routers/
│       ├── user.router.ts
│       ├── post.router.ts
│       └── _app.ts        # Root router
app/
└── api/trpc/[trpc]/route.ts  # Next.js handler
lib/
└── trpc/
    ├── client.ts          # tRPC client
    └── react.tsx          # React Query provider
```

---

## Server Setup

### tRPC Instance

```typescript
// server/trpc/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';
import { type Context } from './context';

const t = initTRPC.context<Context>().create({
	transformer: superjson,
	errorFormatter({ shape, error }) {
		return {
			...shape,
			data: {
				...shape.data,
				zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
			},
		};
	},
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
```

### Context

```typescript
// server/trpc/context.ts
import { type CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { db } from '@db';

export async function createContext(opts: CreateNextContextOptions) {
	const session = await getServerSession(authOptions);

	return {
		session,
		user: session?.user ?? null,
		db,
		req: opts.req,
		res: opts.res,
	};
}

export type Context = Awaited<ReturnType<typeof createContext>>;
```

### Auth Middleware

```typescript
// server/trpc/trpc.ts
const isAuthed = middleware(({ ctx, next }) => {
	if (!ctx.user) {
		throw new TRPCError({
			code: 'UNAUTHORIZED',
			message: 'You must be logged in',
		});
	}
	return next({
		ctx: {
			...ctx,
			user: ctx.user, // User is now guaranteed
		},
	});
});

export const protectedProcedure = t.procedure.use(isAuthed);
```

---

## Router Patterns

### Basic Router

```typescript
// server/trpc/routers/user.router.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = router({
	// Query - fetch data
	getById: publicProcedure
		.input(z.object({ id: z.string().uuid() }))
		.query(async ({ input, ctx }) => {
			const user = await ctx.db.user.findUnique({
				where: { id: input.id },
				select: { id: true, name: true, email: true },
			});

			if (!user) {
				throw new TRPCError({
					code: 'NOT_FOUND',
					message: 'User not found',
				});
			}

			return user;
		}),

	// Mutation - modify data
	updateProfile: protectedProcedure
		.input(
			z.object({
				name: z.string().min(2).max(100),
				bio: z.string().max(500).optional(),
			})
		)
		.mutation(async ({ input, ctx }) => {
			return ctx.db.user.update({
				where: { id: ctx.user.id },
				data: input,
			});
		}),

	// Me - current user
	me: protectedProcedure.query(async ({ ctx }) => {
		return ctx.db.user.findUnique({
			where: { id: ctx.user.id },
		});
	}),
});
```

### Root Router

```typescript
// server/trpc/routers/_app.ts
import { router } from '../trpc';
import { userRouter } from './user.router';
import { postRouter } from './post.router';

export const appRouter = router({
	user: userRouter,
	post: postRouter,
});

export type AppRouter = typeof appRouter;
```

---

## Advanced Patterns

### Pagination

```typescript
const paginationSchema = z.object({
	cursor: z.string().optional(),
	limit: z.number().min(1).max(100).default(20),
});

export const postRouter = router({
	list: publicProcedure.input(paginationSchema).query(async ({ input, ctx }) => {
		const { cursor, limit } = input;

		const posts = await ctx.db.post.findMany({
			take: limit + 1,
			cursor: cursor ? { id: cursor } : undefined,
			orderBy: { createdAt: 'desc' },
		});

		let nextCursor: string | undefined;
		if (posts.length > limit) {
			const nextItem = posts.pop();
			nextCursor = nextItem?.id;
		}

		return {
			items: posts,
			nextCursor,
		};
	}),
});
```

### Optimistic Updates

```typescript
// Client-side with React Query
const utils = trpc.useUtils();

const createPost = trpc.post.create.useMutation({
	onMutate: async (newPost) => {
		// Cancel outgoing refetches
		await utils.post.list.cancel();

		// Snapshot previous value
		const previousPosts = utils.post.list.getData();

		// Optimistically update
		utils.post.list.setData(undefined, (old) => {
			if (!old) return { items: [newPost], nextCursor: undefined };
			return { ...old, items: [newPost, ...old.items] };
		});

		return { previousPosts };
	},

	onError: (err, newPost, context) => {
		// Rollback on error
		utils.post.list.setData(undefined, context?.previousPosts);
	},

	onSettled: () => {
		// Always refetch after error or success
		utils.post.list.invalidate();
	},
});
```

### Batch Requests

```typescript
// tRPC automatically batches by default
// Multiple calls in same tick are batched

const user = trpc.user.me.useQuery();
const posts = trpc.post.list.useQuery();
const notifications = trpc.notification.unread.useQuery();
// These are batched into a single HTTP request
```

---

## Error Handling

### Error Codes

```typescript
throw new TRPCError({
	code: 'NOT_FOUND', // 404
	code: 'BAD_REQUEST', // 400
	code: 'UNAUTHORIZED', // 401
	code: 'FORBIDDEN', // 403
	code: 'CONFLICT', // 409
	code: 'INTERNAL_SERVER_ERROR', // 500
	message: 'Descriptive message',
	cause: originalError,
});
```

### Client Error Handling

```typescript
const mutation = trpc.post.create.useMutation({
	onError: (error) => {
		if (error.data?.code === 'CONFLICT') {
			toast.error('Post with this title already exists');
		} else if (error.data?.zodError) {
			// Validation errors
			const fieldErrors = error.data.zodError.fieldErrors;
			Object.entries(fieldErrors).forEach(([field, errors]) => {
				toast.error(`${field}: ${errors?.join(', ')}`);
			});
		} else {
			toast.error(error.message);
		}
	},
});
```

---

## Client Setup

### React Provider

```typescript
// lib/trpc/react.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { createTRPCReact } from '@trpc/react-query';
import { useState } from 'react';
import superjson from 'superjson';
import { type AppRouter } from '@/server/trpc/routers/_app';

export const trpc = createTRPCReact<AppRouter>();

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 1000,
        refetchOnWindowFocus: false,
      },
    },
  }));

  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
          transformer: superjson,
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

### Usage in Components

```typescript
'use client';

import { trpc } from '@/lib/trpc/react';

export function UserProfile() {
  const { data: user, isLoading } = trpc.user.me.useQuery();
  const updateProfile = trpc.user.updateProfile.useMutation();

  if (isLoading) return <Skeleton />;
  if (!user) return null;

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      updateProfile.mutate({ name: 'New Name' });
    }}>
      <input defaultValue={user.name} />
      <button type="submit" disabled={updateProfile.isPending}>
        Save
      </button>
    </form>
  );
}
```

---

## Next.js Handler

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/trpc/routers/_app';
import { createContext } from '@/server/trpc/context';

const handler = (req: Request) =>
	fetchRequestHandler({
		endpoint: '/api/trpc',
		req,
		router: appRouter,
		createContext: () => createContext({ req }),
	});

export { handler as GET, handler as POST };
```

---

## Agent Integration

This skill is used by:

- **trpc-expert** subagent
- **api-documenter** for API documentation
- **security-auditor** for route validation
- **test-coverage** for API tests

---

## FORBIDDEN

1. **User ID from input** - ALWAYS use `ctx.user.id`
2. **Procedures without `.input()`** - Validate all inputs
3. **`any` in input schemas** - Use proper Zod types
4. **Sensitive data in responses** - Filter with `.select()`
5. **Public procedures for mutations** - Use `protectedProcedure`

---

## Version

- **v1.0.0** - Initial implementation based on tRPC v11 patterns
