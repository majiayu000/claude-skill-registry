---
name: grpc-patterns
description: Protobuf schema design, streaming patterns, interceptor chains, deadline propagation, and error handling for gRPC services.
---

# gRPC Patterns

High-performance RPC patterns with Protocol Buffers and gRPC.

## Protobuf Schema Design

```protobuf
syntax = "proto3";

package order.v1;

option go_package = "github.com/myapp/gen/order/v1;orderv1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/field_mask.proto";

// Service definition
service OrderService {
  // Unary RPC
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // Server streaming: server sends multiple responses
  rpc WatchOrderStatus(WatchOrderStatusRequest) returns (stream OrderStatusEvent);

  // Client streaming: client sends multiple requests
  rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateOrdersResponse);

  // Bidirectional streaming
  rpc OrderChat(stream ChatMessage) returns (stream ChatMessage);
}

// Request/Response naming: <Method>Request, <Method>Response
message GetOrderRequest {
  string order_id = 1;
  // FieldMask for partial responses (bandwidth optimization)
  google.protobuf.FieldMask field_mask = 2;
}

message GetOrderResponse {
  Order order = 1;
}

// Domain message
message Order {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  repeated OrderItem items = 4;
  Money total = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

// Enums: always have UNSPECIFIED as 0
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

// Reusable value type
message Money {
  string currency_code = 1;  // ISO 4217
  int64 units = 2;           // Whole units (dollars)
  int32 nanos = 3;           // Nano units (cents * 10^7)
}

// Pagination
message ListOrdersRequest {
  int32 page_size = 1;       // Max items per page
  string page_token = 2;     // Opaque cursor from previous response
  string filter = 3;         // e.g., "status=SHIPPED"
  string order_by = 4;       // e.g., "created_at desc"
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;  // Empty = no more pages
  int32 total_size = 3;
}
```

## Server Implementation (Go)

```go
package server

import (
    "context"
    "time"

    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"

    pb "github.com/myapp/gen/order/v1"
)

type OrderServer struct {
    pb.UnimplementedOrderServiceServer
    store OrderStore
}

func (s *OrderServer) GetOrder(ctx context.Context, req *pb.GetOrderRequest) (*pb.GetOrderResponse, error) {
    // Validate input
    if req.OrderId == "" {
        return nil, status.Error(codes.InvalidArgument, "order_id is required")
    }

    // Check deadline propagation
    if deadline, ok := ctx.Deadline(); ok {
        if time.Until(deadline) < 100*time.Millisecond {
            return nil, status.Error(codes.DeadlineExceeded, "insufficient time remaining")
        }
    }

    order, err := s.store.GetByID(ctx, req.OrderId)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, status.Error(codes.NotFound, "order not found")
        }
        return nil, status.Error(codes.Internal, "failed to fetch order")
    }

    return &pb.GetOrderResponse{Order: order}, nil
}

// Server streaming
func (s *OrderServer) WatchOrderStatus(
    req *pb.WatchOrderStatusRequest,
    stream pb.OrderService_WatchOrderStatusServer,
) error {
    ctx := stream.Context()
    ch := s.store.WatchStatus(ctx, req.OrderId)

    for {
        select {
        case <-ctx.Done():
            return status.Error(codes.Cancelled, "client disconnected")
        case event, ok := <-ch:
            if !ok {
                return nil  // Channel closed, stream complete
            }
            if err := stream.Send(event); err != nil {
                return err
            }
        }
    }
}
```

## Interceptor Chain (Middleware)

```go
import (
    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
)

// Unary interceptor: logging + metrics
func loggingInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    start := time.Now()

    resp, err := handler(ctx, req)

    duration := time.Since(start)
    code := status.Code(err)

    log.Info("grpc request",
        "method", info.FullMethod,
        "code", code,
        "duration_ms", duration.Milliseconds(),
    )

    // Prometheus metrics
    grpcRequestDuration.WithLabelValues(info.FullMethod, code.String()).Observe(duration.Seconds())
    grpcRequestTotal.WithLabelValues(info.FullMethod, code.String()).Inc()

    return resp, err
}

// Auth interceptor
func authInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    // Skip auth for health check
    if info.FullMethod == "/grpc.health.v1.Health/Check" {
        return handler(ctx, req)
    }

    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.Unauthenticated, "missing metadata")
    }

    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }

    user, err := validateToken(tokens[0])
    if err != nil {
        return nil, status.Error(codes.Unauthenticated, "invalid token")
    }

    // Attach user to context
    ctx = context.WithValue(ctx, userKey, user)
    return handler(ctx, req)
}

// Chain interceptors
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        recoveryInterceptor,   // Panic recovery (outermost)
        loggingInterceptor,    // Request logging
        authInterceptor,       // Authentication
        rateLimitInterceptor,  // Rate limiting
    ),
)
```

## Client with Deadline and Retry

```go
import (
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    grpcRetry "github.com/grpc-ecosystem/go-grpc-middleware/retry"
)

func newOrderClient(addr string) (pb.OrderServiceClient, error) {
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithChainUnaryInterceptor(
            grpcRetry.UnaryClientInterceptor(
                grpcRetry.WithMax(3),
                grpcRetry.WithBackoff(grpcRetry.BackoffExponential(100*time.Millisecond)),
                grpcRetry.WithCodes(codes.Unavailable, codes.ResourceExhausted),
            ),
        ),
    )
    if err != nil {
        return nil, err
    }

    return pb.NewOrderServiceClient(conn), nil
}

// Always set deadline on client calls
func getOrder(client pb.OrderServiceClient, orderID string) (*pb.Order, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    resp, err := client.GetOrder(ctx, &pb.GetOrderRequest{OrderId: orderID})
    if err != nil {
        return nil, fmt.Errorf("get order %s: %w", orderID, err)
    }
    return resp.Order, nil
}
```

## Checklist

- [ ] Enum field 0 is always UNSPECIFIED (proto3 default value)
- [ ] Request/Response wrapper messages (not bare domain types)
- [ ] FieldMask for partial reads and updates
- [ ] Cursor-based pagination (page_token), not offset
- [ ] Deadline set on every client call (5-30s typical)
- [ ] Propagate deadline to downstream calls (context forwarding)
- [ ] Interceptors: recovery, logging, auth, rate limit (in that order)
- [ ] Health check endpoint (grpc.health.v1.Health)

## Anti-Patterns

- Missing UNSPECIFIED enum value: 0 means "not set" in proto3
- Returning domain errors as codes.Internal (use specific codes)
- No deadline on client calls: request hangs forever on server failure
- Large messages (>4MB default limit): use streaming or chunking
- Breaking proto schema changes: never change field numbers or remove fields
- Catching all errors as codes.Internal: map each error to appropriate gRPC code
