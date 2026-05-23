---
name: fido2
description: FIDO2/WebAuthn/パスキー関連の実装・設定・ドキュメント・テストを扱う時に使用。パスキー登録、認証、管理、アテステーション検証に関する作業で自動的に呼び出される。
argument-hint: [作業内容の説明]
---

# FIDO2/WebAuthn コンテキスト

idp-serverにおけるFIDO2/WebAuthn/パスキー実装のコンテキスト情報。

## アーキテクチャ概要

```
クライアント (sample-web)
    │
    ├── navigator.credentials.create() / get()
    │
    ▼
idp-server (認可フロー内)
    │
    ├── WebAuthn4jRegistrationManager (登録)
    ├── WebAuthn4jAuthenticationManager (認証)
    │
    ▼
WebAuthn4j ライブラリ (内部統合)
```

**重要**: 外部FIDO2サーバーではなく、WebAuthn4jライブラリを内部統合。

## 主要ファイル

### 実装 (Java)

| ファイル | 役割 |
|---------|------|
| `libs/idp-server-webauthn4j-adapter/.../WebAuthn4jRegistrationManager.java` | 登録処理・アテステーション検証 |
| `libs/idp-server-webauthn4j-adapter/.../WebAuthn4jAuthenticationManager.java` | 認証処理・署名検証 |
| `libs/idp-server-webauthn4j-adapter/.../WebAuthn4jConfiguration.java` | 設定パース |
| `libs/idp-server-webauthn4j-adapter/.../WebAuthn4jManagerFactory.java` | Manager生成 |

### ドキュメント (How-to)

| ファイル | 内容 |
|---------|------|
| `documentation/.../fido2/01-registration.md` | パスキー登録設定 |
| `documentation/.../fido2/02-authentication.md` | パスキー認証設定 |
| `documentation/.../fido2/03-management.md` | パスキー管理API |
| `documentation/.../fido2/04-attestation-verification.md` | アテステーション検証 |

### E2Eテスト

| ファイル | 内容 |
|---------|------|
| `e2e/src/tests/usecase/mfa/mfa-05-fido2.test.js` | FIDO2基本フロー |
| `e2e/src/tests/usecase/mfa/mfa-06-fido2-attestation-verification.test.js` | アテステーション検証 |
| `e2e/src/lib/fido/fido2.js` | テスト用FIDO2ヘルパー |

### サンプルアプリ

| ファイル | 内容 |
|---------|------|
| `sample-web/src/components/PasskeyRegistration.tsx` | 登録UI |
| `sample-web/src/components/PasskeyAuthentication.tsx` | 認証UI |
| `sample-web/src/components/UserInfo.tsx` | デバイス一覧表示 |

## WebAuthn4j関数マッピング

| interaction | function | 用途 |
|-------------|----------|------|
| `fido2-registration-challenge` | `webauthn4j_registration_challenge` | 登録チャレンジ発行 |
| `fido2-registration` | `webauthn4j_registration` | 登録完了・検証 |
| `fido2-authentication-challenge` | `webauthn4j_authentication_challenge` | 認証チャレンジ発行 |
| `fido2-authentication` | `webauthn4j_authentication` | 認証完了・検証 |

## 設定パラメータ

### 基本設定

```json
{
  "rp_id": "example.com",
  "origin": "https://example.com",
  "rp_name": "My Service",
  "require_resident_key": true,
  "user_verification_required": true
}
```

### アテステーション検証

| モード | 設定 | 用途 |
|--------|------|------|
| なし | `attestation_preference: "none"` | 開発・一般向け |
| TrustStore | `trust_store_path: "/path/to/truststore.p12"` | 特定ベンダー限定 |
| FIDO MDS | `mds.enabled: true` | 本番・高セキュリティ |

### 複数Origin対応

```json
{
  "rp_id": "example.com",
  "allowed_origins": [
    "https://app.example.com",
    "https://www.example.com"
  ]
}
```

## 認証ポリシー設定例

```json
{
  "success_conditions": {
    "any_of": [
      [{ "path": "$.password-authentication.success_count", "operation": "gte", "value": 1 }],
      [{ "path": "$.fido2-authentication.success_count", "operation": "gte", "value": 1 }]
    ]
  }
}
```

## パスキー一覧取得

パスキー一覧は **ID Token / Userinfo の `authentication_devices` クレーム** から取得。

### 前提設定

1. 認可サーバー: `custom_claims_scope_mapping: true`
2. クライアント: `scope: "openid claims:authentication_devices"`
3. 認可リクエスト: `scope=openid+claims:authentication_devices`

## よくある作業パターン

### 新機能追加

1. `WebAuthn4j*Manager.java` に処理追加
2. `WebAuthn4jConfiguration.java` に設定追加
3. E2Eテスト追加
4. ドキュメント更新

### 設定変更

1. `04-attestation-verification.md` で設定例確認
2. `WebAuthn4jConfiguration.java` でパース確認
3. E2Eテストで動作確認

$ARGUMENTS
