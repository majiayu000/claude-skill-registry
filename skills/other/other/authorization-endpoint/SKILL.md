---
name: authorization-endpoint
description: 認可エンドポイント（Authorization Endpoint）機能の開発・修正を行う際に使用。Authorization Request処理、同意フロー、Authorization Code生成実装時に役立つ。
---

# 認可エンドポイント（Authorization Endpoint）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/02-authorization-flow.md` - 認可フロー実装ガイド
- `documentation/docs/content_06_developer-guide/03-application-plane/02-01-authorization-request-verification.md` - 認可リクエスト検証フロー詳細（プロファイル決定、検証チェーン、エラーハンドリング）
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-04-authorization.md` - 認可概念

## 機能概要

認可エンドポイントは、OAuth 2.0/OpenID Connectの認可リクエストを処理する層。
- **Authorization Request処理**: リクエスト検証、保存
- **同意フロー**: ユーザー同意の取得
- **Authorization Code生成**: 認可コード発行
- **Response Type別処理**: code, token, id_token, hybrid
- **動的scopeフィルタリング**: 認証方式・ACRベース

## モジュール構成

```
libs/
├── idp-server-core/                         # 認可コア
│   └── .../oauth/
│       ├── handler/
│       │   ├── OAuthRequestHandler.java    # リクエスト処理
│       │   └── OAuthAuthorizeHandler.java  # 認可処理
│       ├── request/
│       │   ├── AuthorizationRequest.java
│       │   └── AuthorizationRequestIdentifier.java
│       ├── response/
│       │   ├── AuthorizationResponse.java
│       │   ├── AuthorizationResponseCreator.java
│       │   └── AuthorizationResponseCreators.java
│       ├── validator/
│       │   └── OAuthAuthorizeRequestValidator.java
│       └── repository/
│           └── AuthorizationRequestRepository.java
│
├── idp-server-core/grant_management/        # Grant管理
│   ├── grant/
│   │   ├── AuthorizationCodeGrant.java
│   │   └── AuthorizationCodeGrantCreator.java
│   └── AuthorizationGrantedRepository.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/authorization/
```

## OAuthAuthorizeHandler

`idp-server-core/oauth/handler/OAuthAuthorizeHandler.java` 内の実際の実装:

```java
public class OAuthAuthorizeHandler {

    AuthorizationResponseCreators creators;
    AuthorizationRequestRepository authorizationRequestRepository;
    AuthorizationCodeGrantRepository authorizationCodeGrantRepository;
    OAuthTokenCommandRepository oAuthTokenCommandRepository;
    AuthorizationServerConfigurationQueryRepository authorizationServerConfigurationQueryRepository;
    ClientConfigurationQueryRepository clientConfigurationQueryRepository;
    AuthorizationGrantedRepository authorizationGrantedRepository;

    public AuthorizationResponse handle(OAuthAuthorizeRequest request) {

        Tenant tenant = request.tenant();
        AuthorizationRequestIdentifier authorizationRequestIdentifier =
            request.toIdentifier();
        User user = request.user();
        Authentication authentication = request.authentication();
        CustomProperties customProperties = request.toCustomProperties();
        DeniedScopes deniedScopes = request.toDeniedScopes();

        // リクエスト検証
        OAuthAuthorizeRequestValidator validator =
            new OAuthAuthorizeRequestValidator(
                authorizationRequestIdentifier,
                user,
                authentication,
                customProperties
            );
        validator.validate();

        // AuthorizationRequest取得
        AuthorizationRequest authorizationRequest =
            authorizationRequestRepository.get(
                tenant,
                authorizationRequestIdentifier
            );

        // Response生成（Response Type別）
        // AuthorizationResponseCreatorsが適切なCreatorを選択
        // ...
    }
}
```

**注意**: AuthorizationResponseCreatorsが、Response Type（code, token, id_token, hybrid）に応じた適切なCreatorを選択します。

## Authorization Code Grant生成

`idp-server-core/grant_management/grant/` 内:

```java
public class AuthorizationCodeGrantCreator {
    public AuthorizationCodeGrant create(
        AuthorizationGrant authorizationGrant,
        AuthorizationRequest authorizationRequest
    ) {
        // Authorization Code生成
        // AuthorizationGrantとAuthorizationRequestを紐付け
    }
}
```

## Response Type別処理

| Response Type | Creator | 説明 |
|---------------|---------|------|
| `code` | AuthorizationResponseCodeCreator | Authorization Code Flow |
| `token` | AuthorizationResponseTokenCreator | Implicit Flow (非推奨) |
| `id_token` | AuthorizationResponseIdTokenCreator | Implicit Flow |
| `code token` | Hybrid Flow Creator | Hybrid Flow |
| `code id_token` | Hybrid Flow Creator | Hybrid Flow |
| `code id_token token` | Hybrid Flow Creator | Hybrid Flow |

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── oidc_core_3_1_code.test.js          # Authorization Code Flow
│   ├── oidc_core_3_2_implicit.test.js      # Implicit Flow
│   ├── oidc_core_3_3_hybrid.test.js        # Hybrid Flow
│   └── rfc6749_4_1_code.test.js            # OAuth 2.0 Authorization Code
│
└── scenario/application/
    └── scenario-02-sso-oidc.test.js        # SSO認可シナリオ
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- spec/oidc_core_3_1_code.test.js
cd e2e && npm test -- spec/oidc_core_3_3_hybrid.test.js
```

## トラブルシューティング

### Authorization Request検証失敗
- redirect_uriがクライアント登録済みURIと一致するか確認
- scopeが有効か確認
- Response Typeがクライアント設定と一致するか確認

### Authorization Code生成失敗
- AuthorizationGrantが正しく生成されているか確認
- ユーザー認証が完了しているか確認

### 同意画面が表示されない
- Grant管理の設定を確認
- 既存Grantが存在する場合は同意スキップ
