---
name: authentication
description: 認証機能（Authentication Policy, MFA）の開発・修正を行う際に使用。認証ポリシー、パスワード、OTP、FIDO2、条件付き認証実装時に役立つ。
---

# 認証（Authentication）機能 開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/04-authentication.md` - 認証実装ガイド
- `documentation/docs/content_06_developer-guide/05-configuration/authentication-policy.md` - 認証ポリシー設定
- `documentation/docs/content_06_developer-guide/05-configuration/authn/` - 認証方式別設定ガイド
  - `password.md`, `sms.md`, `email.md`, `fido2.md`, `fido-uaf.md`
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-01-authentication-policy.md` - 認証ポリシー概念
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-02-mfa.md` - MFA概念
- `documentation/docs/content_10_ai_developer/ai-41-authentication.md` - AI開発者向けガイド

## 機能概要

認証機能は、ユーザーの本人確認を行う層。
- **多様な認証方式**: Password, Email OTP, SMS OTP, FIDO2/WebAuthn, FIDO-UAF
- **条件付き認証**: scope/ACR/clientベースでポリシー切替
- **Step-up認証**: 高セキュリティ操作時の追加認証
- **MFA**: 多要素認証のオーケストレーション

## モジュール構成

```
libs/
├── idp-server-core/                         # 認証コア
│   └── .../openid/authentication/
│       ├── AuthenticationInteractor.java   # 認証Interactor IF
│       ├── AuthenticationTransaction.java  # 認証トランザクション
│       ├── AuthenticationTransactionCommandRepository.java
│       └── AuthenticationTransactionQueryRepository.java
│
├── idp-server-authentication-interactors/   # 認証Interactor実装
│   └── .../authentication/interactors/
│       ├── password/
│       │   └── PasswordAuthenticationInteractor.java
│       ├── sms/
│       │   └── SmsAuthenticationInteractor.java
│       ├── email/
│       │   └── EmailAuthenticationInteractor.java
│       ├── fido2/
│       │   ├── Fido2AuthenticationInteractor.java
│       │   └── Fido2RegistrationInteractor.java
│       ├── fidouaf/
│       │   └── FidoUafAuthenticationInteractor.java
│       └── ... (各認証方式の実装)
│
└── idp-server-control-plane/                # 管理API
    └── .../management/authentication/
        └── AuthenticationPolicyManagementApi.java
```

## 認証ポリシー設定

認証ポリシーは設定ベースで管理:

```java
public class AuthenticationConfiguration {
    String type;  // password, sms, email, fido2, fido_uaf, etc.
    Map<String, Object> payload;
    // 設定内容は type により異なる
}
```

## 認証Interactorパターン

`idp-server-core/openid/authentication/` 内:

```java
public interface AuthenticationInteractor {

    AuthenticationInteractionType type();

    String method();

    /**
     * 認証インタラクションを実行
     */
    AuthenticationInteractionRequestResult interact(
        Tenant tenant,
        AuthenticationTransaction transaction,
        AuthenticationInteractionType type,
        AuthenticationInteractionRequest request,
        RequestAttributes requestAttributes,
        UserQueryRepository userQueryRepository
    );
}
```

### パスワード認証実装例（概念的）

`idp-server-authentication-interactors/` モジュール内のInteractorは、
interact()メソッドを実装し、AuthenticationInteractionRequestResultを返します。

パスワード検証の概念:
- トランザクションとリクエストを受け取る
- ブルートフォースチェック（CacheStoreによるRedisカウンター）
- ユーザーリポジトリからユーザー情報を取得
- パスワードエンコーダーで検証
- 成功時にカウンターリセット
- 成功/失敗の結果をAuthenticationInteractionRequestResultで返却

詳細は `documentation/docs/content_06_developer-guide/05-configuration/authn/password.md` のブルートフォース対策セクションを参照。

## FIDO2/WebAuthn認証

`idp-server-webauthn4j-adapter/` モジュール内:

WebAuthn Assertion検証をwebauthn4jライブラリを使用して実行し、
公開鍵暗号方式により認証を実現します。

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── oidc_core_3_1_code.test.js           # Authorization Code Flow
│   ├── rfc6749_4_3_resource_owner_password_credentials.test.js  # パスワードグラント
│   └── ... (各OIDCフロー仕様テスト)
│
├── scenario/application/
│   ├── scenario-01-user-registration.test.js  # ユーザー登録
│   ├── scenario-03-mfa-registration.test.js   # MFA登録
│   └── scenario-04-ciba-mfa.test.js           # CIBA MFA
│
├── usecase/mfa/
│   ├── mfa-01-password-reset-email-auth.test.js
│   └── mfa-03-fido-uaf-device-registration-acr-policy.test.js
│
└── monkey/
    ├── password-authentication-monkey.test.js
    └── sms-authentication-monkey.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava
./gradlew :libs:idp-server-authentication-interactors:compileJava
./gradlew :libs:idp-server-webauthn4j-adapter:compileJava

# テスト
cd e2e && npm test -- spec/oidc_core_3_1_code.test.js
cd e2e && npm test -- scenario/application/scenario-03-mfa-registration.test.js
```

## トラブルシューティング

### 認証Interactorが見つからない
- `AuthenticationConfiguration.type` が正しいか確認
- 対応するInteractor実装が登録されているか確認

### MFA登録がブロックされる
- Pre-authentication: ユーザーが認証済みか確認
- ACR Policy: 現在のACRが要求レベルを満たすか確認

### 認証トランザクションが期限切れ
- `AuthenticationTransaction` の有効期限（デフォルト: 5分）を確認
- Redis等のセッションストレージが正常か確認
