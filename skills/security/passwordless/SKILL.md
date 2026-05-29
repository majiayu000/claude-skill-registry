---
name: passwordless
description: パスワードレス認証（Passwordless Authentication）機能の開発・修正を行う際に使用。FIDO2/WebAuthn, Passkey, FIDO-UAF実装時に役立つ。
---

# パスワードレス認証（Passwordless Authentication）開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-07-passwordless.md` - パスワードレス認証概念
- `documentation/docs/content_06_developer-guide/05-configuration/authn/fido2.md` - FIDO2設定
- `documentation/docs/content_06_developer-guide/05-configuration/authn/fido-uaf.md` - FIDO-UAF設定

## 機能概要

パスワードレス認証は、パスワードを使わない認証方式。
- **FIDO2/WebAuthn**: W3C標準、Platform Authenticator（Face ID, Touch ID）、Roaming Authenticator（YubiKey）
- **Passkey**: クラウド同期可能な認証情報（iCloud Keychain, Google Password Manager）
- **FIDO-UAF**: モバイル生体認証（CIBA連携）
- **フィッシング耐性**: 公開鍵暗号方式

## モジュール構成

```
libs/
├── idp-server-webauthn4j-adapter/           # FIDO2/WebAuthn実装
│   └── .../webauthn4j/
│       ├── WebAuthn4jAuthenticationExecutor.java        # 認証実行
│       ├── WebAuthn4jAuthenticationManager.java         # 認証管理
│       ├── WebAuthn4jAuthenticationChallengeExecutor.java
│       ├── WebAuthn4jRegistrationExecutor.java          # 登録実行
│       ├── WebAuthn4jRegistrationManager.java           # 登録管理
│       ├── WebAuthn4jRegistrationChallengeExecutor.java
│       └── WebAuthn4jCredentialRepository.java
│
├── idp-server-authentication-interactors/   # FIDO-UAF実装
│   └── .../authentication/interactor/
│       └── FidoUafAuthenticationInteractor.java
│
└── idp-server-control-plane/                # 管理API
    └── .../management/passwordless/
        └── PasswordlessConfigManagementApi.java
```

## FIDO2/WebAuthn実装

`idp-server-webauthn4j-adapter/` モジュール内:

### WebAuthn4jAuthenticationExecutor

```java
public class WebAuthn4jAuthenticationExecutor
    implements AuthenticationExecutor {

    public Fido2ExecutorType type() {
        return new Fido2ExecutorType("webauthn4j");
    }

    @Override
    public String function() {
        return "webauthn4j_authentication";
    }

    @Override
    public AuthenticationExecutionResult execute(
        Tenant tenant,
        AuthenticationTransactionIdentifier identifier,
        AuthenticationExecutionRequest request,
        RequestAttributes requestAttributes,
        AuthenticationExecutionConfig configuration
    ) {
        // WebAuthn Assertion検証
        // webauthn4jライブラリを使用して公開鍵検証
        // ...
    }
}
```

**注意**: WebAuthn4jは、AuthenticationInteractorではなくAuthenticationExecutorインターフェースを実装します。

### WebAuthn4j主要クラス

| クラス | 役割 |
|--------|------|
| `WebAuthn4jAuthenticationExecutor` | 認証実行 |
| `WebAuthn4jAuthenticationManager` | 認証管理 |
| `WebAuthn4jAuthenticationChallengeExecutor` | Challenge生成 |
| `WebAuthn4jRegistrationExecutor` | 登録実行 |
| `WebAuthn4jRegistrationManager` | 登録管理 |
| `WebAuthn4jRegistrationChallengeExecutor` | 登録Challenge生成 |

## Passkey（クラウド同期）

Passkeyは、FIDO2/WebAuthnの一種で、Resident Key必須:
- ResidentKeyRequirement.REQUIRED設定
- クラウド同期（iCloud Keychain, Google Password Manager）

## FIDO-UAF（モバイル生体認証）

`idp-server-authentication-interactors/` モジュール内:

FIDO-UAFは、モバイルデバイスでの生体認証（指紋、顔認証）を実現します。

### デバイスシークレット自動発行

FIDO-UAF登録時にテナントポリシーに基づいてデバイスシークレットを自動発行できます。

**関連クラス**:
- `DeviceSecretIssuer.java` - シークレット発行ロジック
- `AuthenticationDeviceRule.java` - テナントポリシー設定
- `FidoUafRegistrationInteractor.java` - FIDO-UAF登録インターアクター

**テナントポリシー設定例**:
```json
{
  "identity_policy_config": {
    "authentication_device_rule": {
      "issue_device_secret": true,
      "device_secret_algorithm": "HS256"
    }
  }
}
```

**詳細**: [デバイスクレデンシャル管理](../../documentation/docs/content_03_concepts/03-authentication-authorization/concept-10-device-credential.md)

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   └── (WebAuthn/FIDO2関連仕様テスト)
│
├── scenario/application/
│   └── (パスワードレス認証シナリオ)
│
├── usecase/mfa/
│   └── mfa-03-fido-uaf-device-registration-acr-policy.test.js
│
└── usecase/device-credential/
    └── device-credential-04-device-secret-issuance.test.js  # デバイスシークレット自動発行
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-webauthn4j-adapter:compileJava
./gradlew :libs:idp-server-authentication-interactors:compileJava

# テスト
cd e2e && npm test -- usecase/mfa/mfa-03-fido-uaf-device-registration-acr-policy.test.js
```

## トラブルシューティング

### FIDO2登録失敗
- RP ID設定を確認（ドメイン名と一致）
- HTTPS必須（localhost除く）
- ブラウザがWebAuthn APIをサポートしているか確認

### Challenge検証失敗
- Challengeの有効期限（5分）を確認
- Challenge保存・取得が正しく動作しているか確認

### Passkey同期されない
- ResidentKeyRequirement.REQUIRED設定を確認
- ブラウザ/OSのPasskey設定を確認（iCloud Keychain, Google Password Manager）
