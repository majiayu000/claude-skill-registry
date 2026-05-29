---
name: dotnet-doc-controller
description: Generates comprehensive API documentation for a .NET REST controller. Use when the user wants to document API endpoints, generate controller docs, or create API reference documentation.
allowed-tools: Read, Grep, Glob, Bash, Write, Task
---

# Generate API Documentation for a .NET Controller

You are a documentation generator for .NET REST API Controllers. Your task is to create comprehensive, concise API documentation in Markdown format.

## Input

The user will provide a controller name or file path as argument: `$ARGUMENTS`

## Instructions

1. **Find the Controller**: Search for the controller file in the project. If `$ARGUMENTS` is a file path, read it directly. If it's a controller name (e.g., `User`, `UserController`), search for the matching file in `**/Controllers/**Controller.cs`.

2. **Read the Controller**: Read the entire controller file to understand all endpoints, HTTP methods, route patterns, authorization requirements, request/response types, and error handling.

3. **Find all DTOs and Models**: For every DTO, model, enum, or parameter class referenced in the controller (input parameters, return types, response objects), search the entire codebase to find their full definitions. This includes:
   - Request body DTOs (e.g., `[FromBody] SomeDto param`)
   - Response types (e.g., `ActionResult<SomeDto>`)
   - Nested objects within DTOs (if a DTO has a property of another type, find that type too)
   - Any enums used in any of the above objects
   - Anonymous objects returned via `Ok(new { ... })`

   **IMPORTANT**: Search in ALL projects in the solution, including NuGet package sources if DTOs are in external packages. Use `dotnet` commands or search the NuGet cache if necessary. Check:
   - Local project files (`**/*.cs`)
   - NuGet package cache (`~/.nuget/packages/`)
   - Decompiled sources if needed

4. **Generate the Documentation**: Create a markdown file following the exact format and rules below.

5. **Save the File**: Save the documentation to `docs/<CONTROLLER_NAME>_API_DOCUMENTATION.md` where `<CONTROLLER_NAME>` is in UPPER_SNAKE_CASE (e.g., `User` → `USER`, `UserRole` → `USER_ROLE`). Create the `docs/` directory if it doesn't exist.

## Documentation Format Rules

The generated markdown MUST follow this exact structure:

```markdown
# <ControllerName> API Documentation

> Base URL: `/<route-prefix>`

## Authentication

<Describe the authentication scheme used - Bearer token, API key, etc. Mention which endpoints require auth and which are public.>

## Objects

### <ObjectName>

<Brief one-line description of the object.>

\`\`\`json
{
  "property1": "string value",
  "property2": 123,
  "property3": true,
  "nestedObject": {
    "nestedProp1": "value",
    "nestedProp2": 0
  },
  "arrayProp": []
}
\`\`\`

| Property | Type | Description |
|----------|------|-------------|
| property1 | string | Description |
| property2 | int | Description |

### Enums

#### <EnumName>

\`\`\`json
{
  "0": "Value1",
  "1": "Value2",
  "2": "Value3"
}
\`\`\`

---

## Endpoints

### 1. <Endpoint Name>

<One-line description of what the endpoint does.>

**Endpoint:** `<HTTP_METHOD> /<route>`

**Authentication:** Required / Not Required

**Path Parameters:**
- `paramName` (type, required) - Description

**Query Parameters:**
- `paramName` (type, optional) - Description

**Request Headers:**
- `Header-Name` (type, required/optional) - Description

**Request Body:**
\`\`\`json
{
  "field1": "value",
  "field2": 123
}
\`\`\`

**Request Example:**
\`\`\`http
<HTTP_METHOD> /<full-route>
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

<body if applicable>
\`\`\`

**Response Success (200):**
\`\`\`json
{
  "complete": "json response with all fields populated with example values"
}
\`\`\`

**Response Error (400):**
\`\`\`json
"Validation error message"
\`\`\`

**Response Error (401):**
\`\`\`json
"Not Authorized"
\`\`\`

**Response Error (404):**
\`\`\`json
"Not found message"
\`\`\`

**Response Error (500):**
\`\`\`json
"Error message details"
\`\`\`
```

## Critical Rules

1. **Complete JSON objects**: Every JSON response example MUST include ALL properties of the object, fully populated with realistic example values. Never use `...` or `// more fields`. Show the COMPLETE object.

2. **Enums as JSON**: Every enum used in any response or request object MUST be documented in the "Enums" section with its numeric values mapped to string names.

3. **All HTTP methods**: Document EVERY endpoint in the controller. Cover GET, POST, PUT, DELETE, PATCH - whatever exists.

4. **All response codes**: For each endpoint, document ALL possible HTTP response codes based on the controller code (200, 400, 401, 403, 404, 500, etc.). Only include response codes that actually exist in the code.

5. **Realistic examples**: Use realistic, contextual example values (not "string", "0", "true"). For a user name use "John Doe", for an email use "john.doe@example.com", etc.

6. **Nested objects**: If a response contains nested objects, show them fully expanded in the JSON example.

7. **File naming**: Use UPPER_SNAKE_CASE for the file name: `docs/<NAME>_API_DOCUMENTATION.md`

8. **Only include sections that apply**: If an endpoint has no query parameters, don't include the "Query Parameters" section. If no request body, don't include "Request Body". Keep it concise.

9. **Anonymous objects**: If the controller returns `Ok(new { token, user })`, document the anonymous object shape based on what properties are included.

10. **FormFile endpoints**: For file upload endpoints (`IFormFile`), show the request as `multipart/form-data` with the appropriate Content-Type header.

## Example Output for Different HTTP Methods

### GET Example (with path param):
```
**Endpoint:** `GET /user/getById/{userId}`
**Request Example:**
\`\`\`http
GET /user/getById/42
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
\`\`\`
```

### POST Example (with JSON body):
```
**Endpoint:** `POST /user/insert`
**Request Example:**
\`\`\`http
POST /user/insert
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
\`\`\`
```

### PUT Example (with JSON body):
```
**Endpoint:** `PUT /role/update`
**Request Example:**
\`\`\`http
PUT /role/update
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "roleId": 1,
  "name": "Admin",
  "slug": "admin"
}
\`\`\`
```

### DELETE Example (with path param):
```
**Endpoint:** `DELETE /role/delete/{roleId}`
**Request Example:**
\`\`\`http
DELETE /role/delete/5
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
\`\`\`
```

### POST with File Upload Example:
```
**Endpoint:** `POST /user/uploadImageUser`
**Request Example:**
\`\`\`http
POST /user/uploadImageUser
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="photo.jpg"
Content-Type: image/jpeg

<binary file data>
------FormBoundary--
\`\`\`
```

## After Generating

After creating the file, inform the user:
- The file path where documentation was saved
- The number of endpoints documented
- Any DTOs or enums that could not be fully resolved (if applicable)
