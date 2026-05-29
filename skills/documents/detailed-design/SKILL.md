---
name: detailed-design
description: 詳細設計書作成エージェント。クラス設計、シーケンス図、DB設計、API設計の詳細を定義。キーワード: 詳細設計, detailed design, クラス図, class diagram, シーケンス図, sequence diagram, DB設計.
---

# 詳細設計書作成エージェント

## 役割
基本設計に基づいた詳細設計を担当します。

## 設計書構成

```
docs/design/
├── detailed/
│   ├── 00-overview.md           # 詳細設計概要
│   ├── 01-class-design.md       # クラス設計
│   ├── 02-sequence-design.md    # シーケンス設計
│   ├── 03-database-design.md    # データベース設計
│   ├── 04-api-design.md         # API設計
│   ├── 05-error-handling.md     # エラーハンドリング設計
│   └── modules/
│       ├── auth-module.md       # 認証モジュール
│       ├── user-module.md       # ユーザーモジュール
│       └── ...
└── diagrams/
    ├── class/                   # クラス図
    ├── sequence/                # シーケンス図
    └── er/                      # ER図
```

## 詳細設計書テンプレート

### 1. クラス設計 (01-class-design.md)

```markdown
# クラス設計

## クラス図

classDiagram
    class User {
        -id: UUID
        -email: string
        -passwordHash: string
        -name: string
        -createdAt: DateTime
        -updatedAt: DateTime
        +create(dto: CreateUserDto): User
        +update(dto: UpdateUserDto): void
        +validatePassword(password: string): boolean
    }

    class UserRepository {
        <<interface>>
        +findById(id: UUID): User
        +findByEmail(email: string): User
        +save(user: User): void
        +delete(id: UUID): void
    }

    class UserService {
        -repository: UserRepository
        -passwordEncoder: PasswordEncoder
        +register(dto: CreateUserDto): User
        +authenticate(email: string, password: string): AuthResult
        +updateProfile(id: UUID, dto: UpdateUserDto): User
    }

    UserService --> UserRepository
    UserService --> User
    UserRepository --> User

## クラス一覧

### エンティティ

| クラス名 | 責務 | パッケージ |
|---------|------|-----------|
| User | ユーザー情報を保持 | domain.entity |
| Order | 注文情報を保持 | domain.entity |
| Product | 商品情報を保持 | domain.entity |

### サービス

| クラス名 | 責務 | 依存先 |
|---------|------|--------|
| UserService | ユーザー管理 | UserRepository |
| OrderService | 注文管理 | OrderRepository, ProductService |
| AuthService | 認証処理 | UserRepository, TokenService |

### リポジトリ

| インターフェース | 実装クラス | 説明 |
|----------------|-----------|------|
| UserRepository | UserRepositoryImpl | ユーザーデータアクセス |
| OrderRepository | OrderRepositoryImpl | 注文データアクセス |
```

### 2. シーケンス設計 (02-sequence-design.md)

```markdown
# シーケンス設計

## ユーザー登録シーケンス

sequenceDiagram
    participant C as Client
    participant Ctrl as UserController
    participant Svc as UserService
    participant Repo as UserRepository
    participant DB as Database
    participant Email as EmailService

    C->>Ctrl: POST /api/users
    Ctrl->>Ctrl: validateRequest()
    Ctrl->>Svc: register(createUserDto)

    Svc->>Repo: findByEmail(email)
    Repo->>DB: SELECT * FROM users WHERE email = ?
    DB-->>Repo: null (not found)
    Repo-->>Svc: null

    Svc->>Svc: hashPassword(password)
    Svc->>Repo: save(user)
    Repo->>DB: INSERT INTO users ...
    DB-->>Repo: success
    Repo-->>Svc: user

    Svc->>Email: sendVerificationEmail(user)
    Email-->>Svc: success

    Svc-->>Ctrl: user
    Ctrl-->>C: 201 Created

## エラー時のシーケンス

sequenceDiagram
    participant C as Client
    participant Ctrl as UserController
    participant Svc as UserService
    participant Repo as UserRepository

    C->>Ctrl: POST /api/users (duplicate email)
    Ctrl->>Svc: register(createUserDto)
    Svc->>Repo: findByEmail(email)
    Repo-->>Svc: existingUser
    Svc-->>Ctrl: throw DuplicateEmailException
    Ctrl-->>C: 409 Conflict
```

### 3. データベース設計 (03-database-design.md)

```markdown
# データベース設計

## ER図

erDiagram
    USERS ||--o{ ORDERS : places
    USERS {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar name
        timestamp created_at
        timestamp updated_at
    }

    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS {
        uuid id PK
        uuid user_id FK
        varchar status
        decimal total_amount
        timestamp ordered_at
    }

    PRODUCTS ||--o{ ORDER_ITEMS : includes
    PRODUCTS {
        uuid id PK
        varchar name
        text description
        decimal price
        int stock
    }

    ORDER_ITEMS {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
    }

## テーブル定義

### users テーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | UUID | NO | gen_random_uuid() | 主キー |
| email | VARCHAR(255) | NO | - | メールアドレス（UK） |
| password_hash | VARCHAR(255) | NO | - | パスワードハッシュ |
| name | VARCHAR(100) | NO | - | 表示名 |
| status | VARCHAR(20) | NO | 'active' | ステータス |
| created_at | TIMESTAMP | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | NO | CURRENT_TIMESTAMP | 更新日時 |

#### インデックス
| インデックス名 | カラム | 種別 |
|---------------|--------|------|
| users_pkey | id | PRIMARY |
| users_email_key | email | UNIQUE |
| idx_users_status | status | INDEX |

### DDL

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_status ON users(status);
```

## マイグレーション方針

| 項目 | 方針 |
|------|------|
| ツール | Flyway / Alembic |
| 命名規則 | V{version}__{description}.sql |
| ロールバック | 各マイグレーションにDOWNスクリプト必須 |
```

### 4. エラーハンドリング設計 (05-error-handling.md)

```markdown
# エラーハンドリング設計

## エラーコード体系

| コード範囲 | カテゴリ | 例 |
|-----------|---------|-----|
| 1000-1999 | 認証・認可 | 1001: 認証失敗 |
| 2000-2999 | バリデーション | 2001: 必須項目不足 |
| 3000-3999 | ビジネスロジック | 3001: 在庫不足 |
| 4000-4999 | 外部連携 | 4001: 外部API障害 |
| 9000-9999 | システム | 9001: 内部エラー |

## エラーレスポンス形式

```json
{
  "error": {
    "code": "2001",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "traceId": "abc123-def456"
  }
}
```

## HTTPステータスマッピング

| エラーコード範囲 | HTTPステータス |
|-----------------|---------------|
| 1000-1999 | 401, 403 |
| 2000-2999 | 400 |
| 3000-3999 | 409, 422 |
| 4000-4999 | 502, 503 |
| 9000-9999 | 500 |

## 例外クラス階層

```
ApplicationException (base)
├── AuthenticationException (1000)
├── AuthorizationException (1100)
├── ValidationException (2000)
├── BusinessException (3000)
│   ├── ResourceNotFoundException (3100)
│   ├── DuplicateResourceException (3200)
│   └── InsufficientStockException (3300)
├── ExternalServiceException (4000)
└── SystemException (9000)
```
```

## モジュール別詳細設計

### 認証モジュール (modules/auth-module.md)

```markdown
# 認証モジュール詳細設計

## 概要
JWT based認証を提供するモジュール

## クラス構成

| クラス | 責務 |
|--------|------|
| AuthController | 認証エンドポイント |
| AuthService | 認証ロジック |
| JwtTokenProvider | JWT生成・検証 |
| PasswordEncoder | パスワードハッシュ |

## 処理フロー

### ログイン
1. email/passwordを受け取る
2. ユーザー検索
3. パスワード検証
4. JWT生成（access + refresh）
5. レスポンス返却

### トークンリフレッシュ
1. refresh tokenを受け取る
2. token検証
3. 新しいaccess token生成
4. レスポンス返却

## 設定値

| 項目 | 値 | 環境変数 |
|------|-----|---------|
| Access Token有効期限 | 1時間 | JWT_ACCESS_EXPIRY |
| Refresh Token有効期限 | 7日 | JWT_REFRESH_EXPIRY |
| 署名アルゴリズム | RS256 | - |
```

## 出力形式

詳細設計書作成時の成果物：

1. **設計書ファイル**: `docs/design/detailed/*.md`
2. **モジュール設計**: `docs/design/detailed/modules/*.md`
3. **図表ファイル**: `docs/design/diagrams/{class,sequence,er}/*.mmd`
4. **DDL**: `docs/design/detailed/ddl/*.sql`

## 関連スキル

- 基本設計書エージェント: 基本設計を参照
- API仕様書エージェント: API設計を詳細化
- 実装エージェント: 詳細設計に基づいて実装
- 単体テストエージェント: 設計に基づいてテスト作成
