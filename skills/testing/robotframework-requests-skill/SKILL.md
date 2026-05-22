---
name: robotframework-requests-skill
description: Guide AI agents in creating REST API tests using RequestsLibrary. Use when building HTTP client tests, JSON/XML API testing, session management, authentication, file uploads, and response validation.
---

# Requests Library Skill

## Quick Reference

RequestsLibrary provides HTTP client keywords for REST API testing, wrapping Python's requests library. It supports JSON, XML, form data, file uploads, and all authentication methods.

## Installation

```bash
pip install robotframework-requests
```

## Library Import

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    Collections    # Often needed for dict/list operations
```

## Two Usage Styles

### Style 1: Sessionless (Simple, Recommended for Most Cases)

Direct HTTP calls without session management:

```robotframework
${response}=    GET    https://api.example.com/users
${response}=    POST   https://api.example.com/users    json=${data}
${response}=    PUT    https://api.example.com/users/1  json=${data}
${response}=    DELETE https://api.example.com/users/1
```

### Style 2: With Session (For Multiple Calls to Same API)

Create a session once, reuse for multiple requests:

```robotframework
Create Session    api    https://api.example.com    verify=${True}
${response}=    GET On Session    api    /users
${response}=    POST On Session   api    /users    json=${data}
${response}=    DELETE On Session    api    /users/1
```

## Core Keywords Quick Reference

### HTTP Methods

| Keyword | Usage | Description |
|---------|-------|-------------|
| `GET` | `GET ${URL}` | Retrieve resource |
| `POST` | `POST ${URL} json=${data}` | Create resource |
| `PUT` | `PUT ${URL} json=${data}` | Replace resource |
| `PATCH` | `PATCH ${URL} json=${data}` | Partial update |
| `DELETE` | `DELETE ${URL}` | Remove resource |
| `HEAD` | `HEAD ${URL}` | Get headers only |
| `OPTIONS` | `OPTIONS ${URL}` | Get allowed methods |

### Request Options

| Option | Example | Description |
|--------|---------|-------------|
| `json` | `json=${dict}` | Send JSON body |
| `data` | `data=${form}` | Send form data |
| `params` | `params=${query}` | URL query parameters |
| `headers` | `headers=${headers}` | Custom headers |
| `expected_status` | `expected_status=201` | Verify status code |
| `timeout` | `timeout=30` | Request timeout (seconds) |
| `verify` | `verify=${False}` | SSL verification |

## Working with JSON

### Send JSON Data

```robotframework
&{user}=    Create Dictionary    name=John    email=john@example.com
${response}=    POST    ${API_URL}/users    json=${user}
```

### Parse JSON Response

```robotframework
${response}=    GET    ${API_URL}/users/1
${json}=    Set Variable    ${response.json()}
${name}=    Set Variable    ${json}[name]
${email}=   Set Variable    ${json}[email]
```

### Access Nested JSON

```robotframework
# Response: {"user": {"profile": {"name": "John"}}}
${name}=    Set Variable    ${response.json()}[user][profile][name]
```

## Response Validation

### Status Code Verification

```robotframework
# In request (recommended)
${response}=    GET    ${URL}    expected_status=200
${response}=    POST   ${URL}    json=${data}    expected_status=201
${response}=    DELETE ${URL}    expected_status=204

# Post-request
Status Should Be    200    ${response}
Should Be Equal As Integers    ${response.status_code}    200

# Accept any status (for error testing)
${response}=    GET    ${URL}/notfound    expected_status=anything
```

### Response Content Validation

```robotframework
Should Be Equal    ${response.json()}[status]    success
Should Contain     ${response.text}    success
Dictionary Should Contain Key    ${response.json()}    id
Should Not Be Empty    ${response.json()}[name]
```

## Headers

### Set Request Headers

```robotframework
&{headers}=    Create Dictionary
...    Authorization=Bearer ${TOKEN}
...    Content-Type=application/json
...    Accept=application/json
${response}=    GET    ${URL}    headers=${headers}
```

### Check Response Headers

```robotframework
${content_type}=    Set Variable    ${response.headers}[Content-Type]
Should Contain    ${content_type}    application/json
```

## Common Patterns

### CRUD Operations

```robotframework
*** Test Cases ***
CRUD User Lifecycle
    # Create
    &{user}=    Create Dictionary    name=John    email=john@test.com
    ${response}=    POST    ${API}/users    json=${user}    expected_status=201
    ${user_id}=    Set Variable    ${response.json()}[id]

    # Read
    ${response}=    GET    ${API}/users/${user_id}    expected_status=200
    Should Be Equal    ${response.json()}[name]    John

    # Update
    &{updates}=    Create Dictionary    name=John Updated
    ${response}=    PUT    ${API}/users/${user_id}    json=${updates}    expected_status=200
    Should Be Equal    ${response.json()}[name]    John Updated

    # Delete
    ${response}=    DELETE    ${API}/users/${user_id}    expected_status=204
```

### Authentication Patterns

```robotframework
# Bearer Token
&{headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
${response}=    GET    ${URL}    headers=${headers}

# Basic Auth (using auth parameter)
${auth}=    Create List    ${USERNAME}    ${PASSWORD}
${response}=    GET    ${URL}    auth=${auth}
```

### Query Parameters

```robotframework
&{params}=    Create Dictionary    page=1    limit=10    sort=name
${response}=    GET    ${API}/users    params=${params}
# Results in: GET /users?page=1&limit=10&sort=name
```

## Response Object Properties

| Property | Description | Example |
|----------|-------------|---------|
| `status_code` | HTTP status code | `${response.status_code}` |
| `text` | Response body as text | `${response.text}` |
| `json()` | Parse JSON response | `${response.json()}` |
| `headers` | Response headers dict | `${response.headers}[Content-Type]` |
| `content` | Response body as bytes | `${response.content}` |
| `cookies` | Response cookies | `${response.cookies}` |
| `elapsed` | Request duration | `${response.elapsed.total_seconds()}` |

## When to Load Additional References

Load these reference files for specific use cases:

- Session management with cookies/state -> `references/sessions.md`
- All HTTP methods and options -> `references/request-methods.md`
- Complex JSON payloads/parsing -> `references/json-handling.md`
- XML/SOAP APIs -> `references/xml-text-handling.md`
- Response assertions -> `references/response-validation.md`
- OAuth, JWT, API keys -> `references/authentication.md`
- File upload/download -> `references/files-upload-download.md`
- SSL certificates, mTLS -> `references/ssl-certificates.md`
- Error debugging -> `references/troubleshooting.md`
