---
name: device-credential
description: デバイスクレデンシャル（Device Credential）機能の開発・修正を行う際に使用。デバイスシークレット発行、JWT Bearer Grant、CIBAデバイス認証、セキュリティ実装時に役立つ。
---

# デバイスクレデンシャル開発ガイド

## ドキュメント

- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-10-device-credential.md` - デバイスクレデンシャル管理（概念）
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-09-jwt-bearer-grant.md` - JWT Bearer Grant
- `documentation/docs/content_05_how-to/phase-3-advanced/fido-uaf/01-ciba-flow.md` - CIBA + FIDO-UAFフロー
- `documentation/docs/content_05_how-to/phase-3-advanced/fido-uaf/02-registration.md` - FIDO-UAF登録（シークレット発行含む）
- `documentation/openapi/swagger-authentication-device-ja.yaml` - 認証デバイスAPI（OpenAPI仕様）

## 機能概要

デバイスクレデンシャルは、モバイルアプリがIdPサーバーと安全に通信するための認証情報です。

### 利用パターン

| パターン | 説明 | ユーザー操作 |
|---------|------|-------------|
| **CIBAフロー** | デバイスエンドポイント認証 + FIDO-UAF本人確認 | 必要（生体認証） |
| **JWT Bearer Grant** | アクセストークンを直接取得（RFC 7523） | 不要 |

### 主要機能

1. **デバイスシークレット自動発行**: FIDO-UAF登録時に`device_secret`を発行
2. **デバイスエンドポイント認証**: `device_secret_jwt`でAPIアクセスを認証
3. **JWT Bearer Grant**: デバイスシークレットでアクセストークンを直接取得

## テナントポリシー設定

`identity_policy_config.authentication_device_rule`:

```json
{
  "identity_policy_config": {
    "authentication_device_rule": {
      "max_devices": 5,
      "required_identity_verification": false,
      "authentication_type": "device_secret_jwt",
      "issue_device_secret": true,
      "device_secret_algorithm": "HS256",
      "device_secret_expires_in_seconds": 31536000
    }
  }
}
```

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| `authentication_type` | `device_secret_jwt`: JWT認証を要求 / `none`: 認証不要 | `none` |
| `issue_device_secret` | FIDO-UAF登録時にシークレットを自動発行 | `false` |
| `device_secret_algorithm` | 署名アルゴリズム（HS256/HS384/HS512） | `HS256` |
| `device_secret_expires_in_seconds` | 有効期限（秒）、null=無期限 | `null` |

## FIDO-UAF登録時の発行レスポンス

```json
{
  "status": "success",
  "device_id": "device_abc123",
  "device_secret": "base64url-encoded-random-secret",
  "device_secret_algorithm": "HS256",
  "device_secret_jwt_issuer": "device:device_abc123"
}
```

## JWT Bearer Grant設定

### クライアント設定

```json
{
  "grant_types": ["urn:ietf:params:oauth:grant-type:jwt-bearer"],
  "extension": {
    "available_federations": [
      {
        "issuer": "device",
        "type": "device",
        "jwt_bearer_grant_enabled": true
      }
    ]
  }
}
```

### JWT Assertion構造

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "iss": "device:{deviceId}",
  "sub": "{deviceId}",
  "aud": "https://idp.example.com/{tenantId}",
  "jti": "unique-token-id",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### ユーザー解決ロジック（subject_claim_mapping）

デバイスフェデレーションでは、JWTの`sub`クレームからユーザーを解決します。

| subject_claim_mapping | 動作 | デフォルト |
|----------------------|------|-----------|
| `device_id`（デフォルト） | `sub`をデバイスIDとして扱い、そのデバイスを所有するユーザーを検索 | デバイスフェデレーション |
| `sub` | `sub`をidp-serverのユーザーIDとして扱い、直接ユーザーを検索 | - |

**注意**: 外部IdPフェデレーションの場合、JWTの`sub`は**外部IdPでのユーザー識別子**であり、idp-serverのユーザーIDではありません。`findByExternalIdpSubject(tenant, subject, providerId)`で外部IdP連携されたユーザーを検索します。`providerId`はフェデレーション設定（`available_federations`）の`issuer`から取得されます。

**セキュリティ上の利点（device_id方式）**:
- クライアントがユーザーIDを知る必要がない
- デバイスシークレットが漏洩しても、そのデバイスの登録ユーザーとしてのみ認証可能
- 任意のユーザーになりすましが不可能

**関連ファイル**:
- `JwtBearerGrantService.java` - JWT Bearer Grant処理
- `JwtBearerUserFinder.java` - ユーザー解決ロジック

## セキュリティ考慮事項

### credential_payload の露出防止

`AuthenticationDevice.toMap()` は外部出力（Userinfo、ID Token、Access Token）に使用されます。
**credential_payload は含めてはいけません**（`secret_value`が含まれるため）。

```java
// AuthenticationDevice.java
public Map<String, Object> toMap() {
    // ... other fields ...
    // SECURITY: credential_payload is NOT included - it contains secret_value
    // SECURITY: credential_metadata is safe - only contains issued_at and expires_at
    if (hasCredentialMetadata()) map.put("credential_metadata", credentialMetadata);
    return map;
}
```

### 露出チェック対象

| 出力先 | credential_payload | 検証 |
|--------|-------------------|------|
| Userinfo | 除外必須 | E2Eテストで検証 |
| Access Token | 除外必須 | E2Eテストで検証 |
| ID Token | 除外必須 | E2Eテストで検証 |

### 認証トランザクションのレスポンス制御

デバイス認証の有無によって、認証トランザクションのレスポンスに含まれる情報が制御されます。

| 認証設定 | `context`フィールド | 説明 |
|---------|-------------------|------|
| `authentication_type: "none"` | 除外 | 認証なしでアクセス可能。機密情報は除外 |
| `authentication_type: "access_token"` | 含む | アクセストークン認証成功後のみ詳細情報を返却 |
| `authentication_type: "device_secret_jwt"` | 含む | 対称鍵JWT（HMAC）認証成功後のみ詳細情報を返却 |
| `authentication_type: "private_key_jwt"` | 含む | 非対称鍵JWT（RSA/EC）認証成功後のみ詳細情報を返却 |

**関連ファイル**:
- `AuthenticationRequest.toMapForPublic(boolean isDeviceAuthenticated)`
- `AuthenticationTransaction.toRequestMap(boolean isDeviceAuthenticated)`
- `DeviceEndpointAuthenticationHandler.verifyAndIsAuthenticated()`
- `AuthenticationTransactionEntryService.findList()`

## モジュール構成

```
libs/idp-server-core/
└── .../core/openid/identity/device/
    ├── AuthenticationDevice.java           # デバイスエンティティ
    ├── AuthenticationDevices.java          # デバイスコレクション
    ├── AuthenticationDeviceIdentifier.java # デバイスID値オブジェクト
    └── DeviceSecretIssuer.java             # シークレット発行

libs/idp-server-core/
└── .../core/openid/identity/
    └── AuthenticationDeviceRule.java       # テナントポリシー設定

libs/idp-server-core-extension-ciba/
└── .../extension/ciba/
    └── handler/                            # CIBAでのデバイス認証処理
```

## E2Eテスト

```
e2e/src/tests/usecase/device-credential/
├── device-credential-04-device-secret-issuance.test.js  # デバイスシークレット発行+セキュリティ検証
```

### セキュリティテストの検証項目

1. **Userinfo**: `credential_payload`が含まれていないこと
2. **Access Token**: `credential_payload`が含まれていないこと
3. **ID Token**: `credential_payload`が含まれていないこと
4. **secret_value**: 文字列が含まれていないこと
5. **実際のdeviceSecret値**: 含まれていないこと
6. **認証トランザクション（認証なし）**: `context`が含まれていないこと
7. **認証トランザクション（認証あり）**: `context`が含まれていること

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core:compileJava

# E2Eテスト
cd e2e && npm test -- usecase/device-credential/device-credential-04-device-secret-issuance.test.js
```

## 関連スキル

- `ciba` - CIBAフローでのデバイスシークレット認証
- `passwordless` - FIDO-UAF登録（シークレット発行トリガー）
- `authentication` - 認証ポリシー設定

## トラブルシューティング

### device_secretが発行されない
- テナントポリシーで`issue_device_secret: true`が設定されているか確認
- `device_secret_algorithm`が設定されているか確認

### デバイスエンドポイントで401エラー
- `authentication_type: "device_secret_jwt"`が設定されている場合、JWTが必要
- JWTの`iss`が`device:{deviceId}`形式になっているか確認
- JWTの署名が正しいか確認

### credential_payloadが露出している
- `AuthenticationDevice.toMap()`の実装を確認
- バックエンドを再ビルド・再デプロイ
