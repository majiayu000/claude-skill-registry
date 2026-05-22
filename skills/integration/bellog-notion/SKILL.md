---
name: bellog-notion
description: Provides Notion CMS integration patterns and best practices for Bellog. Triggers when working with Notion data or implementing Notion-based features.
---

# Bellog Notion CMS Integration

This skill defines how to work with Notion as a CMS in the Bellog blog project.

## Architecture Overview

Bellog uses **Notion as a headless CMS**:
- Content is managed in a Notion database
- Data is fetched via Notion API
- Content is rendered using react-notion-x
- Caching with Next.js for performance

## Key Files

- `/src/lib/notion.ts` - Notion API client & queries
- `/src/lib/posts.ts` - Cached data fetching
- `/src/lib/tags.ts` - Tag aggregation
- `/src/types/index.d.ts` - Type definitions
- `/src/app/api/revalidate/route.ts` - Cache invalidation

## Notion Database Schema

### Properties Structure

```typescript
interface NotionPostProperties {
  // Required properties
  title: {
    type: "title";
    title: Array<RichTextItemResponse>;
  };

  date: {
    type: "date";
    date: { start: string } | null;
  };

  description: {
    type: "rich_text";
    rich_text: Array<RichTextItemResponse>;
  };

  slug: {
    type: "rich_text";
    rich_text: Array<RichTextItemResponse>;
  };

  tags: {
    type: "multi_select";
    multi_select: Array<{
      name: string;
      color: string;
    }>;
  };

  status: {
    type: "select";
    select: {
      name: "published" | "draft" | "archived";
    } | null;
  };
}
```

### Field Details

- **title** (Title property) - Post title
- **date** (Date property) - Publication date
- **description** (Rich Text) - Brief summary/excerpt
- **slug** (Rich Text) - URL-friendly identifier
- **tags** (Multi-select) - Post categories/topics
- **status** (Select) - Publication status

## Utility Functions

### From `/src/lib/notion.ts`

#### 1. Get All Published Posts

```typescript
import { getAllPostsFromNotion } from '@/lib/notion';

// Fetches all posts with status = "published"
const posts = await getAllPostsFromNotion();
```

**Returns:**
```typescript
Array<{
  id: string;
  title: string;
  slug: string;
  date: string;
  description: string;
  tags: string[];
  status: string;
}>
```

**Query Details:**
- Filters: `status = "published"`
- Sorts: `date` descending
- Includes: All post properties

#### 2. Get Post by Slug

```typescript
import { getPostBySlugFromNotion } from '@/lib/notion';

const post = await getPostBySlugFromNotion('my-post-slug');
```

**Returns:** Single post object or `null` if not found

#### 3. Get Post Content (RecordMap)

```typescript
import { getPostRecordMap } from '@/lib/notion';

// Get full page content for rendering
const recordMap = await getPostRecordMap(pageId);
```

**Returns:** `ExtendedRecordMap` for react-notion-x

**Use:** When rendering full post content with `NotionRenderer`

## Data Extraction Patterns

### Extract Plain Text from Rich Text

```typescript
function extractPlainText(
  richText: Array<RichTextItemResponse>
): string {
  return richText.map(item => item.plain_text).join('');
}

// Usage
const description = post.properties.description.rich_text
  .map(item => item.plain_text)
  .join('');
```

### Extract Title

```typescript
const title = post.properties.title.title
  .map(item => item.plain_text)
  .join('');
```

### Extract Tags

```typescript
const tags = post.properties.tags.multi_select
  .map(tag => tag.name);
```

### Extract Date

```typescript
const date = post.properties.date.date?.start || '';
```

## Caching Strategy

### Pattern from `/src/lib/posts.ts`

**Two-level caching:**
1. React `cache()` - Request deduplication
2. Next.js `unstable_cache()` - Persistent caching

```typescript
import { cache } from "react";
import { unstable_cache } from "next/cache";
import { getAllPostsFromNotion } from './notion';

export const getAllPosts = cache(
  unstable_cache(
    async () => {
      const posts = await getAllPostsFromNotion();

      // Sort by date descending
      return posts.sort((a, b) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
      );
    },
    ["all-posts"], // Cache key
    {
      revalidate: 3600, // 1 hour
      tags: ["posts", "notion"] // For invalidation
    }
  )
);
```

### Why Two Levels?

- **React cache():** Prevents duplicate fetches in single render
- **unstable_cache():** Persists data across requests with TTL

### Cache Keys

```typescript
["all-posts"]           // All posts list
["post-{slug}"]         // Individual post
["post-recordmap-{id}"] // Post content
```

### Cache Tags

```typescript
["posts", "notion"]     // Tag for bulk invalidation
```

## On-Demand Revalidation

### API Route

**File:** `/src/app/api/revalidate/route.ts`

```typescript
import { revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  // Verify secret
  const secret = request.nextUrl.searchParams.get('secret');

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json(
      { message: 'Invalid secret' },
      { status: 401 }
    );
  }

  // Invalidate cache
  revalidateTag('notion');

  return Response.json({
    revalidated: true,
    now: Date.now()
  });
}
```

### Usage

**Trigger from Notion webhook:**
```bash
curl -X POST "https://bellog.com/api/revalidate?secret=YOUR_SECRET"
```

**Manual trigger:**
```bash
curl -X POST "http://localhost:3000/api/revalidate?secret=dev_secret"
```

### What Gets Revalidated

All cached data with tag `"notion"`:
- Post list
- Individual posts
- Tag counts

## Rendering Notion Content

### With react-notion-x

```typescript
import { NotionRenderer } from 'react-notion-x';
import { getPostRecordMap } from '@/lib/notion';

export default async function PostContent({ postId }: Props) {
  // Fetch content
  const recordMap = await getPostRecordMap(postId);

  return (
    <NotionRenderer
      recordMap={recordMap}
      fullPage={false}
      darkMode={false} // Handle with useTheme in client
      components={{
        // Custom component overrides
        Code: CustomCodeBlock,
        Collection: CustomCollection,
        Equation: CustomEquation
      }}
    />
  );
}
```

### Custom Components

Override default rendering:

```typescript
import { Code } from 'react-notion-x/build/third-party/code';

// Custom code block with line numbers
function CustomCodeBlock({ block }) {
  return (
    <div className="custom-code-wrapper">
      <Code block={block} />
    </div>
  );
}
```

## Environment Variables

### Required in `.env.local`

```bash
# Official Notion API
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# notion-client (for react-notion-x)
NOTION_TOKEN_V2=v02%3Auser_token_or_cookie...
NOTION_ACTIVE_USER=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Cache revalidation
REVALIDATION_SECRET=your_random_secret_string
```

### Getting Values

**NOTION_API_KEY:**
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy "Internal Integration Token"

**NOTION_DATABASE_ID:**
1. Open database in Notion
2. Copy ID from URL: `notion.so/workspace/[THIS_PART]?v=...`

**NOTION_TOKEN_V2:**
1. Open Notion in browser
2. DevTools → Application → Cookies
3. Copy `token_v2` value

**NOTION_ACTIVE_USER:**
1. Same location as token_v2
2. Copy `notion_user_id` value

## Type Safety

### Post Type

```typescript
// /src/types/index.d.ts

export interface Post {
  id: string;
  title: string;
  slug: string;
  date: string;
  description: string;
  tags: string[];
  status: PostStatus;
}

export type PostStatus = 'published' | 'draft' | 'archived';
```

### Accessing Properties

```typescript
// ✅ Type-safe access
import type { QueryDatabaseResponse } from '@notionhq/client/build/src/api-endpoints';

const page = response.results[0] as PageObjectResponse;

if (page.properties.title.type === 'title') {
  const title = page.properties.title.title
    .map(t => t.plain_text)
    .join('');
}
```

## Error Handling

### API Call Errors

```typescript
try {
  const posts = await getAllPostsFromNotion();
  return posts;
} catch (error) {
  console.error('Failed to fetch posts:', error);

  // Return fallback
  return [];

  // Or rethrow for error boundary
  throw new Error('Failed to load posts');
}
```

### Missing Properties

```typescript
// Check property exists and has value
const date = post.properties.date?.date?.start || new Date().toISOString();

// Provide defaults
const description = post.properties.description?.rich_text?.[0]?.plain_text || '';
```

### Notion API Rate Limits

**Limits:**
- 3 requests per second
- Averaged over 1-minute window

**Mitigation:**
- Caching with `unstable_cache`
- Revalidate on-demand instead of frequent polling
- Use TTL (1 hour) to reduce API calls

## Adding New Properties

### Steps

1. **Add to Notion Database**
   - Open database in Notion
   - Add new property with desired type

2. **Update TypeScript Types**
   ```typescript
   // /src/types/index.d.ts
   export interface Post {
     // ... existing fields
     author?: string; // New field
   }
   ```

3. **Extract in Notion Client**
   ```typescript
   // /src/lib/notion.ts
   export async function getAllPostsFromNotion() {
     // ... existing code

     const posts = results.map(page => ({
       // ... existing fields
       author: extractPlainText(page.properties.author.rich_text)
     }));
   }
   ```

4. **Invalidate Cache**
   ```bash
   curl -X POST "http://localhost:3000/api/revalidate?secret=dev_secret"
   ```

## Best Practices

### 1. Always Cache

```typescript
// ✅ Correct - Always use caching
export const getPosts = cache(
  unstable_cache(
    async () => await notion.query(...),
    ['key'],
    { revalidate: 3600 }
  )
);

// ❌ Wrong - Direct API calls
export async function getPosts() {
  return await notion.query(...); // No caching!
}
```

### 2. Handle Missing Data

```typescript
// ✅ Correct - Provide defaults
const title = page.properties.title?.title?.[0]?.plain_text || 'Untitled';

// ❌ Wrong - Can crash if undefined
const title = page.properties.title.title[0].plain_text;
```

### 3. Use Tags for Invalidation

```typescript
// ✅ Correct - Use tags
unstable_cache(
  fetchFunction,
  ['key'],
  { tags: ['posts', 'notion'] } // Can invalidate by tag
);

// ❌ Wrong - No tags
unstable_cache(
  fetchFunction,
  ['key'],
  {} // Can't invalidate efficiently
);
```

### 4. Separate Concerns

```typescript
// ✅ Correct - API calls in notion.ts, caching in posts.ts
// /src/lib/notion.ts
export async function getAllPostsFromNotion() { }

// /src/lib/posts.ts
export const getAllPosts = cache(unstable_cache(...));

// ❌ Wrong - Mix concerns
export const getAllPosts = async () => {
  const response = await notion.databases.query(...); // Mixed!
}
```

### 5. Type Everything

```typescript
// ✅ Correct - Explicit types
import type { PageObjectResponse } from '@notionhq/client/build/src/api-endpoints';

const page = result as PageObjectResponse;

// ❌ Wrong - Any types
const page: any = result;
```

## Performance Tips

### 1. RecordMap Caching

```typescript
// Cache post content separately
export const getPostContent = cache(
  unstable_cache(
    async (id: string) => await getPostRecordMap(id),
    ['post-content'],
    { revalidate: 3600, tags: ['notion'] }
  )
);
```

### 2. Parallel Fetching

```typescript
// Fetch multiple posts in parallel
const [post1, post2] = await Promise.all([
  getPostBySlug('slug-1'),
  getPostBySlug('slug-2')
]);
```

### 3. Partial Revalidation

```typescript
// Only revalidate specific posts
revalidatePath(`/posts/${slug}`);

// Instead of everything
revalidateTag('notion');
```

## Common Patterns

### Get Recent Posts

```typescript
export async function getRecentPosts(limit: number = 5) {
  const allPosts = await getAllPosts();
  return allPosts.slice(0, limit);
}
```

### Filter by Tag

```typescript
export async function getPostsByTag(tag: string) {
  const allPosts = await getAllPosts();
  return allPosts.filter(post => post.tags.includes(tag));
}
```

### Count Posts by Tag

```typescript
// /src/lib/tags.ts
export async function getTagCounts() {
  const posts = await getAllPosts();
  const counts = new Map<string, number>();

  posts.forEach(post => {
    post.tags.forEach(tag => {
      counts.set(tag, (counts.get(tag) || 0) + 1);
    });
  });

  return Array.from(counts.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count);
}
```

## Troubleshooting

### Issue: Stale Data

**Solution:** Trigger revalidation
```bash
curl -X POST "/api/revalidate?secret=YOUR_SECRET"
```

### Issue: Rate Limited

**Check:** Are you calling API too frequently?
**Solution:** Increase cache TTL, reduce manual revalidation

### Issue: Missing Properties

**Check:** Is property name exactly matching?
**Solution:** Use Notion API to inspect property names

### Issue: Empty Content

**Check:** Is NOTION_TOKEN_V2 valid?
**Solution:** Re-copy token from browser cookies

## Quick Reference

```typescript
// Fetch all posts
import { getAllPosts } from '@/lib/posts';
const posts = await getAllPosts();

// Fetch single post
import { getPostBySlugFromNotion } from '@/lib/notion';
const post = await getPostBySlugFromNotion('slug');

// Fetch post content
import { getPostRecordMap } from '@/lib/notion';
const recordMap = await getPostRecordMap(postId);

// Render content
import { NotionRenderer } from 'react-notion-x';
<NotionRenderer recordMap={recordMap} />

// Invalidate cache
revalidateTag('notion');

// Environment variables
NOTION_API_KEY
NOTION_DATABASE_ID
NOTION_TOKEN_V2
NOTION_ACTIVE_USER
REVALIDATION_SECRET
```

Remember: Notion is the source of truth. Always cache and always handle missing data gracefully.
