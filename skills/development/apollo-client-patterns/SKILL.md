---
name: apollo-client-patterns
description: Use when implementing Apollo Client patterns for queries, mutations, cache management, and local state in React applications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Apollo Client Patterns

Master Apollo Client for building efficient GraphQL applications with proper
query management, caching strategies, and state handling.

## Overview

Apollo Client is a comprehensive state management library for JavaScript that
enables you to manage both local and remote data with GraphQL. It integrates
seamlessly with React and provides powerful caching mechanisms.

## Installation and Setup

### Installing Apollo Client

```bash
# Install Apollo Client and dependencies
npm install @apollo/client graphql

# For React applications
npm install @apollo/client graphql react

# Additional packages
npm install graphql-tag @apollo/client/link/error
```

### Basic Configuration

```javascript
// src/apollo/client.js
import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  from
} from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

const httpLink = createHttpLink({
  uri: process.env.REACT_APP_GRAPHQL_URI || 'http://localhost:4000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('authToken');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    }
  };
});

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      )
    );
  }
  if (networkError) {
    console.error(`[Network error]: ${networkError}`);
  }
});

const client = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          posts: {
            merge(existing, incoming) {
              return incoming;
            }
          }
        }
      }
    }
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
      errorPolicy: 'all',
    },
    query: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all',
    },
  },
});

export default client;
```

### Provider Setup

```javascript
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from '@apollo/client';
import client from './apollo/client';
import App from './App';

ReactDOM.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
);
```

## Core Patterns

### 1. Basic Queries

```javascript
// src/graphql/queries.js
import { gql } from '@apollo/client';

export const GET_POSTS = gql`
  query GetPosts($limit: Int, $offset: Int) {
    posts(limit: $limit, offset: $offset) {
      id
      title
      body
      author {
        id
        name
        avatar
      }
      createdAt
    }
  }
`;

export const GET_POST = gql`
  query GetPost($id: ID!) {
    post(id: $id) {
      id
      title
      body
      author {
        id
        name
      }
      comments {
        id
        body
        author {
          id
          name
        }
      }
    }
  }
`;

// src/components/PostsList.js
import React from 'react';
import { useQuery } from '@apollo/client';
import { GET_POSTS } from '../graphql/queries';

function PostsList() {
  const { loading, error, data, refetch, fetchMore } = useQuery(GET_POSTS, {
    variables: { limit: 10, offset: 0 },
    notifyOnNetworkStatusChange: true,
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <button onClick={() => refetch()}>Refresh</button>

      {data.posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.body}</p>
          <span>By {post.author.name}</span>
        </article>
      ))}

      <button
        onClick={() =>
          fetchMore({
            variables: { offset: data.posts.length },
            updateQuery: (prev, { fetchMoreResult }) => {
              if (!fetchMoreResult) return prev;
              return {
                posts: [...prev.posts, ...fetchMoreResult.posts]
              };
            }
          })
        }
      >
        Load More
      </button>
    </div>
  );
}

export default PostsList;
```

### 2. Mutations

```javascript
// src/graphql/mutations.js
import { gql } from '@apollo/client';

export const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      body
      author {
        id
        name
      }
      createdAt
    }
  }
`;

export const UPDATE_POST = gql`
  mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
    updatePost(id: $id, input: $input) {
      id
      title
      body
    }
  }
`;

export const DELETE_POST = gql`
  mutation DeletePost($id: ID!) {
    deletePost(id: $id) {
      id
    }
  }
`;

// src/components/CreatePost.js
import React, { useState } from 'react';
import { useMutation } from '@apollo/client';
import { CREATE_POST } from '../graphql/mutations';
import { GET_POSTS } from '../graphql/queries';

function CreatePost() {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const [createPost, { loading, error }] = useMutation(CREATE_POST, {
    update(cache, { data: { createPost } }) {
      const { posts } = cache.readQuery({ query: GET_POSTS });
      cache.writeQuery({
        query: GET_POSTS,
        data: { posts: [createPost, ...posts] }
      });
    },
    onCompleted: () => {
      setTitle('');
      setBody('');
    },
    onError: (error) => {
      console.error('Error creating post:', error);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createPost({
      variables: {
        input: { title, body }
      }
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={e => setTitle(e.target.value)}
        placeholder="Title"
        disabled={loading}
      />
      <textarea
        value={body}
        onChange={e => setBody(e.target.value)}
        placeholder="Body"
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Post'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </form>
  );
}

export default CreatePost;
```

### 3. Cache Management

```javascript
// src/apollo/cache.js
import { InMemoryCache, makeVar } from '@apollo/client';

// Reactive variables
export const cartItemsVar = makeVar([]);
export const isLoggedInVar = makeVar(!!localStorage.getItem('authToken'));

export const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        cartItems: {
          read() {
            return cartItemsVar();
          }
        },
        isLoggedIn: {
          read() {
            return isLoggedInVar();
          }
        },
        // Pagination with field policies
        posts: {
          keyArgs: false,
          merge(existing = [], incoming, { args }) {
            const merged = existing ? existing.slice(0) : [];
            const offset = args?.offset || 0;

            for (let i = 0; i < incoming.length; i++) {
              merged[offset + i] = incoming[i];
            }

            return merged;
          }
        }
      }
    },
    Post: {
      fields: {
        // Computed field
        isLiked: {
          read(_, { readField }) {
            const likes = readField('likes');
            const currentUserId = localStorage.getItem('userId');
            return likes?.some(like => like.userId === currentUserId);
          }
        }
      }
    }
  }
});

// Cache manipulation helpers
export function addToCart(item) {
  const currentCart = cartItemsVar();
  cartItemsVar([...currentCart, item]);
}

export function removeFromCart(itemId) {
  const currentCart = cartItemsVar();
  cartItemsVar(currentCart.filter(item => item.id !== itemId));
}

// Manual cache updates
export function updatePostInCache(client, postId, updates) {
  const post = client.readFragment({
    id: `Post:${postId}`,
    fragment: gql`
      fragment PostUpdate on Post {
        id
        title
        body
      }
    `
  });

  if (post) {
    client.writeFragment({
      id: `Post:${postId}`,
      fragment: gql`
        fragment PostUpdate on Post {
          id
          title
          body
        }
      `,
      data: {
        ...post,
        ...updates
      }
    });
  }
}
```

### 4. Optimistic Updates

```javascript
// src/components/LikeButton.js
import React from 'react';
import { useMutation } from '@apollo/client';
import { gql } from '@apollo/client';

const LIKE_POST = gql`
  mutation LikePost($postId: ID!) {
    likePost(postId: $postId) {
      id
      likesCount
      isLiked
    }
  }
`;

function LikeButton({ post }) {
  const [likePost] = useMutation(LIKE_POST, {
    variables: { postId: post.id },
    optimisticResponse: {
      __typename: 'Mutation',
      likePost: {
        __typename: 'Post',
        id: post.id,
        likesCount: post.likesCount + 1,
        isLiked: true,
      }
    },
    update(cache, { data: { likePost } }) {
      cache.modify({
        id: cache.identify(post),
        fields: {
          likesCount() {
            return likePost.likesCount;
          },
          isLiked() {
            return likePost.isLiked;
          }
        }
      });
    }
  });

  return (
    <button onClick={() => likePost()}>
      {post.isLiked ? 'Unlike' : 'Like'} ({post.likesCount})
    </button>
  );
}

export default LikeButton;
```

### 5. Subscriptions

```javascript
// src/graphql/subscriptions.js
import { gql } from '@apollo/client';

export const POST_CREATED = gql`
  subscription OnPostCreated {
    postCreated {
      id
      title
      body
      author {
        id
        name
      }
      createdAt
    }
  }
`;

// src/components/RealtimePosts.js
import React from 'react';
import { useQuery, useSubscription } from '@apollo/client';
import { GET_POSTS } from '../graphql/queries';
import { POST_CREATED } from '../graphql/subscriptions';

function RealtimePosts() {
  const { data, loading } = useQuery(GET_POSTS);

  useSubscription(POST_CREATED, {
    onSubscriptionData: ({ client, subscriptionData }) => {
      const newPost = subscriptionData.data.postCreated;

      client.cache.modify({
        fields: {
          posts(existingPosts = []) {
            const newPostRef = client.cache.writeFragment({
              data: newPost,
              fragment: gql`
                fragment NewPost on Post {
                  id
                  title
                  body
                  author {
                    id
                    name
                  }
                }
              `
            });
            return [newPostRef, ...existingPosts];
          }
        }
      });
    }
  });

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      {data.posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.body}</p>
        </article>
      ))}
    </div>
  );
}

export default RealtimePosts;
```

### 6. Lazy Queries

```javascript
// src/components/SearchPosts.js
import React, { useState } from 'react';
import { useLazyQuery } from '@apollo/client';
import { gql } from '@apollo/client';

const SEARCH_POSTS = gql`
  query SearchPosts($query: String!) {
    searchPosts(query: $query) {
      id
      title
      excerpt
    }
  }
`;

function SearchPosts() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchPosts, { loading, data, error, called }] = useLazyQuery(
    SEARCH_POSTS,
    {
      fetchPolicy: 'network-only'
    }
  );

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      searchPosts({ variables: { query: searchTerm } });
    }
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          placeholder="Search posts..."
        />
        <button type="submit">Search</button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p>Error: {error.message}</p>}

      {called && data && (
        <ul>
          {data.searchPosts.map(post => (
            <li key={post.id}>
              <h3>{post.title}</h3>
              <p>{post.excerpt}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SearchPosts;
```

### 7. Error Handling

```javascript
// src/components/PostWithErrorHandling.js
import React from 'react';
import { useQuery } from '@apollo/client';
import { GET_POST } from '../graphql/queries';

function PostWithErrorHandling({ postId }) {
  const { loading, error, data } = useQuery(GET_POST, {
    variables: { id: postId },
    errorPolicy: 'all', // Return partial data and errors
    onError: (error) => {
      // Custom error handling
      if (error.networkError) {
        console.error('Network error:', error.networkError);
      }
      if (error.graphQLErrors) {
        error.graphQLErrors.forEach(({ message, extensions }) => {
          if (extensions.code === 'UNAUTHENTICATED') {
            // Redirect to login
            window.location.href = '/login';
          }
        });
      }
    }
  });

  if (loading) return <p>Loading...</p>;

  if (error && !data) {
    return (
      <div className="error">
        <h3>Something went wrong</h3>
        <p>{error.message}</p>
        <button onClick={() => window.location.reload()}>
          Try Again
        </button>
      </div>
    );
  }

  // Partial data with errors
  if (error && data) {
    console.warn('Partial data with errors:', error);
  }

  return (
    <article>
      <h1>{data.post.title}</h1>
      <p>{data.post.body}</p>
    </article>
  );
}

export default PostWithErrorHandling;
```

### 8. Pagination Patterns

```javascript
// src/components/PaginatedPosts.js
import React from 'react';
import { useQuery } from '@apollo/client';
import { gql } from '@apollo/client';

const GET_PAGINATED_POSTS = gql`
  query GetPaginatedPosts($cursor: String, $limit: Int!) {
    posts(cursor: $cursor, limit: $limit) {
      edges {
        node {
          id
          title
          body
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

function PaginatedPosts() {
  const { data, loading, fetchMore, networkStatus } = useQuery(
    GET_PAGINATED_POSTS,
    {
      variables: { limit: 10 },
      notifyOnNetworkStatusChange: true,
    }
  );

  const loadMore = () => {
    fetchMore({
      variables: {
        cursor: data.posts.pageInfo.endCursor
      }
    });
  };

  if (loading && networkStatus !== 3) return <p>Loading...</p>;

  return (
    <div>
      {data.posts.edges.map(({ node }) => (
        <article key={node.id}>
          <h2>{node.title}</h2>
          <p>{node.body}</p>
        </article>
      ))}

      {data.posts.pageInfo.hasNextPage && (
        <button onClick={loadMore} disabled={networkStatus === 3}>
          {networkStatus === 3 ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}

export default PaginatedPosts;
```

### 9. Local State Management

```javascript
// src/graphql/local.js
import { gql, makeVar } from '@apollo/client';

// Reactive variables
export const themeVar = makeVar('light');
export const sidebarOpenVar = makeVar(false);

// Local-only fields
export const LOCAL_STATE = gql`
  query GetLocalState {
    theme @client
    sidebarOpen @client
  }
`;

// Type policies for local state
export const localStateTypePolicies = {
  Query: {
    fields: {
      theme: {
        read() {
          return themeVar();
        }
      },
      sidebarOpen: {
        read() {
          return sidebarOpenVar();
        }
      }
    }
  }
};

// src/components/ThemeToggle.js
import React from 'react';
import { useQuery } from '@apollo/client';
import { LOCAL_STATE, themeVar } from '../graphql/local';

function ThemeToggle() {
  const { data } = useQuery(LOCAL_STATE);

  const toggleTheme = () => {
    const newTheme = data.theme === 'light' ? 'dark' : 'light';
    themeVar(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <button onClick={toggleTheme}>
      Current theme: {data.theme}
    </button>
  );
}

export default ThemeToggle;
```

### 10. Custom Hooks

```javascript
// src/hooks/usePosts.js
import { useQuery, useMutation } from '@apollo/client';
import { GET_POSTS, GET_POST } from '../graphql/queries';
import { CREATE_POST, UPDATE_POST, DELETE_POST } from '../graphql/mutations';

export function usePosts() {
  const { data, loading, error, refetch } = useQuery(GET_POSTS);

  return {
    posts: data?.posts || [],
    loading,
    error,
    refetch
  };
}

export function usePost(id) {
  const { data, loading, error } = useQuery(GET_POST, {
    variables: { id },
    skip: !id
  });

  return {
    post: data?.post,
    loading,
    error
  };
}

export function useCreatePost() {
  const [createPost, { loading, error }] = useMutation(CREATE_POST, {
    update(cache, { data: { createPost } }) {
      cache.modify({
        fields: {
          posts(existingPosts = []) {
            const newPostRef = cache.writeFragment({
              data: createPost,
              fragment: gql`
                fragment NewPost on Post {
                  id
                  title
                  body
                }
              `
            });
            return [newPostRef, ...existingPosts];
          }
        }
      });
    }
  });

  return { createPost, loading, error };
}

// Usage
function MyComponent() {
  const { posts, loading } = usePosts();
  const { createPost } = useCreatePost();

  // ...
}
```

## Best Practices

1. **Use fragments** - Share field selections across queries
2. **Implement error boundaries** - Gracefully handle errors
3. **Optimize cache configuration** - Configure type policies properly
4. **Use optimistic updates** - Improve perceived performance
5. **Implement proper loading states** - Show feedback during operations
6. **Avoid over-fetching** - Request only needed fields
7. **Leverage automatic cache** - Let Apollo handle caching
8. **Use reactive variables** - Manage local state efficiently
9. **Implement pagination** - Handle large datasets properly
10. **Monitor network status** - Track query states accurately

## Common Pitfalls

1. **Cache inconsistencies** - Not updating cache after mutations
2. **Over-fetching data** - Requesting unnecessary fields
3. **Missing error handling** - Not handling network/GraphQL errors
4. **Polling abuse** - Excessive polling causing performance issues
5. **Not using fragments** - Duplicating field selections
6. **Improper cache normalization** - Missing or wrong cache IDs
7. **Memory leaks** - Not cleaning up subscriptions
8. **Stale data** - Using wrong fetch policies
9. **Missing loading states** - Poor user experience
10. **Auth token issues** - Not refreshing expired tokens

## When to Use

- Building React applications with GraphQL APIs
- Managing complex application state
- Implementing real-time features
- Creating data-driven UIs
- Building mobile apps with React Native
- Developing admin dashboards
- Creating collaborative applications
- Implementing offline-first features
- Building e-commerce platforms
- Developing social media applications

## Resources

- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [Apollo Client GitHub](https://github.com/apollographql/apollo-client)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Apollo Blog](https://www.apollographql.com/blog/)
- [Full-Stack GraphQL Course](https://www.howtographql.com/)
