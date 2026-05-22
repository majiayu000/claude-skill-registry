---
name: Go gRPC
description: High-performance RPC framework with Protocol Buffers.
metadata:
  labels: [golang, grpc, protobuf, rpc]
  triggers:
    files: ['**/*.proto', '**/*_grpc.pb.go']
    keywords: [grpc, proto, RegisterServer, NewClient]
---

# Go gRPC Standards

## Proto Definition

```protobuf
// proto/user.proto
syntax = "proto3";
package user;
option go_package = "myapp/gen/user";

service UserService {
    rpc GetUser (GetUserRequest) returns (User);
    rpc ListUsers (ListUsersRequest) returns (stream User);
    rpc CreateUsers (stream CreateUserRequest) returns (CreateUsersResponse);
    rpc Chat (stream Message) returns (stream Message);
}

message User {
    int64 id = 1;
    string name = 2;
    string email = 3;
}

message GetUserRequest {
    int64 id = 1;
}

message ListUsersRequest {
    int32 page_size = 1;
    string page_token = 2;
}
```

## Code Generation

```bash
# Install
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate
protoc --go_out=. --go-grpc_out=. proto/user.proto
```

## Server Implementation

```go
type userServer struct {
    pb.UnimplementedUserServiceServer
    db *sql.DB
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user, err := s.db.FindUser(ctx, req.Id)
    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user not found: %v", err)
    }
    return &pb.User{
        Id:    user.ID,
        Name:  user.Name,
        Email: user.Email,
    }, nil
}

func main() {
    lis, _ := net.Listen("tcp", ":50051")
    s := grpc.NewServer()
    pb.RegisterUserServiceServer(s, &userServer{db: db})
    s.Serve(lis)
}
```

## Client

```go
func main() {
    conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    client := pb.NewUserServiceClient(conn)

    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()

    user, err := client.GetUser(ctx, &pb.GetUserRequest{Id: 1})
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("User: %v\n", user)
}
```

## Streaming

```go
// Server streaming
func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    users, _ := s.db.ListUsers(req.PageSize)
    for _, user := range users {
        if err := stream.Send(user); err != nil {
            return err
        }
    }
    return nil
}

// Client streaming
func (s *userServer) CreateUsers(stream pb.UserService_CreateUsersServer) error {
    var count int32
    for {
        req, err := stream.Recv()
        if err == io.EOF {
            return stream.SendAndClose(&pb.CreateUsersResponse{Count: count})
        }
        if err != nil {
            return err
        }
        s.db.CreateUser(req)
        count++
    }
}

// Bidirectional streaming
func (s *userServer) Chat(stream pb.UserService_ChatServer) error {
    for {
        msg, err := stream.Recv()
        if err == io.EOF {
            return nil
        }
        if err != nil {
            return err
        }
        reply := &pb.Message{Text: "Echo: " + msg.Text}
        if err := stream.Send(reply); err != nil {
            return err
        }
    }
}
```

## Interceptors

```go
// Unary interceptor
func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    log.Printf("Method: %s, Duration: %s, Error: %v", info.FullMethod, time.Since(start), err)
    return resp, err
}

// Auth interceptor
func authInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.Unauthenticated, "no metadata")
    }
    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "no token")
    }
    // Validate token...
    return handler(ctx, req)
}

// Apply interceptors
s := grpc.NewServer(
    grpc.ChainUnaryInterceptor(loggingInterceptor, authInterceptor),
    grpc.ChainStreamInterceptor(streamLoggingInterceptor),
)
```

## Error Handling

```go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    if req.Id <= 0 {
        return nil, status.Error(codes.InvalidArgument, "invalid user id")
    }

    user, err := s.db.FindUser(ctx, req.Id)
    if err == sql.ErrNoRows {
        return nil, status.Error(codes.NotFound, "user not found")
    }
    if err != nil {
        return nil, status.Error(codes.Internal, "database error")
    }

    return user, nil
}

// Client error handling
user, err := client.GetUser(ctx, req)
if err != nil {
    st, ok := status.FromError(err)
    if ok {
        switch st.Code() {
        case codes.NotFound:
            // Handle not found
        case codes.InvalidArgument:
            // Handle invalid input
        }
    }
}
```

## Best Practices

1. **Proto first**: Design API in proto files
2. **Deadlines**: Always set context timeouts
3. **Errors**: Use gRPC status codes correctly
4. **Streaming**: For large data or real-time
5. **Interceptors**: Logging, auth, metrics
