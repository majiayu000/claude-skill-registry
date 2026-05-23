---
name: graphql-resolvers
description: Use when implementing GraphQL resolvers with resolver functions, context management, DataLoader batching, error handling, authentication, and testing strategies.
allowed-tools: []
---

# GraphQL Resolvers

Apply resolver implementation patterns to create efficient, maintainable
GraphQL servers. This skill covers resolver function signatures,
execution chains, context management, DataLoader patterns, async
handling, authentication, and testing strategies.

## Resolver Function Signature

Every resolver function receives four arguments: parent, args, context,
and info. Understanding these arguments is fundamental to writing
effective resolvers.

```typescript
type ResolverFn = (
  parent: any,
  args: any,
  context: any,
  info: GraphQLResolveInfo
) => any;

const resolvers = {
  Query: {
    // parent: root value (usually undefined for Query)
    // args: arguments passed to the query
    // context: shared context object
    // info: execution information
    user: async (parent, args, context, info) => {
      const { id } = args;
      const { dataSources, user } = context;

      // Use context to access data sources and auth info
      return dataSources.userAPI.getUserById(id);
    },

    posts: async (parent, args, context, info) => {
      const { limit, offset } = args;

      // Access requested fields from info
      const fields = info.fieldNodes[0].selectionSet.selections
        .map(s => s.name.value);

      return context.dataSources.postAPI.getPosts({
        limit,
        offset,
        fields
      });
    }
  }
};
```

## Field Resolvers

Field resolvers define how to resolve individual fields on a type. The
parent argument contains the resolved parent object.

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUserById(id);
    }
  },

  User: {
    // Field resolver for computed field
    fullName: (parent) => {
      return `${parent.firstName} ${parent.lastName}`;
    },

    // Field resolver for related data
    posts: async (parent, args, { dataSources }) => {
      // parent.id available from parent User object
      return dataSources.postAPI.getPostsByAuthor(parent.id);
    },

    // Field resolver with arguments
    friends: async (parent, { limit }, { dataSources }) => {
      return dataSources.userAPI.getFriends(parent.id, limit);
    },

    // Async computed field
    postCount: async (parent, _, { dataSources }) => {
      return dataSources.postAPI.countByAuthor(parent.id);
    }
  },

  Post: {
    author: async (parent, _, { dataSources }) => {
      // parent.authorId from parent Post object
      return dataSources.userAPI.getUserById(parent.authorId);
    },

    comments: async (parent, _, { dataSources }) => {
      return dataSources.commentAPI.getByPostId(parent.id);
    }
  }
};
```

## Context Object Patterns

The context object is shared across all resolvers in a single request.
Use it for authentication, data sources, and request-scoped data.

```typescript
interface Context {
  user: User | null;
  dataSources: DataSources;
  db: Database;
  req: Request;
  loaders: Loaders;
}

// Context creation function
const createContext = async ({ req }): Promise<Context> => {
  // Extract and verify authentication token
  const token = req.headers.authorization?.replace('Bearer ', '');
  const user = token ? await verifyToken(token) : null;

  // Initialize data sources
  const dataSources = {
    userAPI: new UserAPI(),
    postAPI: new PostAPI(),
    commentAPI: new CommentAPI()
  };

  // Initialize DataLoaders
  const loaders = {
    userLoader: new DataLoader(ids => batchGetUsers(ids)),
    postLoader: new DataLoader(ids => batchGetPosts(ids))
  };

  return {
    user,
    dataSources,
    db: database,
    req,
    loaders
  };
};

// Using context in resolvers
const resolvers = {
  Query: {
    me: (_, __, { user }) => {
      if (!user) {
        throw new Error('Not authenticated');
      }
      return user;
    },

    post: async (_, { id }, { loaders }) => {
      return loaders.postLoader.load(id);
    }
  }
};
```

## Resolver Chains and Execution

Resolvers execute in a chain where parent resolvers complete before
child resolvers begin. Understanding execution order is crucial for
optimization.

```typescript
const resolvers = {
  Query: {
    // Step 1: Root resolver executes
    user: async (_, { id }, { db }) => {
      console.log('1. Fetching user');
      return db.users.findById(id);
    }
  },

  User: {
    // Step 2: Field resolvers execute with parent data
    posts: async (parent, _, { db }) => {
      console.log('2. Fetching posts for user', parent.id);
      return db.posts.findByAuthor(parent.id);
    },

    profile: async (parent, _, { db }) => {
      console.log('2. Fetching profile for user', parent.id);
      return db.profiles.findByUserId(parent.id);
    }
  },

  Post: {
    // Step 3: Nested field resolvers execute
    comments: async (parent, _, { db }) => {
      console.log('3. Fetching comments for post', parent.id);
      return db.comments.findByPostId(parent.id);
    }
  }
};

// Query execution order:
// query {
//   user(id: "1") {        # 1. User resolver
//     posts {              # 2. Posts resolver
//       comments {         # 3. Comments resolver
//         text
//       }
//     }
//     profile {            # 2. Profile resolver (parallel)
//       bio
//     }
//   }
// }
```

## DataLoader Pattern for Batching

DataLoader solves the N+1 problem by batching multiple individual
loads into a single batch request and caching results.

```typescript
import DataLoader from 'dataloader';

// Batch function receives array of keys
// Must return array of results in same order
const batchGetUsers = async (userIds: string[]) => {
  console.log('Batch loading users:', userIds);

  // Single database query for all IDs
  const users = await db.users.findByIds(userIds);

  // Create map for O(1) lookup
  const userMap = new Map(users.map(u => [u.id, u]));

  // Return users in same order as input IDs
  return userIds.map(id => userMap.get(id) || null);
};

// Create loader in context
const userLoader = new DataLoader(batchGetUsers, {
  // Optional configuration
  cache: true,            // Cache results (default: true)
  maxBatchSize: 100,      // Maximum batch size
  batchScheduleFn: cb => setTimeout(cb, 10) // Custom scheduling
});

const resolvers = {
  Post: {
    author: async (parent, _, { loaders }) => {
      // These calls are automatically batched
      return loaders.userLoader.load(parent.authorId);
    }
  },

  Comment: {
    author: async (parent, _, { loaders }) => {
      // Added to same batch as Post.author
      return loaders.userLoader.load(parent.authorId);
    }
  }
};

// Example: Without DataLoader (N+1 problem)
// Query for 10 posts = 1 query for posts + 10 queries for authors
//
// With DataLoader:
// Query for 10 posts = 1 query for posts + 1 batched query for all
// authors
```

## Advanced DataLoader Patterns

```typescript
// Composite key loader
interface CompositeKey {
  userId: string;
  type: string;
}

const batchGetUserData = async (keys: CompositeKey[]) => {
  // Group by type for efficient querying
  const byType = keys.reduce((acc, key) => {
    acc[key.type] = acc[key.type] || [];
    acc[key.type].push(key.userId);
    return acc;
  }, {});

  // Fetch data by type
  const results = await Promise.all(
    Object.entries(byType).map(([type, userIds]) =>
      fetchDataByType(type, userIds)
    )
  );

  // Map back to original key order
  return keys.map(key =>
    results.find(r => r.userId === key.userId && r.type === key.type)
  );
};

const dataLoader = new DataLoader(
  batchGetUserData,
  {
    cacheKeyFn: (key: CompositeKey) => `${key.userId}:${key.type}`
  }
);

// Prime the cache
await dataLoader.prime({ userId: '1', type: 'profile' }, userData);

// Clear specific key
dataLoader.clear({ userId: '1', type: 'profile' });

// Clear all cache
dataLoader.clearAll();
```

## Async Error Handling

Proper error handling in resolvers ensures meaningful errors reach the
client while protecting sensitive information.

```typescript
import { GraphQLError } from 'graphql';
import { ApolloServerErrorCode } from '@apollo/server/errors';

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      try {
        const user = await dataSources.userAPI.getUserById(id);

        if (!user) {
          throw new GraphQLError('User not found', {
            extensions: {
              code: 'USER_NOT_FOUND',
              http: { status: 404 }
            }
          });
        }

        return user;
      } catch (error) {
        // Log full error for debugging
        console.error('Error fetching user:', error);

        // Throw safe error to client
        if (error instanceof GraphQLError) {
          throw error;
        }

        throw new GraphQLError('Failed to fetch user', {
          extensions: {
            code: 'INTERNAL_SERVER_ERROR'
          }
        });
      }
    }
  },

  Mutation: {
    createPost: async (_, { input }, { user, dataSources }) => {
      // Validation errors
      if (!input.title || input.title.length < 3) {
        throw new GraphQLError('Title must be at least 3 characters', {
          extensions: {
            code: 'BAD_USER_INPUT',
            argumentName: 'title'
          }
        });
      }

      // Authentication errors
      if (!user) {
        throw new GraphQLError('Must be authenticated', {
          extensions: {
            code: ApolloServerErrorCode.UNAUTHENTICATED
          }
        });
      }

      try {
        return await dataSources.postAPI.create(input);
      } catch (error) {
        throw new GraphQLError('Failed to create post', {
          extensions: {
            code: 'INTERNAL_SERVER_ERROR'
          },
          originalError: error
        });
      }
    }
  }
};
```

## Authentication and Authorization

Implement authentication and authorization patterns in resolvers and
context.

```typescript
// Authentication middleware
const requireAuth = (resolver) => {
  return (parent, args, context, info) => {
    if (!context.user) {
      throw new GraphQLError('Not authenticated', {
        extensions: { code: 'UNAUTHENTICATED' }
      });
    }
    return resolver(parent, args, context, info);
  };
};

// Authorization middleware
const requireRole = (role: string) => (resolver) => {
  return (parent, args, context, info) => {
    if (!context.user) {
      throw new GraphQLError('Not authenticated', {
        extensions: { code: 'UNAUTHENTICATED' }
      });
    }

    if (!context.user.roles.includes(role)) {
      throw new GraphQLError('Insufficient permissions', {
        extensions: { code: 'FORBIDDEN' }
      });
    }

    return resolver(parent, args, context, info);
  };
};

const resolvers = {
  Query: {
    me: requireAuth((_, __, { user }) => user),

    adminPanel: requireRole('ADMIN')(
      async (_, __, { dataSources }) => {
        return dataSources.adminAPI.getDashboard();
      }
    ),

    // Resource-based authorization
    post: async (_, { id }, { user, dataSources }) => {
      const post = await dataSources.postAPI.getById(id);

      if (!post) {
        throw new GraphQLError('Post not found');
      }

      // Check if user can view this post
      if (post.status === 'DRAFT' && post.authorId !== user?.id) {
        throw new GraphQLError('Cannot view draft posts', {
          extensions: { code: 'FORBIDDEN' }
        });
      }

      return post;
    }
  },

  Mutation: {
    updatePost: requireAuth(
      async (_, { id, input }, { user, dataSources }) => {
        const post = await dataSources.postAPI.getById(id);

        // Check ownership
        if (post.authorId !== user.id && !user.roles.includes('ADMIN')) {
          throw new GraphQLError('Not authorized to update this post', {
            extensions: { code: 'FORBIDDEN' }
          });
        }

        return dataSources.postAPI.update(id, input);
      }
    )
  }
};
```

## Caching Strategies

Implement caching at the resolver level for improved performance.

```typescript
import { createHash } from 'crypto';

// In-memory cache
const cache = new Map<string, { data: any; expiry: number }>();

const getCacheKey = (prefix: string, args: any): string => {
  const hash = createHash('md5')
    .update(JSON.stringify(args))
    .digest('hex');
  return `${prefix}:${hash}`;
};

const cacheResolver = (
  resolver,
  { ttl = 300, prefix = 'cache' } = {}
) => {
  return async (parent, args, context, info) => {
    const key = getCacheKey(prefix, args);
    const cached = cache.get(key);

    if (cached && cached.expiry > Date.now()) {
      console.log('Cache hit:', key);
      return cached.data;
    }

    const result = await resolver(parent, args, context, info);

    cache.set(key, {
      data: result,
      expiry: Date.now() + (ttl * 1000)
    });

    return result;
  };
};

const resolvers = {
  Query: {
    // Cache for 5 minutes
    popularPosts: cacheResolver(
      async (_, { limit }, { dataSources }) => {
        return dataSources.postAPI.getPopular(limit);
      },
      { ttl: 300, prefix: 'popular-posts' }
    ),

    // Redis caching
    user: async (_, { id }, { redis, dataSources }) => {
      const cacheKey = `user:${id}`;

      // Try cache first
      const cached = await redis.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }

      // Fetch and cache
      const user = await dataSources.userAPI.getUserById(id);
      await redis.setex(cacheKey, 3600, JSON.stringify(user));

      return user;
    }
  }
};
```

## Resolver Middleware and Plugins

Create reusable middleware patterns for cross-cutting concerns.

```typescript
// Logging middleware
const logResolver = (resolver) => {
  return async (parent, args, context, info) => {
    const start = Date.now();
    const fieldName = info.fieldName;

    try {
      const result = await resolver(parent, args, context, info);
      const duration = Date.now() - start;
      console.log(`${fieldName} resolved in ${duration}ms`);
      return result;
    } catch (error) {
      console.error(`${fieldName} failed:`, error);
      throw error;
    }
  };
};

// Timing middleware
const timeResolver = (resolver) => {
  return async (parent, args, context, info) => {
    const start = performance.now();
    const result = await resolver(parent, args, context, info);
    const duration = performance.now() - start;

    // Add timing to extensions
    info.operation.extensions = info.operation.extensions || {};
    info.operation.extensions.timing =
      info.operation.extensions.timing || {};
    info.operation.extensions.timing[info.fieldName] = duration;

    return result;
  };
};

// Compose middleware
const compose = (...middlewares) => (resolver) => {
  return middlewares.reduceRight(
    (acc, middleware) => middleware(acc),
    resolver
  );
};

const resolvers = {
  Query: {
    user: compose(
      logResolver,
      timeResolver,
      requireAuth
    )(async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUserById(id);
    })
  }
};
```

## Testing Resolvers

Write comprehensive tests for resolvers using mocked context and data
sources.

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('User Resolvers', () => {
  it('should fetch user by id', async () => {
    const mockUser = { id: '1', username: 'test' };

    const mockContext = {
      dataSources: {
        userAPI: {
          getUserById: vi.fn().mockResolvedValue(mockUser)
        }
      }
    };

    const result = await resolvers.Query.user(
      null,
      { id: '1' },
      mockContext,
      {} as any
    );

    expect(result).toEqual(mockUser);
    expect(mockContext.dataSources.userAPI.getUserById)
      .toHaveBeenCalledWith('1');
  });

  it('should throw error when user not found', async () => {
    const mockContext = {
      dataSources: {
        userAPI: {
          getUserById: vi.fn().mockResolvedValue(null)
        }
      }
    };

    await expect(
      resolvers.Query.user(null, { id: '999' }, mockContext, {} as any)
    ).rejects.toThrow('User not found');
  });

  it('should require authentication', async () => {
    const mockContext = {
      user: null,
      dataSources: {}
    };

    await expect(
      resolvers.Query.me(null, {}, mockContext, {} as any)
    ).rejects.toThrow('Not authenticated');
  });

  it('should use DataLoader for batching', async () => {
    const mockUsers = [
      { id: '1', username: 'user1' },
      { id: '2', username: 'user2' }
    ];

    const batchFn = vi.fn().mockResolvedValue(mockUsers);
    const loader = new DataLoader(batchFn);

    const mockContext = {
      loaders: { userLoader: loader }
    };

    // Make multiple calls
    const [user1, user2] = await Promise.all([
      resolvers.Post.author(
        { authorId: '1' },
        {},
        mockContext,
        {} as any
      ),
      resolvers.Post.author(
        { authorId: '2' },
        {},
        mockContext,
        {} as any
      )
    ]);

    expect(user1).toEqual(mockUsers[0]);
    expect(user2).toEqual(mockUsers[1]);
    expect(batchFn).toHaveBeenCalledTimes(1);
    expect(batchFn).toHaveBeenCalledWith(['1', '2']);
  });
});
```

## Best Practices

1. **Keep resolvers thin**: Delegate business logic to service layer,
   use resolvers only for data fetching and transformation
2. **Use DataLoader**: Implement DataLoader for any resolver that
   fetches related data to avoid N+1 queries
3. **Leverage context**: Store shared resources (database, auth, data
   sources) in context for all resolvers
4. **Handle errors gracefully**: Catch errors and throw meaningful
   GraphQLError instances with appropriate codes
5. **Implement proper auth**: Check authentication and authorization in
   resolvers or middleware consistently
6. **Cache strategically**: Cache expensive operations at resolver
   level using in-memory or distributed cache
7. **Use typed resolvers**: Define TypeScript types for resolver
   functions to catch errors at compile time
8. **Test thoroughly**: Write unit tests for resolvers with mocked
   dependencies and edge cases
9. **Avoid blocking operations**: Use async/await and parallel
   execution where possible to prevent blocking
10. **Monitor performance**: Log resolver execution time and identify
    slow resolvers for optimization

## Common Pitfalls

1. **N+1 queries**: Fetching related data in loops without batching,
   causing excessive database queries
2. **Blocking operations**: Using synchronous operations in resolvers
   that block the event loop
3. **Memory leaks**: Storing data in closures or module scope that
   grows unbounded
4. **Inconsistent error handling**: Throwing raw errors without proper
   GraphQLError wrapping and codes
5. **Over-fetching in resolvers**: Fetching entire objects when only
   specific fields are needed
6. **Context mutation**: Modifying context object during resolver
   execution, causing side effects
7. **Missing authentication checks**: Forgetting to verify auth in
   sensitive resolvers
8. **Improper DataLoader usage**: Creating new DataLoader instances per
   resolver instead of per request
9. **Circular resolver chains**: Creating resolver dependencies that
   cause infinite loops
10. **Not using info parameter**: Ignoring the info parameter that
    contains requested fields for optimization

## When to Use This Skill

Use GraphQL resolver skills when:

- Implementing a new GraphQL server
- Optimizing existing resolver performance
- Debugging N+1 query problems
- Adding authentication and authorization
- Implementing data batching and caching
- Writing resolver unit tests
- Refactoring resolvers for better maintainability
- Adding logging and monitoring to resolvers
- Implementing custom middleware or plugins
- Migrating from REST API to GraphQL

## Resources

- [GraphQL Resolvers Documentation](https://graphql.org/learn/execution/) -
  Official execution and resolver guide
- [DataLoader GitHub](https://github.com/graphql/dataloader) - Official
  DataLoader library and documentation
- [Apollo Server Resolvers](https://www.apollographql.com/docs/apollo-server/data/resolvers/)
  Resolver patterns and examples
- [GraphQL Error Handling](https://www.apollographql.com/docs/apollo-server/data/errors/)
  Error handling best practices
- [Testing GraphQL Resolvers](https://www.apollographql.com/docs/apollo-server/testing/testing/)
  Testing strategies
