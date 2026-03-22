---
name: api-cms-payload
description: Payload CMS v3 — TypeScript-native headless CMS with code-first collections, hooks, access control, Local/REST/GraphQL APIs, admin panel, and database adapter pattern
---

# Payload CMS Patterns

> **Quick Guide:** Use Payload for code-first content management with TypeScript. Define collections and globals as config objects with typed fields, hooks, and access control functions. Prefer the Local API (`payload.find`, `payload.create`) for server-side operations. Always generate TypeScript types from your config. Use database adapters (Postgres or MongoDB) and never hardcode credentials. Access control functions receive `{ req }` with the authenticated user. Hooks run at the document lifecycle level (beforeChange, afterChange, etc.) and must not have side effects that block the request unless intentional.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define access control on every collection — open collections are a security risk)**

**(You MUST use the Local API (`payload.find`, `payload.create`) for server-side data operations — it is zero-latency and fully typed)**

**(You MUST generate TypeScript types with `payload generate:types` after every schema change)**

**(You MUST keep JSX/React component imports OUT of the Payload config file — separate config and UI concerns)**

**(You MUST use `overrideAccess: false` when calling the Local API on behalf of a user — the default is `true` which bypasses all access control)**

</critical_requirements>

---

**Auto-detection:** Payload, payload, payloadcms, @payloadcms, buildConfig, CollectionConfig, GlobalConfig, payload.config.ts, payload.find, payload.create, payload.update, payload.delete, payload.findByID, lexicalEditor, richText, beforeChange, afterChange, afterRead, beforeValidate, access control payload, upload collection, imageSizes, versions drafts

**When to use:**

- Configuring `payload.config.ts` with database adapter, collections, and globals
- Defining collection schemas with typed fields (text, richText, relationship, blocks, array, group, upload, select)
- Implementing access control functions (role-based, ownership-based, field-level)
- Writing collection hooks (beforeChange, afterChange, beforeRead, afterRead, beforeValidate, beforeDelete, afterDelete)
- Querying data via Local API, REST API, or GraphQL
- Setting up authentication collections with login, roles, and JWT
- Configuring uploads/media with image sizes and mime type restrictions
- Enabling versions and drafts on collections or globals
- Customizing the admin panel (groups, hidden collections, custom components)

**Key patterns covered:**

- `payload.config.ts` setup with `buildConfig`, database adapters, editor config
- Collection config: slug, fields, hooks, access, auth, upload, versions, admin
- Field types: text, richText, relationship, upload, blocks, array, group, select, tabs, checkbox, date, number, email, code, json, point, radio, textarea, row, collapsible
- Access control: collection-level and field-level, returning boolean or Where query
- Hooks: beforeChange, afterChange, beforeRead, afterRead, beforeValidate, beforeDelete, afterDelete, beforeOperation, afterOperation
- Local API: `payload.find`, `payload.findByID`, `payload.create`, `payload.update`, `payload.delete`, `payload.count`
- REST API: auto-generated endpoints at `/api/{collection-slug}`
- Globals: singleton documents for site settings, navigation, footer
- Auth collections: `auth: true`, roles, login strategies
- Uploads: imageSizes, mimeTypes, media collections
- Versions and drafts: `versions: { drafts: true }`
- TypeScript type generation

**When NOT to use:**

- Simple key-value storage (use a database directly)
- Static site generation without content editing needs
- Applications that only need a REST API without an admin panel (use a plain API framework)
- Client-side data fetching patterns (Payload's Local API is server-only)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core Setup & Collections:**

- [examples/core.md](examples/core.md) — Config setup, collection definitions, field types, access control, hooks

**Advanced Patterns:**

- [examples/advanced.md](examples/advanced.md) — Globals, versions/drafts, uploads/media, auth collections, Local API, REST API

---

<philosophy>

## Philosophy

Payload is a TypeScript-native headless CMS that treats your schema as code. Instead of clicking through a GUI to build content models, you define collections and globals as TypeScript config objects. Payload auto-generates an admin panel, REST API, GraphQL API, and a fully typed Local API from your config.

**Core principles:**

1. **Config-as-code** -- Collections, globals, fields, hooks, and access control are all defined in TypeScript. Your schema is version-controlled, reviewable, and deployable like any other code.
2. **Three APIs from one config** -- Every collection automatically gets a Local API (server-only, zero-latency), REST API (`/api/{slug}`), and GraphQL API. The Local API is the primary interface for server-side operations.
3. **Access control is mandatory** -- Every collection should have explicit `access` functions. By default, Payload denies access to unauthenticated users, but you must define who can do what. Access functions can return a boolean or a `Where` query to scope results.
4. **Hooks for side effects** -- Lifecycle hooks (beforeChange, afterChange, etc.) let you run logic at specific points in the document lifecycle. Keep hooks focused and avoid blocking operations unnecessarily.
5. **Database-agnostic** -- Payload uses database adapters (Postgres via Drizzle, MongoDB via Mongoose). Your collections and fields are defined once and work with any supported database.
6. **Type generation** -- Run `payload generate:types` to produce TypeScript interfaces from your config. This gives you end-to-end type safety from config to API responses.

**When to use Payload:**

- Content-managed applications (blogs, e-commerce, marketing sites)
- Applications needing an admin panel with role-based access
- Projects requiring a typed CMS with version control over the schema
- Multi-tenant applications using access control to scope data per tenant
- Headless CMS backing a frontend framework

**When NOT to use:**

- Pure API servers without content editing needs (use a plain API framework)
- Applications with extremely simple data models (a database + ORM may suffice)
- Client-heavy SPAs where you only need a thin API layer

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: payload.config.ts Setup

The Payload config is the entry point for your entire CMS. It defines the database adapter, collections, globals, editor, and admin settings.

```typescript
// payload.config.ts
import { buildConfig } from "payload";
import { postgresAdapter } from "@payloadcms/db-postgres";
import { lexicalEditor } from "@payloadcms/richtext-lexical";
import { Posts } from "./collections/posts";
import { Users } from "./collections/users";
import { Media } from "./collections/media";
import { SiteSettings } from "./globals/site-settings";

const config = buildConfig({
  db: postgresAdapter({
    pool: {
      connectionString: process.env.DATABASE_URL,
    },
  }),
  editor: lexicalEditor(),
  collections: [Posts, Users, Media],
  globals: [SiteSettings],
  admin: {
    user: Users.slug,
  },
  typescript: {
    outputFile: "./src/payload-types.ts",
  },
  secret: process.env.PAYLOAD_SECRET!,
});

export { config as default };
```

**Why good:** Database adapter configured via environment variable, editor declared once at top level, collections imported from separate files for maintainability, admin user collection specified, TypeScript output path configured, secret from env var

```typescript
// BAD: Everything inline, hardcoded values
import { buildConfig } from "payload";
import { mongooseAdapter } from "@payloadcms/db-mongodb";

export default buildConfig({
  db: mongooseAdapter({ url: "mongodb://localhost/mydb" }), // Hardcoded
  secret: "my-super-secret-key", // Hardcoded secret
  collections: [
    {
      slug: "posts",
      fields: [
        /* 200 lines of inline fields... */
      ],
    },
  ],
});
```

**Why bad:** Hardcoded database URL and secret are security risks, inline collection definitions become unmaintainable at scale, no TypeScript output configured

---

### Pattern 2: Collection Config

Collections are the primary data model in Payload. Each collection generates a database table/collection, admin UI, and API endpoints.

```typescript
// collections/posts.ts
import type { CollectionConfig } from "payload";

const Posts: CollectionConfig = {
  slug: "posts",
  admin: {
    useAsTitle: "title",
    defaultColumns: ["title", "status", "createdAt"],
  },
  access: {
    read: () => true,
    create: ({ req: { user } }) => Boolean(user),
    update: ({ req: { user } }) => Boolean(user),
    delete: ({ req: { user } }) => Boolean(user),
  },
  fields: [
    {
      name: "title",
      type: "text",
      required: true,
    },
    {
      name: "content",
      type: "richText",
    },
    {
      name: "status",
      type: "select",
      defaultValue: "draft",
      options: [
        { label: "Draft", value: "draft" },
        { label: "Published", value: "published" },
      ],
    },
    {
      name: "author",
      type: "relationship",
      relationTo: "users",
      required: true,
    },
    {
      name: "featuredImage",
      type: "upload",
      relationTo: "media",
    },
    {
      name: "publishedDate",
      type: "date",
      admin: {
        date: {
          pickerAppearance: "dayOnly",
        },
      },
    },
  ],
};

export { Posts };
```

**Why good:** Separate file per collection, `useAsTitle` configures admin list display, access control defined per operation, named export, fields use specific types with validation

---

### Pattern 3: Access Control Functions

Access control functions receive `{ req }` with the authenticated user. They return `true`/`false` or a `Where` query to scope results.

#### Collection-Level Access

```typescript
// access/is-admin.ts
import type { Access } from "payload";

const isAdmin: Access = ({ req: { user } }) => {
  if (!user) return false;
  return user.role === "admin";
};

export { isAdmin };

// access/is-admin-or-self.ts
import type { Access } from "payload";

const isAdminOrSelf: Access = ({ req: { user } }) => {
  if (!user) return false;
  if (user.role === "admin") return true;
  // Return a Where query — user can only access their own documents
  return {
    author: {
      equals: user.id,
    },
  };
};

export { isAdminOrSelf };
```

```typescript
// Usage in collection config
const Posts: CollectionConfig = {
  slug: "posts",
  access: {
    read: () => true, // Public read
    create: ({ req: { user } }) => Boolean(user), // Any logged-in user
    update: isAdminOrSelf, // Admin or document owner
    delete: isAdmin, // Admin only
  },
  // ...
};
```

**Why good:** Access functions are reusable across collections, returning a `Where` query scopes results instead of denying access entirely, clear separation between admin-only and self-service operations

#### Field-Level Access

```typescript
const Posts: CollectionConfig = {
  slug: "posts",
  fields: [
    {
      name: "internalNotes",
      type: "textarea",
      access: {
        read: ({ req: { user } }) => user?.role === "admin",
        update: ({ req: { user } }) => user?.role === "admin",
      },
    },
  ],
};
```

**Why good:** Field-level access hides sensitive fields from non-admin users, works independently of collection-level access

---

### Pattern 4: Collection Hooks

Hooks run at specific points in the document lifecycle. They receive typed arguments and can modify data or trigger side effects.

```typescript
// collections/posts.ts
import type { CollectionConfig } from "payload";

const Posts: CollectionConfig = {
  slug: "posts",
  hooks: {
    beforeChange: [
      ({ data, operation, req }) => {
        // Auto-set author on create
        if (operation === "create" && req.user) {
          data.author = req.user.id;
        }
        return data;
      },
    ],
    afterChange: [
      ({ doc, operation, req }) => {
        if (operation === "create") {
          // Trigger notification, revalidate cache, etc.
          req.payload.logger.info(`Post created: ${doc.title}`);
        }
      },
    ],
    beforeRead: [
      ({ doc, req }) => {
        // Runs before the document is returned
        // All locales and hidden fields are available here
        return doc;
      },
    ],
    afterRead: [
      ({ doc, req }) => {
        // Runs after all transforms (locale flattening, field hiding)
        // Last chance to modify before returning to the client
        return doc;
      },
    ],
    beforeDelete: [
      ({ id, req }) => {
        req.payload.logger.info(`Deleting document ${id}`);
      },
    ],
  },
  fields: [
    /* ... */
  ],
};

export { Posts };
```

**Why good:** Hooks are arrays (multiple hooks per lifecycle event), `operation` distinguishes create vs update in beforeChange, `req.payload` provides access to the Local API within hooks, data is returned from beforeChange to pass modifications forward

```typescript
// BAD: Blocking hook with external API call and no error handling
hooks: {
  beforeChange: [
    async ({ data }) => {
      const response = await fetch("https://external-api.com/validate", {
        method: "POST",
        body: JSON.stringify(data),
      });
      // If external API is down, ALL saves fail
      const result = await response.json();
      data.externalId = result.id;
      return data;
    },
  ],
}
```

**Why bad:** External API call in beforeChange blocks every save operation, no error handling means a network failure prevents all document saves, consider using afterChange for non-critical side effects

---

### Pattern 5: Field Types Overview

Payload provides a comprehensive set of field types. Each field has a `name`, `type`, and optional properties like `required`, `unique`, `defaultValue`, `admin`, `access`, and `hooks`.

#### Common Field Types

```typescript
const fields = [
  // Text
  { name: "title", type: "text", required: true, unique: true },

  // Rich Text (Lexical editor)
  { name: "content", type: "richText" },

  // Number
  { name: "price", type: "number", min: 0 },

  // Select (single value)
  {
    name: "status",
    type: "select",
    options: [
      { label: "Draft", value: "draft" },
      { label: "Published", value: "published" },
    ],
  },

  // Checkbox
  { name: "featured", type: "checkbox", defaultValue: false },

  // Date
  { name: "publishedAt", type: "date" },

  // Email
  { name: "contactEmail", type: "email" },

  // Textarea
  { name: "excerpt", type: "textarea", maxLength: 300 },

  // Relationship (to another collection)
  { name: "author", type: "relationship", relationTo: "users" },

  // Upload (to a media collection)
  { name: "image", type: "upload", relationTo: "media" },

  // JSON (arbitrary JSON data)
  { name: "metadata", type: "json" },

  // Code (code editor in admin)
  { name: "customCSS", type: "code", admin: { language: "css" } },

  // Point (geographic coordinates)
  { name: "location", type: "point" },

  // Radio (single choice, displayed as radio buttons)
  {
    name: "priority",
    type: "radio",
    options: [
      { label: "Low", value: "low" },
      { label: "High", value: "high" },
    ],
  },
];
```

#### Structural Field Types

```typescript
const structuralFields = [
  // Group — nested object
  {
    name: "seo",
    type: "group",
    fields: [
      { name: "title", type: "text" },
      { name: "description", type: "textarea" },
    ],
  },

  // Array — repeatable set of fields
  {
    name: "tags",
    type: "array",
    minRows: 1,
    maxRows: 10,
    fields: [
      { name: "label", type: "text", required: true },
      { name: "color", type: "text" },
    ],
  },

  // Blocks — flexible content areas with multiple block types
  {
    name: "layout",
    type: "blocks",
    blocks: [
      {
        slug: "hero",
        fields: [
          { name: "heading", type: "text", required: true },
          { name: "backgroundImage", type: "upload", relationTo: "media" },
        ],
      },
      {
        slug: "content",
        fields: [{ name: "richText", type: "richText" }],
      },
      {
        slug: "cta",
        fields: [
          { name: "label", type: "text", required: true },
          { name: "url", type: "text", required: true },
        ],
      },
    ],
  },

  // Tabs — visual grouping in admin UI (does not affect data shape)
  {
    type: "tabs",
    tabs: [
      {
        label: "Content",
        fields: [
          { name: "title", type: "text" },
          { name: "body", type: "richText" },
        ],
      },
      {
        label: "SEO",
        fields: [
          { name: "metaTitle", type: "text" },
          { name: "metaDescription", type: "textarea" },
        ],
      },
    ],
  },

  // Row — side-by-side fields in admin UI (does not affect data shape)
  {
    type: "row",
    fields: [
      { name: "firstName", type: "text" },
      { name: "lastName", type: "text" },
    ],
  },

  // Collapsible — collapsible section in admin UI (does not affect data shape)
  {
    type: "collapsible",
    label: "Advanced Settings",
    fields: [
      { name: "customClass", type: "text" },
      { name: "htmlId", type: "text" },
    ],
  },
];
```

**Why good:** Fields are strongly typed, structural fields (group, array, blocks) compose to model any content shape, tabs/row/collapsible are admin-only layout helpers that do not affect the data schema

**When to use blocks vs array:** Use **blocks** when content editors need to choose from multiple block types (hero, content, CTA) to build flexible page layouts. Use **array** when every row has the same fields (tags, FAQ items, team members).

---

### Pattern 6: Local API

The Local API is the primary way to query Payload on the server. It is zero-latency (no HTTP overhead), fully typed, and executes hooks and access control.

```typescript
// Server-side usage (API route, server component, script)
import { getPayload } from "payload";
import config from "@payload-config";

async function getPublishedPosts() {
  const payload = await getPayload({ config });

  const PAGE_SIZE = 20;

  const result = await payload.find({
    collection: "posts",
    where: {
      status: { equals: "published" },
    },
    sort: "-createdAt",
    limit: PAGE_SIZE,
    depth: 1,
    overrideAccess: false, // Respect access control
  });

  return result.docs; // Typed as Post[]
}

async function createPost(data: {
  title: string;
  content: object;
  author: string;
}) {
  const payload = await getPayload({ config });

  const post = await payload.create({
    collection: "posts",
    data,
    overrideAccess: false,
  });

  return post; // Typed as Post
}

async function updatePost(
  id: string,
  data: Partial<{ title: string; status: string }>,
) {
  const payload = await getPayload({ config });

  const post = await payload.update({
    collection: "posts",
    id,
    data,
    overrideAccess: false,
  });

  return post;
}

async function deletePost(id: string) {
  const payload = await getPayload({ config });

  await payload.delete({
    collection: "posts",
    id,
    overrideAccess: false,
  });
}
```

**Why good:** `overrideAccess: false` enforces access control (default is `true` which bypasses it), `depth: 1` controls relationship population depth, `sort: "-createdAt"` sorts descending, results are fully typed when types are generated

```typescript
// BAD: Using Local API without access control
const posts = await payload.find({
  collection: "posts",
  // overrideAccess defaults to true — bypasses ALL access control!
});
```

**Why bad:** Without `overrideAccess: false`, access control functions are completely skipped, every user gets admin-level access to all documents

</patterns>

---

<decision_framework>

## Decision Framework

### Which API to Use

```
Where is the code running?
+-- Server-side (API route, server component, script)
|   +-- Local API (zero-latency, fully typed, preferred)
+-- External client (browser, mobile app, third-party)
|   +-- REST API (/api/{collection-slug})
+-- GraphQL client
    +-- GraphQL API (/api/graphql)
```

### Field Type Selection

```
What kind of data?
+-- Single value
|   +-- Short text --> text
|   +-- Long text --> textarea
|   +-- Rich content --> richText
|   +-- Number --> number
|   +-- Boolean --> checkbox
|   +-- Date/time --> date
|   +-- Email --> email
|   +-- Coordinates --> point
|   +-- Code snippet --> code
|   +-- Arbitrary JSON --> json
+-- Choice from options
|   +-- Single choice (dropdown) --> select
|   +-- Single choice (visible) --> radio
|   +-- Linked document --> relationship
|   +-- File/image --> upload
+-- Nested structure
|   +-- Fixed group of fields --> group
|   +-- Repeatable rows (same shape) --> array
|   +-- Flexible content (multiple block types) --> blocks
+-- Admin layout only (no data effect)
    +-- Tabbed sections --> tabs
    +-- Side-by-side fields --> row
    +-- Collapsible section --> collapsible
```

### Access Control Strategy

```
Who should access this data?
+-- Public (anyone) --> read: () => true
+-- Authenticated users only --> read: ({ req: { user } }) => Boolean(user)
+-- Admin only --> read: ({ req: { user } }) => user?.role === 'admin'
+-- Owner only --> read: return Where query matching user.id
+-- Mixed (public read, auth write) --> Different function per operation
+-- Field-level restriction --> access on individual field config
```

### Hooks vs Access Control

```
What do you need to do?
+-- Control WHO can do something --> Access control
+-- Control WHAT happens when they do it --> Hooks
+-- Validate data before saving --> beforeValidate hook or field validation
+-- Transform data before saving --> beforeChange hook
+-- Trigger side effects after saving --> afterChange hook
+-- Filter/transform output --> afterRead hook
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing access control on collections** -- Without explicit `access` functions, Payload denies all access to unauthenticated users but grants full access to any authenticated user. Always define explicit access rules.
- **`overrideAccess` default is `true` in Local API** -- Every `payload.find()`, `payload.create()`, etc. call bypasses access control by default. Always pass `overrideAccess: false` when operating on behalf of a user.
- **Importing JSX/React components in payload.config.ts** -- Payload config runs in a Node context. Importing React components (even transitively) causes bundling errors. Keep config and UI imports completely separate.
- **Hardcoded `secret` or database URL** -- Use environment variables. The Payload secret is used to sign JWTs; hardcoding it is a security vulnerability.

**Medium Priority Issues:**

- **Using `select("*")` equivalent** -- In the Local API, not specifying `select` returns all fields. Use the `select` option to fetch only needed fields for performance.
- **Deep `depth` values** -- Default depth is 2. High depth values cause cascading relationship queries. Set `depth: 0` or `depth: 1` unless you need deeply nested relationships.
- **Blocking hooks with external calls** -- `beforeChange` and `beforeValidate` hooks block the save operation. Move non-critical external API calls to `afterChange` or use background processing.
- **Not running `payload generate:types` after schema changes** -- Stale types lead to runtime errors that TypeScript should have caught at compile time.

**Common Mistakes:**

- **Deep-cloning collection configs** -- `JSON.parse(JSON.stringify(config))` strips hooks and access functions (they are functions, not serializable data). Use spread or Object.assign instead.
- **Forgetting `.select()` equivalent after create/update** -- In the Local API, `payload.create` and `payload.update` return the full document by default. Use the `select` option if you need specific fields.
- **Using `FOR ALL` style access** -- Define separate access functions for `create`, `read`, `update`, `delete` instead of a single function. Different operations have different security requirements.
- **Monorepo version mismatches** -- All packages in a monorepo must use the same version of `payload`, `@payloadcms/*`, `next`, `react`, and `react-dom`. Mismatches cause subtle bundling errors.

**Gotchas & Edge Cases:**

- **`beforeChange` data is a partial on update** -- On `update` operations, `data` contains only the changed fields, not the full document. Use `originalDoc` to access existing values.
- **`beforeChange` has no `id` on create** -- The document ID is not available during `beforeChange` on create operations. If you need the ID, use `afterChange`.
- **`overrideAccess` defaults** -- Local API defaults to `true` (bypass access control). REST and GraphQL always enforce access control. This asymmetry is intentional but catches people off guard.
- **Tabs, rows, and collapsibles do not affect data shape** -- These are admin-only layout fields. A field inside a `tab` is stored at the top level of the document, not nested.
- **Relationship depth cascading** -- Setting `depth: 3` on a collection with circular relationships can cause exponential query growth. Keep depth as low as possible.
- **Auth collections auto-inject fields** -- Collections with `auth: true` automatically get `email`, `hash`, `salt`, `loginAttempts`, and `lockUntil` fields. Do not redefine them.
- **Versions create a separate table** -- Enabling `versions: true` creates a `_posts_versions` table (or equivalent). This can significantly increase storage for high-traffic collections.
- **Access control `Where` queries run as SQL** -- When an access function returns a `Where` query instead of a boolean, it is appended to the database query. Complex `Where` queries can impact database performance.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define access control on every collection — open collections are a security risk)**

**(You MUST use the Local API (`payload.find`, `payload.create`) for server-side data operations — it is zero-latency and fully typed)**

**(You MUST generate TypeScript types with `payload generate:types` after every schema change)**

**(You MUST keep JSX/React component imports OUT of the Payload config file — separate config and UI concerns)**

**(You MUST use `overrideAccess: false` when calling the Local API on behalf of a user — the default is `true` which bypasses all access control)**

**Failure to follow these rules will create security vulnerabilities, type-unsafe operations, and bundling errors.**

</critical_reminders>
