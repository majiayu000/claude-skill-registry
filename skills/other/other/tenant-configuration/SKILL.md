---
name: tenant-configuration
description: テナント設定（Tenant Configuration）の開発・修正を行う際に使用。session_config、cors_config、ui_config、identity_policy、マルチテナント設計実装時に役立つ。
---

# テナント設定（Tenant Configuration）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/05-configuration/tenant.md` - テナント設定ガイド（詳細）
- `documentation/openapi/swagger-control-plane-ja.yaml` - OpenAPI仕様（SessionConfiguration等のスキーマ）
- `documentation/docs/content_11_learning/07-multi-tenancy/tenant-isolation.md` - テナント分離の概念
- `documentation/docs/content_06_developer-guide/04-implementation-guides/oauth-oidc/session-management.md` - セッション管理実装ガイド
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-03-session-management.md` - セッション管理概念
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-03-session-management-security.md` - セッションセキュリティ
- `documentation/docs/content_11_learning/19-session-management/01-web-session-basics.md` - Webセッションの基礎

## 機能概要

Tenantはマルチテナント環境における完全に独立した認証・認可ドメイン。

- **テナント種別**: ADMIN（システム管理）、ORGANIZER（組織管理）、PUBLIC（アプリケーション用）
- **設定カテゴリ**: session_config、cors_config、ui_config、security_event_log_config、identity_policy_config
- **データ分離**: ユーザー、クライアント、認証ポリシー、トークン設定、監査ログ

## モジュール構成

```
libs/
├── idp-server-platform/                      # テナント基盤
│   └── .../multi_tenancy/tenant/
│       ├── Tenant.java                       # テナントエンティティ
│       ├── TenantIdentifier.java             # テナント識別子
│       ├── config/
│       │   ├── SessionConfiguration.java     # セッション設定
│       │   ├── CorsConfiguration.java        # CORS設定
│       │   ├── UIConfiguration.java          # UI設定
│       │   └── ...
│       └── policy/
│           ├── TenantIdentityPolicy.java     # ID Policy
│           └── PasswordPolicyConfig.java     # パスワードポリシー
│
└── idp-server-control-plane/                 # 管理API
    └── .../management/tenant/
        ├── TenantManagementApi.java          # テナント管理API
        └── TenantManagementRegistrationContextCreator.java
```

## 主要設定カテゴリ

### Session Configuration

セッション管理とCookie設定。

```java
public class SessionConfiguration {
    String cookieName;           // Cookie名（null時は自動生成）
    String cookieDomain;         // Cookie Domain属性
    String cookieSameSite;       // SameSite属性（None/Lax/Strict）
    boolean useSecureCookie;     // Secure属性
    boolean useHttpOnlyCookie;   // HttpOnly属性
    String cookiePath;           // Cookieパス（API Gateway対応）
    int timeoutSeconds;          // セッションタイムアウト
    String switchPolicy;         // セッション切替ポリシー
}
```

**重要: cookie_path（API Gateway対応）**

API Gateway経由でコンテキストパス付きでデプロイする場合に設定。

```json
{
  "session_config": {
    "cookie_path": "/idp-admin",
    "cookie_same_site": "None",
    "use_secure_cookie": true
  }
}
```

設定すると、Cookieパスが `/idp-admin/{tenant_id}/` となり、API Gateway経由のリクエストでもCookieが正しく送信される。

**設定例**: `config/examples/oidcc-cross-site-context-path/`

### CORS Configuration

クロスオリジンリソース共有。

```java
public class CorsConfiguration {
    List<String> allowOrigins;   // 許可オリジン
    String allowHeaders;         // 許可ヘッダー
    String allowMethods;         // 許可メソッド
    boolean allowCredentials;    // クレデンシャル許可
}
```

### Identity Policy Configuration

ユーザー識別キーとパスワードポリシー。

```java
public class TenantIdentityPolicy {
    IdentityUniqueKeyType identityUniqueKeyType;  // EMAIL_OR_EXTERNAL_USER_ID等
    PasswordPolicyConfig passwordPolicy;           // パスワードポリシー（複雑性+ブルートフォース対策）
}
```

**PasswordPolicyConfig フィールド**:

| フィールド | デフォルト | 説明 |
|-----------|----------|------|
| `min_length` | 8 | パスワード最小文字数 |
| `max_attempts` | 5 | 最大連続失敗回数（0で無制限） |
| `lockout_duration_seconds` | 900 | ロックアウト期間（秒） |

詳細は `documentation/docs/content_06_developer-guide/05-configuration/authn/password.md` を参照。

## 構成パターン

### 同一オリジン構成
```json
{
  "session_config": {
    "cookie_same_site": "Lax"
  }
}
```

### サブドメイン構成
```json
{
  "session_config": {
    "cookie_domain": "example.com",
    "cookie_same_site": "Lax"
  }
}
```

### クロスサイト構成
```json
{
  "session_config": {
    "cookie_same_site": "None",
    "use_secure_cookie": true
  },
  "cors_config": {
    "allow_origins": ["https://app.another.com"]
  }
}
```

### API Gateway + コンテキストパス構成
```json
{
  "session_config": {
    "cookie_path": "/idp-admin",
    "cookie_same_site": "None",
    "use_secure_cookie": true
  }
}
```

## API

### テナント作成（組織レベル）
```
POST /v1/management/organizations/{org-id}/tenants
```

### テナント更新
```
PUT /v1/management/tenants/{tenant-id}
```

### テナント取得
```
GET /v1/management/tenants/{tenant-id}
```

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   └── management/tenant/ - テナント管理APIテスト
└── scenario/
    └── scenario-xx-multi-tenant.test.js - マルチテナントシナリオ
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-platform:compileJava

# テナント設定更新（ローカル）
bash config/examples/oidcc-cross-site-context-path/update.sh

# API Gateway対応app-view起動
docker compose up -d --build app-view-context-path nginx
```

## トラブルシューティング

### auth_session_mismatch エラー

**症状**: `Missing AUTH_SESSION cookie` エラー

**原因**: API Gateway経由でコンテキストパスが追加されているが、Cookieパスが一致しない

**解決策**: `session_config.cookie_path` にコンテキストパスを設定

### CORS エラー

**症状**: `has been blocked by CORS policy`

**原因**: `cors_config.allow_origins` にオリジンが含まれていない

**解決策**: 許可するオリジンを追加

### セッション切替エラー

**症状**: 別ユーザーでログインできない

**原因**: `switch_policy: "STRICT"` 設定

**解決策**: ログアウトしてから再認証、または `SWITCH_ALLOWED` に変更

## 関連スキル

- `session-management` - セッション管理の詳細
- `control-plane` - 管理API全般
- `local-environment` - ローカル開発環境
