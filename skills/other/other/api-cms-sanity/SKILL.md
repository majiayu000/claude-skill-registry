---
name: api-cms-sanity
description: Structured content platform — GROQ queries, schema definitions, @sanity/client, Portable Text, image handling, real-time listeners, mutations, TypeGen
---

# Sanity Patterns

> **Quick Guide:** Use Sanity for structured content management with GROQ queries, typed schemas via `defineType`/`defineField`, and `@sanity/client` for data fetching. Always set `apiVersion` to a dated string, use `useCdn: true` for public reads, handle draft documents explicitly, use `@sanity/image-url` for image transformations, and render rich text with `@portabletext/react`. Generate TypeScript types with `sanity typegen generate`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always set `apiVersion` on `createClient` to a dated string like `'2025-02-19'` — omitting it uses a legacy API that may break)**

**(You MUST use `useCdn: true` for public read queries and `useCdn: false` when using a token or needing fresh data)**

**(You MUST use parameterized GROQ queries (`$param`) for any dynamic values — never interpolate user input into GROQ strings)**

**(You MUST handle drafts explicitly — draft documents have `_id` prefixed with `drafts.` and are not returned by default with `perspective: 'published'`)**

**(You MUST use `defineQuery()` from `groq` and assign queries to named variables for TypeGen type generation)**

</critical_requirements>

---

**Auto-detection:** Sanity, sanity, @sanity/client, createClient, GROQ, groq, defineType, defineField, defineArrayMember, @sanity/image-url, urlFor, @portabletext/react, PortableText, portable text, block content, sanity.config, sanity.cli, typegen, sanity studio, content lake

**When to use:**

- Setting up `@sanity/client` with `createClient` for data fetching
- Writing GROQ queries (filters, projections, joins, ordering, slicing)
- Defining content schemas with `defineType`, `defineField`, `defineArrayMember`
- Rendering Portable Text (block content) with `@portabletext/react`
- Generating image URLs with `@sanity/image-url` (responsive images, crops, hotspots)
- Performing mutations (create, patch, delete, transactions)
- Setting up real-time listeners with `client.listen()`
- Generating TypeScript types with Sanity TypeGen

**Key patterns covered:**

- Client setup with `createClient` and `apiVersion` configuration
- GROQ query language: filters, projections, ordering, slicing, joins, references
- Schema definitions: document types, object types, arrays, references, images
- Portable Text rendering with custom components
- Image URL builder with responsive images and transformations
- Mutations: create, createOrReplace, patch, delete, transactions
- Real-time listeners via `client.listen()`
- TypeGen for type-safe GROQ queries with `defineQuery()`

**When NOT to use:**

- GraphQL-only APIs (Sanity supports GROQ primarily; use GraphQL skill if needed)
- Direct database access (Sanity is a hosted content lake, not a database)
- Non-Sanity CMS platforms (use dedicated skills for Contentful, Strapi, etc.)

**Detailed Resources:**

- For decision frameworks and quick-reference tables, see [reference.md](reference.md)

**Client & GROQ:**

- [examples/core.md](examples/core.md) — Client setup, GROQ queries, error handling, TypeGen

**Schemas:**

- [examples/schemas.md](examples/schemas.md) — defineType, defineField, document types, object types, references, images

**Rich Content:**

- [examples/rich-content.md](examples/rich-content.md) — Portable Text rendering, image URL builder, responsive images

**Mutations & Real-time:**

- [examples/mutations.md](examples/mutations.md) — Create, patch, delete, transactions, real-time listeners

---

<philosophy>

## Philosophy

Sanity is a structured content platform built around a real-time content lake, GROQ (Graph-Relational Object Queries) as its query language, and Sanity Studio as a customizable editing environment.

**Core principles:**

1. **Structured content** — Content is defined by schemas (`defineType`, `defineField`) that describe shape, validation, and editorial UI. Schemas are code, not configuration files.
2. **GROQ-first querying** — GROQ lets you filter, project, join, and reshape data in a single query. Unlike REST or GraphQL, GROQ queries return exactly the shape you define in the projection.
3. **Content as data** — Rich text is stored as Portable Text (a JSON-based specification), making it renderable in any frontend framework without vendor lock-in.
4. **API versioning** — Every client must specify an `apiVersion` date string. This pins your code to a specific API behavior, preventing breaking changes from affecting production.
5. **CDN caching** — Public read queries use `useCdn: true` for edge-cached responses. Mutations and authenticated reads use `useCdn: false` for fresh data.
6. **Type generation** — Sanity TypeGen generates TypeScript types from both your schemas and GROQ queries, enabling end-to-end type safety from content model to frontend.

**When to use Sanity:**

- Content-driven websites and applications (blogs, marketing sites, documentation)
- Projects needing real-time collaborative editing in a customizable studio
- Multi-channel content delivery (web, mobile, IoT) from a single content source
- Teams wanting type-safe content queries with GROQ and TypeGen

**When NOT to use:**

- Transactional data requiring ACID guarantees (use a database)
- User-generated content at massive scale (Sanity is optimized for editorial content)
- Projects needing a self-hosted CMS (Sanity's content lake is hosted, though the Studio is open source)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup with createClient

Configure `@sanity/client` with your project ID, dataset, API version, and CDN preference.

```typescript
// lib/sanity-client.ts
import { createClient } from "@sanity/client";

const PROJECT_ID = process.env.SANITY_PROJECT_ID!;
const DATASET = process.env.SANITY_DATASET!;
const API_VERSION = "2025-02-19";

export const client = createClient({
  projectId: PROJECT_ID,
  dataset: DATASET,
  apiVersion: API_VERSION,
  useCdn: true, // true for public reads, false for authenticated/fresh data
});
```

**Why good:** `apiVersion` pins API behavior, `useCdn: true` for cached reads, named constants for environment variables, no hardcoded credentials

```typescript
// BAD: Missing apiVersion, hardcoded credentials
import { createClient } from "@sanity/client";

const client = createClient({
  projectId: "abc123",
  dataset: "production",
  // No apiVersion — uses legacy API behavior
});
```

**Why bad:** No `apiVersion` causes unpredictable API behavior across deployments, hardcoded project ID belongs in environment variables, no `useCdn` specified

---

### Pattern 2: GROQ Queries with Filters and Projections

GROQ queries combine filters (what to fetch), projections (what shape to return), and ordering/slicing (how to sort and paginate).

#### Basic Query Structure

```typescript
import { defineQuery } from "groq";

// Filter → Projection → Order → Slice
const POSTS_QUERY = defineQuery(`
  *[_type == "post" && published == true]{
    _id,
    title,
    slug,
    "authorName": author->name,
    "categoryTitle": category->title,
    publishedAt
  } | order(publishedAt desc) [0...10]
`);
```

#### Parameterized Queries

```typescript
const POST_BY_SLUG_QUERY = defineQuery(`
  *[_type == "post" && slug.current == $slug][0]{
    _id,
    title,
    body,
    "author": author->{name, image},
    "categories": categories[]->title
  }
`);

// Always pass dynamic values as parameters
const post = await client.fetch(POST_BY_SLUG_QUERY, { slug: "my-post" });
```

**Why good:** `defineQuery()` enables TypeGen type inference, parameters prevent GROQ injection, projection returns only needed fields, `[0]` returns a single object instead of an array, reference joins via `->` operator

```groq
// BAD: String interpolation in GROQ
const query = `*[_type == "post" && slug.current == "${userInput}"]`;
// GROQ injection vulnerability!
```

**Why bad:** String interpolation allows GROQ injection attacks — always use `$param` parameters

---

### Pattern 3: Schema Definitions with defineType and defineField

Schemas define content structure, validation, and Studio UI. Use `defineType`, `defineField`, and `defineArrayMember` for type safety.

#### Document Type

```typescript
// schemas/post.ts
import { defineType, defineField, defineArrayMember } from "sanity";

export const postType = defineType({
  name: "post",
  title: "Post",
  type: "document",
  fields: [
    defineField({
      name: "title",
      title: "Title",
      type: "string",
      validation: (rule) => rule.required().min(5).max(100),
    }),
    defineField({
      name: "slug",
      title: "Slug",
      type: "slug",
      options: { source: "title", maxLength: 96 },
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: "author",
      title: "Author",
      type: "reference",
      to: [{ type: "author" }],
    }),
    defineField({
      name: "body",
      title: "Body",
      type: "array",
      of: [
        defineArrayMember({ type: "block" }),
        defineArrayMember({ type: "image", options: { hotspot: true } }),
      ],
    }),
    defineField({
      name: "publishedAt",
      title: "Published At",
      type: "datetime",
    }),
  ],
  preview: {
    select: { title: "title", author: "author.name", media: "mainImage" },
    prepare(selection) {
      const { author } = selection;
      return { ...selection, subtitle: author ? `by ${author}` : "" };
    },
  },
});
```

**Why good:** `defineType`/`defineField` provide IDE autocomplete and type checking, validation rules enforce content quality, slug generated from title, `hotspot: true` enables focal point cropping, preview customizes Studio list appearance

---

### Pattern 4: Portable Text Rendering

Render Sanity's block content (Portable Text) using `@portabletext/react` with custom components for non-standard blocks and marks.

```tsx
import { PortableText } from "@portabletext/react";
import type { PortableTextComponents } from "@portabletext/react";

const components: PortableTextComponents = {
  types: {
    image: ({ value }) => {
      if (!value?.asset?._ref) return null;
      return (
        <figure>
          <img src={urlFor(value).width(800).url()} alt={value.alt || ""} />
          {value.caption && <figcaption>{value.caption}</figcaption>}
        </figure>
      );
    },
    code: ({ value }) => (
      <pre data-language={value.language}>
        <code>{value.code}</code>
      </pre>
    ),
  },
  marks: {
    link: ({ children, value }) => {
      const rel = value.href?.startsWith("/")
        ? undefined
        : "noopener noreferrer";
      const target = value.href?.startsWith("/") ? undefined : "_blank";
      return (
        <a href={value.href} rel={rel} target={target}>
          {children}
        </a>
      );
    },
    highlight: ({ children }) => <mark>{children}</mark>,
  },
  block: {
    h2: ({ children }) => <h2 id={children?.toString()}>{children}</h2>,
    blockquote: ({ children }) => <blockquote>{children}</blockquote>,
  },
};

// Usage
function ArticleBody({ body }: { body: PortableTextBlock[] }) {
  return <PortableText value={body} components={components} />;
}
export { ArticleBody };
```

**Why good:** Custom components for image, code, link, and heading blocks; external links get `noopener noreferrer`; images use `urlFor` for optimized URLs; fallback for missing assets; named export

---

### Pattern 5: Image URL Builder

Use `@sanity/image-url` to generate optimized, responsive image URLs with automatic crop and hotspot support.

```typescript
// lib/sanity-image.ts
import { createImageUrlBuilder } from "@sanity/image-url";
import type { SanityImageSource } from "@sanity/image-url";
import { client } from "./sanity-client";

const builder = createImageUrlBuilder(client);

export function urlFor(source: SanityImageSource) {
  return builder.image(source);
}
```

#### Responsive Images

```tsx
const WIDTHS = [400, 800, 1200] as const;

function ResponsiveImage({
  image,
  alt,
}: {
  image: SanityImageSource;
  alt: string;
}) {
  return (
    <img
      src={urlFor(image).width(800).auto("format").url()}
      srcSet={WIDTHS.map(
        (w) => `${urlFor(image).width(w).auto("format").url()} ${w}w`,
      ).join(", ")}
      sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
      alt={alt}
      loading="lazy"
    />
  );
}
export { ResponsiveImage };
```

**Why good:** `createImageUrlBuilder` initializes from client config, `urlFor` helper is reusable, `.auto("format")` serves WebP/AVIF when supported, responsive `srcSet` with named width constants, lazy loading for performance, crop/hotspot applied automatically from the full image field

---

### Pattern 6: Mutations (Create, Patch, Delete)

Use `@sanity/client` methods for creating, updating, and deleting documents.

#### Create

```typescript
const newPost = await client.create({
  _type: "post",
  title: "New Post",
  slug: { _type: "slug", current: "new-post" },
  publishedAt: new Date().toISOString(),
});
```

#### Create or Replace

```typescript
// Overwrites entirely if document exists, creates if it doesn't
await client.createOrReplace({
  _id: "singleton-settings",
  _type: "siteSettings",
  title: "My Site",
  description: "Site description",
});
```

#### Patch

```typescript
// Set fields
await client.patch("post-123").set({ title: "Updated Title" }).commit();

// Increment a number field
await client.patch("post-123").inc({ viewCount: 1 }).commit();

// Unset (remove) a field
await client.patch("post-123").unset(["temporaryField"]).commit();

// Insert into an array at a specific position
await client
  .patch("post-123")
  .insert("after", "tags[-1]", [{ _key: "abc", label: "new-tag" }])
  .commit();
```

#### Delete

```typescript
await client.delete("post-123");
```

#### Transaction (Atomic Multi-Mutation)

```typescript
await client
  .transaction()
  .create({ _type: "log", message: "Post archived" })
  .patch("post-123", (p) => p.set({ archived: true }))
  .commit();
```

**Why good:** `.commit()` required on patches and transactions, `createOrReplace` for singletons, `_key` required for array items, transactions group related mutations atomically

---

### Pattern 7: Real-Time Listeners

Subscribe to document changes with `client.listen()` using a GROQ filter.

```typescript
// Listen for new/updated published posts
const LISTENER_QUERY = `*[_type == "post" && published == true]`;

const subscription = client.listen(LISTENER_QUERY).subscribe({
  next: (update) => {
    if (update.type === "mutation") {
      console.log(`Document ${update.documentId} was ${update.transition}`);
      // update.transition: 'update' | 'appear' | 'disappear'
      // update.result contains the document if it matched the filter
    }
  },
  error: (err) => {
    console.error("Listener error:", err.message);
  },
});

// Cleanup: unsubscribe when done
subscription.unsubscribe();
```

**Why good:** GROQ filter scopes to relevant documents, observable-based subscription with error handling, cleanup via `unsubscribe()`, `transition` field indicates what happened to the document

**When to use:** Preview mode, live dashboards, collaborative editing indicators. For production frontends, evaluate the newer Live Content API as a simpler alternative.

---

### Pattern 8: TypeGen for Type-Safe GROQ

Use Sanity TypeGen to generate TypeScript types from schemas and GROQ queries.

#### Configuration

```typescript
// sanity.cli.ts
import { defineCliConfig } from "sanity/cli";

// NOTE: default export required by Sanity CLI tooling
export default defineCliConfig({
  api: {
    projectId: "your-project-id",
    dataset: "production",
  },
  typegen: {
    enabled: true,
    path: "./src/**/*.{ts,tsx}",
    schema: "schema.json",
    generates: "./sanity.types.ts",
    overloadClientMethods: true,
  },
});
```

#### Query with defineQuery

```typescript
// queries/post-queries.ts
import { defineQuery } from "groq";

export const allPostsQuery = defineQuery(`
  *[_type == "post" && published == true]{
    _id,
    title,
    slug,
    publishedAt
  } | order(publishedAt desc)
`);

export const postBySlugQuery = defineQuery(`
  *[_type == "post" && slug.current == $slug][0]{
    _id,
    title,
    body,
    "author": author->{name, image}
  }
`);
```

#### Using Generated Types

```typescript
import type {
  AllPostsQueryResult,
  PostBySlugQueryResult,
} from "./sanity.types";
import { allPostsQuery, postBySlugQuery } from "./queries/post-queries";

// Return type is automatically inferred when overloadClientMethods is true
const posts = await client.fetch(allPostsQuery);
// posts: AllPostsQueryResult

const post = await client.fetch(postBySlugQuery, { slug: "my-post" });
// post: PostBySlugQueryResult
```

**Why good:** `defineQuery()` enables TypeGen to find and type queries, `overloadClientMethods: true` makes `client.fetch` return typed results, queries in dedicated files for organization, generated types update automatically during `sanity dev`

```typescript
// BAD: Inline query without defineQuery
const posts = await client.fetch(`*[_type == "post"]{ title }`);
// TypeGen cannot generate types for inline queries
// posts is typed as 'any'
```

**Why bad:** TypeGen requires queries assigned to variables using `defineQuery()` or the `groq` template literal — inline strings produce untyped results

</patterns>

---

<decision_framework>

## Decision Framework

### useCdn: true vs false

```
Is the data public and non-personalized?
├─ YES → useCdn: true (edge-cached, fast)
└─ NO →
    ├─ Using a token for authenticated reads? → useCdn: false
    ├─ Need real-time fresh data (preview)? → useCdn: false
    └─ Performing mutations? → useCdn: false
```

### Draft Handling

```
Do you need draft documents?
├─ YES → Use perspective: 'previewDrafts' (requires token)
├─ NO → Use perspective: 'published' (default since API v2025-02-19)
└─ Mixed (preview mode toggle)?
    └─ Create two clients: one public (useCdn: true), one preview (token + useCdn: false)
```

### GROQ Query Return Shape

```
How many documents do you expect?
├─ One (by ID, slug, singleton) → Add [0] at end (returns object or null)
├─ Many (list, feed) → No slice suffix (returns array)
└─ Paginated → Add [start...end] slice
```

### Image Handling

```
How should images be delivered?
├─ Fixed size (thumbnails, avatars) → urlFor(img).width(W).height(H).url()
├─ Responsive (article images) → srcSet with multiple widths
├─ Format optimization → .auto('format') for WebP/AVIF
└─ Cropped to aspect ratio → .width(W).height(H).fit('crop')
```

### Mutation Method Selection

```
What operation do you need?
├─ Create new document → client.create()
├─ Create or fully replace → client.createOrReplace() (for singletons)
├─ Create only if missing → client.createIfNotExists()
├─ Update specific fields → client.patch(id).set({...}).commit()
├─ Remove fields → client.patch(id).unset([...]).commit()
├─ Multiple related changes → client.transaction()...commit()
└─ Delete document → client.delete(id)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing `apiVersion` on client** — Omitting `apiVersion` uses legacy API behavior that may change without notice. Always pin to a date string.
- **String interpolation in GROQ queries** — Interpolating user input into GROQ strings enables GROQ injection. Always use `$param` parameters.
- **Using `useCdn: true` with a token** — CDN-cached responses ignore authentication tokens. Authenticated queries must use `useCdn: false`.
- **Accessing draft documents without a token** — Drafts (`drafts.*` documents) require an API token and `perspective: 'previewDrafts'`. Without a token, drafts are invisible.

**Medium Priority Issues:**

- **Fetching all fields with `{...}` when only a few are needed** — Over-fetching wastes bandwidth and CDN cache efficiency. Project only the fields you need.
- **Missing `.commit()` on patches** — `client.patch(id).set({...})` without `.commit()` does nothing — the mutation is never sent.
- **Not using `defineQuery()` for GROQ queries** — TypeGen cannot generate types for queries that aren't wrapped in `defineQuery()` or assigned to named variables.
- **Hardcoded project ID or dataset** — Use environment variables; hardcoded values prevent environment switching and leak project details.
- **Using deprecated `@sanity/block-content-to-react`** — Replaced by `@portabletext/react`. The old package is unmaintained.

**Common Mistakes:**

- **Forgetting `_key` on array items in mutations** — Every item in a Sanity array must have a unique `_key` field. Mutations without `_key` will fail.
- **Using `_id` with `client.create()`** — `create()` generates a random `_id`. If you specify `_id` and the document exists, it errors. Use `createOrReplace()` or `createIfNotExists()` for idempotent operations.
- **Not handling the case where `[0]` returns `null`** — A GROQ query ending in `[0]` returns `null` if no documents match, not an empty object.
- **Expecting `client.listen()` to work with projections** — The listener only uses the filter portion of a GROQ query. Projections, ordering, and slicing are ignored.

**Gotchas & Edge Cases:**

- **API version `2025-02-19` changed default perspective** — Before this version, the default perspective was `raw` (includes drafts). After, it defaults to `published`. Existing code may break if you update `apiVersion` without accounting for this.
- **CDN cache is eventual** — After a mutation, CDN-cached queries (`useCdn: true`) may return stale data for a few seconds. Use `useCdn: false` or add a small delay for consistency-critical reads after writes.
- **Slug fields store value in `.current`** — Query `slug.current`, not `slug` directly. `*[slug == "my-slug"]` will never match.
- **Image fields require the full object for crop/hotspot** — Passing only `asset._ref` to `urlFor()` works for basic URLs but loses crop and hotspot metadata. Pass the entire image field object.
- **Portable Text arrays need `_key` on every block** — When creating Portable Text content programmatically, every block and inline object needs a unique `_key`.
- **`client.listen()` reconnects automatically** — But there's no built-in guarantee against missed events during reconnection. For critical use cases, combine with periodic re-fetching.
- **TypeGen requires `schema.json` extraction first** — Run `npx sanity schema extract` before `npx sanity typegen generate`. The extract step reads your Studio schemas and outputs a JSON representation.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always set `apiVersion` on `createClient` to a dated string like `'2025-02-19'` — omitting it uses a legacy API that may break)**

**(You MUST use `useCdn: true` for public read queries and `useCdn: false` when using a token or needing fresh data)**

**(You MUST use parameterized GROQ queries (`$param`) for any dynamic values — never interpolate user input into GROQ strings)**

**(You MUST handle drafts explicitly — draft documents have `_id` prefixed with `drafts.` and are not returned by default with `perspective: 'published'`)**

**(You MUST use `defineQuery()` from `groq` and assign queries to named variables for TypeGen type generation)**

**Failure to follow these rules will cause unpredictable API behavior, GROQ injection vulnerabilities, and untyped query results.**

</critical_reminders>
