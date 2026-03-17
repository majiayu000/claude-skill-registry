---
name: ciba
description: CIBA（Client Initiated Backchannel Authentication）機能の開発・修正を行う際に使用。Poll/Push/Pingモード、Login Hint解決、FCM通知実装時に役立つ。
---

# CIBA（Client Initiated Backchannel Authentication）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/06-ciba-flow.md` - CIBA実装ガイド
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-04-authorization.md` - 認可概念（CIBA含む）
- `documentation/docs/content_10_ai_developer/ai-31-extension-ciba.md` - AI開発者向けCIBAガイド

## 機能概要

CIBAは、クライアントがバックチャネル経由でユーザー認証を要求するフロー。
- **3つのモード**: Poll（ポーリング）、Push（通知）、Ping（通知+ポーリング）
- **Login Hint解決**: sub:, email:, phone:, device: プレフィックスでユーザー特定
- **Binding Message**: ユーザーへの確認メッセージ表示
- **ID Token Hint**: 既存ID Tokenでユーザー特定
- **User Code**: ユーザー入力コードによる認証
- **デバイス通知**: FCM push通知
- **デバイスシークレット認証**: device_secret_jwtによるデバイスエンドポイント認証

## デバイスシークレット認証（CIBAフロー）

CIBAフローでモバイルアプリがデバイスエンドポイントにアクセスする際、デバイスシークレットJWTによる認証を要求できます。

### 設定（テナントポリシー）

```json
{
  "identity_policy_config": {
    "authentication_device_rule": {
      "authentication_type": "device_secret_jwt",
      "issue_device_secret": true,
      "device_secret_algorithm": "HS256"
    }
  }
}
```

### フロー

1. **FIDO-UAF登録時**: `device_secret`が自動発行される
2. **CIBAリクエスト**: `login_hint=device:{deviceId}`でデバイス指定
3. **デバイスエンドポイントアクセス**: `Authorization: Bearer {device_secret_jwt}`で認証
4. **FIDO-UAF認証**: 生体認証で本人確認

### 関連ドキュメント

- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-10-device-credential.md` - デバイスクレデンシャル管理（詳細）

### 関連E2Eテスト

- `e2e/src/tests/usecase/device-credential/device-credential-04-device-secret-issuance.test.js` - デバイスシークレット発行+CIBA認証

## モジュール構成

```
libs/
├── idp-server-core-extension-ciba/          # CIBA拡張モジュール
│   └── .../core/extension/ciba/
│       ├── handler/
│       │   └── CibaRequestHandler.java     # CIBA認証リクエスト処理
│       ├── CibaRequestContext.java         # CIBAリクエストコンテキスト
│       ├── grant/
│       │   ├── CibaGrant.java
│       │   ├── CibaGrantFactory.java
│       │   └── CibaGrantService.java       # CIBAグラント管理
│       ├── request/
│       │   └── BackchannelAuthenticationRequest.java
│       ├── response/
│       │   └── BackchannelAuthenticationResponse.java
│       └── repository/
│           └── CibaGrantRepository.java
│
├── idp-server-notification-fcm-adapter/      # FCM通知アダプター
│   └── .../notification/fcm/
│       └── FcmNotificationSender.java
│
└── idp-server-control-plane/                # 管理API
    └── .../management/ciba/
        └── CibaConfigManagementApi.java
```

## CIBA認証リクエスト処理

`idp-server-core-extension-ciba/.../core/extension/ciba/handler/CibaRequestHandler.java` 内:

CibaRequestHandlerは、BackchannelAuthenticationRequestを処理し、
BackchannelAuthenticationResponseを生成します。

処理フロー（概念的）:
1. クライアント認証
2. Login Hint解決（ユーザー特定）
3. auth_req_id生成
4. CibaGrant作成・保存
5. デバイス通知（FCM）
6. BackchannelAuthenticationResponse返却

## CIBAグラント管理

`idp-server-core-extension-ciba/grant/` 内:

```java
// CibaGrantは認証状態を管理
public class CibaGrant {
    AuthReqId authReqId;
    UserId userId;
    ClientId clientId;
    Scope scope;
    GrantStatus status;  // PENDING, AUTHENTICATED, EXPIRED

    public boolean isAuthenticated() {
        return status == GrantStatus.AUTHENTICATED;
    }
}
```

CibaGrantServiceとCibaGrantVerifierが、グラントのライフサイクルを管理します。

## FCM通知

`idp-server-notification-fcm-adapter/` モジュール内:

FCM (Firebase Cloud Messaging)を使用して、認証デバイスに通知を送信します。

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── ciba_authentication_request.test.js   # CIBA認証リクエスト
│   ├── ciba_token_request.test.js            # CIBAトークンリクエスト
│   ├── ciba_push.test.js                     # Pushモード
│   ├── ciba_ping.test.js                     # Pingモード
│   └── ciba_discovery.test.js                # CIBA Discovery
│
├── scenario/application/
│   └── scenario-04-ciba-mfa.test.js          # CIBA MFAシナリオ
│
├── usecase/ciba/
│   ├── ciba-01-require-rar.test.js           # RAR必須
│   ├── ciba-02-multi-device-priority.test.js # マルチデバイス優先度
│   └── ciba-04-security-event-device-ids.test.js
│
└── monkey/
    └── ciba-monkey.test.js                   # CIBAファジングテスト
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-extension-ciba:compileJava
./gradlew :libs:idp-server-notification-fcm-adapter:compileJava

# テスト
cd e2e && npm test -- spec/ciba_authentication_request.test.js
cd e2e && npm test -- spec/ciba_push.test.js
cd e2e && npm test -- usecase/ciba/
```

## トラブルシューティング

### Login Hint解決失敗
- プレフィックス（sub:, email:, phone:）が正しいか確認
- ユーザーが存在するか確認

### Pollモードでauthorization_pending
- ユーザーがまだ認証を完了していない（正常動作）
- `interval`秒待ってから再ポーリング

### FCM通知が届かない
- FCMトークンが登録されているか確認
- Firebase設定（credentials.json）が正しいか確認
- `idp-server-notification-fcm-adapter` モジュールが有効か確認
