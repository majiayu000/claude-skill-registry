---
name: federation
description: 外部IdP連携（Federation/SSO）機能の開発・設定を行う際に使用。Google、Azure AD、カスタムOIDCプロバイダー連携、userinfo_mapping_rules設定、oauth-extension実装時に役立つ。
---

# Federation（外部IdP連携）開発ガイド

## ドキュメント

- `documentation/docs/content_05_how-to/phase-3-advanced/01-federation-setup.md` - 設定ガイド
- `documentation/docs/content_06_developer-guide/03-application-plane/08-federation.md` - 実装ガイド
- `documentation/docs/content_06_developer-guide/05-configuration/federation.md` - 設定リファレンス
- `documentation/docs/content_10_ai_developer/ai-43-federation-oidc.md` - AI開発者向けガイド

## モジュール構成

```
libs/
├── idp-server-federation-oidc/           # OIDC Federation実装
│   └── .../federation/sso/oidc/
│       ├── OidcFederationInteractor.java # メインInteractor
│       ├── OidcSsoExecutor.java          # Executor IF
│       ├── OidcSsoExecutors.java         # Executor管理
│       ├── StandardOidcExecutor.java     # 標準OIDC実行
│       ├── OAuthExtensionExecutor.java   # OAuth拡張実行
│       ├── FacebookOidcExecutor.java     # Facebook専用
│       ├── UserinfoExecutor.java         # UserInfo取得IF
│       ├── UserinfoHttpRequestExecutor.java   # 単一リクエスト
│       ├── UserinfoHttpRequestsExecutor.java  # 複数リクエスト
│       ├── UserinfoExecutionRequest.java # 実行リクエスト
│       ├── UserinfoExecutionResult.java  # 実行結果
│       └── UserInfoMapper.java           # マッピング処理
│
├── idp-server-core/                      # コア定義
│   └── .../openid/federation/
│       └── sso/
│           ├── SsoProvider.java
│           └── FederationConfiguration.java
│
└── idp-server-control-plane/             # 管理API
    └── .../management/federation/
```

## プロバイダータイプ（payload.provider）

| provider | 説明 | 用途 |
|----------|------|------|
| `standard` | 標準OIDCフロー | Google, Azure AD, カスタムOIDC |
| `oauth-extension` | OAuth拡張フロー | カスタムUserInfo取得が必要な場合 |
| `facebook` | Facebook専用 | Facebook Login |

**注意**: 無効なprovider値は404エラー（`No OidcSsoExecutor found for provider xxx`）

## userinfo_mapping_rules

### provider別のJSONPath形式

| provider | JSONPath形式 | 説明 |
|----------|-------------|------|
| `standard` | `$.http_request.response_body.{field}` | 標準OIDCプロバイダー |
| `oauth-extension` (単一) | `$.userinfo_execution_http_request.response_body.{field}` | http_request使用時 |
| `oauth-extension` (複数) | `$.userinfo_execution_http_requests[index].response_body.{field}` | http_requests使用時 |

### 実装の流れ

```
OAuthExtensionExecutor.requestUserInfo()
  ↓ UserinfoExecutionRequest に access_token を設定
  ↓   Map.of("access_token", oidcUserinfoRequest.accessToken())
  ↓
UserinfoHttpRequestExecutor.execute()
  ↓ param.put("request_body", request.toMap())
  ↓ → $.request_body.access_token でアクセストークン参照可能
  ↓
  ↓ 結果を Map.of("userinfo_execution_http_request", result) で返却
  ↓
UserInfoMapper.map()
  ↓ userinfo_mapping_rules で結果をマッピング
```

### standard プロバイダー例

```json
{
  "payload": {
    "provider": "standard",
    "userinfo_mapping_rules": [
      {"from": "$.http_request.response_body.sub", "to": "external_user_id"},
      {"from": "$.http_request.response_body.email", "to": "email"},
      {"from": "$.http_request.response_body.name", "to": "name"}
    ]
  }
}
```

**実装箇所**: `StandardOidcExecutor` クラスの `requestUserInfo()` メソッド
```java
return UserinfoExecutionResult.success(Map.of("http_request", map));
```

### oauth-extension プロバイダー例

#### 単一リクエスト（http_request）

```json
{
  "payload": {
    "provider": "oauth-extension",
    "userinfo_execution": {
      "function": "http_request",
      "http_request": {
        "url": "https://api.example.com/user/profile",
        "method": "GET",
        "header_mapping_rules": [
          {
            "from": "$.request_body.access_token",
            "to": "Authorization",
            "functions": [{"name": "format", "args": {"template": "Bearer {{value}}"}}]
          }
        ]
      }
    },
    "userinfo_mapping_rules": [
      {"from": "$.userinfo_execution_http_request.response_body.user_id", "to": "external_user_id"},
      {"from": "$.userinfo_execution_http_request.response_body.email", "to": "email"}
    ]
  }
}
```

#### 複数リクエスト（http_requests）

```json
{
  "payload": {
    "provider": "oauth-extension",
    "userinfo_execution": {
      "function": "http_requests",
      "http_requests": [
        {
          "url": "https://api.example.com/user/overview",
          "method": "POST",
          "header_mapping_rules": [
            {
              "from": "$.request_body.access_token",
              "to": "Authorization",
              "functions": [{"name": "format", "args": {"template": "Bearer {{value}}"}}]
            }
          ]
        }
      ]
    },
    "userinfo_mapping_rules": [
      {"from": "$.userinfo_execution_http_requests[0].response_body.id", "to": "external_user_id"}
    ]
  }
}
```

## マッピング関数（functions）

`libs/idp-server-platform/src/main/java/org/idp/server/platform/mapper/functions/`

| 関数名 | 説明 | 使用例 |
|--------|------|--------|
| `format` | テンプレート置換 | `{"template": "Bearer {{value}}"}` |
| `join` | 配列結合 | `{"separator": ","}` |
| `split` | 文字列分割 | `{"separator": ","}` |
| `replace` | 文字列置換 | `{"from": "a", "to": "b"}` |
| `regex_replace` | 正規表現置換 | `{"pattern": "...", "replacement": "..."}` |
| `substring` | 部分文字列 | `{"start": 0, "end": 10}` |
| `trim` | 空白除去 | - |
| `case` | 大文字小文字変換 | `{"to": "upper\|lower"}` |
| `convert_type` | 型変換 | `{"to": "string\|integer\|boolean"}` |

## 重要な`to`フィールド（userinfo_mapping_rules）

| フィールド | 説明 | 必須 |
|-----------|------|------|
| `external_user_id` | 外部IdPでのユーザーID | **必須** |
| `email` | メールアドレス | - |
| `name` | 表示名 | - |
| `picture` | プロフィール画像URL | - |
| `preferred_username` | ユーザー名 | - |
| `custom_properties.{key}` | カスタム属性 | - |

## 設定テンプレート

```
config/templates/federation/
├── google-template.json
├── azure-ad-template.json
└── custom-oidc-template.json
```

## E2Eテスト

```
e2e/src/tests/
├── scenario/control_plane/
│   ├── organization/
│   │   ├── organization_federation_config_management.test.js
│   │   └── organization_federation_config_management_structured.test.js
│   └── system/
│       └── federation_management.test.js
│
└── usecase/advance/
    └── advance-01-federation-security-event-user-name.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-federation-oidc:compileJava

# テスト
cd e2e && npm test -- --grep "federation"
cd e2e && npm test -- scenario/control_plane/organization/organization_federation_config_management.test.js
```

## トラブルシューティング

### 404エラー: No OidcSsoExecutor found
- `payload.provider`の値が正しいか確認（大文字小文字を区別）
- 有効な値: `standard`, `oauth-extension`, `facebook`

### userinfo_mapping_rules が動作しない
- JSONPathの形式がproviderタイプに合っているか確認
- `standard` → `$.http_request.response_body.xxx`
- `oauth-extension` → `$.userinfo_execution_http_request.xxx` or `$.userinfo_execution_http_requests[n].xxx`

### アクセストークンがAPIに渡らない
- `header_mapping_rules`で`$.request_body.access_token`を参照
- `format`関数で`Bearer `プレフィックスを追加
