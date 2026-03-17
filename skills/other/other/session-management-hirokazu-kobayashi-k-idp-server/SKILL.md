---
name: session-management
description: セッション管理（Session Management）機能の開発・修正を行う際に使用。OPSession, ClientSession, SSO, RP-Initiated Logout, Back-Channel Logout実装時に役立つ。
---

# セッション管理（Session Management）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/04-implementation-guides/oauth-oidc/session-management.md` - セッション管理実装ガイド
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-03-session-management.md` - セッション管理概念
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-03-session-management-security.md` - セッションセキュリティ

## 機能概要

セッション管理は、ユーザーの認証状態を維持・管理する層。
- **2層セッション**: OPSession（SSO用）+ ClientSession（アプリ別）
- **セッション再利用**: SSO実現のためのセッション共有
- **セッション切替ポリシー**: STRICT, SWITCH_ALLOWED, MULTI_SESSION
- **ACRダウングレード防止**: セッションACR検証
- **ログアウト**: RP-Initiated, Back-Channel, Front-Channel

## モジュール構成

```
libs/
├── idp-server-core/                         # セッションコア
│   └── .../openid/session/
│       ├── OIDCSessionHandler.java         # セッション処理Handler
│       ├── OIDCSessionService.java         # セッション管理Service
│       ├── OPSession.java                  # OPセッション（SSO）
│       ├── ClientSession.java              # クライアントセッション
│       ├── SessionCookieDelegate.java      # Cookie管理
│       ├── SessionSwitchPolicy.java        # セッション切替ポリシー
│       └── repository/
│           ├── OPSessionRepository.java
│           └── ClientSessionRepository.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/session/
        └── SessionManagementApi.java
```

## セッション構造

### OPSession（SSO用）

`idp-server-core/openid/session/OPSession.java` 内の実際の構造:

```java
public class OPSession {
    private OPSessionIdentifier id;
    private TenantIdentifier tenantId;
    private User user;
    private Instant authTime;
    private String acr;
    private List<String> amr;
    private Map<String, Map<String, Object>> interactionResults;
    private BrowserState browserState;
    private Instant createdAt;
    private Instant expiresAt;
    private Instant lastAccessedAt;
    private SessionStatus status;
    private String ipAddress;    // 認証時のIPアドレス
    private String userAgent;    // 認証時のUser-Agent

    // セッション再利用可否判定（概念的）
    public boolean canReuseFor(Acr requiredAcr) {
        // ACRダウングレード防止
        return this.acr.isHigherOrEqualTo(requiredAcr);
    }
}
```

**注意**: ClientSessionは別エンティティとして独立管理されます。

### ClientSession（アプリ別）

```java
public class ClientSession {
    ClientSessionId clientSessionId;
    SessionId opSessionId;  // OPSessionへの参照
    ClientId clientId;
    Scope grantedScope;
    Instant createdAt;
    Instant lastAccessedAt;
}
```

## セッション処理

`idp-server-core/openid/session/OIDCSessionHandler.java` 内:

```java
public class OIDCSessionHandler {
    /**
     * 認証成功時のセッション作成または再利用
     *
     * セッション切替ポリシー:
     * - 同一ユーザー: 既存セッション再利用
     * - 異なるユーザー + STRICT: 例外スロー
     * - 異なるユーザー + SWITCH_ALLOWED: 既存終了、新規作成
     * - 異なるユーザー + MULTI_SESSION: 新規作成（既存維持）
     */
    public OPSession onAuthenticationSuccess(
        Tenant tenant,
        User user,
        Authentication authentication,
        Map<String, Map<String, Object>> interactionResults,
        OPSession existingSession,
        RequestAttributes requestAttributes
    ) {
        // セッション再利用または新規作成ロジック
        // RequestAttributesからIPアドレス・User-Agentを抽出してOPSessionに保存
    }
}
```

## セッション切替ポリシー

```java
public enum SessionSwitchPolicy {
    STRICT,           // セッション切替禁止
    SWITCH_ALLOWED,   // 切替許可（既存セッション無効化）
    MULTI_SESSION;    // 複数セッション許可
}
```

OIDCSessionService内で、ポリシーに応じた処理を実行します。

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   └── (OIDCセッション関連仕様テスト)
│
├── scenario/application/
│   ├── scenario-02-sso-oidc.test.js         # SSOシナリオ
│   └── scenario-13-sso-session-management.test.js
│
├── usecase/standard/
│   └── standard-04-session-switch-policy.test.js
│
└── security/
    └── session_fixation_password_auth.test.js  # セッション固定攻撃対策
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- scenario/application/scenario-02-sso-oidc.test.js
cd e2e && npm test -- security/session_fixation_password_auth.test.js
```

## トラブルシューティング

### SSOが動作しない
- OPSessionのACRを確認
- Cookie設定（domain, path, SameSite）を確認
- `SessionCookieDelegate` の設定を確認

### セッション切替エラー
- `SessionSwitchPolicy`設定を確認
- `STRICT`の場合は既存セッションを無効化してから再認証

### セッションが期限切れ
- OPSessionの有効期限設定を確認
- Redisなどのセッションストレージが正常か確認

## Cookie Path設定（API Gateway対応）

### 背景

API Gateway経由でidp-serverをデプロイする場合、コンテキストパス（例: `/idp-admin`）が追加されることがあります。この場合、Cookieのパスを適切に設定しないと、ブラウザがCookieを送信せず `auth_session_mismatch` エラーが発生します。

### 問題の例

```
# API Gateway構成
https://api.example.com/idp-admin/* → idp-server (/)

# デフォルトのCookieパス
Path=/{tenant_id}/

# ブラウザがアクセスするパス
/idp-admin/{tenant_id}/v1/authorizations

# → パスが一致しないためCookieが送信されない
```

### 解決方法

テナントの `session_config.cookie_path` を設定します:

```json
{
  "tenant": {
    "session_config": {
      "cookie_name": "CONTEXT_PATH_SESSION",
      "cookie_path": "/idp-admin",
      "cookie_same_site": "None",
      "use_secure_cookie": true,
      "timeout_seconds": 3600
    }
  }
}
```

これにより、Cookieパスは `/idp-admin/{tenant_id}/` となり、API Gateway経由のリクエストでもCookieが正しく送信されます。

### 設定例

`config/examples/oidcc-cross-site-context-path/` にAPI Gateway + コンテキストパスの設定例があります:

- `onboarding-request.json` - テナント設定（cookie_path含む）
- `oidc-test/*.json` - OIDC Conformance Suite用設定

### 関連ファイル

- `AuthSessionCookieService.java` - AUTH_SESSION Cookie設定
- `SessionCookieService.java` - IDP_IDENTITY/IDP_SESSION Cookie設定
- `SessionConfiguration.java` - session_config値オブジェクト

### ローカルテスト環境

docker-compose.yamlの `app-view-context-path` サービスと nginx.conf の `/idp-admin/` ルーティングを使用してAPI Gateway動作をシミュレートできます。

```bash
# コンテキストパス対応のapp-viewを起動
docker compose up -d --build app-view-context-path nginx

# テナント設定を更新
bash config/examples/oidcc-cross-site-context-path/update.sh
```
