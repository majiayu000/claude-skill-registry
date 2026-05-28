---
name: openapi-to-components
description: >
  Convert Synnovator OpenAPI spec into fully integrated Next.js frontend components.
  Reads .synnovator/openapi.yaml and frontend/components/pages/*.tsx, then generates
  API client (lib/api-client.ts), TypeScript types (lib/types.ts), server-side data
  fetching functions (lib/api/*.ts), and updates existing page components to replace
  hardcoded mock data with real API calls using Next.js App Router Server Components.
  Use when:
  (1) Need to wire frontend components to backend API endpoints
  (2) Want to replace mock/hardcoded data in page components with real API fetching
  (3) Adding a new page component that needs API integration
  (4) Regenerating API types after OpenAPI spec changes
---

# Auto OpenAPI to Components

Generate API client code and update Synnovator frontend components to fetch real data via Next.js Server Components.

## Prerequisites

- OpenAPI spec at `.synnovator/openapi.yaml`
- Frontend components at `frontend/components/pages/*.tsx`
- Mapping reference at `docs/frontend-api-mapping.md` or [references/frontend-api-mapping.md](references/frontend-api-mapping.md)

## Workflow

### Phase 1: Read Inputs

1. Read `.synnovator/openapi.yaml` to get all endpoints, schemas, and enums
2. Read the target component(s) in `frontend/components/pages/` to identify mock data variables and hardcoded values
3. Read [references/frontend-api-mapping.md](references/frontend-api-mapping.md) for the line-by-line mapping of mock data to API endpoints

### Phase 2: Generate API Infrastructure

Generate these files in order:

#### 2.1 TypeScript Types — `frontend/lib/types.ts`

Extract all `components/schemas` from the OpenAPI spec and convert to TypeScript interfaces:

```typescript
// Example: Post schema -> TypeScript interface
export interface Post {
  id: string;
  title: string;
  type: PostType;
  tags: string[];
  status: PostStatus;
  like_count: number;
  comment_count: number;
  average_rating: number | null;
  content?: string;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

export type PostType = "profile" | "team" | "category" | "for_category" | "certificate" | "general";
export type PostStatus = "draft" | "pending_review" | "published" | "rejected";
```

Conversion rules:
- OpenAPI `string` -> `string`
- OpenAPI `integer` -> `number`
- OpenAPI `number` with `format: float` -> `number`
- OpenAPI `boolean` -> `boolean`
- OpenAPI `string` with `format: date-time` -> `string` (ISO 8601)
- OpenAPI `string` with `format: uri` -> `string`
- OpenAPI `string` with `format: email` -> `string`
- OpenAPI `array` with `items` -> `T[]`
- OpenAPI `object` with `additionalProperties` -> `Record<string, T>`
- OpenAPI `enum` -> TypeScript union type
- OpenAPI `$ref` -> reference to another interface
- OpenAPI `default: "null"` -> `| null` union
- Fields listed in `required` are non-optional; others use `?`
- Paginated list schemas -> `PaginatedList<T>` generic

Generate these paginated wrapper:
```typescript
export interface PaginatedList<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
```

#### 2.2 API Client — `frontend/lib/api-client.ts`

Create a typed fetch wrapper for server-side use:

```typescript
const API_BASE = process.env.API_BASE_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit & { params?: Record<string, string | number | boolean | undefined> }
): Promise<T> {
  const { params, ...fetchOptions } = options || {};

  const url = new URL(path, API_BASE);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) url.searchParams.set(key, String(value));
    });
  }

  const res = await fetch(url.toString(), {
    ...fetchOptions,
    headers: {
      "Content-Type": "application/json",
      ...fetchOptions?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(
      res.status,
      body?.error?.code || "UNKNOWN",
      body?.error?.message || res.statusText
    );
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}
```

#### 2.3 Resource-Specific API Functions — `frontend/lib/api/*.ts`

Create one file per OpenAPI tag. Each function maps to one operation in the spec.

File naming: `frontend/lib/api/{tag}.ts` (e.g., `posts.ts`, `categories.ts`, `users.ts`, `groups.ts`, `resources.ts`, `rules.ts`, `interactions.ts`, `admin.ts`)

Pattern for each function:

```typescript
// frontend/lib/api/posts.ts
import { apiFetch } from "../api-client";
import type { Post, PostCreate, PostUpdate, PaginatedList } from "../types";

export async function listPosts(params?: {
  skip?: number;
  limit?: number;
  type?: string;
  status?: string;
  tags?: string[];
}) {
  return apiFetch<PaginatedList<Post>>("/posts", { params, next: { revalidate: 60 } });
}

export async function getPost(postId: string) {
  return apiFetch<Post>(`/posts/${postId}`, { next: { revalidate: 60 } });
}

export async function createPost(data: PostCreate) {
  return apiFetch<Post>("/posts", { method: "POST", body: JSON.stringify(data) });
}
```

Mapping rules from OpenAPI to function names:
- `operationId: list_posts` -> `listPosts`
- `operationId: get_post` -> `getPost`
- `operationId: create_post` -> `createPost`
- `operationId: update_post` -> `updatePost`
- `operationId: delete_post` -> `deletePost`
- Nested operations use compound names: `list_post_comments` -> `listPostComments`

For GET requests, add `next: { revalidate: 60 }` for ISR caching.

### Phase 3: Update Page Components

For each page component, apply these transformations:

#### 3.1 Convert to Async Server Components

Change the component from client-side to async server component:

```typescript
// BEFORE (client component with mock data)
"use client"
const cards = [{ title: "...", author: "..." }]
export function Home() {
  return <div>...</div>
}

// AFTER (server component with real data)
import { listPosts } from "@/lib/api/posts";
import { listCategories } from "@/lib/api/categories";

export default async function Home() {
  const [postsData, categoriesData] = await Promise.all([
    listPosts({ status: "published", limit: 6 }),
    listCategories({ limit: 10 }),
  ]);
  return <div>...</div>
}
```

#### 3.2 Replace Mock Data Variables

For each mock variable identified in the mapping doc:
1. Delete the `const` declaration (e.g., `const cards = [...]`)
2. Add the corresponding API import and call at the top of the async function
3. Update JSX to reference the API response fields

Field mapping from API response to component props:
- `Post.title` -> card title text
- `Post.created_by` -> author ID (requires separate `getUser` call or embed)
- `Post.tags` -> Badge components
- `Post.like_count` -> like counter display
- `Post.comment_count` -> comment counter display
- `Post.content` -> markdown content area
- `Category.name` -> tab/filter label
- `Category.cover_image` -> banner/card image src
- `User.display_name` -> author name text
- `User.avatar_url` -> Avatar image src
- `User.bio` -> user description text
- `Resource.url` -> image/file src
- `Group.name` -> team name text
- `Group.description` -> team description text

#### 3.3 Extract Interactive Parts to Client Components

Server Components cannot use `onClick`, `useState`, `useEffect` etc. Extract interactive UI into separate client components:

```
frontend/components/
├── pages/          (server components - data fetching)
│   └── home.tsx
├── interactive/    (client components - user interactions)
│   ├── like-button.tsx
│   ├── comment-form.tsx
│   └── search-bar.tsx
└── ui/             (existing shadcn components)
```

Interactive elements to extract:
- Like/unlike button -> `components/interactive/like-button.tsx`
- Comment form -> `components/interactive/comment-form.tsx`
- Search bar -> `components/interactive/search-bar.tsx`
- Tab state management -> keep `"use client"` wrapper per tab section
- Follow/unfollow button -> `components/interactive/follow-button.tsx`

Client components use Server Actions for mutations:

```typescript
// frontend/app/actions/posts.ts
"use server"
import { likePost, unlikePost } from "@/lib/api/interactions";

export async function toggleLike(postId: string, isLiked: boolean) {
  if (isLiked) {
    await unlikePost(postId);
  } else {
    await likePost(postId);
  }
}
```

### Phase 4: Validate

After generating all files:
1. Check TypeScript compilation: `npx tsc --noEmit`
2. Verify no broken imports
3. Ensure all `"use client"` directives are only on interactive components
4. Confirm mock data variables have been removed

## Component-to-API Quick Reference

| Component | Primary API calls |
|-----------|-------------------|
| `home.tsx` | `listPosts`, `listCategories`, `getUser` |
| `post-list.tsx` | `listPosts` (type=team), `listPosts` (type=general) |
| `post-detail.tsx` | `getPost`, `getUser`, `listPostComments`, `listPostResources`, `listPostRelated` |
| `proposal-list.tsx` | `listPosts` (type=for_category), `listCategories` |
| `proposal-detail.tsx` | `getPost`, `getUser`, `listPostComments`, `listPostRatings`, `listPostRelated`, `listPostResources` |
| `category-detail.tsx` | `getCategory`, `listCategoryRules`, `listCategoryPosts`, `listCategoryGroups` |
| `user-profile.tsx` | `getUser`, `listPosts` (filtered by user), `listResources` |
| `team.tsx` | `getGroup`, `listGroupMembers`, `getUser` (per member) |
| `assets.tsx` | `listResources` |
| `following-list.tsx` | `listUsers` (API gap: no follow relationship endpoint) |

## API Gaps

These frontend features have no matching API endpoint. Skip integration for these areas and leave mock data with a `// TODO: API gap` comment:

- Follow/unfollow relationships
- Search
- Notifications
- Favorites/bookmarks
- Post version history
- Resource tags, availability, deadline fields
- Group avatar
- Posts filtered by group
- User statistics aggregation
- Category-to-category relationships
