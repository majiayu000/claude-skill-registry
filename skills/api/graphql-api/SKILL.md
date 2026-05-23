---
name: graphql-api
description: |
  Build GraphQL APIs with schema design, resolvers, and subscriptions.
  Use when: creating GraphQL server, API with complex queries.
  Triggers: "graphql", "gql", "apollo", "async-graphql", "strawberry".
---

# GraphQL API Development

## Project Protection Setup

**MANDATORY before writing any code:**

```bash
# 1. Create .gitignore
cat >> .gitignore << 'EOF'
# Build
target/
node_modules/
__pycache__/
dist/

# Secrets
.env
.env.*
!.env.example
*.key

# IDE
.idea/
.vscode/
.DS_Store
EOF

# 2. Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

---

## Stack Options

| Language | Framework | Best For |
|----------|-----------|----------|
| **Rust** | async-graphql + axum | Performance, type safety |
| **Python** | strawberry / ariadne | Rapid development |
| **Node** | Apollo Server / Mercurius | JS ecosystem |

---

## Quick Start

### Rust (async-graphql + axum)

```toml
# Cargo.toml
[dependencies]
async-graphql = "7"
async-graphql-axum = "7"
axum = "0.7"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

```rust
use async_graphql::{Object, Schema, EmptyMutation, EmptySubscription};
use async_graphql_axum::GraphQL;
use axum::{Router, routing::get};

struct Query;

#[Object]
impl Query {
    async fn hello(&self, name: Option<String>) -> String {
        format!("Hello, {}!", name.unwrap_or("World".to_string()))
    }
}

type AppSchema = Schema<Query, EmptyMutation, EmptySubscription>;

#[tokio::main]
async fn main() {
    let schema = Schema::build(Query, EmptyMutation, EmptySubscription).finish();

    let app = Router::new()
        .route("/", get(graphiql).post_service(GraphQL::new(schema)));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn graphiql() -> impl axum::response::IntoResponse {
    axum::response::Html(async_graphql::http::GraphiQLSource::build().endpoint("/").finish())
}
```

### Python (strawberry)

```python
# requirements.txt
strawberry-graphql[fastapi]
uvicorn
```

```python
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "World") -> str:
        return f"Hello, {name}!"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

### Node (Apollo Server)

```typescript
// package.json: "@apollo/server": "^4", "graphql": "^16"
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type Query {
    hello(name: String): String!
  }
`;

const resolvers = {
  Query: {
    hello: (_: unknown, { name }: { name?: string }) =>
      `Hello, ${name ?? 'World'}!`,
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Server ready at ${url}`);
```

---

## Schema Design

### Types & Fields

```rust
use async_graphql::{Object, SimpleObject, InputObject, ID};

#[derive(SimpleObject)]
struct User {
    id: ID,
    name: String,
    email: String,
    posts: Vec<Post>,
}

#[derive(SimpleObject)]
struct Post {
    id: ID,
    title: String,
    content: String,
    author_id: ID,
}

#[derive(InputObject)]
struct CreateUserInput {
    name: String,
    email: String,
}
```

### Python

```python
import strawberry
from typing import List

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    posts: List["Post"]

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str

@strawberry.input
class CreateUserInput:
    name: str
    email: str
```

---

## Queries & Mutations

### Rust

```rust
struct Query;

#[Object]
impl Query {
    async fn user(&self, ctx: &Context<'_>, id: ID) -> Result<Option<User>> {
        let db = ctx.data::<Database>()?;
        db.get_user(id.parse()?).await
    }

    async fn users(&self, ctx: &Context<'_>, limit: Option<i32>) -> Result<Vec<User>> {
        let db = ctx.data::<Database>()?;
        db.list_users(limit.unwrap_or(10)).await
    }
}

struct Mutation;

#[Object]
impl Mutation {
    async fn create_user(&self, ctx: &Context<'_>, input: CreateUserInput) -> Result<User> {
        let db = ctx.data::<Database>()?;
        db.create_user(input).await
    }

    async fn delete_user(&self, ctx: &Context<'_>, id: ID) -> Result<bool> {
        let db = ctx.data::<Database>()?;
        db.delete_user(id.parse()?).await
    }
}
```

### Python

```python
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, id: strawberry.ID) -> User | None:
        db = info.context["db"]
        return await db.get_user(id)

    @strawberry.field
    async def users(self, info: Info, limit: int = 10) -> list[User]:
        db = info.context["db"]
        return await db.list_users(limit)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info: Info, input: CreateUserInput) -> User:
        db = info.context["db"]
        return await db.create_user(input)
```

---

## DataLoader (N+1 Problem)

### Rust

```rust
use async_graphql::dataloader::{DataLoader, Loader};

struct UserLoader(Database);

impl Loader<i32> for UserLoader {
    type Value = User;
    type Error = Error;

    async fn load(&self, keys: &[i32]) -> Result<HashMap<i32, User>> {
        self.0.get_users_by_ids(keys).await
    }
}

// In schema setup
let schema = Schema::build(Query, Mutation, EmptySubscription)
    .data(DataLoader::new(UserLoader(db.clone()), tokio::spawn))
    .finish();

// In resolver
#[Object]
impl Post {
    async fn author(&self, ctx: &Context<'_>) -> Result<User> {
        let loader = ctx.data::<DataLoader<UserLoader>>()?;
        loader.load_one(self.author_id).await?.ok_or("Not found".into())
    }
}
```

### Python

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    users = await db.get_users_by_ids(keys)
    return [users.get(key) for key in keys]

user_loader = DataLoader(load_fn=load_users)

@strawberry.type
class Post:
    author_id: int

    @strawberry.field
    async def author(self, info: Info) -> User:
        loader = info.context["user_loader"]
        return await loader.load(self.author_id)
```

---

## Subscriptions (Real-time)

### Rust

```rust
use async_graphql::{Subscription, futures_util::Stream};
use tokio_stream::StreamExt;

struct Subscription;

#[Subscription]
impl Subscription {
    async fn messages(&self, ctx: &Context<'_>) -> impl Stream<Item = Message> {
        let mut rx = ctx.data::<broadcast::Sender<Message>>()?.subscribe();

        async_stream::stream! {
            while let Ok(msg) = rx.recv().await {
                yield msg;
            }
        }
    }
}
```

### WebSocket Setup

```rust
use async_graphql_axum::GraphQLSubscription;

let app = Router::new()
    .route("/", get(graphiql).post_service(GraphQL::new(schema.clone())))
    .route_service("/ws", GraphQLSubscription::new(schema));
```

---

## Authentication & Context

### Rust

```rust
use axum::{extract::State, http::HeaderMap};

async fn graphql_handler(
    State(schema): State<AppSchema>,
    headers: HeaderMap,
    req: GraphQLRequest,
) -> GraphQLResponse {
    let token = headers
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.replace("Bearer ", ""));

    let user = if let Some(token) = token {
        verify_token(&token).ok()
    } else {
        None
    };

    schema.execute(req.into_inner().data(user)).await.into()
}

// In resolver
#[Object]
impl Mutation {
    #[graphql(guard = "AuthGuard")]
    async fn create_post(&self, ctx: &Context<'_>, input: CreatePostInput) -> Result<Post> {
        let user = ctx.data::<Option<User>>()?
            .as_ref()
            .ok_or("Unauthorized")?;
        // ...
    }
}
```

---

## Error Handling

### Rust

```rust
use async_graphql::{Error, ErrorExtensions};

#[derive(Debug, thiserror::Error)]
enum ApiError {
    #[error("Not found")]
    NotFound,
    #[error("Unauthorized")]
    Unauthorized,
    #[error("Validation failed: {0}")]
    Validation(String),
}

impl ErrorExtensions for ApiError {
    fn extend(&self) -> Error {
        Error::new(self.to_string()).extend_with(|_, e| {
            match self {
                ApiError::NotFound => e.set("code", "NOT_FOUND"),
                ApiError::Unauthorized => e.set("code", "UNAUTHORIZED"),
                ApiError::Validation(_) => e.set("code", "VALIDATION_ERROR"),
            }
        })
    }
}
```

---

## Testing

### Rust

```rust
#[tokio::test]
async fn test_hello_query() {
    let schema = Schema::build(Query, EmptyMutation, EmptySubscription).finish();

    let result = schema.execute("{ hello(name: \"Test\") }").await;

    assert_eq!(
        result.data,
        async_graphql::Value::from_json(serde_json::json!({
            "hello": "Hello, Test!"
        })).unwrap()
    );
}
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| N+1 queries | Use DataLoader |
| Over-fetching | Design granular types |
| No rate limiting | Implement query complexity |
| Deep nesting | Set max depth limit |
| No caching | Use persisted queries |

---

## Query Complexity Limits

```rust
let schema = Schema::build(Query, Mutation, Subscription)
    .limit_complexity(100)  // Max query complexity
    .limit_depth(10)        // Max nesting depth
    .finish();
```

---

## Testing

### Rust (async-graphql)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_hello_query() {
        let schema = Schema::build(Query, EmptyMutation, EmptySubscription).finish();

        let result = schema
            .execute(r#"{ hello(name: "Test") }"#)
            .await;

        assert!(result.errors.is_empty());
        assert_eq!(
            result.data,
            async_graphql::Value::from_json(serde_json::json!({
                "hello": "Hello, Test!"
            })).unwrap()
        );
    }

    #[tokio::test]
    async fn test_create_user_mutation() {
        let schema = create_test_schema().await;

        let result = schema.execute(r#"
            mutation {
                createUser(input: { name: "Test", email: "test@example.com" }) {
                    id
                    name
                }
            }
        "#).await;

        assert!(result.errors.is_empty());
    }

    #[tokio::test]
    async fn test_unauthorized_mutation_fails() {
        let schema = create_schema_without_auth().await;

        let result = schema.execute(r#"
            mutation { deleteUser(id: "1") }
        "#).await;

        assert!(!result.errors.is_empty());
        assert!(result.errors[0].message.contains("Unauthorized"));
    }
}
```

### Python (strawberry)

```python
import pytest
from strawberry.test import GraphQLTestClient

@pytest.fixture
def client(app):
    return GraphQLTestClient(app)

def test_hello_query(client):
    response = client.query('{ hello(name: "Test") }')
    assert response.data == {"hello": "Hello, Test!"}

def test_create_user(client):
    response = client.query('''
        mutation {
            createUser(input: { name: "Test", email: "test@example.com" }) {
                id
                name
            }
        }
    ''')
    assert response.errors is None
    assert response.data["createUser"]["name"] == "Test"
```

### Node (Apollo)

```typescript
import { ApolloServer } from '@apollo/server';
import { describe, it, expect } from 'vitest';

describe('GraphQL API', () => {
  it('hello query', async () => {
    const server = new ApolloServer({ typeDefs, resolvers });
    const response = await server.executeOperation({
      query: '{ hello(name: "Test") }',
    });

    expect(response.body.singleResult.data).toEqual({ hello: 'Hello, Test!' });
  });
});
```

---

## TDD Workflow

```
1. Task[tdd-test-writer]: "Create users query"
   → Writes test with expected response
   → cargo test → FAILS (RED)

2. Task[rust-developer]: "Implement users resolver"
   → Implements with DataLoader
   → cargo test → PASSES (GREEN)

3. Repeat for each query/mutation

4. Task[code-reviewer]: "Review GraphQL implementation"
   → Checks N+1, auth, complexity limits
```

---

## Security Checklist

- [ ] Query complexity limits set
- [ ] Query depth limits set
- [ ] Authentication on mutations
- [ ] Authorization per field (if needed)
- [ ] No sensitive data in error messages
- [ ] Rate limiting enabled
- [ ] Introspection disabled in production
- [ ] Input validation on all arguments

---

## Project Structure

```
graphql-api/
├── src/
│   ├── main.rs
│   ├── schema/
│   │   ├── mod.rs
│   │   ├── query.rs
│   │   ├── mutation.rs
│   │   └── subscription.rs
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── loaders/       # DataLoaders
│   └── auth.rs
├── tests/
│   └── schema_tests.rs
├── Cargo.toml
├── .env.example
└── schema.graphql     # SDL (optional)
```
