---
name: graphql-api
description: GraphQL API design and implementation patterns. Use when building GraphQL servers, defining schemas, writing resolvers, implementing subscriptions, or consuming GraphQL APIs.
---

# GraphQL API Patterns

## Schema Design (SDL)
```graphql
# schema.graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: Pagination): UserConnection!
  posts(authorId: ID, published: Boolean): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): UserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UserPayload!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  messageAdded(chatId: ID!): Message!
}

type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  body: String!
  published: Boolean!
  author: User!
  tags: [String!]!
}

# Pagination (Relay-style)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type UserEdge { node: User!; cursor: String! }
type PageInfo { hasNextPage: Boolean!; endCursor: String }

# Input types
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UserFilter {
  role: Role
  search: String
}

input Pagination {
  first: Int
  after: String
}

# Error handling — union pattern
union UserPayload = User | UserError
type UserError { message: String!; code: String! }

enum Role { USER ADMIN }
scalar DateTime
```

## Server Setup (Strawberry / Python)
```python
# graphql_app.py
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str

    @strawberry.field
    async def posts(self, info: Info) -> list["Post"]:
        return await info.context["loaders"].posts_by_user.load(self.id)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: Info) -> User | None:
        return await info.context["db"].get_user(id)

    @strawberry.field
    async def users(self) -> list[User]:
        return await info.context["db"].list_users()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, email: str, name: str, info: Info) -> User:
        return await info.context["db"].create_user(email=email, name=name)

schema = strawberry.Schema(query=Query, mutation=Mutation)

# FastAPI integration
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
```

## DataLoader (N+1 Prevention)
```python
from strawberry.dataloader import DataLoader

async def load_posts_by_user(user_ids: list[str]) -> list[list[Post]]:
    """Batch-load posts for many users in one DB query."""
    rows = await db.fetch(
        "SELECT * FROM posts WHERE author_id = ANY($1)", user_ids
    )
    # Group by author_id
    grouped = {}
    for row in rows:
        grouped.setdefault(row["author_id"], []).append(Post(**row))
    return [grouped.get(uid, []) for uid in user_ids]

async def get_context():
    return {
        "db": db,
        "loaders": {
            "posts_by_user": DataLoader(load_fn=load_posts_by_user)
        }
    }
```

## Server Setup (Node.js / Apollo)
```typescript
import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'

const typeDefs = `#graphql
  type Query {
    users: [User!]!
    user(id: ID!): User
  }
  type User {
    id: ID!
    name: String!
    email: String!
  }
`

const resolvers = {
  Query: {
    users: async (_, __, { dataSources }) => dataSources.usersAPI.getUsers(),
    user: async (_, { id }, { dataSources }) => dataSources.usersAPI.getUser(id),
  },
}

const server = new ApolloServer({ typeDefs, resolvers })
const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    token: req.headers.authorization,
    dataSources: { usersAPI: new UsersAPI() },
  }),
})
```

## Client Usage (urql / React)
```typescript
import { useQuery, useMutation } from 'urql'

const GET_USERS = `
  query GetUsers($filter: UserFilter) {
    users(filter: $filter) {
      edges {
        node { id name email }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
`

function UserList() {
  const [result] = useQuery({
    query: GET_USERS,
    variables: { filter: { role: 'USER' } },
  })

  if (result.fetching) return <p>Loading...</p>
  if (result.error) return <p>Error: {result.error.message}</p>

  return result.data.users.edges.map(({ node }) => (
    <div key={node.id}>{node.name}</div>
  ))
}

// Mutation
const CREATE_USER = `
  mutation CreateUser($email: String!, $name: String!) {
    createUser(input: { email: $email, name: $name }) {
      ... on User { id name }
      ... on UserError { message code }
    }
  }
`
const [, createUser] = useMutation(CREATE_USER)
await createUser({ email, name })
```

## Subscriptions (WebSocket)
```typescript
// Server
const typeDefs = `
  type Subscription {
    messageAdded(chatId: ID!): Message!
  }
`

const resolvers = {
  Subscription: {
    messageAdded: {
      subscribe: (_, { chatId }, { pubsub }) =>
        pubsub.asyncIterator(`MESSAGE_ADDED_${chatId}`),
    },
  },
}

// Publish from mutation
await pubsub.publish(`MESSAGE_ADDED_${chatId}`, { messageAdded: newMessage })

// Client
import { createClient } from 'graphql-ws'
const client = createClient({ url: 'ws://localhost:4000/graphql' })

client.subscribe(
  { query: `subscription { messageAdded(chatId: "1") { id text } }` },
  { next: (data) => console.log(data), error: console.error }
)
```

## Authentication & Authorization
```python
# Strawberry permission classes
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        return info.context["user"] is not None

class IsAdmin(BasePermission):
    message = "User is not an admin"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context["user"]
        return user and user.role == "ADMIN"

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: Info) -> User:
        return info.context["user"]

    @strawberry.field(permission_classes=[IsAdmin])
    async def admin_stats(self) -> Stats:
        ...
```

## Rules
- ALWAYS use DataLoaders for relation fields (never query DB in individual resolvers)
- Union types for mutations (UserPayload = User | UserError) — not exceptions
- Relay-style pagination for lists (edges/node/pageInfo + totalCount)
- Never expose internal IDs — use opaque `ID` type
- Depth limiting: reject queries deeper than 5-7 levels (prevent DoS)
- Query complexity analysis: reject queries above budget (e.g., 100 complexity)
- Use persisted queries in production (security + performance)
- Subscriptions over WebSocket; SSE is not standard for GraphQL
