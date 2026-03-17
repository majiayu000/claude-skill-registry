---
name: integration-spec
description: Эксперт по интеграционным спецификациям. Используй для документирования интеграций, webhooks, event schemas и data flows.
---

# Integration Specification Writer

Expert in writing comprehensive integration specifications that serve as contracts between systems.

## Essential Components

Every integration spec must include:

- **Integration Overview**: Purpose, scope, and high-level architecture
- **Authentication & Authorization**: Security mechanisms and token handling
- **Endpoint Definitions**: Complete API contract with request/response schemas
- **Data Models**: Structured definitions of all data objects
- **Error Handling**: Comprehensive error codes and recovery procedures
- **Rate Limiting**: Throttling rules and quota management
- **Sequence Diagrams**: Visual representation of interaction flows
- **Testing Scenarios**: Integration test cases and validation criteria

## Integration Specification Template

```markdown
# Integration Specification: [System A] ↔ [System B]

**Version:** 1.0.0
**Last Updated:** [Date]
**Authors:** [Names]
**Status:** [Draft/Review/Approved/Production]

## 1. Overview

### 1.1 Purpose
[Brief description of why this integration exists]

### 1.2 Scope
- In Scope: [What this integration covers]
- Out of Scope: [What this integration does not cover]

### 1.3 Architecture Diagram
[Include diagram showing systems, data flow, and key components]

## 2. Authentication & Authorization

### 2.1 Authentication Method
[OAuth 2.0 / API Key / JWT / mTLS]

### 2.2 Credential Management
[How credentials are obtained, stored, and rotated]

## 3. Endpoints

[Detailed endpoint specifications]

## 4. Data Models

[Complete schema definitions]

## 5. Error Handling

[Error codes and recovery procedures]

## 6. Rate Limiting

[Throttling rules and quotas]

## 7. Testing

[Test scenarios and validation criteria]
```

## Authentication Specification

```yaml
authentication:
  type: "Bearer Token (OAuth 2.0)"
  flow: "Client Credentials"

  endpoints:
    token:
      url: "https://api.example.com/oauth/token"
      method: "POST"
      content_type: "application/x-www-form-urlencoded"

  request:
    grant_type: "client_credentials"
    client_id: "{CLIENT_ID}"
    client_secret: "{CLIENT_SECRET}"
    scope: "read write"

  response:
    access_token: "string"
    token_type: "Bearer"
    expires_in: 3600
    scope: "read write"

  usage:
    header: "Authorization: Bearer {access_token}"
    content_type: "application/json"

  token_refresh:
    automatic: true
    threshold_seconds: 300  # Refresh 5 min before expiry
    retry_attempts: 3
    retry_delay_seconds: 5

  security_requirements:
    - "Store credentials in secure vault (not in code)"
    - "Use HTTPS for all requests"
    - "Implement token caching to reduce auth calls"
    - "Log authentication failures for monitoring"
```

## Endpoint Documentation Standards

```yaml
# POST /api/v1/orders

endpoint:
  method: "POST"
  path: "/api/v1/orders"
  description: "Create a new order in the system"

headers:
  required:
    Authorization: "Bearer {access_token}"
    Content-Type: "application/json"
    X-Request-ID: "string (UUID) - for request tracing"
  optional:
    X-Idempotency-Key: "string - prevents duplicate processing"

request:
  body:
    type: "object"
    required: ["customer_id", "items"]
    properties:
      customer_id:
        type: "string"
        description: "Unique customer identifier"
        constraints: "max 50 characters, alphanumeric"
        example: "CUST-12345"
      items:
        type: "array"
        minItems: 1
        maxItems: 100
        items:
          type: "object"
          required: ["product_id", "quantity"]
          properties:
            product_id:
              type: "string"
              description: "Product SKU"
              example: "SKU-001"
            quantity:
              type: "integer"
              minimum: 1
              maximum: 999
              example: 2
            unit_price:
              type: "number"
              format: "decimal"
              description: "Price per unit (2 decimal places)"
              example: 29.99
      shipping_address:
        type: "object"
        required: ["street", "city", "postal_code", "country"]
        properties:
          street:
            type: "string"
            maxLength: 100
          city:
            type: "string"
            maxLength: 50
          postal_code:
            type: "string"
            pattern: "^\\d{5}(-\\d{4})?$"
          country:
            type: "string"
            format: "ISO 3166-1 alpha-2"

responses:
  201:
    description: "Order created successfully"
    body:
      order_id: "ORD-12345678"
      status: "pending"
      total_amount: 299.99
      currency: "USD"
      created_at: "2024-01-15T10:30:00Z"
      estimated_delivery: "2024-01-20T10:00:00Z"
      tracking_url: "https://api.example.com/orders/ORD-12345678/track"

  400:
    description: "Invalid request"
    body:
      error_code: "VALIDATION_ERROR"
      message: "Request validation failed"
      details:
        - field: "items[0].quantity"
          error: "Must be between 1 and 999"

  401:
    description: "Authentication failed"
    body:
      error_code: "UNAUTHORIZED"
      message: "Invalid or expired access token"

  409:
    description: "Conflict"
    body:
      error_code: "DUPLICATE_ORDER"
      message: "Order with this idempotency key already exists"
      existing_order_id: "ORD-12345678"

  429:
    description: "Rate limit exceeded"
    headers:
      Retry-After: "60"
      X-RateLimit-Limit: "100"
      X-RateLimit-Remaining: "0"
      X-RateLimit-Reset: "1704067200"
```

## Error Handling Specification

```yaml
error_format:
  standard_response:
    error_code: "string - machine-readable error code"
    message: "string - human-readable description"
    details: "array - specific field errors (optional)"
    request_id: "string - for support reference"
    timestamp: "string - ISO 8601 datetime"

error_codes:
  VALIDATION_ERROR:
    http_status: 400
    description: "Request body failed validation"
    retry_strategy: "Do not retry - fix request and resubmit"
    resolution: "Check error details for specific field issues"

  INVALID_CUSTOMER:
    http_status: 400
    description: "Customer ID not found or inactive"
    retry_strategy: "Do not retry - verify customer data"
    resolution: "Validate customer exists and has active status"

  UNAUTHORIZED:
    http_status: 401
    description: "Invalid or expired authentication"
    retry_strategy: "Refresh token and retry once"
    resolution: "Obtain new access token"

  FORBIDDEN:
    http_status: 403
    description: "Insufficient permissions"
    retry_strategy: "Do not retry"
    resolution: "Contact admin to verify API scopes"

  NOT_FOUND:
    http_status: 404
    description: "Requested resource does not exist"
    retry_strategy: "Do not retry"
    resolution: "Verify resource ID is correct"

  CONFLICT:
    http_status: 409
    description: "Resource state conflict"
    retry_strategy: "Fetch current state and reconcile"
    resolution: "Check existing resource and merge changes"

  RATE_LIMIT_EXCEEDED:
    http_status: 429
    description: "Too many requests"
    retry_strategy: "Wait for Retry-After header duration"
    resolution: "Implement exponential backoff"
    headers:
      Retry-After: "Seconds to wait before retry"
      X-RateLimit-Reset: "Unix timestamp when limit resets"

  INTERNAL_ERROR:
    http_status: 500
    description: "Unexpected server error"
    retry_strategy: "Retry with exponential backoff (max 3 attempts)"
    resolution: "If persists, contact support with request_id"

  SERVICE_UNAVAILABLE:
    http_status: 503
    description: "Service temporarily unavailable"
    retry_strategy: "Retry with exponential backoff"
    resolution: "Check status page, retry after delay"
```

## Webhook Specification

```yaml
webhooks:
  overview:
    description: "Real-time event notifications via HTTP POST"
    delivery: "At-least-once delivery guarantee"
    format: "JSON payload with HMAC signature"

  configuration:
    endpoint_url: "Your HTTPS endpoint"
    secret_key: "Shared secret for signature verification"
    events: ["order.created", "order.updated", "order.cancelled"]

  security:
    signature_header: "X-Webhook-Signature"
    signature_algorithm: "HMAC-SHA256"
    timestamp_header: "X-Webhook-Timestamp"
    replay_prevention: "Reject if timestamp > 5 minutes old"

  verification_example:
    python: |
      import hmac
      import hashlib

      def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
          expected = hmac.new(
              secret.encode(),
              payload,
              hashlib.sha256
          ).hexdigest()
          return hmac.compare_digest(f"sha256={expected}", signature)

  payload_structure:
    event_id: "string - unique event identifier"
    event_type: "string - e.g., order.created"
    timestamp: "string - ISO 8601"
    data:
      object_type: "string - e.g., order"
      object_id: "string - resource identifier"
      changes: "object - changed fields (for update events)"

  retry_policy:
    attempts: 5
    schedule:
      - "Immediate"
      - "1 minute"
      - "5 minutes"
      - "30 minutes"
      - "2 hours"
    success_criteria: "HTTP 2xx response within 30 seconds"
    failure_action: "Event logged, alert sent, manual retry available"

  expected_response:
    status: "2xx within 30 seconds"
    body: "Optional - ignored"

  events:
    order.created:
      description: "Fired when a new order is created"
      payload:
        order_id: "string"
        customer_id: "string"
        total_amount: "number"
        items: "array"
        created_at: "string"

    order.updated:
      description: "Fired when order status changes"
      payload:
        order_id: "string"
        previous_status: "string"
        current_status: "string"
        updated_at: "string"
```

## Rate Limiting Specification

```yaml
rate_limits:
  default:
    requests_per_minute: 100
    requests_per_day: 10000
    burst_allowance: "150% for up to 30 seconds"

  per_endpoint:
    "/api/v1/orders":
      method: "POST"
      limit: "100 requests/minute"
      reason: "Write operation - higher resource cost"

    "/api/v1/orders":
      method: "GET"
      limit: "300 requests/minute"
      reason: "Read operation - cached responses"

    "/api/v1/search":
      limit: "60 requests/minute"
      reason: "Expensive search operation"

  headers:
    X-RateLimit-Limit: "Requests allowed per window"
    X-RateLimit-Remaining: "Requests remaining"
    X-RateLimit-Reset: "Unix timestamp when window resets"

  exceeded_response:
    status: 429
    body:
      error_code: "RATE_LIMIT_EXCEEDED"
      message: "Rate limit exceeded"
      retry_after: 60

  best_practices:
    - "Implement client-side rate limiting"
    - "Use exponential backoff on 429 responses"
    - "Cache responses where possible"
    - "Batch operations when available"
```

## Sequence Diagram Example

```
sequenceDiagram
    participant Client
    participant API Gateway
    participant Order Service
    participant Payment Service
    participant Inventory Service
    participant Notification Service

    Client->>API Gateway: POST /api/v1/orders
    API Gateway->>API Gateway: Validate Token
    API Gateway->>Order Service: Create Order

    Order Service->>Inventory Service: Reserve Items
    Inventory Service-->>Order Service: Reservation Confirmed

    Order Service->>Payment Service: Process Payment
    Payment Service-->>Order Service: Payment Success

    Order Service->>Order Service: Update Order Status
    Order Service-->>API Gateway: Order Created (201)
    API Gateway-->>Client: Order Response

    Order Service--)Notification Service: order.created Event
    Notification Service--)Client: Webhook: order.created
```

## Testing Scenarios

```yaml
test_scenarios:
  happy_path:
    name: "Successful order creation"
    preconditions:
      - "Valid customer account exists"
      - "Products are in stock"
      - "Payment method is valid"
    request:
      method: "POST"
      path: "/api/v1/orders"
      body: "{valid order payload}"
    expected:
      status: 201
      response_contains: ["order_id", "status", "total_amount"]
    postconditions:
      - "Order record created in database"
      - "Inventory reserved"
      - "Payment processed"
      - "Webhook sent"

  validation_errors:
    - name: "Missing required field"
      request: "{order without customer_id}"
      expected_status: 400
      expected_error: "VALIDATION_ERROR"

    - name: "Invalid quantity"
      request: "{order with quantity: 0}"
      expected_status: 400
      expected_error: "VALIDATION_ERROR"

  edge_cases:
    - name: "Insufficient inventory"
      setup: "Set product stock to 0"
      expected_status: 409
      expected_error: "INSUFFICIENT_INVENTORY"

    - name: "Payment failure"
      setup: "Configure payment service to decline"
      expected_status: 402
      expected_error: "PAYMENT_FAILED"
      postcondition: "Inventory reservation released"

  idempotency:
    name: "Duplicate request handling"
    steps:
      - "Send order with X-Idempotency-Key: abc123"
      - "Response: 201 Created, order_id: ORD-001"
      - "Send same request with same idempotency key"
      - "Response: 200 OK, order_id: ORD-001 (same order)"
```

## Environment Configuration

```yaml
environments:
  sandbox:
    base_url: "https://api-sandbox.example.com"
    purpose: "Development and testing"
    rate_limits: "10x production limits"
    data: "Test data, reset daily at 00:00 UTC"
    credentials: "Separate sandbox API keys"

  staging:
    base_url: "https://api-staging.example.com"
    purpose: "Pre-production validation"
    rate_limits: "Same as production"
    data: "Anonymized production-like data"

  production:
    base_url: "https://api.example.com"
    sla:
      uptime: "99.9%"
      response_time_p95: "<200ms"
      response_time_p99: "<500ms"
    maintenance_window: "Sundays 02:00-04:00 UTC"
    support: "support@example.com"
```

## Лучшие практики

1. **Version everything** — версионирование в URL и заголовках
2. **Idempotency** — документируйте идемпотентные операции
3. **Error detail** — достаточно информации для отладки
4. **Rate limit transparency** — всегда возвращайте лимиты в headers
5. **Webhook reliability** — retry policy и signature verification
6. **Environment parity** — sandbox максимально похож на production
