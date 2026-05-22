---
name: token-management
description: トークン管理（Token Management）機能の開発・修正を行う際に使用。Access Token, Refresh Token, ID Token, Introspection, Revocation実装時に役立つ。
---

# トークン管理（Token Management）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/03-token-endpoint.md` - トークンエンドポイント実装ガイド
- `documentation/docs/content_03_concepts/04-tokens-claims/concept-02-token-management.md` - トークン管理概念

## 機能概要

トークン管理は、Access Token/Refresh Token/ID Tokenの発行・検証・取消を行う層。
- **トークン発行**: Authorization Code, Refresh Token, Client Credentials各グラント対応
- **Token Introspection（RFC 7662）**: トークン検証
- **Token Revocation（RFC 7009）**: トークン取消
- **ID Token発行**: OpenID Connect対応

## モジュール構成

```
libs/
├── idp-server-core/                         # トークンコア
│   └── .../token/
│       ├── handler/token/
│       │   └── TokenRequestHandler.java    # トークンリクエスト処理
│       ├── service/
│       │   ├── OAuthTokenCreationServices.java
│       │   ├── AuthorizationCodeGrantService.java
│       │   ├── RefreshTokenGrantService.java
│       │   └── ClientCredentialsGrantService.java
│       ├── OAuthToken.java                 # トークン表現
│       ├── repository/
│       │   ├── OAuthTokenCommandRepository.java
│       │   └── OAuthTokenQueryRepository.java
│       └── handler/
│           ├── tokenintrospection/
│           │   └── TokenIntrospectionHandler.java
│           └── tokenrevocation/
│               └── TokenRevocationHandler.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/token/
        └── TokenConfigManagementApi.java
```

## トークン発行

`idp-server-core/token/handler/token/TokenRequestHandler.java` 内の実際のメソッドシグネチャ:

```java
public class TokenRequestHandler {

    OAuthTokenCreationServices oAuthTokenCreationServices;

    public TokenRequestResponse handle(
        TokenRequest tokenRequest,
        PasswordCredentialsGrantDelegate passwordCredentialsGrantDelegate,
        TokenUserFindingDelegate tokenUserFindingDelegate
    ) {
        // Grant typeに応じた処理はOAuthTokenCreationServicesが管理
        // AuthorizationCodeGrantService
        // RefreshTokenGrantService
        // ClientCredentialsGrantService
        // ...
    }
}
```

**注意**: Grant type別の処理は、OAuthTokenCreationServices経由で各Serviceに委譲されます。

## Grant type別サービス

| サービス | 役割 |
|---------|------|
| `AuthorizationCodeGrantService` | Authorization Code Grant処理 |
| `RefreshTokenGrantService` | Refresh Token Grant処理 |
| `ClientCredentialsGrantService` | Client Credentials Grant処理 |

## Token Introspection（RFC 7662）

`idp-server-core/token/introspection/` 内:

トークンのメタデータを検証し、active/inactiveを返却します。

## Token Revocation（RFC 7009）

`idp-server-core/token/revocation/` 内:

トークンを無効化します。OAuthTokenCommandRepository.delete()を使用します。

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── rfc6749_token_endpoint_*.test.js     # OAuth 2.0 Token Endpoint
│   ├── rfc7009_token_revocation_*.test.js   # Token Revocation
│   ├── rfc7662_token_introspection_*.test.js # Token Introspection
│   └── oidc_core_*.test.js                  # OIDC関連トークンテスト
│
└── scenario/application/
    └── (トークン関連シナリオテスト)
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- spec/rfc6749_token_endpoint_*.test.js
cd e2e && npm test -- spec/rfc7009_token_revocation_*.test.js
cd e2e && npm test -- spec/rfc7662_token_introspection_*.test.js
```

## トラブルシューティング

### トークン発行失敗
- Grant typeが正しいか確認
- Authorization Code/Refresh Tokenが有効か確認
- 対応するGrantServiceが登録されているか確認

### Introspectionでinactive
- トークンが有効期限内か確認
- OAuthTokenが正しく保存されているか確認

### Revocationが失敗
- クライアント認証が成功しているか確認
- OAuthTokenCommandRepository.delete()が正しく呼ばれているか確認
