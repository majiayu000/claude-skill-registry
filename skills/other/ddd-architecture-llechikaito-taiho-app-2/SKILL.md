---
globs:
  - "backend/src/domain/**/*.ts"
  - "backend/src/application/**/*.ts"
  - "backend/src/infrastructure/**/*.ts"
  - "backend/src/presentation/**/*.ts"
  - "backend/src/container/**/*.ts"
---

# DDD Architecture Skill

## Description
ドメイン駆動設計（DDD）に準拠したバックエンドコードを書くためのスキルです。

## Automatic Activation
このスキルは以下のファイルを編集する際に自動で適用されます：
- `backend/src/domain/**/*.ts` - エンティティ、リポジトリIF
- `backend/src/application/**/*.ts` - ユースケース、DTO、サービス
- `backend/src/infrastructure/**/*.ts` - DynamoDB実装、マッパー
- `backend/src/presentation/**/*.ts` - コントローラー、ルート
- `backend/src/container/**/*.ts` - DIコンテナ

## Architecture Layers

```
Presentation Layer (コントローラー、ルート)
    ↓
Application Layer (ユースケース、アプリケーションサービス)
    ↓
Domain Layer (エンティティ、リポジトリインターフェース)
    ↑
Infrastructure Layer (DynamoDBリポジトリ実装)
```

## Directory Structure

```
backend/src/
├── domain/
│   ├── entities/{feature}/      # エンティティ定義
│   └── repositories/{feature}/  # リポジトリインターフェース
├── application/
│   ├── dto/{feature}/           # Data Transfer Objects
│   ├── usecases/{feature}/      # ユースケース
│   └── services/{feature}/      # アプリケーションサービス
├── infrastructure/
│   ├── repositories/{feature}/  # DynamoDB実装
│   └── mappers/{feature}/       # エンティティ⇔DBマッパー
└── presentation/
    ├── controllers/{feature}/   # コントローラー
    └── routes/{feature}/        # ルーティング
```

## Implementation Rules

### 1. Domain Layer
- エンティティはビジネスロジックを持つ
- リポジトリはインターフェースのみ定義
- 外部依存を持たない

### 2. Application Layer
- ユースケースは1つの操作を表す
- DTOで入出力を定義
- ドメインオブジェクトを操作

### 3. Infrastructure Layer
- リポジトリインターフェースを実装
- DynamoDBとの通信を担当
- マッパーでエンティティ変換

### 4. Presentation Layer
- HTTPリクエスト/レスポンスを処理
- 認証・認可のミドルウェア適用
- Swagger定義も更新

## New Feature Checklist

新機能追加時は以下を全て実装:

- [ ] `domain/entities/{feature}/{Feature}.ts`
- [ ] `domain/repositories/{feature}/{Feature}Repository.ts`
- [ ] `application/dto/{feature}/{Feature}Dto.ts`
- [ ] `application/usecases/{feature}/{Feature}UseCase.ts`
- [ ] `infrastructure/repositories/{feature}/DynamoDB{Feature}Repository.ts`
- [ ] `infrastructure/mappers/{feature}/{Feature}Mapper.ts`
- [ ] `presentation/controllers/{feature}/{Feature}Controller.ts`
- [ ] `presentation/routes/{feature}/{feature}Routes.ts`
- [ ] `container/Container.ts` にDI登録
- [ ] `server.ts` にルート追加
- [ ] `config/swagger.ts` にAPI定義追加

## Naming Conventions

| 種類 | 命名規則 | 例 |
|-----|---------|-----|
| エンティティ | PascalCase | `Order`, `MenuItem` |
| リポジトリIF | PascalCase + Repository | `OrderRepository` |
| リポジトリ実装 | DynamoDB + PascalCase + Repository | `DynamoDBOrderRepository` |
| ユースケース | PascalCase + UseCase | `CreateOrderUseCase` |
| コントローラー | PascalCase + Controller | `OrderController` |
| ルート | camelCase + Routes | `orderRoutes` |
| DTO | PascalCase + Dto | `CreateOrderDto` |
