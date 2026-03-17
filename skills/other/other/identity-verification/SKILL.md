---
name: identity-verification
description: 身元確認（Identity Verification/IDA）機能の開発・修正を行う際に使用。eKYC連携、本人確認フロー、設定管理APIの実装時に役立つ。
---

# 身元確認（Identity Verification）機能 開発ガイド

## ドキュメント

詳細なドキュメントは以下を参照：
- `documentation/docs/content_05_how-to/phase-4-extensions/identity-verification/`
  - `01-guide.md` - ガイド
  - `02-application.md` - アプリケーション詳細
  - `03-registration.md` - 登録

## 機能概要

身元確認機能（IDA: Identity Assurance）は、外部サービスと連携してユーザーの本人確認を行う機能。
eKYCサービス、本人確認書類のOCR、顔認証などの外部APIと連携し、身元確認フローを実行する。

## モジュール構成

```
libs/
├── idp-server-core-extension-ida/     # 身元確認コアロジック
│   └── .../identity/verification/
│       ├── configuration/             # 設定クラス
│       │   ├── IdentityVerificationConfiguration.java
│       │   └── process/               # プロセス設定
│       ├── application/               # アプリケーション実行
│       │   └── execution/             # 外部API実行
│       ├── io/                        # 入出力
│       └── repository/                # リポジトリIF
│
├── idp-server-control-plane/          # 管理API
│   └── .../management/identity/verification/
│       ├── *ManagementApi.java
│       └── handler/
│
└── idp-server-core-adapter/           # DB実装
    └── .../identity/verification/
        ├── config/
        ├── application/
        └── result/
```

## 設定構造（JSON）

```json
{
  "id": "uuid",
  "type": "ekyc_type",
  "enabled": true,
  "attributes": {},
  "common": {
    "auth_type": "oauth|hmac|basic"
  },
  "processes": {
    "process_name": {
      "request": { "request_schema": {} },
      "pre_hook": {},
      "execution": { "http_request": {}, "mock": {} },
      "post_hook": {},
      "transition": { "approved": {}, "rejected": {} },
      "store": { "application_details_mapping_rules": [] },
      "response": { "body_mapping_rules": [] }
    }
  }
}
```

## 処理フロー

```
[リクエスト] → [request] スキーマ検証
            → [pre_hook] 事前処理
            → [execution] 外部API実行
            → [post_hook] 事後処理
            → [transition] 状態遷移
            → [store] 結果保存（mapping_rules）
            → [response] レスポンス生成
```

## 主要クラス

| クラス | 役割 |
|-------|------|
| `IdentityVerificationConfiguration` | メイン設定 |
| `IdentityVerificationProcessConfiguration` | プロセス設定 |
| `IdentityVerificationStoreConfig` | 結果保存設定 |
| `IdentityVerificationResponseConfig` | レスポンス設定 |
| `IdentityVerificationApplicationHandler` | アプリケーションハンドラー |
| `IdentityVerificationConfigManagementHandler` | 設定管理ハンドラー |

## API規約

APIレスポンスのJSONキーは**snake_case**を使用：
- `body_mapping_rules` (NOT `bodyMappingRules`)
- `application_details_mapping_rules`
- `pre_hook`, `post_hook`, `http_request`

`toMap()`メソッドのキー名は必ずsnake_caseで出力すること。

## E2Eテスト

```
e2e/src/tests/
├── integration/ida/                   # 統合テスト
│   ├── integration-01-identity_verification-condition.test.js
│   ├── integration-02-identity-verification-retry.test.js
│   └── ...
└── scenario/control_plane/organization/
    └── organization_identity_verification_config_management*.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-extension-ida:compileJava

# テスト
cd e2e && npm test -- --grep "identity.*verification"
```
