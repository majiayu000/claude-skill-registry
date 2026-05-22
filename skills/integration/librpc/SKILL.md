---
name: librpc
description: >
  librpc - gRPC framework for microservices. RpcServer and RpcClient provide
  base classes. loadProto loads protobuf definitions. createClientFactory builds
  typed service clients. hmacAuth provides authentication support. createTracer
  enables distributed tracing. Use for inter-service communication, building
  gRPC services, and service client creation.
---

# librpc Skill

## When to Use

- Building gRPC service implementations
- Creating clients for inter-service calls
- Adding authentication to gRPC endpoints
- Implementing distributed tracing across services

## Key Concepts

**RpcServer**: Base server class for gRPC services with middleware support.

**RpcClient**: Base client class with connection management and error handling.

**createClientFactory**: Factory that creates typed service clients with
optional logging and tracing.

## Usage Patterns

### Pattern 1: Create service server

```javascript
import { RpcServer, createService } from "@copilot-ld/librpc";

const service = createService(MyServiceImpl, proto);
const server = new RpcServer([service], config);
await server.start();
```

### Pattern 2: Create service client

```javascript
import { createClientFactory } from "@copilot-ld/librpc";

const factory = createClientFactory(logger, tracer);
const agentClient = factory.createAgentClient("localhost", 50051);
const response = await agentClient.request(message);
```

## Integration

Used by all services for gRPC communication. Works with libtype for message
types.
