---
name: hurl
description: Run and test HTTP requests with Hurl. Use when working with HTTP APIs, testing web services, or creating HTTP-based test scenarios. Hurl allows you to define HTTP requests in plain text files and validate responses with asserts and captures.
---

# Hurl

## Quick Start

Hurl is a command line tool that runs HTTP requests defined in a simple plain text format. It can chain requests, capture values, and evaluate queries on headers and body responses.

```shell
$ hurl session.hurl
$ hurl --test *.hurl
```

## Hurl File Format

Hurl files use `.hurl` extension and consist of one or more HTTP entries. Each entry has a mandatory request and an optional response section.

```hurl
GET https://example.org/api
HTTP 200
Content-Type: application/json
[Asserts]
jsonpath "$.status" == "success"
```

### Comments

Comments begin with `#` and continue until the end of line:

```hurl
# Check that the API returns the expected response
GET https://example.org/health
HTTP 200
```

## Requests

### Basic Request

```hurl
GET https://example.org/endpoint
```

### HTTP Methods

```hurl
GET https://example.org/resource
POST https://example.org/resource
PUT https://example.org/resource
PATCH https://example.org/resource
DELETE https://example.org/resource
HEAD https://example.org/resource
OPTIONS https://example.org/resource
```

### Headers

```hurl
GET https://example.org/api
User-Agent: MyApp/1.0
Accept: application/json
Content-Type: application/json
```

### Query Parameters

```hurl
GET https://example.org/search
[Query]
term: hurl
page: 1
limit: 10
```

### Form Data

```hurl
POST https://example.org/login
[Form]
username: user@example.com
password: secret123
```

### Multipart Form Data

```hurl
POST https://example.org/upload
[Multipart]
field1: value1
field2: file,data.txt;
field3: file,image.png; image/png
```

### JSON Body

```hurl
POST https://example.org/api/users
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}
```

### XML Body

```hurl
POST https://example.org/soap-service
Content-Type: application/soap+xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body>
    <GetStatus>
      <id>12345</id>
    </GetStatus>
  </soap:Body>
</soap:Envelope>
```

### GraphQL

```hurl
POST https://example.org/graphql
```graphql
query {
  user(id: "123") {
    name
    email
  }
}
```
```

### Basic Authentication

```hurl
GET https://example.org/protected
[BasicAuth]
admin: secretpassword
```

### Cookies

```hurl
GET https://example.org/page
[Cookies]
session: abc123
preference: dark-mode
```

### Variables in Requests

```hurl
GET https://example.org/api/users/{{user_id}}
[Query]
expand: true

POST https://example.org/api/users
{
    "name": "{{user_name}}",
    "email": "{{user_email}}"
}
```

Define variables via command line:

```shell
$ hurl --variable user_id=123 --variable user_name="John" test.hurl
```

Or use a variables file:

```shell
$ hurl --variables-file config.json test.hurl
```

## Responses

Response sections describe expected HTTP responses and can include assertions and captures.

```hurl
GET https://example.org/api
HTTP 200
Content-Type: application/json
[Asserts]
status == 200
```

### Status Code

```hurl
GET https://example.org/resource
HTTP 200
```

Wildcard for any status:

```hurl
GET https://example.org/resource
HTTP *
[Asserts]
status < 300
```

### Headers

```hurl
GET https://example.org/resource
HTTP 200
Content-Type: application/json
Cache-Control: max-age=3600
```

## Captures

Captures extract values from HTTP responses into variables for use in subsequent requests.

```hurl
GET https://example.org/login
HTTP 200
[Captures]
csrf_token: xpath "normalize-space(//meta[@name='csrf-token']/@content)"

POST https://example.org/login
[Form]
csrf_token: {{csrf_token}}
username: user
password: pass
HTTP 302
```

### Capture Types

```hurl
GET https://example.org/api/user
HTTP 200
[Captures]
user_id: jsonpath "$.id"
user_name: jsonpath "$.name"
email: jsonpath "$.email"
redirect_url: header "Location"
status: status
body_text: body
response_bytes: bytes
sha_hash: sha256
```

### XPath Capture

```hurl
GET https://example.org/page
HTTP 200
[Captures]
title: xpath "string(//head/title)"
first_heading: xpath "string(//h1)"
csrf_token: xpath "normalize-space(//meta[@name='csrf_token']/@content)"
```

### JSONPath Capture

```hurl
GET https://example.org/api/data
HTTP 200
[Captures]
user_id: jsonpath "$.user.id"
items_count: jsonpath "$.items.length()"
first_item: jsonpath "$.items[0]"
```

### Regex Capture

```hurl
GET https://example.org/page
HTTP 200
[Captures]
id: regex "user-(\d+)"
version: regex /version\/(\d+\.\d+\.\d+)/
```

### Duration Capture

```hurl
GET https://example.org/api
HTTP 200
[Captures]
response_time: duration
```

Filters can be applied to captures. See [Filters Reference](filters.md) for available filters.

### Certificate Capture

```hurl
GET https://example.org
HTTP 200
[Captures]
cert_subject: certificate "Subject"
cert_issuer: certificate "Issuer"
cert_expiry: certificate "Expire-Date"
```

## Assertions

Assertions validate HTTP responses. They can be implicit (status, headers) or explicit in an `[Asserts]` section.

Filters can be applied to assertions to transform values before comparison. See [Filters Reference](filters.md) for available filters.

```hurl
GET https://example.org/api
HTTP 200
Content-Type: application/json
[Asserts]
jsonpath "$.status" == "success"
jsonpath "$.data.length()" == 10
header "X-Rate-Limit" exists
```

### Status Assertions

```hurl
GET https://example.org/resource
HTTP 200
[Asserts]
status == 200
status >= 200
status < 300
```

### Header Assertions

```hurl
GET https://example.org/resource
HTTP 200
[Asserts]
header "Content-Type" contains "application/json"
header "X-Request-Id" matches /^[a-f0-9]+$/
header "Cache-Control" == "max-age=3600"
header "Set-Cookie" count == 2
```

### Body Assertions

```hurl
GET https://example.org/api
HTTP 200
[Asserts]
body contains "success"
body startsWith "{"
body endsWith "}"
```

### JSONPath Assertions

```hurl
GET https://example.org/api/users
HTTP 200
[Asserts]
jsonpath "$.users[0].name" == "Alice"
jsonpath "$.users[*].active" contains true
jsonpath "$.count" != 0
jsonpath "$.users" count == 25
jsonpath "$.price" > 9.99
jsonpath "$.data" exists
jsonpath "$.items" isEmpty not
jsonpath "$.id" isInteger
jsonpath "$.price" isFloat
```

### XPath Assertions

```hurl
GET https://example.org/page
HTTP 200
[Asserts]
xpath "string(//head/title)" == "Home Page"
xpath "count(//div)" == 5
xpath "//h1" exists
xpath "//error" not exists
xpath "boolean(count(//warning))" == false
```

### Regex Assertions

```hurl
GET https://example.org/page
HTTP 200
[Asserts]
regex "user:(\d+)" == "user:123"
regex /version:(\d+\.\d+)/ == "version:1.0"
```

### Bytes Assertions

```hurl
GET https://example.org/file.zip
HTTP 200
[Asserts]
bytes count == 1024000
sha256 == hex,abc123...
```

### Duration Assertions

```hurl
GET https://example.org/api
HTTP 200
[Asserts]
duration < 1000
```

### Certificate Assertions

```hurl
GET https://example.org
HTTP 200
[Asserts]
certificate "Subject" == "CN=example.org"
certificate "Issuer" == "C=US, O=Let's Encrypt"
certificate "Expire-Date" daysAfterNow > 30
```

### Predicates

Available predicates: `==`, `!=`, `>`, `>=`, `<`, `<=`, `startsWith`, `endsWith`, `contains`, `matches`, `exists`, `isBoolean`, `isEmpty`, `isFloat`, `isInteger`, `isIpv4`, `isIpv6`, `isIsoDate`, `isList`, `isNumber`, `isObject`, `isString`, `isUuid`

All predicates can be negated with `not`:

```hurl
[Asserts]
header "Authorization" not exists
jsonpath "$.error" not contains "failed"
```

## Chaining Requests

Requests can be chained to create multi-step scenarios:

```hurl
# Get CSRF token
GET https://example.org/login
HTTP 200
[Captures]
csrf_token: xpath "normalize-space(//input[@name='csrf']/@value)"

# Login with captured token
POST https://example.org/login
[Form]
csrf: {{csrf_token}}
username: user
password: pass
HTTP 302

# Follow redirect to dashboard
GET https://example.org/dashboard
HTTP 200
[Asserts]
body contains "Welcome, user"
```

## Control Flow

### Retry

```hurl
POST https://example.org/jobs
HTTP 201
[Captures]
job_id: jsonpath "$.id"

GET https://example.org/jobs/{{job_id}}
[Options]
retry: 10
retry-interval: 500ms
HTTP 200
[Asserts]
jsonpath "$.status" == "COMPLETED"
```

### Skip

```hurl
GET https://example.org/optional
[Options]
skip: true
HTTP 200
```

### Repeat

```hurl
GET https://example.org/health
[Options]
repeat: 10
HTTP 200
```

### Delay

```hurl
GET https://example.org/api
[Options]
delay: 2s
HTTP 200
```

## Redirection Handling

### Manual Redirection Testing

```hurl
GET https://example.org
HTTP 301
Location: https://www.example.org

GET https://www.example.org
HTTP 200
```

### Automatic Redirection

```hurl
GET https://example.org
[Options]
location: true
HTTP 200
[Asserts]
url == "https://www.example.org"
redirects count == 1
redirects nth 0 location == "https://www.example.org"
```

## Secrets and Redaction

Hide sensitive values from logs:

```shell
$ hurl --secret api_key=abc123 test.hurl
```

Or make captures redacted:

```hurl
POST https://example.org/login
HTTP 200
[Captures]
token: header "X-Auth-Token" redact
```

## Command Line Options

### Testing

```shell
$ hurl --test *.hurl              # Test mode
$ hurl --test --jobs 4 *.hurl     # Parallel test execution
$ hurl --test --repeat 100 *.hurl # Stress test
```

### Output Control

```shell
$ hurl -o output.json test.hurl   # Write output to file
$ hurl --no-output test.hurl      # Suppress output
$ hurl --include test.hurl        # Include headers in output
$ hurl --color test.hurl          # Colorize output
```

### Reports

```shell
$ hurl --report-html results/ test.hurl    # HTML report
$ hurl --report-json results/ test.hurl    # JSON report
$ hurl --report-junit results.xml test.hurl # JUnit XML
$ hurl --report-tap results.tap test.hurl  # TAP format
```

### Debugging

```shell
$ hurl --verbose test.hurl           # Verbose output
$ hurl --very-verbose test.hurl      # Very verbose (includes headers)
$ hurl --test --error-format long *.hurl # Detailed error output
```

### Request Options

```shell
$ hurl --location test.hurl          # Follow redirects
$ hurl --compressed test.hurl        # Request compressed response
$ hurl -u user:pass test.hurl        # Basic auth
$ hurl -H "Header: value" test.hurl  # Custom header
$ hurl -x proxy:8080 test.hurl       # Use proxy
$ hurl --insecure test.hurl          # Skip SSL verification
$ hurl --max-time 30 test.hurl       # Timeout
$ hurl --retry 3 test.hurl           # Retry on failure
```

### Variables

```shell
$ hurl --variable name=value test.hurl
$ hurl --variables-file vars.json test.hurl
$ HURL_VARIABLE_NAME=value hurl test.hurl
```

### Files and Paths

```shell
$ hurl --file-root /path/to/files test.hurl
$ hurl --glob "tests/**/*.hurl"       # Find files by pattern
$ hurl dir/                           # Run all .hurl files in directory
```

## Testing Best Practices

### Use Test Mode

```shell
$ hurl --test test/api/*.hurl
```

### Generate Reports for CI/CD

```shell
$ hurl --test --report-junit results.xml --report-html reports/ tests/
```

### Organize Tests

```shell
tests/
  api/
    users.hurl
    auth.hurl
    products.hurl
  integration/
    checkout.hurl
    search.hurl
  smoke/
    health.hurl
```

### Test Performance

```hurl
GET https://example.org/api
HTTP 200
[Asserts]
duration < 500
```

### Debug Failing Tests

```shell
$ hurl --test --very-verbose --error-format long failing_test.hurl
```

## Common Patterns

### API Health Check

```hurl
GET https://api.example.org/health
HTTP 200
[Asserts]
jsonpath "$.status" == "healthy"
jsonpath "$.version" exists
```

### REST API CRUD

```hurl
# Create
POST https://api.example.org/users
Content-Type: application/json
{
    "name": "Test User",
    "email": "test@example.com"
}
HTTP 201
[Captures]
user_id: jsonpath "$.id"

# Read
GET https://api.example.org/users/{{user_id}}
HTTP 200
[Asserts]
jsonpath "$.name" == "Test User"

# Update
PUT https://api.example.org/users/{{user_id}}
Content-Type: application/json
{
    "name": "Updated User"
}
HTTP 200

# Delete
DELETE https://api.example.org/users/{{user_id}}
HTTP 204
```

### Form-based Login

```hurl
GET https://example.org/login
HTTP 200
[Captures]
csrf: xpath "normalize-space(//input[@name='_csrf']/@value)"

POST https://example.org/login
[Form]
_csrf: {{csrf}}
username: myuser
password: mypass
HTTP 302
Location: /dashboard
[Asserts]
status == 302
```

### GraphQL Query

```hurl
POST https://api.example.org/graphql
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      title
    }
  }
}
```
variables: {"id": "{{user_id}}"}
HTTP 200
[Asserts]
jsonpath "$.data.user.name" exists
jsonpath "$.errors" not exists
```

### SOAP Request

```hurl
POST https://example.org/soap-service
Content-Type: application/soap+xml; charset=utf-8
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Body>
    <GetProductInfo>
      <productId>12345</productId>
    </GetProductInfo>
  </soap:Body>
</soap:Envelope>
HTTP 200
[Asserts]
xpath "boolean(//product/available)" == true
```

## File Reference

### Local Resources

- [Filters Reference](filters.md) - Available filters for transforming captured values and assertions
- [Variables & Templates](templates.md) - Variables, templating, and secrets documentation
- [Hurl File Format](hurl-file.md) - File structure, comments, and special characters
- [Request Format](request.md) - HTTP method, URL, headers, body, auth, forms
- [Response Format](response.md) - Expected response, version, status, headers
- [Captures](capturing-response.md) - Extracting values from responses
- [Assertions](asserting-response.md) - Validating responses with asserts and predicates
- [Running Tests](running-tests.md) - Test mode, reports, CI/CD integration
