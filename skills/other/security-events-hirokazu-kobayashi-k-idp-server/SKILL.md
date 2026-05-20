---
name: security-events
description: セキュリティイベント・フック（Security Events & Hooks）機能の開発・修正を行う際に使用。イベント通知、Slack/Email/Webhook/SSF連携実装時に役立つ。
---

# セキュリティイベント・フック（Security Events & Hooks）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/03-application-plane/09-security-event.md` - セキュリティイベント実装ガイド
- `documentation/docs/content_06_developer-guide/05-configuration/security-event-hook.md` - セキュリティイベントフック設定
- `documentation/docs/content_03_concepts/06-security-extensions/concept-01-security-events.md` - セキュリティイベント概念
- `documentation/docs/content_10_ai_developer/ai-54-security-event-framework.md` - AI開発者向けガイド

## 機能概要

セキュリティイベント機能は、ユーザー操作やシステムイベントを記録・通知する層。
- **イベントタイプ**: 認証、ユーザーライフサイクル、トークン、認可
- **フック**: Slack, Email, Webhook, SSF
- **フィルタリング**: イベントタイプ別トリガー設定

## モジュール構成

```
libs/
├── idp-server-platform/                     # プラットフォーム基盤
│   └── .../security/
│       └── SecurityEventPublisher.java     # イベント発行
│
├── idp-server-springboot-adapter/           # Spring Boot統合
│   └── .../adapters/springboot/application/event/
│       └── SecurityEventPublisherService.java
│
├── idp-server-security-event-framework/     # イベントフレームワーク
│   └── .../security/event/
│       └── (SSF関連クラス群)
│
├── idp-server-security-event-hooks/         # フック実装
│   └── .../security/event/hook/
│       ├── SsfHookExecutor.java
│       ├── WebHookSecurityEventExecutor.java
│       └── SlackSecurityEventHookExecutor.java
│
└── idp-server-control-plane/                # 管理API
    └── .../management/event/
        └── SecurityEventManagementApi.java
```

**注意**: 統一されたEventHookExecutorインターフェースではなく、各フックタイプごとに個別のExecutorクラスが存在します。

## イベント発行

`idp-server-platform/security/` および `idp-server-springboot-adapter/` 内:

- `SecurityEventPublisher` - プラットフォーム版
- `SecurityEventPublisherService` - Spring Boot統合版

## フック種類

| Executor | 役割 |
|----------|------|
| `SsfHookExecutor` | SSF (Shared Signals Framework) 通知 |
| `WebHookSecurityEventExecutor` | Webhook通知 |
| `SlackSecurityEventHookExecutor` | Slack通知 |

## フック設定

```json
{
  "hook_id": "uuid",
  "name": "Login Success Notification",
  "enabled": true,
  "hook_type": "slack",
  "trigger": {
    "event_types": [
      "PASSWORD_AUTH_SUCCESS",
      "FIDO2_AUTH_SUCCESS"
    ]
  },
  "config": {
    "webhook_url": "https://hooks.slack.com/services/xxx/yyy/zzz",
    "channel": "#security-alerts"
  }
}
```

## E2Eテスト

```
e2e/src/tests/
├── scenario/control_plane/organization/
│   └── organization_security_event_hook_management.test.js
│
└── usecase/
    ├── standard/standard-02-minimal-client-security-event.test.js
    ├── advance/advance-01-federation-security-event-user-name.test.js
    └── ciba/ciba-04-security-event-device-ids.test.js
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-security-event-framework:compileJava
./gradlew :libs:idp-server-security-event-hooks:compileJava

# テスト
cd e2e && npm test -- scenario/control_plane/organization/organization_security_event_hook_management.test.js
```

## トラブルシューティング

### フックが実行されない
- `enabled: true`か確認
- `trigger.event_types`にイベントタイプが含まれているか確認

### Slack通知が届かない
- Webhook URLが正しいか確認
- 対応するExecutor（SlackSecurityEventHookExecutor）が登録されているか確認
