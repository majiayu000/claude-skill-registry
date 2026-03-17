---
name: synthetic-data-generator
description: テスト用の合成データ生成スキル。リアルなユーザーデータ、トランザクション、ログ、APIレスポンス等を生成。GDPR準拠、フェイカー連携、スキーマベース生成、時系列データ、異常データ生成に対応。
---

# Synthetic Data Generator Skill

テスト・開発用のリアルな合成データを生成するスキルです。

## 概要

このスキルは、開発・テスト・デモ用のリアルで多様な合成データを生成します。個人情報を含まない安全なテストデータ、エッジケースのシミュレーション、パフォーマンステスト用の大量データなど、様々なニーズに対応します。

## 主な機能

- **ユーザーデータ生成**: 名前、メール、住所、電話番号など
- **トランザクションデータ**: 購買履歴、決済情報、注文データ
- **ログデータ**: アプリケーションログ、アクセスログ、エラーログ
- **時系列データ**: センサーデータ、メトリクス、株価
- **関係データ**: 正規化されたDB用データ（外部キー関係含む）
- **APIレスポンス**: REST/GraphQL APIのモックレスポンス
- **異常データ**: エッジケース、エラーシナリオ
- **GDPR準拠**: 実在しない個人情報のみ生成
- **複数形式対応**: JSON, CSV, SQL, XML, YAML
- **カスタムスキーマ**: JSONスキーマ、OpenAPI、TypeScript型定義からデータ生成

## データタイプ

### 1. 個人情報（PII）

#### ユーザープロフィール

```json
{
  "id": "usr_7f3k9m2p",
  "firstName": "太郎",
  "lastName": "山田",
  "email": "taro.yamada.test@example.com",
  "phone": "090-1234-5678",
  "dateOfBirth": "1990-05-15",
  "address": {
    "country": "Japan",
    "postalCode": "150-0001",
    "prefecture": "東京都",
    "city": "渋谷区",
    "street": "神宮前1-2-3",
    "building": "テストビル 405号室"
  },
  "createdAt": "2023-01-15T10:30:00Z",
  "lastLogin": "2024-11-20T14:22:33Z"
}
```

#### 企業情報

```json
{
  "companyId": "com_9x4j2k7n",
  "companyName": "テックイノベーション株式会社",
  "industry": "IT・ソフトウェア",
  "employeeCount": 250,
  "founded": "2015-04-01",
  "website": "https://techinnovation-test.example.com",
  "email": "info@techinnovation-test.example.com",
  "phone": "03-1234-5678",
  "address": {
    "country": "Japan",
    "postalCode": "100-0001",
    "prefecture": "東京都",
    "city": "千代田区",
    "street": "丸の内1-1-1"
  }
}
```

### 2. トランザクションデータ

#### 購買データ

```json
{
  "orderId": "ord_20241122_001",
  "customerId": "usr_7f3k9m2p",
  "orderDate": "2024-11-22T09:15:00Z",
  "status": "completed",
  "items": [
    {
      "productId": "prod_laptop_001",
      "productName": "ノートパソコン ProBook 15",
      "category": "Electronics",
      "quantity": 1,
      "unitPrice": 89800,
      "discount": 5000,
      "subtotal": 84800
    },
    {
      "productId": "prod_mouse_042",
      "productName": "ワイヤレスマウス",
      "category": "Accessories",
      "quantity": 2,
      "unitPrice": 2980,
      "discount": 0,
      "subtotal": 5960
    }
  ],
  "subtotal": 90760,
  "tax": 9076,
  "shipping": 0,
  "total": 99836,
  "paymentMethod": "credit_card",
  "shippingAddress": {
    "name": "山田 太郎",
    "postalCode": "150-0001",
    "prefecture": "東京都",
    "city": "渋谷区",
    "street": "神宮前1-2-3",
    "phone": "090-1234-5678"
  }
}
```

#### 決済データ

```json
{
  "transactionId": "txn_20241122_001",
  "orderId": "ord_20241122_001",
  "amount": 99836,
  "currency": "JPY",
  "paymentMethod": "credit_card",
  "cardLast4": "1234",
  "cardBrand": "VISA",
  "status": "succeeded",
  "timestamp": "2024-11-22T09:16:12Z",
  "gatewayResponse": {
    "authCode": "AUTH123456",
    "transactionRef": "ref_abc123xyz"
  }
}
```

### 3. ログデータ

#### アプリケーションログ

```json
{
  "timestamp": "2024-11-22T10:15:32.456Z",
  "level": "INFO",
  "service": "user-service",
  "environment": "production",
  "traceId": "trace_7f3k9m2p4j",
  "spanId": "span_2x9k4n",
  "userId": "usr_7f3k9m2p",
  "action": "user.login",
  "message": "User logged in successfully",
  "metadata": {
    "ipAddress": "192.168.1.100",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "sessionId": "sess_abc123xyz"
  },
  "duration": 234
}
```

#### エラーログ

```json
{
  "timestamp": "2024-11-22T10:16:45.789Z",
  "level": "ERROR",
  "service": "payment-service",
  "environment": "production",
  "traceId": "trace_err_5k2m9p",
  "error": {
    "type": "PaymentGatewayError",
    "message": "Payment gateway timeout",
    "code": "GATEWAY_TIMEOUT",
    "stack": "at processPayment (payment.js:45:12)..."
  },
  "context": {
    "orderId": "ord_20241122_002",
    "amount": 15000,
    "retryCount": 2
  }
}
```

#### アクセスログ（Apache/Nginx形式）

```
192.168.1.100 - - [22/Nov/2024:10:15:32 +0900] "GET /api/users/profile HTTP/1.1" 200 1234 "https://example.com/dashboard" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 0.234
192.168.1.101 - - [22/Nov/2024:10:15:33 +0900] "POST /api/orders HTTP/1.1" 201 567 "https://example.com/cart" "Mozilla/5.0 (Macintosh; Intel Mac OS X)" 0.567
192.168.1.102 - - [22/Nov/2024:10:15:34 +0900] "GET /api/products?category=electronics HTTP/1.1" 200 8901 "-" "PostmanRuntime/7.26.8" 0.123
```

### 4. 時系列データ

#### センサーデータ

```json
{
  "deviceId": "sensor_temp_001",
  "location": "Building A - Room 301",
  "measurements": [
    {
      "timestamp": "2024-11-22T10:00:00Z",
      "temperature": 22.5,
      "humidity": 45.2,
      "pressure": 1013.25
    },
    {
      "timestamp": "2024-11-22T10:05:00Z",
      "temperature": 22.7,
      "humidity": 45.0,
      "pressure": 1013.30
    },
    {
      "timestamp": "2024-11-22T10:10:00Z",
      "temperature": 22.9,
      "humidity": 44.8,
      "pressure": 1013.28
    }
  ]
}
```

#### メトリクスデータ

```json
{
  "service": "api-gateway",
  "metrics": [
    {
      "timestamp": "2024-11-22T10:00:00Z",
      "requestsPerSecond": 1250,
      "averageLatency": 45,
      "p95Latency": 120,
      "p99Latency": 250,
      "errorRate": 0.2,
      "cpuUsage": 45.5,
      "memoryUsage": 62.3
    }
  ]
}
```

### 5. APIレスポンスデータ

#### REST APIレスポンス

```json
{
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "name": "山田太郎",
        "email": "taro@example.com",
        "role": "admin"
      },
      {
        "id": 2,
        "name": "鈴木花子",
        "email": "hanako@example.com",
        "role": "user"
      }
    ],
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 150,
      "totalPages": 8
    }
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2024-11-22T10:15:32Z",
    "version": "v1"
  }
}
```

#### GraphQLレスポンス

```json
{
  "data": {
    "user": {
      "id": "usr_123",
      "name": "山田太郎",
      "email": "taro@example.com",
      "posts": [
        {
          "id": "post_001",
          "title": "初めての投稿",
          "content": "こんにちは、これは私の最初の投稿です。",
          "createdAt": "2024-11-20T10:00:00Z",
          "likes": 42
        }
      ]
    }
  }
}
```

### 6. 関係データ（正規化DB用）

#### Users テーブル

```sql
INSERT INTO users (id, email, name, created_at) VALUES
(1, 'user1@example.com', '山田太郎', '2024-01-15 10:30:00'),
(2, 'user2@example.com', '鈴木花子', '2024-01-16 11:45:00'),
(3, 'user3@example.com', '佐藤次郎', '2024-01-17 09:20:00');
```

#### Orders テーブル（外部キー関係）

```sql
INSERT INTO orders (id, user_id, total_amount, status, created_at) VALUES
(1, 1, 99836, 'completed', '2024-11-22 09:15:00'),
(2, 1, 15000, 'pending', '2024-11-22 14:30:00'),
(3, 2, 45000, 'completed', '2024-11-22 10:00:00');
```

#### Order_Items テーブル

```sql
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 101, 1, 89800),
(2, 1, 102, 2, 2980),
(3, 2, 103, 1, 15000),
(4, 3, 104, 3, 15000);
```

## 異常データ生成

### エッジケース

```json
{
  "testCase": "edge_cases",
  "scenarios": [
    {
      "description": "空文字列",
      "data": {
        "name": "",
        "email": "",
        "phone": ""
      }
    },
    {
      "description": "最大長文字列",
      "data": {
        "name": "A".repeat(255),
        "bio": "Lorem ipsum...".repeat(100)
      }
    },
    {
      "description": "特殊文字",
      "data": {
        "name": "O'Brien",
        "company": "A&B Corp.",
        "note": "Test <script>alert('xss')</script>"
      }
    },
    {
      "description": "数値境界値",
      "data": {
        "age": 0,
        "salary": -1,
        "score": 9999999999
      }
    },
    {
      "description": "日付異常値",
      "data": {
        "birthDate": "1900-01-01",
        "futureDate": "2099-12-31",
        "invalidDate": "2024-02-30"
      }
    }
  ]
}
```

### エラーシナリオ

```json
{
  "testCase": "error_scenarios",
  "scenarios": [
    {
      "statusCode": 400,
      "error": {
        "type": "ValidationError",
        "message": "Invalid email format",
        "fields": ["email"]
      }
    },
    {
      "statusCode": 401,
      "error": {
        "type": "UnauthorizedError",
        "message": "Invalid authentication token"
      }
    },
    {
      "statusCode": 404,
      "error": {
        "type": "NotFoundError",
        "message": "User not found",
        "resourceId": "usr_nonexistent"
      }
    },
    {
      "statusCode": 429,
      "error": {
        "type": "RateLimitError",
        "message": "Too many requests",
        "retryAfter": 60
      }
    },
    {
      "statusCode": 500,
      "error": {
        "type": "InternalServerError",
        "message": "Database connection failed"
      }
    }
  ]
}
```

## スキーマベース生成

### JSONスキーマから生成

```json
{
  "schema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "minLength": 2,
        "maxLength": 50
      },
      "age": {
        "type": "integer",
        "minimum": 18,
        "maximum": 100
      },
      "email": {
        "type": "string",
        "format": "email"
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "minItems": 1,
        "maxItems": 5
      }
    },
    "required": ["name", "email"]
  },
  "count": 10
}
```

生成結果:
```json
[
  {
    "name": "山田太郎",
    "age": 32,
    "email": "taro.yamada@example.com",
    "tags": ["開発", "React", "TypeScript"]
  },
  {
    "name": "鈴木花子",
    "age": 28,
    "email": "hanako.suzuki@example.com",
    "tags": ["デザイン", "UI/UX"]
  }
]
```

### TypeScript型定義から生成

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age?: number;
  roles: ('admin' | 'user' | 'guest')[];
  metadata?: Record<string, any>;
}
```

生成されるデータ:
```json
{
  "id": "usr_7f3k9m2p",
  "name": "山田太郎",
  "email": "taro@example.com",
  "age": 32,
  "roles": ["user"],
  "metadata": {
    "department": "Engineering",
    "joinDate": "2023-04-01"
  }
}
```

### OpenAPI仕様から生成

```yaml
paths:
  /users:
    get:
      responses:
        '200':
          description: User list
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
```

生成されるモックレスポンス:
```json
{
  "users": [
    {
      "id": 1,
      "name": "山田太郎",
      "email": "taro@example.com"
    },
    {
      "id": 2,
      "name": "鈴木花子",
      "email": "hanako@example.com"
    }
  ]
}
```

## 大量データ生成

### パフォーマンステスト用

```
100万件のユーザーデータを生成してください：

要件:
- ユーザーID: user_000001 〜 user_1000000
- 名前: 日本人名（ランダム）
- メール: {name}@example.com 形式
- 登録日: 2020-01-01 〜 2024-11-22 の範囲でランダム
- 出力形式: CSV
- ファイルサイズ: 約100MB想定
```

### 時系列データ（1年分）

```
1年分の時系列センサーデータを生成してください：

要件:
- 期間: 2024-01-01 00:00:00 〜 2024-12-31 23:59:59
- 間隔: 5分ごと
- センサー数: 10個
- 各測定値: temperature, humidity, pressure
- トレンド: 季節変動を含む
- ノイズ: ±2%のランダムノイズ
- 出力形式: JSON（圧縮）
```

## 使用例

### 基本的な使い方

```
ユーザーデータを10件生成してください。
フィールド: id, name, email, age, createdAt
出力形式: JSON
```

### 特定のスキーマに基づく生成

```
以下のTypeScript型定義に基づいてデータを20件生成してください：

interface Product {
  id: string;
  name: string;
  category: 'Electronics' | 'Clothing' | 'Food';
  price: number;
  stock: number;
  isAvailable: boolean;
}

出力形式: JSON配列
```

### 関係データの生成

```
ECサイトのデータベース用に以下のテーブルデータを生成してください：

テーブル:
1. users (100件)
2. products (50件)
3. orders (200件、users.idを参照)
4. order_items (500件、orders.idとproducts.idを参照)

出力形式: SQL INSERT文
```

### APIモックレスポンス生成

```
以下のAPIエンドポイント用のモックレスポンスを10パターン生成してください：

エンドポイント: GET /api/users/:id
レスポンス構造:
- 成功ケース（200）: 8パターン
- エラーケース（404）: 1パターン
- エラーケース（500）: 1パターン

出力形式: JSON（各パターンをファイル化）
```

### テストデータセット生成

```
E2Eテスト用のテストデータセットを生成してください：

シナリオ:
1. 正常系: 標準的なユーザーフロー（10ケース）
2. 異常系: バリデーションエラー（5ケース）
3. エッジケース: 境界値、特殊文字（5ケース)

各ケースに以下を含める:
- 入力データ
- 期待される出力
- テストの説明

出力形式: YAML
```

### 時系列データ生成

```
株価の時系列データを生成してください：

要件:
- 銘柄数: 5
- 期間: 過去1年間（2023-11-22 〜 2024-11-22）
- 頻度: 日次（営業日のみ）
- データ項目: Open, High, Low, Close, Volume
- トレンド: ランダムウォーク + トレンド
- 出力形式: CSV
```

### ログデータ生成

```
1週間分のアプリケーションログを生成してください：

要件:
- 期間: 2024-11-15 00:00:00 〜 2024-11-22 23:59:59
- ログレベル: INFO (70%), WARN (20%), ERROR (10%)
- リクエスト数: 1日あたり約10,000件
- サービス: user-service, order-service, payment-service
- 含める情報: timestamp, level, service, traceId, message, metadata
- 出力形式: JSONL（1行1ログ）
```

## 高度な機能

### データの一貫性保持

```
以下の制約を満たすデータセットを生成してください：

制約:
- 各ユーザーは必ず1件以上の注文を持つ
- 注文の合計金額は商品の単価×数量と一致
- 注文日は必ずユーザー登録日以降
- 在庫数は注文数量の合計を上回る

生成データ:
- Users: 50件
- Products: 100件
- Orders: 200件
- Order_Items: 500件
```

### 現実的な分布

```
現実的な分布に従うデータを生成してください：

年齢分布:
- 20-29歳: 30%
- 30-39歳: 35%
- 40-49歳: 20%
- 50歳以上: 15%

購買金額分布:
- 正規分布（平均: 10,000円、標準偏差: 3,000円）
- 最小値: 1,000円、最大値: 50,000円

都道府県分布:
- 東京都: 20%
- 大阪府: 10%
- その他: 人口比に応じて
```

### 異常検知テスト用データ

```
異常検知アルゴリズムのテスト用データを生成してください：

正常データ: 900件
- 平均: 100、標準偏差: 10

異常データ: 100件
- パターン1: 極端な外れ値（平均の3σ以上）: 50件
- パターン2: トレンドの急激な変化: 30件
- パターン3: 周期性の崩れ: 20件

出力形式: CSV（ラベル付き）
```

### 多言語データ

```
多言語対応アプリのテストデータを生成してください：

言語:
- 日本語: 40%
- 英語: 30%
- 中国語: 20%
- その他（韓国語、フランス語等）: 10%

フィールド:
- name: 各言語の一般的な名前
- address: 各国の住所形式
- phone: 各国の電話番号形式
- email: 国際化ドメイン含む

件数: 100件
出力形式: JSON
```

## GDPR・プライバシー対応

### 完全匿名データ

```
実在しない個人情報のみを使用:
- 名前: ランダム生成（実在の人物と一致しない）
- メール: test用ドメイン（@example.com等）
- 住所: 架空の住所
- 電話番号: 使用されていない番号帯
- クレジットカード: Luhnアルゴリズムで有効だが実在しない番号
```

### 個人情報マスキング

```
実データをベースにマスキング:
- 名前 → ランダムな仮名
- メール → ハッシュ化 + @example.com
- 電話番号 → 最後の4桁以外をマスキング
- 住所 → 地域のみ保持、詳細はランダム化
- 生年月日 → 年代のみ保持（例: 1990年代）
```

## 出力形式

### JSON
```json
[
  {"id": 1, "name": "山田太郎"},
  {"id": 2, "name": "鈴木花子"}
]
```

### CSV
```csv
id,name,email
1,山田太郎,taro@example.com
2,鈴木花子,hanako@example.com
```

### SQL
```sql
INSERT INTO users (id, name, email) VALUES
(1, '山田太郎', 'taro@example.com'),
(2, '鈴木花子', 'hanako@example.com');
```

### XML
```xml
<users>
  <user>
    <id>1</id>
    <name>山田太郎</name>
    <email>taro@example.com</email>
  </user>
</users>
```

### YAML
```yaml
users:
  - id: 1
    name: 山田太郎
    email: taro@example.com
  - id: 2
    name: 鈴木花子
    email: hanako@example.com
```

## ベストプラクティス

1. **現実的なデータ**: 実際のユースケースに近いデータを生成
2. **一貫性**: 関連データ間の整合性を保つ
3. **多様性**: エッジケースを含む多様なパターン
4. **スケーラビリティ**: 大量データでも高速に生成
5. **プライバシー**: 実在する個人情報は使用しない
6. **テスト可能性**: テストに必要な特性を明示的に定義
7. **再現性**: 同じシードで同じデータを生成可能に
8. **ドキュメント**: 生成データの仕様を明記

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-11-22

---

## 使用例まとめ

### シンプルな生成

```
ユーザーデータを5件、JSON形式で生成してください。
```

### スキーマベース

```
以下のTypeScript型定義に基づいて10件生成してください：
{type_definition}
```

### テストデータセット

```
E2Eテスト用の包括的なテストデータセットを生成してください。
正常系、異常系、エッジケースを含めてください。
```

このスキルで、開発・テストに必要なあらゆるデータを生成しましょう！
