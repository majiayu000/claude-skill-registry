---
name: strapi
description: Builds content APIs with Strapi open-source headless CMS. Use when creating self-hosted content management with auto-generated REST/GraphQL APIs, customizable admin panel, and full control over your data.
---

# Strapi CMS

Open-source Node.js headless CMS with auto-generated REST and GraphQL APIs. Self-hosted, customizable, and 100% JavaScript/TypeScript.

## Quick Start

```bash
npx create-strapi@latest my-project
cd my-project
npm run develop
```

Opens admin panel at `http://localhost:1337/admin`. Create your first admin user.

## Content Types

### Via Admin Panel

1. Go to Content-Type Builder
2. Create new Collection Type (e.g., "Article")
3. Add fields: Text, Rich Text, Media, Relation, etc.
4. Save - API auto-generated

### Via Code (Strapi v5)

```typescript
// src/api/article/content-types/article/schema.json
{
  "kind": "collectionType",
  "collectionName": "articles",
  "info": {
    "singularName": "article",
    "pluralName": "articles",
    "displayName": "Article"
  },
  "options": {
    "draftAndPublish": true
  },
  "attributes": {
    "title": {
      "type": "string",
      "required": true
    },
    "slug": {
      "type": "uid",
      "targetField": "title"
    },
    "content": {
      "type": "richtext"
    },
    "cover": {
      "type": "media",
      "allowedTypes": ["images"]
    },
    "author": {
      "type": "relation",
      "relation": "manyToOne",
      "target": "api::author.author",
      "inversedBy": "articles"
    },
    "categories": {
      "type": "relation",
      "relation": "manyToMany",
      "target": "api::category.category"
    },
    "publishedAt": {
      "type": "datetime"
    }
  }
}
```

## REST API

Auto-generated endpoints for each content type.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles` | Get all articles |
| GET | `/api/articles/:id` | Get single article |
| POST | `/api/articles` | Create article |
| PUT | `/api/articles/:id` | Update article |
| DELETE | `/api/articles/:id` | Delete article |

### Fetch Articles

```typescript
// Get all articles
const response = await fetch('http://localhost:1337/api/articles');
const { data } = await response.json();

// Response structure
{
  "data": [
    {
      "id": 1,
      "attributes": {
        "title": "Hello World",
        "slug": "hello-world",
        "content": "...",
        "createdAt": "2024-01-01T00:00:00.000Z",
        "updatedAt": "2024-01-01T00:00:00.000Z",
        "publishedAt": "2024-01-01T00:00:00.000Z"
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pageSize": 25,
      "pageCount": 1,
      "total": 1
    }
  }
}
```

### Query Parameters

```typescript
const params = new URLSearchParams({
  // Populate relations
  'populate': '*',  // or 'populate[0]=author&populate[1]=categories'

  // Filter
  'filters[title][$contains]': 'javascript',
  'filters[publishedAt][$notNull]': 'true',

  // Sort
  'sort[0]': 'publishedAt:desc',

  // Pagination
  'pagination[page]': '1',
  'pagination[pageSize]': '10',

  // Fields selection
  'fields[0]': 'title',
  'fields[1]': 'slug',

  // Locale
  'locale': 'en'
});

const response = await fetch(`http://localhost:1337/api/articles?${params}`);
```

### Filter Operators

```typescript
// Equality
'filters[title][$eq]': 'Hello'

// Not equal
'filters[status][$ne]': 'draft'

// Less/greater than
'filters[price][$lt]': '100'
'filters[price][$lte]': '100'
'filters[price][$gt]': '50'
'filters[price][$gte]': '50'

// Contains (case-sensitive)
'filters[title][$contains]': 'react'

// Contains (case-insensitive)
'filters[title][$containsi]': 'react'

// Starts with
'filters[title][$startsWith]': 'How to'

// In array
'filters[status][$in][0]': 'published'
'filters[status][$in][1]': 'featured'

// Not in array
'filters[status][$notIn][0]': 'draft'

// Null check
'filters[image][$null]': 'true'
'filters[image][$notNull]': 'true'

// Between
'filters[price][$between][0]': '50'
'filters[price][$between][1]': '100'

// Logical operators
'filters[$or][0][title][$contains]': 'react'
'filters[$or][1][title][$contains]': 'vue'

'filters[$and][0][status][$eq]': 'published'
'filters[$and][1][featured][$eq]': 'true'
```

### Populate Relations

```typescript
// Populate all first-level relations
'populate': '*'

// Specific relations
'populate[author]': 'true'
'populate[categories]': 'true'

// Nested populate
'populate[author][populate][0]': 'avatar'

// Deep populate with field selection
'populate[author][fields][0]': 'name'
'populate[author][fields][1]': 'email'
'populate[author][populate][avatar][fields][0]': 'url'

// Populate with filters
'populate[comments][filters][approved][$eq]': 'true'
'populate[comments][sort][0]': 'createdAt:desc'
```

## Client SDK

```bash
npm install @strapi/client
```

```typescript
import { createStrapiClient } from '@strapi/client';

const strapi = createStrapiClient({
  baseURL: 'http://localhost:1337/api',
  auth: {
    token: 'your-api-token'
  }
});

// Get articles
const articles = await strapi.collection('articles').find({
  populate: ['author', 'categories'],
  filters: {
    title: { $contains: 'javascript' }
  },
  sort: ['publishedAt:desc'],
  pagination: { page: 1, pageSize: 10 }
});

// Get single article
const article = await strapi.collection('articles').findOne(1, {
  populate: '*'
});

// Create article
const newArticle = await strapi.collection('articles').create({
  data: {
    title: 'New Article',
    content: 'Article content...'
  }
});

// Update article
await strapi.collection('articles').update(1, {
  data: { title: 'Updated Title' }
});

// Delete article
await strapi.collection('articles').delete(1);
```

## GraphQL

Enable GraphQL plugin:

```bash
npm install @strapi/plugin-graphql
```

```typescript
// Query
const query = `
  query {
    articles(
      filters: { title: { contains: "javascript" } }
      sort: "publishedAt:desc"
      pagination: { page: 1, pageSize: 10 }
    ) {
      data {
        id
        attributes {
          title
          slug
          author {
            data {
              attributes {
                name
              }
            }
          }
        }
      }
      meta {
        pagination {
          total
        }
      }
    }
  }
`;

const response = await fetch('http://localhost:1337/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ query })
});
```

## Authentication

### API Tokens

Create in Admin > Settings > API Tokens.

```typescript
const response = await fetch('http://localhost:1337/api/articles', {
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`
  }
});
```

### User Authentication

```typescript
// Register
const registerResponse = await fetch('http://localhost:1337/api/auth/local/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'user',
    email: 'user@example.com',
    password: 'password123'
  })
});

// Login
const loginResponse = await fetch('http://localhost:1337/api/auth/local', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    identifier: 'user@example.com',
    password: 'password123'
  })
});

const { jwt, user } = await loginResponse.json();

// Use JWT for authenticated requests
const protectedResponse = await fetch('http://localhost:1337/api/articles', {
  headers: {
    'Authorization': `Bearer ${jwt}`
  }
});
```

## Custom Controllers

```typescript
// src/api/article/controllers/article.ts
import { factories } from '@strapi/strapi';

export default factories.createCoreController('api::article.article', ({ strapi }) => ({
  // Override find
  async find(ctx) {
    // Add custom logic
    const { data, meta } = await super.find(ctx);

    // Transform response
    return { data, meta };
  },

  // Custom action
  async featured(ctx) {
    const articles = await strapi.entityService.findMany('api::article.article', {
      filters: { featured: true },
      populate: ['author'],
      limit: 5
    });

    return { data: articles };
  }
}));

// src/api/article/routes/custom.ts
export default {
  routes: [
    {
      method: 'GET',
      path: '/articles/featured',
      handler: 'article.featured'
    }
  ]
};
```

## Custom Services

```typescript
// src/api/article/services/article.ts
import { factories } from '@strapi/strapi';

export default factories.createCoreService('api::article.article', ({ strapi }) => ({
  async findPopular() {
    return strapi.entityService.findMany('api::article.article', {
      filters: { views: { $gt: 1000 } },
      sort: { views: 'desc' },
      limit: 10
    });
  }
}));
```

## Webhooks

Configure in Admin > Settings > Webhooks.

```typescript
// Example webhook payload
{
  "event": "entry.create",
  "model": "article",
  "entry": {
    "id": 1,
    "title": "New Article",
    // ...
  }
}
```

## Next.js Integration

```typescript
// lib/strapi.ts
const STRAPI_URL = process.env.STRAPI_URL || 'http://localhost:1337';
const STRAPI_TOKEN = process.env.STRAPI_TOKEN;

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${STRAPI_URL}/api${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${STRAPI_TOKEN}`,
      ...options.headers
    }
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// Typed fetcher
export async function getArticles() {
  const { data } = await fetchAPI('/articles?populate=*');
  return data;
}

export async function getArticle(slug: string) {
  const { data } = await fetchAPI(
    `/articles?filters[slug][$eq]=${slug}&populate=*`
  );
  return data[0];
}
```

```typescript
// app/articles/[slug]/page.tsx
import { getArticle, getArticles } from '@/lib/strapi';

export async function generateStaticParams() {
  const articles = await getArticles();
  return articles.map((article) => ({
    slug: article.attributes.slug
  }));
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const article = await getArticle(params.slug);

  return (
    <article>
      <h1>{article.attributes.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: article.attributes.content }} />
    </article>
  );
}
```

## Environment Variables

```bash
# .env
HOST=0.0.0.0
PORT=1337
APP_KEYS=key1,key2,key3,key4
API_TOKEN_SALT=your-salt
ADMIN_JWT_SECRET=your-admin-jwt-secret
JWT_SECRET=your-jwt-secret

# Database (PostgreSQL)
DATABASE_CLIENT=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=strapi
DATABASE_USERNAME=strapi
DATABASE_PASSWORD=strapi
```

## Production Deployment

```typescript
// config/env/production/server.ts
export default ({ env }) => ({
  url: env('PUBLIC_URL'),
  proxy: true,
  app: {
    keys: env.array('APP_KEYS')
  }
});

// config/env/production/database.ts
export default ({ env }) => ({
  connection: {
    client: 'postgres',
    connection: {
      connectionString: env('DATABASE_URL'),
      ssl: { rejectUnauthorized: false }
    }
  }
});
```

## Best Practices

1. **Don't modify content types in production** - use migrations
2. **Use PostgreSQL/MySQL** in production (not SQLite)
3. **Create API tokens** for frontend access
4. **Set up proper roles/permissions** for each content type
5. **Use webhooks** to trigger rebuilds/cache invalidation
6. **Store media** in cloud storage (S3, Cloudinary)
