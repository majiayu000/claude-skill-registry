---
name: gRPC Integration
description: Comprehensive guide to gRPC for high-performance microservices communication with Protocol Buffers.
---

# gRPC Integration

## Overview

gRPC (Google Remote Procedure Call) is a high-performance, open-source universal RPC framework that uses Protocol Buffers for serialization. It's ideal for microservices communication, providing efficient binary serialization, streaming capabilities, and built-in code generation.

## gRPC Fundamentals and Protocol Buffers

### What is gRPC?

gRPC is a modern RPC framework that:
- Uses HTTP/2 for transport
- Employs Protocol Buffers for efficient serialization
- Supports multiple programming languages
- Provides built-in streaming (unary, server streaming, client streaming, bidirectional)
- Offers code generation from service definitions

### Protocol Buffers

Protocol Buffers (protobuf) is a language-agnostic binary serialization format:

```proto
syntax = "proto3";

package user;

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  repeated string roles = 4;
  google.protobuf.Timestamp created_at = 5;
}
```

**Key features:**
- Binary format (smaller than JSON)
- Strong typing
- Backward/forward compatible
- Efficient serialization/deserialization

## Service Definition (.proto Files)

### Basic Service Definition

```proto
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  
  // Server streaming RPC
  rpc ListUsers(ListUsersRequest) returns (stream User);
  
  // Client streaming RPC
  rpc CreateUserBatch(stream CreateUserRequest) returns (CreateUserBatchResponse);
  
  // Bidirectional streaming RPC
  rpc UserEvents(stream UserEventRequest) returns (stream UserEventResponse);
}

message GetUserRequest {
  string id = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message CreateUserBatchResponse {
  repeated string user_ids = 1;
  int32 created_count = 2;
}

message UserEventRequest {
  string event_type = 1;
  bytes payload = 2;
}

message UserEventResponse {
  bool acknowledged = 1;
  string message = 2;
}
```

### Proto File Organization

```
proto/
├── user/
│   ├── v1/
│   │   ├── user.proto
│   │   └── user_service.proto
│   └── v2/
│       └── user_service.proto
├── common/
│   ├── timestamp.proto
│   └── pagination.proto
└── google/
    └── protobuf/
        ├── timestamp.proto
        └── empty.proto
```

### Importing Common Definitions

```proto
// common/pagination.proto
syntax = "proto3";

package common;

message PageRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message PageResponse {
  string next_page_token = 1;
  int32 total_size = 2;
}

// user_service.proto
syntax = "proto3";

package user.v1;

import "common/pagination.proto";

service UserService {
  rpc ListUsers(common.PageRequest) returns (ListUsersResponse);
}

message ListUsersResponse {
  repeated User users = 1;
  common.PageResponse page_info = 2;
}
```

## Unary, Server Streaming, Client Streaming, Bidirectional Streaming

### Unary RPC

Simplest pattern - client sends request, server sends response:

```javascript
// Client
const client = new UserServiceClient('localhost:50051', credentials.createInsecure());

const request = new GetUserRequest();
request.setId('123');

client.getUser(request, (error, response) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('User:', response.toObject());
});

// Server
function getUser(call, callback) {
  const user = db.getUser(call.request.getId());
  callback(null, user);
}
```

### Server Streaming RPC

Client sends request, server returns stream of responses:

```javascript
// Client
const call = client.listUsers(new ListUsersRequest());

call.on('data', (user) => {
  console.log('User:', user.toObject());
});

call.on('end', () => {
  console.log('Stream ended');
});

call.on('error', (error) => {
  console.error('Error:', error);
});

// Server
function listUsers(call) {
  const users = db.listUsers();
  users.forEach(user => {
    call.write(user);
  });
  call.end();
}
```

### Client Streaming RPC

Client sends stream of requests, server returns single response:

```javascript
// Client
const call = client.createUserBatch((error, response) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Created:', response.toObject());
});

const users = [{ name: 'John', email: 'john@example.com' }, ...];
users.forEach(user => {
  const request = new CreateUserRequest();
  request.setName(user.name);
  request.setEmail(user.email);
  call.write(request);
});

call.end();

// Server
function createUserBatch(call, callback) {
  const userIds = [];
  
  call.on('data', (request) => {
    const userId = db.createUser(request.toObject());
    userIds.push(userId);
  });
  
  call.on('end', () => {
    const response = new CreateUserBatchResponse();
    response.setUserIdsList(userIds);
    response.setCreatedCount(userIds.length);
    callback(null, response);
  });
}
```

### Bidirectional Streaming RPC

Both client and server send streams:

```javascript
// Client
const call = client.userEvents();

call.on('data', (response) => {
  console.log('Response:', response.toObject());
});

call.on('end', () => {
  console.log('Stream ended');
});

// Send events
function sendEvent(type, payload) {
  const request = new UserEventRequest();
  request.setEventType(type);
  request.setPayload(payload);
  call.write(request);
}

// Server
function userEvents(call) {
  call.on('data', (request) => {
    const response = new UserEventResponse();
    response.setAcknowledged(true);
    response.setMessage('Event received');
    call.write(response);
  });
  
  call.on('end', () => {
    call.end();
  });
}
```

## gRPC vs REST Comparison

| Aspect | gRPC | REST |
|--------|------|------|
| **Protocol** | HTTP/2 | HTTP/1.1 or HTTP/2 |
| **Data Format** | Protocol Buffers (binary) | JSON/XML (text) |
| **Payload Size** | Smaller (binary) | Larger (text) |
| **Code Generation** | Built-in | Manual or third-party |
| **Streaming** | Native support | Limited (SSE) |
| **Browser Support** | Requires gRPC-Web | Native |
| **Learning Curve** | Steeper | Easier |
| **Tooling** | Mature | Very mature |
| **Debugging** | Requires tools | Easy (curl, browser) |
| **Use Case** | Internal microservices | Public APIs |

**When to use gRPC:**
- Internal microservices communication
- High-performance requirements
- Need for streaming
- Strong typing and code generation
- Polyglot environments

**When to use REST:**
- Public-facing APIs
- Browser-based clients
- Simple CRUD operations
- Need for easy debugging
- Legacy system integration

## Code Generation (protoc)

### Installing protoc

```bash
# macOS
brew install protobuf

# Linux
apt-get install protobuf-compiler

# Windows
# Download from https://github.com/protocolbuffers/protobuf/releases
```

### Generating Node.js Code

```bash
# Install plugins
npm install @grpc/grpc-js @grpc/proto-loader

# Generate code
protoc --js_out=import_style=commonjs,binary:. --grpc_out=. \
  --plugin=protoc-gen-grpc=$(which grpc_tools_node_protoc_plugin) \
  user_service.proto
```

### Using @grpc/proto-loader (Dynamic)

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = './proto/user_service.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).user.v1;

const client = new userProto.UserService(
  'localhost:50051',
  grpc.credentials.createInsecure()
);
```

### Generating TypeScript Code

```bash
# Install TypeScript plugin
npm install grpc_tools_node_protoc_ts ts-protoc-gen

# Generate TypeScript code
protoc \
  --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
  --plugin=protoc-gen-grpc=./node_modules/.bin/grpc_tools_node_protoc_plugin \
  --ts_out=./generated \
  --grpc_out=./generated \
  --proto_path=./proto \
  ./proto/user_service.proto
```

### Generating Go Code

```bash
# Install Go plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate Go code
protoc --go_out=. --go_opt=paths=source_relative \
  --go-grpc_out=. --go-grpc_opt=paths=source_relative \
  user_service.proto
```

### Generating Python Code

```bash
# Install Python plugin
pip install grpcio grpcio-tools

# Generate Python code
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/user_service.proto
```

## Error Handling and Status Codes

### gRPC Status Codes

```javascript
const grpc = require('@grpc/grpc-js');

// Common status codes
grpc.status.OK                    // Operation completed successfully
grpc.status.CANCELLED             // Operation was cancelled
grpc.status.UNKNOWN               // Unknown error
grpc.status.INVALID_ARGUMENT      // Client specified invalid argument
grpc.status.DEADLINE_EXCEEDED     // Deadline expired before operation could complete
grpc.status.NOT_FOUND             // Requested entity not found
grpc.status.ALREADY_EXISTS        // Entity already exists
grpc.status.PERMISSION_DENIED     // Caller lacks permission
grpc.status.UNAUTHENTICATED       // Request lacks valid authentication
grpc.status.RESOURCE_EXHAUSTED    // Resource exhausted (quota limit)
grpc.status.FAILED_PRECONDITION   // Operation rejected because system is not in correct state
grpc.status.ABORTED               // Operation was aborted
grpc.status.OUT_OF_RANGE          // Operation attempted past valid range
grpc.status.UNIMPLEMENTED         // Operation is not implemented
grpc.status.INTERNAL              // Internal error
grpc.status.UNAVAILABLE           // Service currently unavailable
grpc.status.DATA_LOSS             // Unrecoverable data loss
```

### Error Handling in Server

```javascript
const grpc = require('@grpc/grpc-js');

function getUser(call, callback) {
  try {
    const userId = call.request.getId();
    
    if (!userId) {
      const error = new Error('User ID is required');
      error.code = grpc.status.INVALID_ARGUMENT;
      error.metadata = new grpc.Metadata();
      error.metadata.set('field', 'id');
      return callback(error);
    }
    
    const user = db.getUser(userId);
    
    if (!user) {
      const error = new Error('User not found');
      error.code = grpc.status.NOT_FOUND;
      return callback(error);
    }
    
    callback(null, user);
  } catch (error) {
    console.error('Error in getUser:', error);
    const grpcError = new Error('Internal server error');
    grpcError.code = grpc.status.INTERNAL;
    callback(grpcError);
  }
}
```

### Error Handling in Client

```javascript
client.getUser(request, (error, response) => {
  if (error) {
    switch (error.code) {
      case grpc.status.NOT_FOUND:
        console.error('User not found');
        break;
      case grpc.status.PERMISSION_DENIED:
        console.error('Permission denied');
        break;
      case grpc.status.DEADLINE_EXCEEDED:
        console.error('Request timeout');
        break;
      default:
        console.error('Error:', error.message);
    }
    return;
  }
  console.log('User:', response.toObject());
});
```

### Custom Error Metadata

```javascript
// Server
function createUser(call, callback) {
  try {
    const { name, email } = call.request.toObject();
    
    const validationErrors = validateUser({ name, email });
    if (validationErrors.length > 0) {
      const error = new Error('Validation failed');
      error.code = grpc.status.INVALID_ARGUMENT;
      error.metadata = new grpc.Metadata();
      error.metadata.set('validation-errors', JSON.stringify(validationErrors));
      return callback(error);
    }
    
    const user = db.createUser({ name, email });
    callback(null, user);
  } catch (error) {
    callback(error);
  }
}

// Client
client.createUser(request, (error, response) => {
  if (error && error.code === grpc.status.INVALID_ARGUMENT) {
    const validationErrors = JSON.parse(
      error.metadata.get('validation-errors')[0]
    );
    console.error('Validation errors:', validationErrors);
  }
});
```

## Interceptors and Middleware

### Server Interceptors

```javascript
const grpc = require('@grpc/grpc-js');

// Logging interceptor
const loggingInterceptor = (options, nextCall) => {
  return new grpc.ServerInterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      console.log(`[Request] ${options.method_definition.path}`);
      const newListener = {
        onReceiveMessage: (message, next) => {
          console.log(`[Message] ${JSON.stringify(message)}`);
          next(message);
        },
        onReceiveStatus: (status, next) => {
          console.log(`[Status] ${status.code} - ${status.details}`);
          next(status);
        },
      };
      next(metadata, newListener);
    },
  });
};

// Authentication interceptor
const authInterceptor = (options, nextCall) => {
  return new grpc.ServerInterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const token = metadata.get('authorization')[0];
      
      if (!token) {
        const error = {
          code: grpc.status.UNAUTHENTICATED,
          details: 'Missing authentication token',
        };
        return next(null, { status: error });
      }
      
      const user = verifyToken(token);
      if (!user) {
        const error = {
          code: grpc.status.UNAUTHENTICATED,
          details: 'Invalid token',
        };
        return next(null, { status: error });
      }
      
      // Add user to call
      options.user = user;
      next(metadata, listener);
    },
  });
};

// Apply interceptors
const server = new grpc.Server();
server.addService(userProto.UserService.service, { getUser, ... });
server.bindAsync(
  '0.0.0.0:50051',
  grpc.ServerCredentials.createInsecure(),
  () => {
    console.log('Server started');
  }
);
```

### Client Interceptors

```javascript
// Retry interceptor
const retryInterceptor = (options, nextCall) => {
  let retryCount = 0;
  const maxRetries = 3;
  
  const newCall = nextCall(options);
  const originalStart = newCall.startWithContext;
  
  newCall.startWithContext = function (metadata, listener, next) {
    const retryListener = {
      onReceiveStatus: (status, next) => {
        if (status.code === grpc.status.UNAVAILABLE && retryCount < maxRetries) {
          retryCount++;
          console.log(`Retrying... (${retryCount}/${maxRetries})`);
          setTimeout(() => {
            newCall.startWithContext(metadata, listener, next);
          }, 1000 * retryCount);
          return;
        }
        next(status);
      },
    };
    originalStart.call(this, metadata, retryListener, next);
  };
  
  return newCall;
};

// Apply client interceptors
const client = new userProto.UserService(
  'localhost:50051',
  grpc.credentials.createInsecure(),
  { interceptors: [retryInterceptor] }
);
```

## Authentication (TLS, JWT, API Keys)

### TLS/SSL Configuration

```javascript
const grpc = require('@grpc/grpc-js');
const fs = require('fs');

// Server with TLS
const serverCredentials = grpc.ServerCredentials.createSsl(
  fs.readFileSync('ca.crt'), // CA certificate
  [
    {
      cert_chain: fs.readFileSync('server.crt'),
      private_key: fs.readFileSync('server.key'),
    },
  ],
  false // check client certificate
);

server.bindAsync(
  '0.0.0.0:50051',
  serverCredentials,
  () => {
    console.log('Secure server started');
  }
);

// Client with TLS
const clientCredentials = grpc.credentials.createSsl(
  fs.readFileSync('ca.crt'),
  fs.readFileSync('client.key'),
  fs.readFileSync('client.crt')
);

const client = new userProto.UserService(
  'localhost:50051',
  clientCredentials
);
```

### JWT Authentication

```javascript
const jwt = require('jsonwebtoken');

// Server JWT verification
const jwtInterceptor = (options, nextCall) => {
  return new grpc.ServerInterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const token = metadata.get('authorization')?.[0]?.replace('Bearer ', '');
      
      if (!token) {
        return next(null, {
          status: { code: grpc.status.UNAUTHENTICATED, details: 'Missing token' },
        });
      }
      
      try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        options.user = decoded;
        next(metadata, listener);
      } catch (error) {
        return next(null, {
          status: { code: grpc.status.UNAUTHENTICATED, details: 'Invalid token' },
        });
      }
    },
  });
};

// Client JWT authentication
const token = jwt.sign({ userId: '123' }, process.env.JWT_SECRET);
const metadata = new grpc.Metadata();
metadata.add('authorization', `Bearer ${token}`);

client.getUser(request, metadata, (error, response) => {
  // ...
});
```

### API Key Authentication

```javascript
// Server API key verification
const apiKeyInterceptor = (options, nextCall) => {
  return new grpc.ServerInterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const apiKey = metadata.get('x-api-key')?.[0];
      
      if (!apiKey || !isValidApiKey(apiKey)) {
        return next(null, {
          status: { code: grpc.status.UNAUTHENTICATED, details: 'Invalid API key' },
        });
      }
      
      options.apiKey = apiKey;
      next(metadata, listener);
    },
  });
};

function isValidApiKey(apiKey) {
  // Check against database or config
  return process.env.API_KEYS.includes(apiKey);
}

// Client API key authentication
const metadata = new grpc.Metadata();
metadata.add('x-api-key', process.env.API_KEY);

client.getUser(request, metadata, (error, response) => {
  // ...
});
```

## Load Balancing and Service Discovery

### Client-Side Load Balancing

```javascript
const { RoundRobin } = require('@grpc/grpc-js/build/src/load-balancer');

const client = new userProto.UserService(
  'dns:///user-service:50051', // DNS-based service discovery
  grpc.credentials.createInsecure(),
  {
    'grpc.load_balancing_config': [
      { round_robin: {} },
    ],
  }
);
```

### gRPC Name Resolution

```javascript
// Custom DNS resolver
const dns = require('dns');

function resolveService(serviceName, callback) {
  dns.resolveSrv(serviceName, (err, addresses) => {
    if (err) {
      return callback(err);
    }
    
    const targets = addresses.map(addr => ({
      host: addr.name,
      port: addr.port,
    }));
    
    callback(null, targets);
  });
}

// Use custom resolver
const client = new userProto.UserService(
  'custom:///user-service',
  grpc.credentials.createInsecure()
);
```

### Service Discovery with Consul

```javascript
const Consul = require('consul');

const consul = new Consul();

async function getServiceAddress(serviceName) {
  const services = await consul.catalog.service.nodes(serviceName);
  if (services.length === 0) {
    throw new Error(`Service ${serviceName} not found`);
  }
  
  const service = services[Math.floor(Math.random() * services.length)];
  return `${service.ServiceAddress}:${service.ServicePort}`;
}

async function createClient(serviceName) {
  const address = await getServiceAddress(serviceName);
  return new userProto.UserService(
    address,
    grpc.credentials.createInsecure()
  );
}
```

## gRPC-Web for Browser Clients

### Envoy Proxy Setup

```yaml
# envoy.yaml
static_resources:
  listeners:
  - name: grpc_web_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          codec_type: AUTO
          stat_prefix: grpc_web
          route_config:
            name: local_route
            virtual_hosts:
            - name: grpc_web_backend
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: grpc_backend
          http_filters:
          - name: envoy.filters.http.grpc_web
          - name: envoy.filters.http.router
  clusters:
  - name: grpc_backend
    connect_timeout: 5s
    type: LOGICAL_DNS
    http2_protocol_options: {}
    load_assignment:
      cluster_name: grpc_backend
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: localhost
                port_value: 50051
```

### Browser Client

```javascript
import { grpc } from '@improbable-eng/grpc-web';
import { UserServiceClient } from './user_service_pb_service';
import { GetUserRequest } from './user_service_pb';

const client = new UserServiceClient('http://localhost:8080', null, null);

const request = new GetUserRequest();
request.setId('123');

client.getUser(request, {}, (err, response) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log('User:', response.toObject());
});
```

## Health Checking

### Standard Health Check Protocol

```proto
syntax = "proto3";

package grpc.health.v1;

service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}

message HealthCheckRequest {
  string service = 1;
}

message HealthCheckResponse {
  enum ServingStatus {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
    SERVICE_UNKNOWN = 3;
  }
  ServingStatus status = 1;
}
```

### Implementing Health Check

```javascript
const grpc = require('@grpc/grpc-js');
const healthProto = grpc.loadPackageDefinition(
  protoLoader.loadSync('./proto/grpc/health/v1/health.proto')
).grpc.health.v1;

const healthStatus = {
  '': healthProto.HealthCheckResponse.ServingStatus.SERVING,
  'user-service': healthProto.HealthCheckResponse.ServingStatus.SERVING,
};

const healthImpl = {
  check: (call, callback) => {
    const service = call.request.getService();
    const status = healthStatus[service] || healthProto.HealthCheckResponse.ServingStatus.SERVICE_UNKNOWN;
    
    const response = new healthProto.HealthCheckResponse();
    response.setStatus(status);
    callback(null, response);
  },
  watch: (call) => {
    const service = call.request.getService();
    
    const interval = setInterval(() => {
      const status = healthStatus[service] || healthProto.HealthCheckResponse.ServingStatus.SERVICE_UNKNOWN;
      const response = new healthProto.HealthCheckResponse();
      response.setStatus(status);
      call.write(response);
    }, 1000);
    
    call.on('cancelled', () => {
      clearInterval(interval);
      call.end();
    });
  },
};

server.addService(healthProto.Health.service, healthImpl);
```

## Deadlines and Timeouts

### Setting Deadlines

```javascript
// Client deadline
const deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 5); // 5 second deadline

client.getUser(request, { deadline }, (error, response) => {
  if (error && error.code === grpc.status.DEADLINE_EXCEEDED) {
    console.error('Request timed out');
  }
});

// Server handling deadline
function getUser(call, callback) {
  if (call.getDeadline().getTime() < Date.now()) {
    const error = new Error('Deadline exceeded');
    error.code = grpc.status.DEADLINE_EXCEEDED;
    return callback(error);
  }
  
  // Process request...
}
```

### Timeout Configuration

```javascript
const client = new userProto.UserService(
  'localhost:50051',
  grpc.credentials.createInsecure(),
  {
    'grpc.max_receive_message_length': -1, // Unlimited message size
    'grpc.max_send_message_length': -1,
    'grpc.initial_reconnect_backoff_ms': 100,
    'grpc.max_reconnect_backoff_ms': 10000,
    'grpc.keepalive_time_ms': 60000,
    'grpc.keepalive_timeout_ms': 5000,
  }
);
```

## Node.js Implementation

### Complete Server Example

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { v4: uuidv4 } = require('uuid');

// Load proto file
const packageDefinition = protoLoader.loadSync('./proto/user_service.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).user.v1;

// In-memory database
const users = new Map();

// Service implementation
const userService = {
  getUser: (call, callback) => {
    const user = users.get(call.request.getId());
    if (!user) {
      const error = new Error('User not found');
      error.code = grpc.status.NOT_FOUND;
      return callback(error);
    }
    callback(null, user);
  },
  
  createUser: (call, callback) => {
    const user = {
      id: uuidv4(),
      name: call.request.getName(),
      email: call.request.getEmail(),
      createdAt: new Date(),
    };
    users.set(user.id, user);
    callback(null, user);
  },
  
  listUsers: (call) => {
    users.forEach(user => {
      call.write(user);
    });
    call.end();
  },
};

// Create server
const server = new grpc.Server();
server.addService(userProto.UserService.service, userService);

server.bindAsync(
  '0.0.0.0:50051',
  grpc.ServerCredentials.createInsecure(),
  (error, port) => {
    if (error) {
      console.error('Failed to start server:', error);
      return;
    }
    console.log(`Server running on port ${port}`);
  }
);
```

### Complete Client Example

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Load proto file
const packageDefinition = protoLoader.loadSync('./proto/user_service.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).user.v1;

// Create client
const client = new userProto.UserService(
  'localhost:50051',
  grpc.credentials.createInsecure()
);

// Unary call
function getUser(id) {
  return new Promise((resolve, reject) => {
    const request = new userProto.GetUserRequest();
    request.setId(id);
    
    client.getUser(request, (error, response) => {
      if (error) {
        return reject(error);
      }
      resolve(response.toObject());
    });
  });
}

// Create user
function createUser(name, email) {
  return new Promise((resolve, reject) => {
    const request = new userProto.CreateUserRequest();
    request.setName(name);
    request.setEmail(email);
    
    client.createUser(request, (error, response) => {
      if (error) {
        return reject(error);
      }
      resolve(response.toObject());
    });
  });
}

// List users (server streaming)
function listUsers() {
  return new Promise((resolve, reject) => {
    const request = new userProto.ListUsersRequest();
    const users = [];
    
    const call = client.listUsers(request);
    
    call.on('data', (user) => {
      users.push(user.toObject());
    });
    
    call.on('end', () => {
      resolve(users);
    });
    
    call.on('error', reject);
  });
}

// Usage
(async () => {
  try {
    // Create user
    const user = await createUser('John Doe', 'john@example.com');
    console.log('Created user:', user);
    
    // Get user
    const found = await getUser(user.id);
    console.log('Found user:', found);
    
    // List users
    const allUsers = await listUsers();
    console.log('All users:', allUsers);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## Python Implementation

### Server Example

```python
import grpc
from concurrent import futures
import user_service_pb2
import user_service_pb2_grpc
import uuid
from datetime import datetime

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
    
    def GetUser(self, request, context):
        user_id = request.id
        if user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_service_pb2.User()
        
        user = self.users[user_id]
        return user_service_pb2.User(
            id=user['id'],
            name=user['name'],
            email=user['email'],
            created_at=datetime_to_timestamp(user['created_at'])
        )
    
    def CreateUser(self, request, context):
        user_id = str(uuid.uuid4())
        user = {
            'id': user_id,
            'name': request.name,
            'email': request.email,
            'created_at': datetime.utcnow()
        }
        self.users[user_id] = user
        
        return user_service_pb2.User(
            id=user_id,
            name=request.name,
            email=request.email,
            created_at=datetime_to_timestamp(user['created_at'])
        )
    
    def ListUsers(self, request, context):
        for user in self.users.values():
            yield user_service_pb2.User(
                id=user['id'],
                name=user['name'],
                email=user['email'],
                created_at=datetime_to_timestamp(user['created_at'])
            )

def datetime_to_timestamp(dt):
    from google.protobuf.timestamp_pb2 import Timestamp
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started on port 50051')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### Client Example

```python
import grpc
import user_service_pb2
import user_service_pb2_grpc

def get_user(stub, user_id):
    request = user_service_pb2.GetUserRequest(id=user_id)
    response = stub.GetUser(request)
    return response

def create_user(stub, name, email):
    request = user_service_pb2.CreateUserRequest(name=name, email=email)
    response = stub.CreateUser(request)
    return response

def list_users(stub):
    request = user_service_pb2.ListUsersRequest()
    for user in stub.ListUsers(request):
        print(user)

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        
        # Create user
        user = create_user(stub, 'John Doe', 'john@example.com')
        print(f'Created user: {user.id}')
        
        # Get user
        found = get_user(stub, user.id)
        print(f'Found user: {found.name}')
        
        # List users
        print('All users:')
        list_users(stub)

if __name__ == '__main__':
    main()
```

## Go Implementation

### Server Example

```go
package main

import (
  "context"
  "log"
  "net"
  "time"

  "google.golang.org/grpc"
  "google.golang.org/grpc/codes"
  "google.golang.org/grpc/status"
  "google.golang.org/protobuf/types/known/timestamppb"

  pb "path/to/proto/user/v1"
)

type server struct {
  pb.UnimplementedUserServiceServer
  users map[string]*pb.User
}

func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
  user, ok := s.users[req.Id]
  if !ok {
    return nil, status.Error(codes.NotFound, "User not found")
  }
  return user, nil
}

func (s *server) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
  user := &pb.User{
    Id:        generateID(),
    Name:      req.Name,
    Email:     req.Email,
    CreatedAt: timestamppb.Now(),
  }
  s.users[user.Id] = user
  return user, nil
}

func (s *server) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
  for _, user := range s.users {
    if err := stream.Send(user); err != nil {
      return err
    }
  }
  return nil
}

func generateID() string {
  return "user-" + time.Now().Format("20060102150405")
}

func main() {
  lis, err := net.Listen("tcp", ":50051")
  if err != nil {
    log.Fatalf("Failed to listen: %v", err)
  }

  s := grpc.NewServer()
  pb.RegisterUserServiceServer(s, &server{
    users: make(map[string]*pb.User),
  })

  log.Println("Server started on port 50051")
  if err := s.Serve(lis); err != nil {
    log.Fatalf("Failed to serve: %v", err)
  }
}
```

### Client Example

```go
package main

import (
  "context"
  "log"
  "time"

  "google.golang.org/grpc"
  "google.golang.org/grpc/credentials/insecure"

  pb "path/to/proto/user/v1"
)

func main() {
  conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
  if err != nil {
    log.Fatalf("Failed to connect: %v", err)
  }
  defer conn.Close()

  client := pb.NewUserServiceClient(conn)
  ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
  defer cancel()

  // Create user
  createResp, err := client.CreateUser(ctx, &pb.CreateUserRequest{
    Name:  "John Doe",
    Email: "john@example.com",
  })
  if err != nil {
    log.Fatalf("Failed to create user: %v", err)
  }
  log.Printf("Created user: %s", createResp.Id)

  // Get user
  getResp, err := client.GetUser(ctx, &pb.GetUserRequest{Id: createResp.Id})
  if err != nil {
    log.Fatalf("Failed to get user: %v", err)
  }
  log.Printf("Found user: %s", getResp.Name)

  // List users
  listResp, err := client.ListUsers(ctx, &pb.ListUsersRequest{})
  if err != nil {
    log.Fatalf("Failed to list users: %v", err)
  }
  for {
    user, err := listResp.Recv()
    if err != nil {
      break
    }
    log.Printf("User: %s (%s)", user.Name, user.Email)
  }
}
```

## Testing gRPC Services

### Unit Testing with Node.js

```javascript
const grpc = require('@grpc/grpc-js');
const { Server } = require('@grpc/grpc-js');
const assert = require('assert');

describe('UserService', () => {
  let server;
  let client;

  before((done) => {
    server = new Server();
    server.addService(userProto.UserService.service, userService);
    server.bindAsync(
      '0.0.0.0:0', // Use port 0 for random available port
      grpc.ServerCredentials.createInsecure(),
      (error, port) => {
        if (error) return done(error);
        client = new userProto.UserService(
          `localhost:${port}`,
          grpc.credentials.createInsecure()
        );
        done();
      }
    );
  });

  after((done) => {
    client.close();
    server.tryShutdown(done);
  });

  it('should create and get user', (done) => {
    const createRequest = new userProto.CreateUserRequest();
    createRequest.setName('Test User');
    createRequest.setEmail('test@example.com');

    client.createUser(createRequest, (error, user) => {
      assert.ifError(error);
      assert.strictEqual(user.getName(), 'Test User');

      const getRequest = new userProto.GetUserRequest();
      getRequest.setId(user.getId());

      client.getUser(getRequest, (error, foundUser) => {
        assert.ifError(error);
        assert.strictEqual(foundUser.getId(), user.getId());
        done();
      });
    });
  });
});
```

## Best Practices

1. **Schema Design**
   - Use semantic versioning for proto packages
   - Keep proto files in a separate repository for sharing
   - Use well-defined common types
   - Document services and messages with comments

2. **Error Handling**
   - Use appropriate gRPC status codes
   - Include helpful error messages
   - Use metadata for additional error context
   - Log errors server-side

3. **Performance**
   - Use connection pooling
   - Implement proper timeout/deadline handling
   - Enable compression for large payloads
   - Use streaming for large datasets

4. **Security**
   - Always use TLS in production
   - Implement proper authentication
   - Use mutual TLS for service-to-service communication
   - Validate all inputs

5. **Observability**
   - Implement structured logging
   - Use metrics for monitoring
   - Enable tracing with OpenTelemetry
   - Set up health checks

## Production Checklist

- [ ] Define and enforce deadlines/timeouts for every RPC (client and server).
- [ ] Standardize status codes + error details, and avoid leaking internals in messages.
- [ ] Use TLS everywhere; prefer mTLS for service-to-service traffic.
- [ ] Add observability: metrics, structured logs, and distributed tracing with correlation IDs.
- [ ] Add health checks and graceful shutdown; verify under load and deploy conditions.

## Related Skills

- `09-microservices/service-design`
- `09-microservices/service-discovery`
