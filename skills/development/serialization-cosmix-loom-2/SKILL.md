---
name: serialization
description: Data serialization and deserialization patterns across formats. Use when implementing data exchange, API payloads, storage formats, encoding/decoding, or cross-language communication. Keywords: serialize, deserialize, serialization, deserialization, JSON, YAML, TOML, XML, Protocol Buffers, protobuf, MessagePack, CBOR, serde, encoding, decoding, schema, schema evolution, versioning, backward compatibility, forward compatibility, binary format, text format, data interchange, gRPC, API contracts.
---

# Serialization

## Overview

Serialization is the process of converting data structures into a format that can be stored or transmitted and later reconstructed. This skill covers JSON best practices, binary formats like Protocol Buffers and MessagePack, schema evolution strategies, and performance considerations.

## Key Concepts

### JSON Serialization Best Practices

**Consistent Naming Conventions:**

```typescript
// camelCase for JavaScript/TypeScript APIs
interface UserResponse {
  userId: string;
  firstName: string;
  lastName: string;
  emailAddress: string;
  createdAt: string;
}

// snake_case for Python/Ruby APIs
interface UserResponseSnake {
  user_id: string;
  first_name: string;
  last_name: string;
  email_address: string;
  created_at: string;
}

// Case conversion utilities
function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function convertKeys(obj: any, converter: (key: string) => string): any {
  if (Array.isArray(obj)) {
    return obj.map((item) => convertKeys(item, converter));
  }
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        converter(key),
        convertKeys(value, converter),
      ]),
    );
  }
  return obj;
}
```

**Date/Time Handling:**

```typescript
// Always use ISO 8601 format
const dateFormats = {
  // Preferred: Full ISO 8601 with timezone
  iso8601: "2024-12-19T14:30:00.000Z",

  // Date only
  dateOnly: "2024-12-19",

  // With timezone offset
  withOffset: "2024-12-19T14:30:00+00:00",

  // Unix timestamp (seconds) - use for precise timing
  unixSeconds: 1703000000,

  // Unix timestamp (milliseconds)
  unixMillis: 1703000000000,
};

class DateSerializer {
  static toJSON(date: Date): string {
    return date.toISOString();
  }

  static fromJSON(value: string | number): Date {
    if (typeof value === "number") {
      // Handle both seconds and milliseconds
      return new Date(value < 1e12 ? value * 1000 : value);
    }
    return new Date(value);
  }

  static toUnix(date: Date): number {
    return Math.floor(date.getTime() / 1000);
  }
}
```

**Null vs Undefined vs Omission:**

```typescript
interface ApiResponse {
  // Required field - always present
  id: string;

  // Optional field - may be omitted
  nickname?: string;

  // Nullable field - present but may be null
  deletedAt: string | null;
}

// Serialization strategies
const serializationStrategies = {
  // Strategy 1: Omit undefined, keep null
  omitUndefined: (obj: any) => JSON.parse(JSON.stringify(obj)),

  // Strategy 2: Convert undefined to null
  undefinedToNull: (obj: any) =>
    JSON.parse(JSON.stringify(obj, (_, v) => (v === undefined ? null : v))),

  // Strategy 3: Explicit handling
  explicit: (obj: any) => {
    const result: any = {};
    for (const [key, value] of Object.entries(obj)) {
      if (value !== undefined) {
        result[key] = value;
      }
    }
    return result;
  },
};
```

**Custom JSON Serialization:**

```typescript
class CustomSerializer {
  private serializers: Map<string, (value: any) => any> = new Map();
  private deserializers: Map<string, (value: any) => any> = new Map();

  registerType<T>(
    typeName: string,
    serialize: (value: T) => any,
    deserialize: (value: any) => T,
  ): void {
    this.serializers.set(typeName, serialize);
    this.deserializers.set(typeName, deserialize);
  }

  serialize(value: any): string {
    return JSON.stringify(value, (key, val) => {
      if (val instanceof Date) {
        return { __type: "Date", value: val.toISOString() };
      }
      if (val instanceof Map) {
        return { __type: "Map", value: Array.from(val.entries()) };
      }
      if (val instanceof Set) {
        return { __type: "Set", value: Array.from(val) };
      }
      if (val instanceof BigInt) {
        return { __type: "BigInt", value: val.toString() };
      }
      return val;
    });
  }

  deserialize<T>(json: string): T {
    return JSON.parse(json, (key, val) => {
      if (val && typeof val === "object" && "__type" in val) {
        switch (val.__type) {
          case "Date":
            return new Date(val.value);
          case "Map":
            return new Map(val.value);
          case "Set":
            return new Set(val.value);
          case "BigInt":
            return BigInt(val.value);
        }
      }
      return val;
    });
  }
}

// Usage
const serializer = new CustomSerializer();
const data = {
  id: 1,
  created: new Date(),
  tags: new Set(["a", "b"]),
  metadata: new Map([["key", "value"]]),
};

const json = serializer.serialize(data);
const restored = serializer.deserialize(json);
```

### Protocol Buffers (Protobuf)

**Schema Definition (.proto):**

```protobuf
syntax = "proto3";

package myapp;

// Enum definition
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

// Message definitions
message User {
  string id = 1;
  string email = 2;
  string name = 3;
  optional string phone = 4;
  repeated string roles = 5;
  map<string, string> metadata = 6;
  google.protobuf.Timestamp created_at = 7;
}

message Address {
  string street = 1;
  string city = 2;
  string state = 3;
  string postal_code = 4;
  string country = 5;
}

message Order {
  string id = 1;
  string user_id = 2;
  OrderStatus status = 3;
  repeated OrderItem items = 4;
  Address shipping_address = 5;
  int64 total_cents = 6;
  string currency = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp updated_at = 9;
}

message OrderItem {
  string product_id = 1;
  string name = 2;
  int32 quantity = 3;
  int64 price_cents = 4;
}

// Service definition (for gRPC)
service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc UpdateOrderStatus(UpdateOrderStatusRequest) returns (Order);
}

message CreateOrderRequest {
  string user_id = 1;
  repeated OrderItem items = 2;
  Address shipping_address = 3;
}

message GetOrderRequest {
  string order_id = 1;
}

message ListOrdersRequest {
  string user_id = 1;
  int32 page_size = 2;
  string page_token = 3;
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
}

message UpdateOrderStatusRequest {
  string order_id = 1;
  OrderStatus status = 2;
}
```

**TypeScript Usage with protobufjs:**

```typescript
import * as protobuf from "protobufjs";

class ProtobufSerializer {
  private root: protobuf.Root;

  async load(protoPath: string): Promise<void> {
    this.root = await protobuf.load(protoPath);
  }

  encode<T>(typeName: string, payload: T): Uint8Array {
    const MessageType = this.root.lookupType(typeName);
    const errMsg = MessageType.verify(payload);
    if (errMsg) throw new Error(errMsg);

    const message = MessageType.create(payload);
    return MessageType.encode(message).finish();
  }

  decode<T>(typeName: string, buffer: Uint8Array): T {
    const MessageType = this.root.lookupType(typeName);
    const message = MessageType.decode(buffer);
    return MessageType.toObject(message, {
      longs: String,
      enums: String,
      defaults: true,
    }) as T;
  }
}

// Usage
const serializer = new ProtobufSerializer();
await serializer.load("./schema.proto");

const order = {
  id: "ord_123",
  userId: "usr_456",
  status: "ORDER_STATUS_PENDING",
  items: [
    { productId: "prod_789", name: "Widget", quantity: 2, priceCents: 1999 },
  ],
  totalCents: 3998,
  currency: "USD",
};

const buffer = serializer.encode("myapp.Order", order);
const decoded = serializer.decode<typeof order>("myapp.Order", buffer);
```

**Python Usage:**

```python
from google.protobuf import json_format
import myapp_pb2

# Create message
order = myapp_pb2.Order(
    id='ord_123',
    user_id='usr_456',
    status=myapp_pb2.ORDER_STATUS_PENDING,
    total_cents=3998,
    currency='USD'
)

# Add repeated field
item = order.items.add()
item.product_id = 'prod_789'
item.name = 'Widget'
item.quantity = 2
item.price_cents = 1999

# Serialize
binary_data = order.SerializeToString()

# Deserialize
parsed_order = myapp_pb2.Order()
parsed_order.ParseFromString(binary_data)

# Convert to/from JSON
json_str = json_format.MessageToJson(order)
from_json = json_format.Parse(json_str, myapp_pb2.Order())
```

### MessagePack

**Basic Usage:**

```typescript
import * as msgpack from "@msgpack/msgpack";

// Simple encode/decode
const data = {
  name: "Alice",
  age: 30,
  tags: ["developer", "typescript"],
  active: true,
  metadata: { key: "value" },
};

const encoded = msgpack.encode(data);
const decoded = msgpack.decode(encoded);

// With options
const encoder = new msgpack.Encoder({
  extensionCodec: createCustomCodec(),
  ignoreUndefined: true,
});

const decoder = new msgpack.Decoder({
  extensionCodec: createCustomCodec(),
});
```

**Custom Extension Types:**

```typescript
import { ExtensionCodec } from "@msgpack/msgpack";

function createCustomCodec(): ExtensionCodec {
  const codec = new ExtensionCodec();

  // Date extension (type 0)
  codec.register({
    type: 0,
    encode: (value: unknown): Uint8Array | null => {
      if (value instanceof Date) {
        const ms = value.getTime();
        const buffer = new ArrayBuffer(8);
        new DataView(buffer).setBigInt64(0, BigInt(ms));
        return new Uint8Array(buffer);
      }
      return null;
    },
    decode: (data: Uint8Array): Date => {
      const ms = new DataView(data.buffer).getBigInt64(0);
      return new Date(Number(ms));
    },
  });

  // BigInt extension (type 1)
  codec.register({
    type: 1,
    encode: (value: unknown): Uint8Array | null => {
      if (typeof value === "bigint") {
        return new TextEncoder().encode(value.toString());
      }
      return null;
    },
    decode: (data: Uint8Array): bigint => {
      return BigInt(new TextDecoder().decode(data));
    },
  });

  return codec;
}
```

**Streaming Encoder/Decoder:**

```typescript
import { Encoder, Decoder, decodeMultiStream } from "@msgpack/msgpack";

// Encode multiple messages to a stream
async function encodeStream(
  messages: any[],
  stream: WritableStream<Uint8Array>,
): Promise<void> {
  const encoder = new Encoder();
  const writer = stream.getWriter();

  for (const message of messages) {
    const encoded = encoder.encode(message);
    await writer.write(encoded);
  }

  await writer.close();
}

// Decode from a stream
async function* decodeStream<T>(
  stream: ReadableStream<Uint8Array>,
): AsyncIterable<T> {
  for await (const message of decodeMultiStream(stream)) {
    yield message as T;
  }
}
```

### Rust Serde Patterns

**Basic Serde Usage:**

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    id: String,
    email: String,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    phone: Option<String>,
    tags: Vec<String>,
}

// Serialize to JSON
let user = User {
    id: "usr_123".to_string(),
    email: "user@example.com".to_string(),
    name: "Alice".to_string(),
    phone: None,
    tags: vec!["admin".to_string()],
};

let json = serde_json::to_string(&user)?;
let pretty = serde_json::to_string_pretty(&user)?;

// Deserialize from JSON
let parsed: User = serde_json::from_str(&json)?;
```

**Custom Serialization with Serde Attributes:**

```rust
use serde::{Deserialize, Serialize};
use std::time::{Duration, SystemTime};

#[derive(Serialize, Deserialize)]
struct Order {
    #[serde(rename = "orderId")]
    id: String,

    #[serde(rename = "userId")]
    user_id: String,

    // Skip serializing default values
    #[serde(skip_serializing_if = "Vec::is_empty", default)]
    items: Vec<OrderItem>,

    // Custom serialization for timestamps
    #[serde(with = "timestamp_serde")]
    created_at: SystemTime,

    // Flatten nested struct into parent
    #[serde(flatten)]
    metadata: OrderMetadata,

    // Skip field entirely
    #[serde(skip)]
    internal_state: String,
}

#[derive(Serialize, Deserialize)]
struct OrderItem {
    product_id: String,
    quantity: u32,
    price_cents: i64,
}

#[derive(Serialize, Deserialize)]
struct OrderMetadata {
    source: String,
    campaign: Option<String>,
}

// Custom timestamp serialization module
mod timestamp_serde {
    use serde::{Deserialize, Deserializer, Serializer};
    use std::time::{SystemTime, UNIX_EPOCH};

    pub fn serialize<S>(time: &SystemTime, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let duration = time.duration_since(UNIX_EPOCH)
            .map_err(serde::ser::Error::custom)?;
        serializer.serialize_u64(duration.as_secs())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<SystemTime, D::Error>
    where
        D: Deserializer<'de>,
    {
        let secs = u64::deserialize(deserializer)?;
        Ok(UNIX_EPOCH + std::time::Duration::from_secs(secs))
    }
}
```

**Serde with Multiple Formats:**

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Config {
    name: String,
    port: u16,
    database_url: String,
    features: Vec<String>,
}

// JSON
let json_str = serde_json::to_string(&config)?;
let from_json: Config = serde_json::from_str(&json_str)?;

// YAML
let yaml_str = serde_yaml::to_string(&config)?;
let from_yaml: Config = serde_yaml::from_str(&yaml_str)?;

// TOML
let toml_str = toml::to_string(&config)?;
let from_toml: Config = toml::from_str(&toml_str)?;

// MessagePack
let msgpack_bytes = rmp_serde::to_vec(&config)?;
let from_msgpack: Config = rmp_serde::from_slice(&msgpack_bytes)?;

// Bincode (binary)
let bincode_bytes = bincode::serialize(&config)?;
let from_bincode: Config = bincode::deserialize(&bincode_bytes)?;
```

**Custom Serialize/Deserialize Implementation:**

```rust
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::fmt;

struct UserId(u64);

impl Serialize for UserId {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        // Serialize as string with prefix
        serializer.serialize_str(&format!("usr_{}", self.0))
    }
}

impl<'de> Deserialize<'de> for UserId {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct UserIdVisitor;

        impl<'de> serde::de::Visitor<'de> for UserIdVisitor {
            type Value = UserId;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("a user ID string like 'usr_123'")
            }

            fn visit_str<E>(self, value: &str) -> Result<UserId, E>
            where
                E: serde::de::Error,
            {
                if let Some(id_str) = value.strip_prefix("usr_") {
                    id_str.parse::<u64>()
                        .map(UserId)
                        .map_err(|_| E::custom("invalid user ID number"))
                } else {
                    Err(E::custom("user ID must start with 'usr_'"))
                }
            }
        }

        deserializer.deserialize_str(UserIdVisitor)
    }
}
```

**Enum Serialization Strategies:**

```rust
use serde::{Deserialize, Serialize};

// Externally tagged (default)
#[derive(Serialize, Deserialize)]
enum Message {
    Text(String),
    Image { url: String, width: u32, height: u32 },
}
// JSON: {"Text": "hello"} or {"Image": {"url": "...", "width": 100, "height": 100}}

// Internally tagged
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
enum MessageInternal {
    Text { content: String },
    Image { url: String, width: u32, height: u32 },
}
// JSON: {"type": "Text", "content": "hello"}

// Adjacently tagged
#[derive(Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
enum MessageAdjacent {
    Text(String),
    Image { url: String, width: u32, height: u32 },
}
// JSON: {"type": "Text", "data": "hello"}

// Untagged (determined by shape)
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum Value {
    String(String),
    Number(i64),
    Boolean(bool),
}
// JSON: "hello" or 123 or true
```

### Protocol Buffers for gRPC

**Service Definition with gRPC:**

```protobuf
syntax = "proto3";

package users.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// User service for managing user accounts
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);

  // Server streaming RPC
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming RPC
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateUsersResponse);

  // Bidirectional streaming RPC
  rpc SyncUsers(stream UserUpdate) returns (stream UserUpdate);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  optional string phone = 4;
  repeated string roles = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

message GetUserRequest {
  string id = 1;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  optional string phone = 3;
  repeated string roles = 4;
}

message UpdateUserRequest {
  string id = 1;
  optional string email = 2;
  optional string name = 3;
  optional string phone = 4;
  repeated string roles = 5;
}

message DeleteUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  optional string filter = 3;
}

message BatchCreateUsersResponse {
  repeated User users = 1;
  int32 success_count = 2;
  int32 failure_count = 3;
}

message UserUpdate {
  enum UpdateType {
    UPDATE_TYPE_UNSPECIFIED = 0;
    UPDATE_TYPE_CREATED = 1;
    UPDATE_TYPE_UPDATED = 2;
    UPDATE_TYPE_DELETED = 3;
  }

  UpdateType type = 1;
  User user = 2;
}
```

**Rust gRPC Server Implementation (tonic):**

```rust
use tonic::{transport::Server, Request, Response, Status};

pub mod users {
    tonic::include_proto!("users.v1");
}

use users::user_service_server::{UserService, UserServiceServer};
use users::{User, GetUserRequest, CreateUserRequest, ListUsersRequest};

#[derive(Default)]
pub struct UserServiceImpl {}

#[tonic::async_trait]
impl UserService for UserServiceImpl {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<User>, Status> {
        let req = request.into_inner();

        // Business logic here
        let user = User {
            id: req.id,
            email: "user@example.com".to_string(),
            name: "Alice".to_string(),
            phone: None,
            roles: vec!["user".to_string()],
            created_at: Some(prost_types::Timestamp::from(std::time::SystemTime::now())),
            updated_at: Some(prost_types::Timestamp::from(std::time::SystemTime::now())),
        };

        Ok(Response::new(user))
    }

    async fn create_user(
        &self,
        request: Request<CreateUserRequest>,
    ) -> Result<Response<User>, Status> {
        let req = request.into_inner();

        // Validation
        if req.email.is_empty() {
            return Err(Status::invalid_argument("email is required"));
        }

        // Create user logic...
        let user = User {
            id: uuid::Uuid::new_v4().to_string(),
            email: req.email,
            name: req.name,
            phone: req.phone,
            roles: req.roles,
            created_at: Some(prost_types::Timestamp::from(std::time::SystemTime::now())),
            updated_at: Some(prost_types::Timestamp::from(std::time::SystemTime::now())),
        };

        Ok(Response::new(user))
    }

    type ListUsersStream = tokio_stream::wrappers::ReceiverStream<Result<User, Status>>;

    async fn list_users(
        &self,
        request: Request<ListUsersRequest>,
    ) -> Result<Response<Self::ListUsersStream>, Status> {
        let (tx, rx) = tokio::sync::mpsc::channel(128);

        tokio::spawn(async move {
            // Stream users from database
            for i in 0..10 {
                let user = User {
                    id: format!("usr_{}", i),
                    email: format!("user{}@example.com", i),
                    name: format!("User {}", i),
                    phone: None,
                    roles: vec![],
                    created_at: None,
                    updated_at: None,
                };

                if tx.send(Ok(user)).await.is_err() {
                    break;
                }
            }
        });

        Ok(Response::new(tokio_stream::wrappers::ReceiverStream::new(rx)))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let service = UserServiceImpl::default();

    Server::builder()
        .add_service(UserServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
```

**Rust gRPC Client:**

```rust
use users::user_service_client::UserServiceClient;
use users::{GetUserRequest, CreateUserRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = UserServiceClient::connect("http://[::1]:50051").await?;

    // Unary call
    let request = tonic::Request::new(GetUserRequest {
        id: "usr_123".to_string(),
    });

    let response = client.get_user(request).await?;
    println!("User: {:?}", response.into_inner());

    // Create user
    let request = tonic::Request::new(CreateUserRequest {
        email: "new@example.com".to_string(),
        name: "New User".to_string(),
        phone: None,
        roles: vec!["user".to_string()],
    });

    let response = client.create_user(request).await?;
    println!("Created: {:?}", response.into_inner());

    // Streaming call
    let request = tonic::Request::new(ListUsersRequest {
        page_size: 10,
        page_token: String::new(),
        filter: None,
    });

    let mut stream = client.list_users(request).await?.into_inner();

    while let Some(user) = stream.message().await? {
        println!("Received user: {:?}", user);
    }

    Ok(())
}
```

### Schema Evolution and Versioning

**Field Numbering Strategy (Protobuf):**

```protobuf
message User {
  // Core fields: 1-15 (1-byte tag, most efficient)
  string id = 1;
  string email = 2;
  string name = 3;

  // Common fields: 16-100
  optional string phone = 16;
  optional string avatar_url = 17;

  // Reserved for future use: 101-200
  reserved 101 to 200;

  // Extension fields: 201+
  map<string, string> metadata = 201;

  // Deprecated fields (never reuse numbers!)
  reserved 50, 51;
  reserved "old_field", "legacy_field";
}
```

**JSON Schema Versioning:**

```typescript
interface SchemaVersion {
  version: number;
  schema: object;
  migrate?: (data: any, fromVersion: number) => any;
}

class VersionedSerializer {
  private versions: Map<number, SchemaVersion> = new Map();
  private currentVersion: number = 1;

  registerVersion(version: SchemaVersion): void {
    this.versions.set(version.version, version);
    if (version.version > this.currentVersion) {
      this.currentVersion = version.version;
    }
  }

  serialize(data: any): { version: number; data: any } {
    return {
      version: this.currentVersion,
      data,
    };
  }

  deserialize(payload: { version: number; data: any }): any {
    let data = payload.data;
    let version = payload.version;

    // Migrate through versions if needed
    while (version < this.currentVersion) {
      const nextVersion = version + 1;
      const schema = this.versions.get(nextVersion);

      if (schema?.migrate) {
        data = schema.migrate(data, version);
      }

      version = nextVersion;
    }

    return data;
  }
}

// Example usage
const serializer = new VersionedSerializer();

serializer.registerVersion({
  version: 1,
  schema: { type: "object", properties: { name: { type: "string" } } },
});

serializer.registerVersion({
  version: 2,
  schema: {
    type: "object",
    properties: {
      firstName: { type: "string" },
      lastName: { type: "string" },
    },
  },
  migrate: (data, fromVersion) => {
    if (fromVersion === 1) {
      const [firstName, ...rest] = (data.name || "").split(" ");
      return {
        firstName,
        lastName: rest.join(" "),
      };
    }
    return data;
  },
});
```

### Backward/Forward Compatibility

**Compatibility Rules:**

```typescript
// Rules for maintaining compatibility
const compatibilityRules = {
  // BACKWARD COMPATIBLE (new code reads old data)
  backwardCompatible: [
    "Add optional field with default",
    "Add new enum value (not at position 0)",
    "Remove required field (treat as optional)",
    "Widen numeric type (int32 -> int64)",
    "Add new message type",
  ],

  // FORWARD COMPATIBLE (old code reads new data)
  forwardCompatible: [
    "Add optional field (old code ignores)",
    "Add new enum value (old code uses default)",
    "Old code ignores unknown fields",
  ],

  // BREAKING CHANGES (avoid!)
  breakingChanges: [
    "Change field type",
    "Change field number",
    "Remove required field",
    "Rename field (in JSON)",
    "Change field from optional to required",
  ],
};
```

**Defensive Deserialization:**

```typescript
class SafeDeserializer<T> {
  constructor(
    private schema: {
      required: string[];
      optional: string[];
      defaults: Partial<T>;
    },
  ) {}

  deserialize(json: string): T {
    let parsed: any;

    try {
      parsed = JSON.parse(json);
    } catch (e) {
      throw new DeserializationError("Invalid JSON");
    }

    if (typeof parsed !== "object" || parsed === null) {
      throw new DeserializationError("Expected object");
    }

    // Check required fields
    for (const field of this.schema.required) {
      if (!(field in parsed)) {
        throw new DeserializationError(`Missing required field: ${field}`);
      }
    }

    // Apply defaults for missing optional fields
    const result = { ...this.schema.defaults } as T;

    for (const key of [...this.schema.required, ...this.schema.optional]) {
      if (key in parsed) {
        (result as any)[key] = parsed[key];
      }
    }

    // Ignore unknown fields (forward compatibility)
    return result;
  }
}

class DeserializationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DeserializationError";
  }
}
```

**Union Types and Discriminators:**

```typescript
// Using discriminated unions for extensibility
type Event =
  | { type: "user.created"; payload: UserCreatedPayload }
  | { type: "user.updated"; payload: UserUpdatedPayload }
  | { type: "order.created"; payload: OrderCreatedPayload };

function deserializeEvent(json: string): Event | null {
  const data = JSON.parse(json);

  // Handle unknown event types gracefully
  switch (data.type) {
    case "user.created":
      return { type: "user.created", payload: data.payload };
    case "user.updated":
      return { type: "user.updated", payload: data.payload };
    case "order.created":
      return { type: "order.created", payload: data.payload };
    default:
      // Forward compatibility: ignore unknown types
      console.warn(`Unknown event type: ${data.type}`);
      return null;
  }
}
```

### Custom Serializers

**Type-Safe Serializer Framework:**

```typescript
interface Serializer<T> {
  serialize(value: T): any;
  deserialize(raw: any): T;
}

class SerializerRegistry {
  private serializers: Map<string, Serializer<any>> = new Map();

  register<T>(name: string, serializer: Serializer<T>): void {
    this.serializers.set(name, serializer);
  }

  get<T>(name: string): Serializer<T> {
    const serializer = this.serializers.get(name);
    if (!serializer) {
      throw new Error(`No serializer registered for: ${name}`);
    }
    return serializer;
  }
}

// Built-in serializers
const dateSerializer: Serializer<Date> = {
  serialize: (date) => date.toISOString(),
  deserialize: (raw) => new Date(raw),
};

const decimalSerializer: Serializer<number> = {
  serialize: (num) => num.toFixed(2),
  deserialize: (raw) => parseFloat(raw),
};

const moneySerializer: Serializer<{ amount: number; currency: string }> = {
  serialize: (money) => ({
    amount: Math.round(money.amount * 100),
    currency: money.currency,
  }),
  deserialize: (raw) => ({
    amount: raw.amount / 100,
    currency: raw.currency,
  }),
};
```

**Decorator-Based Serialization:**

```typescript
import "reflect-metadata";

const SERIALIZABLE_KEY = Symbol("serializable");
const PROPERTY_KEY = Symbol("property");

interface PropertyOptions {
  name?: string;
  serializer?: Serializer<any>;
  optional?: boolean;
  default?: any;
}

function Serializable(options?: { discriminator?: string }) {
  return function (constructor: Function) {
    Reflect.defineMetadata(SERIALIZABLE_KEY, options || {}, constructor);
  };
}

function Property(options?: PropertyOptions) {
  return function (target: any, propertyKey: string) {
    const existing = Reflect.getMetadata(PROPERTY_KEY, target) || [];
    existing.push({ key: propertyKey, options: options || {} });
    Reflect.defineMetadata(PROPERTY_KEY, existing, target);
  };
}

@Serializable()
class User {
  @Property()
  id: string;

  @Property({ name: "email_address" })
  email: string;

  @Property({ serializer: dateSerializer })
  createdAt: Date;

  @Property({ optional: true, default: [] })
  tags: string[];
}

function serialize<T>(instance: T): any {
  const prototype = Object.getPrototypeOf(instance);
  const properties = Reflect.getMetadata(PROPERTY_KEY, prototype) || [];

  const result: any = {};

  for (const { key, options } of properties) {
    const value = (instance as any)[key];
    const outputKey = options.name || key;

    if (value === undefined && options.optional) {
      continue;
    }

    if (options.serializer) {
      result[outputKey] = options.serializer.serialize(value);
    } else {
      result[outputKey] = value;
    }
  }

  return result;
}
```

### Performance Considerations

**Benchmark Comparison:**

```typescript
import Benchmark from "benchmark";
import * as msgpack from "@msgpack/msgpack";

const testData = {
  id: "user_123456789",
  email: "user@example.com",
  name: "Test User",
  age: 30,
  active: true,
  roles: ["admin", "user"],
  metadata: {
    lastLogin: "2024-12-19T00:00:00Z",
    preferences: { theme: "dark", language: "en" },
  },
};

const suite = new Benchmark.Suite();

suite
  .add("JSON.stringify", () => {
    JSON.stringify(testData);
  })
  .add("JSON.parse", () => {
    JSON.parse(JSON.stringify(testData));
  })
  .add("MessagePack encode", () => {
    msgpack.encode(testData);
  })
  .add("MessagePack decode", () => {
    msgpack.decode(msgpack.encode(testData));
  })
  .on("cycle", (event: any) => {
    console.log(String(event.target));
  })
  .run();
```

**Size Optimization:**

```typescript
// Strategies for reducing payload size

// 1. Field name shortening (with mapping)
const fieldMap = {
  userId: "u",
  firstName: "fn",
  lastName: "ln",
  emailAddress: "e",
  createdAt: "ca",
};

function compressKeys(obj: any, map: Record<string, string>): any {
  const result: any = {};
  for (const [key, value] of Object.entries(obj)) {
    const newKey = map[key] || key;
    result[newKey] =
      typeof value === "object" && value !== null
        ? compressKeys(value, map)
        : value;
  }
  return result;
}

// 2. Array-based encoding for known schemas
interface UserTuple {
  0: string; // id
  1: string; // email
  2: string; // name
  3: number; // createdAt (unix timestamp)
}

function toTuple(user: User): UserTuple {
  return [user.id, user.email, user.name, user.createdAt.getTime()];
}

function fromTuple(tuple: UserTuple): User {
  return {
    id: tuple[0],
    email: tuple[1],
    name: tuple[2],
    createdAt: new Date(tuple[3]),
  };
}

// 3. Delta encoding for updates
function createDelta(original: any, updated: any): any {
  const delta: any = {};

  for (const key of Object.keys(updated)) {
    if (JSON.stringify(original[key]) !== JSON.stringify(updated[key])) {
      delta[key] = updated[key];
    }
  }

  return delta;
}

function applyDelta(original: any, delta: any): any {
  return { ...original, ...delta };
}
```

**Streaming for Large Payloads:**

```typescript
import { createReadStream, createWriteStream } from "fs";
import { Transform } from "stream";

class JSONLineSerializer extends Transform {
  constructor() {
    super({ objectMode: true });
  }

  _transform(chunk: any, encoding: string, callback: Function): void {
    try {
      const line = JSON.stringify(chunk) + "\n";
      callback(null, line);
    } catch (error) {
      callback(error);
    }
  }
}

class JSONLineDeserializer extends Transform {
  private buffer: string = "";

  constructor() {
    super({ objectMode: true });
  }

  _transform(chunk: Buffer, encoding: string, callback: Function): void {
    this.buffer += chunk.toString();
    const lines = this.buffer.split("\n");
    this.buffer = lines.pop() || "";

    for (const line of lines) {
      if (line.trim()) {
        try {
          this.push(JSON.parse(line));
        } catch (error) {
          // Skip malformed lines
        }
      }
    }

    callback();
  }

  _flush(callback: Function): void {
    if (this.buffer.trim()) {
      try {
        this.push(JSON.parse(this.buffer));
      } catch (error) {
        // Skip malformed line
      }
    }
    callback();
  }
}
```

## Best Practices

### JSON

- Use consistent naming conventions (camelCase or snake_case)
- Always use ISO 8601 for dates
- Handle null/undefined explicitly
- Keep payloads reasonably sized
- Validate input before processing

### Protocol Buffers

- Reserve field numbers for deprecated fields
- Use optional for fields that may be absent
- Avoid changing field types
- Use well-known types for common patterns (Timestamp, Duration, Empty)
- Version your .proto files with package names (e.g., myapp.v1)
- For gRPC: design services with clear unary/streaming semantics

### Rust Serde

- Use derive macros for standard cases
- Leverage serde attributes for field renaming and control
- Implement custom Serialize/Deserialize for complex types
- Use skip_serializing_if to omit optional fields
- Choose enum tagging strategy based on JSON compatibility needs
- Support multiple formats (JSON, YAML, TOML) with minimal code

### Schema Evolution

- Plan for schema changes from the start
- Always add new fields as optional
- Never reuse field numbers or names
- Test backward/forward compatibility
- Document breaking changes
- Use versioned packages in protobuf (e.g., users.v1, users.v2)
- Implement migration logic for breaking changes

### Performance

- Choose format based on use case (JSON for debug, binary for perf)
- Use streaming for large payloads
- Consider compression for large JSON
- Profile serialization in your specific context
- Cache serializers/deserializers
- For Rust: bincode is fastest, MessagePack balances size and speed

## Examples

### Complete Serialization Layer

```typescript
// Generic serialization layer supporting multiple formats
interface SerializationFormat {
  name: string;
  contentType: string;
  encode<T>(data: T): Buffer;
  decode<T>(buffer: Buffer): T;
}

const jsonFormat: SerializationFormat = {
  name: "json",
  contentType: "application/json",
  encode: (data) => Buffer.from(JSON.stringify(data)),
  decode: (buffer) => JSON.parse(buffer.toString()),
};

const msgpackFormat: SerializationFormat = {
  name: "msgpack",
  contentType: "application/msgpack",
  encode: (data) => Buffer.from(msgpack.encode(data)),
  decode: (buffer) => msgpack.decode(buffer) as any,
};

class SerializationService {
  private formats: Map<string, SerializationFormat> = new Map();
  private defaultFormat: string = "json";

  constructor() {
    this.registerFormat(jsonFormat);
    this.registerFormat(msgpackFormat);
  }

  registerFormat(format: SerializationFormat): void {
    this.formats.set(format.name, format);
  }

  serialize<T>(
    data: T,
    formatName?: string,
  ): {
    buffer: Buffer;
    contentType: string;
  } {
    const format = this.formats.get(formatName || this.defaultFormat);
    if (!format) {
      throw new Error(`Unknown format: ${formatName}`);
    }

    return {
      buffer: format.encode(data),
      contentType: format.contentType,
    };
  }

  deserialize<T>(buffer: Buffer, contentType: string): T {
    const format = Array.from(this.formats.values()).find(
      (f) => f.contentType === contentType,
    );

    if (!format) {
      throw new Error(`Unknown content type: ${contentType}`);
    }

    return format.decode(buffer);
  }

  // Content negotiation helper
  negotiate(acceptHeader: string): SerializationFormat {
    const accepted = acceptHeader.split(",").map((s) => s.trim().split(";")[0]);

    for (const type of accepted) {
      const format = Array.from(this.formats.values()).find(
        (f) => f.contentType === type,
      );
      if (format) return format;
    }

    return this.formats.get(this.defaultFormat)!;
  }
}

// Express middleware
function serializationMiddleware(service: SerializationService) {
  return (
    req: express.Request,
    res: express.Response,
    next: express.NextFunction,
  ) => {
    // Determine response format
    const format = service.negotiate(req.headers.accept || "application/json");

    // Override res.json
    const originalJson = res.json.bind(res);
    res.json = (data: any) => {
      const { buffer, contentType } = service.serialize(data, format.name);
      res.contentType(contentType);
      res.send(buffer);
      return res;
    };

    next();
  };
}
```
