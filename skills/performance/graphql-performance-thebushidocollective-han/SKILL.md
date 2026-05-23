---
name: graphql-performance
description: Use when optimizing GraphQL API performance with query complexity analysis, batching, caching strategies, depth limiting, monitoring, and database optimization.
allowed-tools: []
---

# GraphQL Performance

Apply GraphQL performance optimization techniques to create efficient,
scalable APIs. This skill covers query complexity analysis, depth
limiting, batching and caching strategies, DataLoader optimization,
monitoring, tracing, and database query optimization.

## Query Complexity Analysis

Query complexity analysis prevents expensive queries from overwhelming
your server by calculating and limiting the computational cost.

```typescript
import { GraphQLError } from 'graphql';
import { ApolloServer } from '@apollo/server';

// Complexity calculator
const getComplexity = (field, childComplexity, args) => {
  // Base complexity for field
  let complexity = 1;

  // List multiplier based on limit argument
  if (args.limit) {
    complexity = args.limit;
  } else if (args.first) {
    complexity = args.first;
  }

  // Add child complexity
  return complexity + childComplexity;
};

// Directive-based complexity
const schema = `
  directive @complexity(
    value: Int!
    multipliers: [String!]
  ) on FIELD_DEFINITION

  type Query {
    user(id: ID!): User @complexity(value: 1)
    users(limit: Int): [User!]! @complexity(
      value: 1,
      multipliers: ["limit"]
    )
    posts(first: Int): [Post!]! @complexity(
      value: 5,
      multipliers: ["first"]
    )
  }

  type User {
    id: ID!
    posts: [Post!]! @complexity(value: 10)
  }
`;

// Complexity validation plugin
const complexityPlugin = {
  requestDidStart: () => ({
    async didResolveOperation({ request, document, operationName }) {
      const complexity = calculateComplexity({
        document,
        operationName,
        variables: request.variables
      });

      const maxComplexity = 1000;

      if (complexity > maxComplexity) {
        throw new GraphQLError(
          `Query is too complex: ${complexity}. ` +
          `Maximum allowed: ${maxComplexity}`,
          {
            extensions: {
              code: 'QUERY_TOO_COMPLEX',
              complexity,
              maxComplexity
            }
          }
        );
      }
    }
  })
};

// Manual complexity calculation
const calculateComplexity = ({ document, operationName, variables }) => {
  let totalComplexity = 0;

  const visit = (node, multiplier = 1) => {
    if (node.kind === 'Field') {
      // Get field complexity from directive or default
      const complexity = getFieldComplexity(node);

      // Handle multipliers from arguments
      const args = getArguments(node, variables);
      const fieldMultiplier = getMultiplier(args);

      totalComplexity += complexity * multiplier * fieldMultiplier;

      // Visit child fields
      if (node.selectionSet) {
        node.selectionSet.selections.forEach(child =>
          visit(child, multiplier * fieldMultiplier)
        );
      }
    }
  };

  visit(document);
  return totalComplexity;
};
```

## Depth Limiting

Prevent deeply nested queries that can cause performance issues and
potential denial of service attacks.

```typescript
import { ValidationContext, GraphQLError } from 'graphql';

const depthLimit = (maxDepth: number) => {
  return (validationContext: ValidationContext) => {
    return {
      Field(node, key, parent, path, ancestors) {
        const depth = ancestors.filter(
          ancestor => ancestor.kind === 'Field'
        ).length;

        if (depth > maxDepth) {
          validationContext.reportError(
            new GraphQLError(
              `Query exceeds maximum depth of ${maxDepth}. ` +
              `Found depth of ${depth}.`,
              {
                nodes: [node],
                extensions: {
                  code: 'DEPTH_LIMIT_EXCEEDED',
                  depth,
                  maxDepth
                }
              }
            )
          );
        }
      }
    };
  };
};

// Usage with Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)]
});

// Example queries
// ✅ Allowed (depth: 4)
query {
  user {
    posts {
      comments {
        author {
          username
        }
      }
    }
  }
}

// ❌ Rejected (depth: 8)
query {
  user {
    friends {
      friends {
        friends {
          friends {
            friends {
              friends {
                friends {
                  username
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Query Cost Analysis

Implement cost-based rate limiting to protect against expensive
queries.

```typescript
interface CostConfig {
  objectCost: number;
  scalarCost: number;
  defaultListSize: number;
}

const calculateQueryCost = (
  document,
  variables,
  config: CostConfig
) => {
  let totalCost = 0;

  const visit = (node, multiplier = 1) => {
    if (node.kind === 'Field') {
      const fieldType = getFieldType(node);

      // List cost
      if (isListType(fieldType)) {
        const listSize = getListSize(node, variables) ||
          config.defaultListSize;
        multiplier *= listSize;
      }

      // Field cost
      if (isObjectType(fieldType)) {
        totalCost += config.objectCost * multiplier;
      } else {
        totalCost += config.scalarCost * multiplier;
      }

      // Visit children
      if (node.selectionSet) {
        node.selectionSet.selections.forEach(child =>
          visit(child, multiplier)
        );
      }
    }
  };

  visit(document);
  return totalCost;
};

// Rate limiting based on cost
const costLimitPlugin = {
  requestDidStart: () => ({
    async didResolveOperation({ request, document, contextValue }) {
      const cost = calculateQueryCost(
        document,
        request.variables,
        { objectCost: 1, scalarCost: 0.1, defaultListSize: 10 }
      );

      // Check user's rate limit
      const limit = await getRateLimit(contextValue.user);
      const used = await getCostUsed(contextValue.user);

      if (used + cost > limit) {
        throw new GraphQLError('Rate limit exceeded', {
          extensions: {
            code: 'RATE_LIMIT_EXCEEDED',
            cost,
            used,
            limit
          }
        });
      }

      // Track cost usage
      await incrementCostUsed(contextValue.user, cost);
    }
  })
};
```

## Batching with DataLoader

Optimize data fetching by batching multiple requests into single
database queries.

```typescript
import DataLoader from 'dataloader';

// Basic DataLoader setup
const createUserLoader = (db) => {
  return new DataLoader<string, User>(
    async (userIds) => {
      // Single query for all users
      const users = await db.users.findByIds(userIds);

      // Map to maintain order
      const userMap = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => userMap.get(id) || null);
    },
    {
      // Cache for duration of request
      cache: true,
      // Batch at most 100 at a time
      maxBatchSize: 100,
      // Wait 10ms before batching
      batchScheduleFn: callback => setTimeout(callback, 10)
    }
  );
};

// Advanced batching with joins
const createPostsLoader = (db) => {
  return new DataLoader<string, Post[]>(
    async (authorIds) => {
      // Single query with all author IDs
      const posts = await db.posts.query()
        .whereIn('authorId', authorIds)
        .select();

      // Group by author ID
      const postsByAuthor = authorIds.map(authorId =>
        posts.filter(post => post.authorId === authorId)
      );

      return postsByAuthor;
    }
  );
};

// Multi-key loader
interface PostKey {
  authorId: string;
  status: string;
}

const createFilteredPostsLoader = (db) => {
  return new DataLoader<PostKey, Post[]>(
    async (keys) => {
      // Extract unique author IDs and statuses
      const authorIds = [...new Set(keys.map(k => k.authorId))];
      const statuses = [...new Set(keys.map(k => k.status))];

      // Single query for all combinations
      const posts = await db.posts.query()
        .whereIn('authorId', authorIds)
        .whereIn('status', statuses)
        .select();

      // Map back to original keys
      return keys.map(key =>
        posts.filter(post =>
          post.authorId === key.authorId &&
          post.status === key.status
        )
      );
    },
    {
      cacheKeyFn: (key) => `${key.authorId}:${key.status}`
    }
  );
};

// Loader with custom cache
import { LRUCache } from 'lru-cache';

const createCachedLoader = (db) => {
  const cache = new LRUCache<string, User>({
    max: 500,
    ttl: 1000 * 60 * 5 // 5 minutes
  });

  return new DataLoader<string, User>(
    async (userIds) => {
      const users = await db.users.findByIds(userIds);
      const userMap = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => userMap.get(id) || null);
    },
    {
      cacheMap: cache
    }
  );
};
```

## Response Caching Strategies

Implement multi-level caching for optimal performance.

```typescript
import { createHash } from 'crypto';

// Field-level caching
const cacheControl = {
  User: {
    __cacheControl: { maxAge: 3600 }, // 1 hour

    posts: {
      __cacheControl: { maxAge: 300 } // 5 minutes
    }
  },

  Post: {
    __cacheControl: { maxAge: 600, scope: 'PUBLIC' }
  }
};

// Redis caching
import Redis from 'ioredis';

const redis = new Redis();

const cacheQuery = async (key: string, ttl: number, fn: () => any) => {
  // Try cache
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }

  // Execute and cache
  const result = await fn();
  await redis.setex(key, ttl, JSON.stringify(result));

  return result;
};

const resolvers = {
  Query: {
    posts: async (_, args) => {
      const cacheKey = `posts:${JSON.stringify(args)}`;

      return cacheQuery(cacheKey, 300, async () => {
        return db.posts.find(args);
      });
    },

    // Automatic cache with hash
    user: async (_, { id }) => {
      const cacheKey = `user:${id}`;

      return cacheQuery(cacheKey, 3600, async () => {
        return db.users.findById(id);
      });
    }
  }
};

// CDN caching with APQ
// Automatic Persisted Queries reduce bandwidth and enable CDN caching
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    {
      async requestDidStart() {
        return {
          async responseForOperation({ request, operation }) {
            // Only cache if APQ hash is present
            if (!request.extensions?.persistedQuery?.sha256Hash) {
              return null;
            }

            // Cache GET requests at CDN
            return {
              http: {
                headers: new Map([
                  ['cache-control', 'public, max-age=300']
                ])
              }
            };
          }
        };
      }
    }
  ]
});
```

## Persistent Queries and APQ

Implement Automatic Persisted Queries to reduce payload size and
enable better caching.

```typescript
import { ApolloServer } from '@apollo/server';
import { KeyvAdapter } from '@apollo/utils.keyvadapter';
import Keyv from 'keyv';

// APQ with Redis backend
const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new KeyvAdapter(new Keyv('redis://localhost:6379'))
  }
});

// Client sends hash instead of full query
// First request:
// POST /graphql
// {
//   "query": "query GetUser { user(id: \"1\") { id name } }",
//   "extensions": {
//     "persistedQuery": {
//       "version": 1,
//       "sha256Hash": "abc123..."
//     }
//   }
// }

// Subsequent requests (99% smaller):
// GET /graphql?extensions={"persistedQuery":{"version":1,"sha256Hash":"abc123..."}}

// Query whitelisting
const allowedQueries = new Map([
  ['getUser', 'query GetUser($id: ID!) { user(id: $id) { id name } }'],
  ['getPosts', 'query GetPosts { posts { id title } }']
]);

const whitelistPlugin = {
  requestDidStart: () => ({
    async didResolveSource({ source }) {
      const hash = source.extensions?.persistedQuery?.sha256Hash;

      if (!hash || !allowedQueries.has(hash)) {
        throw new GraphQLError('Query not whitelisted', {
          extensions: { code: 'FORBIDDEN' }
        });
      }
    }
  })
};
```

## Database Query Optimization

Optimize database queries to support GraphQL efficiently.

```typescript
// Use info parameter for selective field loading
import { GraphQLResolveInfo } from 'graphql';
import { parseResolveInfo } from 'graphql-parse-resolve-info';

const resolvers = {
  Query: {
    users: async (_, args, { db }, info: GraphQLResolveInfo) => {
      // Parse requested fields
      const parsedInfo = parseResolveInfo(info);
      const fields = Object.keys(parsedInfo.fields);

      // Only select requested fields
      return db.users.query().select(fields);
    },

    // Conditional joins based on requested fields
    posts: async (_, args, { db }, info: GraphQLResolveInfo) => {
      const parsedInfo = parseResolveInfo(info);

      let query = db.posts.query();

      // Join author only if requested
      if (parsedInfo.fields.author) {
        query = query.withGraphFetched('author');
      }

      // Join comments only if requested
      if (parsedInfo.fields.comments) {
        query = query.withGraphFetched('comments');
      }

      return query;
    }
  }
};

// Optimized relationship loading
const optimizedResolvers = {
  Query: {
    users: async (_, { limit, offset }, { db }) => {
      // Use joins instead of N queries
      return db.users.query()
        .limit(limit)
        .offset(offset)
        .withGraphFetched('[posts, profile]');
    }
  },

  User: {
    posts: async (parent, _, { db }) => {
      // If already fetched with join, return it
      if (parent.posts) {
        return parent.posts;
      }

      // Otherwise, fetch individually
      return db.posts.query().where('authorId', parent.id);
    }
  }
};

// Database indexes for GraphQL queries
// CREATE INDEX idx_posts_author_id ON posts(author_id);
// CREATE INDEX idx_posts_status ON posts(status);
// CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
// CREATE INDEX idx_posts_author_status ON posts(author_id, status);
```

## Monitoring and Profiling

Implement comprehensive monitoring to identify performance bottlenecks.

```typescript
import { ApolloServer } from '@apollo/server';

// Timing plugin
const timingPlugin = {
  requestDidStart() {
    const start = Date.now();

    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;

        // Add timing to response
        response.extensions = {
          ...response.extensions,
          timing: { duration }
        };
      }
    };
  }
};

// Detailed resolver timing
const detailedTimingPlugin = {
  requestDidStart() {
    const resolverTimings = {};

    return {
      async executionDidStart() {
        return {
          willResolveField({ info }) {
            const start = Date.now();

            return () => {
              const duration = Date.now() - start;
              const path = info.path.key;

              resolverTimings[path] = duration;
            };
          }
        };
      },

      async willSendResponse({ response }) {
        response.extensions = {
          ...response.extensions,
          resolverTimings
        };
      }
    };
  }
};

// Performance tracking
const performancePlugin = {
  requestDidStart() {
    return {
      async didResolveOperation({ request, operation }) {
        // Track operation metrics
        trackMetric('graphql.operation', 1, {
          operation: operation.operation,
          name: operation.name?.value || 'anonymous'
        });
      },

      async didEncounterErrors({ errors }) {
        errors.forEach(error => {
          trackMetric('graphql.error', 1, {
            code: error.extensions?.code || 'UNKNOWN'
          });
        });
      },

      async willSendResponse({ response }) {
        const responseSize = JSON.stringify(response).length;

        trackMetric('graphql.response_size', responseSize);
      }
    };
  }
};
```

## Tracing and Observability

Implement distributed tracing for GraphQL operations.

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

// OpenTelemetry tracing plugin
const tracingPlugin = {
  requestDidStart() {
    const tracer = trace.getTracer('graphql-server');

    return {
      async didResolveOperation({ request, operation }) {
        const span = tracer.startSpan('graphql.operation', {
          attributes: {
            'graphql.operation.type': operation.operation,
            'graphql.operation.name': operation.name?.value
          }
        });

        return {
          async executionDidStart() {
            return {
              willResolveField({ info }) {
                const fieldSpan = tracer.startSpan(
                  `graphql.resolve.${info.fieldName}`,
                  { attributes: { 'graphql.field': info.fieldName } }
                );

                return () => {
                  fieldSpan.end();
                };
              }
            };
          },

          async willSendResponse({ errors }) {
            if (errors) {
              span.setStatus({
                code: SpanStatusCode.ERROR,
                message: errors[0].message
              });
            }

            span.end();
          }
        };
      }
    };
  }
};

// Apollo Studio tracing
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    require('apollo-server-plugin-response-cache')(),
    {
      requestDidStart() {
        return {
          async willSendResponse({ response, metrics }) {
            // Send to Apollo Studio
            if (process.env.APOLLO_KEY) {
              sendToApolloStudio({
                operation: metrics.operationName,
                duration: metrics.duration,
                errors: response.errors
              });
            }
          }
        };
      }
    }
  ]
});
```

## Pagination Optimization

Implement efficient pagination strategies for large datasets.

```typescript
// Cursor-based pagination with database optimization
const resolvers = {
  Query: {
    posts: async (_, { first, after }, { db }) => {
      const limit = first || 10;

      let query = db.posts.query()
        .orderBy('createdAt', 'desc')
        .limit(limit + 1); // Fetch one extra to determine hasNextPage

      if (after) {
        const cursor = decodeCursor(after);
        query = query.where('createdAt', '<', cursor.createdAt);
      }

      const posts = await query;
      const hasNextPage = posts.length > limit;

      const edges = posts.slice(0, limit).map(post => ({
        cursor: encodeCursor({ createdAt: post.createdAt }),
        node: post
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          endCursor: edges[edges.length - 1]?.cursor
        }
      };
    }
  }
};

// Keyset pagination for better performance
const keysetPagination = async (table, { after, limit }) => {
  let query = db(table)
    .orderBy([
      { column: 'createdAt', order: 'desc' },
      { column: 'id', order: 'desc' }
    ])
    .limit(limit + 1);

  if (after) {
    const cursor = JSON.parse(Buffer.from(after, 'base64').toString());
    query = query.where(function() {
      this.where('createdAt', '<', cursor.createdAt)
        .orWhere(function() {
          this.where('createdAt', '=', cursor.createdAt)
            .andWhere('id', '<', cursor.id);
        });
    });
  }

  return query;
};
```

## Best Practices

1. **Implement query complexity limits**: Prevent expensive queries
   from overwhelming your server with complexity analysis
2. **Use depth limiting**: Set maximum query depth to prevent deeply
   nested queries that cause performance issues
3. **Batch with DataLoader**: Always use DataLoader for related data to
   avoid N+1 query problems
4. **Cache strategically**: Implement multi-level caching (DataLoader,
   Redis, CDN) based on data volatility
5. **Monitor performance**: Track resolver timing, query complexity,
   and error rates to identify bottlenecks
6. **Optimize database queries**: Use selective field loading and
   conditional joins based on requested fields
7. **Implement APQ**: Use Automatic Persisted Queries to reduce payload
   size and enable CDN caching
8. **Use cursor pagination**: Prefer cursor-based pagination over
   offset for large datasets
9. **Add proper indexes**: Create database indexes for common query
   patterns and filter fields
10. **Enable tracing**: Use OpenTelemetry or Apollo Studio for
    distributed tracing and debugging

## Common Pitfalls

1. **No query limits**: Allowing unbounded queries that can cause
   denial of service
2. **Inefficient resolvers**: Writing resolvers that don't use batching
   or caching, causing N+1 problems
3. **Missing indexes**: Not creating database indexes for GraphQL query
   patterns
4. **Over-caching**: Caching data too aggressively, leading to stale
   data being served
5. **Ignoring info parameter**: Not using GraphQLResolveInfo to
   optimize field selection
6. **No monitoring**: Deploying without performance monitoring and
   unable to identify issues
7. **Blocking operations**: Using synchronous operations in resolvers
   that block the event loop
8. **Inefficient pagination**: Using offset-based pagination for large
   datasets
9. **No rate limiting**: Allowing unlimited queries per user without
   cost-based limits
10. **Cache stampede**: Not handling cache expiration properly, causing
    all requests to hit the database simultaneously

## When to Use This Skill

Use GraphQL performance optimization skills when:

- Building a new GraphQL API that needs to scale
- Experiencing slow query response times
- Debugging N+1 query problems in production
- Implementing rate limiting and query cost analysis
- Adding caching layers to improve performance
- Optimizing database queries for GraphQL patterns
- Setting up monitoring and observability
- Protecting against malicious or expensive queries
- Migrating to production and need performance tuning
- Identifying and fixing performance bottlenecks

## Resources

- [GraphQL Best Practices](https://graphql.org/learn/best-practices/) -
  Official performance guidance
- [DataLoader Documentation](https://github.com/graphql/dataloader) -
  Batching and caching patterns
- [Apollo Performance Guide](https://www.apollographql.com/docs/apollo-server/performance/caching/)
  Performance optimization guide
- [GraphQL Query Complexity](https://github.com/slicknode/graphql-query-complexity)
  Query complexity analysis
- [OpenTelemetry for GraphQL](https://opentelemetry.io/docs/) -
  Distributed tracing implementation
