---
name: operations
description: 運用・監視（Operations & Monitoring）機能の開発・修正を行う際に使用。監査ログ、テナント統計、期限切れデータ削除実装時に役立つ。
---

# 運用・監視（Operations & Monitoring）開発ガイド

## ドキュメント

- `documentation/docs/content_08_ops/` - 運用ガイド
- `documentation/docs/content_03_concepts/07-operations/` - 運用概念

## 機能概要

運用・監視機能は、システムの健全性維持・問題調査を行う層。
- **監査ログ（AuditLog）**: 管理API操作記録
- **セキュリティイベント（SecurityEvent）**: ユーザー操作記録
- **テナント統計**: DAU/MAU/YAU

## モジュール構成

```
libs/
├── idp-server-platform/                     # プラットフォーム基盤
│   ├── audit/
│   │   └── AuditLog.java                   # 監査ログ
│   └── statistics/
│       └── TenantStatistics.java           # テナント統計
│
├── idp-server-springboot-adapter/           # Spring Boot統合
│   └── .../adapters/springboot/application/event/
│       └── SecurityEventPublisherService.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/operations/
        └── OperationsManagementApi.java
```

## AuditLog構造

`idp-server-platform/audit/AuditLog.java` 内の実際の構造:

```java
public class AuditLog {
    String id;
    String type;
    String description;
    String tenantId;
    String clientId;
    String userId;
    String externalUserId;
    JsonNodeWrapper userPayload;
    String targetResource;
    String targetResourceAction;
    JsonNodeWrapper request;
    JsonNodeWrapper before;
    JsonNodeWrapper after;
    String outcomeResult;
    String outcomeReason;
    String targetTenantId;
    String ipAddress;
    String userAgent;
    JsonNodeWrapper attributes;
    boolean dryRun;
    LocalDateTime createdAt;
}
```

**注意**: AuditLogは`idp-server-platform`モジュールに配置されています（`idp-server-core`ではありません）。

## TenantStatistics

`idp-server-platform/statistics/` 内:

テナント別の統計情報（DAU/MAU/YAU、ログイン数、トークン発行数等）を管理します。

## SecurityEventPublisher

`idp-server-springboot-adapter/` および `idp-server-platform/` 内:

- `SecurityEventPublisherService` - Spring Boot統合版
- `SecurityEventPublisher` - プラットフォーム版

## E2Eテスト

```
e2e/src/tests/
├── scenario/control_plane/organization/
│   └── (監査ログ関連テスト)
│
└── usecase/standard/
    └── standard-01-onboarding-and-audit.test.js  # 監査ログテスト
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-platform:compileJava

# テスト
cd e2e && npm test -- usecase/standard/standard-01-onboarding-and-audit.test.js

# ヘルスチェック
curl http://localhost:8080/actuator/health
```

## トラブルシューティング

### 監査ログが記録されない
- AuditLog保存が成功しているか確認
- Repository実装が正しいか確認

### テナント統計が更新されない
- SecurityEventが正しく発行されているか確認
- StatisticsCollectorが動作しているか確認
