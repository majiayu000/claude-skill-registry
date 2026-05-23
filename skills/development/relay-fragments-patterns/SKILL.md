---
name: relay-fragments-patterns
description: Use when relay fragment composition, data masking, colocation, and container patterns for React applications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Relay Fragments Patterns

Master Relay's fragment composition for building maintainable React
applications with proper data dependencies and component colocation.

## Overview

Relay fragments enable component-level data declaration with automatic
composition, data masking, and optimal data fetching. Fragments colocate data
requirements with components for better maintainability.

## Installation and Setup

### Installing Relay

```bash
# Install Relay packages
npm install react-relay relay-runtime

# Install Relay compiler
npm install --save-dev relay-compiler babel-plugin-relay

# Install GraphQL
npm install graphql
```

### Relay Configuration

```javascript
// relay.config.js
module.exports = {
  src: './src',
  schema: './schema.graphql',
  exclude: ['**/node_modules/**', '**/__mocks__/**', '**/__generated__/**'],
  language: 'typescript',
  artifactDirectory: './src/__generated__'
};

// package.json
{
  "scripts": {
    "relay": "relay-compiler",
    "relay:watch": "relay-compiler --watch"
  }
}
```

### Environment Setup

```javascript
// RelayEnvironment.js
import {
  Environment,
  Network,
  RecordSource,
  Store
} from 'relay-runtime';

function fetchQuery(operation, variables) {
  return fetch('http://localhost:4000/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      query: operation.text,
      variables
    })
  }).then(response => response.json());
}

const environment = new Environment({
  network: Network.create(fetchQuery),
  store: new Store(new RecordSource())
});

export default environment;
```

## Core Patterns

### 1. Basic Fragment Definition

```javascript
// PostCard.jsx
import { graphql, useFragment } from 'react-relay';

const PostCardFragment = graphql`
  fragment PostCard_post on Post {
    id
    title
    excerpt
    publishedAt
    author {
      name
      avatar
    }
  }
`;

function PostCard({ post }) {
  const data = useFragment(PostCardFragment, post);

  return (
    <article>
      <h2>{data.title}</h2>
      <p>{data.excerpt}</p>
      <div>
        <img src={data.author.avatar} alt={data.author.name} />
        <span>{data.author.name}</span>
      </div>
      <time>{data.publishedAt}</time>
    </article>
  );
}

export default PostCard;
```

### 2. Fragment Composition

```javascript
// UserProfile.jsx
const UserProfileFragment = graphql`
  fragment UserProfile_user on User {
    id
    name
    bio
    ...UserAvatar_user
    ...UserStats_user
  }
`;

function UserProfile({ user }) {
  const data = useFragment(UserProfileFragment, user);

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.bio}</p>
      <UserAvatar user={data} />
      <UserStats user={data} />
    </div>
  );
}

// UserAvatar.jsx
const UserAvatarFragment = graphql`
  fragment UserAvatar_user on User {
    name
    avatar
    isOnline
  }
`;

function UserAvatar({ user }) {
  const data = useFragment(UserAvatarFragment, user);

  return (
    <div className="avatar-container">
      <img src={data.avatar} alt={data.name} />
      {data.isOnline && <span className="online-indicator" />}
    </div>
  );
}

// UserStats.jsx
const UserStatsFragment = graphql`
  fragment UserStats_user on User {
    postsCount
    followersCount
    followingCount
  }
`;

function UserStats({ user }) {
  const data = useFragment(UserStatsFragment, user);

  return (
    <div className="stats">
      <div>Posts: {data.postsCount}</div>
      <div>Followers: {data.followersCount}</div>
      <div>Following: {data.followingCount}</div>
    </div>
  );
}
```

### 3. Fragment Arguments

```javascript
// Post.jsx
const PostFragment = graphql`
  fragment Post_post on Post
  @argumentDefinitions(
    includeComments: { type: "Boolean!", defaultValue: false }
    commentsFirst: { type: "Int", defaultValue: 10 }
  ) {
    id
    title
    body
    comments(first: $commentsFirst) @include(if: $includeComments) {
      edges {
        node {
          ...Comment_comment
        }
      }
    }
  }
`;

function Post({ post, showComments = false }) {
  const data = useFragment(
    PostFragment,
    post,
    {
      includeComments: showComments,
      commentsFirst: 20
    }
  );

  return (
    <article>
      <h1>{data.title}</h1>
      <div>{data.body}</div>
      {showComments && (
        <CommentsList comments={data.comments.edges.map(e => e.node)} />
      )}
    </article>
  );
}
```

### 4. Data Masking

```javascript
// Parent component
const ParentFragment = graphql`
  fragment Parent_data on Query {
    user {
      id
      ...Child_user
    }
  }
`;

function Parent({ data }) {
  const parentData = useFragment(ParentFragment, data);

  // parentData.user only contains id and fragment reference
  // Cannot access user.name here (data masking)

  return (
    <div>
      <h1>User ID: {parentData.user.id}</h1>
      <Child user={parentData.user} />
    </div>
  );
}

// Child component
const ChildFragment = graphql`
  fragment Child_user on User {
    name
    email
    avatar
  }
`;

function Child({ user }) {
  const data = useFragment(ChildFragment, user);

  // Only Child can access name, email, avatar
  return (
    <div>
      <h2>{data.name}</h2>
      <p>{data.email}</p>
      <img src={data.avatar} alt={data.name} />
    </div>
  );
}
```

### 5. Fragment with Connections

```javascript
// PostsList.jsx
const PostsListFragment = graphql`
  fragment PostsList_query on Query
  @argumentDefinitions(
    first: { type: "Int", defaultValue: 10 }
    after: { type: "String" }
  )
  @refetchable(queryName: "PostsListRefetchQuery") {
    posts(first: $first, after: $after)
    @connection(key: "PostsList_posts") {
      edges {
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function PostsList({ query }) {
  const { data, loadNext, hasNext, isLoadingNext } = usePaginationFragment(
    PostsListFragment,
    query
  );

  return (
    <div>
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
```

### 6. Refetchable Fragments

```javascript
// UserProfile.jsx
const UserProfileFragment = graphql`
  fragment UserProfile_user on User
  @refetchable(queryName: "UserProfileRefetchQuery") {
    id
    name
    bio
    posts(first: 10) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
`;

function UserProfile({ user }) {
  const [data, refetch] = useRefetchableFragment(
    UserProfileFragment,
    user
  );

  const handleRefresh = () => {
    refetch({}, { fetchPolicy: 'network-only' });
  };

  return (
    <div>
      <button onClick={handleRefresh}>Refresh</button>
      <h1>{data.name}</h1>
      <p>{data.bio}</p>
      <PostsList posts={data.posts.edges} />
    </div>
  );
}
```

### 7. Plural Fragments

```javascript
// PostsList.jsx
const PostsListFragment = graphql`
  fragment PostsList_posts on Post @relay(plural: true) {
    id
    title
    excerpt
  }
`;

function PostsList({ posts }) {
  const data = useFragment(PostsListFragment, posts);

  return (
    <div>
      {data.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}

// Usage
const query = graphql`
  query PostsQuery {
    posts {
      ...PostsList_posts
    }
  }
`;
```

### 8. Conditional Fragments

```javascript
// Content.jsx
const ContentFragment = graphql`
  fragment Content_content on Content {
    __typename
    ... on Post {
      title
      body
      author {
        name
      }
    }
    ... on Video {
      title
      duration
      thumbnailUrl
      creator {
        name
      }
    }
    ... on Image {
      title
      imageUrl
      photographer {
        name
      }
    }
  }
`;

function Content({ content }) {
  const data = useFragment(ContentFragment, content);

  switch (data.__typename) {
    case 'Post':
      return (
        <article>
          <h2>{data.title}</h2>
          <p>{data.body}</p>
          <span>By {data.author.name}</span>
        </article>
      );

    case 'Video':
      return (
        <div>
          <video src={data.thumbnailUrl} />
          <h2>{data.title}</h2>
          <span>Duration: {data.duration}s</span>
          <span>By {data.creator.name}</span>
        </div>
      );

    case 'Image':
      return (
        <figure>
          <img src={data.imageUrl} alt={data.title} />
          <figcaption>
            {data.title} by {data.photographer.name}
          </figcaption>
        </figure>
      );

    default:
      return null;
  }
}
```

### 9. Fragment Containers Legacy Pattern

```javascript
// Legacy container pattern (v1-11)
import { createFragmentContainer, graphql } from 'react-relay';

class PostCard extends React.Component {
  render() {
    const { post } = this.props;
    return (
      <article>
        <h2>{post.title}</h2>
        <p>{post.excerpt}</p>
      </article>
    );
  }
}

export default createFragmentContainer(PostCard, {
  post: graphql`
    fragment PostCard_post on Post {
      id
      title
      excerpt
    }
  `
});

// Modern hooks pattern (v12+)
function PostCard({ post }) {
  const data = useFragment(
    graphql`
      fragment PostCard_post on Post {
        id
        title
        excerpt
      }
    `,
    post
  );

  return (
    <article>
      <h2>{data.title}</h2>
      <p>{data.excerpt}</p>
    </article>
  );
}
```

### 10. Advanced Fragment Patterns

```javascript
// Recursive fragments
const CommentFragment = graphql`
  fragment Comment_comment on Comment {
    id
    body
    author {
      name
    }
    replies(first: 5) {
      edges {
        node {
          ...Comment_comment
        }
      }
    }
  }
`;

function Comment({ comment, depth = 0 }) {
  const data = useFragment(CommentFragment, comment);

  if (depth > 3) return null; // Prevent infinite recursion

  return (
    <div style={{ marginLeft: depth * 20 }}>
      <p>{data.body}</p>
      <span>{data.author.name}</span>

      {data.replies?.edges.map(({ node }) => (
        <Comment key={node.id} comment={node} depth={depth + 1} />
      ))}
    </div>
  );
}

// Fragment with inline data
const PostWithInlineFragment = graphql`
  fragment PostWithInline_post on Post {
    id
    title
    author {
      ... on User {
        id
        name
        isVerified
      }
      ... on Organization {
        id
        name
        type
      }
    }
  }
`;

// Fragment with directives
const ConditionalFragment = graphql`
  fragment Conditional_post on Post
  @argumentDefinitions(
    includeLikes: { type: "Boolean!", defaultValue: false }
    includeComments: { type: "Boolean!", defaultValue: true }
  ) {
    id
    title
    likesCount @include(if: $includeLikes)
    comments(first: 10) @include(if: $includeComments) {
      edges {
        node {
          id
          body
        }
      }
    }
  }
`;

// Fragment with required fields
const RequiredFieldsFragment = graphql`
  fragment RequiredFields_user on User {
    id
    name @required(action: LOG)
    email @required(action: THROW)
    avatar @required(action: NONE)
  }
`;
```

## Best Practices

1. **Colocate fragments with components** - Keep data requirements together
2. **Use fragment composition** - Build complex queries from simple fragments
3. **Leverage data masking** - Prevent tight coupling between components
4. **Define minimal fragments** - Request only necessary fields
5. **Use arguments for flexibility** - Make fragments reusable
6. **Follow naming conventions** - ComponentName_propName pattern
7. **Avoid circular dependencies** - Design fragment hierarchy carefully
8. **Use refetchable fragments** - Enable component-level refetching
9. **Handle loading states** - Provide feedback during data fetches
10. **Type fragments properly** - Ensure type safety with TypeScript

## Common Pitfalls

1. **Fragment overfetching** - Requesting unnecessary fields
2. **Missing data masking** - Accessing non-declared fields
3. **Circular fragment references** - Creating dependency cycles
4. **Improper fragment composition** - Not spreading child fragments
5. **Hardcoded values** - Not using fragment arguments
6. **Breaking data contracts** - Changing fragment fields carelessly
7. **Missing fragment keys** - Not providing unique keys in lists
8. **Ignoring type conditions** - Not handling union types properly
9. **Excessive nesting** - Creating overly deep fragment hierarchies
10. **Poor error handling** - Not handling missing data gracefully

## When to Use

- Building React applications with GraphQL
- Implementing component-driven architecture
- Creating reusable UI components
- Developing data-intensive applications
- Building social media platforms
- Creating e-commerce applications
- Implementing collaborative tools
- Developing content management systems
- Building admin dashboards
- Creating mobile applications with React Native

## Resources

- [Relay Documentation](https://relay.dev/)
- [Relay Fragments Guide](https://relay.dev/docs/guided-tour/rendering/fragments/)
- [Relay Compiler](https://relay.dev/docs/guides/compiler/)
- [GraphQL Specification](https://spec.graphql.org/)
- [Relay Examples](https://github.com/relayjs/relay-examples)
- [Relay Community](https://github.com/facebook/relay/discussions)
