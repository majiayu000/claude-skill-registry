---
name: kratos-proto-api
description: Generates protobuf API definitions for go-kratos microservices with HTTP annotations, validation rules, and OpenAPI documentation. Use when defining service contracts and APIs.
---

<objective>
Create protobuf service definitions that generate both gRPC and HTTP/JSON APIs with validation rules and OpenAPI specs for go-kratos microservices.
</objective>

<quick_start>
Create proto file in `api/{service}/v1/{entity}.proto`:

```protobuf
syntax = "proto3";

package {service}.v1;

import "google/api/annotations.proto";
import "validate/validate.proto";

service {Entity}Service {
  rpc Create{Entity}(Create{Entity}Request) returns (Create{Entity}Response) {
    option (google.api.http) = {
      post: "/v1/{entities}"
      body: "*"
    };
  }
}

message Create{Entity}Request {
  string name = 1 [(validate.rules).string = {min_len: 1, max_len: 255}];
}

message Create{Entity}Response {
  {Entity} {entity} = 1;
}

message {Entity} {
  uint64 id = 1;
  string name = 2;
}
```
</quick_start>

<service_patterns>
## Service Definition

```protobuf
service {Entity}Service {
  // Create
  rpc Create{Entity}(Create{Entity}Request) returns (Create{Entity}Response) {
    option (google.api.http) = {
      post: "/v1/{entities}"
      body: "*"
    };
  }

  // Get
  rpc Get{Entity}(Get{Entity}Request) returns (Get{Entity}Response) {
    option (google.api.http) = {
      get: "/v1/{entities}/{id}"
    };
  }

  // Update
  rpc Update{Entity}(Update{Entity}Request) returns (Update{Entity}Response) {
    option (google.api.http) = {
      put: "/v1/{entities}/{id}"
      body: "*"
    };
  }

  // Delete
  rpc Delete{Entity}(Delete{Entity}Request) returns (Delete{Entity}Response) {
    option (google.api.http) = {
      delete: "/v1/{entities}/{id}"
    };
  }

  // List
  rpc List{Entities}(List{Entities}Request) returns (List{Entities}Response) {
    option (google.api.http) = {
      get: "/v1/{entities}"
    };
  }
}
```
</service_patterns>

<message_patterns>
## Message Patterns

**Create Request**:
```protobuf
message Create{Entity}Request {
  string name = 1 [(validate.rules).string = {min_len: 1, max_len: 255}];
  uint64 project_id = 2 [(validate.rules).uint64 = {gt: 0}];
}
```

**Update Request**:
```protobuf
message Update{Entity}Request {
  uint64 id = 1 [(validate.rules).uint64 = {gt: 0}];
  string name = 2 [(validate.rules).string = {min_len: 1, max_len: 255}];
}
```

**Get Request**:
```protobuf
message Get{Entity}Request {
  uint64 id = 1 [(validate.rules).uint64 = {gt: 0}];
}
```

**List Request**:
```protobuf
message List{Entities}Request {
  uint64 offset = 1;
  uint64 limit = 2 [(validate.rules).uint64 = {gte: 1, lte: 100}];
}
```

**List Response with Pagination**:
```protobuf
message List{Entities}Response {
  repeated {Entity} {entities} = 1;
  PaginationMeta meta = 2;
}

message PaginationMeta {
  uint64 total = 1;
  uint64 offset = 2;
  uint64 limit = 3;
}
```
</message_patterns>

<validation_rules>
## Validation Rules

**Strings**:
```protobuf
string name = 1 [(validate.rules).string = {min_len: 1, max_len: 255}];
string email = 2 [(validate.rules).string = {email: true}];
string uuid = 3 [(validate.rules).string = {uuid: true}];
string status = 4 [(validate.rules).string = {in: ["active", "inactive"]}];
```

**Numbers**:
```protobuf
uint64 id = 1 [(validate.rules).uint64 = {gt: 0}];
uint32 count = 2 [(validate.rules).uint32 = {gte: 0, lte: 1000}];
```

**Optional Fields**: Omit validation or use `ignore_empty: true`
</validation_rules>

<http_annotations>
## HTTP Mapping

**REST patterns**:
- POST `/v1/{entities}` - Create
- GET `/v1/{entities}/{id}` - Get
- PUT `/v1/{entities}/{id}` - Update
- DELETE `/v1/{entities}/{id}` - Delete
- GET `/v1/{entities}` - List

**Path variables**:
```protobuf
rpc Get{Entity}(Get{Entity}Request) returns (Get{Entity}Response) {
  option (google.api.http) = {
    get: "/v1/{entities}/{id}"  // {id} matches field in request
  };
}

message Get{Entity}Request {
  uint64 id = 1;  // Extracted from URL path
}
```

**Query parameters** (for GET/DELETE):
All request fields not in path become query params

**Request body** (for POST/PUT):
Use `body: "*"` to send entire request as JSON body
</http_annotations>

<file_structure>
## Proto File Organization

```
api/{service}/v1/
├── {entity}.proto         # Main entity definitions
├── common.proto          # Shared messages (PaginationMeta, etc.)
└── errors.proto          # Error definitions (optional)
```

**Required imports**:
```protobuf
import "google/api/annotations.proto";
import "validate/validate.proto";
import "google/protobuf/timestamp.proto";  // If using timestamps
```
</file_structure>

<generation_commands>
## After Creating Proto

1. **Format proto files**:
   ```bash
   make contracts-format
   ```

2. **Lint proto files**:
   ```bash
   make contracts-lint
   ```

3. **Generate code**:
   ```bash
   make contracts-generate
   ```

4. **Check for breaking changes**:
   ```bash
   make contracts-breaking
   ```
</generation_commands>

<success_criteria>
Proto definitions are correct when:
- [ ] Service name matches entity ({{Entity}Service)
- [ ] HTTP annotations follow REST conventions
- [ ] Validation rules on all required fields
- [ ] Message names follow {Operation}{Entity}{Request|Response}
- [ ] Path variables match request fields
- [ ] Repeated fields use plural names
- [ ] Imports include google/api/annotations and validate
- [ ] File compiles with `make contracts-generate`
- [ ] No breaking changes in `make contracts-breaking`
</success_criteria>