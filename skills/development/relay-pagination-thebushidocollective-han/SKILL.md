---
name: relay-pagination
description: Use when relay pagination with cursor-based pagination, infinite scroll, load more patterns, and connection protocols.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Relay Pagination

Master Relay's cursor-based pagination for efficiently loading and displaying
large datasets with infinite scroll and load more patterns.

## Overview

Relay implements the GraphQL Cursor Connections Specification for efficient
pagination. It provides hooks like usePaginationFragment for declarative
pagination with automatic cache updates and connection management.

## Installation and Setup

### Pagination Query Structure

```graphql
# schema.graphql
type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type PostEdge {
  cursor: String!
  node: Post!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Post {
  id: ID!
  title: String!
  body: String!
}
```

## Core Patterns

### 1. Basic Pagination

```javascript
// PostsList.jsx
import { graphql, usePaginationFragment } from 'react-relay';

const PostsListFragment = graphql`
  fragment PostsList_query on Query
  @refetchable(queryName: "PostsListPaginationQuery")
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 10 }
    after: { type: "String" }
  ) {
    posts(first: $first, after: $after)
    @connection(key: "PostsList_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

function PostsList({ query }) {
  const {
    data,
    loadNext,
    loadPrevious,
    hasNext,
    hasPrevious,
    isLoadingNext,
    isLoadingPrevious,
    refetch
  } = usePaginationFragment(PostsListFragment, query);

  return (
    <div>
      <button
        onClick={() => refetch({ first: 10 })}
        disabled={isLoadingNext}
      >
        Refresh
      </button>

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <button
          onClick={() => loadNext(10)}
          disabled={isLoadingNext}
        >
          {isLoadingNext ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}

export default PostsList;
```

### 2. Infinite Scroll

```javascript
// InfiniteScrollPosts.jsx
import { useEffect, useRef } from 'react';
import { graphql, usePaginationFragment } from 'react-relay';

const InfiniteScrollFragment = graphql`
  fragment InfiniteScrollPosts_query on Query
  @refetchable(queryName: "InfiniteScrollPostsQuery")
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 20 }
    after: { type: "String" }
  ) {
    posts(first: $first, after: $after)
    @connection(key: "InfiniteScroll_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function InfiniteScrollPosts({ query }) {
  const { data, loadNext, hasNext, isLoadingNext } = usePaginationFragment(
    InfiniteScrollFragment,
    query
  );

  const observerRef = useRef();
  const loadMoreRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNext && !isLoadingNext) {
          loadNext(20);
        }
      },
      { threshold: 0.5 }
    );

    const currentRef = loadMoreRef.current;
    if (currentRef) {
      observer.observe(currentRef);
    }

    observerRef.current = observer;

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, [hasNext, isLoadingNext, loadNext]);

  return (
    <div>
      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <div ref={loadMoreRef} className="load-more-trigger">
          {isLoadingNext && <Spinner />}
        </div>
      )}

      {!hasNext && <div>No more posts</div>}
    </div>
  );
}
```

### 3. Bidirectional Pagination

```javascript
// BidirectionalPosts.jsx
const BidirectionalFragment = graphql`
  fragment BidirectionalPosts_query on Query
  @refetchable(queryName: "BidirectionalPostsQuery")
  @argumentDefinitions(
    first: { type: "Int" }
    after: { type: "String" }
    last: { type: "Int" }
    before: { type: "String" }
  ) {
    posts(first: $first, after: $after, last: $last, before: $before)
    @connection(key: "Bidirectional_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
      }
    }
  }
`;

function BidirectionalPosts({ query }) {
  const {
    data,
    loadNext,
    loadPrevious,
    hasNext,
    hasPrevious,
    isLoadingNext,
    isLoadingPrevious
  } = usePaginationFragment(BidirectionalFragment, query);

  return (
    <div>
      {hasPrevious && (
        <button
          onClick={() => loadPrevious(10)}
          disabled={isLoadingPrevious}
        >
          {isLoadingPrevious ? 'Loading...' : 'Load Previous'}
        </button>
      )}

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <button
          onClick={() => loadNext(10)}
          disabled={isLoadingNext}
        >
          {isLoadingNext ? 'Loading...' : 'Load Next'}
        </button>
      )}
    </div>
  );
}
```

### 4. Filtered Pagination

```javascript
// FilteredPosts.jsx
const FilteredPostsFragment = graphql`
  fragment FilteredPosts_query on Query
  @refetchable(queryName: "FilteredPostsQuery")
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 10 }
    after: { type: "String" }
    status: { type: "PostStatus" }
    authorId: { type: "ID" }
  ) {
    posts(
      first: $first
      after: $after
      status: $status
      authorId: $authorId
    )
    @connection(key: "FilteredPosts_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function FilteredPosts({ query }) {
  const [status, setStatus] = useState('PUBLISHED');
  const [authorId, setAuthorId] = useState(null);

  const { data, loadNext, hasNext, refetch } = usePaginationFragment(
    FilteredPostsFragment,
    query
  );

  const handleFilterChange = (newStatus, newAuthorId) => {
    setStatus(newStatus);
    setAuthorId(newAuthorId);

    refetch({
      first: 10,
      after: null,
      status: newStatus,
      authorId: newAuthorId
    });
  };

  return (
    <div>
      <FilterControls
        status={status}
        authorId={authorId}
        onChange={handleFilterChange}
      />

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <button onClick={() => loadNext(10)}>Load More</button>
      )}
    </div>
  );
}
```

### 5. Pagination with Search

```javascript
// SearchablePosts.jsx
const SearchablePostsFragment = graphql`
  fragment SearchablePosts_query on Query
  @refetchable(queryName: "SearchablePostsQuery")
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 10 }
    after: { type: "String" }
    searchTerm: { type: "String" }
  ) {
    posts(first: $first, after: $after, searchTerm: $searchTerm)
    @connection(key: "SearchablePosts_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
      totalCount
    }
  }
`;

function SearchablePosts({ query }) {
  const [searchTerm, setSearchTerm] = useState('');
  const { data, loadNext, hasNext, refetch, isLoadingNext } =
    usePaginationFragment(SearchablePostsFragment, query);

  const handleSearch = (term) => {
    setSearchTerm(term);
    refetch({
      first: 10,
      after: null,
      searchTerm: term
    });
  };

  return (
    <div>
      <SearchInput
        value={searchTerm}
        onChange={handleSearch}
        placeholder="Search posts..."
      />

      <div>
        Showing {data.posts.edges.length} of {data.posts.totalCount} posts
      </div>

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <button onClick={() => loadNext(10)} disabled={isLoadingNext}>
          {isLoadingNext ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

### 6. Optimistic Pagination Updates

```javascript
// OptimisticPaginationPosts.jsx
const CreatePostMutation = graphql`
  mutation OptimisticPaginationCreatePostMutation(
    $input: CreatePostInput!
    $connections: [ID!]!
  ) {
    createPost(input: $input) {
      postEdge @prependEdge(connections: $connections) {
        cursor
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function OptimisticPaginationPosts({ query }) {
  const { data } = usePaginationFragment(PostsFragment, query);
  const [commit] = useMutation(CreatePostMutation);

  const connectionID = ConnectionHandler.getConnectionID(
    'client:root',
    'Posts_posts'
  );

  const handleCreate = (title, body) => {
    commit({
      variables: {
        input: { title, body },
        connections: [connectionID]
      },

      optimisticResponse: {
        createPost: {
          postEdge: {
            cursor: 'temp-cursor',
            node: {
              id: `temp-${Date.now()}`,
              title,
              body,
              createdAt: new Date().toISOString(),
              author: {
                id: currentUser.id,
                name: currentUser.name
              }
            }
          }
        }
      }
    });
  };

  return (
    <div>
      <CreatePostForm onSubmit={handleCreate} />
      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}
    </div>
  );
}
```

### 7. Paginated Tabs

```javascript
// TabbedPosts.jsx
const TabbedPostsFragment = graphql`
  fragment TabbedPosts_user on User
  @refetchable(queryName: "TabbedPostsQuery")
  @argumentDefinitions(
    draftsFirst: { type: "Int", defaultValue: 10 }
    draftsAfter: { type: "String" }
    publishedFirst: { type: "Int", defaultValue: 10 }
    publishedAfter: { type: "String" }
  ) {
    draftPosts: posts(
      first: $draftsFirst
      after: $draftsAfter
      status: DRAFT
    )
    @connection(key: "TabbedPosts_draftPosts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }

    publishedPosts: posts(
      first: $publishedFirst
      after: $publishedAfter
      status: PUBLISHED
    )
    @connection(key: "TabbedPosts_publishedPosts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function TabbedPosts({ user }) {
  const [activeTab, setActiveTab] = useState('published');
  const { data } = usePaginationFragment(TabbedPostsFragment, user);

  const posts =
    activeTab === 'draft' ? data.draftPosts : data.publishedPosts;

  return (
    <div>
      <Tabs value={activeTab} onChange={setActiveTab}>
        <Tab value="published">Published</Tab>
        <Tab value="draft">Drafts</Tab>
      </Tabs>

      {posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}
    </div>
  );
}
```

### 8. Virtual Scrolling with Pagination

```javascript
// VirtualizedPosts.jsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { graphql, usePaginationFragment } from 'react-relay';

const VirtualizedPostsFragment = graphql`
  fragment VirtualizedPosts_query on Query
  @refetchable(queryName: "VirtualizedPostsQuery")
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 50 }
    after: { type: "String" }
  ) {
    posts(first: $first, after: $after)
    @connection(key: "VirtualizedPosts_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function VirtualizedPosts({ query }) {
  const { data, loadNext, hasNext, isLoadingNext } = usePaginationFragment(
    VirtualizedPostsFragment,
    query
  );

  const parentRef = useRef();
  const posts = data.posts.edges.map(e => e.node);

  const virtualizer = useVirtualizer({
    count: posts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 200,
    overscan: 5
  });

  useEffect(() => {
    const [lastItem] = [...virtualizer.getVirtualItems()].reverse();

    if (!lastItem) return;

    if (
      lastItem.index >= posts.length - 1 &&
      hasNext &&
      !isLoadingNext
    ) {
      loadNext(50);
    }
  }, [
    hasNext,
    loadNext,
    isLoadingNext,
    posts.length,
    virtualizer.getVirtualItems()
  ]);

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`
            }}
          >
            <PostCard post={posts[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 9. Pagination State Management

```javascript
// PaginationStateManager.jsx
function PaginationStateManager({ query }) {
  const {
    data,
    loadNext,
    hasNext,
    isLoadingNext,
    refetch
  } = usePaginationFragment(PostsFragment, query);

  const [paginationState, setPaginationState] = useState({
    currentPage: 1,
    itemsPerPage: 10,
    totalLoaded: 0
  });

  const handleLoadMore = () => {
    const itemsToLoad = paginationState.itemsPerPage;
    loadNext(itemsToLoad);

    setPaginationState(prev => ({
      ...prev,
      currentPage: prev.currentPage + 1,
      totalLoaded: prev.totalLoaded + itemsToLoad
    }));
  };

  const handleChangePageSize = (newSize) => {
    setPaginationState(prev => ({
      ...prev,
      itemsPerPage: newSize
    }));

    refetch({
      first: newSize,
      after: null
    });
  };

  return (
    <div>
      <div>
        Page {paginationState.currentPage} -
        Loaded {paginationState.totalLoaded} items
      </div>

      <select
        value={paginationState.itemsPerPage}
        onChange={(e) => handleChangePageSize(Number(e.target.value))}
      >
        <option value={10}>10 per page</option>
        <option value={25}>25 per page</option>
        <option value={50}>50 per page</option>
      </select>

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && (
        <button onClick={handleLoadMore} disabled={isLoadingNext}>
          Load More
        </button>
      )}
    </div>
  );
}
```

### 10. Custom Pagination Hook

```javascript
// hooks/usePagination.js
import { useState, useCallback } from 'react';
import { usePaginationFragment } from 'react-relay';

export function usePagination(fragment, fragmentRef, options = {}) {
  const {
    onLoadMore,
    onLoadPrevious,
    onRefetch,
    pageSize = 10
  } = options;

  const {
    data,
    loadNext,
    loadPrevious,
    hasNext,
    hasPrevious,
    isLoadingNext,
    isLoadingPrevious,
    refetch
  } = usePaginationFragment(fragment, fragmentRef);

  const [page, setPage] = useState(1);

  const handleLoadNext = useCallback(() => {
    loadNext(pageSize);
    setPage(p => p + 1);
    onLoadMore?.();
  }, [loadNext, pageSize, onLoadMore]);

  const handleLoadPrevious = useCallback(() => {
    loadPrevious(pageSize);
    setPage(p => Math.max(1, p - 1));
    onLoadPrevious?.();
  }, [loadPrevious, pageSize, onLoadPrevious]);

  const handleRefetch = useCallback((variables) => {
    refetch(variables);
    setPage(1);
    onRefetch?.();
  }, [refetch, onRefetch]);

  return {
    data,
    page,
    hasNext,
    hasPrevious,
    isLoadingNext,
    isLoadingPrevious,
    loadNext: handleLoadNext,
    loadPrevious: handleLoadPrevious,
    refetch: handleRefetch
  };
}

// Usage
function PostsList({ query }) {
  const {
    data,
    page,
    hasNext,
    loadNext,
    refetch
  } = usePagination(PostsFragment, query, {
    pageSize: 20,
    onLoadMore: () => console.log('Loaded more'),
    onRefetch: () => console.log('Refetched')
  });

  return (
    <div>
      <div>Page {page}</div>
      <button onClick={() => refetch({ first: 20 })}>Refresh</button>

      {data.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {hasNext && <button onClick={loadNext}>Load More</button>}
    </div>
  );
}
```

## Best Practices

1. **Use @connection directive** - Ensure proper cache updates
2. **Implement loading states** - Show feedback during pagination
3. **Handle edge cases** - Empty states, no more data
4. **Optimize page size** - Balance UX and performance
5. **Use infinite scroll wisely** - Consider virtual scrolling for large lists
6. **Implement search/filter** - Allow users to narrow results
7. **Cache pagination state** - Preserve scroll position
8. **Handle errors gracefully** - Retry failed pagination requests
9. **Test pagination thoroughly** - Edge cases, network failures
10. **Monitor performance** - Track pagination metrics

## Common Pitfalls

1. **Missing @connection directive** - Cache updates fail
2. **Incorrect cursor management** - Duplicate or missing items
3. **No loading states** - Poor user experience
4. **Over-fetching** - Requesting too many items per page
5. **Memory leaks** - Not cleaning up observers
6. **Missing error handling** - Failed requests break pagination
7. **Inconsistent page sizes** - Confusing user experience
8. **Not handling empty states** - Poor UX for no results
9. **Race conditions** - Multiple concurrent pagination requests
10. **Missing accessibility** - Keyboard navigation, screen readers

## When to Use

- Displaying large lists of data
- Building infinite scroll interfaces
- Creating feed-based applications
- Implementing search results
- Building e-commerce product listings
- Creating social media timelines
- Developing comment threads
- Building admin dashboards
- Creating data tables
- Implementing file browsers

## Resources

- [Relay Pagination](https://relay.dev/docs/guided-tour/list-data/pagination/)
- [Connection Specification](https://relay.dev/graphql/connections.htm)
- [usePaginationFragment](https://relay.dev/docs/api-reference/use-pagination-fragment/)
- [Cursor Connections](https://graphql.org/learn/pagination/)
- [Relay Examples](https://github.com/relayjs/relay-examples)
