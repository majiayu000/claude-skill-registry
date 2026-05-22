---
name: api-spec
description: API仕様書作成エージェント。OpenAPI/Swagger形式のAPI定義、リクエスト/レスポンス仕様、認証仕様を作成。キーワード: API仕様, api spec, OpenAPI, Swagger, REST API, エンドポイント.
---

# API仕様書作成エージェント

## 役割
RESTful APIの仕様書をOpenAPI形式で作成します。

## 仕様書構成

```
docs/api/
├── openapi.yaml             # メインOpenAPI定義
├── schemas/                 # スキーマ定義
│   ├── user.yaml
│   ├── order.yaml
│   └── common.yaml
├── paths/                   # エンドポイント定義
│   ├── auth.yaml
│   ├── users.yaml
│   └── orders.yaml
└── examples/                # リクエスト/レスポンス例
    ├── user-examples.yaml
    └── order-examples.yaml
```

## OpenAPI テンプレート

### メイン定義 (openapi.yaml)

```yaml
openapi: 3.0.3
info:
  title: [プロジェクト名] API
  description: |
    [プロジェクトの説明]

    ## 認証
    Bearer Tokenによる認証を使用します。
    `Authorization: Bearer <token>` ヘッダーを付与してください。

  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging
  - url: http://localhost:8000/v1
    description: Development

tags:
  - name: auth
    description: 認証関連
  - name: users
    description: ユーザー管理
  - name: orders
    description: 注文管理

security:
  - bearerAuth: []

paths:
  $ref: './paths/_index.yaml'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    $ref: './schemas/_index.yaml'

  responses:
    BadRequest:
      description: Bad Request
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
      description: Not Found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### エンドポイント定義 (paths/users.yaml)

```yaml
/users:
  get:
    tags:
      - users
    summary: ユーザー一覧取得
    description: 登録されているユーザーの一覧を取得します
    operationId: getUsers
    parameters:
      - name: page
        in: query
        description: ページ番号
        schema:
          type: integer
          default: 1
          minimum: 1
      - name: limit
        in: query
        description: 1ページあたりの件数
        schema:
          type: integer
          default: 20
          minimum: 1
          maximum: 100
      - name: status
        in: query
        description: ステータスでフィルタ
        schema:
          type: string
          enum: [active, inactive, suspended]
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '../schemas/user.yaml#/User'
                pagination:
                  $ref: '../schemas/common.yaml#/Pagination'
      '401':
        $ref: '../openapi.yaml#/components/responses/Unauthorized'

  post:
    tags:
      - users
    summary: ユーザー作成
    description: 新規ユーザーを作成します
    operationId: createUser
    security: []  # 認証不要
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '../schemas/user.yaml#/CreateUserRequest'
          example:
            email: user@example.com
            password: SecurePass123!
            name: 山田太郎
    responses:
      '201':
        description: 作成成功
        content:
          application/json:
            schema:
              $ref: '../schemas/user.yaml#/User'
      '400':
        $ref: '../openapi.yaml#/components/responses/BadRequest'
      '409':
        description: メールアドレス重複
        content:
          application/json:
            schema:
              $ref: '../schemas/common.yaml#/Error'

/users/{userId}:
  get:
    tags:
      - users
    summary: ユーザー詳細取得
    operationId: getUser
    parameters:
      - name: userId
        in: path
        required: true
        description: ユーザーID
        schema:
          type: string
          format: uuid
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              $ref: '../schemas/user.yaml#/User'
      '404':
        $ref: '../openapi.yaml#/components/responses/NotFound'

  put:
    tags:
      - users
    summary: ユーザー更新
    operationId: updateUser
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '../schemas/user.yaml#/UpdateUserRequest'
    responses:
      '200':
        description: 更新成功
        content:
          application/json:
            schema:
              $ref: '../schemas/user.yaml#/User'

  delete:
    tags:
      - users
    summary: ユーザー削除
    operationId: deleteUser
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid
    responses:
      '204':
        description: 削除成功
```

### スキーマ定義 (schemas/user.yaml)

```yaml
User:
  type: object
  properties:
    id:
      type: string
      format: uuid
      description: ユーザーID
      example: 550e8400-e29b-41d4-a716-446655440000
    email:
      type: string
      format: email
      description: メールアドレス
      example: user@example.com
    name:
      type: string
      description: 表示名
      example: 山田太郎
    status:
      type: string
      enum: [active, inactive, suspended]
      description: ステータス
      example: active
    createdAt:
      type: string
      format: date-time
      description: 作成日時
    updatedAt:
      type: string
      format: date-time
      description: 更新日時
  required:
    - id
    - email
    - name
    - status
    - createdAt
    - updatedAt

CreateUserRequest:
  type: object
  properties:
    email:
      type: string
      format: email
      description: メールアドレス
      maxLength: 255
    password:
      type: string
      format: password
      description: パスワード（8文字以上、英数字記号混在）
      minLength: 8
      maxLength: 100
    name:
      type: string
      description: 表示名
      minLength: 1
      maxLength: 100
  required:
    - email
    - password
    - name

UpdateUserRequest:
  type: object
  properties:
    name:
      type: string
      minLength: 1
      maxLength: 100
    status:
      type: string
      enum: [active, inactive]
```

### 共通スキーマ (schemas/common.yaml)

```yaml
Error:
  type: object
  properties:
    error:
      type: object
      properties:
        code:
          type: string
          description: エラーコード
          example: "2001"
        message:
          type: string
          description: エラーメッセージ
          example: "Validation failed"
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
        traceId:
          type: string
          description: トレースID
          example: "abc123-def456"

Pagination:
  type: object
  properties:
    page:
      type: integer
      description: 現在のページ
      example: 1
    limit:
      type: integer
      description: 1ページあたりの件数
      example: 20
    totalItems:
      type: integer
      description: 総件数
      example: 100
    totalPages:
      type: integer
      description: 総ページ数
      example: 5
```

## API設計ガイドライン

### URL設計

| パターン | 用途 | 例 |
|---------|------|-----|
| GET /resources | 一覧取得 | GET /users |
| GET /resources/{id} | 詳細取得 | GET /users/123 |
| POST /resources | 作成 | POST /users |
| PUT /resources/{id} | 全体更新 | PUT /users/123 |
| PATCH /resources/{id} | 部分更新 | PATCH /users/123 |
| DELETE /resources/{id} | 削除 | DELETE /users/123 |

### ステータスコード

| コード | 用途 |
|--------|------|
| 200 | 成功（GET, PUT, PATCH） |
| 201 | 作成成功（POST） |
| 204 | 成功・レスポンスなし（DELETE） |
| 400 | バリデーションエラー |
| 401 | 認証エラー |
| 403 | 認可エラー |
| 404 | リソース未発見 |
| 409 | 競合（重複など） |
| 422 | ビジネスロジックエラー |
| 500 | サーバーエラー |

### ページネーション

```
GET /users?page=2&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "totalItems": 100,
    "totalPages": 5
  }
}
```

## コマンド

```bash
# OpenAPI仕様の検証
npx @redocly/cli lint docs/api/openapi.yaml

# ドキュメント生成
npx @redocly/cli build-docs docs/api/openapi.yaml -o docs/api-docs.html

# モックサーバー起動
npx prism mock docs/api/openapi.yaml

# クライアントコード生成
npx openapi-generator-cli generate -i docs/api/openapi.yaml -g typescript-axios -o src/api
```

## 出力形式

API仕様書作成時の成果物：

1. **OpenAPI定義**: `docs/api/openapi.yaml`
2. **スキーマ定義**: `docs/api/schemas/*.yaml`
3. **パス定義**: `docs/api/paths/*.yaml`
4. **HTMLドキュメント**: `docs/api-docs.html`（生成）

## 関連スキル

- 基本設計書エージェント: API全体設計を参照
- 詳細設計書エージェント: 内部実装設計と連携
- 実装エージェント: API仕様に基づいて実装
- E2Eテストエージェント: APIテストを作成
