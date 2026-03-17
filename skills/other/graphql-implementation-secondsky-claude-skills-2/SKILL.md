---
name: graphql-implementation
description: Builds GraphQL APIs with schema design, resolvers, error handling, and performance optimization using Apollo or Graphene. Use when creating flexible query APIs, migrating from REST, or implementing real-time subscriptions.
---

# GraphQL Implementation

Build GraphQL APIs with proper schema design, resolvers, and performance optimization.

## Schema Definition

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(limit: Int = 10): [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  createPost(input: CreatePostInput!): Post!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

## Apollo Server Setup

```javascript
const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');

const resolvers = {
  Query: {
    user: (_, { id }, { dataSources }) =>
      dataSources.userAPI.getUser(id),
    users: (_, { limit, offset }, { dataSources }) =>
      dataSources.userAPI.getUsers({ limit, offset })
  },
  User: {
    posts: (user, { limit }, { dataSources }) =>
      dataSources.postAPI.getPostsByUser(user.id, limit)
  },
  Mutation: {
    createUser: (_, { input }, { dataSources }) =>
      dataSources.userAPI.createUser(input)
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
```

## DataLoader for N+1 Prevention

```javascript
const DataLoader = require('dataloader');

const userLoader = new DataLoader(async (ids) => {
  const users = await User.find({ _id: { $in: ids } });
  return ids.map(id => users.find(u => u.id === id));
});
```

## Error Handling

```javascript
const { GraphQLError } = require('graphql');

throw new GraphQLError('User not found', {
  extensions: { code: 'NOT_FOUND', argumentName: 'id' }
});
```

## Best Practices

- Use DataLoader to batch queries
- Implement query complexity limits
- Design schema around client needs
- Validate all inputs
- Use descriptive naming conventions

## Python Graphene

See [references/python-graphene.md](references/python-graphene.md) for complete Flask implementation with:
- ObjectType definitions
- Query and Mutation classes
- Input types
- Flask integration

## Best Practices

**Do:**
- Use DataLoader to batch queries
- Implement query complexity limits
- Design schema around client needs
- Validate all inputs
- Use descriptive naming conventions
- Add subscriptions for real-time data

**Don't:**
- Allow deeply nested queries without limits
- Expose database internals
- Ignore N+1 query problems
- Return unauthorized data
- Skip input validation
