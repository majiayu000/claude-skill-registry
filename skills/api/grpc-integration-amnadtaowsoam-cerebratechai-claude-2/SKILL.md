# gRPC Integration

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

gRPC (Google Remote Procedure Call) เป็น high-performance, open-source universal RPC framework ที่ใช้ Protocol Buffers สำหรับ serialization เหมาะสำหรับ microservices communication โดยให้ efficient binary serialization, streaming capabilities และ built-in code generation

gRPC ประกอบด้วย:
- **HTTP/2** - Transport protocol ที่มี performance สูง
- **Protocol Buffers** - Binary serialization format ที่ efficient
- **Code Generation** - Auto-generate client และ server code
- **Streaming** - Support unary, server streaming, client streaming, bidirectional
- **Multi-Language** - Support หลาย programming languages
- **Strong Typing** - Type-safe contracts ด้วย .proto files

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Performance** - gRPC ช่วยเพิ่ม performance ได้ถึง 5-10x เมื่อเทียบกับ REST
2. **ลด Latency** - HTTP/2 multiplexing ช่วยลด latency
3. **ลด Bandwidth** - Protocol Buffers ช่วยลด payload size ได้ถึง 70%
4. **เพิ่ม Developer Productivity** - Code generation ช่วยลด boilerplate code
5. **ปรับปรุง Type Safety** - Strong typing ช่วยลด runtime errors

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Schema-First** - gRPC ต้อง schema-first design ด้วย .proto files
2. **Type-Safe** - APIs ต้อง type-safe ด้วย Protocol Buffers
3. **High-Performance** - APIs ต้อง support high-throughput scenarios
4. **Streaming-Ready** - APIs ต้อง support real-time streaming
5. **Multi-Language** - APIs ต้อง support polyglot environments

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

gRPC ประกอบด้วย:

1. **Protocol Buffers** - Binary serialization format สำหรับ efficient data transfer
2. **Service Definition** - .proto files สำหรับ defining services และ messages
3. **Code Generation** - protoc compiler สำหรับ generating client/server code
4. **HTTP/2 Transport** - Multiplexing, header compression, binary framing
5. **Streaming** - Support 4 types: unary, server streaming, client streaming, bidirectional
6. **Interceptors** - Middleware pattern สำหรับ cross-cutting concerns
7. **Load Balancing** - Client-side load balancing ด้วย DNS-based discovery

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              gRPC Architecture                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Client Layer                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Node.js    │  │    Go       │  │  Python   │  │  │
│  │  │  Client     │  │  Client     │  │  Client   │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              gRPC Client Layer                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │   Stub      │  │  Channel    │  │Interceptor│  │  │
│  │  │  Generated  │  │  Management │  │           │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Network Layer (HTTP/2)              │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │Multiplexing │  │Compression  │  │Binary Frame│  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              gRPC Server Layer                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │   Service   │  │Interceptor  │  │   Handler  │  │  │
│  │  │  Registry   │  │  Chain      │  │  Logic     │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Data Layer                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Database   │  │  Cache      │  │  External  │  │  │
│  │  │             │  │             │  │  Services  │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

1. **Proto Definition** - Define services and messages in .proto files
2. **Code Generation** - Generate client and server code with protoc
3. **Service Implementation** - Implement service handlers
4. **Server Setup** - Configure server with credentials and interceptors
5. **Client Setup** - Create client stub with connection settings
6. **Testing** - Write unit and integration tests
7. **Deployment** - Deploy with load balancing and monitoring

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Enterprise Features |
|------|---------|---------------------|
| protoc | Protocol Buffer compiler | Multi-language code generation |
| @grpc/grpc-js | Node.js gRPC runtime | Production-ready, streaming support |
| grpc-go | Go gRPC runtime | High performance, built-in load balancing |
| grpcio | Python gRPC runtime | Async support, interceptors |
| Envoy | gRPC-Web proxy | HTTP/1.1 to HTTP/2 translation |
| Consul | Service discovery | Health checks, DNS-based discovery |

### 3.2 Configuration Essentials

```javascript
// grpc-server.config.js
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

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **gRPC Specification** - Follow official gRPC spec
- **Protocol Buffers Specification** - Follow protobuf encoding rules
- **HTTP/2 Specification** - Follow HTTP/2 RFC
- **TLS 1.3** - Use latest TLS version for secure communication

### 4.2 Security Protocol

1. **TLS/SSL** - Always use TLS in production
2. **Mutual TLS** - Use mTLS for service-to-service communication
3. **Authentication** - Implement JWT or API key authentication
4. **Authorization** - Implement role-based access control
5. **Input Validation** - Validate all inputs
6. **Rate Limiting** - Implement per-client rate limits
7. **Deadlines** - Enforce deadlines for all RPCs

### 4.3 Explainability

- **Proto Documentation** - Document all services and messages
- **Error Messages** - Provide clear, actionable error messages
- **Status Codes** - Use appropriate gRPC status codes
- **Logging** - Log all RPCs with request/response metadata
- **Tracing** - Implement distributed tracing with OpenTelemetry

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

```
Total Cost = (Server Cost) + (Network Cost) + (Storage Cost)

Server Cost = (Instance Hours × Hourly Rate)
Network Cost = (Data Transfer × Cost Per GB)
Storage Cost = (Proto Storage × Cost Per GB)

gRPC Optimization Savings:
- Bandwidth reduction: 50-70% (vs JSON)
- Latency reduction: 30-50% (HTTP/2 multiplexing)
- CPU reduction: 20-30% (binary serialization)
```

### 5.2 Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| RPC Latency | < 50ms | p95 latency |
| Throughput | > 10,000 RPS | Requests per second |
| Error Rate | < 0.01% | Total errors / Total requests |
| Connection Pool Utilization | < 80% | Active connections / Pool size |
| Deadline Exceeded Rate | < 0.1% | Deadline errors / Total requests |
| Serialization Time | < 5ms | Average serialization time |

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Weeks 1-2)**
- Define proto files for core services
- Set up protoc build pipeline
- Implement basic unary RPCs

**Phase 2: Integration (Weeks 3-4)**
- Implement streaming RPCs
- Add interceptors for auth and logging
- Set up TLS configuration

**Phase 3: Optimization (Weeks 5-6)**
- Implement load balancing
- Add deadlines and timeouts
- Performance tuning

**Phase 4: Production (Weeks 7-8)**
- Deploy with monitoring
- Set up service discovery
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Ignoring Deadlines** - Always set deadlines for all RPCs
2. **Blocking Calls** - Use async patterns to avoid blocking
3. **No Error Handling** - Handle all gRPC status codes properly
4. **Skipping TLS** - Always use TLS in production
5. **Large Messages** - Keep messages small and use streaming
6. **No Observability** - Monitor all RPCs with metrics and tracing
7. **Versioning Issues** - Use semantic versioning for proto packages

### 6.3 Best Practices Checklist

- [ ] Use semantic versioning for proto packages
- [ ] Keep proto files in separate repository
- [ ] Document all services and messages
- [ ] Use appropriate gRPC status codes
- [ ] Implement deadlines for all RPCs
- [ ] Use TLS in production
- [ ] Implement authentication and authorization
- [ ] Add interceptors for logging and metrics
- [ ] Use connection pooling
- [ ] Implement health checks
- [ ] Set up distributed tracing
- [ ] Use streaming for large datasets
- [ ] Implement graceful shutdown
- [ ] Add input validation
- [ ] Monitor performance metrics

---

## 7. Implementation Examples

### 7.1 Proto File Definition

```proto
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";

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

### 7.2 Node.js Server Implementation

```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { v4: uuidv4 } = require('uuid');

const PROTO_PATH = './proto/user_service.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).user.v1;

const users = new Map();

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
  
  createUserBatch: (call, callback) => {
    const userIds = [];
    
    call.on('data', (request) => {
      const user = {
        id: uuidv4(),
        name: request.getName(),
        email: request.getEmail(),
        createdAt: new Date(),
      };
      users.set(user.id, user);
      userIds.push(user.id);
    });
    
    call.on('end', () => {
      const response = new userProto.CreateUserBatchResponse();
      response.setUserIdsList(userIds);
      response.setCreatedCount(userIds.length);
      callback(null, response);
    });
  },
  
  userEvents: (call) => {
    call.on('data', (request) => {
      const response = new userProto.UserEventResponse();
      response.setAcknowledged(true);
      response.setMessage('Event received');
      call.write(response);
    });
    
    call.on('end', () => {
      call.end();
    });
  },
};

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

### 7.3 Node.js Client Implementation

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

### 7.4 Authentication Interceptor

```javascript
const grpc = require('@grpc/grpc-js');
const jwt = require('jsonwebtoken');

const authInterceptor = (options, nextCall) => {
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

const server = new grpc.Server({
  interceptors: [authInterceptor],
});
server.addService(userProto.UserService.service, userService);
```

### 7.5 TLS Configuration

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
  (error, port) => {
    if (error) {
      console.error('Failed to start server:', error);
      return;
    }
    console.log(`Secure server running on port ${port}`);
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

### 7.6 Deadline Configuration

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

### 7.7 Load Balancing with DNS

```javascript
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

### 7.8 Health Check Implementation

```javascript
const healthStatus = {
  '': grpc.status.OK,
  'user-service': grpc.status.OK,
};

const healthImpl = {
  check: (call, callback) => {
    const service = call.request.getService();
    const status = healthStatus[service] || grpc.status.SERVICE_UNKNOWN;
    
    const response = new healthProto.HealthCheckResponse();
    response.setStatus(status);
    callback(null, response);
  },
  
  watch: (call) => {
    const service = call.request.getService();
    
    const interval = setInterval(() => {
      const status = healthStatus[service] || grpc.status.SERVICE_UNKNOWN;
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

---

## 8. Related Skills

- [`03-backend-api/express-rest`](03-backend-api/express-rest/SKILL.md)
- [`03-backend-api/nodejs-api`](03-backend-api/nodejs-api/SKILL.md)
- [`03-backend-api/websocket-patterns`](03-backend-api/websocket-patterns/SKILL.md)
- [`09-microservices/service-design`](09-microservices/service-design/SKILL.md)
- [`09-microservices/service-discovery`](09-microservices/service-discovery/SKILL.md)
- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
