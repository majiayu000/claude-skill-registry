---
name: api-doc-generation
description: "Generate and update API documentation from NestJS controllers. Use when modifying controllers, adding endpoints, or when the user asks about API documentation."
event: controller-change
auto_trigger: true
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - controller_files
  - existing_api_docs
  - dto_files
output: updated_api_docs
output_format: "Markdown API doc (04-API-DESIGN-TEMPLATE.md)"
output_path: "docs/technical/backend/api/"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "controller-change"
    - "api-endpoint-added"
  file_patterns:
    - "apps/api/**/*.controller.ts"
    - "apps/api/**/*.dto.ts"
  conditions:
    - "controller file modified"
    - "new endpoint added"

# Validation
validation_rules:
  - "all endpoints documented"
  - "request/response DTOs included"
  - "status codes listed"

# Chaining
chain_after: []
chain_before: [doc-index-update]

# Agent Association
called_by: ["@Backend"]
mcp_tools:
  - grep_search
  - read_file
  - mcp_payment-syste_query_docs_by_type
---

# API Documentation Generation Skill

> **Purpose:** Generate and update API documentation from NestJS controllers. Keeps API docs in sync with implementation.

## Trigger

**When:** Controller files (`*.controller.ts`) are modified
**Context Needed:** Controller code, DTOs, existing API docs
**MCP Tools:** `grep_search`, `read_file`, `mcp_payment-syste_query_docs_by_type`

## Controller → Doc Mapping

Parse NestJS decorators to extract:

```typescript
@Controller('products')          // Base path: /api/v1/products
@Get(':id')                      // GET /api/v1/products/:id
@Post()                          // POST /api/v1/products
@UseGuards(JwtAuthGuard)         // Auth required
@ApiOperation({ summary: '...'}) // Description
```

## Extraction Rules

| Decorator                 | Extracted Info |
| :------------------------ | :------------- |
| `@Controller(path)`       | Base path      |
| `@Get/@Post/@Put/@Delete` | HTTP method    |
| `@Param/@Query/@Body`     | Parameters     |
| `@UseGuards`              | Authentication |
| `@ApiOperation`           | Description    |
| `@ApiResponse`            | Response codes |

## API Doc Format

````markdown
### GET /api/v1/products/:id

**Description:** Get product by ID

**Authentication:** Required (JWT)

**Parameters:**

| Name | In   | Type   | Required | Description |
| :--- | :--- | :----- | :------- | :---------- |
| id   | path | string | Yes      | Product ID  |

**Responses:**

| Code | Description | Schema             |
| :--- | :---------- | :----------------- |
| 200  | Success     | ProductResponseDto |
| 404  | Not found   | ErrorDto           |

**Example Request:**

```bash
curl -X GET /api/v1/products/abc123 \
  -H "Authorization: Bearer {token}"
```
````

````

## Frontmatter Template

```yaml
---
document_type: "api-design"
module: "[module]"
status: "approved"
version: "1.0.0"
last_updated: "YYYY-MM-DD"
author: "@Backend"

keywords:
  - "api"
  - "rest"
  - "[module]"

api_metadata:
  base_path: "/api/v1/[resource]"
  auth_required: true
  rate_limited: true
---
````

## Workflow

1. **Detect changes** - Which controllers changed?
2. **Parse decorators** - Extract API metadata
3. **Load DTOs** - Get request/response types
4. **Find existing doc** - Match by module
5. **Update endpoints** - Add/modify/remove
6. **Bump version** - If endpoints changed
7. **Update date** - Set last_updated

## DTO Extraction

```typescript
// From DTO class
export class CreateProductDto {
  @IsString()
  @MinLength(1)
  name: string;

  @IsOptional()
  @IsNumber()
  price?: number;
}

// Generate table
| Field | Type | Required | Validation |
| name | string | Yes | MinLength(1) |
| price | number | No | - |
```

## Reference

- [04-API-DESIGN-TEMPLATE.md](/docs/templates/04-API-DESIGN-TEMPLATE.md)
- [backend.instructions.md](../instructions/backend.instructions.md)
