---
name: grpc-expert
version: 1.0.0
description: Expert-level gRPC, Protocol Buffers, microservices communication, and streaming
category: api
tags: [grpc, protobuf, microservices, rpc, streaming]
allowed-tools:
  - Read
  - Write
  - Edit
---

# gRPC Expert

Expert guidance for gRPC services, Protocol Buffers, microservices communication, and streaming patterns.

## Core Concepts

### gRPC Fundamentals
- Protocol Buffers (protobuf)
- Service definitions
- RPC patterns (unary, server streaming, client streaming, bidirectional)
- HTTP/2 transport
- Code generation
- Interceptors and middleware

### Communication Patterns
- Unary RPC (request-response)
- Server streaming RPC
- Client streaming RPC
- Bidirectional streaming RPC
- Deadline/timeout handling
- Error handling and status codes

### Production Features
- Load balancing
- Service discovery
- Health checking
- Authentication (TLS, tokens)
- Monitoring and tracing
- Retry policies

## Protocol Buffer Definition

```protobuf
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";

service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);

  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  google.protobuf.Timestamp created_at = 4;
  UserRole role = 5;
}

enum UserRole {
  USER_ROLE_UNSPECIFIED = 0;
  USER_ROLE_USER = 1;
  USER_ROLE_ADMIN = 2;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message CreateUsersResponse {
  repeated string user_ids = 1;
  int32 created_count = 2;
}

message ChatMessage {
  string user_id = 1;
  string message = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

## Python gRPC Server

```python
import grpc
from concurrent import futures
import logging
from typing import Iterator

import user_pb2
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}

    def GetUser(self, request, context):
        """Unary RPC"""
        user_id = request.id

        if user_id not in self.users:
            context.abort(grpc.StatusCode.NOT_FOUND, f"User {user_id} not found")

        user = self.users[user_id]
        return user_pb2.GetUserResponse(user=user)

    def ListUsers(self, request, context):
        """Server streaming RPC"""
        page_size = request.page_size or 10

        for i, user in enumerate(self.users.values()):
            if i >= page_size:
                break
            yield user

    def CreateUsers(self, request_iterator, context):
        """Client streaming RPC"""
        created_ids = []

        for request in request_iterator:
            user_id = self._generate_id()
            user = user_pb2.User(
                id=user_id,
                email=request.email,
                name=request.name
            )
            self.users[user_id] = user
            created_ids.append(user_id)

        return user_pb2.CreateUsersResponse(
            user_ids=created_ids,
            created_count=len(created_ids)
        )

    def Chat(self, request_iterator, context):
        """Bidirectional streaming RPC"""
        for message in request_iterator:
            # Echo back with modification
            response = user_pb2.ChatMessage(
                user_id="server",
                message=f"Echo: {message.message}",
                timestamp=message.timestamp
            )
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
```

## Go gRPC Server

```go
package main

import (
    "context"
    "io"
    "log"
    "net"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
    pb "example.com/user/v1"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    users map[string]*pb.User
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    user, exists := s.users[req.Id]
    if !exists {
        return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
    }

    return &pb.GetUserResponse{User: user}, nil
}

func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    pageSize := req.PageSize
    if pageSize == 0 {
        pageSize = 10
    }

    count := 0
    for _, user := range s.users {
        if count >= int(pageSize) {
            break
        }

        if err := stream.Send(user); err != nil {
            return err
        }
        count++
    }

    return nil
}

func (s *userServer) CreateUsers(stream pb.UserService_CreateUsersServer) error {
    var userIds []string

    for {
        req, err := stream.Recv()
        if err == io.EOF {
            return stream.SendAndClose(&pb.CreateUsersResponse{
                UserIds:      userIds,
                CreatedCount: int32(len(userIds)),
            })
        }
        if err != nil {
            return err
        }

        userId := generateID()
        user := &pb.User{
            Id:    userId,
            Email: req.Email,
            Name:  req.Name,
        }

        s.users[userId] = user
        userIds = append(userIds, userId)
    }
}

func (s *userServer) Chat(stream pb.UserService_ChatServer) error {
    for {
        msg, err := stream.Recv()
        if err == io.EOF {
            return nil
        }
        if err != nil {
            return err
        }

        response := &pb.ChatMessage{
            UserId:    "server",
            Message:   "Echo: " + msg.Message,
            Timestamp: msg.Timestamp,
        }

        if err := stream.Send(response); err != nil {
            return err
        }
    }
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    s := grpc.NewServer()
    pb.RegisterUserServiceServer(s, &userServer{
        users: make(map[string]*pb.User),
    })

    log.Println("Server listening on :50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## gRPC Client with Interceptors

```python
import grpc
import user_pb2
import user_pb2_grpc
from typing import Callable

def logging_interceptor(
    method: Callable,
    request,
    call_details: grpc.ClientCallDetails
):
    """Unary-unary interceptor for logging"""
    print(f"Calling method: {call_details.method}")
    print(f"Request: {request}")

    response = method(request, call_details)

    print(f"Response: {response}")
    return response

class UserClient:
    def __init__(self, host: str = 'localhost:50051'):
        # Create channel with interceptor
        self.channel = grpc.insecure_channel(host)
        self.channel = grpc.intercept_channel(
            self.channel,
            logging_interceptor
        )
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)

    def get_user(self, user_id: str) -> user_pb2.User:
        """Call unary RPC"""
        request = user_pb2.GetUserRequest(id=user_id)

        try:
            response = self.stub.GetUser(
                request,
                timeout=5.0  # 5 second timeout
            )
            return response.user
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
            raise

    def list_users(self, page_size: int = 10):
        """Call server streaming RPC"""
        request = user_pb2.ListUsersRequest(page_size=page_size)

        try:
            for user in self.stub.ListUsers(request):
                yield user
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

    def create_users_batch(self, users: list):
        """Call client streaming RPC"""
        def request_generator():
            for user in users:
                yield user_pb2.CreateUserRequest(
                    email=user['email'],
                    name=user['name']
                )

        try:
            response = self.stub.CreateUsers(request_generator())
            return response
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

    def close(self):
        self.channel.close()
```

## Best Practices

### Design
- Use semantic versioning for protobuf packages
- Design backward-compatible changes
- Use proper field numbering (never reuse)
- Include metadata in messages
- Use enums with explicit UNSPECIFIED value
- Design for pagination in list operations

### Performance
- Enable HTTP/2 connection pooling
- Use streaming for large data transfers
- Implement proper timeouts
- Use compression for large payloads
- Batch operations when possible
- Monitor and tune thread pool sizes

### Production
- Implement health checks
- Use TLS for secure communication
- Add authentication/authorization
- Implement retry policies with backoff
- Monitor gRPC metrics (latency, errors)
- Use service discovery for dynamic endpoints

## Anti-Patterns

❌ Breaking backward compatibility
❌ No timeout configuration
❌ Ignoring error status codes
❌ Not handling stream cancellation
❌ Over-sized messages
❌ No health checking
❌ Missing authentication

## Resources

- gRPC: https://grpc.io/
- Protocol Buffers: https://protobuf.dev/
- gRPC-Go: https://github.com/grpc/grpc-go
- gRPC-Python: https://grpc.io/docs/languages/python/
