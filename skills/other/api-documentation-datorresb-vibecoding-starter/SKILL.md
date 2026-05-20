---
name: api-documentation
description: Comprehensive guidance for documenting REST, GraphQL, gRPC, and WebSocket APIs. Use when creating API endpoints, updating existing APIs, preparing public API releases, or documenting external integrations.
---

# API Documentation Skill

## Core Principle

**APIs are products. Documentation is the user interface.**

Your API might be technically perfect, but if developers can't figure out how to use it, it's worthless. Good API documentation:
- **Enables self-service** (developers don't need to ask questions)
- **Shows real examples** (copy-paste ready code)
- **Documents the "why"** not just the "what"
- **Stays synchronized** with implementation

---

## When to Use This Skill

Use this skill when:
- Creating new API endpoints or services
- Updating existing API interfaces
- Preparing APIs for public release
- Enabling external teams to integrate with your API
- Versioning or deprecating API endpoints
- Writing SDK or client library documentation
- Documenting authentication and authorization flows
- Creating interactive API explorers

---

## API Documentation Types

### 1. REST API Documentation

**Purpose:** Document HTTP-based APIs following REST principles

**Essential components:**
- Base URL and versioning strategy
- Authentication mechanisms
- Resource endpoints (paths)
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Request parameters (path, query, body)
- Response formats and status codes
- Error handling and status codes
- Rate limiting and pagination
- Example requests and responses

**Example:**
```markdown
## Get User by ID

Retrieve a single user's details by their unique identifier.

### Endpoint

    GET /api/v1/users/{userId}

### Path Parameters

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| userId    | string | Yes      | Unique user identifier|

### Query Parameters

| Parameter | Type    | Required | Description                    |
|-----------|---------|----------|--------------------------------|
| include   | string  | No       | Comma-separated related data   |
|           |         |          | Options: `profile`, `settings` |

### Headers

    Authorization: Bearer <token>
    Accept: application/json

### Response 200 (Success)

```json
{
  "id": "usr_123abc",
  "email": "john@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z",
  "profile": {
    "bio": "Software developer",
    "avatar_url": "https://example.com/avatar.jpg"
  }
}
```

### Response 404 (Not Found)

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user found with ID: usr_123abc"
  }
}
```

### Response 401 (Unauthorized)

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Valid authentication token required"
  }
}
```

### Example Request

```bash
curl -X GET "https://api.example.com/api/v1/users/usr_123abc?include=profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Accept: application/json"
```

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/json"
}

response = requests.get(
    "https://api.example.com/api/v1/users/usr_123abc",
    params={"include": "profile"},
    headers=headers
)

user = response.json()
print(f"User: {user['name']}")
```

```javascript
const response = await fetch(
  'https://api.example.com/api/v1/users/usr_123abc?include=profile',
  {
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Accept': 'application/json'
    }
  }
);

const user = await response.json();
console.log(`User: ${user.name}`);
```
```

---

### 2. GraphQL API Documentation

**Purpose:** Document GraphQL schemas, queries, mutations, and subscriptions

**Essential components:**
- Schema definitions (types, interfaces, unions)
- Query documentation with arguments
- Mutation documentation with input types
- Subscription patterns
- Authentication and authorization
- Error handling patterns
- Pagination strategies (cursor-based, offset)
- Example queries with variables

**Example:**
```markdown
## User Queries

### getUser

Fetch a single user by ID with optional related data.

#### Schema Definition

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  profile: Profile
  posts(first: Int, after: String): PostConnection
}

type Profile {
  bio: String
  avatarUrl: String
  location: String
}

type Query {
  getUser(id: ID!, includeProfile: Boolean): User
}
```

#### Arguments

| Argument       | Type    | Required | Description                |
|----------------|---------|----------|----------------------------|
| id             | ID      | Yes      | User's unique identifier   |
| includeProfile | Boolean | No       | Include profile data       |

#### Example Query

```graphql
query GetUserWithProfile($userId: ID!) {
  getUser(id: $userId, includeProfile: true) {
    id
    email
    name
    createdAt
    profile {
      bio
      avatarUrl
      location
    }
  }
}
```

#### Variables

```json
{
  "userId": "usr_123abc"
}
```

#### Response

```json
{
  "data": {
    "getUser": {
      "id": "usr_123abc",
      "email": "john@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-15T10:30:00Z",
      "profile": {
        "bio": "Software developer",
        "avatarUrl": "https://example.com/avatar.jpg",
        "location": "San Francisco, CA"
      }
    }
  }
}
```

#### Error Response

```json
{
  "errors": [
    {
      "message": "User not found",
      "locations": [{"line": 2, "column": 3}],
      "path": ["getUser"],
      "extensions": {
        "code": "USER_NOT_FOUND",
        "userId": "usr_123abc"
      }
    }
  ],
  "data": {
    "getUser": null
  }
}
```

#### Client Code Examples

```javascript
// Using Apollo Client
import { gql, useQuery } from '@apollo/client';

const GET_USER = gql`
  query GetUserWithProfile($userId: ID!) {
    getUser(id: $userId, includeProfile: true) {
      id
      name
      email
      profile {
        bio
        avatarUrl
      }
    }
  }
`;

function UserProfile({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { userId }
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>{data.getUser.name}</h1>
      <p>{data.getUser.profile.bio}</p>
    </div>
  );
}
```

```python
# Using gql library
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url='https://api.example.com/graphql',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
    query GetUserWithProfile($userId: ID!) {
        getUser(id: $userId, includeProfile: true) {
            id
            name
            email
            profile {
                bio
                avatarUrl
            }
        }
    }
""")

result = client.execute(query, variable_values={"userId": "usr_123abc"})
print(f"User: {result['getUser']['name']}")
```
```

### GraphQL Mutations

```markdown
## createUser

Create a new user account.

#### Schema Definition

```graphql
input CreateUserInput {
  email: String!
  name: String!
  password: String!
  profile: ProfileInput
}

input ProfileInput {
  bio: String
  location: String
}

type CreateUserPayload {
  user: User
  token: String!
  errors: [UserError!]
}

type UserError {
  field: String!
  message: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}
```

#### Example Mutation

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      email
      name
    }
    token
    errors {
      field
      message
    }
  }
}
```

#### Variables

```json
{
  "input": {
    "email": "jane@example.com",
    "name": "Jane Smith",
    "password": "SecurePass123!",
    "profile": {
      "bio": "Product designer",
      "location": "New York, NY"
    }
  }
}
```

#### Success Response

```json
{
  "data": {
    "createUser": {
      "user": {
        "id": "usr_456def",
        "email": "jane@example.com",
        "name": "Jane Smith"
      },
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "errors": []
    }
  }
}
```

#### Validation Error Response

```json
{
  "data": {
    "createUser": {
      "user": null,
      "token": null,
      "errors": [
        {
          "field": "email",
          "message": "Email already registered"
        },
        {
          "field": "password",
          "message": "Password must be at least 8 characters"
        }
      ]
    }
  }
}
```
```

---

### 3. gRPC API Documentation

**Purpose:** Document Protocol Buffer based APIs

**Essential components:**
- Service definitions
- Message types (requests/responses)
- Field types and constraints
- Error codes and handling
- Streaming patterns (unary, server stream, client stream, bidirectional)
- Example implementations in multiple languages

**Example:**
```markdown
## User Service

Service for managing user accounts and profiles.

### Proto Definition

```protobuf
syntax = "proto3";

package user.v1;

service UserService {
  // Get a user by ID
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  // Create a new user
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);

  // Stream user updates (server streaming)
  rpc WatchUser(WatchUserRequest) returns (stream UserUpdate);
}

message GetUserRequest {
  string user_id = 1;  // Required: User identifier
  bool include_profile = 2;  // Optional: Include profile data
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  int64 created_at = 4;  // Unix timestamp
  Profile profile = 5;  // Optional
}

message Profile {
  string bio = 1;
  string avatar_url = 2;
  string location = 3;
}

message UserUpdate {
  User user = 1;
  UpdateType type = 2;

  enum UpdateType {
    UPDATED = 0;
    DELETED = 1;
  }
}
```

### GetUser RPC

Retrieve a single user by their unique identifier.

#### Request

```go
req := &userpb.GetUserRequest{
    UserId:         "usr_123abc",
    IncludeProfile: true,
}
```

#### Response (Success)

```go
resp := &userpb.GetUserResponse{
    User: &userpb.User{
        Id:    "usr_123abc",
        Email: "john@example.com",
        Name:  "John Doe",
        CreatedAt: 1705315800,  // Unix timestamp
        Profile: &userpb.Profile{
            Bio:       "Software developer",
            AvatarUrl: "https://example.com/avatar.jpg",
            Location:  "San Francisco, CA",
        },
    },
}
```

#### Error Handling

gRPC uses standard status codes:

| Code           | Description                      | When to Use                |
|----------------|----------------------------------|----------------------------|
| OK             | Success                          | Request completed          |
| NOT_FOUND      | Resource not found               | User ID doesn't exist      |
| INVALID_ARG    | Invalid parameters               | Malformed user ID          |
| UNAUTHENTICATED| Missing/invalid credentials      | No auth token provided     |
| PERMISSION_DENIED| Insufficient permissions        | Can't access user          |
| INTERNAL       | Server error                     | Unexpected failures        |

#### Example Implementations

**Go Client:**

```go
package main

import (
    "context"
    "log"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"
    userpb "example.com/proto/user/v1"
)

func main() {
    // Setup TLS credentials
    creds, err := credentials.NewClientTLSFromFile("cert.pem", "")
    if err != nil {
        log.Fatal(err)
    }

    // Connect to server
    conn, err := grpc.Dial(
        "api.example.com:443",
        grpc.WithTransportCredentials(creds),
    )
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // Create client
    client := userpb.NewUserServiceClient(conn)

    // Make request
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    resp, err := client.GetUser(ctx, &userpb.GetUserRequest{
        UserId:         "usr_123abc",
        IncludeProfile: true,
    })
    if err != nil {
        log.Fatalf("GetUser failed: %v", err)
    }

    log.Printf("User: %s (%s)", resp.User.Name, resp.User.Email)
}
```

**Python Client:**

```python
import grpc
from user.v1 import user_pb2, user_pb2_grpc

# Setup channel with credentials
credentials = grpc.ssl_channel_credentials(
    open('cert.pem', 'rb').read()
)
channel = grpc.secure_channel('api.example.com:443', credentials)

# Create client stub
client = user_pb2_grpc.UserServiceStub(channel)

# Make request
try:
    response = client.GetUser(
        user_pb2.GetUserRequest(
            user_id='usr_123abc',
            include_profile=True
        ),
        timeout=5.0
    )
    print(f"User: {response.user.name} ({response.user.email})")
except grpc.RpcError as e:
    print(f"Error: {e.code()} - {e.details()}")
```
```

---

### 4. WebSocket API Documentation

**Purpose:** Document real-time, bidirectional communication APIs

**Essential components:**
- Connection endpoint and protocol
- Authentication handshake
- Message formats (JSON, binary)
- Event types (client-to-server, server-to-client)
- Connection lifecycle (connect, disconnect, reconnect)
- Error handling and recovery
- Rate limiting and backpressure

**Example:**
```markdown
## Real-Time Notifications API

WebSocket API for receiving real-time user notifications.

### Connection

**Endpoint:** `wss://api.example.com/v1/notifications`

**Protocol:** WebSocket over TLS

### Authentication

Include JWT token in connection query parameter or initial message.

#### Option 1: Query Parameter

```javascript
const ws = new WebSocket(
  'wss://api.example.com/v1/notifications?token=YOUR_JWT_TOKEN'
);
```

#### Option 2: Initial Message

```javascript
const ws = new WebSocket('wss://api.example.com/v1/notifications');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'YOUR_JWT_TOKEN'
  }));
};
```

### Message Format

All messages are JSON with the following structure:

```json
{
  "type": "string",
  "id": "string",
  "timestamp": "ISO8601",
  "data": {}
}
```

### Client-to-Server Messages

#### Subscribe to Notifications

```json
{
  "type": "subscribe",
  "id": "msg_001",
  "data": {
    "channels": ["user_updates", "mentions"]
  }
}
```

#### Unsubscribe

```json
{
  "type": "unsubscribe",
  "id": "msg_002",
  "data": {
    "channels": ["mentions"]
  }
}
```

#### Ping (Keepalive)

```json
{
  "type": "ping",
  "id": "msg_003"
}
```

### Server-to-Client Messages

#### Authentication Success

```json
{
  "type": "auth_success",
  "id": "srv_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "user_id": "usr_123abc",
    "session_id": "sess_xyz789"
  }
}
```

#### Notification Event

```json
{
  "type": "notification",
  "id": "notif_456",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "notification_id": "n_789",
    "category": "mention",
    "title": "You were mentioned in a comment",
    "body": "John Doe mentioned you in 'Project Alpha'",
    "action_url": "/projects/alpha#comment-123",
    "read": false
  }
}
```

#### Pong (Keepalive Response)

```json
{
  "type": "pong",
  "id": "srv_002",
  "timestamp": "2024-01-15T10:30:01Z"
}
```

#### Error

```json
{
  "type": "error",
  "id": "srv_003",
  "timestamp": "2024-01-15T10:30:02Z",
  "data": {
    "code": "INVALID_CHANNEL",
    "message": "Channel 'unknown_channel' does not exist",
    "retry_after": null
  }
}
```

### Connection Lifecycle

#### 1. Connect

```javascript
const ws = new WebSocket('wss://api.example.com/v1/notifications');

ws.onopen = () => {
  console.log('Connected to notification service');

  // Authenticate
  ws.send(JSON.stringify({
    type: 'auth',
    token: localStorage.getItem('jwt_token')
  }));
};
```

#### 2. Handle Messages

```javascript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case 'auth_success':
      console.log('Authenticated:', message.data.user_id);
      // Subscribe to channels
      ws.send(JSON.stringify({
        type: 'subscribe',
        data: { channels: ['user_updates', 'mentions'] }
      }));
      break;

    case 'notification':
      console.log('New notification:', message.data.title);
      displayNotification(message.data);
      break;

    case 'error':
      console.error('Error:', message.data.message);
      break;
  }
};
```

#### 3. Handle Errors

```javascript
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

#### 4. Handle Disconnection

```javascript
ws.onclose = (event) => {
  console.log('Disconnected:', event.code, event.reason);

  // Implement reconnection logic
  if (event.code !== 1000) {  // 1000 = normal closure
    setTimeout(() => {
      console.log('Reconnecting...');
      connectWebSocket();
    }, 5000);
  }
};
```

### Error Codes

| Code | Name               | Description                          |
|------|--------------------|--------------------------------------|
| 1000 | Normal Closure     | Connection closed normally           |
| 1001 | Going Away         | Server shutting down                 |
| 1008 | Policy Violation   | Authentication failed                |
| 1011 | Internal Error     | Unexpected server error              |
| 4000 | Invalid Token      | JWT token invalid or expired         |
| 4001 | Rate Limited       | Too many messages sent               |
| 4002 | Invalid Message    | Malformed JSON or unknown type       |

### Rate Limiting

- Maximum 100 messages per minute per connection
- Exceeded limits result in error message and potential disconnection
- Reconnection allowed after 1 minute cooldown

### Keepalive

- Server sends ping every 30 seconds if no activity
- Client should respond with pong within 10 seconds
- Connection closed if 3 consecutive pings timeout
```

---

## Essential API Documentation Components

### 1. Overview and Introduction

Start with the big picture:

```markdown
# MyAPI Documentation

## Overview

MyAPI is a RESTful service for managing user accounts and content. It provides
endpoints for authentication, user management, content creation, and real-time
notifications.

## Base URL

Production: `https://api.example.com/v1`
Staging: `https://staging-api.example.com/v1`

## API Version

Current version: **v1** (Released: 2024-01-15)

## Supported Formats

- Request: JSON (`application/json`)
- Response: JSON (`application/json`)
- Encoding: UTF-8

## Rate Limits

- Authenticated: 5000 requests/hour
- Unauthenticated: 100 requests/hour

## Support

- Email: api-support@example.com
- Discord: https://discord.gg/example
- Status: https://status.example.com
```

---

### 2. Authentication Documentation

Document every authentication method thoroughly:

```markdown
## Authentication

MyAPI uses Bearer token authentication with JWT tokens.

### Obtaining a Token

**Endpoint:** `POST /auth/login`

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "fdb8fdbecf1d03ce5e6125c067733c0d51de209c",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Using the Token

Include the access token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://api.example.com/v1/users/me
```

### Token Refresh

**Endpoint:** `POST /auth/refresh`

```json
{
  "refresh_token": "fdb8fdbecf1d03ce5e6125c067733c0d51de209c"
}
```

### Security Best Practices

- Store tokens securely (never in localStorage for sensitive apps)
- Use HTTPS for all API calls
- Refresh tokens before expiration
- Revoke tokens on logout
```

---

### 3. Error Handling Documentation

Consistent error format is critical:

```markdown
## Error Responses

All errors follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "additional context"
    },
    "request_id": "req_abc123",
    "documentation_url": "https://docs.example.com/errors/ERROR_CODE"
  }
}
```

### HTTP Status Codes

| Code | Meaning              | When Used                           |
|------|----------------------|-------------------------------------|
| 200  | OK                   | Successful GET, PUT, PATCH          |
| 201  | Created              | Successful POST (resource created)  |
| 204  | No Content           | Successful DELETE                   |
| 400  | Bad Request          | Invalid parameters or body          |
| 401  | Unauthorized         | Missing or invalid authentication   |
| 403  | Forbidden            | Authenticated but not authorized    |
| 404  | Not Found            | Resource doesn't exist              |
| 409  | Conflict             | Resource conflict (duplicate, etc.) |
| 422  | Unprocessable Entity | Validation failed                   |
| 429  | Too Many Requests    | Rate limit exceeded                 |
| 500  | Internal Server Error| Server error                        |
| 503  | Service Unavailable  | Temporary downtime                  |

### Common Error Codes

#### VALIDATION_ERROR (400)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "email": "Invalid email format",
      "age": "Must be at least 18"
    }
  }
}
```

#### RESOURCE_NOT_FOUND (404)

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "details": {
      "resource_type": "user",
      "resource_id": "usr_123abc"
    }
  }
}
```

#### RATE_LIMIT_EXCEEDED (429)

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "details": {
      "limit": 5000,
      "window": "1 hour",
      "retry_after": 3600
    }
  }
}
```

**Headers:**
```
Retry-After: 3600
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705332600
```
```

---

### 4. Pagination Documentation

```markdown
## Pagination

List endpoints return paginated results.

### Cursor-Based Pagination (Recommended)

**Request:**

```bash
GET /api/v1/users?limit=20&cursor=eyJpZCI6MTIzfQ
```

**Parameters:**

| Parameter | Type   | Default | Description                      |
|-----------|--------|---------|----------------------------------|
| limit     | int    | 20      | Items per page (max: 100)        |
| cursor    | string | null    | Pagination cursor from previous  |

**Response:**

```json
{
  "data": [
    { "id": "usr_001", "name": "User 1" },
    { "id": "usr_002", "name": "User 2" }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6MTI1fQ",
    "has_more": true,
    "total_count": null
  }
}
```

**Usage:**

```python
def fetch_all_users():
    users = []
    cursor = None

    while True:
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor

        response = requests.get('https://api.example.com/v1/users', params=params)
        data = response.json()

        users.extend(data['data'])

        if not data['pagination']['has_more']:
            break

        cursor = data['pagination']['next_cursor']

    return users
```
```

---

### 5. Versioning Documentation

```markdown
## API Versioning

MyAPI uses URL-based versioning.

### Current Version: v1

All endpoints are prefixed with `/v1`:

```
https://api.example.com/v1/users
```

### Version Lifecycle

| Version | Status     | EOL Date   | Notes                    |
|---------|------------|------------|--------------------------|
| v1      | Current    | -          | Latest stable version    |
| v0      | Deprecated | 2024-06-30 | Migrate to v1            |

### Breaking Changes

We consider these changes as breaking:
- Removing or renaming fields
- Changing field types
- Removing endpoints
- Changing authentication
- Changing status code meanings

### Non-Breaking Changes

These changes may occur in current version:
- Adding new endpoints
- Adding new optional fields
- Adding new query parameters
- Deprecation warnings (6 months notice)

### Migration Guide: v0 → v1

**Authentication Changes:**

v0:
```bash
curl -H "X-API-Key: YOUR_KEY" https://api.example.com/users
```

v1:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/v1/users
```

**Response Format Changes:**

v0:
```json
{
  "users": [...],
  "page": 1,
  "total": 100
}
```

v1:
```json
{
  "data": [...],
  "pagination": {
    "cursor": "...",
    "has_more": true
  }
}
```
```

---

### 6. Rate Limiting Documentation

```markdown
## Rate Limiting

API requests are rate-limited to ensure fair usage.

### Limits

| Authentication | Limit               | Window  |
|----------------|---------------------|---------|
| Authenticated  | 5000 requests       | 1 hour  |
| Unauthenticated| 100 requests        | 1 hour  |
| Burst          | 100 requests        | 1 minute|

### Rate Limit Headers

Every response includes rate limit information:

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4850
X-RateLimit-Reset: 1705332600
```

| Header                  | Description                          |
|-------------------------|--------------------------------------|
| X-RateLimit-Limit       | Maximum requests in window           |
| X-RateLimit-Remaining   | Requests remaining in current window |
| X-RateLimit-Reset       | Unix timestamp when limit resets     |

### Handling Rate Limits

```python
import time
import requests

def api_call_with_retry(url, headers):
    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            # Rate limited
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            wait_seconds = reset_time - int(time.time())

            print(f"Rate limited. Waiting {wait_seconds} seconds...")
            time.sleep(max(wait_seconds, 1))
            continue

        return response
```

### Rate Limit Strategies

**Exponential Backoff:**

```javascript
async function apiCallWithBackoff(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url);

    if (response.status === 429) {
      const resetTime = response.headers.get('X-RateLimit-Reset');
      const waitMs = (resetTime * 1000) - Date.now();

      await new Promise(resolve => setTimeout(resolve, waitMs));
      continue;
    }

    return response;
  }

  throw new Error('Max retries exceeded');
}
```
```

---

## Documentation Formats and Tools

### 1. OpenAPI/Swagger (REST APIs)

**Purpose:** Machine-readable API specification

**Complete OpenAPI 3.x Example:**

```yaml
openapi: 3.0.3
info:
  title: MyAPI
  description: User and content management API
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - bearerAuth: []

paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      description: Retrieve detailed information about a specific user
      operationId: getUser
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          description: Unique user identifier
          schema:
            type: string
            pattern: '^usr_[a-zA-Z0-9]+$'
            example: usr_123abc
        - name: include
          in: query
          required: false
          description: Comma-separated list of related data to include
          schema:
            type: string
            enum: [profile, settings, posts]
          example: profile
      responses:
        '200':
          description: User found successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              examples:
                withProfile:
                  summary: User with profile
                  value:
                    id: usr_123abc
                    email: john@example.com
                    name: John Doe
                    created_at: '2024-01-15T10:30:00Z'
                    profile:
                      bio: Software developer
                      avatar_url: https://example.com/avatar.jpg
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '429':
          $ref: '#/components/responses/RateLimitError'

  /users:
    post:
      summary: Create new user
      description: Register a new user account
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              basic:
                summary: Basic user registration
                value:
                  email: jane@example.com
                  name: Jane Smith
                  password: SecurePass123!
      responses:
        '201':
          description: User created successfully
          headers:
            Location:
              description: URL of the created user
              schema:
                type: string
                format: uri
                example: /v1/users/usr_456def
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          description: User already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error:
                  code: USER_ALREADY_EXISTS
                  message: Email already registered

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login

  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - created_at
      properties:
        id:
          type: string
          pattern: '^usr_[a-zA-Z0-9]+$'
          example: usr_123abc
        email:
          type: string
          format: email
          example: john@example.com
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: John Doe
        created_at:
          type: string
          format: date-time
          example: '2024-01-15T10:30:00Z'
        profile:
          $ref: '#/components/schemas/Profile'

    Profile:
      type: object
      properties:
        bio:
          type: string
          maxLength: 500
          example: Software developer
        avatar_url:
          type: string
          format: uri
          example: https://example.com/avatar.jpg
        location:
          type: string
          example: San Francisco, CA

    CreateUserRequest:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8
          maxLength: 128
          format: password
          description: Must contain uppercase, lowercase, number, and symbol

    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              example: RESOURCE_NOT_FOUND
            message:
              type: string
              example: Resource not found
            details:
              type: object
              additionalProperties: true
            request_id:
              type: string
              example: req_abc123

  responses:
    UnauthorizedError:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: UNAUTHORIZED
              message: Valid authentication token required

    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: RESOURCE_NOT_FOUND
              message: Resource not found

    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: VALIDATION_ERROR
              message: Request validation failed
              details:
                email: Invalid email format
                password: Must be at least 8 characters

    RateLimitError:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Maximum requests per window
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Requests remaining
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Unix timestamp when limit resets
        Retry-After:
          schema:
            type: integer
          description: Seconds to wait before retry
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

**Generating OpenAPI Spec from Code:**

```python
# Using FastAPI (Python)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MyAPI",
    description="User and content management API",
    version="1.0.0"
)

class User(BaseModel):
    id: str
    email: str
    name: str

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get user by ID"""
    # Auto-generates OpenAPI spec
    pass

# Access at: http://localhost:8000/docs
```

---

### 2. GraphQL Documentation Tools

**GraphQL Playground / GraphiQL:**

```javascript
// Setup GraphQL Playground
const { ApolloServer } = require('apollo-server');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  playground: {
    settings: {
      'editor.theme': 'light',
      'editor.reuseHeaders': true,
    },
  },
  introspection: true,  // Enable schema introspection
});

// Access at: http://localhost:4000/graphql
```

**Schema Documentation Comments:**

```graphql
"""
Represents a user account in the system.
"""
type User {
  """
  Unique identifier for the user.
  Format: usr_[a-zA-Z0-9]+
  """
  id: ID!

  """
  User's email address.
  Must be unique across all users.
  """
  email: String!

  """
  Display name for the user.
  Max length: 100 characters
  """
  name: String!
}

"""
Query operations for users.
"""
type Query {
  """
  Retrieve a single user by their unique identifier.

  Returns null if user not found.
  Requires authentication.
  """
  getUser(
    """User's unique identifier"""
    id: ID!

    """Whether to include the user's profile data"""
    includeProfile: Boolean = false
  ): User
}
```

---

### 3. API Documentation Tools

**Swagger UI:**

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "/openapi.yaml",
      dom_id: '#swagger-ui',
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout"
    });
  </script>
</body>
</html>
```

**Redoc:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
</head>
<body>
  <redoc spec-url="/openapi.yaml"></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

**Stoplight:**

- Visual API designer
- Automatic mock servers
- API style guides
- Collaborative editing
- Hosted documentation

**Postman Collections:**

```json
{
  "info": {
    "name": "MyAPI",
    "description": "User and content management API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Users",
      "item": [
        {
          "name": "Get User",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/users/:userId?include=profile",
              "host": ["{{base_url}}"],
              "path": ["users", ":userId"],
              "query": [
                {
                  "key": "include",
                  "value": "profile"
                }
              ],
              "variable": [
                {
                  "key": "userId",
                  "value": "usr_123abc"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

---

## API Documentation Best Practices

### 1. Provide Runnable Examples

❌ **Bad:**
```markdown
Call the API with the user ID.
```

✅ **Good:**
```markdown
**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/users/usr_123abc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**

```json
{
  "id": "usr_123abc",
  "name": "John Doe",
  "email": "john@example.com"
}
```
```

---

### 2. Show Error Scenarios

❌ **Bad:**
```markdown
Returns 404 if not found.
```

✅ **Good:**
```markdown
**Error Response (404 Not Found):**

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user found with ID: usr_123abc",
    "details": {
      "resource_type": "user",
      "resource_id": "usr_123abc"
    }
  }
}
```

**Handling the Error:**

```python
response = requests.get(f"https://api.example.com/v1/users/{user_id}")

if response.status_code == 404:
    error = response.json()['error']
    print(f"User not found: {error['message']}")
    # Fallback logic here
```
```

---

### 3. Include Multiple Language Examples

Provide examples in popular languages:

```markdown
**Python:**

```python
import requests

response = requests.get(
    "https://api.example.com/v1/users/usr_123abc",
    headers={"Authorization": f"Bearer {token}"}
)
user = response.json()
```

**JavaScript:**

```javascript
const response = await fetch(
  'https://api.example.com/v1/users/usr_123abc',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);
const user = await response.json();
```

**Go:**

```go
req, _ := http.NewRequest("GET",
    "https://api.example.com/v1/users/usr_123abc", nil)
req.Header.Set("Authorization", "Bearer "+token)

resp, err := http.DefaultClient.Do(req)
defer resp.Body.Close()

var user User
json.NewDecoder(resp.Body).Decode(&user)
```

**cURL:**

```bash
curl -X GET "https://api.example.com/v1/users/usr_123abc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
```

---

### 4. Document Rate Limits Clearly

```markdown
## Rate Limiting

Your requests are limited to **5000 per hour**.

Check remaining quota:
```bash
curl -I https://api.example.com/v1/users
```

Response headers:
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4850
X-RateLimit-Reset: 1705332600
```

If rate limited:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests"
  }
}
```

Wait until `X-RateLimit-Reset` timestamp before retrying.
```

---

### 5. Keep Documentation Synchronized with Code

**Strategies:**

- **Generate docs from code** (FastAPI, Swagger annotations)
- **Test examples in CI** (ensure they work)
- **Version docs with API** (v1 docs match v1 code)
- **Review docs in PRs** (docs changes required for API changes)
- **Automate OpenAPI generation** (from code annotations)

**Example CI Check:**

```yaml
# .github/workflows/docs.yml
name: Validate Documentation

on: [pull_request]

jobs:
  test-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test API Examples
        run: |
          # Extract code examples from docs
          python scripts/extract_examples.py docs/

          # Run examples against staging API
          python scripts/test_examples.py --api-url https://staging-api.example.com
```

---

### 6. Provide SDKs and Client Libraries

Document language-specific clients:

```markdown
## Official SDKs

### Python

```bash
pip install myapi-client
```

```python
from myapi import Client

client = Client(api_key="YOUR_API_KEY")
user = client.users.get("usr_123abc")
print(user.name)
```

### JavaScript

```bash
npm install @myapi/client
```

```javascript
import { MyAPIClient } from '@myapi/client';

const client = new MyAPIClient({ apiKey: 'YOUR_API_KEY' });
const user = await client.users.get('usr_123abc');
console.log(user.name);
```
```

---

## Quick Reference Checklist

Before publishing API documentation:

- [ ] **Overview** — Purpose, base URL, version documented
- [ ] **Authentication** — All auth methods explained with examples
- [ ] **Endpoints** — Every endpoint documented
- [ ] **Parameters** — All parameters described with types and constraints
- [ ] **Examples** — Request/response examples for each endpoint
- [ ] **Multiple Languages** — Examples in Python, JavaScript, cURL minimum
- [ ] **Error Handling** — All error codes and responses documented
- [ ] **Rate Limiting** — Limits, headers, and handling documented
- [ ] **Pagination** — Strategy documented with examples
- [ ] **Versioning** — Current version and migration guides
- [ ] **Status Codes** — All HTTP codes explained
- [ ] **Testing** — Examples are tested and work
- [ ] **Interactive Docs** — Swagger/GraphQL Playground available
- [ ] **Search** — Documentation is searchable
- [ ] **Changelog** — API changes documented

---

## Integration with Other Skills

### With Technical Writing

- Apply technical writing principles to API docs
- Use active voice, specific language
- Show don't tell (examples over descriptions)
- Progressive disclosure (essentials first)

### With Code Review

- Review API documentation in pull requests
- Ensure breaking changes are documented
- Verify examples are accurate
- Check that OpenAPI spec is updated

### With Documentation Writing

- Follow documentation standards
- Maintain consistent structure
- Keep docs in version control
- Update docs with code changes

### With Testing Strategy

- Test API examples in CI/CD
- Validate OpenAPI specs automatically
- Generate API tests from documentation
- Contract testing (Pact, Spring Cloud Contract)

---

**Remember:** Your API is only as good as its documentation. Developers will judge your API by how easy it is to get started. Invest in comprehensive, accurate, example-rich documentation. Test your examples. Keep docs synchronized with code. Make documentation a first-class citizen in your development process.
