---
name: keystonejs
description: Builds content APIs with KeystoneJS, the Node.js headless CMS with GraphQL. Use when creating admin UIs and APIs with automatic CRUD operations, relationships, access control, and TypeScript support.
---

# KeystoneJS

Open-source Node.js headless CMS that auto-generates GraphQL API and Admin UI from your schema. TypeScript-first with powerful access control.

## Quick Start

```bash
npm create keystone-app@latest my-app
cd my-app
npm run dev
```

Opens:
- Admin UI: `http://localhost:3000`
- GraphQL Playground: `http://localhost:3000/api/graphql`

## Configuration

```typescript
// keystone.ts
import { config } from '@keystone-6/core';
import { lists } from './schema';
import { withAuth, session } from './auth';

export default withAuth(
  config({
    db: {
      provider: 'postgresql',  // or 'sqlite', 'mysql'
      url: process.env.DATABASE_URL!,
    },
    lists,
    session,
    ui: {
      isAccessAllowed: (context) => !!context.session?.data,
    },
  })
);
```

## Schema Definition

```typescript
// schema.ts
import { list } from '@keystone-6/core';
import { text, timestamp, relationship, select, checkbox, password } from '@keystone-6/core/fields';
import { document } from '@keystone-6/fields-document';

export const lists = {
  User: list({
    fields: {
      name: text({ validation: { isRequired: true } }),
      email: text({
        validation: { isRequired: true },
        isIndexed: 'unique',
      }),
      password: password({ validation: { isRequired: true } }),
      posts: relationship({ ref: 'Post.author', many: true }),
    },
  }),

  Post: list({
    fields: {
      title: text({ validation: { isRequired: true } }),
      slug: text({ isIndexed: 'unique' }),
      status: select({
        options: [
          { label: 'Draft', value: 'draft' },
          { label: 'Published', value: 'published' },
        ],
        defaultValue: 'draft',
        ui: { displayMode: 'segmented-control' },
      }),
      content: document({
        formatting: true,
        links: true,
        dividers: true,
        layouts: [
          [1, 1],
          [1, 1, 1],
        ],
      }),
      publishedAt: timestamp(),
      author: relationship({
        ref: 'User.posts',
        ui: {
          displayMode: 'cards',
          cardFields: ['name', 'email'],
          inlineCreate: { fields: ['name', 'email'] },
        },
      }),
      tags: relationship({
        ref: 'Tag.posts',
        many: true,
        ui: {
          displayMode: 'select',
          labelField: 'name',
        },
      }),
    },
    hooks: {
      resolveInput: async ({ resolvedData, inputData }) => {
        // Auto-generate slug from title
        if (inputData.title && !inputData.slug) {
          resolvedData.slug = inputData.title.toLowerCase().replace(/\s+/g, '-');
        }
        return resolvedData;
      },
    },
  }),

  Tag: list({
    fields: {
      name: text({ validation: { isRequired: true } }),
      posts: relationship({ ref: 'Post.tags', many: true }),
    },
  }),
};
```

## Field Types

```typescript
import {
  text,
  password,
  integer,
  float,
  decimal,
  checkbox,
  select,
  multiselect,
  timestamp,
  calendarDay,
  json,
  relationship,
  file,
  image,
} from '@keystone-6/core/fields';
import { document } from '@keystone-6/fields-document';

// Text
text({ validation: { isRequired: true, length: { max: 255 } } })

// Password (hashed)
password({ validation: { isRequired: true } })

// Numbers
integer({ defaultValue: 0 })
float()
decimal({ precision: 10, scale: 2 })

// Boolean
checkbox({ defaultValue: false })

// Select
select({
  options: [
    { label: 'Draft', value: 'draft' },
    { label: 'Published', value: 'published' },
  ],
  defaultValue: 'draft',
})

// Multi-select
multiselect({
  options: [
    { label: 'React', value: 'react' },
    { label: 'Vue', value: 'vue' },
    { label: 'Svelte', value: 'svelte' },
  ],
})

// Dates
timestamp()
calendarDay()

// JSON
json()

// Relationship
relationship({
  ref: 'Post.author',  // Related list.field
  many: false,         // One or many
})

// File upload
file({ storage: 's3' })

// Image with transforms
image({ storage: 'local' })

// Rich text (Document)
document({
  formatting: true,
  links: true,
  dividers: true,
  layouts: [[1, 1]],
})
```

## Access Control

```typescript
import { list } from '@keystone-6/core';

export const lists = {
  Post: list({
    access: {
      operation: {
        query: () => true,  // Anyone can query
        create: ({ session }) => !!session,  // Logged in only
        update: ({ session }) => !!session,
        delete: ({ session }) => session?.data.isAdmin,  // Admin only
      },

      filter: {
        query: ({ session }) => {
          // Non-logged in users only see published
          if (!session) {
            return { status: { equals: 'published' } };
          }
          return true;  // Logged in see all
        },
      },

      item: {
        update: ({ session, item }) => {
          // Users can only update their own posts
          if (session?.data.isAdmin) return true;
          return session?.itemId === item.authorId;
        },
      },
    },
    fields: {/* ... */},
  }),
};
```

## Hooks

```typescript
export const lists = {
  Post: list({
    hooks: {
      // Before validation
      resolveInput: async ({ resolvedData, inputData, item, context }) => {
        // Modify data before saving
        if (inputData.title) {
          resolvedData.slug = inputData.title.toLowerCase().replace(/\s+/g, '-');
        }
        return resolvedData;
      },

      // Validation
      validateInput: async ({ resolvedData, addValidationError }) => {
        if (resolvedData.title?.length < 3) {
          addValidationError('Title must be at least 3 characters');
        }
      },

      // Before save
      beforeOperation: async ({ operation, resolvedData, context }) => {
        if (operation === 'create') {
          // Set author to current user
          resolvedData.author = { connect: { id: context.session?.itemId } };
        }
      },

      // After save
      afterOperation: async ({ operation, item, context }) => {
        if (operation === 'create') {
          console.log(`New post created: ${item.title}`);
          // Send notification, revalidate cache, etc.
        }
      },
    },
    fields: {/* ... */},
  }),
};
```

## GraphQL API

Auto-generated based on your schema.

### Queries

```graphql
# Get all posts
query {
  posts {
    id
    title
    status
    author {
      name
    }
  }
}

# Get single post
query {
  post(where: { id: "123" }) {
    title
    content {
      document
    }
  }
}

# Filter and sort
query {
  posts(
    where: {
      status: { equals: "published" }
      title: { contains: "javascript" }
    }
    orderBy: { publishedAt: desc }
    take: 10
    skip: 0
  ) {
    id
    title
    publishedAt
  }
}

# Count
query {
  postsCount(where: { status: { equals: "published" } })
}
```

### Mutations

```graphql
# Create
mutation {
  createPost(data: {
    title: "New Post"
    content: { document: [...] }
    author: { connect: { id: "user-id" } }
  }) {
    id
    title
  }
}

# Update
mutation {
  updatePost(
    where: { id: "123" }
    data: { title: "Updated Title" }
  ) {
    id
    title
  }
}

# Delete
mutation {
  deletePost(where: { id: "123" }) {
    id
  }
}

# Create many
mutation {
  createPosts(data: [
    { title: "Post 1" },
    { title: "Post 2" }
  ]) {
    id
    title
  }
}
```

### Filter Operators

```graphql
where: {
  # Equality
  title: { equals: "Hello" }
  title: { not: { equals: "Hello" } }

  # String matching
  title: { contains: "react" }
  title: { startsWith: "How to" }
  title: { endsWith: "Guide" }

  # Comparison
  views: { gt: 100 }
  views: { gte: 100 }
  views: { lt: 1000 }
  views: { lte: 1000 }

  # List
  status: { in: ["draft", "review"] }
  status: { notIn: ["archived"] }

  # Relationship
  author: { id: { equals: "user-id" } }
  author: { name: { contains: "John" } }
  tags: { some: { name: { equals: "react" } } }
  tags: { every: { name: { in: ["react", "javascript"] } } }
  tags: { none: { name: { equals: "deprecated" } } }

  # Logical
  AND: [{ status: { equals: "published" } }, { featured: { equals: true } }]
  OR: [{ status: { equals: "published" } }, { author: { id: { equals: "me" } } }]
  NOT: { status: { equals: "archived" } }
}
```

## Query API (Server-Side)

```typescript
// In resolvers, hooks, or custom API routes
const posts = await context.query.Post.findMany({
  where: { status: { equals: 'published' } },
  orderBy: { publishedAt: 'desc' },
  take: 10,
  query: 'id title slug author { name }',
});

const post = await context.query.Post.findOne({
  where: { id: 'post-id' },
  query: 'id title content { document } author { name email }',
});

// Create
const newPost = await context.query.Post.createOne({
  data: {
    title: 'New Post',
    author: { connect: { id: context.session?.itemId } },
  },
  query: 'id title',
});

// Update
await context.query.Post.updateOne({
  where: { id: 'post-id' },
  data: { title: 'Updated' },
});

// Delete
await context.query.Post.deleteOne({
  where: { id: 'post-id' },
});
```

## Authentication

```typescript
// auth.ts
import { createAuth } from '@keystone-6/auth';
import { statelessSessions } from '@keystone-6/core/session';

const { withAuth } = createAuth({
  listKey: 'User',
  identityField: 'email',
  secretField: 'password',
  sessionData: 'id name email isAdmin',
  initFirstItem: {
    fields: ['name', 'email', 'password'],
  },
});

const session = statelessSessions({
  maxAge: 60 * 60 * 24 * 30,  // 30 days
  secret: process.env.SESSION_SECRET!,
});

export { withAuth, session };
```

## File Storage

```typescript
// keystone.ts
import { config } from '@keystone-6/core';

export default config({
  storage: {
    local: {
      kind: 'local',
      type: 'file',
      generateUrl: (path) => `/files${path}`,
      serverRoute: { path: '/files' },
      storagePath: 'public/files',
    },
    s3: {
      kind: 's3',
      type: 'file',
      bucketName: process.env.S3_BUCKET!,
      region: process.env.S3_REGION!,
      accessKeyId: process.env.S3_ACCESS_KEY!,
      secretAccessKey: process.env.S3_SECRET_KEY!,
    },
  },
  // ...
});
```

## Custom GraphQL

```typescript
import { graphql } from '@keystone-6/core';

export const lists = {
  Post: list({
    fields: {/* ... */},
  }),
};

export const extendGraphqlSchema = graphql.extend((base) => ({
  query: {
    featuredPosts: graphql.field({
      type: graphql.list(graphql.nonNull(base.object('Post'))),
      resolve: async (root, args, context) => {
        return context.query.Post.findMany({
          where: { featured: { equals: true } },
          orderBy: { publishedAt: 'desc' },
          take: 5,
        });
      },
    }),
  },
  mutation: {
    publishPost: graphql.field({
      type: base.object('Post'),
      args: { id: graphql.arg({ type: graphql.nonNull(graphql.ID) }) },
      resolve: async (root, { id }, context) => {
        return context.query.Post.updateOne({
          where: { id },
          data: {
            status: 'published',
            publishedAt: new Date().toISOString(),
          },
        });
      },
    }),
  },
}));
```

## Next.js Integration

```typescript
// lib/keystone.ts
const KEYSTONE_URL = process.env.KEYSTONE_URL || 'http://localhost:3000';

export async function fetchGraphQL(query: string, variables = {}) {
  const response = await fetch(`${KEYSTONE_URL}/api/graphql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });

  const { data, errors } = await response.json();

  if (errors) {
    throw new Error(errors[0].message);
  }

  return data;
}

// Typed fetchers
export async function getPosts() {
  const { posts } = await fetchGraphQL(`
    query {
      posts(where: { status: { equals: "published" } }, orderBy: { publishedAt: desc }) {
        id
        title
        slug
        excerpt
        publishedAt
        author { name }
      }
    }
  `);
  return posts;
}

export async function getPost(slug: string) {
  const { posts } = await fetchGraphQL(`
    query GetPost($slug: String!) {
      posts(where: { slug: { equals: $slug } }) {
        id
        title
        content { document }
        author { name }
      }
    }
  `, { slug });
  return posts[0];
}
```

## Deployment

```bash
# Build
npm run build

# Start production
npm run start
```

Database migrations are handled automatically. For production:

1. Use PostgreSQL or MySQL (not SQLite)
2. Set `SESSION_SECRET` environment variable
3. Configure storage for uploads (S3 recommended)

## Best Practices

1. **Use TypeScript** for full type safety
2. **Define access control** for all lists
3. **Use hooks** for business logic and side effects
4. **Extend GraphQL** for custom operations
5. **Set up proper relationships** with `ref` bidirectional references
6. **Use the Query API** for server-side data fetching
