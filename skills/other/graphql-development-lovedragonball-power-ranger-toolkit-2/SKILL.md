---
name: graphql-development
description: GraphQL schema design, resolvers, and client integration. Use for building GraphQL APIs and front-end queries.
---

# 🔗 GraphQL Development Skill

## Schema Design

### Types
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  published: Boolean!
}

input CreatePostInput {
  title: String!
  content: String!
}
```

### Queries & Mutations
```graphql
type Query {
  users: [User!]!
  user(id: ID!): User
  posts(published: Boolean): [Post!]!
}

type Mutation {
  createUser(name: String!, email: String!): User!
  createPost(input: CreatePostInput!): Post!
  deletePost(id: ID!): Boolean!
}

type Subscription {
  postCreated: Post!
}
```

---

## Server Setup (Apollo)

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type Query {
    hello: String
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello, world!'
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
```

---

## Resolvers Pattern

```typescript
const resolvers = {
  Query: {
    users: async (_, __, { dataSources }) => {
      return dataSources.userAPI.getUsers();
    },
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUser(id);
    }
  },
  User: {
    posts: async (parent, _, { dataSources }) => {
      return dataSources.postAPI.getPostsByUser(parent.id);
    }
  },
  Mutation: {
    createUser: async (_, { name, email }, { dataSources }) => {
      return dataSources.userAPI.createUser({ name, email });
    }
  }
};
```

---

## Client Queries

```typescript
import { gql, useQuery, useMutation } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function Users() {
  const { loading, error, data } = useQuery(GET_USERS);
  
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  
  return data.users.map(user => <div key={user.id}>{user.name}</div>);
}
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| Pagination | Use cursor-based pagination |
| N+1 Problem | Use DataLoader for batching |
| Error Handling | Return errors in extensions |
| Versioning | Avoid, use evolution |
| Caching | Use Apollo Client cache |

---

## Checklist

- [ ] Design schema (types, queries, mutations)
- [ ] Implement resolvers
- [ ] Add data validation
- [ ] Handle N+1 with DataLoader
- [ ] Set up client Apollo/urql
- [ ] Add error handling
