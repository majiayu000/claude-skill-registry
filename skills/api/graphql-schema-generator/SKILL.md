---
name: graphql-schema-generator
description: Generate GraphQL schemas, resolvers, and type definitions. Use when designing GraphQL APIs or documenting GraphQL schemas.
---

# GraphQL Schema Generator Skill

GraphQLスキーマを生成するスキルです。

## 概要

データモデルからGraphQLスキーマ、リゾルバーを自動生成します。

## 主な機能

- **スキーマ定義**: Type、Query、Mutation
- **リゾルバー生成**: 実装テンプレート
- **ベストプラクティス**: ページネーション、エラーハンドリング
- **ドキュメント**: 自動生成

## 生成例

### Schema

```graphql
# Types
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
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(first: Int = 10, after: String): UserConnection!
  post(id: ID!): Post
  posts(published: Boolean): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post!
}

# Inputs
input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

input UpdateUserInput {
  name: String
  email: String
}

input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
}

# Pagination
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Custom Scalars
scalar DateTime
```

### Resolvers (JavaScript)

```javascript
const resolvers = {
  Query: {
    user: async (parent, { id }, { dataSources }) => {
      return dataSources.userAPI.getUserById(id);
    },
    users: async (parent, { first, after }, { dataSources }) => {
      return dataSources.userAPI.getUsers({ first, after });
    },
    post: async (parent, { id }, { dataSources }) => {
      return dataSources.postAPI.getPostById(id);
    },
    posts: async (parent, { published }, { dataSources }) => {
      return dataSources.postAPI.getPosts({ published });
    }
  },

  Mutation: {
    createUser: async (parent, { input }, { dataSources }) => {
      return dataSources.userAPI.createUser(input);
    },
    updateUser: async (parent, { id, input }, { dataSources }) => {
      return dataSources.userAPI.updateUser(id, input);
    },
    deleteUser: async (parent, { id }, { dataSources }) => {
      return dataSources.userAPI.deleteUser(id);
    },
    createPost: async (parent, { input }, { dataSources, user }) => {
      if (!user) throw new Error('Unauthorized');
      return dataSources.postAPI.createPost(input);
    },
    publishPost: async (parent, { id }, { dataSources, user }) => {
      if (!user) throw new Error('Unauthorized');
      return dataSources.postAPI.publishPost(id);
    }
  },

  User: {
    posts: async (parent, args, { dataSources }) => {
      return dataSources.postAPI.getPostsByAuthor(parent.id);
    }
  },

  Post: {
    author: async (parent, args, { dataSources }) => {
      return dataSources.userAPI.getUserById(parent.authorId);
    }
  }
};
```

## バージョン情報

- スキルバージョン: 1.0.0
