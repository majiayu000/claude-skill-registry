---
name: api-docs-generator
description: Generate API documentation in OpenAPI/Swagger, Markdown, or Postman Collection formats. Use when documenting REST APIs, GraphQL schemas, or creating client code examples.
---

# API Documentation Generator Skill

APIドキュメントを自動生成するスキルです。

## 概要

このスキルは、ソースコードから美しく、詳細で、インタラクティブなAPIドキュメントを自動生成します。OpenAPI/Swagger、Markdown、HTML、Postman Collection等の多様な形式に対応し、開発者に優しいドキュメントを作成します。

## 主な機能

- **OpenAPI/Swagger仕様生成**: REST APIの標準仕様
- **Markdown形式**: GitHub/GitLab対応
- **インタラクティブHTML**: 試せるAPIドキュメント
- **Postman Collection**: インポート可能なコレクション
- **GraphQL Schema**: GraphQL APIのドキュメント
- **コード例生成**: 複数言語のクライアントコード
- **認証ドキュメント**: OAuth、JWT、API Key等の説明
- **エラーコードリファレンス**: 包括的なエラー情報
- **レート制限情報**: 制限とベストプラクティス
- **バージョニング**: API バージョン管理

## サポートフレームワーク

### REST API
- **Express.js** (Node.js)
- **FastAPI** (Python)
- **Flask** (Python)
- **Django REST Framework** (Python)
- **Spring Boot** (Java)
- **ASP.NET Core** (C#)
- **Gin/Echo** (Go)
- **Rails** (Ruby)
- **Laravel** (PHP)

### GraphQL
- **Apollo Server**
- **GraphQL Yoga**
- **Hasura**

## 使用方法

### 基本的なドキュメント生成

```
このAPIエンドポイントのドキュメントを生成：

GET /api/users/{id}

実装コード:
[コードを貼り付け]

形式: OpenAPI 3.0
```

### コントローラー全体

```
このコントローラーの完全なAPIドキュメントを生成：
- すべてのエンドポイント
- リクエスト/レスポンス例
- エラーケース
- 認証要件

[コントローラーコード]
```

### プロジェクト全体

```
プロジェクト全体のAPIドキュメントを生成：
フレームワーク: Express.js
出力形式: OpenAPI 3.0 + Swagger UI
含める内容:
- 認証フロー
- すべてのエンドポイント
- データモデル
- エラーコード
```

## 出力形式

### 1. OpenAPI/Swagger 3.0

```yaml
openapi: 3.0.0
info:
  title: User Management API
  description: API for managing users in the system
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: Get all users
      description: Retrieve a paginated list of users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          description: Page number (starts at 1)
          required: false
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
              examples:
                success:
                  value:
                    data:
                      - id: 1
                        name: John Doe
                        email: john@example.com
                        created_at: "2024-01-15T10:30:00Z"
                      - id: 2
                        name: Jane Smith
                        email: jane@example.com
                        created_at: "2024-01-16T14:20:00Z"
                    pagination:
                      page: 1
                      limit: 20
                      total: 2
                      total_pages: 1
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalServerError'
      security:
        - bearerAuth: []

    post:
      summary: Create a new user
      description: Create a new user with the provided information
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
                - password
              properties:
                name:
                  type: string
                  minLength: 2
                  maxLength: 100
                  example: John Doe
                email:
                  type: string
                  format: email
                  example: john@example.com
                password:
                  type: string
                  format: password
                  minLength: 8
                  example: SecurePass123!
            examples:
              user:
                value:
                  name: John Doe
                  email: john@example.com
                  password: SecurePass123!
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{id}:
    get:
      summary: Get user by ID
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          description: User ID
          schema:
            type: integer
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        total_pages:
          type: integer

    Error:
      type: object
      properties:
        error:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### 2. Markdown形式

```markdown
# User Management API Documentation

Version: 1.0.0

Base URL: `https://api.example.com/v1`

## Authentication

This API uses JWT Bearer token authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

To obtain a token, use the `/auth/login` endpoint.

## Endpoints

### Get All Users

Retrieve a paginated list of users.

**Endpoint:** `GET /users`

**Authentication:** Required

**Query Parameters:**

| Parameter | Type    | Required | Default | Description                |
|-----------|---------|----------|---------|----------------------------|
| page      | integer | No       | 1       | Page number (starts at 1)  |
| limit     | integer | No       | 20      | Items per page (max: 100)  |

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=20" \
  -H "Authorization: Bearer your-token-here"
```

**Success Response (200 OK):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50,
    "total_pages": 3
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: Server error

### Create User

Create a new user account.

**Endpoint:** `POST /users`

**Authentication:** Admin only

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Field Validation:**

| Field    | Type   | Required | Constraints              |
|----------|--------|----------|--------------------------|
| name     | string | Yes      | 2-100 characters         |
| email    | string | Yes      | Valid email format       |
| password | string | Yes      | Min 8 chars, mixed case  |

**Example Request:**

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer your-admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Success Response (201 Created):**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-20T15:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions

## Error Codes

| Code | Message                  | Description                        |
|------|--------------------------|----------------------------------- |
| 1001 | Invalid email format     | Email doesn't match required format|
| 1002 | Email already exists     | Account with this email exists     |
| 1003 | Password too weak        | Password doesn't meet requirements |
| 2001 | User not found           | User ID doesn't exist              |
| 3001 | Unauthorized access      | Missing or invalid authentication  |

## Rate Limiting

- **Limit:** 1000 requests per hour per API key
- **Headers:** Check `X-RateLimit-*` headers in responses
- **Exceeded:** Returns `429 Too Many Requests`

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642684800
```
```

### 3. インタラクティブHTML (Swagger UI)

```html
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "openapi.yaml",
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true
      })
    }
  </script>
</body>
</html>
```

### 4. Postman Collection

```json
{
  "info": {
    "name": "User Management API",
    "description": "API for managing users",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [{
      "key": "token",
      "value": "{{jwt_token}}",
      "type": "string"
    }]
  },
  "variable": [{
    "key": "base_url",
    "value": "https://api.example.com/v1"
  }],
  "item": [
    {
      "name": "Users",
      "item": [
        {
          "name": "Get All Users",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/users?page=1&limit=20",
              "host": ["{{base_url}}"],
              "path": ["users"],
              "query": [
                {"key": "page", "value": "1"},
                {"key": "limit", "value": "20"}
              ]
            }
          }
        },
        {
          "name": "Create User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john@example.com\",\n  \"password\": \"SecurePass123!\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/users",
              "host": ["{{base_url}}"],
              "path": ["users"]
            }
          }
        }
      ]
    }
  ]
}
```

## コード例生成

### JavaScript/Node.js

```javascript
// Get all users
const response = await fetch('https://api.example.com/v1/users?page=1&limit=20', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});
const data = await response.json();

// Create user
const newUser = await fetch('https://api.example.com/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});
```

### Python

```python
import requests

# Get all users
headers = {'Authorization': 'Bearer YOUR_TOKEN'}
response = requests.get(
    'https://api.example.com/v1/users',
    params={'page': 1, 'limit': 20},
    headers=headers
)
users = response.json()

# Create user
new_user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'SecurePass123!'
}
response = requests.post(
    'https://api.example.com/v1/users',
    json=new_user_data,
    headers=headers
)
```

### cURL

```bash
# Get all users
curl -X GET "https://api.example.com/v1/users?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create user
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"SecurePass123!"}'
```

## GraphQL ドキュメント

```graphql
"""
User type representing a user in the system
"""
type User {
  """Unique identifier"""
  id: ID!

  """User's full name"""
  name: String!

  """User's email address"""
  email: String!

  """Account creation timestamp"""
  createdAt: DateTime!

  """Last update timestamp"""
  updatedAt: DateTime!
}

type Query {
  """
  Get all users with pagination

  Arguments:
  - page: Page number (default: 1)
  - limit: Items per page (default: 20, max: 100)
  """
  users(page: Int = 1, limit: Int = 20): UserConnection!

  """
  Get a specific user by ID

  Returns null if user doesn't exist
  """
  user(id: ID!): User
}

type Mutation {
  """
  Create a new user

  Errors:
  - EMAIL_EXISTS: Email already registered
  - INVALID_INPUT: Validation failed
  """
  createUser(input: CreateUserInput!): User!

  """Update existing user"""
  updateUser(id: ID!, input: UpdateUserInput!): User!

  """Delete user"""
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  """User's full name (2-100 chars)"""
  name: String!

  """Valid email address"""
  email: String!

  """Password (min 8 chars)"""
  password: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

## ベストプラクティス

### 1. 詳細な説明

- エンドポイントの目的を明確に記述
- パラメータの意味と制約を説明
- 典型的な使用例を提供

### 2. リアルな例

- 実際のデータに近い例を使用
- 成功とエラーの両方のケースを含める
- エッジケースも文書化

### 3. バージョニング

- APIバージョンを明記
- 変更履歴を記録
- 非推奨機能の移行ガイド

### 4. セキュリティ

- 認証方法を明確に説明
- 権限要件を文書化
- セキュリティのベストプラクティスを提供

## カスタマイズ

```
以下の要件でAPIドキュメントを生成：

- 出力形式: OpenAPI 3.0 + Markdown
- 認証: OAuth 2.0
- コード例言語: JavaScript, Python, Go
- エラーコード: 完全なリファレンス
- レート制限: 詳細情報を含める
- バージョン: v2.0
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
このExpressルーターのAPIドキュメントを生成：

router.get('/api/products', async (req, res) => {
  const { category, minPrice, maxPrice } = req.query;
  const products = await Product.find({ category, price: { $gte: minPrice, $lte: maxPrice } });
  res.json(products);
});

形式: OpenAPI 3.0 + Markdown
コード例: JavaScript, Python
```

完全なAPIドキュメントが生成されます！
