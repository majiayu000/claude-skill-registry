---
name: robotframework-restinstance-skill
description: Guide AI agents in creating REST API tests using RESTinstance library. Use when building API tests with JSON Schema validation, built-in assertions, response field validation, and OpenAPI spec integration.
---

# RESTinstance Library Skill

## Quick Reference

RESTinstance is a REST API testing library with built-in JSON validation, schema support, and OpenAPI/Swagger spec integration. It provides a fluent interface for API testing with automatic response validation.

## Installation

```bash
pip install RESTinstance
```

## Library Import

```robotframework
*** Settings ***
Library    REST    ${API_URL}
```

## Key Differentiators from RequestsLibrary

| Feature | RESTinstance | RequestsLibrary |
|---------|--------------|-----------------|
| Built-in assertions | Yes | No (use RF assertions) |
| JSON Schema validation | Yes | No (need JSONLibrary) |
| OpenAPI/Swagger support | Yes | No |
| Response type validation | Yes (String, Integer, etc.) | Manual |
| State management | Automatic instance tracking | Session-based |

## Basic Usage

### Simple GET Request

```robotframework
GET    /users/1
Integer    response status    200
String     response body name    John
Integer    response body id    1
```

### POST with JSON Body

```robotframework
POST    /users    {"name": "John", "email": "john@test.com"}
Integer    response status    201
Integer    response body id
String     response body name    John
```

### Complete CRUD Example

```robotframework
*** Test Cases ***
CRUD User Lifecycle
    # Create
    POST    /users    {"name": "John"}
    Integer    response status    201
    ${id}=    Integer    response body id

    # Read
    GET    /users/${id}
    Integer    response status    200
    String    response body name    John

    # Update
    PUT    /users/${id}    {"name": "John Updated"}
    Integer    response status    200
    String    response body name    John Updated

    # Delete
    DELETE    /users/${id}
    Integer    response status    204
```

## Core Keywords Quick Reference

### HTTP Methods

| Keyword | Usage | Description |
|---------|-------|-------------|
| `GET` | `GET /endpoint` | GET request |
| `POST` | `POST /endpoint {"json": "body"}` | POST with JSON |
| `PUT` | `PUT /endpoint {"json": "body"}` | Replace resource |
| `PATCH` | `PATCH /endpoint {"json": "body"}` | Partial update |
| `DELETE` | `DELETE /endpoint` | Delete resource |
| `HEAD` | `HEAD /endpoint` | Headers only |
| `OPTIONS` | `OPTIONS /endpoint` | Get allowed methods |

### Response Validation Keywords

| Keyword | Usage | Description |
|---------|-------|-------------|
| `Integer` | `Integer response status 200` | Validate integer value |
| `String` | `String response body name John` | Validate string value |
| `Number` | `Number response body price 19.99` | Validate float/number |
| `Boolean` | `Boolean response body active true` | Validate boolean |
| `Null` | `Null response body deleted_at` | Validate null value |
| `Array` | `Array response body items` | Validate array type |
| `Object` | `Object response body profile` | Validate object type |
| `Output` | `Output response body` | Log value (must exist) |
| `Missing` | `Missing response body error` | Validate field absent |

## Response Validation

### Status Code

```robotframework
GET    /users/1
Integer    response status    200

POST    /users    {"name": "Test"}
Integer    response status    201

DELETE    /users/1
Integer    response status    204
```

### Body Fields

```robotframework
GET    /users/1

# Validate type only (any value)
String     response body name
Integer    response body id
Boolean    response body active

# Validate type AND value
String     response body name    John
Integer    response body age     30
Boolean    response body active  true
```

### Nested Fields

```robotframework
# Response: {"user": {"profile": {"name": "John"}}}
GET    /users/1
String    response body user profile name    John
Integer   response body user id              1
```

### Array Access

```robotframework
# Response: {"items": [{"id": 1}, {"id": 2}]}
GET    /items
Integer    response body items 0 id    1
Integer    response body items 1 id    2
String     response body items 0 name
```

### Field Existence

```robotframework
GET    /users/1
Output     response body id      # Field must exist (logs value)
Missing    response body error   # Field must NOT exist
```

## Headers and Authentication

### Set Headers

```robotframework
Set Headers    {"Authorization": "Bearer ${TOKEN}"}
GET    /protected
```

### Per-Request Headers

```robotframework
GET    /data    headers={"X-Custom": "value"}
```

### Basic Auth

```robotframework
${credentials}=    Evaluate    base64.b64encode(b'${USER}:${PASS}').decode()    modules=base64
Set Headers    {"Authorization": "Basic ${credentials}"}
GET    /protected
```

### Bearer Token

```robotframework
Set Headers    {"Authorization": "Bearer ${TOKEN}"}
GET    /users/me
Integer    response status    200
```

## JSON Schema Validation

### Inline Schema

```robotframework
GET    /users/1
Object    response body    {"type": "object", "required": ["id", "name"]}
```

### Schema From File

```robotframework
GET    /users/1
Output Schema    response body    ${CURDIR}/schemas/user.json
```

### Example Schema File (user.json)

```json
{
  "type": "object",
  "required": ["id", "name", "email"],
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string", "minLength": 1},
    "email": {"type": "string", "format": "email"},
    "active": {"type": "boolean"}
  }
}
```

## Pattern Matching

### Wildcard Matching

```robotframework
String    response body name    John*        # Starts with John
String    response body type    *_active     # Ends with _active
String    response body id      *abc*        # Contains abc
```

### Regex Matching

```robotframework
String    response body email    /^[\\w.-]+@[\\w.-]+\\.\\w+$/
String    response body phone    /^\\+?\\d{10,}$/
String    response body uuid     /^[a-f0-9-]{36}$/
```

## Common Patterns

### API Test Structure

```robotframework
*** Settings ***
Library    REST    https://api.example.com

*** Test Cases ***
Get User By ID
    GET    /users/1
    Integer    response status    200
    String     response body name
    Integer    response body id    1
    Missing    response body error

Create User Successfully
    POST    /users    {"name": "Test", "email": "test@test.com"}
    Integer    response status    201
    String     response body name    Test
    Integer    response body id
```

### Store and Reuse Values

```robotframework
*** Test Cases ***
Create And Verify User
    POST    /users    {"name": "John"}
    ${id}=    Integer    response body id

    GET    /users/${id}
    Integer    response body id    ${id}
    String     response body name    John
```

### Validate Response Headers

```robotframework
GET    /users
String    response headers Content-Type    application/json*
```

## When to Load Additional References

Load these reference files for specific use cases:

- Instance state management -> `references/instance-management.md`
- All request keywords -> `references/request-keywords.md`
- Deep response validation -> `references/response-validation.md`
- JSON Schema patterns -> `references/json-schema-validation.md`
- OAuth, JWT, API keys -> `references/authentication.md`
- OpenAPI/Swagger testing -> `references/spec-driven-testing.md`
- Error debugging -> `references/troubleshooting.md`
