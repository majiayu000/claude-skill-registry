---
name: strawberry-graphql
description: Strawberry GraphQL library for Python with FastAPI integration, type-safe resolvers, DataLoader patterns, and subscriptions. Use when building GraphQL APIs with Python, implementing real-time features, or creating federated schemas.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [graphql, strawberry, fastapi, dataloader, subscriptions, federation, python, 2026]
author: SkillForge
user-invocable: false
---

# Strawberry GraphQL Patterns

Type-safe GraphQL in Python with code-first schema definition.

## Overview

- Complex data relationships (nested queries, multiple entities)
- Client-driven data fetching (mobile apps, SPAs)
- Real-time features (subscriptions for live updates)
- Federated microservice architecture

## When NOT to Use

- Simple CRUD APIs (REST is simpler)
- Internal microservice communication (use gRPC)

## Schema Definition

```python
import strawberry
from datetime import datetime
from strawberry import Private

@strawberry.enum
class UserStatus:
    ACTIVE = "active"
    INACTIVE = "inactive"

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    status: UserStatus
    password_hash: Private[str]  # Not exposed in schema

    @strawberry.field
    def display_name(self) -> str:
        return f"{self.name} ({self.email})"

    @strawberry.field
    async def posts(self, info: strawberry.Info, limit: int = 10) -> list["Post"]:
        return await info.context.post_loader.load_by_user(self.id, limit)

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    author_id: strawberry.ID

    @strawberry.field
    async def author(self, info: strawberry.Info) -> User:
        return await info.context.user_loader.load(self.author_id)

@strawberry.input
class CreateUserInput:
    email: str
    name: str
    password: str
```

## Query and Mutation

```python
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: strawberry.Info, id: strawberry.ID) -> User | None:
        return await info.context.user_service.get(id)

    @strawberry.field
    async def me(self, info: strawberry.Info) -> User | None:
        user_id = info.context.current_user_id
        return await info.context.user_service.get(user_id) if user_id else None

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info: strawberry.Info, input: CreateUserInput) -> User:
        return await info.context.user_service.create(
            email=input.email, name=input.name, password=input.password
        )

    @strawberry.mutation
    async def delete_user(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        await info.context.user_service.delete(id)
        return True
```

## DataLoader (N+1 Prevention)

```python
from strawberry.dataloader import DataLoader

class UserLoader(DataLoader[str, User]):
    def __init__(self, user_repo):
        super().__init__(load_fn=self.batch_load)
        self.user_repo = user_repo

    async def batch_load(self, keys: list[str]) -> list[User]:
        users = await self.user_repo.get_many(keys)
        user_map = {u.id: u for u in users}
        return [user_map.get(key) for key in keys]

class GraphQLContext:
    def __init__(self, request, user_service, user_repo, post_repo):
        self.request = request
        self.user_service = user_service
        self.user_loader = UserLoader(user_repo)
        self._current_user_id = None

    @property
    def current_user_id(self) -> str | None:
        if self._current_user_id is None:
            token = self.request.headers.get("authorization", "").replace("Bearer ", "")
            self._current_user_id = decode_token(token) if token else None
        return self._current_user_id
```

## FastAPI Integration

```python
from fastapi import FastAPI, Request, Depends
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

async def get_context(request: Request, user_service=Depends(get_user_service)) -> GraphQLContext:
    return GraphQLContext(request=request, user_service=user_service, ...)

graphql_router = GraphQLRouter(schema, context_getter=get_context, graphiql=True)

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")
```

## Subscriptions

```python
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_updated(self, info: strawberry.Info, user_id: strawberry.ID) -> AsyncGenerator[User, None]:
        async for message in info.context.pubsub.subscribe(f"user:{user_id}:updated"):
            yield User(**message)

    @strawberry.subscription
    async def notifications(self, info: strawberry.Info) -> AsyncGenerator["Notification", None]:
        user_id = info.context.current_user_id
        if not user_id:
            raise PermissionError("Authentication required")
        async for message in info.context.pubsub.subscribe(f"user:{user_id}:notifications"):
            yield Notification(**message)
```

## Authentication and Authorization

```python
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source, info: strawberry.Info, **kwargs) -> bool:
        return info.context.current_user_id is not None

class IsAdmin(BasePermission):
    message = "Admin access required"

    async def has_permission(self, source, info: strawberry.Info, **kwargs) -> bool:
        user_id = info.context.current_user_id
        if not user_id:
            return False
        user = await info.context.user_service.get(user_id)
        return user and user.role == "admin"

# Usage
@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: strawberry.Info) -> User:
        return await info.context.user_service.get(info.context.current_user_id)

    @strawberry.field(permission_classes=[IsAdmin])
    async def all_users(self, info: strawberry.Info) -> list[User]:
        return await info.context.user_service.list_all()
```

## Error Handling with Union Types

```python
@strawberry.type
class CreateUserSuccess:
    user: User

@strawberry.type
class UserError:
    message: str
    code: str
    field: str | None = None

@strawberry.type
class CreateUserError:
    errors: list[UserError]

CreateUserResult = strawberry.union("CreateUserResult", [CreateUserSuccess, CreateUserError])

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info: strawberry.Info, input: CreateUserInput) -> CreateUserResult:
        errors = []
        if not is_valid_email(input.email):
            errors.append(UserError(message="Invalid email", code="INVALID_EMAIL", field="email"))
        if errors:
            return CreateUserError(errors=errors)

        try:
            user = await info.context.user_service.create(**input.__dict__)
            return CreateUserSuccess(user=user)
        except DuplicateEmailError:
            return CreateUserError(errors=[UserError(message="Email exists", code="DUPLICATE_EMAIL", field="email")])
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Schema approach | Code-first with Strawberry types |
| N+1 prevention | DataLoader for all nested resolvers |
| Pagination | Relay-style cursor pagination |
| Auth | Permission classes, context-based |
| Errors | Union types for mutations |
| Subscriptions | Redis PubSub for horizontal scaling |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER make database calls in resolver loops (N+1 queries!)
for post_id in self.post_ids:
    posts.append(await db.get_post(post_id))

# CORRECT: Use DataLoader
return await info.context.post_loader.load_many(self.post_ids)

# NEVER expose internal IDs without encoding
id: int  # Exposes auto-increment ID!

# CORRECT: Use opaque IDs
id: strawberry.ID  # base64 encoded

# NEVER skip input validation in mutations
```

## Related Skills

- `api-design-framework` - REST API patterns
- `grpc-python` - gRPC alternative
- `streaming-api-patterns` - WebSocket patterns
