---
name: relay-mutations-patterns
description: Use when relay mutations with optimistic updates, connections, declarative mutations, and error handling.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Relay Mutations Patterns

Master Relay mutations for building interactive applications with optimistic
updates, connection handling, and declarative data updates.

## Overview

Relay mutations provide a declarative way to update data with automatic cache
updates, optimistic responses, and rollback on error. Mutations integrate
seamlessly with Relay's normalized cache and connection protocol.

## Installation and Setup

### Mutation Configuration

```javascript
// mutations/CreatePostMutation.js
import { graphql, commitMutation } from 'react-relay';
import environment from '../RelayEnvironment';

const mutation = graphql`
  mutation CreatePostMutation($input: CreatePostInput!) {
    createPost(input: $input) {
      postEdge {
        __typename
        cursor
        node {
          id
          title
          body
          createdAt
          author {
            id
            name
          }
        }
      }
    }
  }
`;

export default function createPost(title, body) {
  return new Promise((resolve, reject) => {
    commitMutation(environment, {
      mutation,
      variables: {
        input: { title, body }
      },
      onCompleted: (response, errors) => {
        if (errors) {
          reject(errors);
        } else {
          resolve(response);
        }
      },
      onError: reject
    });
  });
}
```

## Core Patterns

### 1. Basic Mutation

```javascript
// CreatePost.jsx
import { graphql, useMutation } from 'react-relay';

const CreatePostMutation = graphql`
  mutation CreatePostMutation($input: CreatePostInput!) {
    createPost(input: $input) {
      post {
        id
        title
        body
        author {
          id
          name
        }
      }
    }
  }
`;

function CreatePost() {
  const [commit, isInFlight] = useMutation(CreatePostMutation);

  const handleSubmit = (title, body) => {
    commit({
      variables: {
        input: { title, body }
      },
      onCompleted: (response, errors) => {
        if (errors) {
          console.error('Errors:', errors);
        } else {
          console.log('Post created:', response.createPost.post);
        }
      },
      onError: (error) => {
        console.error('Network error:', error);
      }
    });
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      handleSubmit(e.target.title.value, e.target.body.value);
    }}>
      <input name="title" placeholder="Title" disabled={isInFlight} />
      <textarea name="body" placeholder="Body" disabled={isInFlight} />
      <button type="submit" disabled={isInFlight}>
        {isInFlight ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

### 2. Optimistic Updates

```javascript
// LikeButton.jsx
import { graphql, useMutation } from 'react-relay';

const LikePostMutation = graphql`
  mutation LikePostMutation($input: LikePostInput!) {
    likePost(input: $input) {
      post {
        id
        likesCount
        viewerHasLiked
      }
    }
  }
`;

function LikeButton({ post }) {
  const [commit, isInFlight] = useMutation(LikePostMutation);

  const handleLike = () => {
    commit({
      variables: {
        input: { postId: post.id }
      },

      // Optimistic response
      optimisticResponse: {
        likePost: {
          post: {
            id: post.id,
            likesCount: post.likesCount + 1,
            viewerHasLiked: true
          }
        }
      },

      // Optimistic updater
      optimisticUpdater: (store) => {
        const postRecord = store.get(post.id);
        if (postRecord) {
          postRecord.setValue(post.likesCount + 1, 'likesCount');
          postRecord.setValue(true, 'viewerHasLiked');
        }
      }
    });
  };

  return (
    <button onClick={handleLike} disabled={isInFlight}>
      {post.viewerHasLiked ? 'Unlike' : 'Like'} ({post.likesCount})
    </button>
  );
}
```

### 3. Connection Updates

```javascript
// CreateComment.jsx
const CreateCommentMutation = graphql`
  mutation CreateCommentMutation(
    $input: CreateCommentInput!
    $connections: [ID!]!
  ) {
    createComment(input: $input) {
      commentEdge @appendEdge(connections: $connections) {
        cursor
        node {
          id
          body
          createdAt
          author {
            id
            name
            avatar
          }
        }
      }
    }
  }
`;

function CreateComment({ postId, connectionID }) {
  const [commit, isInFlight] = useMutation(CreateCommentMutation);

  const handleSubmit = (body) => {
    commit({
      variables: {
        input: { postId, body },
        connections: [connectionID]
      },

      // No manual updater needed, @appendEdge handles it

      optimisticResponse: {
        createComment: {
          commentEdge: {
            cursor: 'temp-cursor',
            node: {
              id: `temp-${Date.now()}`,
              body,
              createdAt: new Date().toISOString(),
              author: {
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar
              }
            }
          }
        }
      }
    });
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      handleSubmit(e.target.body.value);
      e.target.reset();
    }}>
      <textarea name="body" placeholder="Add a comment..." />
      <button type="submit" disabled={isInFlight}>Post</button>
    </form>
  );
}

// Usage with connection ID
function Post({ post }) {
  const data = useFragment(
    graphql`
      fragment Post_post on Post {
        id
        comments(first: 10)
        @connection(key: "Post_comments") {
          edges {
            node {
              id
              ...Comment_comment
            }
          }
        }
      }
    `,
    post
  );

  const connectionID = ConnectionHandler.getConnectionID(
    post.id,
    'Post_comments'
  );

  return (
    <div>
      <CommentsList comments={data.comments.edges} />
      <CreateComment postId={post.id} connectionID={connectionID} />
    </div>
  );
}
```

### 4. Manual Cache Updates

```javascript
// DeletePost.jsx
const DeletePostMutation = graphql`
  mutation DeletePostMutation($input: DeletePostInput!) {
    deletePost(input: $input) {
      deletedPostId
    }
  }
`;

function DeletePost({ postId, onDelete }) {
  const [commit] = useMutation(DeletePostMutation);

  const handleDelete = () => {
    commit({
      variables: {
        input: { id: postId }
      },

      updater: (store) => {
        // Remove from connection
        const root = store.getRoot();
        const connection = ConnectionHandler.getConnection(
          root,
          'PostsList_posts'
        );

        if (connection) {
          ConnectionHandler.deleteNode(connection, postId);
        }

        // Delete the record
        store.delete(postId);
      },

      optimisticUpdater: (store) => {
        const root = store.getRoot();
        const connection = ConnectionHandler.getConnection(
          root,
          'PostsList_posts'
        );

        if (connection) {
          ConnectionHandler.deleteNode(connection, postId);
        }
      },

      onCompleted: () => {
        onDelete?.();
      }
    });
  };

  return (
    <button onClick={handleDelete} className="delete-button">
      Delete
    </button>
  );
}
```

### 5. Complex Updater Functions

```javascript
// UpdatePost.jsx
const UpdatePostMutation = graphql`
  mutation UpdatePostMutation($input: UpdatePostInput!) {
    updatePost(input: $input) {
      post {
        id
        title
        body
        status
        updatedAt
      }
    }
  }
`;

function UpdatePost({ post }) {
  const [commit] = useMutation(UpdatePostMutation);

  const handleUpdate = (title, body, status) => {
    commit({
      variables: {
        input: {
          id: post.id,
          title,
          body,
          status
        }
      },

      updater: (store, data) => {
        const updatedPost = data.updatePost.post;
        const postRecord = store.get(updatedPost.id);

        if (postRecord) {
          postRecord.setValue(updatedPost.title, 'title');
          postRecord.setValue(updatedPost.body, 'body');
          postRecord.setValue(updatedPost.status, 'status');
          postRecord.setValue(updatedPost.updatedAt, 'updatedAt');

          // Update related records
          const author = postRecord.getLinkedRecord('author');
          if (author) {
            const postsCount = author.getValue('postsCount') || 0;
            author.setValue(postsCount, 'postsCount');
          }
        }
      },

      optimisticResponse: {
        updatePost: {
          post: {
            id: post.id,
            title,
            body,
            status,
            updatedAt: new Date().toISOString()
          }
        }
      }
    });
  };

  return <EditForm post={post} onSubmit={handleUpdate} />;
}
```

### 6. Multiple Mutations

```javascript
// PublishPost.jsx
const PublishPostMutation = graphql`
  mutation PublishPostMutation($input: PublishPostInput!) {
    publishPost(input: $input) {
      post {
        id
        status
        publishedAt
      }
      edge @prependEdge(connections: $connections) {
        cursor
        node {
          id
          ...PostCard_post
        }
      }
    }
  }
`;

function PublishPost({ post, draftConnectionID, publishedConnectionID }) {
  const [commit] = useMutation(PublishPostMutation);

  const handlePublish = () => {
    commit({
      variables: {
        input: { id: post.id },
        connections: [publishedConnectionID]
      },

      updater: (store) => {
        // Remove from drafts
        const draftConnection = store.get(draftConnectionID);
        if (draftConnection) {
          ConnectionHandler.deleteNode(draftConnection, post.id);
        }

        // Update post status
        const postRecord = store.get(post.id);
        if (postRecord) {
          postRecord.setValue('PUBLISHED', 'status');
          postRecord.setValue(new Date().toISOString(), 'publishedAt');
        }
      },

      optimisticUpdater: (store) => {
        const draftConnection = store.get(draftConnectionID);
        if (draftConnection) {
          ConnectionHandler.deleteNode(draftConnection, post.id);
        }

        const postRecord = store.get(post.id);
        if (postRecord) {
          postRecord.setValue('PUBLISHED', 'status');
          postRecord.setValue(new Date().toISOString(), 'publishedAt');
        }
      }
    });
  };

  return (
    <button onClick={handlePublish}>
      Publish
    </button>
  );
}
```

### 7. Error Handling

```javascript
// CreatePostWithValidation.jsx
function CreatePostWithValidation() {
  const [commit, isInFlight] = useMutation(CreatePostMutation);
  const [errors, setErrors] = useState(null);

  const handleSubmit = (title, body) => {
    setErrors(null);

    commit({
      variables: {
        input: { title, body }
      },

      onCompleted: (response, errors) => {
        if (errors) {
          // GraphQL errors
          setErrors(errors.map(e => e.message));
        } else if (response.createPost.errors) {
          // Application errors
          setErrors(response.createPost.errors);
        } else {
          // Success
          console.log('Post created successfully');
        }
      },

      onError: (error) => {
        // Network or runtime errors
        setErrors(['Network error. Please try again.']);
        console.error('Mutation error:', error);
      }
    });
  };

  return (
    <div>
      {errors && (
        <div className="error-list">
          {errors.map((error, i) => (
            <div key={i} className="error">{error}</div>
          ))}
        </div>
      )}

      <form onSubmit={(e) => {
        e.preventDefault();
        handleSubmit(
          e.target.title.value,
          e.target.body.value
        );
      }}>
        <input name="title" required disabled={isInFlight} />
        <textarea name="body" required disabled={isInFlight} />
        <button type="submit" disabled={isInFlight}>
          Create Post
        </button>
      </form>
    </div>
  );
}
```

### 8. Batched Mutations

```javascript
// BulkActions.jsx
function BulkActions({ selectedPostIds }) {
  const [deletePosts] = useMutation(DeletePostsMutation);
  const [archivePosts] = useMutation(ArchivePostsMutation);

  const handleBulkDelete = () => {
    deletePosts({
      variables: {
        input: { ids: selectedPostIds }
      },

      updater: (store) => {
        const root = store.getRoot();
        const connection = ConnectionHandler.getConnection(
          root,
          'PostsList_posts'
        );

        selectedPostIds.forEach(id => {
          if (connection) {
            ConnectionHandler.deleteNode(connection, id);
          }
          store.delete(id);
        });
      },

      optimisticUpdater: (store) => {
        const root = store.getRoot();
        const connection = ConnectionHandler.getConnection(
          root,
          'PostsList_posts'
        );

        selectedPostIds.forEach(id => {
          if (connection) {
            ConnectionHandler.deleteNode(connection, id);
          }
        });
      }
    });
  };

  const handleBulkArchive = () => {
    archivePosts({
      variables: {
        input: { ids: selectedPostIds }
      },

      updater: (store) => {
        selectedPostIds.forEach(id => {
          const postRecord = store.get(id);
          if (postRecord) {
            postRecord.setValue('ARCHIVED', 'status');
          }
        });
      }
    });
  };

  return (
    <div>
      <button onClick={handleBulkDelete}>Delete Selected</button>
      <button onClick={handleBulkArchive}>Archive Selected</button>
    </div>
  );
}
```

### 9. Declarative Mutation Configuration

```javascript
// mutations/configs.js
import { ConnectionHandler } from 'relay-runtime';

export const createPostConfig = {
  mutation: CreatePostMutation,

  getVariables(input) {
    return { input };
  },

  getOptimisticResponse(input) {
    return {
      createPost: {
        postEdge: {
          node: {
            id: `temp-${Date.now()}`,
            title: input.title,
            body: input.body,
            createdAt: new Date().toISOString(),
            author: {
              id: currentUser.id,
              name: currentUser.name
            }
          }
        }
      }
    };
  },

  getConfigs() {
    return [{
      type: 'RANGE_ADD',
      parentID: 'client:root',
      connectionInfo: [{
        key: 'PostsList_posts',
        rangeBehavior: 'prepend'
      }],
      edgeName: 'postEdge'
    }];
  },

  onSuccess(response) {
    console.log('Post created:', response.createPost.postEdge.node);
  },

  onFailure(errors) {
    console.error('Failed to create post:', errors);
  }
};

// Usage
function CreatePost() {
  const [commit] = useMutation(createPostConfig.mutation);

  const handleSubmit = (input) => {
    commit({
      variables: createPostConfig.getVariables(input),
      optimisticResponse: createPostConfig.getOptimisticResponse(input),
      configs: createPostConfig.getConfigs(),
      onCompleted: (response, errors) => {
        if (errors) {
          createPostConfig.onFailure(errors);
        } else {
          createPostConfig.onSuccess(response);
        }
      }
    });
  };

  return <CreatePostForm onSubmit={handleSubmit} />;
}
```

### 10. Subscription-Like Mutations

```javascript
// RealtimeComments.jsx
import { requestSubscription, graphql } from 'react-relay';

const CommentAddedSubscription = graphql`
  subscription CommentAddedSubscription($postId: ID!) {
    commentAdded(postId: $postId) {
      commentEdge {
        cursor
        node {
          id
          body
          createdAt
          author {
            id
            name
          }
        }
      }
    }
  }
`;

function RealtimeComments({ postId }) {
  useEffect(() => {
    const subscription = requestSubscription(environment, {
      subscription: CommentAddedSubscription,
      variables: { postId },

      updater: (store) => {
        const payload = store.getRootField('commentAdded');
        const edge = payload.getLinkedRecord('commentEdge');
        const node = edge.getLinkedRecord('node');

        // Add to connection
        const post = store.get(postId);
        if (post) {
          const connection = ConnectionHandler.getConnection(
            post,
            'Post_comments'
          );

          if (connection) {
            ConnectionHandler.insertEdgeAfter(connection, edge);
          }
        }
      },

      onNext: (response) => {
        console.log('New comment:', response.commentAdded);
      },

      onError: (error) => {
        console.error('Subscription error:', error);
      }
    });

    return () => subscription.dispose();
  }, [postId]);

  return null; // This component just manages the subscription
}
```

## Best Practices

1. **Use optimistic updates** - Improve perceived performance
2. **Handle errors gracefully** - Provide user feedback on failures
3. **Update connections properly** - Use @appendEdge/@prependEdge directives
4. **Implement proper validation** - Validate before committing mutations
5. **Clean up after deletions** - Remove deleted items from cache
6. **Use declarative configs** - Centralize mutation configuration
7. **Batch related mutations** - Reduce network overhead
8. **Implement retry logic** - Handle transient failures
9. **Track mutation state** - Show loading indicators
10. **Test mutation updaters** - Ensure cache updates work correctly

## Common Pitfalls

1. **Missing updaters** - Not updating cache after mutations
2. **Incorrect optimistic updates** - Optimistic data doesn't match reality
3. **Memory leaks** - Not disposing subscriptions
4. **Race conditions** - Multiple concurrent mutations
5. **Stale connection IDs** - Using wrong connection identifiers
6. **Missing error handling** - Not handling mutation failures
7. **Over-optimistic updates** - Optimistic updates for unsafe operations
8. **Cache inconsistencies** - Manual updates causing data mismatches
9. **Missing rollbacks** - Not reverting failed optimistic updates
10. **Poor UX during mutations** - No loading or error feedback

## When to Use

- Creating, updating, or deleting data
- Implementing user interactions
- Building real-time collaborative features
- Developing form submissions
- Creating like/favorite functionality
- Implementing comment systems
- Building shopping carts
- Developing social features
- Creating admin interfaces
- Implementing bulk operations

## Resources

- [Relay Mutations Guide](https://relay.dev/docs/guided-tour/updating-data/graphql-mutations/)
- [Relay Updater Functions](https://relay.dev/docs/guided-tour/updating-data/imperatively-modifying-store-data/)
- [Optimistic Updates](https://relay.dev/docs/guided-tour/updating-data/client-only-data/)
- [Connection Handler](https://relay.dev/docs/api-reference/store/#connectionhandler)
- [Relay Examples](https://github.com/relayjs/relay-examples)
