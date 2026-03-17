---
name: external-integration
description: 外部サービス連携（External Service Integration）機能の開発・修正を行う際に使用。HTTP Request Executor, MappingRule, OAuth/HMAC認証実装時に役立つ。
---

# 外部サービス連携（External Service Integration）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/06-security-extensions/concept-02-external-service-integration.md` - 外部連携概念

## 機能概要

外部サービス連携は、HTTP経由で外部APIと連携する層。
- **HTTP Request Executor**: リトライロジック付きHTTPクライアント
- **MappingRule**: JSONPath + 変換関数によるデータマッピング
- **認証**: OAuth 2.0, HMAC, Basic認証
- **冪等性**: Idempotency-Keyヘッダー対応
- **Rate Limiting**: Retry-Afterヘッダー対応

## モジュール構成

```
libs/
└── idp-server-platform/                     # プラットフォーム基盤
    └── .../platform/
        ├── http/
        │   ├── HttpRequestExecutor.java
        │   └── retry/
        │       └── RetryStrategy.java
        ├── mapper/
        │   ├── MappingRule.java            # マッピングルール
        │   ├── FunctionSpec.java           # 関数仕様
        │   ├── ConditionSpec.java          # 条件仕様
        │   ├── TypeConverter.java          # 型変換
        │   ├── ObjectCompositor.java       # オブジェクト合成
        │   └── functions/
        │       ├── FormatFunction.java
        │       ├── TrimFunction.java
        │       ├── ReplaceFunction.java
        │       ├── RegexReplaceFunction.java
        │       └── ... (その他のマッピング関数)
        └── auth/
            ├── OAuth2Authenticator.java
            └── HmacAuthenticator.java
```

## MappingRule

`idp-server-platform/mapper/MappingRule.java` 内の実際の構造:

```java
public class MappingRule {
    String from;             // JSONPathソース
    Object staticValue;      // 静的値（fromの代わり）
    String to;              // マッピング先
    List<FunctionSpec> functions;  // 変換関数
    ConditionSpec condition;       // 条件

    public MappingRule(String from, String to) {
        this.from = from;
        this.to = to;
    }

    public MappingRule(
        String from,
        String to,
        List<FunctionSpec> functions
    ) {
        this.from = from;
        this.to = to;
        this.functions = functions;
    }
}
```

## Mapping Rule設定

```json
{
  "mapping_rules": [
    {
      "from": "$.response.user.id",
      "to": "external_user_id"
    },
    {
      "from": "$.response.user.roles",
      "to": "custom_properties.roles",
      "functions": [
        {
          "name": "join",
          "args": {
            "separator": ","
          }
        }
      ]
    }
  ]
}
```

## Mapping Functions

`idp-server-platform/mapper/functions/` 内に実装:

| クラス | 説明 | 使用例 |
|--------|------|--------|
| `FormatFunction` | テンプレート置換 | `{"template": "Bearer {{value}}"}` |
| `TrimFunction` | 空白除去 | - |
| `ReplaceFunction` | 文字列置換 | `{"from": "a", "to": "b"}` |
| `RegexReplaceFunction` | 正規表現置換 | `{"pattern": "...", "replacement": "..."}` |

**使用場所**: Federation（userinfo_mapping_rules）、Identity Verification（mapping_rules）

## HTTP Request Executor

`idp-server-platform/http/` 内:

HTTP Request Executorは、リトライロジックとRate Limiting対応を提供します。

## E2Eテスト

```
e2e/src/tests/
└── (外部連携は各機能のテスト内で検証)
    ├── integration/ida/           # Identity Verification外部連携
    └── usecase/advance/          # Federation外部連携
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-platform:compileJava

# テスト
cd e2e && npm test -- integration/ida/
cd e2e && npm test -- usecase/advance/
```

## トラブルシューティング

### HTTP Request失敗
- URLが正しいか確認
- 認証情報（OAuth, HMAC）を確認

### MappingRuleが動作しない
- JSONPath (`from`) が正しいか確認
- ソースデータの構造を確認
- FunctionSpecの設定を確認

### 変換関数が失敗
- 関数名が正しいか確認（FormatFunction, TrimFunction等）
- 関数のargsが正しいか確認
