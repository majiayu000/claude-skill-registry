---
name: grpc-python
description: gRPC with Python using grpcio and protobuf for high-performance microservice communication. Use when implementing service-to-service APIs, streaming data, or building polyglot microservices requiring strong typing.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [grpc, protobuf, microservices, rpc, streaming, python, 2026]
author: SkillForge
user-invocable: false
---

# gRPC Python Patterns

High-performance RPC framework for microservice communication.

## Overview

- Internal microservice communication (lower latency than REST)
- Streaming data (real-time updates, file transfers)
- Polyglot environments (shared proto definitions)
- Strong typing between services (compile-time validation)
- Bidirectional streaming (chat, gaming, real-time sync)

## When NOT to Use

- Public APIs (prefer REST/GraphQL for browser compatibility)
- Simple CRUD with few services (REST is simpler)
- When HTTP/2 is not available

## Proto Definition

```protobuf
// protos/user_service.proto
syntax = "proto3";
package user.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);  // Server streaming
  rpc BulkCreateUsers(stream CreateUserRequest) returns (BulkCreateResponse);  // Client streaming
  rpc UserUpdates(stream UserUpdateRequest) returns (stream User);  // Bidirectional
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  UserStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
}

enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
}

message GetUserRequest { string user_id = 1; }
message CreateUserRequest { string email = 1; string name = 2; string password = 3; }
message ListUsersRequest { int32 page_size = 1; string page_token = 2; }
message BulkCreateResponse { int32 created_count = 1; repeated string user_ids = 2; }
```

### Code Generation

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./app/protos --pyi_out=./app/protos --grpc_python_out=./app/protos ./protos/user_service.proto
```

## Server Implementation

```python
import grpc
from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp
from app.protos import user_service_pb2 as pb2
from app.protos import user_service_pb2_grpc as pb2_grpc

class UserServiceServicer(pb2_grpc.UserServiceServicer):
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def GetUser(self, request, context):
        user = self.user_repo.get(request.user_id)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, f"User {request.user_id} not found")
        return self._to_proto(user)

    def CreateUser(self, request, context):
        if not request.email or "@" not in request.email:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid email")
        if self.user_repo.get_by_email(request.email):
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Email already registered")
        user = self.user_repo.create(email=request.email, name=request.name)
        return self._to_proto(user)

    def ListUsers(self, request, context):
        """Server streaming: yield users one by one."""
        for user in self.user_repo.iterate(page_size=request.page_size or 100):
            if not context.is_active():
                return
            yield self._to_proto(user)

    def BulkCreateUsers(self, request_iterator, context):
        """Client streaming: receive multiple requests."""
        created_ids = []
        for request in request_iterator:
            try:
                user = self.user_repo.create(email=request.email, name=request.name)
                created_ids.append(user.id)
            except Exception as e:
                pass  # Log error, continue
        return pb2.BulkCreateResponse(created_count=len(created_ids), user_ids=created_ids)

    def _to_proto(self, user) -> pb2.User:
        created_at = Timestamp()
        created_at.FromDatetime(user.created_at)
        return pb2.User(id=user.id, email=user.email, name=user.name, created_at=created_at)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(user_repo), server)
    from grpc_health.v1 import health, health_pb2_grpc
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
```

## Async Server (grpcio >= 1.50)

```python
import grpc.aio

class AsyncUserServiceServicer(pb2_grpc.UserServiceServicer):
    async def GetUser(self, request, context):
        user = await self.user_repo.get(request.user_id)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return self._to_proto(user)

async def serve_async():
    server = grpc.aio.server()
    pb2_grpc.add_UserServiceServicer_to_server(AsyncUserServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
```

## Client Implementation

```python
class UserServiceClient:
    def __init__(self, host: str = "localhost:50051"):
        self.channel = grpc.insecure_channel(host, options=[
            ("grpc.keepalive_time_ms", 30000),
            ("grpc.keepalive_timeout_ms", 10000),
        ])
        self.stub = pb2_grpc.UserServiceStub(self.channel)

    def get_user(self, user_id: str, timeout: float = 5.0):
        try:
            return self.stub.GetUser(pb2.GetUserRequest(user_id=user_id), timeout=timeout)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise UserNotFoundError(user_id)
            raise

    def list_users(self, page_size: int = 100):
        for user in self.stub.ListUsers(pb2.ListUsersRequest(page_size=page_size)):
            yield user

    def close(self):
        self.channel.close()
```

## Interceptors

```python
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        start = time.time()
        handler = continuation(handler_call_details)
        logger.info(f"{handler_call_details.method} in {time.time() - start:.3f}s")
        return handler

class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.public_methods = {"/user.v1.UserService/CreateUser"}

    def intercept_service(self, continuation, handler_call_details):
        if handler_call_details.method not in self.public_methods:
            metadata = dict(handler_call_details.invocation_metadata)
            token = metadata.get("authorization", "").replace("Bearer ", "")
            if not token or not self.auth_service.verify(token):
                return grpc.unary_unary_rpc_method_handler(
                    lambda req, ctx: ctx.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
                )
        return continuation(handler_call_details)

class RetryInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.retry_codes = {grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED}

    def intercept_unary_unary(self, continuation, client_call_details, request):
        for attempt in range(self.max_retries):
            try:
                return continuation(client_call_details, request)
            except grpc.RpcError as e:
                if e.code() not in self.retry_codes or attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Proto organization | One service per file, shared messages in common.proto |
| Versioning | Package version (user.v1, user.v2), backward compatible |
| Streaming | Server stream for large lists, bidirectional for real-time |
| Error codes | Use standard gRPC codes, add details for validation |
| Auth | Interceptor with metadata, JWT tokens |
| Timeouts | Always set client-side deadlines |
| Health checks | Required for load balancers |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER skip deadline/timeout
stub.GetUser(request)  # Can hang forever! Use timeout=5.0

# NEVER ignore streaming cancellation
def ListUsers(self, request, context):
    for user in all_users:
        if not context.is_active():  # Check if client disconnected
            return
        yield user

# NEVER return None for message fields
# NEVER use proto2 syntax for new services
# ALWAYS close channels to prevent resource leaks
```

## Related Skills

- `api-design-framework` - REST/OpenAPI patterns
- `strawberry-graphql` - GraphQL alternative
- `streaming-api-patterns` - SSE/WebSocket patterns
