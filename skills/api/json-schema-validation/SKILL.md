---
name: json-schema-validation
description: JSONスキーマ検証（JSON Schema Validation）機能の開発・修正を行う際に使用。ユーザー登録スキーマ、Identity Verificationスキーマ、外部API検証実装時に役立つ。
---

# JSONスキーマ検証（JSON Schema Validation）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/06-security-extensions/concept-03-schema-validation.md` - JSONスキーマ検証概念

## 機能概要

JSONスキーマ検証は、入力データの構造・型・制約を検証する層。
- **JSON Schema Draft 2020-12準拠**
- **ユーザー登録検証**: テナント別カスタムスキーマ
- **Identity Verification検証**: 本人確認申請データ検証
- **外部API検証**: リクエスト/レスポンス検証
- **詳細エラーメッセージ**: フィールド別エラー

## モジュール構成

```
libs/
└── idp-server-platform/                     # プラットフォーム基盤
    └── .../platform/json/schema/
        ├── JsonSchemaDefinition.java       # スキーマ定義
        ├── JsonSchemaValidator.java        # スキーマ検証
        └── JsonSchemaValidationException.java
```

## ユーザー登録でのスキーマ検証

`idp-server-core/openid/identity/IdPUserCreator.java` 内:

```java
public class IdPUserCreator {

    JsonSchemaDefinition definition;
    AuthenticationInteractionRequest request;

    public User create() {
        User user = User.initialized();

        // スキーマ定義に基づいてフィールドを設定
        if (definition.hasProperty("name") &&
            request.containsKey("name")) {
            user.setName(request.getValueAsString("name"));
        }

        if (definition.hasProperty("email") &&
            request.containsKey("email")) {
            user.setEmail(request.getValueAsString("email"));
        }

        // その他のフィールドも同様に処理
        // ...

        return user;
    }
}
```

**注意**: JsonSchemaDefinitionが、許可されたフィールドを定義します。

## スキーマ定義例

### ユーザー登録スキーマ

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "format": "email"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "birthdate": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    }
  },
  "required": ["email", "name"]
}
```

### Identity Verification申請スキーマ

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "document_type": {
      "type": "string",
      "enum": ["passport", "drivers_license", "national_id"]
    },
    "document_number": {
      "type": "string",
      "minLength": 5
    }
  },
  "required": ["document_type", "document_number"]
}
```

## スキーマ検証エラー

```java
public class JsonSchemaValidationException {
    // フィールド別の詳細エラーメッセージ
    // - 必須フィールド不足
    // - 型不一致
    // - フォーマット違反
    // - 制約違反（minLength, maxLength, pattern等）
}
```

## E2Eテスト

```
e2e/src/tests/
└── integration/ida/
    └── (Identity Verificationスキーマ検証テスト)
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-platform:compileJava

# テスト
cd e2e && npm test -- integration/ida/
```

## トラブルシューティング

### スキーマ検証失敗
- スキーマ定義が正しいか確認（JSON Schema Draft 2020-12形式）
- 必須フィールドが含まれているか確認

### 型エラー
- フィールドの型がスキーマと一致するか確認
- string, number, boolean, object, arrayを正しく使用

### フォーマット検証失敗
- email, uri, date-time等のフォーマットが正しいか確認
- カスタムpattern（正規表現）が正しいか確認

### カスタムスキーマが反映されない
- テナント別スキーマ設定が正しいか確認
- JsonSchemaDefinitionが正しくロードされているか確認
