---
name: userinfo-endpoint
description: UserInfoエンドポイント（UserInfo Endpoint）機能の開発・修正を行う際に使用。UserInfo claims、scopeフィルタリング、verified_claims実装時に役立つ。
---

# UserInfoエンドポイント（UserInfo Endpoint）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/05-userinfo.md` - UserInfo実装ガイド
- `documentation/docs/content_03_concepts/04-tokens-claims/concept-01-id-token.md` - クレーム概念

## 機能概要

UserInfoエンドポイントは、Access Tokenを使ってユーザー情報を取得するエンドポイント。
- **Access Token検証**: トークンの有効性確認
- **Scopeベースクレームフィルタリング**: scopeに応じたクレーム返却
- **標準クレーム**: profile, email, phone, address
- **カスタムクレーム**: `claims:` プレフィックス
- **Verified Claims**: `verified_claims:` プレフィックス（OIDC4IDA）

## モジュール構成

```
libs/
└── idp-server-core/                         # UserInfoコア
    └── .../openid/userinfo/
        ├── handler/
        │   ├── UserinfoHandler.java        # UserInfo処理
        │   └── UserinfoErrorHandler.java   # エラー処理
        ├── UserinfoClaimsCreator.java      # クレーム生成
        ├── UserinfoResponse.java           # レスポンス
        ├── validator/
        │   └── UserinfoValidator.java
        ├── verifier/
        │   └── UserinfoVerifier.java
        └── plugin/
            └── UserinfoCustomIndividualClaimsCreators.java
```

## UserinfoHandler

`idp-server-core/openid/userinfo/handler/UserinfoHandler.java` 内の実際の実装:

```java
public class UserinfoHandler {

    OAuthTokenQueryRepository oAuthTokenQueryRepository;
    AuthorizationServerConfigurationQueryRepository authorizationServerConfigurationQueryRepository;
    ClientConfigurationQueryRepository clientConfigurationQueryRepository;
    UserinfoCustomIndividualClaimsCreators userinfoCustomIndividualClaimsCreators;

    public UserinfoRequestResponse handle(
        UserinfoRequest request,
        UserinfoDelegate delegate
    ) {
        AccessTokenEntity accessTokenEntity = request.toAccessToken();
        Tenant tenant = request.tenant();

        // リクエスト検証
        UserinfoValidator validator = new UserinfoValidator(request);
        validator.validate();

        // Access Token取得
        OAuthToken oAuthToken = oAuthTokenQueryRepository.find(
            tenant,
            accessTokenEntity
        );

        if (!oAuthToken.exists()) {
            throw new TokenInvalidException("not found token");
        }

        // ユーザー取得
        User user = delegate.findUser(tenant, oAuthToken.subject());

        // 検証
        UserinfoVerifier verifier = new UserinfoVerifier(
            oAuthToken,
            request.toClientCert(),
            user
        );
        verifier.verify();

        // クレーム生成
        UserinfoClaimsCreator claimsCreator =
            new UserinfoClaimsCreator(
                user,
                oAuthToken.authorizationGrant(),
                authorizationServerConfiguration,
                clientConfiguration,
                userinfoCustomIndividualClaimsCreators
            );

        Map<String, Object> claims = claimsCreator.createClaims();
        UserinfoResponse userinfoResponse =
            new UserinfoResponse(user, claims);

        return new UserinfoRequestResponse(
            UserinfoRequestStatus.OK,
            oAuthToken,
            userinfoResponse
        );
    }
}
```

## UserinfoClaimsCreator

UserInfoクレームは、以下の要素から生成:
1. **User属性**: sub, name, email, phone等
2. **AuthorizationGrant**: 認可時のscope
3. **AuthorizationServerConfiguration**: サーバー設定
4. **ClientConfiguration**: クライアント設定
5. **UserinfoCustomIndividualClaimsCreators**: カスタムクレーム

## Scopeベースフィルタリング

| Scope | 含まれるClaims |
|-------|----------------|
| `profile` | name, family_name, given_name, middle_name, nickname, preferred_username, profile, picture, website, gender, birthdate, zoneinfo, locale, updated_at |
| `email` | email, email_verified |
| `phone` | phone_number, phone_number_verified |
| `address` | address |
| `claims:xxx` | カスタムクレーム |
| `verified_claims:xxx` | 本人確認済みクレーム（OIDC4IDA） |

## E2Eテスト

```
e2e/src/tests/
└── spec/
    └── oidc_core_5_userinfo.test.js        # UserInfo仕様テスト
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# テスト
cd e2e && npm test -- spec/oidc_core_5_userinfo.test.js
```

## トラブルシューティング

### Access Token検証失敗
- トークンが有効期限内か確認
- トークンが正しく送信されているか確認（Bearer形式）

### クレームが含まれない
- Access Tokenのscopeを確認
- ユーザー属性が存在するか確認

### Verified Claimが含まれない
- ユーザーが本人確認済みか確認
- `verified_claims:` scopeが含まれているか確認

### mTLSバインディング検証失敗
- Access Tokenのcnfクレームとクライアント証明書が一致するか確認
