---
name: api-designer
description: REST/GraphQL API architect specializing in OpenAPI 3.1, HATEOAS, pagination, and versioning strategies
---

# API Designer

## Purpose

Provides expert REST and GraphQL API architecture expertise specializing in OpenAPI 3.1 specifications, API versioning strategies, pagination patterns, and hypermedia-driven design (HATEOAS). Focuses on building scalable, well-documented, developer-friendly APIs with proper error handling and standardization.

## When to Use

- Designing RESTful or GraphQL APIs from requirements
- Creating OpenAPI 3.1 specifications for API documentation
- Implementing API versioning strategies (URL, header, content negotiation)
- Designing pagination, filtering, and sorting patterns for large datasets
- Building HATEOAS-compliant APIs (hypermedia-driven)
- Standardizing error responses and status codes across services
- Designing API authentication and authorization patterns

## Quick Start

**Invoke this skill when:**
- Designing RESTful or GraphQL APIs from requirements
- Creating OpenAPI 3.1 specifications for API documentation
- Implementing API versioning strategies (URL, header, content negotiation)
- Designing pagination, filtering, and sorting patterns for large datasets
- Building HATEOAS-compliant APIs (hypermedia-driven)
- Standardizing error responses and status codes across services

**Do NOT invoke when:**
- Only implementing pre-designed API endpoints (use backend-developer)
- Database schema design without API context (use database-administrator)
- Frontend API integration (use frontend-developer)
- API security implementation (use security-engineer for authentication/authorization)
- API performance optimization (use performance-engineer)

---
---

## Core Workflows

### Workflow 1: Design RESTful API with OpenAPI 3.1

**Use case:** E-commerce platform needs product catalog API

**Step 1: Resource Modeling**
```yaml
# Resources identified:
# - Products (CRUD)
# - Categories (read-only, hierarchical)
# - Reviews (nested under products)
# - Inventory (separate resource, linked to products)

# URL Structure Design:
GET    /v1/products              # List products (paginated)
POST   /v1/products              # Create product
GET    /v1/products/{id}         # Get product details
PUT    /v1/products/{id}         # Update product (full replacement)
PATCH  /v1/products/{id}         # Partial update
DELETE /v1/products/{id}         # Delete product

GET    /v1/products/{id}/reviews        # Get reviews for product
POST   /v1/products/{id}/reviews        # Create review
GET    /v1/products/{id}/reviews/{reviewId}  # Get specific review

GET    /v1/categories            # List categories
GET    /v1/categories/{id}       # Get category + subcategories

# Query parameters (filtering, pagination, sorting):
GET /v1/products?category=electronics&min_price=100&max_price=500&sort=price:asc&limit=20&cursor=abc123
```

**Step 2: OpenAPI 3.1 Specification**
```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: E-commerce Product API
  version: 1.0.0
  description: RESTful API for product catalog management
  contact:
    name: API Support
    email: api@ecommerce.com

servers:
  - url: https://api.ecommerce.com/v1
    description: Production server
  - url: https://staging-api.ecommerce.com/v1
    description: Staging server

paths:
  /products:
    get:
      summary: List products
      operationId: listProducts
      tags: [Products]
      parameters:
        - name: category
          in: query
          description: Filter by category slug
          schema:
            type: string
            example: electronics
        - name: min_price
          in: query
          description: Minimum price filter
          schema:
            type: number
            format: float
            minimum: 0
        - name: max_price
          in: query
          description: Maximum price filter
          schema:
            type: number
            format: float
            minimum: 0
        - name: sort
          in: query
          description: Sort order (field:direction)
          schema:
            type: string
            enum: [price:asc, price:desc, created_at:asc, created_at:desc]
            default: created_at:desc
        - name: limit
          in: query
          description: Number of results per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor (opaque token)
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                required: [data, meta, links]
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  meta:
                    type: object
                    properties:
                      total_count:
                        type: integer
                        description: Total number of products matching filters
                      has_more:
                        type: boolean
                        description: Whether more results exist
                  links:
                    type: object
                    properties:
                      self:
                        type: string
                        format: uri
                      next:
                        type: string
                        format: uri
                        nullable: true
                      prev:
                        type: string
                        format: uri
                        nullable: true
              examples:
                success:
                  value:
                    data:
                      - id: "prod_123"
                        name: "Wireless Headphones"
                        description: "Premium noise-cancelling headphones"
                        price: 299.99
                        currency: "USD"
                        category:
                          id: "cat_1"
                          name: "Electronics"
                        created_at: "2024-01-15T10:30:00Z"
                    meta:
                      total_count: 1523
                      has_more: true
                    links:
                      self: "/v1/products?limit=20"
                      next: "/v1/products?limit=20&cursor=eyJpZCI6InByb2RfMTIzIn0="
                      prev: null
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /products/{id}:
    get:
      summary: Get product details
      operationId: getProduct
      tags: [Products]
      parameters:
        - name: id
          in: path
          required: true
          description: Product ID
          schema:
            type: string
            pattern: '^prod_[a-zA-Z0-9]+$'
      responses:
        '200':
          description: Product found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Product:
      type: object
      required: [id, name, price, currency]
      properties:
        id:
          type: string
          description: Unique product identifier
          example: "prod_123"
        name:
          type: string
          minLength: 1
          maxLength: 200
          example: "Wireless Headphones"
        description:
          type: string
          maxLength: 2000
          nullable: true
        price:
          type: number
          format: float
          minimum: 0
          example: 299.99
        currency:
          type: string
          enum: [USD, EUR, GBP, JPY]
          default: USD
        category:
          $ref: '#/components/schemas/Category'
        images:
          type: array
          items:
            type: string
            format: uri
          maxItems: 10
        inventory_count:
          type: integer
          minimum: 0
          description: Available stock
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Category:
      type: object
      required: [id, name, slug]
      properties:
        id:
          type: string
          example: "cat_1"
        name:
          type: string
          example: "Electronics"
        slug:
          type: string
          pattern: '^[a-z0-9-]+$'
          example: "electronics"
        parent_id:
          type: string
          nullable: true

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              description: Machine-readable error code
              example: "invalid_parameter"
            message:
              type: string
              description: Human-readable error message
              example: "The 'price' parameter must be a positive number"
            details:
              type: object
              description: Additional error context
              additionalProperties: true

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "invalid_parameter"
              message: "The 'min_price' parameter must be a non-negative number"
              details:
                parameter: "min_price"
                value: "-10"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "resource_not_found"
              message: "Product with ID 'prod_999' not found"

    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "internal_server_error"
              message: "An unexpected error occurred. Please try again later."
              details:
                request_id: "req_abc123"

  securitySchemes:
    ApiKey:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - ApiKey: []
  - BearerAuth: []
```

**Step 3: Generate Documentation**
```bash
# Install Redoc CLI
npm install -g redoc-cli

# Generate static HTML documentation
redoc-cli bundle openapi.yaml -o api-docs.html

# Host documentation
npx serve api-docs.html

# Interactive Swagger UI
docker run -p 8080:8080 -e SWAGGER_JSON=/docs/openapi.yaml \
  -v $(pwd):/docs swaggerapi/swagger-ui

# Open http://localhost:8080 for interactive API testing
```

---
---

## Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Inconsistent Error Responses

**What it looks like:**
```json
// Endpoint 1: Login failure
{
  "error": "Invalid credentials"
}

// Endpoint 2: Validation failure
{
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}

// Endpoint 3: Server error
{
  "status": "error",
  "message": "Internal server error",
  "code": 500
}

// Problem: Clients need custom error handling per endpoint
```

**Why it fails:**
- Client code becomes complex (multiple error parsing strategies)
- Frontend developers frustrated (inconsistent contracts)
- Error logging/monitoring difficult (no standard format)

**Correct approach:**
```json
// Standardized error response (all endpoints)
{
  "error": {
    "code": "invalid_credentials",
    "message": "The provided email or password is incorrect",
    "details": null,
    "request_id": "req_abc123"
  }
}

// Validation errors (multiple fields)
{
  "error": {
    "code": "validation_failed",
    "message": "One or more fields failed validation",
    "details": {
      "fields": [
        { "field": "email", "message": "Invalid email format" },
        { "field": "password", "message": "Password must be at least 8 characters" }
      ]
    },
    "request_id": "req_def456"
  }
}

// Client-side error handling (consistent)
function handleApiError(response) {
  const { code, message, details } = response.error;
  
  switch (code) {
    case 'validation_failed':
      // Display field-specific errors
      details.fields.forEach(({ field, message }) => {
        showFieldError(field, message);
      });
      break;
    
    case 'unauthorized':
      // Redirect to login
      redirectToLogin();
      break;
    
    default:
      // Generic error message
      showToast(message);
  }
}
```

---
---

## Integration Patterns

**backend-developer:**
- Handoff: API designer creates spec → Backend implements endpoints
- Collaboration: Error response formats, authentication patterns
- Tools: OpenAPI code generation, API mocking

**frontend-developer:**
- Handoff: API spec published → Frontend consumes API
- Collaboration: Query patterns, pagination, error handling
- Tools: TypeScript type generation from OpenAPI/GraphQL schema

**security-engineer:**
- Handoff: API designer defines authentication needs → Security implements auth
- Collaboration: Rate limiting, API key management, OAuth flows
- Critical: JWT validation, API gateway security policies

**devops-engineer:**
- Handoff: API design finalized → DevOps deploys API gateway
- Collaboration: API versioning deployment, blue-green releases
- Tools: Kong, AWS API Gateway, Traefik configuration

---
