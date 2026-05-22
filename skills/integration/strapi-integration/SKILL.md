---
name: Strapi Integration
description: Integrating with Strapi open-source headless CMS built with Node.js, including setup, content types, customization, API integration, and deployment patterns.
---

# Strapi Integration

> **Current Level:** Intermediate  
> **Domain:** Content Management / Backend

---

## Overview

Strapi is an open-source headless CMS built with Node.js. This guide covers setup, content types, customization, and integration patterns for building content-driven applications with a developer-friendly CMS.

## Strapi Setup

```bash
# Create new Strapi project
npx create-strapi-app@latest my-project --quickstart

# Or with custom database
npx create-strapi-app@latest my-project \
  --dbclient=postgres \
  --dbhost=localhost \
  --dbport=5432 \
  --dbname=strapi \
  --dbusername=postgres \
  --dbpassword=password

# Start development server
npm run develop
```

## Content Types

### Single Types

```javascript
// src/api/homepage/content-types/homepage/schema.json
{
  "kind": "singleType",
  "collectionName": "homepages",
  "info": {
    "singularName": "homepage",
    "pluralName": "homepages",
    "displayName": "Homepage"
  },
  "options": {
    "draftAndPublish": true
  },
  "attributes": {
    "hero": {
      "type": "component",
      "repeatable": false,
      "component": "sections.hero"
    },
    "features": {
      "type": "component",
      "repeatable": true,
      "component": "sections.feature"
    },
    "seo": {
      "type": "component",
      "repeatable": false,
      "component": "shared.seo"
    }
  }
}
```

### Collection Types

```javascript
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
    "excerpt": {
      "type": "text",
      "maxLength": 200
    },
    "coverImage": {
      "type": "media",
      "multiple": false,
      "required": true,
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
      "target": "api::category.category",
      "inversedBy": "articles"
    },
    "publishedAt": {
      "type": "datetime"
    },
    "seo": {
      "type": "component",
      "repeatable": false,
      "component": "shared.seo"
    }
  }
}
```

## Components and Dynamic Zones

```javascript
// src/components/sections/hero.json
{
  "collectionName": "components_sections_heroes",
  "info": {
    "displayName": "Hero",
    "icon": "star"
  },
  "options": {},
  "attributes": {
    "title": {
      "type": "string",
      "required": true
    },
    "subtitle": {
      "type": "text"
    },
    "image": {
      "type": "media",
      "multiple": false,
      "required": true,
      "allowedTypes": ["images"]
    },
    "buttons": {
      "type": "component",
      "repeatable": true,
      "component": "elements.button"
    }
  }
}

// Dynamic Zone in content type
{
  "attributes": {
    "blocks": {
      "type": "dynamiczone",
      "components": [
        "sections.hero",
        "sections.features",
        "sections.testimonials",
        "sections.cta"
      ]
    }
  }
}
```

## API Integration

### REST API

```typescript
// services/strapi-client.service.ts
import axios, { AxiosInstance } from 'axios';

export class StrapiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.STRAPI_API_URL || 'http://localhost:1337/api',
      headers: {
        'Authorization': `Bearer ${process.env.STRAPI_API_TOKEN}`
      }
    });
  }

  async getArticles(params?: QueryParams): Promise<Article[]> {
    const response = await this.client.get('/articles', {
      params: {
        populate: '*',
        ...params
      }
    });

    return response.data.data;
  }

  async getArticle(slug: string): Promise<Article> {
    const response = await this.client.get('/articles', {
      params: {
        filters: { slug: { $eq: slug } },
        populate: 'deep'
      }
    });

    return response.data.data[0];
  }

  async getHomepage(): Promise<Homepage> {
    const response = await this.client.get('/homepage', {
      params: {
        populate: 'deep'
      }
    });

    return response.data.data;
  }

  async createArticle(data: CreateArticleDto): Promise<Article> {
    const response = await this.client.post('/articles', {
      data
    });

    return response.data.data;
  }

  async updateArticle(id: number, data: Partial<Article>): Promise<Article> {
    const response = await this.client.put(`/articles/${id}`, {
      data
    });

    return response.data.data;
  }

  async deleteArticle(id: number): Promise<void> {
    await this.client.delete(`/articles/${id}`);
  }
}

interface QueryParams {
  sort?: string;
  filters?: any;
  populate?: string | string[];
  pagination?: {
    page?: number;
    pageSize?: number;
  };
}
```

### GraphQL API

```typescript
// services/strapi-graphql.service.ts
import { GraphQLClient } from 'graphql-request';

export class StrapiGraphQLClient {
  private client: GraphQLClient;

  constructor() {
    this.client = new GraphQLClient(
      process.env.STRAPI_GRAPHQL_URL || 'http://localhost:1337/graphql',
      {
        headers: {
          'Authorization': `Bearer ${process.env.STRAPI_API_TOKEN}`
        }
      }
    );
  }

  async getArticles(): Promise<Article[]> {
    const query = `
      query GetArticles {
        articles {
          data {
            id
            attributes {
              title
              slug
              excerpt
              publishedAt
              coverImage {
                data {
                  attributes {
                    url
                    alternativeText
                  }
                }
              }
              author {
                data {
                  attributes {
                    name
                    avatar {
                      data {
                        attributes {
                          url
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    `;

    const data = await this.client.request(query);
    return data.articles.data;
  }
}
```

## Custom Controllers

```javascript
// src/api/article/controllers/article.js
'use strict';

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::article.article', ({ strapi }) => ({
  // Custom action
  async findBySlug(ctx) {
    const { slug } = ctx.params;

    const entity = await strapi.db.query('api::article.article').findOne({
      where: { slug },
      populate: ['author', 'categories', 'coverImage']
    });

    if (!entity) {
      return ctx.notFound();
    }

    const sanitizedEntity = await this.sanitizeOutput(entity, ctx);
    return this.transformResponse(sanitizedEntity);
  },

  // Override default find
  async find(ctx) {
    // Custom logic before
    const { data, meta } = await super.find(ctx);
    
    // Custom logic after
    return { data, meta };
  },

  // Custom endpoint
  async incrementViews(ctx) {
    const { id } = ctx.params;

    const article = await strapi.entityService.update('api::article.article', id, {
      data: {
        views: { $inc: 1 }
      }
    });

    return { views: article.views };
  }
}));
```

## Custom Routes

```javascript
// src/api/article/routes/custom-article.js
module.exports = {
  routes: [
    {
      method: 'GET',
      path: '/articles/slug/:slug',
      handler: 'article.findBySlug',
      config: {
        auth: false
      }
    },
    {
      method: 'POST',
      path: '/articles/:id/increment-views',
      handler: 'article.incrementViews',
      config: {
        auth: false
      }
    }
  ]
};
```

## Plugins Development

```javascript
// src/plugins/my-plugin/admin/src/index.js
export default {
  register(app) {
    // Register plugin
  },
  bootstrap(app) {
    // Bootstrap plugin
  }
};

// src/plugins/my-plugin/server/register.js
module.exports = ({ strapi }) => {
  // Register custom fields, services, etc.
};

// src/plugins/my-plugin/server/services/my-service.js
module.exports = ({ strapi }) => ({
  async doSomething() {
    // Service logic
  }
});
```

## Webhooks

```javascript
// config/plugins.js
module.exports = {
  webhooks: {
    enabled: true,
    config: {
      populateRelations: true
    }
  }
};

// Webhook handler (external service)
app.post('/webhooks/strapi', async (req, res) => {
  const event = req.body;

  switch (event.event) {
    case 'entry.create':
      await handleEntryCreated(event);
      break;

    case 'entry.update':
      await handleEntryUpdated(event);
      break;

    case 'entry.delete':
      await handleEntryDeleted(event);
      break;

    case 'entry.publish':
      await handleEntryPublished(event);
      break;
  }

  res.json({ received: true });
});

async function handleEntryPublished(event) {
  const { model, entry } = event;

  if (model === 'article') {
    // Revalidate Next.js page
    await fetch(`${process.env.NEXT_URL}/api/revalidate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slug: entry.slug })
    });
  }
}
```

## Authentication Integration

```typescript
// services/strapi-auth.service.ts
export class StrapiAuthService {
  async register(data: RegisterDto): Promise<AuthResponse> {
    const response = await fetch(`${process.env.STRAPI_API_URL}/auth/local/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    return response.json();
  }

  async login(identifier: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${process.env.STRAPI_API_URL}/auth/local`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password })
    });

    return response.json();
  }

  async getMe(jwt: string): Promise<User> {
    const response = await fetch(`${process.env.STRAPI_API_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${jwt}`
      }
    });

    return response.json();
  }
}

interface RegisterDto {
  username: string;
  email: string;
  password: string;
}

interface AuthResponse {
  jwt: string;
  user: User;
}

interface User {
  id: number;
  username: string;
  email: string;
}
```

## Deployment

```yaml
# docker-compose.yml
version: '3'
services:
  strapi:
    image: strapi/strapi
    environment:
      DATABASE_CLIENT: postgres
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_NAME: strapi
      DATABASE_USERNAME: strapi
      DATABASE_PASSWORD: strapi
      JWT_SECRET: your-secret-key
    volumes:
      - ./app:/srv/app
    ports:
      - '1337:1337'
    depends_on:
      - postgres

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: strapi
      POSTGRES_USER: strapi
      POSTGRES_PASSWORD: strapi
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

```javascript
// config/env/production/database.js
module.exports = ({ env }) => ({
  connection: {
    client: 'postgres',
    connection: {
      host: env('DATABASE_HOST'),
      port: env.int('DATABASE_PORT'),
      database: env('DATABASE_NAME'),
      user: env('DATABASE_USERNAME'),
      password: env('DATABASE_PASSWORD'),
      ssl: env.bool('DATABASE_SSL', false) && {
        rejectUnauthorized: env.bool('DATABASE_SSL_SELF', false)
      }
    },
    debug: false
  }
});
```

## Best Practices

1. **Content Types** - Design reusable content types
2. **Components** - Use components for reusable content
3. **Relations** - Properly define relationships
4. **Permissions** - Configure role-based permissions
5. **API Tokens** - Use API tokens for authentication
6. **Webhooks** - Use webhooks for real-time updates
7. **Custom Controllers** - Extend default controllers
8. **Plugins** - Develop custom plugins for specific needs
9. **Performance** - Optimize queries with populate
10. **Deployment** - Use Docker for consistent deployments

---

## Quick Start

### Strapi API Client

```javascript
const Strapi = require('strapi-sdk-javascript').default

const strapi = new Strapi('http://localhost:1337')

// Fetch entries
const articles = await strapi.getEntries('articles', {
  _sort: 'created_at:desc',
  _limit: 10
})

// Create entry
const article = await strapi.createEntry('articles', {
  title: 'My Article',
  content: 'Article content',
  published: true
})
```

---

## Production Checklist

- [ ] **Strapi Setup**: Strapi instance configured
- [ ] **Content Types**: Content types defined
- [ ] **API Access**: API access configured
- [ ] **Authentication**: API authentication set up
- [ ] **Permissions**: Content permissions configured
- [ ] **Media Library**: Media library configured
- [ ] **Custom Fields**: Custom fields added if needed
- [ ] **Webhooks**: Webhooks for content updates
- [ ] **Caching**: Cache API responses
- [ ] **Performance**: Optimize API performance
- [ ] **Documentation**: Document content structure
- [ ] **Backup**: Backup Strapi data

---

## Anti-patterns

### ❌ Don't: Expose Admin API

```javascript
// ❌ Bad - Expose admin API
const strapi = new Strapi('http://localhost:1337/admin')
// Admin API exposed!
```

```javascript
// ✅ Good - Use public API
const strapi = new Strapi('http://localhost:1337')
// Public API with proper permissions
```

### ❌ Don't: No Caching

```javascript
// ❌ Bad - No caching
const articles = await strapi.getEntries('articles')
// Every request hits Strapi!
```

```javascript
// ✅ Good - Cache responses
const cacheKey = 'articles'
let articles = await cache.get(cacheKey)
if (!articles) {
  articles = await strapi.getEntries('articles')
  await cache.set(cacheKey, articles, 3600)  // 1 hour
}
```

---

## Integration Points

- **Headless CMS** (`33-content-management/headless-cms/`) - CMS patterns
- **Contentful Integration** (`33-content-management/contentful-integration/`) - Alternative CMS
- **Next.js Patterns** (`02-frontend/nextjs-patterns/`) - SSG/ISR

---

## Further Reading

- [Strapi Documentation](https://docs.strapi.io/)
- [Strapi SDK](https://github.com/strapi/strapi-sdk-javascript)
- [Strapi Deployment](https://docs.strapi.io/developer-docs/latest/setup-deployment-guides/deployment.html)

## Resources

- [Strapi Documentation](https://docs.strapi.io/)
- [Strapi API Reference](https://docs.strapi.io/developer-docs/latest/developer-resources/database-apis-reference/rest-api.html)
- [Strapi Plugins](https://market.strapi.io/)
- [Strapi Community](https://strapi.io/community)
